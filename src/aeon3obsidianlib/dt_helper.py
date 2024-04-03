"""Provide helper functions for date/time processing.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/aeon3yw
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""


def fix_iso_dt(dateTimeStr):
    """Return a date/time string with a four-number year.
    
    Positional arguments:
        dateTimeStr -- str: date/time as read in from Aeon3 csv export.
    
    This is required for comparing date/time strings, 
    and by the datetime.fromisoformat() method.

    Substitute missing time by "00:00:00".
    Substitute missing month by '01'.
    Substitute missing day by '01'.
    If the date is empty or out of yWriter's range, return None. 
    """
    if not dateTimeStr:
        return None

    if dateTimeStr.startswith('BC'):
        return None

    dt = dateTimeStr.split(' ')
    if len(dt) == 1:
        dt.append('00:00:00')
    date = dt[0].split('-')
    while len(date) < 3:
        date.append('01')
    if int(date[0]) < 100:
        return None

    if int(date[0]) > 9999:
        return None

    date[0] = date[0].zfill(4)
    dt[0] = ('-').join(date)
    dateTimeStr = (' ').join(dt)
    return dateTimeStr
