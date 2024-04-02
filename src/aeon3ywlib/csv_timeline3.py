"""Provide a class for Aeon Timeline 3 csv representation.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/aeon3yw
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import csv
from datetime import datetime
from pywriter.pywriter_globals import ERROR
from pywriter.model.novel import Novel
from pywriter.model.scene import Scene
from pywriter.model.chapter import Chapter
from pywriter.model.world_element import WorldElement
from pywriter.model.character import Character
from aeon3ywlib.dt_helper import fix_iso_dt


class CsvTimeline3(Novel):
    """File representation of a csv file exported by Aeon Timeline 3. 

    Public methods:
        read() -- parse the file and get the instance variables.

    Represents a csv file with a record per scene.
    - Records are separated by line breaks.
    - Data fields are delimited by commas.
    """
    EXTENSION = '.csv'
    DESCRIPTION = 'Aeon Timeline CSV export'
    SUFFIX = ''
    _SEPARATOR = ','

    # Aeon 3 csv export structure (fix part)

    # Types
    _TYPE_EVENT = 'Event'
    _TYPE_NARRATIVE = 'Narrative Folder'

    # Field names
    _LABEL_FIELD = 'Label'
    _TYPE_FIELD = 'Type'
    _SCENE_FIELD = 'Narrative Position'
    _START_DATE_TIME_FIELD = 'Start Date'
    _END_DATE_TIME_FIELD = 'End Date'

    # Narrative position markers
    _PART_MARKER = 'Part'
    _CHAPTER_MARKER = 'Chapter'
    _SCENE_MARKER = 'Scene'
    # Events assigned to the "narrative" become
    # regular scenes, the others become Notes scenes.

    def __init__(self, filePath, **kwargs):
        """Initialize instance variables.

        Positional arguments:
            filePath -- str: path to the file represented by the Novel instance.
            
        Required keyword arguments:
            part_number_prefix -- str: prefix to the part number in the part's heading.
            chapter_number_prefix -- str: prefix to the chapter number in the chapter's heading.
            type_location -- str: label of the "Location" item type representing locations.
            type_item -- str: label of the "Item" item type representing items.
            type_character -- str: label of the "Character" item type representing characters. 
            part_desc_label -- str: label of the csv field for the part's description.
            chapter_desc_label -- str: label of the csv field for the chapter's description.
            scene_desc_label -- str: label of the csv field for the scene's description.
            scene_title_label -- str: label of the csv field for the scene's title.
            notes_label -- str: label of the "Notes" property of events and characters.
            tag_label -- str: label of the csv field for the scene's tags.
            item_label -- str: label of the "Item" role type.
            character_label -- str: label of the "Participant" role type.
            viewpoint_label -- str: label of the "Viewpoint" property of events.
            location_label -- str: label of the "Location" role type.
            character_desc_label1 -- str: label of the character property imported as 1st part of the description.
            character_desc_label2 -- str: label of the character property imported as 2nd part of the description.
            character_desc_label3 -- str: label of the character property imported as 3rd part of the description.
            character_bio_label -- str: 
            character_aka_label -- str: label of the "Nickname" property of characters.           
        
        Extends the superclass constructor.
        """
        super().__init__(filePath, **kwargs)
        self.labels = []
        self.partNrPrefix = kwargs['part_number_prefix']
        if self.partNrPrefix:
            self.partNrPrefix += ' '
        self.chapterNrPrefix = kwargs['chapter_number_prefix']
        if self.chapterNrPrefix:
            self.chapterNrPrefix += ' '
        self.typeLocation = kwargs['type_location']
        self.typeItem = kwargs['type_item']
        self.typeCharacter = kwargs['type_character']
        self.partDescField = kwargs['part_desc_label']
        self.chapterDescField = kwargs['chapter_desc_label']
        self.sceneDescField = kwargs['scene_desc_label']
        self.sceneTitleField = kwargs['scene_title_label']
        self.notesField = kwargs['notes_label']
        self.tagField = kwargs['tag_label']
        self.itemField = kwargs['item_label']
        self.characterField = kwargs['character_label']
        self.viewpointField = kwargs['viewpoint_label']
        self.locationField = kwargs['location_label']
        self.characterDescField1 = kwargs['character_desc_label1']
        self.characterDescField2 = kwargs['character_desc_label2']
        self.characterDescField3 = kwargs['character_desc_label3']
        self.characterBioField = kwargs['character_bio_label']
        self.characterAkaField = kwargs['character_aka_label']
        self.locationDescField = kwargs['location_desc_label']

    def read(self):
        """Parse the file and get the instance variables.
        
        Build a yWriter novel structure from an Aeon3 csv export.
        Return a message beginning with the ERROR constant in case of error.
        Overrides the superclass method.
        """

        def get_lcIds(lcTitles):
            """Return a list of location IDs; Add new location to the project."""
            lcIds = []
            for lcTitle in lcTitles:
                if lcTitle in self.locIdsByTitle:
                    lcIds.append(self.locIdsByTitle[lcTitle])
                else:
                    return None
            return lcIds

        def get_itIds(itTitles):
            """Return a list of item IDs; Add new item to the project."""
            itIds = []
            for itTitle in itTitles:
                if itTitle in self.itmIdsByTitle:
                    itIds.append(self.itmIdsByTitle[itTitle])
                else:
                    return None
            return itIds

        def get_crIds(crTitles):
            """Return a list of character IDs; Add new characters to the project."""
            crIds = []
            for crTitle in crTitles:
                if crTitle in self.chrIdsByTitle:
                    crIds.append(self.chrIdsByTitle[crTitle])
                else:
                    return None
            return crIds
        #--- Read the csv file.
        internalDelimiter = ','
        try:
            with open(self.filePath, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f, delimiter=self._SEPARATOR)
                for label in reader.fieldnames:
                    self.labels.append(label)
                eventsAndFolders = []
                characterCount = 0
                self.chrIdsByTitle = {}
                # key = character title
                # value = character ID
                locationCount = 0
                self.locIdsByTitle = {}
                # key = location title
                # value = location ID
                itemCount = 0
                self.itmIdsByTitle = {}
                # key = item title
                # value = item ID
                for row in reader:
                    aeonEntity = {}
                    for label in row:
                        aeonEntity[label] = row[label]
                    if self._TYPE_EVENT == aeonEntity[self._TYPE_FIELD]:
                        eventsAndFolders.append(aeonEntity)
                    elif self._TYPE_NARRATIVE == aeonEntity[self._TYPE_FIELD]:
                        eventsAndFolders.append(aeonEntity)
                    elif self.typeCharacter == aeonEntity[self._TYPE_FIELD]:
                        characterCount += 1
                        crId = str(characterCount)
                        self.chrIdsByTitle[aeonEntity[self._LABEL_FIELD]] = crId
                        self.characters[crId] = Character()
                        self.characters[crId].title = aeonEntity[self._LABEL_FIELD]
                        charDesc = []
                        if self.characterDescField1 in aeonEntity:
                            charDesc.append(aeonEntity[self.characterDescField1])
                        if self.characterDescField2 and self.characterDescField2 in aeonEntity:
                            charDesc.append(aeonEntity[self.characterDescField2])
                        if self.characterDescField3 and self.characterDescField3 in aeonEntity:
                            charDesc.append(aeonEntity[self.characterDescField3])
                        self.characters[crId].desc = ('\n').join(charDesc)
                        if self.characterBioField in aeonEntity:
                            self.characters[crId].bio = aeonEntity[self.characterBioField]
                        if self.characterAkaField in aeonEntity:
                            self.characters[crId].aka = aeonEntity[self.characterAkaField]
                        if self.tagField in aeonEntity and aeonEntity[self.tagField]:
                            self.characters[crId].tags = aeonEntity[self.tagField].split(internalDelimiter)
                        if self.notesField in aeonEntity:
                            self.characters[crId].notes = aeonEntity[self.notesField]
                        self.srtCharacters.append(crId)
                    elif self.typeLocation == aeonEntity[self._TYPE_FIELD]:
                        locationCount += 1
                        lcId = str(locationCount)
                        self.locIdsByTitle[aeonEntity[self._LABEL_FIELD]] = lcId
                        self.locations[lcId] = WorldElement()
                        self.locations[lcId].title = aeonEntity[self._LABEL_FIELD]
                        self.srtLocations.append(lcId)
                        if self.locationDescField in aeonEntity:
                            self.locations[lcId].desc = aeonEntity[self.locationDescField]
                        if self.tagField in aeonEntity:
                            self.locations[lcId].tags = aeonEntity[self.tagField].split(internalDelimiter)
                    elif self.typeItem == aeonEntity[self._TYPE_FIELD]:
                        itemCount += 1
                        itId = str(itemCount)
                        self.itmIdsByTitle[aeonEntity[self._LABEL_FIELD]] = itId
                        self.items[itId] = WorldElement()
                        self.items[itId].title = aeonEntity[self._LABEL_FIELD]
                        self.srtItems.append(itId)
        except(FileNotFoundError):
            return f'{ERROR}"{os.path.normpath(self.filePath)}" not found.'

        except:
            return f'{ERROR}Can not parse csv file "{os.path.normpath(self.filePath)}".'

        try:
            for label in [self._SCENE_FIELD, self.sceneTitleField, self._START_DATE_TIME_FIELD, self._END_DATE_TIME_FIELD]:
                if not label in self.labels:
                    return f'{ERROR}Label "{label}" is missing.'

            scIdsByStruc = {}
            chIdsByStruc = {}
            otherEvents = []
            eventCount = 0
            chapterCount = 0
            for aeonEntity in eventsAndFolders:
                if aeonEntity[self._SCENE_FIELD]:
                    narrativeType, narrativePosition = aeonEntity[self._SCENE_FIELD].split(' ')

                    # Make the narrative position a sortable string.
                    numbers = narrativePosition.split('.')
                    for i in range(len(numbers)):
                        numbers[i] = numbers[i].zfill(4)
                        narrativePosition = ('.').join(numbers)
                else:
                    narrativeType = ''
                    narrativePosition = ''
                if aeonEntity[self._TYPE_FIELD] == self._TYPE_NARRATIVE:
                    if narrativeType == self._CHAPTER_MARKER:
                        chapterCount += 1
                        chId = str(chapterCount)
                        chIdsByStruc[narrativePosition] = chId
                        self.chapters[chId] = Chapter()
                        self.chapters[chId].chLevel = 0
                        if self.chapterDescField:
                            self.chapters[chId].desc = aeonEntity[self.chapterDescField]
                    elif narrativeType == self._PART_MARKER:
                        chapterCount += 1
                        chId = str(chapterCount)
                        chIdsByStruc[narrativePosition] = chId
                        self.chapters[chId] = Chapter()
                        self.chapters[chId].chLevel = 1
                        narrativePosition += '.0000'
                        if self.partDescField:
                            self.chapters[chId].desc = aeonEntity[self.partDescField]
                    continue

                elif aeonEntity[self._TYPE_FIELD] != self._TYPE_EVENT:
                    continue

                eventCount += 1
                scId = str(eventCount)
                self.scenes[scId] = Scene()
                if narrativeType == self._SCENE_MARKER:
                    self.scenes[scId].isNotesScene = False
                    scIdsByStruc[narrativePosition] = scId
                else:
                    self.scenes[scId].isNotesScene = True
                    otherEvents.append(scId)
                self.scenes[scId].title = aeonEntity[self.sceneTitleField]
                startDateTimeStr = fix_iso_dt(aeonEntity[self._START_DATE_TIME_FIELD])
                if startDateTimeStr is not None:
                    startDateTime = startDateTimeStr.split(' ')
                    self.scenes[scId].date = startDateTime[0]
                    self.scenes[scId].time = startDateTime[1]
                    endDateTimeStr = fix_iso_dt(aeonEntity[self._END_DATE_TIME_FIELD])
                    if endDateTimeStr is not None:
                        # Calculate duration of scenes that begin after 99-12-31.
                        sceneStart = datetime.fromisoformat(startDateTimeStr)
                        sceneEnd = datetime.fromisoformat(endDateTimeStr)
                        sceneDuration = sceneEnd - sceneStart
                        lastsHours = sceneDuration.seconds // 3600
                        lastsMinutes = (sceneDuration.seconds % 3600) // 60
                        self.scenes[scId].lastsDays = str(sceneDuration.days)
                        self.scenes[scId].lastsHours = str(lastsHours)
                        self.scenes[scId].lastsMinutes = str(lastsMinutes)
                else:
                    self.scenes[scId].date = Scene.NULL_DATE
                    self.scenes[scId].time = Scene.NULL_TIME
                if self.sceneDescField in aeonEntity:
                    self.scenes[scId].desc = aeonEntity[self.sceneDescField]
                if self.notesField in aeonEntity:
                    self.scenes[scId].sceneNotes = aeonEntity[self.notesField]
                if self.tagField in aeonEntity and aeonEntity[self.tagField]:
                    self.scenes[scId].tags = aeonEntity[self.tagField].split(internalDelimiter)
                if self.locationField in aeonEntity:
                    self.scenes[scId].locations = get_lcIds(aeonEntity[self.locationField].split(internalDelimiter))
                if self.characterField in aeonEntity:
                    self.scenes[scId].characters = get_crIds(aeonEntity[self.characterField].split(internalDelimiter))
                if self.viewpointField in aeonEntity:
                    vpIds = get_crIds([aeonEntity[self.viewpointField]])
                    if vpIds is not None:
                        vpId = vpIds[0]
                        if self.scenes[scId].characters is None:
                            self.scenes[scId].characters = []
                        elif vpId in self.scenes[scId].characters:
                            self.scenes[scId].characters.remove[vpId]
                        self.scenes[scId].characters.insert(0, vpId)
                if self.itemField in aeonEntity:
                    self.scenes[scId].items = get_itIds(aeonEntity[self.itemField].split(internalDelimiter))

                self.scenes[scId].status = 1
                # Set scene status = "Outline".
        except(FileNotFoundError):
            return f'{ERROR}"{os.path.normpath(self.filePath)}" not found.'

        except(KeyError):
            return f'{ERROR}Wrong csv structure.'

        except(ValueError):
            return f'{ERROR}Wrong date/time format.'

        except:
            return f'{ERROR}Can not parse "{os.path.normpath(self.filePath)}".'

        # Build the chapter structure as defined with Aeon v3.
        srtChpDict = sorted(chIdsByStruc.items())
        srtScnDict = sorted(scIdsByStruc.items())
        partNr = 0
        chapterNr = 0
        for ch in srtChpDict:
            self.srtChapters.append(ch[1])
            if self.chapters[ch[1]].chLevel == 0:
                chapterNr += 1
                self.chapters[ch[1]].title = self.chapterNrPrefix + str(chapterNr)
                for sc in srtScnDict:
                    if sc[0].startswith(ch[0]):
                        self.chapters[ch[1]].srtScenes.append(sc[1])
            else:
                partNr += 1
                self.chapters[ch[1]].title = self.partNrPrefix + str(partNr)
        # Create a chapter for the non-narrative events.
        chapterNr += 1
        chId = str(chapterCount + 1)
        self.chapters[chId] = Chapter()
        self.chapters[chId].title = 'Other events'
        self.chapters[chId].desc = 'Scenes generated from events that ar not assigned to the narrative structure.'
        self.chapters[chId].chType = 1
        self.chapters[chId].srtScenes = otherEvents
        self.srtChapters.append(chId)
        return 'Timeline data converted to novel structure.'
