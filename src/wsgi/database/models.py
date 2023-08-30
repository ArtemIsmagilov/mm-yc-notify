from wsgi.settings import DB_URL

from sqlalchemy import (
    MetaData, Table, Column, Integer, String, Boolean, ForeignKey, create_engine, text
)

engine = create_engine(DB_URL)
metadata_obj = MetaData()


class User:
    user_account_table = Table(
        "user_account",
        metadata_obj,
        Column("id", Integer, primary_key=True),
        Column("mm_user_id", String, nullable=False, unique=True),
        Column("login", String, nullable=False, unique=True),
        Column("token", String, nullable=False, unique=True),
        Column("timezone", String, nullable=False),
        Column("e_c", Boolean, nullable=False),
        Column("ch_stat", Boolean, nullable=False),
    )

    @classmethod
    def add_user(cls, mm_user_id: str, login: str, token: str, timezone: str, e_c: bool, ch_stat: bool):
        with engine.begin() as connection:
            c = cls.user_account_table.columns

            result = connection.execute(
                cls.user_account_table
                .insert()
                .values(mm_user_id=mm_user_id, login=login, token=token, timezone=timezone, e_c=e_c, ch_stat=ch_stat)
                .returning(c)
            )

        return result.first()

    @classmethod
    def get_user(cls, mm_user_id: str):
        with engine.begin() as connection:
            c = cls.user_account_table.columns

            result = connection.execute(
                cls.user_account_table
                .select()
                .where(c.mm_user_id == mm_user_id)
            )

        return result.first()

    @classmethod
    def remove_user(cls, mm_user_id: str):
        with engine.begin() as connection:
            c = cls.user_account_table.columns

            result = connection.execute(
                cls.user_account_table
                .delete()
                .where(c.mm_user_id == mm_user_id)
                .returning(c)
            )

        return result.first()

    @classmethod
    def update_user(cls, mm_user_id: str, **kwargs):
        with engine.begin() as connection:
            c = cls.user_account_table.columns

            result = connection.execute(
                cls.user_account_table
                .update()
                .where(c.mm_user_id == mm_user_id)
                .values(kwargs)
                .returning(c)
            )

        return result.first()

    def __init__(self, mm_user_id, login, token, timezone, e_c=False, ch_stat=False):
        self.mm_user_id = mm_user_id
        self.login = login
        self.token = token
        self.timezone = timezone
        self.e_c = e_c
        self.ch_stat = ch_stat


class YandexCalendar:
    yandex_calendar_table = Table(
        "yandex_calendar",
        metadata_obj,
        Column("id", Integer, primary_key=True),
        Column(
            "user_id",
            ForeignKey("user_account.id", onupdate="CASCADE", ondelete="CASCADE"),
            nullable=False
        ),
        Column("cal_id", String, nullable=False, unique=True),
        Column("sync_token", String, unique=True),
    )

    @classmethod
    def add_one_cal(cls, user_id: int, cal_id: str, sync_token: str):
        with engine.begin() as connection:
            c = cls.yandex_calendar_table.columns

            result = connection.execute(
                cls.yandex_calendar_table
                .insert()
                .values(user_id=user_id, cal_id=cal_id, sync_token=sync_token)
                .returning(c)
            )

        return result.first()

    @classmethod
    def add_many_cals(cls, cals: list[dict, ...]):
        with engine.begin() as connection:
            c = cls.yandex_calendar_table.columns

            result = connection.execute(
                cls.yandex_calendar_table
                .insert()
                .values(cals)
                .returning(c)
            )

        return result.all()

    @classmethod
    def get_cal(cls, cal_id: str):
        with engine.begin() as connection:
            c = cls.yandex_calendar_table.columns

            result = connection.execute(
                cls.yandex_calendar_table
                .select()
                .where(c.cal_id == cal_id)
            )

        return result.first()

    @classmethod
    def get_cals(cls, user_id: int):
        with engine.begin() as connection:
            c = cls.yandex_calendar_table.columns

            result = connection.execute(
                cls.yandex_calendar_table
                .select()
                .where(c.user_id == user_id)
            )

        return result.all()

    @classmethod
    def remove_cal(cls, cal_id: str):
        with engine.begin() as connection:
            c = cls.yandex_calendar_table.columns

            result = connection.execute(
                cls.yandex_calendar_table
                .delete()
                .where(c.cal_id == cal_id)
                .returning(c)
            )

        return result.first()

    @classmethod
    def remove_cals(cls, user_id: int):
        with engine.begin() as connection:
            c = cls.yandex_calendar_table.columns

            result = connection.execute(
                cls.yandex_calendar_table
                .delete()
                .where(c.user_id == user_id)
                .returning(c)
            )

        return result.all()

    @classmethod
    def update_cal(cls, cal_id: str, **kwargs):
        with engine.begin() as connection:
            c = cls.yandex_calendar_table.columns

            result = connection.execute(
                cls.yandex_calendar_table
                .update()
                .where(c.cal_id == cal_id)
                .values(kwargs)
                .returning(c)
            )

        return result.first()

    @classmethod
    def custom_stmt(cls, stmt: str, params: dict | list):
        with engine.begin() as connection:
            result = connection.execute(stmt, params)

        return result.first()


class YandexConference:
    yandex_conference_table = Table(
        "yandex_conference",
        metadata_obj,
        Column("id", Integer, primary_key=True),
        Column(
            "cal_id",
            ForeignKey("yandex_calendar.cal_id", onupdate="CASCADE", ondelete="CASCADE"),
            nullable=False
        ),
        Column('uid', String, nullable=False, unique=True),
        Column('timezone', String, nullable=False),
        Column('dtstart', String, nullable=False),
        Column('dtend', String, nullable=False),
        Column('summary', String),
        Column('created', String),
        Column('last_modified', String),
        Column('description', String),
        Column('url_event', String),
        Column('categories', String),
        Column('x_telemost_conference', String),
        Column('organizer', String),
        Column('attendee', String),
        Column('location', String),
    )

    @classmethod
    def get_conference(cls, uid: str):
        with engine.begin() as connection:
            c = cls.yandex_conference_table.columns

            result = connection.execute(
                cls.yandex_conference_table
                .select()
                .where(c.uid == uid)
            )

        return result.first()

    @classmethod
    def add_conference(cls,
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
        with engine.begin() as connection:
            c = cls.yandex_conference_table.columns

            result = connection.execute(
                cls.yandex_conference_table
                .insert()
                .values(cal_id=cal_id,
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
                .returning(c)
            )

        return result.first()

    @classmethod
    def remove_conference(cls, uid: str):
        with engine.begin() as connection:
            c = cls.yandex_conference_table.columns

            result = connection.execute(
                cls.yandex_conference_table
                .delete()
                .where(c.uid == uid)
                .returning(c)
            )

        return result.first()

    @classmethod
    def update_conference(cls, uid: str, **kwargs):
        with engine.begin() as connection:
            c = cls.yandex_conference_table.columns

            result = connection.execute(
                cls.yandex_conference_table
                .update()
                .where(c.uid == uid)
                .values(kwargs)
                .returning(c)
            )

        return result.first()
