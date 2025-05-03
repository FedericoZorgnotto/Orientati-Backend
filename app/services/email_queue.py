import asyncio
from typing import Callable

queue = asyncio.Queue()


async def enqueue_email(callable_func: Callable, *args, **kwargs):
    await queue.put((callable_func, args, kwargs))

async def email_worker():
    while True:
        print("Email queue")

        func, args, kwargs = await queue.get()
        try:
            await func(*args, **kwargs)
        except Exception as e:
            print(f"Errore nell'invio email: {e}")
        queue.task_done()
