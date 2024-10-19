import asyncio

from bleak import BleakScanner
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData


def discovery_callback(device: BLEDevice, advertisement_data: AdvertisementData) -> None:
    print(f"{device.address} {advertisement_data}")


async def main() -> None:
    scanner = BleakScanner()
    await scanner.discover(detection_callback=discovery_callback)

asyncio.run(main())
