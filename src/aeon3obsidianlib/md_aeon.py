"""Provide a base class for Markdown export from Aeon Timeline 3.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/aeon3obsidian
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
from string import Template
from pywriter.file.file_export import FileExport
from pywriter.pywriter_globals import ERROR


class MdAeon(FileExport):
    """Markdown Aeon Timeline export fileset representation.
    """
    EXTENSION = ''
    DESCRIPTION = 'Obsidian folder'
    FORBIDDEN_CHARACTERS = ('\\', '/', ':', '*', '?', '"', '<', '>', '|')
    # set of characters that filenames cannot contain

    _partTemplate = '''$Desc
    
'''

    _chapterTemplate = '''$Desc
    
'''

    _sceneTemplate = '''**Location:** $Locations

**Date/Time/Duration:** $ScDate $ScTime $Duration

**Participants:** $Characters

$Desc

**Notes:** $Notes

$Tags

'''

    _characterSectionHeading = '''# Characters
    
'''

    _characterTemplate = '''$FullName$AKA

$Bio

$Goals

$Desc

**Notes:** $Notes

$Tags

'''

    _locationSectionHeading = '''## Locations

'''

    _locationTemplate = '''## ">$AKA

$Desc

$Tags

'''

    def _strip_title(self, title):
        for c in self.FORBIDDEN_CHARACTERS:
            title = title.replace(c, '')
        return title

    def _get_characterMapping(self, crId):
        """Return a mapping dictionary for a character section. 
        
        Positional arguments:
            crId -- str: character ID.
        
        Extends the superclass method.
        """
        characterMapping = super()._get_characterMapping(crId)
        if characterMapping['Tags']:
            tags = characterMapping['Tags'].split(', ')
            taglist = []
            for tag in tags:
                taglist.append(f'#{tag.replace(" ","_")}')
            characterMapping['Tags'] = ' '.join(taglist)
        if self.characters[crId].aka:
            characterMapping['AKA'] = f' ("{self.characters[crId].aka}")'
        if self.characters[crId].fullName and self.characters[crId].fullName != self.characters[crId].title:
            characterMapping['FullName'] = f'/{self.characters[crId].fullName}'
        else:
            characterMapping['FullName'] = ''
        return characterMapping

    def _get_locationMapping(self, lcId):
        """Return a mapping dictionary for a location section. 
        
        Positional arguments:
            lcId -- str: location ID.

        Extends the superclass method.
        """
        locationMapping = super().get_locationMapping(lcId)
        if locationMapping['Tags']:
            tags = locationMapping['Tags'].split(', ')
            taglist = []
            for tag in tags:
                taglist.append(f'#{tag.replace(" ","_")}')
            locationMapping['Tags'] = ' '.join(taglist)
        if self.locations[lcId].aka:
            locationMapping['AKA'] = f' ("{self.locations[lcId].aka}")'
        return locationMapping

    def _convert_from_yw(self, text, quick=False):
        """Return text, converted from yw7 markup to target format.
        
        Positional arguments:
            text -- string to convert.
        
        Optional arguments:
            quick -- bool: if True, apply a conversion mode for one-liners without formatting.
        
        Overrides the superclass method.
        """
        if text is None:
            text = ''
        else:
            text = text.strip().replace('\n', '\n\n')
        return(text)

    def _get_sceneMapping(self, scId):
        sceneMapping = super()._get_sceneMapping(scId, 0, 0, 0)
        if sceneMapping['Tags']:
            tags = sceneMapping['Tags'].split(', ')
            taglist = []
            for tag in tags:
                taglist.append(f'#{tag.replace(" ","_")}')
            sceneMapping['Tags'] = ' '.join(taglist)

        if sceneMapping['Characters']:
            characters = sceneMapping['Characters'].split(', ')
            charlist = []
            for character in characters:
                for c in self.FORBIDDEN_CHARACTERS:
                    character = character.replace(c, '')
                charlist.append(f'[[{character}]]')
            sceneMapping['Characters'] = ' '.join(charlist)

        if sceneMapping['Locations']:
            locations = sceneMapping['Locations'].split(', ')
            loclist = []
            for location in locations:
                for c in self.FORBIDDEN_CHARACTERS:
                    location = location.replace(c, '')
                loclist.append(f'[[{location}]]')
            sceneMapping['Locations'] = ' '.join(loclist)

        return sceneMapping

    def _get_scenes(self, chId):
        """Process the scenes.
        
        Positional arguments:
            chId -- str: chapter ID.
        
        Iterate through a sorted scene list and apply the templates, 
        substituting placeholders according to the scene mapping dictionary.
        Skip scenes not accepted by the scene filter.
        
        Return list of strings: Link to the processed scene.
        
        This is a template method that can be extended or overridden by subclasses.
        """
        lines = []
        template = Template(self._sceneTemplate)

        for scId in self.chapters[chId].srtScenes:
            title = self._strip_title(self.scenes[scId].title)
            lines.append(f'- [[{title}]]')
            text = template.safe_substitute(self._get_sceneMapping(scId))
            self.write_file(f'{self._obsidianDir}/{title}.md', text)
        return lines

    def _get_chapters(self):
        """Process the chapters and nested scenes.
        
        Iterate through the sorted chapter list and apply the templates, 
        substituting placeholders according to the chapter mapping dictionary.
        For each chapter call the processing of its included scenes.
        Skip chapters not accepted by the chapter filter.
        Return a list of strings.
        This is a template method that can be extended or overridden by subclasses.
        """
        lines = ['# Narrative']
        template = Template(self._chapterTemplate)

        for chId in self.srtChapters:
            title = self._strip_title(self.chapters[chId].title)
            if not self._chapterFilter.accept(self, chId):
                continue

            if self.chapters[chId].chLevel == 1:
                lines.append(f'## [[{title}]]')
            else:
                lines.append(f'### [[{title}]]')
            text = template.safe_substitute(self._get_chapterMapping(chId, 0))
            self.write_file(f'{self._obsidianDir}/{title}.md', text)

            #--- Process scenes.
            sceneLines = self._get_scenes(chId)
            lines.extend(sceneLines)
        return lines

    def _get_characters(self):
        """Process the characters.
        
        Iterate through the sorted character list and apply the template, 
        substituting placeholders according to the character mapping dictionary.
        Skip characters not accepted by the character filter.
        Return a list of strings.
        This is a template method that can be extended or overridden by subclasses.
        """
        lines = ['# Characters']
        template = Template(self._characterTemplate)

        for crId in self.srtCharacters:
            title = self._strip_title(self.characters[crId].title)
            lines.append(f'- [[{title}]]')
            text = template.safe_substitute(self._get_characterMapping(crId))
            self.write_file(f'{self._obsidianDir}/{title}.md', text)
        return lines

    def _get_locations(self):
        """Process the locations.
        
        Iterate through the sorted location list and apply the template, 
        substituting placeholders according to the location mapping dictionary.
        Skip locations not accepted by the location filter.
        Return a list of strings.
        This is a template method that can be extended or overridden by subclasses.
        """
        lines = ['# Locations']
        template = Template(self._locationTemplate)

        for lcId in self.srtLocations:
            title = self._strip_title(self.locations[lcId].title)
            lines.append(f'- [[{title}]]')
            text = template.safe_substitute(self._get_locationMapping(lcId))
            self.write_file(f'{self._obsidianDir}/{title}.md', text)
        return lines

    def write(self):
        """Write instance variables to the export file.
        
        Create a template-based output file. 
        Return a message beginning with the ERROR constant in case of error.
        """
        aeonDir, aeonFile = os.path.split(self.filePath)
        self._obsidianDir = os.path.join(aeonDir, aeonFile)
        os.makedirs(self._obsidianDir, exist_ok=True)
        lines = []
        try:
            lines.extend(self._get_chapters())
            lines.extend(self._get_characters())
            lines.extend(self._get_locations())
            self.write_file(f'{self._obsidianDir}/_index.md', '\n\n'.join(lines))
        except Exception as ex:
            return f'{ERROR}{str(ex)}'
        return 'Files written.'

    def write_file(self, filePath, text):
        backedUp = False
        if os.path.isfile(filePath):
            try:
                os.replace(filePath, f'{filePath}.bak')
                backedUp = True
            except Exception as ex:
                raise Exception(f'{ERROR}Cannot overwrite "{os.path.normpath(filePath)}": {str(ex)}.')

        try:
            with open(filePath, 'w', encoding='utf-8') as f:
                f.write(text)
        except Exception as ex:
            if backedUp:
                os.replace(f'{filePath}.bak', self.filePath)
            raise Exception(f'Cannot write "{os.path.normpath(filePath)}": {str(ex)}.')

        return f'"{os.path.normpath(filePath)}" written.'

