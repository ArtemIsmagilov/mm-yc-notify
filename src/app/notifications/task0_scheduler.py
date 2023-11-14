import asyncio
from apscheduler import AsyncScheduler
from apscheduler.triggers.interval import IntervalTrigger

from ..notifications.tasks import task0
from settings import Conf


# python -m app.notifications.task0_scheduler
async def start_scheduler():
    async with AsyncScheduler() as scheduler:
        await scheduler.add_schedule(task0, IntervalTrigger(seconds=Conf.CHECK_EVENTS))
        await scheduler.run_until_stopped()

# if __name__ == '__main__':
#     asyncio.run(start_scheduler())
