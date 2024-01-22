from quart import request

from ..dict_responses import (
    is_enable_integration,
    is_disable_integration
)
from ..sql_app.database import get_conn
from ..sql_app.crud import User


async def check_user() -> dict:
    data = await request.json
    mm_username = data['context']['acting_user']['username']
    mm_user_id = data['context']['acting_user']['id']

    async with get_conn() as conn:
        user = await User.get_user(conn, mm_user_id)

    if user:

        return is_enable_integration(mm_username)

    else:

        return is_disable_integration(mm_username)
