import asyncio
from secrets import token_hex

from ..bots.bot_commands import send_ephemeral_msg_client
from ..calendars import caldav_api
from ..calendars.caldav_funcs import take_principal
from ..converters import client_id_calendar, create_table_md
from ..decorators.account_decorators import app_error
from ..sql_app.crud import User, YandexCalendar
from ..sql_app.database import get_conn


@app_error
async def bg_profile(
        mm_user_id: str,
        mm_username: str,
        channel_id: str
):
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
                    conn, principal, YandexCalendar.get_cals(conn, mm_user_id)
                )

                if type(cals) is dict:
                    return cals

                account.update(sync_calendars=', '.join(client_id_calendar(c) for c in cals or 'None'))

    text = create_table_md(account)

    asyncio.create_task(send_ephemeral_msg_client(mm_user_id, channel_id, text))


@app_error
async def bg_create_account(
        mm_user_id: str,
        login: str,
        token: str,
        timezone: str,
):
    async with get_conn() as conn:
        await User.add_user(
            conn,
            mm_user_id=mm_user_id,
            login=login,
            token=token,
            timezone=timezone,
            e_c=False,
            ch_stat=False,
            session=token_hex(16)
        )


@app_error
async def bg_update_account(
        mm_user_id: str,
        login: str,
        token: str,
        timezone: str,
):
    async with get_conn() as conn:
        await asyncio.gather(
            YandexCalendar.remove_cals(conn, mm_user_id),
            User.update_user(
                conn,
                mm_user_id,
                login=login,
                token=token,
                timezone=timezone,
                e_c=False,
                ch_stat=False,
                session=token_hex(16),
            ),
        )


@app_error
async def bg_remove_account(
        mm_user_id: str
):
    async with get_conn() as conn:
        await User.remove_user(conn, mm_user_id)
