import asyncio
import random


@asyncio.coroutine
def perform(**kwargs):
    print(__name__ + "coroutine start!!")
    yield from asyncio.sleep(random.uniform(5, 10))
    print(__name__ + "coroutine end")
