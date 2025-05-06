"""Build a stub for the aeon3obsidian regression test.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/aeon3obsidian
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os
import sys
import inliner

SRC = '../src/'
BUILD = '../test/'
SOURCE_FILE = f'{SRC}aeon3obsidian_.py'
TARGET_FILE = f'{BUILD}aeon3obsidian.py'


def main():
    inliner.run(SOURCE_FILE, TARGET_FILE, 'aeon3lib', '../src/')
    print('Done.')


if __name__ == '__main__':
    main()
