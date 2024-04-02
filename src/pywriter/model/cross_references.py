"""Provide a class for yWriter cross reference generation.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""


class CrossReferences:
    """Dictionaries containing a novel's cross references.

    Public methods:
        generate_xref(novel) -- Generate cross references for a novel.

    Public instance variables:
        scnPerChr -- scenes per character.
        scnPerLoc -- scenes per location.
        scnPerItm -- scenes per item.
        scnPerTag -- scenes per tag.
        chrPerTag -- characters per tag.
        locPerTag -- locations per tag.
        itmPerTag -- items per tag.
        chpPerScn -- chapters per scene.
        srtScenes -- the novel's sorted scene IDs.
    """

    def __init__(self):
        """Initialize instance variables."""
        
        # Cross reference dictionaries:

        self.scnPerChr = {}
        # dict
        # key = character ID, value: list of scene IDs
        # Scenes per character

        self.scnPerLoc = {}
        # dict
        # key = location ID, value: list of scene IDs
        # Scenes per location

        self.scnPerItm = {}
        # dict
        # key = item ID, value: list of scene IDs
        # Scenes per item

        self.scnPerTag = {}
        # dict
        # key = tag, value: list of scene IDs
        # Scenes per tag

        self.chrPerTag = {}
        # dict
        # key = tag, value: list of character IDs
        # Characters per tag

        self.locPerTag = {}
        # dict
        # key = tag, value: list of location IDs
        # Locations per tag

        self.itmPerTag = {}
        # dict
        # key = tag, value: list of item IDs
        # Items per tag

        self.chpPerScn = {}
        # dict
        # key = scene ID, value: chapter ID
        # Chapter to which the scene belongs

        self.srtScenes = None
        # list of str
        # Scene IDs in the overall order

    def generate_xref(self, novel):
        """Generate cross references for a novel.
        
        Positional argument:
            novel -- Novel instance to process.
        """
        self.scnPerChr = {}
        self.scnPerLoc = {}
        self.scnPerItm = {}
        self.scnPerTag = {}
        self.chrPerTag = {}
        self.locPerTag = {}
        self.itmPerTag = {}
        self.chpPerScn = {}
        self.srtScenes = []

        #--- Characters per tag.
        for crId in novel.srtCharacters:
            self.scnPerChr[crId] = []
            if novel.characters[crId].tags:
                for tag in novel.characters[crId].tags:
                    if not tag in self.chrPerTag:
                        self.chrPerTag[tag] = []
                    self.chrPerTag[tag].append(crId)

        #--- Locations per tag.
        for lcId in novel.srtLocations:
            self.scnPerLoc[lcId] = []
            if novel.locations[lcId].tags:
                for tag in novel.locations[lcId].tags:
                    if not tag in self.locPerTag:
                        self.locPerTag[tag] = []
                    self.locPerTag[tag].append(lcId)

        #--- Items per tag.
        for itId in novel.srtItems:
            self.scnPerItm[itId] = []
            if novel.items[itId].tags:
                for tag in novel.items[itId].tags:
                    if not tag in self.itmPerTag:
                        self.itmPerTag[tag] = []
                    self.itmPerTag[tag].append(itId)
                    
        #--- Process chapters and scenes.
        for chId in novel.srtChapters:

            for scId in novel.chapters[chId].srtScenes:
                self.srtScenes.append(scId)
                self.chpPerScn[scId] = chId

                #--- Scenes per character.
                if novel.scenes[scId].characters:
                    for crId in novel.scenes[scId].characters:
                        self.scnPerChr[crId].append(scId)

                #--- Scenes per location.
                if novel.scenes[scId].locations:
                    for lcId in novel.scenes[scId].locations:
                        self.scnPerLoc[lcId].append(scId)

                #--- Scenes per item.
                if novel.scenes[scId].items:
                    for itId in novel.scenes[scId].items:
                        self.scnPerItm[itId].append(scId)

                #--- Scenes per tag.
                if novel.scenes[scId].tags:
                    for tag in novel.scenes[scId].tags:
                        if not tag in self.scnPerTag:
                            self.scnPerTag[tag] = []
                        self.scnPerTag[tag].append(scId)
