"""Provide a class for Aeon Timeline 3 'aeon' file representation.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/aeon3yw
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import json
from aeon3obsidianlib.aeon3_fop import scan_file
from datetime import datetime
from datetime import timedelta


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

        #--- Read the aeon file and get a JSON data structure.
        jsonPart = scan_file(self.filePath)
        jsonData = json.loads(jsonPart)

        #--- Create a labels dictionary for types and relationships.
        for uid in jsonData['definitions']['types']['byId']:
            element = jsonData['definitions']['types']['byId'][uid].get('label', '').strip()
            if element:
                self.labels[uid] = element
        for uid in jsonData['definitions']['references']['byId']:
            element = jsonData['definitions']['references']['byId'][uid].get('label', '').strip()
            if element:
                self.labels[uid] = element

        #--- create a tag lookup dictionary.
        for uid in jsonData['data']['tags']:
            element = jsonData['data']['tags'][uid].strip()
            self.tags[uid] = element

        #--- Create a data model and extend the labels dictionary.
        for uid in jsonData['data']['items']['byId']:
            aeonItem = jsonData['data']['items']['byId'][uid]
            self.labels[uid] = aeonItem['label'].strip()
            self.items[uid] = self._read_item(aeonItem)

        #--- Create an index.
        for uid in jsonData['data']['items']['allIdsForType']:
            itemUidList = jsonData['data']['items']['allIdsForType'][uid]
            self.itemIndex[uid] = itemUidList

        #--- Create a relationships dictionary.
        for uid in jsonData['data']['relationships']['byId']:
            refId = jsonData['data']['relationships']['byId'][uid]['reference']
            objId = jsonData['data']['relationships']['byId'][uid]['object']
            self.relationships[uid] = (refId, objId)

        #--- Get the narrative tree.
        self.narrative = jsonData['data'].get('narrative', self.narrative)

        return 'Aeon 3 file successfully read.'

    def _read_item(self, aeonItem):
        """Return a dictionary with the relevant item properties."""
        item = {}
        item['shortLabel'] = aeonItem['shortLabel']
        item['summary'] = aeonItem['summary']
        item['references'] = aeonItem['references']
        item['children'] = aeonItem['children']
        tags = []
        for uid in aeonItem['tags']:
            tags.append(f"#{self.tags[uid].strip().replace(' ','_')}")
            item['tags'] = tags
        timestamp = aeonItem['startDate'].get('timestamp', 'null')
        if timestamp and timestamp != 'null':
            startDateTime = datetime.min + timedelta(seconds=timestamp)
            item['Date'] = startDateTime.strftime('%x')
            timeStr = startDateTime.strftime('%X')
            seconds = aeonItem['startDate'].get('second', 0)
            if not seconds:
                h, m, s = timeStr.split(':')
                timeStr = ':'.join([h, m])
            item['Time'] = timeStr

        return item

