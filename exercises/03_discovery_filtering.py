import asyncio

from bleak import BleakScanner
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData


def discovery_callback(device: BLEDevice, advertisement_data: AdvertisementData) -> None:
    print(f"{device.address} {advertisement_data}")


async def main() -> None:
    scanner = BleakScanner()

    await scanner.discover(detection_callback=discovery_callback,
                           service_uuids=["0000181a-0000-1000-8000-00805f9b34fb",
                                          "51FF12BB-3ED8-46E5-B4F9-D64E2FEC021B"])

asyncio.run(main())
