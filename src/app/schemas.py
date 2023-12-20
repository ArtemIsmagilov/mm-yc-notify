from dataclasses import dataclass
from datetime import datetime


@dataclass
class UserView:
    mm_user_id: str | None = None
    login: str | None = None
    token: str | None = None
    timezone: str | None = None
    e_c: bool | None = None
    ch_stat: bool | None = None
    session: str | None = None
    status: str | None = None


@dataclass
class ConferenceView:
    uid: str | None = None
    dtstart: datetime | None = None
    dtend: datetime | None = None
    summary: str | None = None
    created: str | None = None
    last_modified: str | None = None
    description: str | None = None
    url_event: str | None = None
    categories: str | None = None
    x_telemost_conference: str | None = None
    organizer: dict | None = None
    attendee: list | None = None
    location: str | None = None
    timezone: str | None = None
    recurrence_id: datetime | None = None
    conf_id: str | None = None
