"""Provide a class with helper methods for date/time formatting.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/aeon3obsidian
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""


class Aeon3Calendar:

    HIDDEN_ERAS = ('AD')

    def __init__(self, calendarDefinitions):
        self.eraShortNames = []
        self.eraNames = []
        for era in calendarDefinitions['eras']:
            self.eraShortNames.append(era['shortName'])
            self.eraNames.append(era['name'])
        self.monthShortNames = []
        self.monthNames = []
        for month in calendarDefinitions['months']:
            self.monthShortNames.append(month['shortName'])
            self.monthNames.append(month['name'])
        self.weekdayShortNames = []
        self.weekdayNames = []
        for weekday in calendarDefinitions['weekdays']:
            self.weekdayShortNames.append(weekday['shortName'])
            self.weekdayNames.append(weekday['name'])

    def get_date_str(self, itemDates):
        startDate = itemDates.get('startDate', None)
        if startDate is None:
            return ''

        dateStr = ''

        # Get the weekday.
        weekday = startDate.get('weekday', None)
        if weekday is not None:
            try:
                weekday = self.weekdayNames[weekday]
            except:
                pass
            dateStr = f'{weekday}'

        # Get the day.
        day = startDate.get('day', None)
        if day is not None:
            dateStr = f'{dateStr} {day}'

        # Get the month.
        month = startDate.get('month', None)
        if month is not None:
            try:
                month = self.monthNames[month]
            except:
                pass
            dateStr = f'{dateStr} {month}'

        # Get the year.
        year = startDate.get('year', None)
        if year is not None:
            dateStr = f'{dateStr} {year}'

        # Get the era.
        era = startDate.get('era', None)
        if era is not None:
            try:
                era = self.eraNames[era]
            except:
                pass
            if era not in self.HIDDEN_ERAS:
                dateStr = f'{dateStr} {era}'
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

        timeStr = ''

        # Get hour.
        hour = startDate.get('hour', None)
        if hour is not None:
            timeStr = f'{hour}'

        # Get minute.
        minute = startDate.get('minute', None)
        if minute is not None:
            timeStr = f'{timeStr}:{minute}'

        # Get second
        second = startDate.get('second', 0)
        if second:
            timeStr = f'{timeStr}:{second}'
        return timeStr

