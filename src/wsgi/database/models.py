from wsgi.settings import DB_URL

from sqlalchemy import (
    MetaData, Table, Column, Integer, String, Boolean, ForeignKey, create_engine
)

engine = create_engine(DB_URL)
metadata_obj = MetaData()


class User:
    user_account_table = Table(
        "user_account",
        metadata_obj,
        Column("id", Integer, primary_key=True),
        Column("mm_user_id", String, nullable=False, unique=True),
        Column("login", String, nullable=False),
        Column("token", String, nullable=False, unique=True),
        Column("timezone", String, nullable=False),
        Column("e_c", Boolean, nullable=False),
        Column("ch_stat", Boolean, nullable=False),
    )

    @classmethod
    def add_user(cls, **kwargs):
        with engine.begin() as connection:
            c = cls.user_account_table.columns

            result = connection.execute(
                cls.user_account_table
                .insert()
                .values(kwargs)
                .returning(c)
            )

        return result.first()

    @classmethod
    def get_user(cls, **kwargs):
        col, val = kwargs.popitem()

        with engine.begin() as connection:
            c = cls.user_account_table.columns

            result = connection.execute(
                cls.user_account_table
                .select()
                .where(getattr(c, col) == val)
            )

        return result.first()

    @classmethod
    def remove_user(cls, **kwargs):
        col, val = kwargs.popitem()

        with engine.begin() as connection:
            c = cls.user_account_table.columns

            result = connection.execute(
                cls.user_account_table
                .delete()
                .where(getattr(c, col) == val)
                .returning(c)
            )

        return result.first()

    @classmethod
    def update_user(cls, **kwargs):
        with engine.begin() as connection:
            c = cls.user_account_table.columns

            result = connection.execute(
                cls.user_account_table
                .update()
                .where(c.mm_user_id == kwargs['mm_user_id'])
                .values(kwargs)
                .returning(c)
            )

        return result.first()

    def __init__(self, **kwargs):
        [setattr(self, col, val) for col, val in kwargs.items()]

    def save(self):
        return User.add_user(self.mm_user_id, self.login, self.token, self.timezone, self.e_c, self.ch_stat)


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
        Column("sync_token", String, ),
    )

    @classmethod
    def add_one_cal(cls, **kwargs):
        with engine.begin() as connection:
            c = cls.yandex_calendar_table.columns

            result = connection.execute(
                cls.yandex_calendar_table
                .insert()
                .values(kwargs)
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
    def get_cal(cls, **kwargs):
        col, val = kwargs.popitem()

        with engine.begin() as connection:
            c = cls.yandex_calendar_table.columns

            result = connection.execute(
                cls.yandex_calendar_table
                .select()
                .where(getattr(c, col) == val)
            )

        return result.first()

    @classmethod
    def get_cals(cls, **kwargs):
        col, val = kwargs.popitem()

        with engine.begin() as connection:
            c = cls.yandex_calendar_table.columns

            result = connection.execute(
                cls.yandex_calendar_table
                .select()
                .where(getattr(c, col) == val)
            )

        return result.all()

    @classmethod
    def remove_cal(cls, **kwargs):
        col, val = kwargs.popitem()

        with engine.begin() as connection:
            c = cls.yandex_calendar_table.columns

            result = connection.execute(
                cls.yandex_calendar_table
                .delete()
                .where(getattr(c, col) == val)
                .returning(c)
            )

        return result.first()

    @classmethod
    def remove_cals(cls, **kwargs):
        col, val = kwargs.popitem()

        with engine.begin() as connection:
            c = cls.yandex_calendar_table.columns

            result = connection.execute(
                cls.yandex_calendar_table
                .delete()
                .where(getattr(c, col) == val)
                .returning(c)
            )

        return result.all()

    @classmethod
    def update_cal(cls, **kwargs):
        with engine.begin() as connection:
            c = cls.yandex_calendar_table.columns

            result = connection.execute(
                cls.yandex_calendar_table
                .update()
                .where(c.cal_id == kwargs.get('cal_id'))
                .values(kwargs)
                .returning(c)
            )

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
    def get_conference(cls, **kwargs):
        col, val = kwargs.popitem()

        with engine.begin() as connection:
            c = cls.yandex_conference_table.columns

            result = connection.execute(
                cls.yandex_conference_table
                .select()
                .where(getattr(c, col) == val)
            )

        return result.first()

    @classmethod
    def add_conference(cls, **kwargs):
        with engine.begin() as connection:
            c = cls.yandex_conference_table.columns

            result = connection.execute(
                cls.yandex_conference_table
                .insert()
                .values(kwargs)
                .returning(c)
            )

        return result.first()

    @classmethod
    def remove_conference(cls, **kwargs):
        col, val = kwargs.popitem()

        with engine.begin() as connection:
            c = cls.yandex_conference_table.columns

            result = connection.execute(
                cls.yandex_conference_table
                .delete()
                .where(getattr(c, col) == val)
                .returning(c)
            )

        return result.first()

    @classmethod
    def update_conference(cls, **kwargs):
        with engine.begin() as connection:
            c = cls.yandex_conference_table.columns

            result = connection.execute(
                cls.yandex_conference_table
                .update()
                .where(c.uid == kwargs.get('uid'))
                .values(kwargs)
                .returning(c)
            )

        return result.first()
