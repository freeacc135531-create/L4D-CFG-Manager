from tkinter import ttk

class ThemeManager:

    def __init__(self, root):
        self.root = root
        self.dark = False
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.apply_light()

    def apply_dark(self):
        self.style.configure(".", background="#2b2b2b", foreground="white")
        self.style.configure("TEntry", fieldbackground="#3c3f41", foreground="white")
        self.style.configure("TFrame", background="#2b2b2b")
        self.root.configure(bg="#2b2b2b")

    def apply_light(self):
        self.style.theme_use("clam")
        self.root.configure(bg="#f0f0f0")

    def toggle(self):
        self.dark = not self.dark
        if self.dark:
            self.apply_dark()
        else:
            self.apply_light()