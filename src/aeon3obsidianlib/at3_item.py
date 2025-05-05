"""Provide a class for Aeon Timeline 3 items.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/aeon3obsidian
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""

from aeon3obsidianlib.aeon3obsidian_globals import output


class At3Item:

    def __init__(self, uid: str, calendar, label:str=None):
        self.uid: str = uid
        self.calendar = calendar

        self.label: str = label
        # single line text

        self.shortLabel: str = None
        # single line text

        self.summary: str = None
        # multiline text

        self.tags: list[str] = None

        self.type: str = None

        self.date: str = None
        # ISO date string

        self.time: str = None
        # ISO time string

        self.duration: str = None

        self.relationships: dict[str, list[str]] = None
        # key: role ID, value: list of entity IDs

        self.children = None

    def set_data(
            self,
            jsonItem,
            allTags,
            itemDate,
            relationships,
            ):

        self.shortLabel = jsonItem.get('shortLabel', None)
        output(f' - shortLabel: {self.shortLabel}')
        self.summary = jsonItem.get('summary', None)
        output(f' - summary   : {self.summary}')

        #--- Read tags.
        self.tags = []
        for uid in jsonItem['tags']:
            self.tags.append(self._sanitize_tag(allTags[uid]))
        output(f' - tags      : {self.tags}')

        #--- Read date/time/duration.
        dateStr = self.calendar.get_date_str(itemDate)
        if dateStr:
            self.date = dateStr
            output(f' - date      : {dateStr}')
        timeStr = self.calendar.get_time_str(itemDate)
        if timeStr:
            self.time = timeStr
            output(f' - time      : {timeStr}')
        durationStr = self.calendar.get_duration_str(itemDate)
        if durationStr:
            self.duration = durationStr
            output(f' - duration  : {durationStr}')

    def _sanitize_tag(self, label):
        return label.strip().replace(' ', '_')

