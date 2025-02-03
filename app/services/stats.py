import asyncio
from datetime import datetime

import psutil

from app.config import settings
from app.database import get_mongodb


async def update_stats():
    database = get_mongodb()
    while database is None:
        await asyncio.sleep(1)
        database = get_mongodb()
    stats_collection = database.get_collection(settings.MONGODB_STATS_COLLECTION)

    while True:
        asyncio.create_task(send_stats(stats_collection))
        await asyncio.sleep(5)


async def send_stats(stats_collection):
    cpu = psutil.cpu_percent(interval=1)  # Percentuale uso CPU
    ram = psutil.virtual_memory().percent  # Percentuale uso RAM

    dato = {
        "timestamp": datetime.now(),  # Timestamp BSON richiesto da MongoDB
        "cpu_percent": cpu,
        "ram_percent": ram
    }

    stats_collection.insert_one(dato)
