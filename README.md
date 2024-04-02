# The aeon3obsidian Python script: Convert Aeon Timeline 3 project data to Markdown

For more information, see the [project homepage](https://peter88213.github.io/aeon3obsidian) with description and download instructions.

## Development

*aeon3obsidian* is organized as an Eclipse PyDev project. The official release branch on GitHub is *main*.

## Important

Please note that this script has not yet been extensively tested. To me, it's actually just a proof of concept. I probably won't develop the script further. Feel free to copy the project and modify it to your own liking.

### Conventions

See https://github.com/peter88213/PyWriter/blob/main/docs/conventions.md

Exceptions:
- No localization is required.
- The directory structure is modified to minimize dependencies:

```
.
└── aeon3obsidian/
    ├── src/
    │   ├── pywriter/
    │   ├── aeon3ywlib/
    │   └── aeon3obsidianlib/
    ├── test/
    └── tools/ 
        ├── build_aeon3obsidian.py
        ├── build.xml
        └── inliner.py
```

### Development tools

- [Python](https://python.org) version 3.10.
- [Eclipse IDE](https://eclipse.org) with [PyDev](https://pydev.org) and EGit.
- Apache Ant is used for building the application.

## License

*aeon3obsidian* is distributed under the [MIT License](http://www.opensource.org/licenses/mit-license.php).
