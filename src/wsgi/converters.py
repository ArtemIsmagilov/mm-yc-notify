from datetime import datetime, UTC
from zoneinfo import ZoneInfo


def get_hours_minutes_with_UTC_from_form(h_m: str, from_timezone: str) -> tuple[str, str]:
    h, m = map(int, h_m.split(':'))

    dt_tz = datetime.now(ZoneInfo(from_timezone)).replace(hour=h, minute=m)
    dt_utc = dt_tz.astimezone(UTC)

    return str(dt_utc.hour), str(dt_utc.minute)


def get_dt_with_UTC_tz_from_iso(dt: str) -> datetime:
    return datetime.fromisoformat(dt).astimezone(UTC)


def get_dt_with_user_tz_from_iso(dt: str) -> datetime:
    return datetime.fromisoformat(dt)
