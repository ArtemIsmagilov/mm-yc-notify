import asyncio
from asyncio.exceptions import CancelledError
from ..notifications.tasks import task0
from settings import Conf


# python -m app.notifications.task0_scheduler
async def start_scheduler():
    try:
        while True:
            await task0()
            await asyncio.sleep(Conf.CHECK_EVENTS)
    except (KeyboardInterrupt, CancelledError) as exp:
        print(exp)


if __name__ == '__main__':
    asyncio.run(start_scheduler())
