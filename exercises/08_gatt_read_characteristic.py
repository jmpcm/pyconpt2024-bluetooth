import asyncio

from bleak import BleakClient, BleakScanner
from bleak.backends.characteristic import BleakGATTCharacteristic
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData

ENVIRONMENTAL_SENSING_UUID = "0000181a-0000-1000-8000-00805f9b34fb"
MANUFACTURER_NAME_CHAR_UUID = "00002a29-0000-1000-8000-00805f9b34fb"
MODEL_NUMBER_CHAR_UUID = "00002a24-0000-1000-8000-00805f9b34fb"
SERIAL_NUMBER_CHAR_UUID = "00002a25-0000-1000-8000-00805f9b34fb"

discovered_device: BLEDevice = None


def discovery_callback(device: BLEDevice, advertisement_data: AdvertisementData) -> None:
    print(f"Peripheral {device.name} ({device.address}) "
          f"with service {advertisement_data.service_uuids} found!")
    global discovered_device  # noqa: PLW0603
    discovered_device = device


def disconnected_clbk(client: BleakClient) -> None:
    print(f"Disconnected from {client.address}")


async def main() -> None:
    scanner = BleakScanner()

    while discovered_device is None:
        await scanner.discover(detection_callback=discovery_callback,
                               service_uuids=[ENVIRONMENTAL_SENSING_UUID])
        if discovered_device is None:
            print("No devices with environmental sensing service found")

    async with BleakClient(discovered_device,
                           disconnected_callback=disconnected_clbk) as client:
        print(f"Connected to {discovered_device}")

        # for _, char in client.services.characteristics.items():
        #     value = await client.read_gatt_char(char)
        #     print(f"{char.description} = {value.decode('utf-8')}")

        for char_uuid in (MANUFACTURER_NAME_CHAR_UUID,
                          MODEL_NUMBER_CHAR_UUID,
                          SERIAL_NUMBER_CHAR_UUID):
            char = client.services.get_characteristic(char_uuid)
            value = await client.read_gatt_char(char)
            print(f"{char.description} = {value.decode('utf-8')}")


asyncio.run(main())
