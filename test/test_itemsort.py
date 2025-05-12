"""Unit test for the Aeon3Data.sort_items_by_date() method.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/aeon3obsidian
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import unittest

from aeon3lib.aeon3_data import Aeon3Data
from aeon3lib.aeon3_item import Aeon3Item


class TestItemsort(unittest.TestCase):

    def setUp(self):
        self.data = Aeon3Data()
        self.data.items = {
            'item5': Aeon3Item(
                'item 5',
                'EV1',
                'defaultEvent',
                era=None,
                timestamp=None,
                ),
            'item0': Aeon3Item(
                'item 0',
                'EV2',
                'defaultEvent',
                era=(1, 'AD', 'AD'),
                timestamp=100,
                ),
            'item1': Aeon3Item(
                'item 1',
                'EV3',
                'defaultEvent',
                era=(0, 'BC', 'BC'),
                timestamp=101,
                ),
            'item2': Aeon3Item(
                'item 2',
                'EV4',
                'defaultEvent',
                era=(1, 'AD', 'AD'),
                timestamp=99,
                ),
            'item3': Aeon3Item(
                'item 3',
                'EV5',
                'defaultEvent',
                era=(0, 'BC', 'BC'),
                timestamp=96,
                ),
            'item4': Aeon3Item(
                'item 4',
                'EV6',
                'defaultEvent',
                era=(1, 'AD', 'AD'),
                timestamp=98,
                ),
        }

    def test_sort_items_by_date(self):
        testList = ['item5', 'item0', 'item1', 'item2', 'item3', 'item4', 'item6']
        self.assertEqual(
            self.data.sort_items_by_date(testList),
            ['item3', 'item1', 'item4', 'item2', 'item0', 'item5']
            )


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
