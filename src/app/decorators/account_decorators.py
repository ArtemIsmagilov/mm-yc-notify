from ..dict_responses import already_exists_integration, unauth_integration
from ..schemas import UserInDb
from ..sql_app.database import get_conn
from ..sql_app.crud import User
from ..calendars.caldav_funcs import take_principal

from functools import wraps
import logging, traceback
from quart import request
from httpx import HTTPError


def auth_required(view):
    @wraps(view)
    async def wrapped_view(*args, **kwargs):
        data = await request.json
        mm_user_id = data['context']['acting_user']['id']
        mm_username = data['context']['acting_user']['username']
        async with get_conn() as conn:
            user = await User.get_user(conn, mm_user_id)
            if not user:
                return unauth_integration(mm_username)
            else:
                user_view = UserInDb(user)
                kwargs.update(conn=conn, user=user_view)

                return await view(*args, **kwargs)

    return wrapped_view


def required_account_does_not_exist(view):
    @wraps(view)
    async def wrapped_view(*args, **kwargs):
        data = await request.json
        mm_user_id = data['context']['acting_user']['id']
        mm_username = data['context']['acting_user']['username']
        async with get_conn() as conn:
            user = await User.get_user(conn, mm_user_id)
            if user:
                return already_exists_integration(mm_username)
            else:
                kwargs.update(conn=conn)
                return await view(*args, **kwargs)

    return wrapped_view


def dependency_principal(func):
    @wraps(func)
    async def wrapped_funcs(user: UserInDb, *args, **kwargs):
        response = await take_principal(user.login, user.token)

        if type(response) is dict:
            return response

        kwargs.update(principal=response, user=user)
        return await func(*args, **kwargs)

    return wrapped_funcs


def bot_error(func):
    @wraps(func)
    async def wrapped(*args, **kwargs):
        try:
            result = await func(*args, **kwargs)
        except HTTPError as exp:
            logging.error('Bot http error: %s', traceback.format_exc())
            return exp
        else:
            return result

    return wrapped


def app_error(func):
    @wraps(func)
    async def wrapped(*args, **kwargs):
        try:
            result = await func(*args, **kwargs)
        except Exception as exp:
            logging.error('App error: %s', traceback.format_exc())
            return exp
        else:
            return result

    return wrapped
