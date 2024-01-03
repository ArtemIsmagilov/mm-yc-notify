from datetime import datetime
from sqlalchemy import Row
from dataclasses import dataclass


class UserInDb:
    def __init__(self, user: Row):
        self.mm_user_id: str | None = user.mm_user_id
        self.login: str | None = user.login
        self.token: str | None = user.token
        self.timezone: str | None = user.timezone
        self.e_c: bool | None = user.e_c
        self.ch_stat: bool | None = user.ch_stat
        self.session: str | None = user.session
        self.status: str | None = user.status


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
