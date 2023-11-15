from datetime import datetime, UTC, timedelta


def is_exist_conf_at_time(dt_iso: str) -> bool:
    start_point = datetime.now(UTC)  # before 10 min(dtstart - 10 min)
    middle_point = datetime.fromisoformat(dt_iso).astimezone(UTC)  # dtstart
    end_point = start_point + timedelta(minutes=15)  # before 10 min + 15 min(dtstart - 10 min + 15 min)

    return start_point < middle_point < end_point


def start_gt_15_min(dt_iso: str) -> bool:
    start_point = datetime.fromisoformat(dt_iso).astimezone(UTC)
    end_point = datetime.now(UTC) + timedelta(minutes=15)

    return start_point > end_point


def start_gt_now(dt_iso: str) -> bool:
    now = datetime.now(UTC)
    dt_start = datetime.fromisoformat(dt_iso).astimezone(UTC)

    return dt_start > now
