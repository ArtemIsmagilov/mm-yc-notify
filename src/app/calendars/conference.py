from icalendar.prop import vCategory, vText, vDDDTypes, vCalAddress, vUri
from icalendar import Event
from zoneinfo import ZoneInfo
from datetime import datetime, date
from textwrap import shorten


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
        self.uid: str | None = self._set_uid(event.get("UID"))
        self.dtstart: datetime | None = self._set_dtstart(event.get("DTSTART"))
        self.dtend: datetime | None = self._set_dtend(event.get("DTEND"))
        self.summary: str | None = self._set_summary(event.get("SUMMARY"))
        self.created: datetime | None = self._set_created(event.get("CREATED"))
        self.last_modified: datetime | None = self._set_last_modified(event.get("LAST-MODIFIED"))
        self.description: str | None = self._set_description(event.get("DESCRIPTION"))
        self.url_event: str | None = self._set_url_event(event.get("URL"))
        self.categories: str | None = self._set_categories(event.get("CATEGORIES"))
        self.x_telemost_conference: str | None = self._set_x_telemost_conference(event.get("X-TELEMOST-CONFERENCE"))
        self.organizer: dict | None = self._set_organizer(event.get("ORGANIZER"))
        self.attendee: list[dict] | None = self._set_attendee(event.get("ATTENDEE"))
        self.location: str | None = self._set_location(event.get("LOCATION"))
        self.recurrence_id: datetime | None = self._set_recurrence_id(event.get('RECURRENCE-ID'))
        self.conf_id: str | None = self._set_conf_id()

    def __repr__(self):
        return f"""<\
Conference \
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
conf_id:{self.conf_id!r} \
>"""

    def _set_uid(self, attribute: vText | None) -> str | None:
        if attribute:
            return shorten(str(attribute), 255)

    def _set_dtstart(self, attribute: vDDDTypes | None) -> datetime | None:
        if attribute:
            dt = attribute.dt

            if type(dt) is date:
                dt = datetime(year=dt.year, month=dt.month, day=dt.day, tzinfo=ZoneInfo(self.timezone))

            return dt.astimezone(ZoneInfo(self.timezone))

    def _set_dtend(self, attribute: vDDDTypes | None) -> datetime | None:
        if attribute:
            dt = attribute.dt

            if type(dt) is date:
                dt = datetime(year=dt.year, month=dt.month, day=dt.day, tzinfo=ZoneInfo(self.timezone))

            return dt.astimezone(ZoneInfo(self.timezone))

    def _set_summary(self, attribute: vText | None) -> str | None:
        if attribute:
            return shorten(str(attribute), 255)

    def _set_created(self, attribute: vDDDTypes | None) -> datetime | None:
        if attribute:
            dt = attribute.dt

            if type(dt) is date:
                dt = datetime(year=dt.year, month=dt.month, day=dt.day, tzinfo=ZoneInfo(self.timezone))

            return dt.astimezone(ZoneInfo(self.timezone))

    def _set_last_modified(self, attribute: vDDDTypes | None) -> datetime | None:
        if attribute:
            dt = attribute.dt

            if type(dt) is date:
                dt = datetime(year=dt.year, month=dt.month, day=dt.day, tzinfo=ZoneInfo(self.timezone))

            return dt.astimezone(ZoneInfo(self.timezone))

    def _set_description(self, attribute: vText | None) -> str | None:
        if attribute:
            return shorten(str(attribute), 255)

    def _set_url_event(self, attribute: vUri | None) -> str | None:
        if attribute:
            return shorten(str(attribute), 255)

    def _set_categories(self, attribute: vCategory | None) -> str | None:
        if attribute:
            return shorten(attribute.to_ical().decode("utf-8"), 255)

    def _set_x_telemost_conference(self, attribute: vText | None) -> str | None:
        if attribute:
            return shorten(str(attribute), 255)

    def _set_organizer(self, attribute: vCalAddress | None) -> dict[str, str] | None:
        if attribute:
            result = {"email": str(attribute).removeprefix("mailto:")}

            if attribute.params:
                result.update({k.lower(): v for k, v in attribute.params.items()})

            return result

    def _set_attendee(self, attribute: list[vCalAddress] | None) -> list[dict[str, str]] | None:
        if attribute:
            result = []

            for at in attribute:
                at_dict = {"email": at.removeprefix("mailto:")}

                if at.params:
                    at_dict.update({a.lower(): v for a, v in at.params.items()})

                result.append(at_dict)

            return result

    def _set_location(self, attribute: vText | None) -> str | None:
        if attribute:
            return shorten(str(attribute), 255)

    def _set_recurrence_id(self, attribute: list[vDDDTypes] | vDDDTypes | None) -> datetime | None:
        if attribute:
            if type(attribute) is list:
                dt = attribute[0].dt
            else:
                dt = attribute.dt

            if type(dt) is date:
                dt = datetime(year=dt.year, month=dt.month, day=dt.day, tzinfo=ZoneInfo(self.timezone))
            return dt.astimezone(ZoneInfo(self.timezone))

    def _set_conf_id(self) -> str:
        return f'{self.uid}__{self.recurrence_id}'
