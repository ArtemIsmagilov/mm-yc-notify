from ..sql_app.database import get_conn
from ..sql_app.crud import User
from ..calendars.caldav_funcs import take_principal

import functools, logging
from quart import g, request
from httpx import HTTPError
from sqlalchemy.engine import Row


def auth_required(view):
    @functools.wraps(view)
    async def wrapped_view(*args, **kwargs):
        data = await request.json
        mm_user_id = data['context']['acting_user']['id']
        async with get_conn() as conn:
            user = await User.get_user(conn, mm_user_id)
            if not user:
                return {
                    'type': 'error',
                    'text': 'Your haven\'t integration with yandex-calendar. First, to connect'
                }
            else:

                kwargs.update(conn=conn, user=user)
                return await view(*args, **kwargs)

    return wrapped_view


def required_account_does_not_exist(view):
    @functools.wraps(view)
    async def wrapped_view(*args, **kwargs):
        data = await request.json
        mm_user_id = data['context']['acting_user']['id']
        async with get_conn() as conn:
            user = await User.get_user(conn, mm_user_id)
            if user:
                return {
                    'type': 'error',
                    'text': 'Your integration with yandex-calendar already exists.'
                }
            else:
                kwargs.update(conn=conn)
                return await view(*args, **kwargs)

    return wrapped_view


def dependency_principal(func):
    @functools.wraps(func)
    async def wrapped_funcs(user: Row, *args, **kwargs):
        response = await take_principal(user.login, user.token)

        if type(response) is dict:
            return response

        kwargs.update(principal=response, user=user)
        return await func(*args, **kwargs)

    return wrapped_funcs


def bot_error(func):
    @functools.wraps(func)
    async def wrapped(*args, **kwargs):
        try:
            result = await func(*args, **kwargs)
        except HTTPError as exp:
            logging.error('Bot http error: %s', exp)
            return exp
        else:
            return result

    return wrapped
