import asyncio
import signal

from bleak import BleakScanner
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData


def discovery_callback(device: BLEDevice, advertisement_data: AdvertisementData) -> None:
    print(f"{device.address} {advertisement_data}")


async def main() -> None:
    stop_scanning = asyncio.Event()
    scanner = BleakScanner(discovery_callback,
                           service_uuids=["0000181a-0000-1000-8000-00805f9b34fb"])

    def stop_scanning_clbk(sig, frame) -> None:
        stop_scanning.set()

    signal.signal(signal.SIGINT, stop_scanning_clbk)
    signal.signal(signal.SIGTERM, stop_scanning_clbk)

    while not stop_scanning.is_set():
        async with scanner:
            await stop_scanning.wait()

asyncio.run(main())
