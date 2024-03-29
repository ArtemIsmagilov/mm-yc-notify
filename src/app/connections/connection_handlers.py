import asyncio

from quart import (
    url_for,
    request
)
from sqlalchemy.ext.asyncio import AsyncConnection

from ..app_handlers import static_file
from ..calendars.caldav_funcs import take_principal
from ..constants import (
    EXPAND_DICT,
    UTCs
)
from ..decorators.account_decorators import (
    required_account_does_not_exist,
    auth_required
)
from ..dict_responses import (
    success_remove_integration,
    success_create_integration,
    success_update_integration,
    success_ok
)
from ..connections import connection_backgrounds
from ..schemas import UserInDb


async def profile() -> dict:
    data = await request.json

    mm_user_id = data['context']['acting_user']['id']
    mm_username = data['context']['acting_user']['username']
    channel_id = data['context']['channel']['id']
    asyncio.create_task(connection_backgrounds.bg_profile(mm_user_id, mm_username, channel_id))
    return success_ok(mm_username)


@required_account_does_not_exist
async def create_account(conn: AsyncConnection) -> dict:
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

    asyncio.create_task(connection_backgrounds.bg_create_account(mm_user_id, login, token, timezone))

    return success_create_integration(mm_username)


async def really_update_account() -> dict:
    data = await request.json
    mm_username = data['context']['acting_user']['username']

    return {
        "type": "form",
        "values": data,
        "form": {
            "title": "Update connections?",
            "header": '**%s**, are you sure, what need update integration with yandex-calendar?' % mm_username,
            "icon": static_file('cal.png'),
            "submit": {
                "path": url_for('connections.update_account_form'),
                "expand": EXPAND_DICT,
            },
        }
    }


def update_account_form() -> dict:
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
async def update_account(conn: AsyncConnection, user: UserInDb) -> dict:
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

    asyncio.create_task(connection_backgrounds.bg_update_account(mm_user_id, login, token, timezone))

    return success_update_integration(mm_username)


async def really_delete_account() -> dict:
    data = await request.json
    mm_username = data['context']['acting_user']['username']

    return {
        "type": "form",
        "form": {
            "title": "Delete connections?",
            "header": '**%s**, are you sure, what need delete integration with yandex-calendar?' % mm_username,
            "icon": static_file('cal.png'),
            "submit": {
                "path": url_for('connections.disconnect_account'),
                "expand": EXPAND_DICT,
            },
        }
    }


@auth_required
async def delete_account(conn: AsyncConnection, user: UserInDb) -> dict:
    data = await request.json
    mm_user_id = data['context']['acting_user']['id']
    mm_username = data['context']['acting_user']['username']

    asyncio.create_task(connection_backgrounds.bg_remove_account(mm_user_id))

    return success_remove_integration(mm_username)
