"""Provide a class for Aeon Timeline 3 'aeon' file representation.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/aeon3obsidian
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import json
import os
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
        print(f'Reading file "{os.path.normpath(self.filePath)}" ...')
        jsonPart = scan_file(self.filePath)
        jsonData = json.loads(jsonPart)

        if not 'core' in jsonData:
            raise ValueError('Error: JSON structure missing "core" key.')

        print(f'Found "core" version {jsonData["core"].get("coreFileVersion", "Unknown")}.')
        labelText = {}

        #--- Create a labels dictionary for types and relationships.
        for uid in jsonData['core']['definitions']['types']['byId']:
            item = jsonData['core']['definitions']['types']['byId'][uid].get('label', '').strip()
            if item:
                add_label(uid, item)
                print(f'Found item "{item}".')
        for uid in jsonData['core']['definitions']['references']['byId']:
            reference = jsonData['core']['definitions']['references']['byId'][uid].get('label', '').strip()
            if reference:
                self.labels[uid] = reference
                print(f'Found reference "{reference}".')

        #--- Create a tag lookup dictionary.
        for uid in jsonData['core']['data']['tags']:
            element = jsonData['core']['data']['tags'][uid].strip()
            self.tags[uid] = element.replace('&', '\\&')

        #--- Create a data model and extend the labels dictionary.
        for uid in jsonData['core']['data']['itemsById']:
            aeonItem = jsonData['core']['data']['itemsById'][uid]
            aeonLabel = aeonItem.get('label', None)
            if aeonLabel is not None:
                print(f'Processing "{aeonLabel}" ...')
                add_label(uid, aeonLabel.strip())
                self.items[uid] = self._get_item(
                    aeonItem,
                    jsonData['core']['data']['itemDatesById'][uid],
                    jsonData['collection']['relationshipIdsByItemId'][uid],
                    )

        #--- Create an item index.
        for uid in jsonData['core']['data']['itemOrderByType']:
            if uid in self.items:
                itemUidList = jsonData['core']['data']['itemOrderByType'][uid]
                self.itemIndex[uid] = itemUidList

        #--- Create a relationships dictionary.
        for uid in jsonData['core']['data']['relationshipsById']:
            if uid in self.items:
                refId = jsonData['core']['data']['relationshipsById'][uid]['reference']
                objId = jsonData['core']['data']['relationshipsById'][uid]['object']
                self.relationships[uid] = (refId, objId)

        #--- Get the narrative tree.
        narrative = jsonData['collection'].get('self.narrative', self.narrative)

        return 'Aeon 3 file successfully read.'

    def _get_date(self, itemDate):
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

    def _get_duration(self, itemDates):
        durationList = []
        durationDict = itemDates.get('duration', None)
        if durationDict:
            durations = list(durationDict)
            for unit in durations:
                if durationDict[unit]:
                    durationList.append(f'{durationDict[unit]} {unit}')
        durationStr = ', '.join(durationList)
        return durationStr

    def _get_item(self, aeonItem, itemDate, relationships):
        """Return a dictionary with the relevant item properties."""

        item = {}
        item['shortLabel'] = aeonItem['shortLabel']
        item['summary'] = aeonItem['summary']
        item['references'] = [r for r in relationships]
        print(item['references'])
        # item['children'] = aeonItem['children']

        # Read tags.
        tags = []
        for uid in aeonItem['tags']:
            tags.append(f"#{self.tags[uid].strip().replace(' ','_')}")
            item['tags'] = tags

        # Read date/time/duration.

        dateStr = self._get_date(itemDate)
        if dateStr:
            item['Date'] = dateStr
            print(dateStr)
        timeStr = self._get_time(itemDate)
        if timeStr:
            item['Time'] = timeStr
            print(timeStr)
        durationStr = self._get_duration(itemDate)
        if durationStr:
            item['Duration'] = durationStr
            print(durationStr)

        return item

    def _get_time(self, itemDate):
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

