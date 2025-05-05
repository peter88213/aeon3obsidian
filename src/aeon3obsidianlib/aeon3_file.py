"""Provide a class for Aeon Timeline 3 'aeon' file representation.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/aeon3obsidian
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import codecs
import json
import os

from aeon3obsidianlib.aeon3obsidian_globals import output
from aeon3obsidianlib.at3_item import At3Item
from aeon3obsidianlib.py_calendar import PyCalendar


class Aeon3File:

    def __init__(self, filePath):
        self.filePath = filePath
        self.dataModel = None
        self.labels = {}
        self.itemIndex = {}
        self.relationships = {}
        self.allTags = {}
        self.narrative = {}

    def read(self):
        """Read the Aeon 3 project file.
        
        Store the relevant data in the data model.
        Return a success message.
        """

        def get_unique_label(key, value):
            # Add an entry to the labels dictionary, handling multiple labels.
            if value in labelText:
                print(f'Multiple label: {value}')
                number = labelText[value] + 1
                labelText[value] = number
                value = f'{value}({number})'
            else:
                labelText[value] = 0
            self.labels[key] = value
            return value

        #--- Read the aeon file and get a JSON data structure.
        print(f'Reading file "{os.path.normpath(self.filePath)}" ...')
        jsonPart = self._get_json()
        jsonData = json.loads(jsonPart)

        print(f'Found "core" version {jsonData["core"].get("coreFileVersion", "Unknown")}.')
        labelText = {}

        #--- Create a labels dictionary for types and relationships.
        for uid in jsonData['core']['definitions']['types']['byId']:
            item = jsonData['core']['definitions']['types']['byId'][uid].get('label', '').strip()
            if item:
                get_unique_label(uid, item)
                output(f'Found item "{item}".')
        for uid in jsonData['core']['definitions']['references']['byId']:
            reference = jsonData['core']['definitions']['references']['byId'][uid].get('label', '').strip()
            if reference:
                self.labels[uid] = reference
                output(f'Found reference "{reference}".')

        #--- Create a tag lookup dictionary.
        for uid in jsonData['core']['data']['tags']:
            element = jsonData['core']['data']['tags'][uid].strip()
            self.allTags[uid] = element.replace('&', '\\&')

        #--- Create a data model and extend the labels dictionary.
        calendar = PyCalendar()
        for uid in jsonData['core']['data']['itemsById']:
            jsonItem = jsonData['core']['data']['itemsById'][uid]
            aeonLabel = jsonItem.get('label', None)
            if aeonLabel is not None:
                uniqueLabel = get_unique_label(uid, aeonLabel.strip())
                output(f'Processing "{uniqueLabel}" ...')
                self.dataModel.items[uid] = At3Item(
                    uid,
                    calendar,
                    uniqueLabel,
                    )
                self.dataModel.items[uid].set_data(
                    jsonItem,
                    self.allTags,
                    jsonData['core']['data']['itemDatesById'][uid],
                    jsonData['collection']['relationshipIdsByItemId'][uid],
                    )

        #--- Create an item index.
        for uid in jsonData['core']['data']['itemOrderByType']:
            if uid in self.dataModel.items:
                itemUidList = jsonData['core']['data']['itemOrderByType'][uid]
                self.itemIndex[uid] = itemUidList

        #--- Create a relationships dictionary.
        for uid in jsonData['core']['data']['relationshipsById']:
            if uid in self.dataModel.items:
                refId = jsonData['core']['data']['relationshipsById'][uid]['reference']
                objId = jsonData['core']['data']['relationshipsById'][uid]['object']
                self.relationships[uid] = (refId, objId)

        #--- Get the narrative tree.
        narrative = jsonData['collection'].get('self.narrative', self.narrative)

        return 'Aeon 3 file successfully read.'

    def _get_json(self):
        """Read and scan the project file.
        
        Return a string containing the JSON part.
        """
        with open(self.filePath, 'rb') as f:
            binInput = f.read()

        # JSON part: all characters between the first and last curly bracket.
        chrData = []
        opening = ord('{')
        closing = ord('}')
        level = 0
        for c in binInput:
            if c == opening:
                level += 1
            if level > 0:
                chrData.append(c)
                if c == closing:
                    level -= 1
                    if level == 0:
                        break
        if level != 0:
            raise ValueError('Error: Corrupted data.')

        jsonStr = codecs.decode(bytes(chrData), encoding='utf-8')
        if not jsonStr:
            raise ValueError('Error: No JSON part found.')

        return jsonStr

