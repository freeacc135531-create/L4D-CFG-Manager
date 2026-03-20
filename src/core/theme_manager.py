import tkinter as tk
from tkinter import ttk

class ThemeManager:

    def __init__(self, root):
        self.root = root
        self.dark = False
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.apply_light()

    def apply_dark(self):
        self.style.theme_use("clam")

        self.style.configure(".", background="#2b2b2b", foreground="white")
        self.style.configure("TFrame", background="#2b2b2b")
        self.style.configure("TLabel", background="#2b2b2b", foreground="white")
        self.style.configure("TButton", background="#3c3f41", foreground="white")
        self.style.configure("TEntry", fieldbackground="#3c3f41", foreground="white")
        self.style.configure("TCombobox", fieldbackground="#3c3f41", foreground="white")

        self.root.configure(bg="#2b2b2b")

        for widget in self.root.winfo_children():
            self._apply_dark_recursive(widget)

    def _apply_dark_recursive(self, widget):
        if isinstance(widget, tk.Text):
            widget.configure(bg="#2b2b2b", fg="white", insertbackground="white")
        elif isinstance(widget, tk.Canvas):
            widget.configure(bg="#2b2b2b")

        for child in widget.winfo_children():
            self._apply_dark_recursive(child)

    def apply_light(self):
        self.style.theme_use("default")

        self.style.configure(".", background="#f0f0f0", foreground="black")
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TLabel", background="#f0f0f0", foreground="black")
        self.style.configure("TButton", background="#e0e0e0", foreground="black")
        self.style.configure("TEntry", fieldbackground="white", foreground="black")
        self.style.configure("TCombobox", fieldbackground="white", foreground="black")

        self.root.configure(bg="#f0f0f0")

        for widget in self.root.winfo_children():
            self._apply_light_recursive(widget)

    def _apply_light_recursive(self, widget):
        if isinstance(widget, tk.Text):
            widget.configure(bg="white", fg="black", insertbackground="black")
        elif isinstance(widget, tk.Canvas):
            widget.configure(bg="#f0f0f0")

        for child in widget.winfo_children():
            self._apply_light_recursive(child)

    def toggle(self):
        self.dark = not self.dark
        if self.dark:
            self.apply_dark()
        else:
            self.apply_light()