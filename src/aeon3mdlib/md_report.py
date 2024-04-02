"""Provide a class for Markdown project report export.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/aeon3obsidian
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from aeon3obsidianlib.md_aeon import MdAeon


class MdReport(MdAeon):
    """Markdown scene summaries file representation.

    Export a full synopsis.
    """
    DESCRIPTION = 'Project report'
    SUFFIX = '_report'

    _partTemplate = '''# $Title – $Desc
    
'''

    _chapterTemplate = '''## $Title – $Desc
    
'''

    _sceneTemplate = '''### Scene $SceneNumber – ${Title}
    
**Tags:** $Tags


**Location:** $Locations


**Date/Time/Duration:** $ScDate $ScTime $Duration


**Participants:** $Characters


$Desc


**Notes:** $Notes

'''

    _characterSectionHeading = '''# Characters
    
'''

    _characterTemplate = '''## $Title$FullName$AKA


**Tags:** $Tags


$Bio


$Goals


$Desc


**Notes:** $Notes

'''

    _locationSectionHeading = '''## Locations

'''

    _locationTemplate = '''## ">$Title$AKA
    
**Tags:** $Tags


$Desc

'''
