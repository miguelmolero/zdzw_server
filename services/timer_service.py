import asyncio
from datetime import datetime
from services.received_data_handling import read_received_data

async def get_received_records():
    await read_received_data()

async def start_timer():
    while True:
        await get_received_records()
        await asyncio.sleep(60)