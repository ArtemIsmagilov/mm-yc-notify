from datetime import datetime, UTC, timedelta


def is_exist_conf_at_time(dt: datetime) -> bool:
    # now - 10 min < dt < dt + 30 min
    start_point = datetime.now(UTC)
    middle_point = dt.astimezone(UTC)
    end_point = start_point + timedelta(minutes=30)

    return start_point < middle_point < end_point


def start_gt_10_min(start_dt: datetime) -> bool:
    return start_dt.astimezone(UTC) > datetime.now(UTC) + timedelta(minutes=10)


def start_gt_now(start_dt: datetime) -> bool:
    return start_dt.astimezone(UTC) > datetime.now(UTC)
