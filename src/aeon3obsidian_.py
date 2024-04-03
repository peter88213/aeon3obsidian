#!/usr/bin/python3
"""Convert Aeon Timeline 3 project data to Obsidian Markdown fileset. 

usage: aeon3obsidian.py Sourcefile

positional arguments:
  Sourcefile  The path of the .aeon or .csv file.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/aeon3obsidian
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import sys
from aeon3obsidianlib.aeon3_file import Aeon3File
from aeon3obsidianlib.obsidian_files import ObsidianFiles


def main(sourcePath):
    """Convert an .aeon source file to a set of Markdown files.
    
    Positional arguments:
        sourcePath -- str: The path of the .aeon file.
        
    """

    # Create an Aeon 3 file object and read the data.
    aeon3File = Aeon3File(sourcePath)
    print(aeon3File.read())

    # Define the output directory.
    aeonDir, aeonFilename = os.path.split(sourcePath)
    projectName = os.path.splitext(aeonFilename)[0]
    obsidianFolder = os.path.join(aeonDir, projectName)

    # Create an Obsidian fileset object and write the data.
    obsidianFiles = ObsidianFiles(obsidianFolder)
    obsidianFiles.items = aeon3File.items
    obsidianFiles.labels = aeon3File.labels
    obsidianFiles.itemIndex = aeon3File.itemIndex
    obsidianFiles.relationships = aeon3File.relationships
    obsidianFiles.narrative = aeon3File.narrative
    print(obsidianFiles.write())


if __name__ == '__main__':
    main(sys.argv[1])
