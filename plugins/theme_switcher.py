import tkinter as tk
from tkinter import ttk
from core.plugin_system import BasePlugin


class ThemeSwitcherTab:

    def __init__(self, parent, app):
        self.app = app
        self.frame = ttk.Frame(parent)
        self._build_ui()

    def _build_ui(self):

        title = ttk.Label(
            self.frame,
            text="Theme Switcher",
            font=("Arial", 18)
        )
        title.pack(pady=20)

        theme_frame = ttk.Frame(self.frame)
        theme_frame.pack(pady=10)

        ttk.Label(theme_frame, text="Select Theme").pack(side="left", padx=10)

        self.theme_var = tk.StringVar()

        self.theme_select = ttk.Combobox(
            theme_frame,
            textvariable=self.theme_var,
            values=[
                "Light",
                "Dark",
                "Source",
                "Matrix"
            ],
            state="readonly",
            width=20
        )

        self.theme_select.pack(side="left", padx=10)

        ttk.Button(
            self.frame,
            text="Apply Theme",
            command=self.apply_theme
        ).pack(pady=10)

    def apply_theme(self):

        theme = self.theme_var.get()

        style = ttk.Style()

        if theme == "Light":

            style.configure("TFrame", background="#f0f0f0")
            style.configure("TLabel", background="#f0f0f0", foreground="#000000")
            style.configure("TButton", background="#ffffff", foreground="#000000")

        elif theme == "Dark":

            style.configure("TFrame", background="#1e1e1e")
            style.configure("TLabel", background="#1e1e1e", foreground="#ffffff")
            style.configure("TButton", background="#2b2b2b", foreground="#ffffff")

        elif theme == "Source":

            style.configure("TFrame", background="#2b2b2b")
            style.configure("TLabel", background="#2b2b2b", foreground="#ff6600")
            style.configure("TButton", background="#3a3a3a", foreground="#ff6600")

        elif theme == "Matrix":

            style.configure("TFrame", background="#000000")
            style.configure("TLabel", background="#000000", foreground="#00ff00")
            style.configure("TButton", background="#111111", foreground="#00ff00")


class Plugin(BasePlugin):

    name = "Theme Switcher"
    version = "1.0"
    author = "paradox32000"

    def on_load(self, app):

        tab = ThemeSwitcherTab(app.tabControl, app)
        app.tabControl.add(tab.frame, text="Themes")