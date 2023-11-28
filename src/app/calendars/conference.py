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
    )

    def __init__(self, event: Event, timezone: str):
        self._uid: vText = event.get("UID")
        self._dtstart: vDDDTypes = event.get("DTSTART")
        self._dtend: vDDDTypes = event.get("DTEND")
        self._summary: vText = event.get("SUMMARY")
        self._created: vDDDTypes = event.get("CREATED")
        self._last_modified: vDDDTypes = event.get("LAST-MODIFIED")
        self._description: vText = event.get("DESCRIPTION")
        self._url_event: vUri = event.get("URL")
        self._categories: vCategory = event.get("CATEGORIES")
        self._x_telemost_conference: vText = event.get("X-TELEMOST-CONFERENCE")
        self._organizer: vCalAddress = event.get("ORGANIZER")
        self._attendee: list[vCalAddress, ...] = event.get("ATTENDEE")
        self._location: vText = event.get("LOCATION")
        self._timezone: str = timezone

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
location:{self.location!r}\
>"""

    @property
    def uid(self) -> str | None:
        if self._uid:
            return shorten(str(self._uid), 255)

    @property
    def timezone(self) -> str | None:
        return shorten(self._timezone, 255)

    @property
    def dtstart(self) -> str | None:
        if self._dtstart:
            dt = self._dtstart.dt

            if type(dt) is date:
                dt = datetime(year=dt.year, month=dt.month, day=dt.day, tzinfo=ZoneInfo(self.timezone))

            return shorten(dt.astimezone(ZoneInfo(self.timezone)).isoformat(), 255)

    @property
    def dtend(self) -> str | None:
        if self._dtend:
            dt = self._dtend.dt

            if type(dt) is date:
                dt = datetime(year=dt.year, month=dt.month, day=dt.day, tzinfo=ZoneInfo(self.timezone))

            return shorten(dt.astimezone(ZoneInfo(self.timezone)).isoformat(), 255)

    @property
    def summary(self) -> str | None:
        if self._summary:
            return shorten(str(self._summary), 255)

    @property
    def created(self) -> str | None:
        if self._created:
            dt = self._created.dt

            if type(dt) is date:
                dt = datetime(year=dt.year, month=dt.month, day=dt.day, tzinfo=ZoneInfo(self.timezone))

            return shorten(dt.astimezone(ZoneInfo(self.timezone)).isoformat(), 255)

    @property
    def last_modified(self) -> str | None:
        if self._last_modified:
            dt = self._last_modified.dt

            if type(dt) is date:
                dt = datetime(year=dt.year, month=dt.month, day=dt.day, tzinfo=ZoneInfo(self.timezone))

            return shorten(dt.astimezone(ZoneInfo(self.timezone)).isoformat(), 255)

    @property
    def description(self) -> str | None:
        if self._description:
            return shorten(str(self._description), 255)

    @property
    def url_event(self) -> str | None:
        if self._url_event:
            return shorten(str(self._url_event), 255)

    @property
    def categories(self) -> str | None:
        if self._categories:
            return shorten(self._categories.to_ical().decode("utf-8"), 255)

    @property
    def x_telemost_conference(self) -> str | None:
        if self._x_telemost_conference:
            return shorten(str(self._x_telemost_conference), 255)

    @property
    def organizer(self) -> dict[str, str] | None:
        if self._organizer:
            result = {"email": str(self._organizer).removeprefix("mailto:")}

            if self._organizer.params:
                result.update({k.lower(): v for k, v in self._organizer.params.items()})

            return result

    @property
    def attendee(self) -> list[dict[str, str]] | None:
        if self._attendee:
            result = []

            for at in self._attendee:
                at_dict = {"email": at.removeprefix("mailto:")}

                if at.params:
                    at_dict.update({a.lower(): v for a, v in at.params.items()})

                result.append(at_dict)

            return result

    @property
    def location(self) -> str | None:
        if self._location:
            return shorten(str(self._location), 255)
