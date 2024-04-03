"""Provide a class for Aeon Timeline 3 'aeon' file representation.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/aeon3yw
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import json
from aeon3obsidianlib.aeon3_fop import scan_file


class Aeon3File:

    def __init__(self, filePath):
        """Set the Aeon 3 project file path."""
        self.filePath = filePath
        self.dataModel = {}
        self.labelLookup = {}

    def _read_item(self, aeonItem):
        """Return a dictionary with the relevant item properties."""
        item = {}
        item['shortLabel'] = aeonItem['shortLabel']
        item['summary'] = aeonItem['summary']
        return item

    def read(self):
        """Read the Aeon 3 project file.
        
        Store the relevant data in the dataModel dictionary.
        Populate the labelLookup dictionary.
        
        Return a success message.
        """

        #--- Read the aeon file and get a JSON data structure.
        jsonPart = scan_file(self.filePath)
        jsonData = json.loads(jsonPart)

        #--- Create a labelLookup dictionary for types and relationships.
        for uid in jsonData['definitions']['types']['byId']:
            element = jsonData['definitions']['types']['byId'][uid].get('label', None)
            if element:
                self.labelLookup[uid] = element
        for uid in jsonData['definitions']['references']['byId']:
            element = jsonData['definitions']['references']['byId'][uid].get('label', None)
            if element:
                self.labelLookup[uid] = element
        for uid in jsonData['data']['tags']:
            element = jsonData['data']['tags'][uid]
            self.labelLookup[uid] = element

        #--- Create a data model and extend the labelLookup dictionary.
        for uid in jsonData['data']['items']['byId']:
            aeonItem = jsonData['data']['items']['byId'][uid]
            self.labelLookup[uid] = aeonItem['label']
            self.dataModel[uid] = self._read_item(aeonItem)

        return 'Aeon 3 file successfully read.'

