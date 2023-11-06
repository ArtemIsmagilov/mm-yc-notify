from ..sql_app.database import get_conn
from ..sql_app.crud import YandexCalendar
from quart import request


async def check_scheduler() -> dict:
    data = await request.json
    mm_user_id = data['context']['acting_user']['id']

    async with get_conn() as conn:
        first_cal = await YandexCalendar.get_first_cal(conn, mm_user_id)

    if first_cal:

        text = '# Your scheduler is enable :)'

    else:

        text = '# You don\'t have scheduler notifications :('

    return {
        'type': 'ok',
        'text': text,
    }
