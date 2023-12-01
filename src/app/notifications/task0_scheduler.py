import asyncio
from ..notifications.tasks import task0
from settings import Conf


# python -m app.notifications.task0_scheduler
async def start_scheduler():
    while True:
        await asyncio.sleep(Conf.CHECK_EVENTS)
        await task0()


if __name__ == '__main__':
    asyncio.run(start_scheduler())
