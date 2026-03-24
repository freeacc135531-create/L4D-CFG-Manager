import tkinter as tk
from tkinter import ttk
import json
import os

class GlowTab(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.vars = {}

        self.build_ui()

    def load_commands(self):
        path = os.path.join("data", "glow_commands.json")
        with open(path, "r") as f:
            return json.load(f)

    def build_ui(self):
        commands = self.load_commands()

        canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)

        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for category, cmds in commands.items():
            label = ttk.Label(scrollable_frame, text=f"=== {category} ===")
            label.pack(anchor="w", padx=5, pady=5)

            for cmd in cmds:
                frame = ttk.Frame(scrollable_frame)
                frame.pack(fill="x", padx=5, pady=2)

                ttk.Label(frame, text=cmd, width=35).pack(side="left")

                var = tk.StringVar()
                entry = ttk.Entry(frame, textvariable=var, width=10)
                entry.pack(side="left")

                var.trace_add("write", self.update_autoexec)

                self.vars[cmd] = var

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)

    def build_lines(self):
        lines = ["// === GLOW SETTINGS ==="]

        for cmd, var in self.vars.items():
            value = var.get().strip()
            if value:
                lines.append(f'{cmd} "{value}"')

        return lines

    def update_autoexec(self, *args):
        lines = self.build_lines()
        self.app.autoexec_tab.set_external_commands(lines)