"""Provide helper functions for Aeon Timeline 3 file operation.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/aeon3yw
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import codecs
from pywriter.pywriter_globals import ERROR


def scan_file(filePath):
    """Read and scan the project file.
    
    Positional arguments:
        filePath -- str: Path to the Aeon 3 project file.
    
    Return a string containing either the JSON part or an error message.
    """
    try:
        with open(filePath, 'rb') as f:
            binInput = f.read()
    except(FileNotFoundError):
        return f'{ERROR}"{os.path.normpath(filePath)}" not found.'

    except:
        return f'{ERROR}Cannot read "{os.path.normpath(filePath)}".'
    
    # JSON part: all characters between the first and last curly bracket.
    chrData = []
    opening = ord('{')
    closing = ord('}')
    level = 0
    for c in binInput:
        if c == opening:
            level += 1
        if level > 0:
            chrData.append(c)
            if c == closing:
                level -= 1
                if level == 0:
                    break

    if level != 0:
        return f'{ERROR}Corrupted data.'

    try:
        jsonStr = codecs.decode(bytes(chrData), encoding='utf-8')
    except:
        return f'{ERROR}Cannot decode "{os.path.normpath(filePath)}".'

    return jsonStr
