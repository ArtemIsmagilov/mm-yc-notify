from dataclasses import dataclass


@dataclass
class UserView:
    mm_user_id: str
    login: str
    token: str
    timezone: str
    e_c: bool
    ch_stat: bool
    session: str
    status: str | None

