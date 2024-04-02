"""Regression test for the aeon3obsidian project.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/aeon3yw
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from shutil import copyfile
import os
import unittest
import aeon3obsidian_

# Test environment

# The paths are relative to the "test" directory,
# where this script is placed and executed
UPDATE = False

TEST_PATH = os.getcwd() + '/../test'
TEST_DATA_PATH = TEST_PATH + '/data/'
TEST_EXEC_PATH = TEST_PATH + '/'

NORMAL_AEON = TEST_DATA_PATH + 'normal.aeon'
NORMAL_CSV = TEST_DATA_PATH + 'normal.csv'
PARTS = TEST_DATA_PATH + 'parts.md'
CHAPTERS = TEST_DATA_PATH + 'chapters.md'
SCENES = TEST_DATA_PATH + 'scenes.md'
CHARACTERS_A = TEST_DATA_PATH + 'characters_a.md'
CHARACTERS_C = TEST_DATA_PATH + 'characters_c.md'
LOCATIONS = TEST_DATA_PATH + 'locations.md'
REPORT_A = TEST_DATA_PATH + 'report_a.md'
REPORT_C = TEST_DATA_PATH + 'report_c.md'

# Test data
TEST_AEON = TEST_EXEC_PATH + 'yw7 Sample Project.aeon'
TEST_CSV = TEST_EXEC_PATH + 'yw7 Sample Project.csv'
TEST_PARTS = TEST_EXEC_PATH + 'yw7 Sample Project_chapter_overview.md'
TEST_CHAPTERS = TEST_EXEC_PATH + 'yw7 Sample Project_brief_synopsis.md'
TEST_SCENES = TEST_EXEC_PATH + 'yw7 Sample Project_full_synopsis.md'
TEST_CHARACTERS = TEST_EXEC_PATH + 'yw7 Sample Project_character_sheets.md'
TEST_LOCATIONS = TEST_EXEC_PATH + 'yw7 Sample Project_location_sheets.md'
TEST_REPORT = TEST_EXEC_PATH + 'yw7 Sample Project_report.md'


def read_file(inputFile):
    try:
        with open(inputFile, 'r', encoding='utf-8') as f:
            return f.read()
    except:
        # HTML files exported by a word processor may be ANSI encoded.
        with open(inputFile, 'r') as f:
            return f.read()


def remove_all_testfiles():

    try:
        os.remove(TEST_CSV)
    except:
        pass

    try:
        os.remove(TEST_AEON)
    except:
        pass

    try:
        os.remove(TEST_PARTS)
    except:
        pass

    try:
        os.remove(TEST_CHAPTERS)
    except:
        pass

    try:
        os.remove(TEST_SCENES)
    except:
        pass

    try:
        os.remove(TEST_CHARACTERS)
    except:
        pass

    try:
        os.remove(TEST_LOCATIONS)
    except:
        pass

    try:
        os.remove(TEST_REPORT)
    except:
        pass


class NormalOperation(unittest.TestCase):
    """Test case: Normal operation."""

    def setUp(self):

        try:
            os.mkdir(TEST_EXEC_PATH)

        except:
            pass

        remove_all_testfiles()

    def test_aeon_chapter_overview(self):
        copyfile(NORMAL_AEON, TEST_AEON)
        aeon3obsidian_.main(TEST_AEON, '_chapter_overview')
        if UPDATE:
            copyfile(TEST_PARTS, PARTS)
        self.assertEqual(read_file(TEST_PARTS), read_file(PARTS))

    def test_csv_chapter_overview(self):
        copyfile(NORMAL_CSV, TEST_CSV)
        aeon3obsidian_.main(TEST_CSV, '_chapter_overview')
        if UPDATE:
            copyfile(TEST_PARTS, PARTS)
        self.assertEqual(read_file(TEST_PARTS), read_file(PARTS))

    def test_aeon_brief_synopsis(self):
        copyfile(NORMAL_AEON, TEST_AEON)
        aeon3obsidian_.main(TEST_AEON, '_brief_synopsis')
        if UPDATE:
            copyfile(TEST_CHAPTERS, CHAPTERS)
        self.assertEqual(read_file(TEST_CHAPTERS), read_file(CHAPTERS))

    def test_csv_brief_synopsis(self):
        copyfile(NORMAL_CSV, TEST_CSV)
        aeon3obsidian_.main(TEST_CSV, '_brief_synopsis')
        if UPDATE:
            copyfile(TEST_CHAPTERS, CHAPTERS)
        self.assertEqual(read_file(TEST_CHAPTERS), read_file(CHAPTERS))

    def test_aeon_full_synopsis(self):
        copyfile(NORMAL_AEON, TEST_AEON)
        aeon3obsidian_.main(TEST_AEON, '_full_synopsis')
        if UPDATE:
            copyfile(TEST_SCENES, SCENES)
        self.assertEqual(read_file(TEST_SCENES), read_file(SCENES))

    def test_csv_full_synopsis(self):
        copyfile(NORMAL_CSV, TEST_CSV)
        aeon3obsidian_.main(TEST_CSV, '_full_synopsis')
        if UPDATE:
            copyfile(TEST_SCENES, SCENES)
        self.assertEqual(read_file(TEST_SCENES), read_file(SCENES))

    def test_aeon_character_sheets(self):
        copyfile(NORMAL_AEON, TEST_AEON)
        aeon3obsidian_.main(TEST_AEON, '_character_sheets')
        if UPDATE:
            copyfile(TEST_CHARACTERS, CHARACTERS_A)
        self.assertEqual(read_file(TEST_CHARACTERS), read_file(CHARACTERS_A))

    def test_csv_character_sheets(self):
        copyfile(NORMAL_CSV, TEST_CSV)
        aeon3obsidian_.main(TEST_CSV, '_character_sheets')
        if UPDATE:
            copyfile(TEST_CHARACTERS, CHARACTERS_C)
        self.assertEqual(read_file(TEST_CHARACTERS), read_file(CHARACTERS_C))

    @unittest.skip('No example available')
    def test_aeon_location_sheets(self):
        copyfile(NORMAL_AEON, TEST_AEON)
        aeon3obsidian_.main(TEST_AEON, '_location_sheets')
        if UPDATE:
            copyfile(LOCATIONS, TEST_LOCATIONS)
        self.assertEqual(read_file(LOCATIONS), read_file(TEST_LOCATIONS))

    @unittest.skip('No example available')
    def test_csv_location_sheets(self):
        copyfile(NORMAL_CSV, TEST_CSV)
        aeon3obsidian_.main(TEST_CSV, '_location_sheets')
        if UPDATE:
            copyfile(LOCATIONS, TEST_LOCATIONS)
        self.assertEqual(read_file(LOCATIONS), read_file(TEST_LOCATIONS))

    def test_aeon_report(self):
        copyfile(NORMAL_AEON, TEST_AEON)
        aeon3obsidian_.main(TEST_AEON, '_report')
        if UPDATE:
            copyfile(TEST_REPORT, REPORT_A)
        self.assertEqual(read_file(TEST_REPORT), read_file(REPORT_A))

    def test_csv_report(self):
        copyfile(NORMAL_CSV, TEST_CSV)
        aeon3obsidian_.main(TEST_CSV, '_report')
        if UPDATE:
            copyfile(TEST_REPORT, REPORT_C)
        self.assertEqual(read_file(TEST_REPORT), read_file(REPORT_C))

    def tearDown(self):
        remove_all_testfiles()


def main():
    unittest.main()


if __name__ == '__main__':
    main()
