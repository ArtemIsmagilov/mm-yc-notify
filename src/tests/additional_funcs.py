from secrets import token_hex
from datetime import datetime

from app.schemas import UserView
from .conftest import mm_user_id
from app.sql_app.database import get_conn
from app.sql_app.crud import User, YandexCalendar, YandexConference
from settings import Conf


async def increase_user():
    # create test_user connection
    async with get_conn() as conn:
        await User.add_user(
            conn,
            mm_user_id,
            Conf.test_client_ya_login,
            Conf.test_client_ya_token,
            Conf.test_client_ya_timezone,
            e_c=False,
            ch_stat=False,
            session=token_hex(16)
        )


async def decrease_user():
    # delete testuser after connection
    async with get_conn() as conn:
        await User.remove_user(conn, mm_user_id)


async def modify_user(**kwargs):
    async with get_conn() as conn:
        await User.update_user(
            conn,
            mm_user_id,
            **kwargs
        )


async def get_user():
    async with get_conn() as conn:
        user = await User.get_user(conn, mm_user_id)
        if user:
            return UserView(
                mm_user_id=user.mm_user_id,
                login=user.login,
                token=user.token,
                timezone=user.timezone,
                e_c=user.e_c,
                ch_stat=user.ch_stat,
                session=user.session,
                status=user.status,
            )


async def increase_calendar(cal_id: str):
    async with get_conn() as conn:
        await YandexCalendar.add_one_cal(
            conn,
            mm_user_id,
            cal_id,
        )


async def decrease_calendar(cal_id: str):
    async with get_conn() as conn:
        await YandexCalendar.remove_cal(conn, cal_id)


async def get_calendar(cal_id: str):
    async with get_conn() as conn:
        return await YandexCalendar.get_cal(conn, cal_id)


async def increase_conference(
        cal_id: str,
        conf_id: str,
        uid: str,
        timezone: str,
        dtstart: datetime,
        dtend: datetime,
        x_telemost_conference: str,
):
    async with get_conn() as conn:
        await YandexConference.add_conference(
            conn,
            cal_id=cal_id,
            conf_id=conf_id,
            uid=uid,
            timezone=timezone,
            dtstart=dtstart,
            dtend=dtend,
            x_telemost_conference=x_telemost_conference,
        )
