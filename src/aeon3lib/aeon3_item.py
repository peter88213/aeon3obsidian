"""Provide a class for Aeon Timeline 3 items.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/aeon3obsidian
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""

from aeon3lib.aeon3obsidian_globals import output


class Aeon3Item:

    def __init__(
            self,
            label,
            shortLabel=None,
            summary=None,
            properties=[],
            tags=None,
            timestamp=None,
            era=None,
            dateStr=None,
            timeStr=None,
            durationStr=None,
            relationships=[],
            children=[],
            ):

        self.label = label
        self.shortLabel = shortLabel
        self.summary = summary
        self.properties = properties
        self.tags = tags
        self.timestamp = timestamp
        if era:
            self.era, self.eraShortName, self.eraFullName = era
        else:
            self.era = self.eraShortName = self.eraFullName = None
        self.date = dateStr
        self.time = timeStr
        self.duration = durationStr
        self.relationships = relationships
        self.children = children

    def write_to_console(self):
        output(f' - shortLabel    : {self.shortLabel}')
        output(f' - summary       : {self.summary}')
        if self.properties:
            output(' - properties    :')
            for reference, customProperty  in self.properties:
                output(f'    - {reference} : {customProperty}')
        output(f' - tags          : {self.tags}')
        if self.eraShortName and self.eraFullName:
            output(f' - era           : {self.eraFullName} ({self.eraShortName})')
        if self.date:
            output(f' - date          : {self.date}')
        if self.time:
            output(f' - time          : {self.time}')
        if self.duration:
            output(f' - duration      : {self.duration}')
        if self.relationships:
            output(' - relationships :')
            for target, reference in self.relationships:
                output(f'    - {reference} : {target}')
        if self.children:
            output(' - children      :')
            for child  in self.children:
                output(f'    - {child}')
