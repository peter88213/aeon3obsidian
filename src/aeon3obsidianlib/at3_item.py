"""Provide a class for Aeon Timeline 3 items.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/aeon3obsidian
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""

from aeon3obsidianlib.aeon3obsidian_globals import output


class At3Item:

    def __init__(
            self,
            label,
            shortLabel=None,
            summary=None,
            tags=None,
            dateStr=None,
            timeStr=None,
            durationStr=None,
            relationships=[],
            children=[],
            ):

        #--- Set properties.
        self.label = label
        self.shortLabel = shortLabel
        output(f' - shortLabel    : {self.shortLabel}')
        self.summary = summary
        output(f' - summary       : {self.summary}')
        self.tags = tags
        output(f' - tags          : {self.tags}')

        #--- Set date/time/duration.
        if dateStr:
            self.date = dateStr
            output(f' - date          : {dateStr}')
        if timeStr:
            self.time = timeStr
            output(f' - time          : {timeStr}')
        if durationStr:
            self.duration = durationStr
            output(f' - duration      : {durationStr}')

        #--- Set relationships.
        if relationships:
            output(' - relationships :')
            self.relationships = relationships
            for object, reference in self.relationships:
                output(f'    - {reference} : {object}')

        #--- Set children.
        if children:
            output(' - children      :')
            self.children = children
            for child, reference in self.children:
                output(f'    - {reference} : {child}')
