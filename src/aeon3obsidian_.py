#!/usr/bin/python3
"""Convert Aeon Timeline 3 project data to Obsidian Markdown files. 

usage: aeon3obsidian.py [-h] [--silent] Sourcefile Suffix

positional arguments:
  Sourcefile  The path of the .aeon or .csv file.

optional arguments:
  -h, --help  show this help message and exit
  --silent    suppress messages and the request to confirm overwriting


Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/aeon3obsidian
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import argparse
from argparse import RawTextHelpFormatter
import os
from pywriter.ui.ui import Ui
from pywriter.ui.ui_cmd import UiCmd
from pywriter.config.configuration import Configuration
from aeon3obsidianlib.aeon3obsidian_converter import Aeon3ObsidianConverter

SETTINGS = dict(
    part_number_prefix='Part',
    chapter_number_prefix='Chapter',
    type_event='Event',
    type_character='Character',
    type_location='Location',
    type_item='Item',
    character_label='Participant',
    location_label='Location',
    item_label='Item',
    part_desc_label='Label',
    chapter_desc_label='Label',
    scene_desc_label='Summary',
    scene_title_label='Label',
    notes_label='Notes',
    tag_label='Tags',
    viewpoint_label='Viewpoint',
    character_bio_label='Summary',
    character_aka_label='Nickname',
    character_desc_label1='Characteristics',
    character_desc_label2='Traits',
    character_desc_label3='',
    location_desc_label='Summary',
)


def main(sourcePath, silent=True):
    """Convert an .aeon or .csv source file to Markdown target files.
    
    Positional arguments:
        sourcePath -- str: The path of the .aeon or .csv file.
        
    Optional arguments:
        silent -- boolean: If True, suppress messages and the request to confirm overwriting.    
    """
    converter = Aeon3ObsidianConverter()
    if silent:
        converter.ui = Ui('')
    else:
        converter.ui = UiCmd('Convert Aeon Timeline 3 project data to Obsidian.')
    iniFileName = 'aeon3obsidian.ini'
    sourceDir = os.path.dirname(sourcePath)
    if not sourceDir:
        sourceDir = './'
    else:
        sourceDir += '/'
    iniFiles = [f'{sourceDir}{iniFileName}']
    configuration = Configuration(SETTINGS)
    for iniFile in iniFiles:
        configuration.read(iniFile)
    kwargs = {'suffix': ''}
    kwargs.update(configuration.settings)
    kwargs.update(configuration.options)
    converter.run(sourcePath, **kwargs)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Convert Aeon Timeline 3 project data to Obsidian markdown files.',
        epilog='', formatter_class=RawTextHelpFormatter)
    parser.add_argument('sourcePath', metavar='Sourcefile',
                        help='The path of the .aeon or .csv file.')
    parser.add_argument('--silent',
                        action="store_true",
                        help='suppress messages and the request to confirm overwriting')
    args = parser.parse_args()
    main(args.sourcePath, args.silent)

