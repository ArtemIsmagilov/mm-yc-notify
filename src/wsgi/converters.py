from wsgi.calendars.conference import Conference
from wsgi.constants import CONFERENCE_PROPERTIES

from datetime import datetime, UTC
from zoneinfo import ZoneInfo
from sqlalchemy.engine import Row


def get_hours_minutes_with_UTC_from_form(h_m: str, from_timezone: str) -> tuple[str, str]:
    h, m = map(int, h_m.split(":"))

    dt_tz = datetime.now(ZoneInfo(from_timezone)).replace(hour=h, minute=m)
    dt_utc = dt_tz.astimezone(UTC)

    return str(dt_utc.hour), str(dt_utc.minute)


def get_dt_with_UTC_tz_from_iso(iso: str) -> datetime:
    return datetime.fromisoformat(iso).astimezone(UTC)


def iso1_gt_iso2(iso1: str, iso2: str) -> bool:
    first = datetime.fromisoformat(iso1).astimezone(UTC)
    second = datetime.fromisoformat(iso2).astimezone(UTC)
    return first > second


def dont_clear(iso_data: str) -> bool:
    """0001-01-01T00:00:00Z"""
    inf_d = datetime(year=1, month=1, day=1, hour=0, minute=0)
    obj_d = datetime.fromisoformat(iso_data).replace(tzinfo=None)
    return inf_d == obj_d


def create_conference_table(conf_obj: Conference, new_line='   '):
    """
    example table: {'uid': 'id conference', 'timezone': 'UTC', ...}
    """
    table = {}
    for p in CONFERENCE_PROPERTIES:
        v = getattr(conf_obj, p)
        if v:
            if p == "organizer":

                table["organizer"] = "name - {}, email - {}".format(v.get("name"), v.get("email"))

            elif p == "attendee":
                table["attendee"] = "; ".join(", ".join(f"**{attr}** - *{value}*" for attr, value in a.items()) for a in v)

            else:
                brs_v = v.replace("\n", new_line)

                if len(brs_v) > 155:
                    brs_v = "".join((brs_v[:155], "..."))

                table[p] = brs_v

    header, delimiter, body = " | ".join(table.keys()), "-|" * len(table), " | ".join(table.values())

    return f"| {header} |\n|{delimiter}\n| {body} |"


def create_row_table(row_obj: Row, new_line='   '):
    """
    example table: {'uid': 'id conference', 'timezone': 'UTC', ...}
    """
    table = {}
    for p in CONFERENCE_PROPERTIES:
        v = getattr(row_obj, p)
        if v:
            brs_v = v.replace("\n", new_line)

            if len(brs_v) > 155:
                brs_v = "".join((brs_v[:155], "..."))

            table[p] = brs_v

    header, delimiter, body = " | ".join(table.keys()), "-|" * len(table), " | ".join(table.values())

    return f"| {header} |\n|{delimiter}\n| {body} |"
