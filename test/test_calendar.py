"""Unit tests for of the Aeon3Calendar time extraction methods.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/aeon3obsidian
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import unittest

from aeon3lib.aeon3_calendar import Aeon3Calendar


class TestCalendar(unittest.TestCase):

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
        itemUid = 'D857497B-3FEF-4DE9-8A82-FD7E81490118'
        self.itemDates = self.jsonData['core']['data']['itemDatesById'][itemUid]

    def test_get_timestamp(self):
        self.assertEqual(self.calendar.get_timestamp(self.itemDates), 60971179260)

    def test_get_era(self):
        self.assertEqual(self.calendar.get_era(self.itemDates), (1, 'AD', 'AD'))

    def test_get_year(self):
        self.assertEqual(self.calendar.get_year(self.itemDates), 1933)

    def test_get_month(self):
        self.assertEqual(self.calendar.get_month(self.itemDates), (2, 'Feb', 'February'))

    def test_get_day(self):
        self.assertEqual(self.calendar.get_day(self.itemDates), 6)

    def test_get_hour(self):
        self.assertEqual(self.calendar.get_hour(self.itemDates), 22)

    def test_get_minute(self):
        self.assertEqual(self.calendar.get_minute(self.itemDates), 41)

    def test_get_second(self):
        self.assertEqual(self.calendar.get_second(self.itemDates), 0)

    def test_get_weekday(self):
        self.assertEqual(self.calendar.get_weekday(self.itemDates), (1, 'Mon', 'Monday'))

    def test_get_iso_date(self):
        self.assertEqual(self.calendar.get_iso_date(self.itemDates), '1933-02-06')

    def test_get_iso_time(self):
        self.assertEqual(self.calendar.get_iso_time(self.itemDates), '22:41:00')
