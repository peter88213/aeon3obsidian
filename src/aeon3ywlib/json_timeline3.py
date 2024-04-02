"""Provide a class for Aeon Timeline 3 JSON representation.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/aeon3yw
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import json
from datetime import datetime
from datetime import timedelta
from pywriter.pywriter_globals import ERROR
from pywriter.model.novel import Novel
from pywriter.model.scene import Scene
from pywriter.model.chapter import Chapter
from pywriter.model.world_element import WorldElement
from pywriter.model.character import Character
from aeon3ywlib.aeon3_fop import scan_file


class JsonTimeline3(Novel):
    """File representation of an Aeon Timeline 3 project. 

    Public methods:
        read() -- parse the file and get the instance variables.

    Represents the JSON part of the project file.
    """
    EXTENSION = '.aeon'
    DESCRIPTION = 'Aeon Timeline 3 project'
    SUFFIX = ''
    DATE_LIMIT = (datetime(100, 1, 1) - datetime.min).total_seconds()
    # Dates before 100-01-01 can not be displayed properly in yWriter

    def __init__(self, filePath, **kwargs):
        """Initialize instance variables.

        Positional arguments:
            filePath -- str: path to the file represented by the Novel instance.
            
        Required keyword arguments:
            type_event -- str: label of the "Event" item type representing scenes.
            type_character -- str: label of the "Character" item type representing characters. 
            type_location -- str: label of the "Location" item type representing locations.
            type_item -- str: label of the "Item" item type representing items.
            notes_label -- str: label of the "Notes" property of events and characters.
            character_desc_label1 -- str: label of the character property imported as 1st part of the description.
            character_desc_label2 -- str: label of the character property imported as 2nd part of the description.
            character_desc_label3 -- str: label of the character property imported as 3rd part of the description.
            character_aka_label -- str: label of the "Nickname" property of characters.
            viewpoint_label -- str: label of the "Viewpoint" property of events.
            character_label -- str: label of the "Participant" role type.
            location_label -- str: label of the "Location" role type.
            item_label -- str: label of the "Item" role type.
            part_number_prefix -- str: prefix to the part number in the part's heading.
            chapter_number_prefix -- str: prefix to the chapter number in the chapter's heading.
        
        Extends the superclass constructor.
        """
        super().__init__(filePath, **kwargs)

        # JSON[definitions][types][byId]
        self._labelEventType = kwargs['type_event']
        self._labelCharacterType = kwargs['type_character']
        self._labelLocationType = kwargs['type_location']
        self._labelItemType = kwargs['type_item']

        # JSON[definitions][properties][byId]
        self._labelNotesProperty = kwargs['notes_label']
        self._labelChrDesc1Property = kwargs['character_desc_label1']
        self._labelChrDesc2Property = kwargs['character_desc_label2']
        self._labelChrDesc3Property = kwargs['character_desc_label3']
        self._labelAkaProperty = kwargs['character_aka_label']
        self._labelViewpointProperty = kwargs['viewpoint_label']

        # JSON[definitions][references][byId]
        self._labelParticipantRef = kwargs['character_label']
        self._labelLocationRef = kwargs['location_label']
        self._labelItemRef = kwargs['item_label']

        # Misc.
        self._partHdPrefix = kwargs['part_number_prefix']
        self._chapterHdPrefix = kwargs['chapter_number_prefix']

    def read(self):
        """Parse the file and get the instance variables.
        
        Extract the JSON part of the Aeon Timeline 3 file located at filePath
        and build a yWriter novel structure.
        Return a message beginning with the ERROR constant in case of error.
        Overrides the superclass method.
        """
        jsonPart = scan_file(self.filePath)
        if not jsonPart:
            return f'{ERROR}No JSON part found.'
        elif jsonPart.startswith(ERROR):
            return jsonPart
        try:
            jsonData = json.loads(jsonPart)
        except('JSONDecodeError'):
            return f'{ERROR}Invalid JSON data.'

        #--- Find types.
        typeEventUid = None
        typeCharacterUid = None
        typeLocationUid = None
        typeItemUid = None
        NarrativeFolderTypes = []
        for uid in jsonData['definitions']['types']['byId']:

            if jsonData['definitions']['types']['byId'][uid]['isNarrativeFolder']:
                NarrativeFolderTypes.append(uid)

            elif jsonData['definitions']['types']['byId'][uid]['label'] == self._labelEventType:
                typeEventUid = uid

            elif jsonData['definitions']['types']['byId'][uid]['label'] == self._labelCharacterType:
                typeCharacterUid = uid

            elif jsonData['definitions']['types']['byId'][uid]['label'] == self._labelLocationType:
                typeLocationUid = uid

            elif jsonData['definitions']['types']['byId'][uid]['label'] == self._labelItemType:
                typeItemUid = uid

        #--- Find properties.
        propNotesUid = None
        propChrDesc1Uid = None
        propChrDesc2Uid = None
        propChrDesc3Uid = None
        propAkaUid = None
        propViewpointUid = None
        for uid in jsonData['definitions']['properties']['byId']:

            if jsonData['definitions']['properties']['byId'][uid]['label'] == self._labelNotesProperty:
                typeNotesUid = uid

            elif jsonData['definitions']['properties']['byId'][uid]['label'] == self._labelChrDesc1Property:
                propChrDesc1Uid = uid

            elif jsonData['definitions']['properties']['byId'][uid]['label'] == self._labelChrDesc2Property:
                propChrDesc2Uid = uid

            elif jsonData['definitions']['properties']['byId'][uid]['label'] == self._labelChrDesc3Property:
                propChrDesc3Uid = uid

            elif jsonData['definitions']['properties']['byId'][uid]['label'] == self._labelAkaProperty:
                propAkaUid = uid

            elif jsonData['definitions']['properties']['byId'][uid]['label'] == self._labelViewpointProperty:
                propViewpointUid = uid

        #--- Find references.
        refParticipant = None
        refLocation = None
        for uid in jsonData['definitions']['references']['byId']:

            if jsonData['definitions']['references']['byId'][uid]['label'] == self._labelParticipantRef:
                refParticipant = uid

            elif jsonData['definitions']['references']['byId'][uid]['label'] == self._labelLocationRef:
                refLocation = uid

        #--- Read items.
        crIdsByGuid = {}
        lcIdsByGuid = {}
        itIdsByGuid = {}
        scIdsByGuid = {}
        chIdsByGuid = {}
        characterCount = 0
        locationCount = 0
        itemCount = 0
        eventCount = 0
        chapterCount = 0
        vpGuidByScId = {}
        for uid in jsonData['data']['items']['byId']:
            dataItem = jsonData['data']['items']['byId'][uid]
            if dataItem['type'] == typeEventUid:

                #--- Create scenes.
                eventCount += 1
                scId = str(eventCount)
                scIdsByGuid[uid] = scId
                self.scenes[scId] = Scene()
                self.scenes[scId].status = 1
                # Set scene status = "Outline"
                self.scenes[scId].isNotesScene = True
                # Will be set to False later if it is part of the narrative.
                self.scenes[scId].title = dataItem['label']
                self.scenes[scId].desc = dataItem['summary']
                timestamp = dataItem['startDate']['timestamp']

                #--- Get scene tags.
                for tagId in dataItem['tags']:
                    if self.scenes[scId].tags is None:
                        self.scenes[scId].tags = []
                    self.scenes[scId].tags.append(jsonData['data']['tags'][tagId])

                #--- Get scene properties.
                for propId in dataItem['propertyValues']:
                    if propId == propNotesUid:
                        self.scenes[scId].sceneNotes = dataItem['propertyValues'][propId]
                    elif propId == propViewpointUid:
                        vpGuidByScId[scId] = dataItem['propertyValues'][propId]

                #--- Get scene date, time, and duration.
                if timestamp is not None and timestamp >= self.DATE_LIMIT:
                    # Restrict date/time calculation to dates within yWriter's range
                    sceneStart = datetime.min + timedelta(seconds=timestamp)
                    startDateTime = sceneStart.isoformat().split('T')
                    self.scenes[scId].date = startDateTime[0]
                    self.scenes[scId].time = startDateTime[1]

                    # Calculate duration.
                    if dataItem['duration']['years'] > 0 or dataItem['duration']['months'] > 0:
                        endYear = sceneStart.year + dataItem['duration']['years']
                        endMonth = sceneStart.month
                        if dataItem['duration']['months'] > 0:
                            endMonth += dataItem['duration']['months']
                            while endMonth > 12:
                                endMonth -= 12
                                endYear += 1
                        sceneDuration = datetime(endYear, endMonth, sceneStart.day) - \
                                datetime(sceneStart.year, sceneStart.month, sceneStart.day)
                        lastsDays = sceneDuration.days
                        lastsHours = sceneDuration.seconds // 3600
                        lastsMinutes = (sceneDuration.seconds % 3600) // 60
                    else:
                        lastsDays = 0
                        lastsHours = 0
                        lastsMinutes = 0
                    lastsDays += dataItem['duration']['weeks'] * 7
                    lastsDays += dataItem['duration']['days']
                    lastsDays += dataItem['duration']['hours'] // 24
                    lastsHours += dataItem['duration']['hours'] % 24
                    lastsHours += dataItem['duration']['minutes'] // 60
                    lastsMinutes += dataItem['duration']['minutes'] % 60
                    lastsMinutes += dataItem['duration']['seconds'] // 60
                    lastsHours += lastsMinutes // 60
                    lastsMinutes %= 60
                    lastsDays += lastsHours // 24
                    lastsHours %= 24
                    self.scenes[scId].lastsDays = str(lastsDays)
                    self.scenes[scId].lastsHours = str(lastsHours)
                    self.scenes[scId].lastsMinutes = str(lastsMinutes)
            elif dataItem['type'] in NarrativeFolderTypes:
                #--- Create chapters.
                chapterCount += 1
                chId = str(chapterCount)
                chIdsByGuid[uid] = chId
                self.chapters[chId] = Chapter()
                self.chapters[chId].desc = dataItem['label']
            elif dataItem['type'] == typeCharacterUid:
                #--- Create characters.
                characterCount += 1
                crId = str(characterCount)
                crIdsByGuid[uid] = crId
                self.characters[crId] = Character()
                if dataItem['shortLabel']:
                    self.characters[crId].title = dataItem['shortLabel']
                else:
                    self.characters[crId].title = dataItem['label']
                self.characters[crId].fullName = dataItem['label']
                self.characters[crId].bio = dataItem['summary']
                self.srtCharacters.append(crId)

                #--- Get character tags.
                for tagId in dataItem['tags']:
                    if self.characters[crId].tags is None:
                        self.characters[crId].tags = []
                    self.characters[crId].tags.append(jsonData['data']['tags'][tagId])

                #--- Get character properties.
                charDesc = []
                for propId in dataItem['propertyValues']:
                    if propId == propNotesUid:
                        self.characters[crId].notes = dataItem['propertyValues'][propId]
                    elif propId == propAkaUid:
                        self.characters[crId].aka = dataItem['propertyValues'][propId]
                    elif propId == propChrDesc1Uid:
                        charDesc.append(dataItem['propertyValues'][propId])
                    elif propId == propChrDesc2Uid:
                        charDesc.append(dataItem['propertyValues'][propId])
                    elif propId == propChrDesc3Uid:
                        charDesc.append(dataItem['propertyValues'][propId])
                self.characters[crId].desc = ('\n').join(charDesc)
            elif dataItem['type'] == typeLocationUid:
                #--- Create locations.
                locationCount += 1
                lcId = str(locationCount)
                lcIdsByGuid[uid] = lcId
                self.locations[lcId] = WorldElement()
                self.locations[lcId].title = dataItem['label']
                self.locations[lcId].desc = dataItem['summary']
                self.srtLocations.append(lcId)

                #--- Get location tags.
                for tagId in dataItem['tags']:
                    if self.locations[lcId].tags is None:
                        self.locations[lcId].tags = []
                    self.locations[lcId].tags.append(jsonData['data']['tags'][tagId])
            elif dataItem['type'] == typeItemUid:
                #--- Create items.
                itemCount += 1
                itId = str(itemCount)
                itIdsByGuid[uid] = itId
                self.items[itId] = WorldElement()
                self.items[itId].title = dataItem['label']
                self.items[itId].desc = dataItem['summary']
                self.srtItems.append(itId)

                #--- Get item tags.
                for tagId in dataItem['tags']:
                    if self.items[itId].tags is None:
                        self.items[itId].tags = []
                    self.items[itId].tags.append(jsonData['data']['tags'][tagId])
        #--- Read relationships.
        for uid in jsonData['data']['relationships']['byId']:
            if jsonData['data']['relationships']['byId'][uid]['reference'] == refParticipant:
                #--- Assign characters.
                try:
                    scId = scIdsByGuid[jsonData['data']['relationships']['byId'][uid]['subject']]
                    crId = crIdsByGuid[jsonData['data']['relationships']['byId'][uid]['object']]
                    if self.scenes[scId].characters is None:
                        self.scenes[scId].characters = []
                    if not crId in self.scenes[scId].characters:
                        self.scenes[scId].characters.append(crId)
                except:
                    pass
            elif jsonData['data']['relationships']['byId'][uid]['reference'] == refLocation:
                #--- Assign locations.
                try:
                    scId = scIdsByGuid[jsonData['data']['relationships']['byId'][uid]['subject']]
                    lcId = lcIdsByGuid[jsonData['data']['relationships']['byId'][uid]['object']]
                    if self.scenes[scId].locations is None:
                        self.scenes[scId].locations = []
                    if not lcId in self.scenes[scId].locations:
                        self.scenes[scId].locations.append(lcId)
                except:
                    pass
        #--- Set scene viewpoints.
        for scId in vpGuidByScId:
            if vpGuidByScId[scId] in crIdsByGuid:
                vpId = crIdsByGuid[vpGuidByScId[scId]]
                if self.scenes[scId].characters is None:
                    self.scenes[scId].characters = []
                elif vpId in self.scenes[scId].characters:
                    self.scenes[scId].characters.remove[vpId]
                self.scenes[scId].characters.insert(0, vpId)
        #--- Build a narrative structure with 2 or 3 levels.
        for narrative0 in jsonData['data']['narrative']['children']:
            if narrative0['id'] in chIdsByGuid:
                self.srtChapters.append(chIdsByGuid[narrative0['id']])
            for narrative1 in narrative0['children']:
                if narrative1['id'] in chIdsByGuid:
                    self.srtChapters.append(chIdsByGuid[narrative1['id']])
                    self.chapters[chIdsByGuid[narrative0['id']]].chLevel = 1
                    for narrative2 in narrative1['children']:
                        if narrative2['id'] in scIdsByGuid:
                            self.chapters[chIdsByGuid[narrative1['id']]].srtScenes.append(
                                scIdsByGuid[narrative2['id']])
                            self.scenes[scIdsByGuid[narrative2['id']]].isNotesScene = False
                            self.chapters[chIdsByGuid[narrative1['id']]].chLevel = 0
                elif narrative1['id'] in scIdsByGuid:
                    self.chapters[chIdsByGuid[narrative0['id']]].srtScenes.append(scIdsByGuid[narrative1['id']])
                    self.scenes[scIdsByGuid[narrative1['id']]].isNotesScene = False
                    self.chapters[chIdsByGuid[narrative0['id']]].chLevel = 0
        #--- Auto-number untitled chapters.
        partCount = 0
        chapterCount = 0
        for chId in self.srtChapters:
            if self.chapters[chId].chLevel == 1:
                partCount += 1
                if not self.chapters[chId].title:
                    self.chapters[chId].title = f'{self._partHdPrefix} {partCount}'
            else:
                chapterCount += 1
                if not self.chapters[chId].title:
                    self.chapters[chId].title = f'{self._chapterHdPrefix} {chapterCount}'
        #--- Create a "Notes" chapter for non-narrative scenes.
        chId = str(partCount + chapterCount + 1)
        self.chapters[chId] = Chapter()
        self.chapters[chId].title = 'Other events'
        self.chapters[chId].desc = 'Scenes generated from events that ar not assigned to the narrative structure.'
        self.chapters[chId].chType = 1
        self.srtChapters.append(chId)
        for scId in self.scenes:
            if self.scenes[scId].isNotesScene:
                self.chapters[chId].srtScenes.append(scId)
        return 'Timeline data converted to novel structure.'
