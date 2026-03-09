import tkinter as tk
from tkinter import ttk

from ui.autoexec_tab import AutoexecTab
from ui.binds_tab import BindsTab
from ui.scripts_tab import ScriptsTab


class L4DConfigApp:
    def __init__(self, root):
        self.root = root
        self.root.title("L4D CFG Manager")
        self.root.geometry("900x700")

        self.tabControl = ttk.Notebook(self.root)
        self.tabControl.pack(expand=1, fill="both")

        self._init_tabs()

    def _init_tabs(self):
        self.autoexec_tab = AutoexecTab(self.tabControl)
        self.tabControl.add(self.autoexec_tab, text="Autoexec")

        self.binds_tab = BindsTab(self.tabControl)
        self.tabControl.add(self.binds_tab, text="Binds")

        self.scripts_tab = ScriptsTab(self.tabControl)
        self.tabControl.add(self.scripts_tab, text="Scripts")