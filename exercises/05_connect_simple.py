import asyncio

from bleak import BleakClient, BleakScanner
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData

ENVIRONMENTAL_SENSING_UUID = "0000181a-0000-1000-8000-00805f9b34fb"

discovered_device: BLEDevice = None


def discovery_callback(device: BLEDevice, advertisement_data: AdvertisementData) -> None:
    print(
        f"Peripheral {device.name} ({device.address}) "
        f"with service {advertisement_data.service_uuids} found!")
    global discovered_device  # noqa: PLW0603
    discovered_device = device


def disconnected_clbk(client: BleakClient) -> None:
    print(f"Disconnected from {client.address}")


async def main() -> None:

    scanner = BleakScanner()

    def service_uuid_filter(device: BLEDevice, adv: AdvertisementData) -> None:  # noqa: ARG001
        return ENVIRONMENTAL_SENSING_UUID in adv.service_uuids

    device = await scanner.find_device_by_filter(service_uuid_filter)
    print(device)

    while discovered_device is None:
        await scanner.discover(detection_callback=discovery_callback,
                               service_uuids=[ENVIRONMENTAL_SENSING_UUID])
        if discovered_device is None:
            print("No devices with environmental sensing service found")

    client = BleakClient(discovered_device,
                         disconnected_callback=disconnected_clbk)
    await client.connect()
    print(f"Connected to {discovered_device}")
    await asyncio.sleep(2)
    await client.disconnect()


asyncio.run(main())
