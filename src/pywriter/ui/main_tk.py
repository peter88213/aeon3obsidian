#!/usr/bin/env python3
""""Provide a tkinter GUI class with main menu and main window.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from pywriter.pywriter_globals import ERROR
from pywriter.ui.ui import Ui


class MainTk(Ui):
    """A tkinter GUI root class.

    Public methods:
        start() -- start the Tk main loop.
        open_project(fileName, fileTypes=[('yWriter 7 project', '.yw7')]) 
            -- select a valid project file and display the path.
        ask_yes_no(text) -- query yes or no with a pop-up box.
        set_info_how(message) -- show how the converter is doing.

    Public instance variables: 
        kwargs -- keyword arguments buffer. 

    Main menu, title bar, main window frame, status bar, path bar.
    """

    def __init__(self, title, **kwargs):
        """Initialize the GUI window and instance variables.
        
        Positional arguments:
            title -- application title to be displayed at the window frame.
         
        Required keyword arguments:
            yw_last_open -- str: initial file.
        
        Operation:
        - Create a main menu to be extended by subclasses.
        - Create a title bar for the project title.
        - Open a main window frame to be used by subclasses.
        - Create a status bar to be used by subclasses.
        - Create a path bar for the project file path.
        
        Extends the superclass constructor.
        """
        super().__init__(title)
        self._statusText = ''
        self.kwargs = kwargs
        self._ywPrj = None
        self._root = tk.Tk()
        self._root.title(title)
        self._mainMenu = tk.Menu(self._root)
        self._fileMenu = tk.Menu(self._mainMenu, title='my title', tearoff=0)
        self._mainMenu.add_cascade(label='File', menu=self._fileMenu)
        self._fileMenu.add_command(label='Open...', command=lambda: self.open_project(''))
        self._fileMenu.add_command(label='Close', command=lambda: self._close_project())
        self._fileMenu.entryconfig('Close', state='disabled')
        self._fileMenu.add_command(label='Exit', command=self._root.quit)
        
        self._extend_menu()
        # Hook for subclasses
        
        self._root.config(menu=self._mainMenu) 
        self._titleBar = tk.Label(self._root, text='', padx=5, pady=2)
        self._titleBar.pack(expand=False, anchor='w')
        self._mainWindow = tk.Frame()
        self._mainWindow.pack(expand=True, fill='both')
        self._statusBar = tk.Label(self._root, text='', anchor='w', padx=5, pady=2)
        self._statusBar.pack(expand=False, fill='both')
        self._pathBar = tk.Label(self._root, text='', padx=5, pady=3)
        self._pathBar.pack(expand=False, anchor='w')

    def _extend_menu(self):
        """Create an object that represents the project file.
        
        This is a template method that can be overridden by subclasses. 
        """

    def _disable_menu(self):
        """Disable menu entries when no project is open.
        
        To be extended by subclasses.
        """
        self._fileMenu.entryconfig('Close', state='disabled')

    def _enable_menu(self):
        """Enable menu entries when a project is open.
        
        To be extended by subclasses.
        """
        self._fileMenu.entryconfig('Close', state='normal')

    def start(self):
        """Start the Tk main loop.
        
        Note: This can not be done in the constructor method.
        """
        self._root.mainloop()

    def open_project(self, fileName, fileTypes=[('yWriter 7 project', '.yw7')]):
        """Select a valid project file and display the path.

        Positional arguments:
            fileName -- str: project file path.
            
        Optional arguments:
            fileTypes -- list of tuples for file selection (display text, extension).

        Priority:
        1. use file name argument
        2. open file select dialog

        Return the file name.
        To be extended by subclasses.
        """
        self._set_status(self._statusText)
        initDir = os.path.dirname(self.kwargs['yw_last_open'])
        if not initDir:
            initDir = './'
        if not fileName or not os.path.isfile(fileName):
            fileName = filedialog.askopenfilename(filetypes=fileTypes, defaultextension='.yw7', initialdir=initDir)
        if fileName:
            self.kwargs['yw_last_open'] = fileName
            self._pathBar.config(text=os.path.normpath(fileName))
        return fileName

    def _close_project(self):
        """Close the yWriter project without saving and reset the user interface.
        
        To be extended by subclasses.
        """
        self._ywPrj = None
        self._titleBar.config(text='')
        self._set_status('')
        self._pathBar.config(text='')
        self._disable_menu()

    def ask_yes_no(self, text):
        """Query yes or no with a pop-up box.
        
        Positional arguments:
            text -- question to be asked in the pop-up box. 
            
        Overrides the superclass method.       
        """
        return messagebox.askyesno('WARNING', text)

    def set_info_how(self, message):
        """Show how the converter is doing.
        
        Positional arguments:
            message -- message to be displayed. 
            
        Display the message at the status bar.
        Overrides the superclass method.
        """
        if message.startswith(ERROR):
            self._statusBar.config(bg='red')
            self._statusBar.config(fg='white')
            self.infoHowText = message.split(ERROR, maxsplit=1)[1].strip()
        else:
            self._statusBar.config(bg='green')
            self._statusBar.config(fg='white')
            self.infoHowText = message
        self._statusBar.config(text=self.infoHowText)

    def _set_status(self, message):
        """Put text on the status bar."""
        self._statusText = message
        self._statusBar.config(bg=self._root.cget('background'))
        self._statusBar.config(fg='black')
        self._statusBar.config(text=message)
