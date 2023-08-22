from wsgi.calendars import caldav_api
from wsgi.database import db
from wsgi.schedulers import sd

from flask import Request
from sqlalchemy.engine import Row


def profile(request: Request):
    return {
        'type': 'ok',
        'text': 'Not implemented.'
    }


def update_account(request: Request, user: Row) -> dict:
    values = request.json['values']

    mm_user_id = request.json['context']['acting_user']['id']
    login = values['login']
    token = values['token']
    timezone = values['timezone']['value']

    principal = caldav_api.take_principal(db.User(mm_user_id=mm_user_id, login=login, token=token, timezone=timezone))

    if type(principal) is dict:
        return principal

    msg = {
        'type': 'ok',
        'text': ('Successfully UPDATE integration with yandex calendar. '
                 'Your scheduler notifications was deleted if is existed'),
    }

    updated_user_row = db.User.update_user(
        mm_user_id=mm_user_id, login=login, token=token, timezone=timezone, e_c=False, ch_stat=False
    )

    result = db.YandexCalendar.remove_cals(user_id=updated_user_row.id)

    sd.delete_jobs_by_mm_user_id(mm_user_id)

    return msg


def delete_account(request: Request, user: Row) -> dict:
    mm_user_id = request.json['context']['acting_user']['id']

    msg = {
        'type': 'ok',
        'text': ('Successfully REMOVE integration with yandex calendar. '
                 'Your scheduler notifications was deleted if is existed.'),
    }

    db.User.remove_user(mm_user_id=mm_user_id)

    sd.delete_jobs_by_mm_user_id(mm_user_id)

    return msg


def create_account(request: Request) -> dict:
    values = request.json['values']

    mm_user_id = request.json['context']['acting_user']['id']
    login = values['login']
    token = values['token']
    timezone = values['timezone']['value']

    principal = caldav_api.take_principal(db.User(mm_user_id=mm_user_id, login=login, token=token, timezone=timezone, e_c=False, ch_stat=False))

    if type(principal) is dict:
        return principal

    msg = {
        'type': 'ok',
        'text': 'Successfully CREATE integration with yandex calendar'
    }

    result = db.User.add_user(mm_user_id=mm_user_id, login=login, token=token, timezone=timezone, e_c=False, ch_stat=False)

    return msg
