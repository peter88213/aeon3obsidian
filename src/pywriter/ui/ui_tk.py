"""Provide a facade class for a Tkinter based GUI.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from tkinter import *
from tkinter import messagebox
from pywriter.pywriter_globals import ERROR
from pywriter.ui.ui import Ui


class UiTk(Ui):
    """UI subclass implementing a Tkinter facade.
    
    Public methods:
        ask_yes_no(text) -- query yes or no with a pop-up box.
        set_info_what(message) -- show what the converter is going to do.
        set_info_how(message) -- show how the converter is doing.
        start() -- start the Tk main loop.
    """

    def __init__(self, title):
        """Initialize the GUI window.
        
        Positional arguments:
            title -- application title to be displayed at the window frame.
            
        Extends the superclass constructor.
        """
        super().__init__(title)
        self._root = Tk()
        self._root.minsize(400, 150)
        self._root.resizable(width=FALSE, height=FALSE)
        self._root.title(title)
        self._appInfo = Label(self._root, text='')
        self._appInfo.pack(padx=20, pady=5)
        self._processInfo = Label(self._root, text='', padx=20)
        self._processInfo.pack(pady=20, fill='both')
        self._root.quitButton = Button(text="Quit", command=quit)
        self._root.quitButton.config(height=1, width=10)
        self._root.quitButton.pack(pady=10)

    def ask_yes_no(self, text):
        """Query yes or no with a pop-up box.
        
        Positional arguments:
            text -- question to be asked in the pop-up box. 
            
        Overrides the superclass method.       
        """
        return messagebox.askyesno('WARNING', text)

    def set_info_what(self, message):
        """Show what the converter is going to do.
        
        Positional arguments:
            message -- message to be displayed. 
            
        Display the message at the _appinfo label.
        Overrides the superclass method.
        """
        self.infoWhatText = message
        self._appInfo.config(text=message)

    def set_info_how(self, message):
        """Show how the converter is doing.
        
        Positional arguments:
            message -- message to be displayed. 
            
        Display the message at the _processinfo label.
        Overrides the superclass method.
        """
        if message.startswith(ERROR):
            self._processInfo.config(bg='red')
            self._processInfo.config(fg='white')
            self.infoHowText = message.split(ERROR, maxsplit=1)[1].strip()
        else:
            self._processInfo.config(bg='green')
            self._processInfo.config(fg='white')
            self.infoHowText = message
        self._processInfo.config(text=self.infoHowText)

    def start(self):
        """Start the Tk main loop."""
        self._root.mainloop()

    def _show_open_button(self, open_cmd):
        """Add an 'Open' button to the main window.
        
        Positional argument:
            open_cmd -- subclass method that opens the file.
        """
        self._root.openButton = Button(text="Open", command=open_cmd)
        self._root.openButton.config(height=1, width=10)
        self._root.openButton.pack(pady=10)
