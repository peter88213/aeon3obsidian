## Development

*aeon3obsidian* is organized as an Eclipse PyDev project. The official release branch on GitHub is *main*.

### Conventions

See https://github.com/peter88213/PyWriter/blob/main/docs/conventions.md

Exceptions:
- No localization is required.
- The directory structure is modified to minimize dependencies:

```
.
└── aeon3obsidian/
    ├── src/
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

