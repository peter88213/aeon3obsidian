"""Provide a class for Aeon Timeline 3 items.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/aeon3obsidian
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""


class Aeon3Item:

    def __init__(
            self,
            label,
            shortLabel=None,
            summary=None,
            properties=[],
            tags=None,
            timestamp=None,
            isoDate=None,
            isoTime=None,
            era=None,
            weekday=None,
            month=None,
            year=None,
            day=None,
            hour=None,
            minute=None,
            second=None,
            durationStr=None,
            relationships=[],
            children=[],
            ):

        self.label = label
        self.shortLabel = shortLabel
        self.summary = summary
        self.properties = properties
        self.tags = tags
        self.timestamp = timestamp
        self.isoDate = isoDate
        self.isoTime = isoTime
        if era:
            self.era, self.eraShortName, self.eraName = era
        else:
            self.era = self.eraShortName = self.eraName = None
        if weekday:
            self.weekday, self.weekdayShortName, self.weekdayName = weekday
        else:
            self.weekday = self.weekdayShortName = self.weekdayName = None
        if month:
            self.month, self.monthShortName, self.monthName = month
        else:
            self.month = self.monthShortName = self.monthName = None
        self.year = year
        self.day = day
        self.hour = hour
        self.minute = minute
        self.second = second
        self.duration = durationStr
        self.relationships = relationships
        self.children = children

