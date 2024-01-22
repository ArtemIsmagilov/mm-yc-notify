from typing import AsyncGenerator
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy.engine import Row

from ..sql_app.models import (
    user_account_table,
    yandex_calendar_table,
    yandex_conference_table
)


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
            session: str,
            status: str | None = None,
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
                session=session,
                status=status,
            )
        )

    @classmethod
    async def get_user(cls, conn: AsyncConnection, mm_user_id: str) -> Row | None:
        result = await conn.execute(
            user_account_table
            .select()
            .where(user_account_table.c.mm_user_id == mm_user_id)
        )
        return result.first()

    @classmethod
    async def get_user_by_session(cls, conn: AsyncConnection, session: str) -> Row | None:
        result = await conn.execute(
            user_account_table
            .select()
            .where(user_account_table.c.session == session)
        )
        return result.first()

    @classmethod
    async def all_users(cls, conn: AsyncConnection) -> AsyncGenerator[Row, None]:
        result = await conn.stream(
            user_account_table
            .select()
        )
        async for row in result:
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
    async def add_one_cal(cls, conn: AsyncConnection, mm_user_id: str, cal_id: str):
        await conn.execute(
            yandex_calendar_table
            .insert()
            .values(mm_user_id=mm_user_id, cal_id=cal_id)
        )

    @classmethod
    async def add_many_cals(cls, conn: AsyncConnection, cals: list[dict]):
        await conn.execute(
            yandex_calendar_table
            .insert()
            .values(cals)
        )

    @classmethod
    async def get_cal(cls, conn: AsyncConnection, cal_id: str) -> Row | None:
        result = await conn.execute(
            yandex_calendar_table
            .select()
            .where(yandex_calendar_table.c.cal_id == cal_id)
        )
        return result.first()

    @classmethod
    async def get_cals(cls, conn: AsyncConnection, mm_user_id: str) -> AsyncGenerator[Row, None]:
        result = await conn.stream(
            yandex_calendar_table
            .select()
            .where(yandex_calendar_table.c.mm_user_id == mm_user_id)
        )
        async for row in result:
            yield row

    @classmethod
    async def get_first_cal(cls, conn: AsyncConnection, mm_user_id: str) -> Row | None:
        result = await conn.execute(
            yandex_calendar_table
            .select()
            .where(yandex_calendar_table.c.mm_user_id == mm_user_id)
            .limit(1)
        )

        return result.first()

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
    async def get_conference(cls, conn: AsyncConnection, conf_id: str) -> Row | None:
        result = await conn.execute(
            yandex_conference_table
            .select()
            .where(yandex_conference_table.c.conf_id == conf_id)
        )

        return result.first()

    @classmethod
    async def get_first_conference_by_uid_last_modified(
            cls, conn: AsyncConnection, uid: str, last_modified: datetime
    ) -> Row | None:
        result = await conn.execute(
            yandex_conference_table
            .select()
            .where(
                yandex_conference_table.c.uid == uid,
                yandex_conference_table.c.last_modified == last_modified,
            )
            .limit(1)
        )

        return result.first()

    @classmethod
    async def get_first_conference_by_uid(cls, conn: AsyncConnection, uid: str) -> Row | None:
        result = await conn.execute(
            yandex_conference_table
            .select()
            .where(yandex_conference_table.c.uid == uid)
            .limit(1)
        )

        return result.first()

    @classmethod
    async def add_conference(
            cls,
            conn: AsyncConnection,
            cal_id: str,
            conf_id: str,
            uid: str,
            timezone: str,
            dtstart: datetime,
            dtend: datetime,
            summary: str | None = None,
            created: datetime | None = None,
            last_modified: datetime | None = None,
            description: str | None = None,
            url_event: str | None = None,
            categories: str | None = None,
            x_telemost_conference: str | None = None,
            organizer: str | None = None,
            attendee: str | None = None,
            location: str | None = None,
            recurrence_id: datetime | None = None,
    ):
        await conn.execute(
            yandex_conference_table
            .insert()
            .values(
                conf_id=conf_id,
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
                recurrence_id=recurrence_id,
            )
        )

    @classmethod
    async def remove_conference(cls, conn: AsyncConnection, conf_id: str):
        await conn.execute(
            yandex_conference_table
            .delete()
            .where(yandex_conference_table.c.conf_if == conf_id)
        )

    @classmethod
    async def remove_conferences_by_uid(cls, conn: AsyncConnection, uid: str):
        await conn.execute(
            yandex_conference_table
            .delete()
            .where(yandex_conference_table.c.uid == uid)
        )

    @classmethod
    async def remove_conferences_not_in_conf_ids_by_cal_id(
            cls, conn: AsyncConnection, cal_id: str, conf_ids: set) -> AsyncGenerator[Row, None]:
        result = await conn.stream(
            yandex_conference_table
            .delete()
            .where(
                yandex_conference_table.c.conf_id.not_in(conf_ids),
                yandex_conference_table.c.cal_id == cal_id,
            )
            .returning(yandex_conference_table.c)
        )

        async for row in result:
            yield row

    @classmethod
    async def update_conference(cls, conn: AsyncConnection, conf_id: str, **kwargs):
        await conn.execute(
            yandex_conference_table
            .update()
            .where(yandex_conference_table.c.conf_id == conf_id)
            .values(kwargs)
        )
