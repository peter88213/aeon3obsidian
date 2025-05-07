"""Provide a class with helper methods for date/time formatting.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/aeon3obsidian
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from datetime import date
from datetime import datetime
from datetime import timedelta


class PyCalendar:

    def __init__(self, calendarDefinitions):
        self.eraShortNames = []
        self.eraNames = []
        for era in calendarDefinitions['eras']:
            self.eraShortNames.append(era['shortName'])
            self.eraNames.append(era['name'])

    def get_date_str(self, itemDates):
        startDate = itemDates.get('startDate', None)
        if startDate is None:
            return ''

        timestamp = startDate.get('timestamp', 'null')
        if timestamp and timestamp != 'null':
            startDateTime = datetime.min + timedelta(seconds=timestamp)
            dateStr = date.isoformat(startDateTime)
        else:
            dateStr = ''
        return dateStr

    def get_duration_str(self, itemDates):
        durationList = []
        durationDict = itemDates.get('duration', None)
        if durationDict:
            durations = list(durationDict)
            for unit in durations:
                if durationDict[unit]:
                    durationList.append(f'{durationDict[unit]} {unit}')
        durationStr = ', '.join(durationList)
        return durationStr

    def get_era(self, itemDates):
        """Return a tuple: (era's order, era's short name, era's name)."""
        startDate = itemDates.get('startDate', None)
        if startDate is None:
            return

        eraStr = startDate.get('era', None)
        if eraStr is None:
            return

        try:
            eraInt = int(eraStr)
            return eraInt, self.eraShortNames[eraInt], self.eraNames[eraInt]
        except:
            return

    def get_timestamp(self, itemDates):
        """Return an integer timestamp or None."""
        startDate = itemDates.get('startDate', None)
        if startDate is None:
            return

        timestampStr = startDate.get('timestamp', None)
        if timestampStr is None:
            return

        try:
            timestamp = int(timestampStr)
        except:
            return
        else:
            return timestamp

    def get_time_str(self, itemDates):
        startDate = itemDates.get('startDate', None)
        if startDate is None:
            return ''

        timestamp = startDate.get('timestamp', 'null')
        if timestamp and timestamp != 'null':
            startDateTime = datetime.min + timedelta(seconds=timestamp)
            timeStr = startDateTime.strftime('%X')
            seconds = itemDates['startDate'].get('second', 0)
            if not seconds:
                h, m, _ = timeStr.split(':')
                timeStr = ':'.join([h, m])
        else:
            timeStr = ''
        return timeStr

