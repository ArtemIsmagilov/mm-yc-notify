import asyncio
from apscheduler import AsyncScheduler
from apscheduler.triggers.interval import IntervalTrigger

from ..settings import envs
from ..notifications.tasks import task0


# python -m app.notifications.task0_scheduler
async def main():
    async with AsyncScheduler() as scheduler:
        await scheduler.add_schedule(task0, IntervalTrigger(seconds=envs.CHECK_EVENTS))
        await scheduler.run_until_stopped()


if __name__ == '__main__':
    asyncio.run(main())
