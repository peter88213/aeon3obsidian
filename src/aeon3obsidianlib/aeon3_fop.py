"""Provide helper functions for Aeon Timeline 3 file operation.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/aeon3obsidian
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import codecs


def scan_file(filePath):
    """Read and scan the project file.
    
    Positional arguments:
        filePath -- str: Path to the Aeon 3 project file.
    
    Return a string containing the JSON part.
    """
    with open(filePath, 'rb') as f:
        binInput = f.read()

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
        raise ValueError('Error: Corrupted data.')

    jsonStr = codecs.decode(bytes(chrData), encoding='utf-8')
    if not jsonStr:
        raise ValueError('Error: No JSON part found.')

    return jsonStr
