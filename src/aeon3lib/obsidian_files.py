"""Provide a base class for Markdown export from Aeon Timeline 3.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/aeon3obsidian
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os
import re


class ObsidianFiles:

    def __init__(self, folderPath):
        """Set the Obsidian folder."""
        self.folderPath = folderPath
        self.data = None

    def write(self):
        """Create a set of Markdown files in the Obsidian folder.
        
        Return a success message.
        """
        os.makedirs(self.folderPath, exist_ok=True)
        for uid in self.data.items:
            item = self.data.items[uid]
            title = self._sanitize_title(item.label)
            text = self._build_content(item)
            self._write_file(f'{self.folderPath}/{title}.md', text)
        # self._build_index()
        # self._build_narrative()
        return 'Obsidian files successfully written.'

    def _build_content(self, item):
        """Return a string with the Markdown file content.
        
        Positional arguments:
            item: dictionary of Aeon item properties.
        """
        lines = []
        if item.shortLabel:
            lines.append(item.shortLabel)
        if item.summary:
            lines.append(self._to_markdown(item.summary))
        if item.properties:
            propertyStr = ''
            for reference , customProperty in item.properties:
                propertyStr = f'{propertyStr}- **{reference}** : {self._to_markdown(customProperty)}\n'
            lines.append(propertyStr)
        if item.tags:
            tagStr = ''
            for tag in item.tags:
                tagStr = f'{tagStr} #{self._sanitize_tag(tag)}'
            lines.append(tagStr)
        if item.date:
            lines.append(item.date)
        if item.time:
            lines.append(item.time)
        if item.duration:
            lines.append(item.duration)
        if item.relationships:
            relationshipStr = ''
            for target, reference in item.relationships:
                relationshipStr = f'{relationshipStr}- **{reference}** : [[{self._sanitize_title(target)}]]\n'
            lines.append(relationshipStr)
        if item.children:
            childrenStr = ''
            for child, reference in item.children:
                childrenStr = f'{childrenStr}- **{reference}** : [[{self._sanitize_title(child)}]]\n'
            lines.append(childrenStr)
        return '\n\n'.join(lines)

    def _build_index(self):
        """Create index pages."""
        mainIndexlines = []
        for uid in self.itemIndex:
            itemType = f'_{self._sanitize_title(self.labels[uid])}'
            mainIndexlines.append(f'- [[{itemType}]]')
            itemUidList = self.itemIndex[uid]

            # Create an index file with the items of the type.
            lines = []
            for itemUid in itemUidList:
                itemLabel = self._sanitize_title(self.labels[itemUid])
                lines.append(f'- [[{itemLabel}]]')
            text = '\n'.join(lines)
            self._write_file(f'{self.folderPath}/{itemType}.md', text)

        # Create a main index file with the types.
        text = '\n'.join(mainIndexlines)
        self._write_file(f'{self.folderPath}/__index.md', text)

    def _build_narrative(self):
        """Create a page with the narrative tree."""

        def get_branch(root, level):
            level += 1
            uid = root['id']
            if uid in self.labels:
                link = self._sanitize_title(self.labels[uid])
                lines.append(f"{'#' * level} [[{link}]]")
            for branch in root['children']:
                get_branch(branch, level)

        lines = []
        get_branch(self.narrative, 1)
        text = '\n\n'.join(lines)
        self._write_file(f'{self.folderPath}/__narrative.md', text)

    def _sanitize_tag(self, tag):
        # Return tag with non-alphanumeric characters replaced.
        return re.sub(r'\W+', '_', tag)

    def _sanitize_title(self, title):
        # Return title with disallowed characters removed.
        return re.sub(r'[\\|\/|\:|\*|\?|\"|\<|\>|\|]+', '', title)

    def _to_markdown(self, text):
        return text.replace('\n', '\n\n')

    def _write_file(self, filePath, text):
        """Write a single file and create a backup copy, if applicable.
        
        Positional arguments:
            filePath: str -- Path of the file to write.
            text: str -- File content.
        """
        backedUp = False
        if os.path.isfile(filePath):
            try:
                os.replace(filePath, f'{filePath}.bak')
                backedUp = True
            except Exception as ex:
                raise Exception(f'Error: Cannot overwrite "{os.path.normpath(filePath)}": {str(ex)}.')

        try:
            with open(filePath, 'w', encoding='utf-8') as f:
                f.write(text)
        except Exception as ex:
            if backedUp:
                os.replace(f'{filePath}.bak', self.filePath)
            raise Exception(f'Error: Cannot write "{os.path.normpath(filePath)}": {str(ex)}.')

        return f'"{os.path.normpath(filePath)}" written.'

