"""Provide a class for Aeon Timeline 3 'aeon' file representation.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/aeon3obsidian
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import codecs
import json
import os

from aeon3lib.aeon3_calendar import Aeon3Calendar
from aeon3lib.aeon3_item import Aeon3Item
from aeon3lib.aeon3_type import Aeon3Type


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

        print(f'Found file version: "{jsonData.get("fileVersion", "Unknown")}".')

        #--- Create lookup dictionaries (labels by UID).
        itemLabelLookup, uniqueItemLabelLookup = self._get_item_label_lookup(jsonData)
        tagLookup = self._get_tag_lookup(jsonData)
        relationshipTypeLookup = self._get_relationship_type_lookup(jsonData)
        propertyTypeLookup = self._get_property_type_lookup(jsonData)
        propertyEnumLookup = self._get_property_enum_lookup(jsonData)

        #--- Set the item types of the data model.
        self.data.itemTypes = self._get_item_types(jsonData)

        #--- Build the items of the data model.
        calendar = Aeon3Calendar(jsonData['core']['definitions']['calendar'])

        for itemUid in uniqueItemLabelLookup:
            label = itemLabelLookup[itemUid]
            uniqueLabel = uniqueItemLabelLookup[itemUid]

            # Get properties.
            jsonItem = jsonData['core']['data']['itemsById'][itemUid]
            displayId = jsonItem.get('displayId', None)
            typeUid = jsonItem.get('type', None)
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
                    uniqueItemLabelLookup[relationship['object']],
                    relationshipTypeLookup[relationship['reference']]
                )
                relationships.append(itemRelationship)

            # Get children.
            children = []
            jsonChildrenDict = jsonData['core']['data']['superAndChildOrderById'][itemUid]
            for childUid in jsonChildrenDict['childOrder']:
                if not childUid in uniqueItemLabelLookup:
                    # child might be deleted
                    continue

                children.append(uniqueItemLabelLookup[childUid])

            # Get date/time/duration.
            itemDates = jsonData['core']['data']['itemDatesById'][itemUid]
            era = calendar.get_era(itemDates)
            weekday = calendar.get_weekday(itemDates)
            month = calendar.get_month(itemDates)
            year = calendar.get_year(itemDates)
            day = calendar.get_day(itemDates)
            hour = calendar.get_hour(itemDates)
            minute = calendar.get_minute(itemDates)
            second = calendar.get_second(itemDates)
            timestamp = calendar.get_timestamp(itemDates)
            isoDate = calendar.get_iso_date(itemDates)
            isoTime = calendar.get_iso_time(itemDates)

            # Instantiate the item object.
            self.data.items[itemUid] = Aeon3Item(
                uniqueLabel,
                displayId,
                typeUid,
                label=label,
                shortLabel=shortLabel,
                summary=summary,
                properties=properties,
                tags=tags,
                timestamp=timestamp,
                isoDate=isoDate,
                isoTime=isoTime,
                era=era,
                weekday=weekday,
                month=month,
                year=year,
                day=day,
                hour=hour,
                minute=minute,
                second=second,
                relationships=relationships,
                children=children,
                )

        #--- Create an item index.
        itemIndex = {}
        jsonItemIndex = jsonData['collection']['itemIdsByType']
        for typeUid in jsonItemIndex:
            itemIndex[typeUid] = []
            for itemUid in jsonItemIndex[typeUid]:
                itemIndex[typeUid].append(itemUid)
        self.data.itemIndex = itemIndex

        #--- Get the narrative tree.
        self.data.narrative = self._get_narrative_tree(jsonData)
        return 'Aeon 3 file successfully read.'

    def _get_item_label_lookup(self, jsonData):
        # Return a lookup dictionary with unique item labels by UID.
        uniqueItemLabelLookup = {}
        itemLabelLookup = {}
        jsonItems = jsonData['core']['data']['itemsById']
        for itemUid in jsonItems:
            if not jsonData['collection']['allItemIds'][itemUid]:
                # item might be deleted
                continue

            jsonItem = jsonItems[itemUid]
            aeonLabel = jsonItem.get('label', None)
            if aeonLabel is not None:
                itemLabelLookup[itemUid] = aeonLabel
                uniqueLabel = self._get_unique_label(aeonLabel.strip())
                uniqueItemLabelLookup[itemUid] = uniqueLabel
        return itemLabelLookup, uniqueItemLabelLookup

    def _get_item_types(self, jsonData):
        # Return a dictionary with item types by UID.
        itemTypes = {}
        jsonTypes = jsonData['core']['definitions']['types']['byId']
        for typeUid in jsonTypes:
            label = jsonTypes[typeUid].get('label', '').strip()
            isNarrativeFolder = jsonTypes[typeUid].get('isNarrativeFolder', None)
            itemTypes[typeUid] = Aeon3Type(label, isNarrativeFolder)
        return itemTypes

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

    def _get_narrative_tree(self, jsonData):
        # Return a tree of narrative item UIDs.

        def get_branch(uid, branch):
            for child in jsonNarrative[uid]['children']:
                branch[child] = {}
                get_branch(child, branch[child])

        narrativeTree = {}
        jsonNarrative = jsonData['collection'].get('narrativeSacById', None)
        if jsonNarrative is None:
            return narrativeTree

        for folderUid in jsonNarrative:
            if jsonNarrative[folderUid]['super'] is None:
                break

        narrativeTree[folderUid] = {}
        get_branch(folderUid, narrativeTree[folderUid])
        return narrativeTree

    def _get_property_enum_lookup(self, jsonData):
        # Return a lookup dictionary with allowed property enum labels by UID.
        propertyEnumLookup = {}
        propertyTypes = jsonData['core']['definitions']['properties']['byId']
        for propertyTypeUid in propertyTypes:
            propertyType = propertyTypes[propertyTypeUid]
            for enumUid in propertyType['allowed']:
                enumLabel = propertyType['allowed'][enumUid]['label']
                propertyEnumLookup[enumUid] = enumLabel
        return propertyEnumLookup

    def _get_property_type_lookup(self, jsonData):
        # Return a lookup dictionary with property type labels by UID.
        propertyTypeLookup = {}
        propertyTypes = jsonData['core']['definitions']['properties']['byId']
        for propertyTypeUid in propertyTypes:
            propertyType = propertyTypes[propertyTypeUid]
            propertyTypeLabel = propertyType['label']
            propertyTypeLookup[propertyTypeUid] = propertyTypeLabel.strip()
        return propertyTypeLookup

    def _get_relationship_type_lookup(self, jsonData):
        # Return a lookup dictionary with relationship type labels by UID.
        relationshipTypeLookup = {}
        relationshipTypes = jsonData['core']['definitions']['references']['byId']
        for relationshipTypeUid in relationshipTypes:
            relationshipType = relationshipTypes[relationshipTypeUid]['label']
            relationshipTypeLookup[relationshipTypeUid] = relationshipType.strip()
        return relationshipTypeLookup

    def _get_tag_lookup(self, jsonData):
        # Return a lookup dictionary with tags by UID.
        tagLookup = {}
        tags = jsonData['core']['data']['tags']
        for tagUid in tags:
            tagName = tags[tagUid]
            tagLookup[tagUid] = tagName.strip()
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
