The *aeon3obsidian* Python script extracts the items of an [Aeon Timeline 3](https://timeline.app/) 
project and generates a set of Markdown documents.

![Screenshot](Screenshots/screen01.png)

## Features

- Creates a page for each *aeon* item. 
- Creates links between the pages according to the relationships. 
- Inserts tags, if any. 
- Inserts date/time (Gregorian date, "A.D." only) for the event-based pages. 
- Inserts duration (as set in Aeon) for the event-based pages. 
- The `__index.md` file holds the table of contents on the top level. 
- The `__narrative.md` file holds the table of contents of the narrative. 

## Requirements

- [Python](https://www.python.org/) version 3.6+.

## Download and install {#download}

[Download the latest release (version 1.0.0)](https://raw.githubusercontent.com/peter88213/aeon3obsidian/main/dist/aeon3obsidian_v1.0.0.zip)

- Unpack the zipfile and copy *aeon3obsidian.py* whereever you want.

[Changelog](changelog)

## Usage

```
aeon3obsidian.py Sourcefile

positional arguments:
  Sourcefile  The path of the .aeon or .csv file.

```

You can also drag an *.aeon* file and drop it on the *aeon3obsidian.py* icon. 

The created Markdown files are placed in a subfolder, named after the *aeon* project.

## License

This extension is distributed under the [MIT
License](http://www.opensource.org/licenses/mit-license.php).

