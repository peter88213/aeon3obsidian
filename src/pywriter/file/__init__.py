"""Package for template-based document generation.

This is how the file generation from a yWriter project is generally done:
The write method runs through all chapters, scenes, and world building 
elements, such as characters, locations ans items, and fills templates. 

The package's README file contains a list of templates and placeholders:
https://github.com/peter88213/PyWriter/tree/main/src/pywriter/file#readme

Modules:

file_export.py -- Provide a generic class for template-based file export.
filter.py -- Provide a generic filter class for template-based file export.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
