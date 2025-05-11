"""Unit tests for TDD of the Aron3Calendar timestamp calculations

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/aeon3obsidian
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import unittest

from aeon3lib.aeon3_calendar import Aeon3Calendar
from aeon3lib.aeon3_item import Aeon3Item


class TestTimestamp(unittest.TestCase):

    def setUp(self):
        jsonCalendar = {
            "calendarType": 2,
            "dateFormat": "Long",
            "dateFormatIncludesDayName": False,
            "dateOrder": "DayMonthYear",
            "defaultToModernCentury": True,
            "eras": [
                {
                    "duration": 2147483647,
                    "hasLeapYears": True,
                    "isBackwards": True,
                    "leapOffset": 1,
                    "name": "BC",
                    "shortName": "BC"
                },
                {
                    "duration": 2147483647,
                    "hasLeapYears": True,
                    "isBackwards": False,
                    "leapOffset": 0,
                    "name": "AD",
                    "shortName": "AD"
                }
            ],
            "hoursInDay": 24,
            "ignoreEras": False,
            "leapCycles": [
                4,
                100,
                400
            ],
            "maxPrecision": 7,
            "months": [
                {
                    "leapDuration": 31,
                    "name": "January",
                    "normalDuration": 31,
                    "shortName": "Jan"
                },
                {
                    "leapDuration": 29,
                    "name": "February",
                    "normalDuration": 28,
                    "shortName": "Feb"
                },
                {
                    "leapDuration": 31,
                    "name": "March",
                    "normalDuration": 31,
                    "shortName": "Mar"
                },
                {
                    "leapDuration": 30,
                    "name": "April",
                    "normalDuration": 30,
                    "shortName": "Apr"
                },
                {
                    "leapDuration": 31,
                    "name": "May",
                    "normalDuration": 31,
                    "shortName": "May"
                },
                {
                    "leapDuration": 30,
                    "name": "June",
                    "normalDuration": 30,
                    "shortName": "Jun"
                },
                {
                    "leapDuration": 31,
                    "name": "July",
                    "normalDuration": 31,
                    "shortName": "Jul"
                },
                {
                    "leapDuration": 31,
                    "name": "August",
                    "normalDuration": 31,
                    "shortName": "Aug"
                },
                {
                    "leapDuration": 30,
                    "name": "September",
                    "normalDuration": 30,
                    "shortName": "Sep"
                },
                {
                    "leapDuration": 31,
                    "name": "October",
                    "normalDuration": 31,
                    "shortName": "Oct"
                },
                {
                    "leapDuration": 30,
                    "name": "November",
                    "normalDuration": 30,
                    "shortName": "Nov"
                },
                {
                    "leapDuration": 31,
                    "name": "December",
                    "normalDuration": 31,
                    "shortName": "Dec"
                }
            ],
            "overrideNowTimestamp": 60972739200,
            "thousandSeparatorFormat": "Comma",
            "timeFormat": "Twelve",
            "weekdayIndexAtZero": 1,
            "weekdays": [
                {
                    "name": "Sunday",
                    "shortName": "Sun"
                },
                {
                    "name": "Monday",
                    "shortName": "Mon"
                },
                {
                    "name": "Tuesday",
                    "shortName": "Tue"
                },
                {
                    "name": "Wednesday",
                    "shortName": "Wed"
                },
                {
                    "name": "Thursday",
                    "shortName": "Thu"
                },
                {
                    "name": "Friday",
                    "shortName": "Fri"
                },
                {
                    "name": "Saturday",
                    "shortName": "Sat"
                }
            ],
            "zeroDateTimestamp": 60971011200
        }
        self.calendar = Aeon3Calendar(jsonCalendar)
        self.jsonData = {
            "core": {
                "data": {
                    "itemDatesById": {
                        "D857497B-3FEF-4DE9-8A82-FD7E81490118": {
                            "duration": {
                                "days": 0,
                                "hours": 0,
                                "minutes": 14,
                                "months": 0,
                                "seconds": 0,
                                "weeks": 0,
                                "years": 0
                            },
                            "durationToEarliestEnd": None,
                            "earliestEndDate": None,
                            "endDate": {
                                "day": 6,
                                "era": 1,
                                "hour": 22,
                                "minute": 55,
                                "month": 2,
                                "precision": 7,
                                "second": 0,
                                "timestamp": 60971180100,
                                "weekday": 1,
                                "year": 1933
                            },
                            "hasOngoingDescendants": False,
                            "isDateLocked": False,
                            "latestFixedChildDate": None,
                            "latestStartDate": None,
                            "ongoing": False,
                            "preferredDuration": {
                                "days": 0,
                                "hours": 0,
                                "minutes": 14,
                                "months": 0,
                                "seconds": 0,
                                "weeks": 0,
                                "years": 0
                            },
                            "preferredEndDate": {
                                "day": 6,
                                "era": 1,
                                "hour": 22,
                                "minute": 55,
                                "month": 2,
                                "precision": 7,
                                "second": 0,
                                "timestamp": 60971180100,
                                "weekday": 1,
                                "year": 1933
                            },
                            "preferredPrecision": 8,
                            "preferredStartDate": {
                                "day": 6,
                                "era": 1,
                                "hour": 22,
                                "minute": 41,
                                "month": 2,
                                "precision": 7,
                                "second": 0,
                                "timestamp": 60971179260,
                                "weekday": 1,
                                "year": 1933
                            },
                            "startDate": {
                                "day": 6,
                                "era": 1,
                                "hour": 22,
                                "minute": 41,
                                "month": 2,
                                "precision": 7,
                                "second": 0,
                                "timestamp": 60971179260,
                                "weekday": 1,
                                "year": 1933
                            }
                        }
                    }
                }
            }
        }
        # Get date/time/duration.
        self.itemUid = 'D857497B-3FEF-4DE9-8A82-FD7E81490118'
        self.itemDates = self.jsonData['core']['data']['itemDatesById'][self.itemUid]
        era = self.calendar.get_era(self.itemDates)
        weekday = self.calendar.get_weekday(self.itemDates)
        day = self.calendar.get_day(self.itemDates)
        hour = self.calendar.get_hour(self.itemDates)
        minute = self.calendar.get_minute(self.itemDates)
        second = self.calendar.get_second(self.itemDates)
        timestamp = self.calendar.get_timestamp(self.itemDates)
        isoDate = self.calendar.get_iso_date(self.itemDates)
        isoTime = self.calendar.get_iso_time(self.itemDates)
        self.testItem = Aeon3Item(
            "Greta Ohlsson asks Mrs Hubbard for some aspirin",
            "defaultEvent",
            timestamp=timestamp,
            isoDate=isoDate,
            isoTime=isoTime,
            era=era,
            weekday=weekday,
            month=(2, 'Feb', 'February'),
            year=1933,
            day=day,
            hour=hour,
            minute=minute,
            second=second,
            )

    def test_get_date(self):
        self.assertEqual(self.calendar.get_year(self.itemDates), 1933)
        self.assertEqual(self.calendar.get_month(self.itemDates), (2, 'Feb', 'February'))
