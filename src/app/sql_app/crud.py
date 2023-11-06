from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy.engine import Row
from sqlalchemy import select

from ..sql_app.models import user_account_table, yandex_calendar_table, yandex_conference_table


class User:
    @classmethod
    async def add_user(
            cls,
            conn: AsyncConnection,
            mm_user_id: str,
            login: str,
            token: str,
            timezone: str,
            e_c: bool,
            ch_stat: bool,
            status: str = None,
    ):
        await conn.execute(
            user_account_table
            .insert()
            .values(
                mm_user_id=mm_user_id,
                login=login,
                token=token,
                timezone=timezone,
                e_c=e_c,
                ch_stat=ch_stat,
                status=status,
            )
        )

    @classmethod
    async def get_user(cls, conn: AsyncConnection, mm_user_id: str) -> Row:
        result = await conn.execute(
            select(
                user_account_table.c['mm_user_id', 'login', 'token', 'token', 'timezone', 'e_c', 'ch_stat', 'status'])
            .where(user_account_table.c.mm_user_id == mm_user_id)
        )
        return result.first()

    @classmethod
    async def all_users(cls, conn: AsyncConnection) -> AsyncGenerator[Row, None]:
        result = await conn.execute(
            select(
                user_account_table.c['mm_user_id', 'login', 'token', 'token', 'timezone', 'e_c', 'ch_stat', 'status']
            )
        )
        for row in result:
            yield row

    @classmethod
    async def remove_user(cls, conn: AsyncConnection, mm_user_id: str):
        await conn.execute(
            user_account_table
            .delete()
            .where(user_account_table.c.mm_user_id == mm_user_id)
        )

    @classmethod
    async def update_user(cls, conn: AsyncConnection, mm_user_id: str, **kwargs):
        await conn.execute(
            user_account_table
            .update()
            .where(user_account_table.c.mm_user_id == mm_user_id)
            .values(kwargs)
        )


class YandexCalendar:

    @classmethod
    async def add_one_cal(cls, conn: AsyncConnection, mm_user_id: str, cal_id: str, sync_token: str):
        await conn.execute(
            yandex_calendar_table
            .insert()
            .values(mm_user_id=mm_user_id, cal_id=cal_id, sync_token=sync_token)
        )

    @classmethod
    async def add_many_cals(cls, conn: AsyncConnection, cals: list[dict]):
        await conn.execute(
            yandex_calendar_table
            .insert()
            .values(cals)
        )


    @classmethod
    async def get_cal(cls, conn: AsyncConnection, cal_id: str) -> Row:
        result = await conn.execute(
            select(yandex_calendar_table.c['mm_user_id', 'cal_id', 'sync_token'])
            .where(yandex_calendar_table.c.cal_id == cal_id)
        )
        return result.first()

    @classmethod
    async def get_cals(cls, conn: AsyncConnection, mm_user_id: str) -> AsyncGenerator[Row, None]:
        result = await conn.execute(
            select(yandex_calendar_table.c['mm_user_id', 'cal_id', 'sync_token'])
            .where(yandex_calendar_table.c.mm_user_id == mm_user_id)
        )
        for row in result:
            yield row

    @classmethod
    async def get_first_cal(cls, conn: AsyncConnection, mm_user_id: str) -> Row:
        result = await conn.execute(
            select(yandex_calendar_table.c['mm_user_id', 'cal_id', 'sync_token'])
            .where(yandex_calendar_table.c.mm_user_id == mm_user_id)
            .limit(1)
        )

        data = result.first()

        return data

    @classmethod
    async def remove_cal(cls, conn: AsyncConnection, cal_id: str):
        await conn.execute(
            yandex_calendar_table
            .delete()
            .where(yandex_calendar_table.c.cal_id == cal_id)
        )

    @classmethod
    async def remove_cals(cls, conn: AsyncConnection, mm_user_id: str):
        await conn.execute(
            yandex_calendar_table
            .delete()
            .where(yandex_calendar_table.c.mm_user_id == mm_user_id)
        )

    @classmethod
    async def update_cal(cls, conn: AsyncConnection, cal_id: str, **kwargs):
        await conn.execute(
            yandex_calendar_table
            .update()
            .where(yandex_calendar_table.c.cal_id == cal_id)
            .values(kwargs)
        )


class YandexConference:

    @classmethod
    async def get_conference(cls, conn: AsyncConnection, uid: str) -> Row:
        result = await conn.execute(
            yandex_conference_table
            .select()
            .where(yandex_conference_table.c.uid == uid)
        )

        return result.first()

    @classmethod
    async def add_conference(
            cls,
            conn: AsyncConnection,
            cal_id: str,
            uid: str,
            timezone: str,
            dtstart: str,
            dtend: str,
            summary: str = None,
            created: str = None,
            last_modified: str = None,
            description: str = None,
            url_event: str = None,
            categories: str = None,
            x_telemost_conference: str = None,
            organizer: str = None,
            attendee: str = None,
            location: str = None,
    ):
        await conn.execute(
            yandex_conference_table
            .insert()
            .values(
                cal_id=cal_id,
                uid=uid,
                timezone=timezone,
                dtstart=dtstart,
                dtend=dtend,
                summary=summary,
                created=created,
                last_modified=last_modified,
                description=description,
                url_event=url_event,
                categories=categories,
                x_telemost_conference=x_telemost_conference,
                organizer=organizer,
                attendee=attendee,
                location=location,
            )
        )

    @classmethod
    async def remove_conference(cls, conn: AsyncConnection, uid: str) -> Row:
        result = await conn.execute(
            yandex_conference_table
            .delete()
            .where(yandex_conference_table.c.uid == uid)
            .returning(yandex_conference_table.c)
        )

        return result.first()

    @classmethod
    async def update_conference(cls, conn: AsyncConnection, uid: str, **kwargs):
        await conn.execute(
            yandex_conference_table
            .update()
            .where(yandex_conference_table.c.uid == uid)
            .values(kwargs)
        )
