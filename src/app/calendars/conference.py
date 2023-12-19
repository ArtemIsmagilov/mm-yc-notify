from icalendar.prop import vCategory, vText, vDDDTypes, vCalAddress, vUri
from icalendar import Event
from zoneinfo import ZoneInfo
from datetime import datetime, date
from textwrap import shorten


class Conference:
    __slots__ = (
        "_uid",
        "_dtstart",
        "_dtend",
        "_summary",
        "_created",
        "_last_modified",
        "_description",
        "_url_event",
        "_categories",
        "_x_telemost_conference",
        "_organizer",
        "_attendee",
        "_location",
        "_timezone",
        "_recurrence_id",
    )

    def __init__(self, event: Event, timezone: str):
        self._uid: vText | None = event.get("UID")
        self._dtstart: vDDDTypes | None = event.get("DTSTART")
        self._dtend: vDDDTypes | None = event.get("DTEND")
        self._summary: vText | None = event.get("SUMMARY")
        self._created: vDDDTypes | None = event.get("CREATED")
        self._last_modified: vDDDTypes | None = event.get("LAST-MODIFIED")
        self._description: vText | None = event.get("DESCRIPTION")
        self._url_event: vUri | None = event.get("URL")
        self._categories: vCategory | None = event.get("CATEGORIES")
        self._x_telemost_conference: vText | None = event.get("X-TELEMOST-CONFERENCE")
        self._organizer: vCalAddress | None = event.get("ORGANIZER")
        self._attendee: list[vCalAddress] | None = event.get("ATTENDEE")
        self._location: vText | None = event.get("LOCATION")
        self._timezone: str = timezone
        self._recurrence_id: list[vDDDTypes] | vDDDTypes | None = event.get('RECURRENCE-ID')

    def __repr__(self):
        return f"""
<Conference \
uid:{self.uid!r} \
timezone:{self.timezone} \
dtstart:{self.dtstart!r} \
dtend:{self.dtend!r} \
summary:{self.summary!r} \
created:{self.created!r} \
last_modified:{self.last_modified!r} \
description:{self.description!r} \
url_event:{self.url_event!r} \
categories:{self.categories!r} \
x_telemost_conference:{self.x_telemost_conference!r} \
organizer:{self.organizer!r} \
attendee:{self.attendee!r} \
location:{self.location!r} \
recurrence_id:{self.recurrence_id!r} \
>"""

    @property
    def uid(self) -> str | None:
        if self._uid:
            return shorten(str(self._uid), 255)

    @property
    def timezone(self) -> str | None:
        return shorten(self._timezone, 255)

    @property
    def dtstart(self) -> datetime | None:
        attribute = self._dtstart
        if attribute:
            dt = attribute.dt

            if type(dt) is date:
                dt = datetime(year=dt.year, month=dt.month, day=dt.day, tzinfo=ZoneInfo(self.timezone))

            return dt.astimezone(ZoneInfo(self.timezone))

    @property
    def dtend(self) -> datetime | None:
        attribute = self._dtend
        if attribute:
            dt = attribute.dt

            if type(dt) is date:
                dt = datetime(year=dt.year, month=dt.month, day=dt.day, tzinfo=ZoneInfo(self.timezone))

            return dt.astimezone(ZoneInfo(self.timezone))

    @property
    def summary(self) -> str | None:
        attribute = self._summary
        if attribute:
            return shorten(str(attribute), 255)

    @property
    def created(self) -> datetime | None:
        attribute = self._created
        if attribute:
            dt = attribute.dt

            if type(dt) is date:
                dt = datetime(year=dt.year, month=dt.month, day=dt.day, tzinfo=ZoneInfo(self.timezone))

            return dt.astimezone(ZoneInfo(self.timezone))

    @property
    def last_modified(self) -> datetime | None:
        attribute = self._last_modified
        if attribute:
            dt = attribute.dt

            if type(dt) is date:
                dt = datetime(year=dt.year, month=dt.month, day=dt.day, tzinfo=ZoneInfo(self.timezone))

            return dt.astimezone(ZoneInfo(self.timezone))

    @property
    def description(self) -> str | None:
        attribute = self._description
        if attribute:
            return shorten(str(attribute), 255)

    @property
    def url_event(self) -> str | None:
        attribute = self._url_event
        if attribute:
            return shorten(str(attribute), 255)

    @property
    def categories(self) -> str | None:
        attribute = self._categories
        if attribute:
            return shorten(attribute.to_ical().decode("utf-8"), 255)

    @property
    def x_telemost_conference(self) -> str | None:
        attribute = self._x_telemost_conference
        if attribute:
            return shorten(str(attribute), 255)

    @property
    def organizer(self) -> dict[str, str] | None:
        attribute = self._organizer
        if attribute:
            result = {"email": str(attribute).removeprefix("mailto:")}

            if attribute.params:
                result.update({k.lower(): v for k, v in attribute.params.items()})

            return result

    @property
    def attendee(self) -> list[dict[str, str]] | None:
        attribute = self._attendee
        if attribute:
            result = []

            for at in attribute:
                at_dict = {"email": at.removeprefix("mailto:")}

                if at.params:
                    at_dict.update({a.lower(): v for a, v in at.params.items()})

                result.append(at_dict)

            return result

    @property
    def location(self) -> str | None:
        attribute = self._location
        if attribute:
            return shorten(str(attribute), 255)

    @property
    def recurrence_id(self) -> datetime | None:
        attribute = self._recurrence_id
        if attribute:
            if type(attribute) is list:
                dt = attribute[0].dt
            else:
                dt = attribute.dt

            if type(dt) is date:
                dt = datetime(year=dt.year, month=dt.month, day=dt.day, tzinfo=ZoneInfo(self.timezone))
            return dt.astimezone(ZoneInfo(self.timezone))

    @property
    def conf_id(self) -> str:
        return f'{self.uid}__{self.recurrence_id}'
