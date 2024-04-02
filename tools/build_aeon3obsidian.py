"""Build a stub for the aeon3obsidian regression test.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/aeon3obsidian
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import sys
import inliner

SRC = '../src/'
BUILD = '../test/'
SOURCE_FILE = f'{SRC}aeon3obsidian_.py'
TARGET_FILE = f'{BUILD}aeon3obsidian.py'


def main():
    inliner.run(SOURCE_FILE, TARGET_FILE, 'aeon3obsidianlib', '../src/')
    inliner.run(TARGET_FILE, TARGET_FILE, 'aeon3ywlib', '../src/')
    inliner.run(TARGET_FILE, TARGET_FILE, 'pywriter', '../src/')
    print('Done.')


if __name__ == '__main__':
    main()
