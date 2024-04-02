"""Provide a class for Markdown scene descriptions export.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/aeon3obsidian
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from aeon3obsidianlib.md_aeon import MdAeon


class MdFullSynopsis(MdAeon):
    """Markdown scene summaries file representation.

    Export a full synopsis.
    """
    DESCRIPTION = 'Full synopsis'
    SUFFIX = '_full_synopsis'

    _partTemplate = '''# $Title
    
'''

    _chapterTemplate = '''## $Title
    
'''

    _sceneTemplate = '''<!--- $Title --->

$Desc

'''

    _sceneDivider = '''* * *

'''
