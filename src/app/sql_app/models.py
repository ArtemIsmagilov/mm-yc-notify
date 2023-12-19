import sqlalchemy as sa

from ..sql_app.database import metadata_obj

user_account_table = sa.Table(
    "user_account",
    metadata_obj,
    sa.Column("mm_user_id", sa.String, primary_key=True),
    sa.Column("login", sa.String, nullable=False, unique=True),
    sa.Column("token", sa.String, nullable=False, unique=True),
    sa.Column("timezone", sa.String, nullable=False),
    sa.Column("e_c", sa.Boolean, nullable=False),
    sa.Column("ch_stat", sa.Boolean, nullable=False),
    sa.Column("session", sa.String, nullable=False, unique=True),
    sa.Column("status", sa.String),
)

yandex_calendar_table = sa.Table(
    "yandex_calendar",
    metadata_obj,
    sa.Column("mm_user_id", sa.ForeignKey("user_account.mm_user_id", onupdate="CASCADE", ondelete="CASCADE"),
              nullable=False),
    sa.Column("cal_id", sa.String, primary_key=True),
)

yandex_conference_table = sa.Table(
    "yandex_conference",
    metadata_obj,
    sa.Column("cal_id", sa.ForeignKey("yandex_calendar.cal_id", onupdate="CASCADE", ondelete="CASCADE"),
              nullable=False),
    sa.Column('conf_id', sa.String, primary_key=True),
    sa.Column('uid', sa.String, nullable=False),
    sa.Column('timezone', sa.String, nullable=False),
    sa.Column('dtstart', sa.DateTime(timezone=True), nullable=False),
    sa.Column('dtend', sa.DateTime(timezone=True), nullable=False),
    sa.Column('summary', sa.String),
    sa.Column('created', sa.DateTime(timezone=True)),
    sa.Column('last_modified', sa.DateTime(timezone=True)),
    sa.Column('description', sa.String),
    sa.Column('url_event', sa.String),
    sa.Column('categories', sa.String),
    sa.Column('x_telemost_conference', sa.String, nullable=False),
    sa.Column('organizer', sa.String),
    sa.Column('attendee', sa.String),
    sa.Column('location', sa.String),
    sa.Column('recurrence_id', sa.DateTime(timezone=True)),
)
