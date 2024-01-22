from zoneinfo import ZoneInfo
from datetime import datetime, date
from textwrap import shorten

from icalendar.prop import (
    vCategory,
    vText,
    vDDDTypes,
    vCalAddress,
    vUri
)
from icalendar import Event


def _set_uid(attribute: vText | None) -> str | None:
    if attribute:
        return shorten(str(attribute), 255)


def _set_dtstart(tz: str, attribute: vDDDTypes | None) -> datetime | None:
    if attribute:
        dt = attribute.dt

        if type(dt) is date:
            dt = datetime(year=dt.year, month=dt.month, day=dt.day, tzinfo=ZoneInfo(tz))

        return dt.astimezone(ZoneInfo(tz))


def _set_dtend(tz: str, attribute: vDDDTypes | None) -> datetime | None:
    if attribute:
        dt = attribute.dt

        if type(dt) is date:
            dt = datetime(year=dt.year, month=dt.month, day=dt.day, tzinfo=ZoneInfo(tz))

        return dt.astimezone(ZoneInfo(tz))


def _set_summary(attribute: vText | None) -> str | None:
    if attribute:
        return shorten(str(attribute), 255)


def _set_created(tz: str, attribute: vDDDTypes | None) -> datetime | None:
    if attribute:
        dt = attribute.dt

        if type(dt) is date:
            dt = datetime(year=dt.year, month=dt.month, day=dt.day, tzinfo=ZoneInfo(tz))

        return dt.astimezone(ZoneInfo(tz))


def _set_last_modified(tz: str, attribute: vDDDTypes | None) -> datetime | None:
    if attribute:
        dt = attribute.dt

        if type(dt) is date:
            dt = datetime(year=dt.year, month=dt.month, day=dt.day, tzinfo=ZoneInfo(tz))

        return dt.astimezone(ZoneInfo(tz))


def _set_description(attribute: vText | None) -> str | None:
    if attribute:
        return shorten(str(attribute), 255)


def _set_url_event(attribute: vUri | None) -> str | None:
    if attribute:
        return shorten(str(attribute), 255)


def _set_categories(attribute: vCategory | None) -> str | None:
    if attribute:
        return shorten(', '.join(attribute.cats), 255)


def _set_x_telemost_conference(attribute: vText | None) -> str | None:
    if attribute:
        return shorten(str(attribute), 255)


def _set_organizer(attribute: vCalAddress | None) -> dict[str, str] | None:
    if attribute:
        result = {"email": str(attribute).removeprefix("mailto:")}

        if attribute.params:
            result.update({k.lower(): v for k, v in attribute.params.items()})

        return result


def _set_attendee(attribute: list[vCalAddress] | None) -> list[dict[str, str]] | None:
    if attribute:
        result = []

        for at in attribute:
            at_dict = {"email": at.removeprefix("mailto:")}

            if at.params:
                at_dict.update({a.lower(): v for a, v in at.params.items()})

            result.append(at_dict)

        return result


def _set_location(attribute: vText | None) -> str | None:
    if attribute:
        return shorten(str(attribute), 255)


def _set_recurrence_id(tz: str, attribute: list[vDDDTypes] | vDDDTypes | None) -> datetime | None:
    if attribute:
        if type(attribute) is list:
            dt = attribute[0].dt
        else:
            dt = attribute.dt

        if type(dt) is date:
            dt = datetime(year=dt.year, month=dt.month, day=dt.day, tzinfo=ZoneInfo(tz))
        return dt.astimezone(ZoneInfo(tz))


def _set_conf_id(uid: str, recurrence_id: datetime) -> str:
    return f'{uid}__{recurrence_id}'


class Conference:
    __slots__ = (
        "uid",
        "dtstart",
        "dtend",
        "summary",
        "created",
        "last_modified",
        "description",
        "url_event",
        "categories",
        "x_telemost_conference",
        "organizer",
        "attendee",
        "location",
        "timezone",
        "recurrence_id",
        "conf_id",
    )

    def __init__(self, event: Event, timezone: str):
        self.timezone: str = timezone
        self.uid = _set_uid(event.get("UID"))
        self.dtstart = _set_dtstart(self.timezone, event.get("DTSTART"))
        self.dtend = _set_dtend(self.timezone, event.get("DTEND"))
        self.summary = _set_summary(event.get("SUMMARY"))
        self.created = _set_created(self.timezone, event.get("CREATED"))
        self.last_modified = _set_last_modified(self.timezone, event.get("LAST-MODIFIED"))
        self.description = _set_description(event.get("DESCRIPTION"))
        self.url_event = _set_url_event(event.get("URL"))
        self.categories = _set_categories(event.get("CATEGORIES"))
        self.x_telemost_conference = _set_x_telemost_conference(event.get("X-TELEMOST-CONFERENCE"))
        self.organizer = _set_organizer(event.get("ORGANIZER"))
        self.attendee = _set_attendee(event.get("ATTENDEE"))
        self.location = _set_location(event.get("LOCATION"))
        self.recurrence_id = _set_recurrence_id(self.timezone, event.get('RECURRENCE-ID'))
        self.conf_id = _set_conf_id(self.uid, self.recurrence_id)

    def __repr__(self):
        return f"""\
Conference(\
uid={self.uid!r} \
timezone={self.timezone} \
dtstart={self.dtstart!r} \
dtend={self.dtend!r} \
summary={self.summary!r} \
created={self.created!r} \
last_modified={self.last_modified!r} \
description={self.description!r} \
url_event={self.url_event!r} \
categories={self.categories!r} \
x_telemost_conference={self.x_telemost_conference!r} \
organizer={self.organizer!r} \
attendee={self.attendee!r} \
location={self.location!r} \
recurrence_id={self.recurrence_id!r} \
conf_id={self.conf_id!r}\
)"""
