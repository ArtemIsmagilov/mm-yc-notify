from wsgi.schedulers import sd

from flask import Request


def check_scheduler(request: Request) -> dict:
    mm_user_id = request.json['context']['acting_user']['id']

    exists_jobs = sd.get_jobs_by_mm_user_id(mm_user_id)

    if exists_jobs:

        text = '# Your scheduler is enable :)'

    else:

        text = '# You don\'t have scheduler notifications :('

    return {
        'type': 'ok',
        'text': text,
    }
