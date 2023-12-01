from sqlalchemy import Table, Column, Integer, String, Boolean, ForeignKey

from ..sql_app.database import metadata_obj

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
    Column("session", String, nullable=False, unique=True),
    Column("status", String),
)

yandex_calendar_table = Table(
    "yandex_calendar",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("mm_user_id", ForeignKey("user_account.mm_user_id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False),
    Column("cal_id", String, nullable=False, unique=True),
    Column("sync_token", String, unique=True),
)

yandex_conference_table = Table(
    "yandex_conference",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("cal_id", ForeignKey("yandex_calendar.cal_id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False),
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
