#!/usr/bin/python3
"""Convert Aeon Aeon3Data 3 project data to Obsidian Markdown fileset. 

Version @release
Requires Python 3.6+

usage: aeon3obsidian.py Sourcefile

positional arguments:
  Sourcefile  The path of the .aeon file.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/aeon3obsidian
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)

This program is free software: you can redistribute it and/or modify 
it under the terms of the GNU General Public License as published by 
the Free Software Foundation, either version 3 of the License, or 
(at your option) any later version.

This program is distributed in the hope that it will be useful, 
but WITHOUT ANY WARRANTY; without even the implied warranty of 
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
GNU General Public License for more details.
"""
import os
import sys

from aeon3obsidianlib.aeon3_data import Aeon3Data
from aeon3obsidianlib.aeon3_file import Aeon3File
from aeon3obsidianlib.obsidian_files import ObsidianFiles


def main(sourcePath):
    """Convert an .aeon source file to a set of Markdown files.
    
    Positional arguments:
        sourcePath -- str: The path of the .aeon file.
    """
    print('aeon3obsidian version @release')

    # Create an Aeon 3 file object and read the data.
    aeon3File = Aeon3File(sourcePath)
    aeon3File.data = Aeon3Data()
    print(aeon3File.read())

    # Define the output directory.
    aeonDir, aeonFilename = os.path.split(sourcePath)
    projectName = os.path.splitext(aeonFilename)[0]
    obsidianFolder = os.path.join(aeonDir, projectName)

    # Create an Obsidian fileset object and write the data.
    obsidianFiles = ObsidianFiles(obsidianFolder)
    obsidianFiles.data = aeon3File.data
    # print(obsidianFiles.write())


if __name__ == '__main__':
    main(sys.argv[1])
