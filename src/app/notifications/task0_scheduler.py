import asyncio
from apscheduler import AsyncScheduler
from apscheduler.triggers.interval import IntervalTrigger

from ..notifications.tasks import task0
from ..settings import envs


# python -m app.notifications.task0_scheduler
async def start_scheduler():
    async with AsyncScheduler() as scheduler:
        await scheduler.add_schedule(task0, IntervalTrigger(seconds=envs.CHECK_EVENTS))
        await scheduler.run_until_stopped()

if __name__ == '__main__':
    asyncio.run(start_scheduler())
