from .calendars.conference import Conference
from .constants import CONFERENCE_PROPERTIES

from datetime import datetime, UTC
from zoneinfo import ZoneInfo
from sqlalchemy.engine import Row
from caldav import Calendar
import textwrap, caldav
from apscheduler.triggers.cron import CronTrigger


def get_delay_daily(hour: int, minute: int) -> int:
    delay = round(
        (CronTrigger(hour=hour, minute=minute, timezone=UTC).next() - datetime.now(UTC)).total_seconds()) * 1000
    return delay


def get_delay_with_dtstart(dtstart: datetime) -> int:
    delay = round((dtstart.astimezone(UTC) - datetime.now(UTC)).total_seconds()) * 1000
    return delay


def get_h_m_utc(h_m: str, tz: str):
    h, m = map(int, h_m.split(":"))
    dt = datetime.now(ZoneInfo(tz)).replace(hour=h, minute=m).astimezone(UTC)
    return dt.hour, dt.minute


def get_dt_with_UTC_tz_from_iso(iso: datetime) -> datetime:
    return iso.astimezone(UTC)


def iso1_gt_iso2(iso1: str, iso2: str) -> bool:
    first = datetime.fromisoformat(iso1).astimezone(UTC)
    second = datetime.fromisoformat(iso2).astimezone(UTC)
    return first > second


def conference_all_day(conf: Conference):
    start, end = conf.dtstart, conf.dtend
    return (start.hour, start.minute, start.second) == (end.hour, end.minute, end.second) == (0, 0, 0)


def dont_clear(iso_data: str) -> bool:
    """0001-01-01T00:00:00Z"""
    inf_d = datetime(year=1, month=1, day=1, hour=0, minute=0)
    obj_d = datetime.fromisoformat(iso_data).replace(tzinfo=None)
    return inf_d == obj_d


def create_conference_table(conf_obj: Conference) -> str:
    """
    example table: {'uid': 'id conference', 'timezone': 'UTC', ...}
    """
    table = {}
    for p in CONFERENCE_PROPERTIES:
        v = getattr(conf_obj, p)
        if v:
            if p == "organizer":
                v = to_str_organizer(v)

            elif p == "attendee":
                v = to_str_attendee(v)
            v = '%s' % v

            new_v = v.replace("\n", ' ')

            table[p] = textwrap.shorten(new_v, 155)

    return create_table_md(table)


def create_row_table(row_obj: Row, tz: str):
    """
    example table: {'uid': 'id conference', 'timezone': 'UTC', ...}
    """
    table = {}
    for p in CONFERENCE_PROPERTIES:
        v = getattr(row_obj, p)
        if v:
            if type(v) is datetime:
                v = v.astimezone(ZoneInfo(tz))
            v = '%s' % v

            new_v = v.replace("\n", ' ')
            table[p] = textwrap.shorten(new_v, 155)

    return create_table_md(table)


def equal_conferences(conf: Conference | Row, other_conf: Conference | Row):
    for p in CONFERENCE_PROPERTIES:
        if p in ("organizer", "attendee", "last_modified"):
            continue
        if getattr(conf, p) != getattr(other_conf, p):
            return False
    return True


def past_conference(conf: Conference | Row):
    return conf.dtend.astimezone(UTC) < datetime.now(UTC)


def create_table_md(table: dict) -> str:
    header, delimiter, body = " | ".join(table.keys()), "-|" * len(table), " | ".join(table.values())

    return f"| {header} |\n|{delimiter}\n| {body} |"


def hex_color_calendar(cal: Calendar):
    color = cal.get_properties([caldav.elements.ical.CalendarColor()])
    _, hex_color = color.popitem()

    return hex_color


def client_hex_calendar(cal: Calendar):
    pass


def client_id_calendar(c: Calendar) -> str:
    return '%s(%s)' % (str(c), c.id)


def to_str_attendee(v: list):
    return "; ".join(", ".join(f"**{attr}** - *{value}*" for attr, value in a.items()) for a in v)


def to_str_organizer(v: dict):
    return ", ".join(f"**{attr}** - *{value}*" for attr, value in v.items())