"""Provide a class for Markdown chapter descriptions export.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/aeon3obsidian
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from aeon3obsidianlib.md_aeon import MdAeon


class MdBrieflSynopsis(MdAeon):
    """Markdown chapter summaries snf scene titles file representation.

    Export a brief synopsis.
    """
    DESCRIPTION = 'Brief synopsis'
    SUFFIX = '_brief_synopsis'

    _partTemplate = '''# $Desc

'''

    _chapterTemplate = '''## $Desc
    
'''

    _sceneTemplate = '''$Title
    
'''
