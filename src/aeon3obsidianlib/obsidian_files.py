"""Provide a base class for Markdown export from Aeon Timeline 3.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/aeon3obsidian
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os


class ObsidianFiles:
    FORBIDDEN_CHARACTERS = ('\\', '/', ':', '*', '?', '"', '<', '>', '|')
    # set of characters that filenames cannot contain

    def __init__(self, folderPath):
        """Set the Obsidian folder."""
        self.folderPath = folderPath
        self.dataModel = {}
        self.labelLookup = {}

    def _build_content(self, item):
        """Return a string with the Markdown file content.
        
        Positional arguments:
            item: dictionary of Aeon item properties.
        """
        lines = []
        for itemProperty in item:
            if item[itemProperty]:
                lines.append(item[itemProperty])
        return '\n\n'.join(lines)

    def write(self):
        """Create a set of Markdown files in the Obsidian folder.
        
        Return a success message.
        """
        os.makedirs(self.folderPath, exist_ok=True)
        for uid in self.dataModel:
            title = self._strip_title(self.labelLookup[uid])
            text = self._build_content(self.dataModel[uid])
            self._write_file(f'{self.folderPath}/{title}.md', text)
        return 'Obsidian files successfully written.'

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

    def _strip_title(self, title):
        """Return title with characters removed that must not appear in a file name."""
        for c in self.FORBIDDEN_CHARACTERS:
            title = title.replace(c, '')
        return title

