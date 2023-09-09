from wsgi.database.models import engine, metadata_obj
from wsgi.settings import envs

from flask import current_app
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.job import Job
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
import logging


def init_app(app):
    if envs.DEBUG:
        logging.basicConfig()
        apscheduler_logger = logging.getLogger('apscheduler')
        apscheduler_logger.setLevel('DEBUG')
    # scheduler.add_listener(my_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
    # app.cli.add_command(CLIs.something_command)

    if not scheduler.running:
        scheduler.start()


def my_listener(event):
    if event.exception:
        current_app.logger.error('Crash job: %s' % event)
    else:
        current_app.logger.debug('Success job: %s' % event)


def delete_rt_stat_job(mm_user_id: str):
    pattern = f'{mm_user_id}(rt_stat)'
    [job.remove() for job in scheduler.get_jobs('default') if job.id == pattern]


def delete_job_by_uid(uid: str):
    [job.remove() for job in scheduler.get_jobs('default') if uid in job.id]


def delete_jobs_by_mm_user_id(mm_user_id: str) -> None:
    [job.remove() for job in scheduler.get_jobs('default') if job.id.startswith(mm_user_id)]


def delete_jobs_by_cal_id(cal_id: str) -> None:
    [job.remove() for job in scheduler.get_jobs('default') if cal_id in job.id]


def check_exists_jobs_by_mm_user_id(mm_user_id: str) -> bool:
    for job in scheduler.get_jobs():
        if job.id.startswith(mm_user_id):
            return True
    return False


def get_jobs_by_mm_user_id(mm_user_id: str) -> list[Job]:
    return [job for job in scheduler.get_jobs(jobstore='default') if job.id.startswith(mm_user_id)]


scheduler_config = {
    'apscheduler.jobstores.default': {
        'type': 'sqlalchemy',
        'engine': engine,
        'tablename': 'apscheduler_job',
        'metadata': metadata_obj,
    },
    'apscheduler.executors.default': {
        'class': 'apscheduler.executors.pool:ThreadPoolExecutor',
        'max_workers': '20'
    },
    'apscheduler.executors.processpool': {
        'type': 'processpool',
        'max_workers': '5'
    },
    'apscheduler.job_defaults.coalesce': 'true',
    'apscheduler.job_defaults.max_instances': '1',
    'apscheduler.timezone': 'UTC',
}

scheduler = BackgroundScheduler(scheduler_config)
