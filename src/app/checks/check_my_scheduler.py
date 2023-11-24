from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy.engine import Row
from quart import request

from ..decorators.account_decorators import auth_required
from ..dict_responses import is_disable_scheduler, is_enable_scheduler
from ..sql_app.crud import YandexCalendar


@auth_required
async def check_scheduler(
        conn: AsyncConnection,
        user: Row
) -> dict:
    data = await request.json
    mm_user_id = data['context']['acting_user']['id']
    mm_username = data['context']['acting_user']['username']

    first_cal = await YandexCalendar.get_first_cal(conn, mm_user_id)

    if first_cal:

        return is_enable_scheduler(mm_username)

    else:

        return is_disable_scheduler(mm_username)
