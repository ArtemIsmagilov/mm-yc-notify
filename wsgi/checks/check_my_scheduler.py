from wsgi.schedulers.sd import get_jobs_by_user_id

from flask import Request


def check_scheduler(request: Request):
    user_id = request.json['context']['acting_user']['id']

    exists_jobs = get_jobs_by_user_id(user_id)

    if exists_jobs:

        text = '# Your scheduler is enable :)'

    else:

        text = '# You don\'t have scheduler notifications :('

    return {
        'type': 'ok',
        'text': text,
    }
