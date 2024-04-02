"""Provide a class for Markdown descriptions export.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/aeon3obsidian
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from aeon3obsidianlib.md_aeon import MdAeon


class MdLocationSheets(MdAeon):
    """Markdown location descriptions file representation.

    Export a location sheet.
    """
    DESCRIPTION = 'Location sheets'
    SUFFIX = '_location_sheets'

    _locationTemplate = '''## $Title$AKA
    
    
**Tags:** $Tags

$Desc

'''
