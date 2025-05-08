import unittest

from aeon3lib.aeon3_item import Aeon3Item
from aeon3lib.aeon3_data import Aeon3Data


class TestItemsort(unittest.TestCase):

    def setUp(self):
        self.data = Aeon3Data()
        self.data.items = {
            'item5': Aeon3Item(
                'item 5',
                era=None,
                timestamp=None,
                ),
            'item0': Aeon3Item(
                'item 0',
                era=(1, 'AD', 'AD'),
                timestamp=100,
                ),
            'item1': Aeon3Item(
                'item 1',
                era=(0, 'BC', 'BC'),
                timestamp=101,
                ),
            'item2': Aeon3Item(
                'item 2',
                era=(1, 'AD', 'AD'),
                timestamp=99,
                ),
            'item3': Aeon3Item(
                'item 3',
                era=(0, 'BC', 'BC'),
                timestamp=96,
                ),
            'item4': Aeon3Item(
                'item 4',
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
