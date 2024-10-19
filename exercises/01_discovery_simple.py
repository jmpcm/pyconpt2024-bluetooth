import asyncio

from bleak import BleakScanner


async def main() -> None:
    devices = await BleakScanner.discover()

    for d in devices:
        print(d)

asyncio.run(main())
