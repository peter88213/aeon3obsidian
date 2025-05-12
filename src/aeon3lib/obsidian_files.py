"""Provide a class for Markdown export from Aeon Timeline 3.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/aeon3obsidian
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os
import re


class ObsidianFiles:

    HIDDEN_ERAS = ('AD')

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
            title = self._sanitize_title(item.uniqueLabel)
            text = self._get_item_page_yaml(item)
            text = f'{text}{self._get_item_page_markdown(item)}'
            self._write_file(f'{self.folderPath}/{title}.md', text)

        self._create_index_page()
        self._create_narrative_page()
        return 'Obsidian files successfully written.'

    def _create_index_page(self):
        # Write a file containing of item links grouped by item types.
        mainIndexlines = ['\n']
        for typeUid in self.data.itemIndex:
            typeLabel = self.data.itemTypes[typeUid].label
            mainIndexlines.append(f'- [[_{typeLabel}]]')
            lines = []
            sortedItems = self.data.sort_items_by_date(self.data.itemIndex[typeUid])
            for itemUid in sortedItems:
                lines.append(f'- [[{self.data.items[itemUid].uniqueLabel}]]')
            text = '\n'.join(lines)
            self._write_file(f'{self.folderPath}/_{typeLabel}.md', text)
        text = '\n'.join(mainIndexlines)
        self._write_file(f'{self.folderPath}/__Index.md', text)

    def _create_narrative_page(self):

        def get_branch(branch, level):
            level += 1
            for uid in branch:
                if uid in self.data.items:
                    link = self._sanitize_title(self.data.items[uid].uniqueLabel)
                    typeUid = self.data.items[uid].typeUid
                    if self.data.itemTypes[typeUid].isNarrativeFolder:
                        linkPrefix = f"{'#' * level} "
                    else:
                        linkPrefix = ''
                    lines.append(f"{linkPrefix}[[{link}]]")
                get_branch(branch[uid], level)

        lines = []
        get_branch(self.data.narrative, 1)
        text = '\n\n'.join(lines)
        self._write_file(f'{self.folderPath}/__Narrative.md', text)

    def _get_date_str(self, item):
        # Return a formatted string with the date to display.
        dateStr = ''
        if item.weekdayName is not None:
            dateStr = f'{item.weekdayName}'
        if item.day is not None:
            dateStr = f'{dateStr} {item.day}'
        if item.monthName is not None:
            dateStr = f'{dateStr} {item.monthName}'
        if item.year is not None:
            dateStr = f'{dateStr} {item.year}'
        if item.eraShortName is not None:
            if item.eraShortName not in self.HIDDEN_ERAS:
                dateStr = f'{dateStr} {item.eraShortName}'
        return dateStr

    def _get_item_page_markdown(self, item):
        # Return the Markdown part of an item page as a single string.
        lines = ['\n']

        #--- Summary between rulers.
        if item.summary:
            lines.append('---')
            lines.append(self._to_markdown(item.summary))
            lines.append('---')

        #--- Date and time in a row.
        dateTimeStr = ''
        dateStr = self._get_date_str(item)
        if dateStr:
            dateTimeStr = f'- **When** : {dateStr} {self._get_time_str(item)}\n'

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

    def _get_item_page_yaml(self, item):
        # Return the YAML part of an item page as a single string.
        obsidianProperties = {}

        #--- Label.
        if item.label:
            obsidianProperties['label'] = f'{item.label}'

        #--- Short label as Alias.
        if item.shortLabel:
            obsidianProperties['aliases'] = f'\n  - {item.shortLabel}'

        #--- Type.
        obsidianProperties['type'] = f'{self.data.itemTypes[item.typeUid].label}'

        #--- Display ID.
        if item.displayId:
            obsidianProperties['ID'] = f'{item.displayId}'

        #--- Date and time in ISO format ("AD" era only).
        if item.isoDate:
            obsidianProperties['date'] = item.isoDate
            if item.isoTime:
                obsidianProperties['time'] = f'{item.isoDate}T{item.isoTime}'

        #--- List of tags.
        if item.tags:
            tags = []
            for tag in item.tags:
                tags.append(f'  - {self._sanitize_tag(tag)}')
            tagStr = '\n'.join(tags)
            obsidianProperties['tags'] = f'\n{tagStr}'

        if not obsidianProperties:
            return ''

        yamlLines = ['---']
        for propertyLabel in obsidianProperties:
            yamlLines.append(f'{propertyLabel}: {obsidianProperties[propertyLabel]}')
        yamlLines.append('---')
        return '\n'.join(yamlLines)

    def _get_time_str(self, item):
        # Return a formatted string with the time to display.
        timeStr = ''
        if item.hour is not None:
            timeStr = f'{item.hour}'
        if item.minute is not None:
            timeStr = f'{timeStr}:{item.minute:02}'
        if item.second:
            timeStr = f'{timeStr}:{item.second:02}'
        return timeStr

    def _sanitize_tag(self, tag):
        # Return tag with non-alphanumeric characters replaced.
        return re.sub(r'\W+', '_', tag)

    def _sanitize_title(self, title):
        # Return title with disallowed characters removed.
        return re.sub(r'[\\|\/|\:|\*|\?|\"|\<|\>|\|]+', '', title)

    def _to_markdown(self, text):
        # Return a string with double linebreaks.
        while '\n\n' in text:
            text = text.replace('\n\n', '\n')
        return text.replace('\n', '\n\n')

    def _to_markdown_list_element(self, text):
        # Return a string with single linebreaks and indented lines.
        while '\n\n' in text:
            text = text.replace('\n\n', '\n')
        return text.replace('\n', '\n  ')

    def _write_file(self, filePath, text):
        # Write text to a single file specified by filePath.
        # Create a backup copy, if applicable.
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

