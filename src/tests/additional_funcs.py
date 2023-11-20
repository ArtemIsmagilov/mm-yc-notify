from app.sql_app.crud import User, YandexCalendar
from app.sql_app.database import get_conn
from settings import Conf
from tests.conftest import mm_user_id


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
            ch_stat=False
        )


async def decrease_user():
    # delete testuser after connection
    async with get_conn() as conn:
        await User.remove_user(conn, mm_user_id)


async def increase_calendar(cal_id: str):
    async with get_conn() as conn:
        await YandexCalendar.add_one_cal(
            conn,
            mm_user_id,
            cal_id,
            cal_id + 'fake_sync_token'
        )


async def decrease_calendar(cal_id: str):
    async with get_conn() as conn:
        await YandexCalendar.remove_cal(conn, cal_id)


async def modify_account(**kwargs):
    async with get_conn() as conn:
        await User.update_user(
            conn,
            mm_user_id,
            **kwargs
        )
