"""Provide a class for Aeon Timeline 3 'aeon' file representation.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/aeon3obsidian
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import codecs
import json
import os

from aeon3lib.aeon3obsidian_globals import output
from aeon3lib.aeon3_item import Aeon3Item
from aeon3lib.py_calendar import PyCalendar


class Aeon3File:

    def __init__(self, filePath):
        self.filePath = filePath
        self.data = None
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

        #--- Create lookup dictionaries (labels by UID).
        itemLabelLookup = self._get_item_label_lookup(jsonData)
        tagLookup = self._get_tag_lookup(jsonData)
        relationshipTypeLookup = self._get_relationship_type_lookup(jsonData)
        propertyTypeLookup = self._get_property_type_lookup(jsonData)
        propertyEnumLookup = self._get_property_enum_lookup(jsonData)
        itemTypeLookup = self._get_item_type_lookup(jsonData)

        #--- Build the items of the data model.
        calendar = PyCalendar()
        for itemUid in itemLabelLookup:
            uniqueLabel = itemLabelLookup[itemUid]
            output(f'Processing "{uniqueLabel}" ...')

            # Get properties.
            jsonItem = jsonData['core']['data']['itemsById'][itemUid]
            shortLabel = jsonItem.get('shortLabel', None)
            summary = jsonItem.get('summary', None)
            tags = []
            for tagUid in jsonItem['tags']:
                tags.append(tagLookup[tagUid])
            properties = []
            for propertyTypeUid in jsonItem['propertyValues']:
                propertyValues = jsonItem['propertyValues'][propertyTypeUid]
                customProperty = (
                    propertyTypeLookup[propertyTypeUid],
                    propertyEnumLookup.get(propertyValues, propertyValues)
                )
                properties.append(customProperty)

            # Get relationships.
            relationships = []
            jsonRelationshipDict = jsonData['collection']['relationshipIdsByItemId'][itemUid]
            for relUid in jsonRelationshipDict:
                if not jsonRelationshipDict[relUid]:
                    # target might be deleted
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
            self.data.items[itemUid] = Aeon3Item(
                uniqueLabel,
                shortLabel=shortLabel,
                summary=summary,
                properties=properties,
                tags=tags,
                dateStr=dateStr,
                timeStr=timeStr,
                durationStr=durationStr,
                relationships=relationships,
                )
            self.data.items[itemUid].write_to_console()

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
        self.data.itemIndex = itemIndex

        #--- Get the narrative tree.

        return 'Aeon 3 file successfully read.'

    def _get_item_label_lookup(self, jsonData):
        # Return a lookup dictionary with unique item labels by UID.
        itemLabelLookup = {}
        jsonItems = jsonData['core']['data']['itemsById']
        for itemUid in jsonItems:
            if not jsonData['collection']['allItemIds'][itemUid]:
                # item might be deleted
                continue

            jsonItem = jsonItems[itemUid]
            aeonLabel = jsonItem.get('label', None)
            if aeonLabel is not None:
                uniqueLabel = self._get_unique_label(aeonLabel.strip())
                itemLabelLookup[itemUid] = uniqueLabel
                output(f'Found item "{uniqueLabel}" ...')
        return itemLabelLookup

    def _get_item_type_lookup(self, jsonData):
        # Return a lookup dictionary with item type labels by UID.
        itemTypeLookup = {}
        itemTypes = jsonData['core']['definitions']['types']['byId']
        for itemTypeUid in itemTypes:
            itemType = itemTypes[itemTypeUid].get('label', '').strip()
            itemTypeLookup[itemTypeUid] = itemType
            output(f'Found item type "{itemType}".')
        return itemTypeLookup

    def _get_json_string(self):
        # Return a string containing the JSON part of the aeon file.
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

    def _get_property_enum_lookup(self, jsonData):
        # Return a lookup dictionary with allowed property enum labels by UID.
        propertyEnumLookup = {}
        propertyTypes = jsonData['core']['definitions']['properties']['byId']
        for propertyTypeUid in propertyTypes:
            propertyType = propertyTypes[propertyTypeUid]
            for enumUid in propertyType['allowed']:
                enumLabel = propertyType['allowed'][enumUid]['label']
                propertyEnumLookup[enumUid] = enumLabel
                output(f'Found property enum "{enumLabel}".')
        return propertyEnumLookup

    def _get_property_type_lookup(self, jsonData):
        # Return a lookup dictionary with property type labels by UID.
        propertyTypeLookup = {}
        propertyTypes = jsonData['core']['definitions']['properties']['byId']
        for propertyTypeUid in propertyTypes:
            propertyType = propertyTypes[propertyTypeUid]
            propertyTypeLabel = propertyType['label']
            propertyTypeLookup[propertyTypeUid] = propertyTypeLabel.strip()
            output(f'Found property type "{propertyTypeLabel}".')
        return propertyTypeLookup

    def _get_relationship_type_lookup(self, jsonData):
        # Return a lookup dictionary with relationship type labels by UID.
        relationshipTypeLookup = {}
        relationshipTypes = jsonData['core']['definitions']['references']['byId']
        for relationshipTypeUid in relationshipTypes:
            relationshipType = relationshipTypes[relationshipTypeUid]['label']
            relationshipTypeLookup[relationshipTypeUid] = relationshipType.strip()
            output(f'Found relationship type "{relationshipType}".')
        return relationshipTypeLookup

    def _get_tag_lookup(self, jsonData):
        # Return a lookup dictionary with tags by UID.
        tagLookup = {}
        tags = jsonData['core']['data']['tags']
        for tagUid in tags:
            tagName = tags[tagUid]
            tagLookup[tagUid] = tagName.strip()
            output(f'Found tag "{tagName}".')
        return tagLookup

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
