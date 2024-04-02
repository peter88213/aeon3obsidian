"""Provide a factory class for a yWriter object to write.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
from pywriter.pywriter_globals import ERROR
from pywriter.converter.file_factory import FileFactory


class ImportTargetFactory(FileFactory):
    """A factory class that instantiates a yWriter object to write.

    Public methods:
        make_file_objects(self, sourcePath, **kwargs) -- return conversion objects.
    """

    def make_file_objects(self, sourcePath, **kwargs):
        """Instantiate a target object for conversion to a yWriter project.

        Positional arguments:
            sourcePath -- str: path to the source file to convert.

        Optional arguments:
            suffix -- str: an indicator for the source file type.

        Required keyword arguments: 
            suffix -- str: target file name suffix.

        Return a tuple with three elements:
        - A message beginning with the ERROR constant in case of error
        - sourceFile: None
        - targetFile: a YwFile subclass instance, or None in case of error
        """
        fileName, __ = os.path.splitext(sourcePath)
        sourceSuffix = kwargs['suffix']
        if sourceSuffix:
            ywPathBasis = fileName.split(sourceSuffix)[0]
        else:
            ywPathBasis = fileName

        # Look for an existing yWriter project to rewrite.
        for fileClass in self._fileClasses:
            if os.path.isfile(f'{ywPathBasis}{fileClass.EXTENSION}'):
                targetFile = fileClass(f'{ywPathBasis}{fileClass.EXTENSION}', **kwargs)
                return 'Target object created.', None, targetFile
            
        return f'{ERROR}No yWriter project to write.', None, None
