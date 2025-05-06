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
        self.timeline = None
        self._labelCounts = {}

    def read(self):
        """Read the Aeon 3 project file.
        
        Store the relevant data in the data model.
        Return a success message.
        """

        #--- Read the aeon file and get a JSON data structure.
        print(f'Reading file "{os.path.normpath(self.filePath)}" ...')
        jsonStr = self._get_json_string()
        jsonData = json.loads(jsonStr)

        print(f'Found file version: "{jsonData["core"].get("coreFileVersion", "Unknown")}".')

        #--- Create an item type lookup dictionary.
        itemTypeLookup = {}
        for itemTypeUid in jsonData['core']['definitions']['types']['byId']:
            itemType = jsonData['core']['definitions']['types']['byId'][itemTypeUid].get('label', '').strip()
            itemTypeLookup[itemTypeUid] = itemType
            output(f'Found item type "{itemType}".')

        #--- Create an item label lookup dictionary with unique labels.
        itemLabelLookup = {}
        for itemUid in jsonData['core']['data']['itemsById']:
            if not jsonData['collection']['allItemIds'][itemUid]:
                # this item is deleted
                continue

            jsonItem = jsonData['core']['data']['itemsById'][itemUid]
            aeonLabel = jsonItem.get('label', None)
            if aeonLabel is not None:
                uniqueLabel = self._get_unique_label(aeonLabel.strip())
                itemLabelLookup[itemUid] = uniqueLabel
                output(f'Found item "{uniqueLabel}" ...')

        #--- Create a relationship type lookup dictionary.
        relationshipTypeLookup = {}
        for relationshipTypeUid in jsonData['core']['definitions']['references']['byId']:
            reference = jsonData['core']['definitions']['references']['byId'][relationshipTypeUid].get('label', '').strip()
            relationshipTypeLookup[relationshipTypeUid] = reference
            output(f'Found relationship type "{reference}".')

        #--- Create a tag lookup dictionary.
        tagLookup = {}
        for tagUid in jsonData['core']['data']['tags']:
            tagName = jsonData['core']['data']['tags'][tagUid].strip()
            tagName = tagName.replace('&', '\\&')
            tagLookup[tagUid] = tagName
            output(f'Found tag "{tagName}".')

        #--- Instantiate the item objects of the data model.
        calendar = PyCalendar()
        for itemUid in itemLabelLookup:
            uniqueLabel = itemLabelLookup[itemUid]
            output(f'Processing "{uniqueLabel}" ...')

            # Get item properties.
            jsonItem = jsonData['core']['data']['itemsById'][itemUid]
            shortLabel = jsonItem.get('shortLabel', None)
            summary = jsonItem.get('summary', None)
            tags = []
            for tagUid in jsonItem['tags']:
                tags.append(self._sanitize_tag(tagLookup[tagUid]))

            # Get relationships.
            relationships = []
            jsonRelationshipDict = jsonData['collection']['relationshipIdsByItemId'][itemUid]
            for relUid in jsonRelationshipDict:
                if not jsonRelationshipDict[relUid]:
                    # target is deleted
                    continue

                relationship = jsonData['core']['data']['relationshipsById'][relUid]
                itemRelationship = (
                    itemLabelLookup[relationship['object']],
                    relationshipTypeLookup[relationship['reference']]
                )
                relationships.append(itemRelationship)

            # Get date/time/duration.
            itemDate = jsonData['core']['data']['itemDatesById'][itemUid]
            dateStr = calendar.get_date_str(itemDate)
            timeStr = calendar.get_time_str(itemDate)
            durationStr = calendar.get_duration_str(itemDate)

            # Instantiate the item object.
            self.timeline.items[itemUid] = At3Item(
                uniqueLabel,
                shortLabel=shortLabel,
                summary=summary,
                tags=tags,
                dateStr=dateStr,
                timeStr=timeStr,
                durationStr=durationStr,
                relationships=relationships,
                )

        #--- Create an item index.
        output('Generating item index ...')
        itemIndex = {}
        jsonItemIndex = jsonData['collection']['itemIdsByType']
        for typeUid in jsonItemIndex:
            itemType = itemTypeLookup[typeUid]
            itemIndex[itemType] = []
            output(f'* Type: {itemType}')
            for itemUid in jsonItemIndex[typeUid]:
                itemLabel = itemLabelLookup[itemUid]
                itemIndex[itemType].append(itemLabel)
                output(f'  * Item: {itemLabel}')
        self.timeline.itemIndex = itemIndex

        #--- Get the narrative tree.

        return 'Aeon 3 file successfully read.'

    def _sanitize_tag(self, label):
        return label.strip().replace(' ', '_')

    def _get_json_string(self):
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

    def _get_unique_label(self, aeonLabel):
        # Return a unique item label.
        if aeonLabel in self._labelCounts:
            print(f'Multiple aeonLabel: {aeonLabel}')
            counts = self._labelCounts[aeonLabel] + 1
            self._labelCounts[aeonLabel] = counts
            aeonLabel = f'{aeonLabel}({counts})'
        else:
            self._labelCounts[aeonLabel] = 0
        return aeonLabel
