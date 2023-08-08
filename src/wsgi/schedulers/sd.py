from wsgi.settings import DEBUG
from wsgi.database.db import SCHEDULER_CONF

from flask import current_app
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.job import Job
import logging


def init_app(app):
    if DEBUG:
        logging.basicConfig()
        apscheduler_logger = logging.getLogger('apscheduler')
        apscheduler_logger.setLevel(DEBUG)
    # schedulers.add_listener(my_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
    # app.cli.add_command(CLIs.something_command)
    scheduler.start()


def my_listener(event):
    if event.exception:
        current_app.logger.error('Crash job: %s' % event)
    else:
        current_app.logger.debug('Success job: %s' % event)


def delete_jobs_by_user_id(user_id: str) -> None:
    [job.remove() for job in scheduler.get_jobs('default') if job.id.startswith(user_id)]


def check_exists_jobs_by_user_id(user_id: str) -> bool:
    return bool(get_jobs_by_user_id(user_id))


def get_jobs_by_user_id(user_id: str) -> list[Job]:
    return [job for job in scheduler.get_jobs(jobstore='default') if job.id.startswith(user_id)]


scheduler = BackgroundScheduler()
scheduler.configure(SCHEDULER_CONF)
