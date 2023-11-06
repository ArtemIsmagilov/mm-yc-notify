from quart import request

from ..sql_app.database import get_conn
from ..sql_app.crud import User


async def check_user() -> dict:
    data = await request.json
    mm_username = data['context']['acting_user']['username']
    mm_user_id = data['context']['acting_user']['id']

    async with get_conn() as conn:
        user = await User.get_user(conn, mm_user_id)

    if user:

        return {
            'type': 'ok',
            'text': f'# @{mm_username}, your integration with Yandex Calendar is enable :)',
        }

    else:

        return {
            'type': 'ok',
            'text': (f'# @{mm_username}, your integration with Yandex Calendar is disable :(\n'
                     'You need complete connect to integration.'),
        }
