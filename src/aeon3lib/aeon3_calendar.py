"""Provide a class with helper methods for date/time formatting.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/aeon3obsidian
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""


class Aeon3Calendar:

    ISO_ERAS = ('AD')

    def __init__(self, calendarDefinitions):

        self.hoursInDay = calendarDefinitions['hoursInDay']
        self.minutesInHour = 60
        self.secondsInMinute = 60
        self.leapCycles = calendarDefinitions['leapCycles']

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

    def get_day(self, itemDates):
        """Return an integer day or None."""
        startDate = itemDates.get('startDate', None)
        if startDate is not None:
            return startDate.get('day', None)

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
        timestamp = self.get_timestamp(itemDates)
        if timestamp is None:
            return

        minutesTotal = timestamp // self.secondsInMinute
        hoursTotal = minutesTotal // self.minutesInHour
        daysTotal = hoursTotal // self.hoursInDay
        return hoursTotal % daysTotal

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
            hour = self.get_hour(itemDates)
            minute = self.get_minute(itemDates)
            second = self.get_second(itemDates)
        except:
            return

        return f'{hour:02}:{minute:02}:{second:02}'

    def get_minute(self, itemDates):
        """Return an integer minute or None."""
        timestamp = self.get_timestamp(itemDates)
        if timestamp is None:
            return

        minutesTotal = timestamp // self.secondsInMinute
        hoursTotal = minutesTotal // self.minutesInHour
        return minutesTotal % hoursTotal

    def get_month(self, itemDates):
        """Return a tuple: (month's order, month's short name, month's name)."""
        startDate = itemDates.get('startDate', None)
        if startDate is None:
            return

        month = startDate.get('month', None)
        if month is None:
            return

        try:
            return month, self.monthShortNames[month - 1], self.monthNames[month - 1]
        except:
            return

    def get_second(self, itemDates):
        """Return an integer second or None."""
        timestamp = self.get_timestamp(itemDates)
        if timestamp is None:
            return

        return timestamp % self.secondsInMinute

    def get_timestamp(self, itemDates):
        """Return an integer timestamp or None."""
        startDate = itemDates.get('startDate', None)
        if startDate is not None:
            return startDate.get('timestamp', None)

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
        """Return an integer year or None."""
        startDate = itemDates.get('startDate', None)
        if startDate is not None:
            return startDate.get('year', None)

