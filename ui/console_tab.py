import tkinter as tk
from tkinter import ttk

from core.logger import Logger


class ConsoleTab(ttk.Frame):

    def __init__(self, parent):

        super().__init__(parent)

        self.text = tk.Text(self, bg="#111", fg="#0f0")
        self.text.pack(fill="both", expand=True)

        Logger.attach_console(self.text)

        Logger.log("Console initialized")