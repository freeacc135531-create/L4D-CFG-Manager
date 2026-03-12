import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os

from core.profile_service import ProfileService
from core.presets import PRESETS
from core.cfg_analyzer import parse_cfg, compare_configs
from core.cfg_stats import get_cfg_stats


TOOLTIPS = {
"rate": "Network bandwidth limit\nRecommended: 30000 - 100000",
"cl_cmdrate": "Number of command packets sent per second",
"cl_updaterate": "Updates received per second from server",
"cl_interp": "Interpolation delay",
"cl_interp_ratio": "Interpolation ratio multiplier",
"fps_max": "Maximum FPS limit",
"mat_queue_mode": "Multithreading mode",
"cl_forcepreload": "Preload game assets",
"m_rawinput": "Raw mouse input",
"m_filter": "Mouse smoothing",
"sensitivity": "Mouse sensitivity",
"snd_mixahead": "Sound buffer delay",
"volume": "Game volume",
"cl_drawhud": "Enable HUD"
}

DROPDOWNS = {
"mat_queue_mode": ["-1", "0", "1", "2"],
"cl_forcepreload": ["0", "1"],
"m_rawinput": ["0", "1"],
"m_filter": ["0", "1"],
"cl_drawhud": ["0", "1"]
}


class ToolTip:

    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip = None
        widget.bind("<Enter>", self.show)
        widget.bind("<Leave>", self.hide)

    def show(self, event=None):

        if self.tip:
            return

        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + 20

        self.tip = tk.Toplevel(self.widget)
        self.tip.wm_overrideredirect(True)
        self.tip.wm_geometry(f"+{x}+{y}")

        label = tk.Label(
            self.tip,
            text=self.text,
            background="#ffffe0",
            relief="solid",
            borderwidth=1,
            justify="left"
        )

        label.pack()

    def hide(self, event=None):

        if self.tip:
            self.tip.destroy()
            self.tip = None


class AutoexecTab(ttk.Frame):

    def __init__(self, parent):

        super().__init__(parent)

        self.profile_service = ProfileService()
        self.entries = {}

        self.build_ui()
        self.load_initial_profile()

    def build_ui(self):

        profile_frame = ttk.Frame(self)
        profile_frame.pack(fill="x", pady=5, padx=5)

        ttk.Label(profile_frame, text="Profile:").pack(side="left")

        self.profile_var = tk.StringVar()

        self.profile_dropdown = ttk.Combobox(
            profile_frame,
            textvariable=self.profile_var,
            values=self.profile_service.list_profiles(),
            width=25
        )

        self.profile_dropdown.pack(side="left", padx=5)
        self.profile_dropdown.bind("<<ComboboxSelected>>", self.switch_profile)

        ttk.Button(profile_frame, text="New", command=self.create_profile).pack(side="left")
        ttk.Button(profile_frame, text="Delete", command=self.delete_profile).pack(side="left")

        preset_frame = ttk.Frame(self)
        preset_frame.pack(fill="x", pady=5, padx=5)

        ttk.Label(preset_frame, text="Preset:").pack(side="left")

        self.preset_var = tk.StringVar()

        preset_dropdown = ttk.Combobox(
            preset_frame,
            textvariable=self.preset_var,
            values=list(PRESETS.keys()),
            width=25
        )

        preset_dropdown.pack(side="left", padx=5)
        preset_dropdown.bind("<<ComboboxSelected>>", self.apply_preset)

        config_frame = ttk.Frame(self)
        config_frame.pack(fill="both", expand=True, padx=10, pady=5)

        left_frame = ttk.Frame(config_frame)
        left_frame.pack(side="left", fill="both", expand=True, padx=10)

        right_frame = ttk.Frame(config_frame)
        right_frame.pack(side="left", fill="both", expand=True, padx=10)

        left_keys = [
            "rate", "cl_cmdrate", "cl_updaterate",
            "cl_interp", "cl_interp_ratio",
            "fps_max", "mat_queue_mode"
        ]

        right_keys = [
            "cl_forcepreload",
            "m_rawinput", "m_filter", "sensitivity",
            "snd_mixahead", "volume",
            "cl_drawhud"
        ]

        for key in left_keys:
            self.create_entry(left_frame, key)

        for key in right_keys:
            self.create_entry(right_frame, key)

        ttk.Label(self, text="autoexec.cfg Preview:").pack(anchor="w", padx=10)

        self.preview = tk.Text(self, height=10)
        self.preview.pack(fill="both", expand=True, padx=10, pady=5)

        self.preview.tag_config("cmd", foreground="blue")
        self.preview.tag_config("value", foreground="green")
        self.preview.tag_config("alias", foreground="purple")
        self.preview.tag_config("bind", foreground="orange")
        self.preview.tag_config("wait", foreground="red")

        button_frame = ttk.Frame(self)
        button_frame.pack(fill="x", pady=5, padx=10)

        ttk.Button(button_frame, text="Save Profile", command=self.save_profile).pack(side="left")
        ttk.Button(button_frame, text="Analyze CFG", command=self.analyze_cfg).pack(side="left")
        ttk.Button(button_frame, text="CFG Stats", command=self.show_stats).pack(side="left")
        ttk.Button(button_frame, text="Import autoexec.cfg", command=self.import_autoexec).pack(side="left")

        ttk.Button(button_frame, text="Export autoexec.cfg", command=self.export_autoexec).pack(side="right")

    def create_entry(self, parent, key):

        row = ttk.Frame(parent)
        row.pack(fill="x", pady=3)

        label = ttk.Label(row, text=key, width=18, anchor="w")
        label.pack(side="left")

        ToolTip(label, TOOLTIPS.get(key, ""))

        var = tk.StringVar()

        if key in DROPDOWNS:
            entry = ttk.Combobox(row, textvariable=var, values=DROPDOWNS[key], width=12)
        else:
            entry = ttk.Entry(row, textvariable=var, width=14)

        entry.pack(side="left", fill="x", expand=True)

        var.trace_add("write", lambda *args: self.update_preview())

        self.entries[key] = var

    def update_preview(self):

        self.preview.delete("1.0", tk.END)

        for key, var in self.entries.items():

            value = var.get()

            if not value:
                continue

            if key == "alias":
                tag = "alias"
            elif key == "bind":
                tag = "bind"
            elif key == "wait":
                tag = "wait"
            else:
                tag = "cmd"

            self.preview.insert(tk.END, key, tag)
            self.preview.insert(tk.END, " ")
            self.preview.insert(tk.END, value, "value")
            self.preview.insert(tk.END, "\n")

    def create_profile(self):

        name = tk.simpledialog.askstring("New Profile", "Profile name:")

        if name:

            self.profile_service.create_profile(name, {})
            self.profile_dropdown["values"] = self.profile_service.list_profiles()

    def delete_profile(self):

        name = self.profile_var.get()

        if name:

            self.profile_service.delete_profile(name)
            self.profile_dropdown["values"] = self.profile_service.list_profiles()

    def switch_profile(self, event=None):

        name = self.profile_var.get()
        data = self.profile_service.load_profile(name)

        for key, var in self.entries.items():
            var.set(data.get(key, ""))

        self.update_preview()

    def save_profile(self):

        name = self.profile_var.get()

        if not name:
            messagebox.showerror("Error", "No profile selected")
            return

        data = {key: var.get() for key, var in self.entries.items()}

        self.profile_service.save_profile(name, data)

        messagebox.showinfo("Saved", "Profile saved successfully")

    def apply_preset(self, event=None):

        preset_name = self.preset_var.get()
        preset = PRESETS.get(preset_name, {})

        for key, value in preset.items():

            if key in self.entries:
                self.entries[key].set(value)

        self.update_preview()

    def analyze_cfg(self):

        path = filedialog.askopenfilename(filetypes=[("CFG files", "*.cfg")])

        if not path:
            return

        aliases = 0
        binds = 0
        waits = 0
        commands = 0

        with open(path, "r", encoding="utf-8") as f:

            for line in f:

                line = line.strip()

                if not line:
                    continue

                commands += 1

                if line.startswith("alias"):
                    aliases += 1

                if line.startswith("bind"):
                    binds += 1

                if "wait" in line:
                    waits += 1

        result = (
            f"Commands: {commands}\n"
            f"Aliases: {aliases}\n"
            f"Binds: {binds}\n"
            f"Wait usage: {waits}"
        )

        messagebox.showinfo("CFG Analysis", result)

    def show_stats(self):

        data = {}

        for key, var in self.entries.items():

            value = var.get()

            if value:
                data[key] = value

        stats = get_cfg_stats(data)

        message = (
            f"Total commands: {stats['total_commands']}\n"
            f"Network: {stats['network']}\n"
            f"Input: {stats['input']}\n"
            f"Audio: {stats['audio']}\n"
            f"Graphics: {stats['graphics']}\n"
            f"Other: {stats['other']}"
        )

        messagebox.showinfo("CFG Statistics", message)

    def import_autoexec(self):

        path = filedialog.askopenfilename(
            title="Import autoexec.cfg",
            filetypes=[("CFG files", "*.cfg")]
        )

        if not path:
            return

        data = parse_cfg(path)

        for key, var in self.entries.items():

            if key in data:
                var.set(data[key])

        self.update_preview()

        messagebox.showinfo("Import", "autoexec.cfg imported successfully")

    def export_autoexec(self):

        path = filedialog.asksaveasfilename(
            defaultextension=".cfg",
            filetypes=[("CFG files", "*.cfg")],
            initialfile="autoexec.cfg"
        )

        if not path:
            return

        content = self.preview.get("1.0", tk.END)

        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

        messagebox.showinfo("Exported", "autoexec.cfg exported successfully")

    def load_initial_profile(self):

        profiles = self.profile_service.list_profiles()

        if profiles:

            self.profile_var.set(profiles[0])
            self.switch_profile()