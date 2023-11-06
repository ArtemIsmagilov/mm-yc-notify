from ..app_handlers import static_file
from ..calendars import caldav_api
from ..calendars.caldav_funcs import take_principal
from ..constants import EXPAND_DICT, UTCs
from ..converters import create_table_md, client_id_calendar
from ..decorators.account_decorators import required_account_does_not_exist, auth_required
from ..sql_app.database import get_conn
from ..sql_app.crud import User, YandexCalendar

import asyncio
from quart import url_for, request
from sqlalchemy.engine import Row
from sqlalchemy.ext.asyncio import AsyncConnection


async def profile():
    data = await request.json

    mm_user_id = data['context']['acting_user']['id']
    mm_username = data['context']['acting_user']['username']

    account = {'status': 'Anonymous'}

    async with get_conn() as conn:

        user = await User.get_user(conn, mm_user_id)

        if user:

            account.update(
                status='User',
                login=user.login,
                username='@%s' % mm_username,
                timezone=user.timezone,
                notify_every_confernece='%s' % user.e_c,
                changing_status_every_confernece='%s' % user.ch_stat,
                sync_calendars='None',
            )

            principal = await take_principal(user.login, user.token)

            if type(principal) is dict:
                await User.remove_user(conn, mm_user_id)
                return principal

            if await YandexCalendar.get_first_cal(conn, mm_user_id):
                cals = await caldav_api.check_exist_calendars_by_cal_id(
                    principal, YandexCalendar.get_cals(conn, mm_user_id)
                )

                if type(cals) is dict:
                    await YandexCalendar.remove_cals(conn, mm_user_id)
                    return cals

                account.update(sync_calendars=', '.join(client_id_calendar(c) for c in cals))

    text = create_table_md(account)

    return {
        'type': 'ok',
        'text': text,
    }


@required_account_does_not_exist
async def create_account(conn: AsyncConnection):
    data = await request.json
    values = data['values']

    mm_user_id = data['context']['acting_user']['id']
    login = values['login']
    token = values['token']
    timezone = values['timezone']['value']

    mm_username = data['context']['acting_user']['username']

    principal = await take_principal(login, token)

    if type(principal) is dict:
        return principal

    msg = {
        'type': 'ok',
        'text': f'@{mm_username}, you successfully CREATE integration with yandex calendar'
    }

    await User.add_user(
        conn,
        mm_user_id=mm_user_id,
        login=login,
        token=token,
        timezone=timezone,
        e_c=False,
        ch_stat=False,
    )

    return msg


async def really_update_account():
    data = await request.json
    mm_username = data['context']['acting_user']['username']

    return {
        "type": "form",
        "values": data,
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


@auth_required
async def update_account(conn: AsyncConnection, user: Row) -> dict:
    data = await request.json
    values = data['values']

    mm_user_id = data['context']['acting_user']['id']
    mm_username = data['context']['acting_user']['username']

    login = values['login']
    token = values['token']
    timezone = values['timezone']['value']

    principal = await take_principal(login, token)

    if type(principal) is dict:
        return principal

    async with asyncio.TaskGroup() as tg:
        tg.create_task(YandexCalendar.remove_cals(
            conn, mm_user_id=mm_user_id
        ))

        tg.create_task(User.update_user(
            conn, mm_user_id, login=login, token=token, timezone=timezone, e_c=False, ch_stat=False
        ))

    text = (f'@{mm_username}, you successfully UPDATE integration with yandex calendar. '
            'Your scheduler notifications was deleted if is existed')
    msg = {
        'type': 'ok',
        'text': text,
    }

    return msg


async def really_delete_account():
    data = await request.json
    mm_username = data['context']['acting_user']['username']

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


@auth_required
async def delete_account(conn: AsyncConnection, user: Row) -> dict:
    data = await request.json
    mm_user_id = data['context']['acting_user']['id']
    mm_username = data['context']['acting_user']['username']

    text = (f'@{mm_username}, you successfully REMOVE integration with yandex calendar. '
            'Your scheduler notifications was deleted if is existed.')

    msg = {
        'type': 'ok',
        'text': text,
    }

    await User.remove_user(conn, mm_user_id)

    return msg
