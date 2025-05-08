"""Provide a class with helper methods for date/time formatting.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/aeon3obsidian
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""


class Aeon3Calendar:

    HIDDEN_ERAS = ('AD')
    ISO_ERAS = ('AD')

    def __init__(self, calendarDefinitions):

        #--- Era enumerations.
        self.eraShortNames = []
        self.eraNames = []
        for era in calendarDefinitions['eras']:
            self.eraShortNames.append(era['shortName'])
            self.eraNames.append(era['name'])

        #--- Month enumerations.
        self.monthShortNames = []
        self.monthNames = []
        for month in calendarDefinitions['months']:
            self.monthShortNames.append(month['shortName'])
            self.monthNames.append(month['name'])

        #--- Weekday enumerations.
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

        #--- Get the weekday.
        weekday = startDate.get('weekday', None)
        if weekday is not None:
            try:
                weekday = self.weekdayNames[weekday]
            except:
                pass
            dateStr = f'{weekday}'

        #--- Get the day.
        day = startDate.get('day', None)
        if day is not None:
            dateStr = f'{dateStr} {day}'

        #--- Get the month.
        month = startDate.get('month', None)
        if month is not None:
            try:
                month = self.monthNames[month]
            except:
                pass
            dateStr = f'{dateStr} {month}'

        #--- Get the year.
        year = startDate.get('year', None)
        if year is not None:
            dateStr = f'{dateStr} {year}'

        #--- Get the era.
        era = startDate.get('era', None)
        if era is not None:
            try:
                era = self.eraNames[era]
            except:
                pass
            if era not in self.HIDDEN_ERAS:
                dateStr = f'{dateStr} {era}'
        return dateStr

    def get_day(self, itemDates):
        """Return a tuple: (day as an integer, day's short name, day's name)."""
        startDate = itemDates.get('startDate', None)
        if startDate is None:
            return

        day = startDate.get('day', None)
        if day is None:
            return

        try:
            return day, self.dayShortNames[day], self.dayNames[day]
        except:
            return

    def get_duration_str(self, itemDates):
        """Return a string with comma-separated elements of the duration."""
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
        """Return a tuple: (era as an integer, era's short name, era's name)."""
        startDate = itemDates.get('startDate', None)
        if startDate is None:
            return

        era = startDate.get('era', None)
        if era is None:
            return

        try:
            return era, self.eraShortNames[era], self.eraNames[era]
        except:
            return

    def get_hour(self, itemDates):
        """Return an integer hour or None."""
        startDate = itemDates.get('startDate', None)
        if startDate is not  None:
            return  startDate.get('hour', None)

    def get_iso_date(self, itemDates):
        """Return a date string formatted acc. to ISO 8601, if applicable. 
        
        Return None, if the date isn't within the range specified by ISO 8601, 
        or in case of error.
        """
        try:
            startDate = itemDates['startDate']
            era = startDate['era']
            eraName = self.eraNames[era]
            if eraName not in self.ISO_ERAS:
                return

            year = startDate['year']
            month = startDate['month']
            day = startDate['day']
        except:
            return

        return f'{year:04}-{month:02}-{day:02}'

    def get_iso_time(self, itemDates):
        """Return a time string formatted acc. to ISO 8601. 
        
        Return None in case of error.
        """
        try:
            startDate = itemDates['startDate']
            hour = startDate['hour']
            minute = startDate['minute']
            second = startDate['second']
        except:
            return

        return f'{hour:02}:{minute:02}:{second:02}'

    def get_minute(self, itemDates):
        """Return an integer minute or None."""
        startDate = itemDates.get('startDate', None)
        if startDate is not None:
            return startDate.get('minute', None)

    def get_month(self, itemDates):
        """Return a tuple: (month's order, month's short name, month's name)."""
        startDate = itemDates.get('startDate', None)
        if startDate is None:
            return

        month = startDate.get('month', None)
        if month is None:
            return

        try:
            return month, self.monthShortNames[month], self.monthNames[month]
        except:
            return

    def get_second(self, itemDates):
        """Return an integer second or None."""
        startDate = itemDates.get('startDate', None)
        if startDate is not None:
            return startDate.get('second', None)

    def get_timestamp(self, itemDates):
        """Return an integer timestamp or None."""
        startDate = itemDates.get('startDate', None)
        if startDate is not None:
            return startDate.get('timestamp', None)

    def get_time_str(self, itemDates):
        startDate = itemDates.get('startDate', None)
        if startDate is None:
            return ''

        timeStr = ''

        # Get hour.
        hour = startDate.get('hour', None)
        if hour is not None:
            timeStr = f'{hour:02}'

        # Get minute.
        minute = startDate.get('minute', None)
        if minute is not None:
            timeStr = f'{timeStr}:{minute:02}'

        # Get second
        second = startDate.get('second', 0)
        if second:
            timeStr = f'{timeStr}:{second:02}'
        return timeStr

    def get_weekday(self, itemDates):
        """Return a tuple: (weekday as an integer, weekday's short name, weekday's name)."""
        startDate = itemDates.get('startDate', None)
        if startDate is None:
            return

        weekday = startDate.get('weekday', None)
        if weekday is None:
            return

        try:
            return weekday, self.weekdayShortNames[weekday], self.weekdayNames[weekday]
        except:
            return

    def get_year(self, itemDates):
        """Return a tuple: (year as an integer, year's short name, year's name)."""
        startDate = itemDates.get('startDate', None)
        if startDate is None:
            return

        year = startDate.get('year', None)
        if year is None:
            return

        try:
            return year, self.yearShortNames[year], self.yearNames[year]
        except:
            return

