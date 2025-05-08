"""Provide a class for the AT3 data model.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/aeon3obsidian
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""


class Aeon3Data:

    def __init__(self):
        self.items = {}
        self.itemIndex = {}
        self.narrative = {}

    def sort_items_by_date(self, itemList):
        """Return a list of item UIDs, sorted by date including the era.
        
        Positional arguments:
            itemList -- List of item UIDs.
        
        UIDs of undated items are placed last in original order.
        Invalid UIDs are discarded.
        """
        datedItems = []
        undatedItems = []
        for uid in itemList:
            try:
                if self.items[uid].timestamp is not None:
                    datedItems.append(uid)
                else:
                    undatedItems.append(uid)
            except KeyError:
                continue

        datedItems.sort(key=lambda e: (self.items[e].era, self.items[e].timestamp))
        return datedItems + undatedItems

