# This example demonstrates a simple temperature sensor peripheral.
#
# The sensor's local value is updated, and it will notify
# any connected central every 10 seconds.

import bluetooth
import random
import struct
import time
import machine
import ubinascii
from ble_advertising import advertising_payload
from micropython import const
from machine import Pin

_IRQ_CENTRAL_CONNECT = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)
_IRQ_GATTS_INDICATE_DONE = const(20)
_IRQ_GATTS_READ_REQUEST = const(4)


_FLAG_READ = const(0x0002)
_FLAG_NOTIFY = const(0x0010)
_FLAG_INDICATE = const(0x0020)

# org.bluetooth.service.environmental_sensing
_ENV_SENSE_UUID = bluetooth.UUID(0x181A)
# org.bluetooth.characteristic.temperature
_TEMP_CHAR = (bluetooth.UUID(0x2A6E),
              _FLAG_READ | _FLAG_NOTIFY | _FLAG_INDICATE, )
_ENV_SENSE_SERVICE = (
    _ENV_SENSE_UUID,
    (_TEMP_CHAR,),
)

_DEVICE_INFO_UUID = bluetooth.UUID(0x180A)
# org.bluetooth.characteristic.manufacturer_name
_MANUFACTURER_NAME_CHAR = (bluetooth.UUID(0x2A29), _FLAG_READ)
# org.bluetooth.characteristic.model_number
_MODEL_NUMBER_CHAR = (bluetooth.UUID(0x2A24), _FLAG_READ)
# org.bluetooth.characteristic.serial_number
_SERIAL_NUMBER_CHAR = (bluetooth.UUID(0x2A25), _FLAG_READ)
_DEVICE_INFO_SERVICE = (
    _DEVICE_INFO_UUID,
    (_MANUFACTURER_NAME_CHAR, _MODEL_NUMBER_CHAR, _SERIAL_NUMBER_CHAR)
)

SERVICES = (_DEVICE_INFO_SERVICE, _ENV_SENSE_SERVICE)

# org.bluetooth.characteristic.gap.appearance.xml
_ADV_APPEARANCE_GENERIC_THERMOMETER = const(768)


class BLEDevice:
    def __init__(self, ble, name=""):
        self._sensor_temp = machine.ADC(4)
        self._ble = ble
        self._ble.active(True)
        
        self._ble.irq(self._irq)
        (
            (self._manufacturer, self._model, self._serial),
            (self._handle,),
        ) = self._ble.gatts_register_services(SERVICES)
        self._ble.gatts_write(self._manufacturer,"PyconTemperatureSensor")
        self._ble.gatts_write(self._model,"FANTASTIC.2024")
        self._ble.gatts_write(self._serial,"2024.10.19")
        
        self._connections = set()
        if len(name) == 0:
            name = 'Pico %s' % ubinascii.hexlify(
                self._ble.config('mac')[1], ':').decode().upper()
        print('Sensor name %s' % name)
        self._payload = advertising_payload(
            name=name, services=[_ENV_SENSE_UUID]
        )
        self._advertise()

    def _irq(self, event, data):
        # Track connections so we can send notifications.
        if event == _IRQ_CENTRAL_CONNECT:
            conn_handle, _, _ = data
            self._connections.add(conn_handle)
        elif event == _IRQ_CENTRAL_DISCONNECT:
            conn_handle, _, _ = data
            self._connections.remove(conn_handle)
            # Start advertising again to allow a new connection.
            self._advertise()
        elif event == _IRQ_GATTS_INDICATE_DONE:
            conn_handle, value_handle, status = data
        # elif event == _IRQ_GATTS_READ_REQUEST:
        #     conn_handle, attr_handle = data
        #     # print("attr_handle = " % str(type(attr_handle)))
        #     # gatt_read_manufacturer = self._ble.gatts_read(self._manufacturer)
        #     # print(gatt_read_manufacturer)

    def update_temperature(self, notify=False, indicate=False):
        # Write the local value, ready for a central to read.
        temp_deg_c = self._get_temp()
        print("write temp %.2f degc" % temp_deg_c)
        self._ble.gatts_write(self._handle, struct.pack(
            "<h", int(temp_deg_c * 100)))
        if notify or indicate:
            for conn_handle in self._connections:
                if notify:
                    # Notify connected centrals.
                    self._ble.gatts_notify(conn_handle, self._handle)
                if indicate:
                    # Indicate connected centrals.
                    self._ble.gatts_indicate(conn_handle, self._handle)

    def _advertise(self, interval_us=100000):
        self._ble.gap_advertise(interval_us, adv_data=self._payload)

    # ref https://github.com/raspberrypi/pico-micropython-examples/blob/master/adc/temperature.py
    def _get_temp(self):
        conversion_factor = 3.3 / (65535)
        reading = self._sensor_temp.read_u16() * conversion_factor

        # The temperature sensor measures the Vbe voltage of a biased bipolar diode, connected to the fifth ADC channel
        # Typically, Vbe = 0.706V at 27 degrees C, with a slope of -1.721mV (0.001721) per degree.
        return 27 - (reading - 0.706) / 0.001721


# class BLETemperature:
#     def __init__(self, ble, name=""):
#         self._sensor_temp = machine.ADC(4)
#         self._ble = ble
#         self._ble.active(True)
#         self._ble.irq(self._irq)
#         ((self._handle,),) = self._ble.gatts_register_services((_ENV_SENSE_SERVICE,))
#         self._connections = set()

#         if len(name) == 0:
#             name = 'Pico %s' % ubinascii.hexlify(
#                 self._ble.config('mac')[1], ':').decode().upper()
#         print('Sensor name %s' % name)
#         self._payload = advertising_payload(
#             name=name, services=[_ENV_SENSE_UUID]
#         )
#         self._advertise()

#     def _irq(self, event, data):
#         # Track connections so we can send notifications.
#         if event == _IRQ_CENTRAL_CONNECT:
#             conn_handle, _, _ = data
#             self._connections.add(conn_handle)
#         elif event == _IRQ_CENTRAL_DISCONNECT:
#             conn_handle, _, _ = data
#             self._connections.remove(conn_handle)
#             # Start advertising again to allow a new connection.
#             self._advertise()
#         elif event == _IRQ_GATTS_INDICATE_DONE:
#             conn_handle, value_handle, status = data

#     def update_temperature(self, notify=False, indicate=False):
#         # Write the local value, ready for a central to read.
#         temp_deg_c = self._get_temp()
#         print("write temp %.2f degc" % temp_deg_c)
#         self._ble.gatts_write(self._handle, struct.pack(
#             "<h", int(temp_deg_c * 100)))
#         if notify or indicate:
#             for conn_handle in self._connections:
#                 if notify:
#                     # Notify connected centrals.
#                     self._ble.gatts_notify(conn_handle, self._handle)
#                 if indicate:
#                     # Indicate connected centrals.
#                     self._ble.gatts_indicate(conn_handle, self._handle)

#     def _advertise(self, interval_us=100000):
#         self._ble.gap_advertise(interval_us, adv_data=self._payload)

#     # ref https://github.com/raspberrypi/pico-micropython-examples/blob/master/adc/temperature.py
#     def _get_temp(self):
#         conversion_factor = 3.3 / (65535)
#         reading = self._sensor_temp.read_u16() * conversion_factor

#         # The temperature sensor measures the Vbe voltage of a biased bipolar diode, connected to the fifth ADC channel
#         # Typically, Vbe = 0.706V at 27 degrees C, with a slope of -1.721mV (0.001721) per degree.
#         return 27 - (reading - 0.706) / 0.001721


def demo():
    ble = bluetooth.BLE()
    # temp = BLETemperature(ble)
    temp = BLEDevice(ble)
    # counter = 0
    led = Pin('LED', Pin.OUT)

    while True:
        # if counter % 10 == 0:
        temp.update_temperature(notify=True, indicate=False)
        led.toggle()
        time.sleep_ms(1000)
        # counter += 1


if __name__ == "__main__":
    demo()
