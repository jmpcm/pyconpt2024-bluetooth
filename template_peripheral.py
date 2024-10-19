import asyncio
import signal

async def main():
    stop_scanning = asyncio.Event()
    
    def stop_scanning_clbk(sig, frame):
        stop_scanning.set()

    signal.signal(signal.SIGINT, stop_scanning_clbk)
    signal.signal(signal.SIGTERM, stop_scanning_clbk)

    while not stop_scanning.is_set():
        await stop_scanning.wait()

asyncio.run(main())
