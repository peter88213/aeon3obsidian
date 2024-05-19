"""Provide a class for Aeon Timeline 3 'aeon' file representation.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/aeon3obsidian
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import json
from aeon3obsidianlib.aeon3_fop import scan_file
from datetime import datetime
from datetime import timedelta
from datetime import date


class Aeon3File:

    def __init__(self, filePath):
        """Set the Aeon 3 project file path."""
        self.filePath = filePath
        self.items = {}
        self.labels = {}
        self.itemIndex = {}
        self.relationships = {}
        self.tags = {}
        self.narrative = {}

    def read(self):
        """Read the Aeon 3 project file.
        
        Store the relevant data in the items dictionary.
        Populate the labels dictionary.
        Populate the itemIndex dictionary.
        
        Return a success message.
        """

        def add_label(key, value):
            """Add an entry to the labels dictionary, handling multiple labels."""
            if value in labelText:
                print(f'Multiple label: {value}')
                number = labelText[value] + 1
                labelText[value] = number
                value = f'{value}({number})'
            else:
                labelText[value] = 0
            self.labels[key] = value

        #--- Read the aeon file and get a JSON data structure.
        jsonPart = scan_file(self.filePath)
        jsonData = json.loads(jsonPart)
        labelText = {}

        #--- Create a labels dictionary for types and relationships.
        for uid in jsonData['definitions']['types']['byId']:
            item = jsonData['definitions']['types']['byId'][uid].get('label', '').strip()
            if item:
                add_label(uid, item)
        for uid in jsonData['definitions']['references']['byId']:
            reference = jsonData['definitions']['references']['byId'][uid].get('label', '').strip()
            if reference:
                self.labels[uid] = reference

        #--- Create a tag lookup dictionary.
        for uid in jsonData['data']['tags']:
            element = jsonData['data']['tags'][uid].strip()
            self.tags[uid] = element

        #--- Create a data model and extend the labels dictionary.
        for uid in jsonData['data']['items']['byId']:
            aeonItem = jsonData['data']['items']['byId'][uid]
            aeonLabel = aeonItem.get('label', None)
            if aeonLabel is not None:
                add_label(uid, aeonLabel.strip())
                self.items[uid] = self._get_item(aeonItem)

        #--- Create an item index.
        for uid in jsonData['data']['items']['allIdsForType']:
            if uid in self.items:
                itemUidList = jsonData['data']['items']['allIdsForType'][uid]
                self.itemIndex[uid] = itemUidList

        #--- Create a relationships dictionary.
        for uid in jsonData['data']['relationships']['byId']:
            if uid in self.items:
                refId = jsonData['data']['relationships']['byId'][uid]['reference']
                objId = jsonData['data']['relationships']['byId'][uid]['object']
                self.relationships[uid] = (refId, objId)

        #--- Get the narrative tree.
        self.narrative = jsonData['data'].get('narrative', self.narrative)

        return 'Aeon 3 file successfully read.'

    def _get_date(self, aeonItem):
        timestamp = aeonItem['startDate'].get('timestamp', 'null')
        if timestamp and timestamp != 'null':
            startDateTime = datetime.min + timedelta(seconds=timestamp)
            dateStr = date.isoformat(startDateTime)
        else:
            dateStr = ''
        return dateStr

    def _get_duration(self, aeonItem):
        durationList = []
        durationDict = aeonItem.get('duration', None)
        if durationDict:
            durations = list(durationDict)
            for unit in durations:
                if durationDict[unit]:
                    durationList.append(f'{durationDict[unit]} {unit}')
        durationStr = ', '.join(durationList)
        return durationStr

    def _get_item(self, aeonItem):
        """Return a dictionary with the relevant item properties."""
        item = {}
        item['shortLabel'] = aeonItem['shortLabel']
        item['summary'] = aeonItem['summary']
        item['references'] = aeonItem['references']
        item['children'] = aeonItem['children']

        # Read tags.
        tags = []
        for uid in aeonItem['tags']:
            tags.append(f"#{self.tags[uid].strip().replace(' ','_')}")
            item['tags'] = tags

        # Read date/time/duration.
        dateStr = self._get_date(aeonItem)
        if dateStr:
            item['Date'] = dateStr
        timeStr = self._get_time(aeonItem)
        if timeStr:
            item['Time'] = timeStr
        durationStr = self._get_duration(aeonItem)
        if durationStr:
            item['Duration'] = durationStr

        return item

    def _get_time(self, aeonItem):
        timestamp = aeonItem['startDate'].get('timestamp', 'null')
        if timestamp and timestamp != 'null':
            startDateTime = datetime.min + timedelta(seconds=timestamp)
            timeStr = startDateTime.strftime('%X')
            seconds = aeonItem['startDate'].get('second', 0)
            if not seconds:
                h, m, _ = timeStr.split(':')
                timeStr = ':'.join([h, m])
        else:
            timeStr = ''
        return timeStr

