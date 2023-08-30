from wsgi.app_handlers import static_file
from wsgi.calendars import caldav_api
from wsgi.constants import EXPAND_DICT, UTCs
from wsgi.database import db
from wsgi.schedulers import sd

from flask import Request, url_for
from sqlalchemy.engine import Row


def profile(user: Row, request: Request):
    account = {'status': 'Anonymous'}

    if user:

        mm_username = request.json['context']['acting_user']['username']
        account.update(
            status='User',
            login=user.login,
            username=f'@{mm_username}',
            timezone=user.timezone,
            notify_every_confernece=str(user.e_c),
            changing_status_every_confernece=str(user.ch_stat),
        )

        get_user_cals = db.YandexCalendar.get_cals(user_id=user.id)

        if get_user_cals:
            cals = caldav_api.check_exist_calendars_by_cal_id(user, (c.cal_id for c in get_user_cals))

            if type(cals) is dict:
                return cals

            account.update(sync_calendars=', '.join(f'**{c.get_display_name()}**({c.id})' for c in cals))

        else:

            account.update(sync_calendars=str(None))

    header = " | ".join(account.keys())
    delimiter = "-|" * len(account)
    body = " | ".join(account.values())

    text = f"| {header} |\n|{delimiter}\n| {body} |"

    return {
        'type': 'ok',
        'text': text,
    }


def create_account(request: Request) -> dict:
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
        'text': 'Successfully CREATE integration with yandex calendar'
    }

    result = db.User.add_user(mm_user_id=mm_user_id, login=login, token=token, timezone=timezone, e_c=False,
                              ch_stat=False)

    return msg


def really_update_account(request: Request):
    mm_username = request.json['context']['acting_user']['username']

    return {
        "type": "form",
        "form": {
            "title": "Update connections?",
            "header": f'**{mm_username}**, are you sure, what need update integration with yandex-calendar?',
            "icon": static_file('cal.png'),
            "submit": {
                "path": url_for('connections.update_account_form'),
                "expand": EXPAND_DICT,
            },
        }
    }


def update_account_form():
    return {
        "type": "form",
        "form": {
            "title": "Update integrations with Yandex Calendar over CalDAV protocol",
            "header": "Update",
            "icon": static_file('cal.png'),
            "fields": [
                {
                    "name": "login",
                    "label": "login",
                    "modal_label": 'Login',
                    "type": "text",
                    "subtype": "input",
                    "description": "Enter login",
                    'is_required': True,
                    'hint': '[login]'
                },
                {
                    "name": "token",
                    "label": "token",
                    "modal_label": 'Token',
                    "type": "text",
                    "subtype": "password",
                    "description": "Enter created yandex calendar app token",
                    'hint': '[token]',
                    'is_required': True,
                },
                {
                    "name": "timezone",
                    "type": "static_select",
                    "label": "utc",
                    "modal_label": 'TimeZone',
                    "options": UTCs,
                    "is_required": True,
                    "description": 'Select timezone',
                    "value": {'label': '(UTC+00:00) UTC', 'value': 'UTC'},
                    "hint": '[(UTC-12)|(UTC+12)]',
                },
            ],
            "submit": {
                "path": url_for('connections.update_account'),
                'expand': EXPAND_DICT,
            }
        }
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

    updated_user = db.User.update_user(mm_user_id, login=login, token=token, timezone=timezone, e_c=False,
                                       ch_stat=False)

    result = db.YandexCalendar.remove_cals(user_id=updated_user.id)
    sd.delete_jobs_by_mm_user_id(mm_user_id)

    return msg


def really_delete_account(request: Request):
    mm_username = request.json['context']['acting_user']['username']

    return {
        "type": "form",
        "form": {
            "title": "Delete connections?",
            "header": f'**{mm_username}**, are you sure, what need delete integration with yandex-calendar?',
            "icon": static_file('cal.png'),
            "submit": {
                "path": url_for('connections.disconnect_account'),
                "expand": EXPAND_DICT,
            },
        }
    }


def delete_account(request: Request) -> dict:
    mm_user_id = request.json['context']['acting_user']['id']

    msg = {
        'type': 'ok',
        'text': ('Successfully REMOVE integration with yandex calendar. '
                 'Your scheduler notifications was deleted if is existed.'),
    }

    db.User.remove_user(mm_user_id)
    sd.delete_jobs_by_mm_user_id(mm_user_id)

    return msg
