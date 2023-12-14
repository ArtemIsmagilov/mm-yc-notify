from datetime import datetime
import asyncio
from caldav import Principal
import caldav.lib.error as caldav_errs

from . import calendar_views
from ..async_wraps.async_wrap_caldav import caldav_calendar_by_cal_id, caldav_get_supported_components
from ..bots.bot_commands import send_ephemeral_msg_client
from ..sql_app.crud import YandexCalendar
from ..sql_app.database import get_conn


async def run_in_background(mm_user_id: str, channel_id: str, principal: Principal, start: datetime, end: datetime):
    async with get_conn() as conn:
        cals_server = set()
        async for c in YandexCalendar.get_cals(conn, mm_user_id):
            calendar_server = await caldav_calendar_by_cal_id(principal, c.cal_id)
            try:
                await caldav_get_supported_components(calendar_server)
            except caldav_errs.NotFoundError as exp:
                await YandexCalendar.remove_cal(conn, c.cal_id)
            else:
                cals_server.add(calendar_server)

    result = await calendar_views.base_view(cals_server, 'get_all.md', (start, end))
    asyncio.create_task(send_ephemeral_msg_client(mm_user_id, channel_id, result['text']))
