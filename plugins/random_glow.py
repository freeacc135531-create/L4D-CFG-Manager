import random
import tkinter as tk
from tkinter import ttk
from core.plugin_system import BasePlugin



class RandomGlowTab:

    def __init__(self, parent, app):
        self.app = app
        self.frame = ttk.Frame(parent)
        self.last_generated = ""
        self._build_ui()

    def _build_ui(self):

        title = ttk.Label(
            self.frame,
            text="Random Glow Generator",
            font=("Arial", 18)
        )
        title.pack(pady=20)

        self.text_area = tk.Text(self.frame, height=15, width=90)
        self.text_area.pack(pady=10)

        button_frame = ttk.Frame(self.frame)
        button_frame.pack(pady=10)

        ttk.Button(
            button_frame,
            text="Generate Random Glow",
            command=self.generate_glow
        ).pack(side="left", padx=10)

        ttk.Button(
            button_frame,
            text="Copy",
            command=self.copy_to_clipboard
        ).pack(side="left", padx=10)

        ttk.Button(
            button_frame,
            text="Add to autoexec",
            command=self.add_to_autoexec
        ).pack(side="left", padx=10)


    def random_color(self):
        return (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255)
        )

    def generate_glow(self):

        survivor = self.random_color()
        infected = self.random_color()
        items = self.random_color()

        glow_cfg = f"""// ===== Random Glow Generated =====

// Survivor Glow
cl_glow_survivor_r {survivor[0]}
cl_glow_survivor_g {survivor[1]}
cl_glow_survivor_b {survivor[2]}

// Infected Glow
cl_glow_infected_r {infected[0]}
cl_glow_infected_g {infected[1]}
cl_glow_infected_b {infected[2]}

// Item Glow
cl_glow_item_r {items[0]}
cl_glow_item_g {items[1]}
cl_glow_item_b {items[2]}

"""

        self.last_generated = glow_cfg

        self.text_area.delete("1.1", tk.END)
        self.text_area.insert(tk.END, glow_cfg)

    def copy_to_clipboard(self):
        content = self.text_area.get("1.1", tk.END)
        self.frame.clipboard_clear()
        self.frame.clipboard_append(content)

    def add_to_autoexec(self):
        if not self.last_generated:
            return

        if hasattr(self.app, "autoexec_tab"):
            text_widget = self.app.autoexec_tab.preview
            text_widget.insert(tk.END, "\n" + self.last_generated)



class Plugin(BasePlugin):
    name = "Random Glow Generator"
    version = "1.1"
    author = "paradox32000"

    def on_load(self, app):
        tab = RandomGlowTab(app.tabControl, app)
        app.tabControl.add(tab.frame, text="Random Glow")