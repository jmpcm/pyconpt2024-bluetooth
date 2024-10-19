import asyncio

from bleak import BleakClient, BleakScanner
from bleak.backends.characteristic import BleakGATTCharacteristic
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData

ENVIRONMENTAL_SENSING_UUID = "0000181a-0000-1000-8000-00805f9b34fb"
ENVIRONMENTAL_SENSING_TEMPERATURE_UUID = "00002a6e-0000-1000-8000-00805f9b34fb"

discovered_device: BLEDevice = None


def discovery_callback(device: BLEDevice, advertisement_data: AdvertisementData) -> None:
    print(f"Peripheral {device.name} ({device.address}) "
          f"with service {advertisement_data.service_uuids} found!")
    global discovered_device  # noqa: PLW0603
    discovered_device = device


def disconnected_clbk(client: BleakClient) -> None:
    print(f"Disconnected from {client.address}")


def notification_handler(characteristic: BleakGATTCharacteristic, data: bytearray) -> None:
    # print(f"{characteristic.description}: {data.hex()}")
    print(f"data received: {''.join(f'0x{d:02x} ' for d in data)}")
    print(f"{characteristic.description} = "
          f"{int.from_bytes(data, byteorder='little', signed=True) / 100}")


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

        char = client.services.get_characteristic(
            ENVIRONMENTAL_SENSING_TEMPERATURE_UUID)
        await client.start_notify(char, notification_handler)
        await asyncio.sleep(5.0)
        await client.stop_notify(char)


asyncio.run(main())
