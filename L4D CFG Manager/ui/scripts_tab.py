from tkinter import ttk


class ScriptsTab(ttk.Frame):

    def __init__(self, notebook):
        super().__init__(notebook)

        ttk.Label(self, text="Script Generator Coming Soon").pack(pady=20)