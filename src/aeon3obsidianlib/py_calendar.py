"""Provide a class with helper methods for date/time formatting.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/aeon3obsidian
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from datetime import date
from datetime import datetime
from datetime import timedelta


class PyCalendar:

    def get_date_str(self, itemDate):
        startDate = itemDate.get('startDate', None)
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

    def get_time_str(self, itemDate):
        startDate = itemDate.get('startDate', None)
        if startDate is None:
            return ''

        timestamp = startDate.get('timestamp', 'null')
        if timestamp and timestamp != 'null':
            startDateTime = datetime.min + timedelta(seconds=timestamp)
            timeStr = startDateTime.strftime('%X')
            seconds = itemDate['startDate'].get('second', 0)
            if not seconds:
                h, m, _ = timeStr.split(':')
                timeStr = ':'.join([h, m])
        else:
            timeStr = ''
        return timeStr

