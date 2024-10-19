from __future__ import annotations

import asyncio
import logging
import random
import signal
import sys
import threading
import time
from pathlib import Path
from typing import Any

from bless import (
    BlessGATTCharacteristic,
    BlessServer,
    GATTAttributePermissions,
    GATTCharacteristicProperties,
)


def read_temperature_raw(device: str) -> list[str]:
    with Path(device).open() as fp:
        return fp.readlines()


def read_temperature(device: str) -> tuple[float, float] | None:
    lines = read_temperature_raw(device)
    print(f"{lines=}")

    # Check if the reading is correct. The first line must contain YES.
    while lines[0].strip()[-3:] != "YES":
        time.sleep(0.2)
        lines = read_temperature_raw(DEVICE_FILE)

    # Calculate temperature and convert to Fahrenheit. The temperature is in the second line.
    equals_pos = lines[1].find("t=")

    if equals_pos == -1:
        return None

    temp_string = lines[1][equals_pos+2:]
    temp_c = float(temp_string) / 1000.0
    temp_f = temp_c * 9.0 / 5.0 + 32.0

    return temp_c, temp_f


ENVIRONMENTAL_SENSING_UUID = "0000181a-0000-1000-8000-00805f9b34fb"
ENVIRONMENTAL_SENSING_TEMPERATURE_UUID = "00002a6e-0000-1000-8000-00805f9b34fb"
BASE_DIR = Path("/sys/bus/w1/devices/")
# DEVICE_DIR = glob.glob(BASE_DIR, "28*")[0]

if Path.exists(BASE_DIR):
    try:
        DEVICE_DIR = next(BASE_DIR.glob("28*"), None)
        print(DEVICE_DIR)
        DEVICE_FILE = Path(DEVICE_DIR).joinpath("/w1_slave")
        print(DEVICE_FILE)
    except (StopIteration, TypeError):
        DEVICE_DIR = None
        DEVICE_FILE = None
else:
    DEVICE_DIR = None
    DEVICE_FILE = None


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(name=__name__)

# NOTE: Some systems require different synchronization methods.
stop_server: asyncio.Event | threading.Event
if sys.platform in ["darwin", "win32"]:
    stop_server = threading.Event()
else:
    stop_server = asyncio.Event()


def read_request(characteristic: BlessGATTCharacteristic, **kwargs) -> bytearray | None:
    if characteristic.uuid != ENVIRONMENTAL_SENSING_TEMPERATURE_UUID:
        return None

    temperature: int

    if DEVICE_FILE is not None:
        temp_c, temp_f = read_temperature(DEVICE_FILE)
        logger.debug(f"{temp_c=}; {temp_f=}")
        temperature = int(temp_c * 100).to_bytes(length=2, byteorder="little")
    else:
        temp = round(random.uniform(23.0, 24.5), 2)  # noqa: S311
        logger.debug(f"Reading temperature = {temp}")
        temperature = int(temp * 100).to_bytes(length=2, byteorder="little")

    return temperature


def write_request(characteristic: BlessGATTCharacteristic, value: Any, **kwargs):
    characteristic.value = value
    logger.debug(f"Char value set to {characteristic.value}")
    if characteristic.value == b"\x0f":
        logger.debug("NICE")


async def run(loop):
    def stop_server_clbk(sig, frame):
        stop_server.set()

    signal.signal(signal.SIGINT, stop_server_clbk)
    signal.signal(signal.SIGTERM, stop_server_clbk)

    # Instantiate the server
    my_service_name = "PyCon Environment Sensing (mac)"
    server = BlessServer(name=my_service_name, loop=loop)
    server.read_request_func = read_request
    server.write_request_func = write_request

    # Add Service
    my_service_uuid = ENVIRONMENTAL_SENSING_UUID
    await server.add_new_service(my_service_uuid)

    # Add a Characteristic to the service
    my_char_uuid = ENVIRONMENTAL_SENSING_TEMPERATURE_UUID
    char_flags = (
        GATTCharacteristicProperties.read
        | GATTCharacteristicProperties.notify
        | GATTCharacteristicProperties.indicate
    )
    permissions = GATTAttributePermissions.readable
    await server.add_new_characteristic(
        my_service_uuid, my_char_uuid, char_flags, None, permissions,
    )

    logger.debug(server.get_characteristic(my_char_uuid))

    await server.start()
    logger.debug("Advertising")

    if stop_server.__module__ == "threading":
        stop_server.wait()
    else:
        await stop_server.wait()

    logger.info("Stopping server")
    await server.stop()


loop = asyncio.get_event_loop()
loop.run_until_complete(run(loop))
