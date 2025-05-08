"""Provide a class for Aeon Timeline 3 item type representation.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/aeon3obsidian
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""


class Aeon3Type:

    def __init__(self, label, isNarrativeFolder):
        self.label = label
        self.isNarrativeFolder = isNarrativeFolder
