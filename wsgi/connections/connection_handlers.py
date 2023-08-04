from wsgi.calendars import caldav_api
from wsgi.database import db
from wsgi.notifications.jobs import delete_jobs_by_user_id

import logging, traceback
from flask import Request
from sqlalchemy.exc import SQLAlchemyError


def profile(request: Request):
    pass


def update_account(request: Request):
    values = request.json['values']

    user_id = request.json['context']['acting_user']['id']
    login = values['login']
    token = values['token']
    timezone = values['timezone']['value']

    principal = caldav_api.take_principal(db.User(user_id, login, token, timezone))
    if type(principal) is dict:
        return principal

    try:

        msg = {

            'type': 'ok',
            'text': 'Successfully UPDATE integration with yandex calendar. ' \
                    'Your scheduler notifications was deleted if is existed',

        }

        result = db.User.update_user(user_id, login, token, timezone)

    except SQLAlchemyError as exp:

        msg = {'type': 'error', 'text': f'Error updating integration with yandex calendar.'}
        logging.error(f'Error updating user in DB, {user_id=}. Traceback: {traceback.print_exc()}')

    else:

        delete_jobs_by_user_id(user_id)

    return msg


def delete_account(request: Request):
    user_id = request.json['context']['acting_user']['id']

    msg = {

        'type': 'ok',
        'text': 'Successfully REMOVE integration with yandex calendar. ' \
                'Your scheduler notifications was deleted if is existed',

    }

    try:

        result = db.User.remove_user(user_id)

    except SQLAlchemyError as exp:

        msg = {

            'type': 'error',
            'text': f'Error removing integration with yandex calendar.',

        }

        logging.error(f'Error removing user in DB, {user_id=}. Traceback: {traceback.print_exc()}')

    else:

        delete_jobs_by_user_id(user_id)

    return msg


def create_account(request: Request):
    values = request.json['values']

    user_id = request.json['context']['acting_user']['id']
    login = values['login']
    token = values['token']
    timezone = values['timezone']['value']

    principal = caldav_api.take_principal(db.User(user_id, login, token, timezone))

    if type(principal) is dict:
        return principal

    msg = {'type': 'ok', 'text': 'Successfully CREATE integration with yandex calendar'}

    try:

        result = db.User.add_user(user_id, login, token, timezone)

    except SQLAlchemyError as exp:

        msg = {'type': 'error', 'text': f'Error creating integration with yandex calendar.'}
        logging.error(f'Error adding user in DB, {user_id=}. Traceback: {traceback.print_exc()}')

    return msg
