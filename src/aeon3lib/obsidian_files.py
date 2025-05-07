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

        #--- Create one file per item.
        for uid in self.data.items:
            item = self.data.items[uid]
            title = self._sanitize_title(item.label)
            text = self._get_item_page_str(item)
            self._write_file(f'{self.folderPath}/{title}.md', text)

        self._create_index_page()
        self._create_narrative_page()
        return 'Obsidian files successfully written.'

    def _get_item_page_str(self, item):
        lines = ['\n']

        #--- Short label.
        if item.shortLabel:
            lines.append(item.shortLabel)

        #--- Tags in a row.
        if item.tags:
            tagStr = ''
            for tag in item.tags:
                tagStr = f'{tagStr} #{self._sanitize_tag(tag)}'
            lines.append(tagStr)

        #--- Summary between rulers.
        if item.summary:
            lines.append('---')
            lines.append(self._to_markdown(item.summary))
            lines.append('---')

        #--- Date and time in a row.
        dateTimeStr = ''
        dateStr = ''
        if item.date:
            dateStr = item.date
        if item.time:
            dateStr = f'{dateStr} {item.time}'
        if dateStr:
            dateTimeStr = f'- **When** : {dateStr}\n'

        #--- Duration.
        if item.duration:
            dateTimeStr = f'{dateTimeStr}- **Lasts** : {item.duration}'
        lines.append(dateTimeStr)

        #--- List of properties.
        if item.properties:
            propertyStr = ''
            for reference , customProperty in item.properties:
                propertyStr = f'{propertyStr}- **{reference}** : {self._to_markdown_list_element(customProperty)}\n'
            lines.append(propertyStr)

        #--- List of relationships.
        if item.relationships:
            relationshipStr = ''
            for target, reference in item.relationships:
                relationshipStr = f'{relationshipStr}- **{reference}** : [[{self._sanitize_title(target)}]]\n'
            lines.append(relationshipStr)

        #--- List of children.
        if item.children:
            childrenStr = ''
            for child in item.children:
                childrenStr = f'{childrenStr}- [[{self._sanitize_title(child)}]]\n'
            lines.append(childrenStr)

        return '\n\n'.join(lines)

    def _create_index_page(self):
        mainIndexlines = ['\n']
        for itemType in self.data.itemIndex:
            mainIndexlines.append(f'- [[_{itemType}]]')
            lines = []
            for itemLabel in self.data.itemIndex[itemType]:
                lines.append(f'- [[{itemLabel}]]')
            text = '\n'.join(lines)
            self._write_file(f'{self.folderPath}/_{itemType}.md', text)
        text = '\n'.join(mainIndexlines)
        self._write_file(f'{self.folderPath}/__Index.md', text)

    def _create_narrative_page(self):

        def get_branch(root, level):
            level += 1
            uid = root['id']
            if uid in self.labels:
                link = self._sanitize_title(self.labels[uid])
                lines.append(f"{'#' * level} [[{link}]]")
            for branch in root['children']:
                get_branch(branch, level)

        lines = []
        # get_branch(self.data.narrative, 1)
        text = '\n\n'.join(lines)
        self._write_file(f'{self.folderPath}/__Narrative.md', text)

    def _sanitize_tag(self, tag):
        # Return tag with non-alphanumeric characters replaced.
        return re.sub(r'\W+', '_', tag)

    def _sanitize_title(self, title):
        # Return title with disallowed characters removed.
        return re.sub(r'[\\|\/|\:|\*|\?|\"|\<|\>|\|]+', '', title)

    def _to_markdown(self, text):
        while '\n\n' in text:
            text = text.replace('\n\n', '\n')
        return text.replace('\n', '\n\n')

    def _to_markdown_list_element(self, text):
        while '\n\n' in text:
            text = text.replace('\n\n', '\n')
        return text.replace('\n', '\n  ')

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

