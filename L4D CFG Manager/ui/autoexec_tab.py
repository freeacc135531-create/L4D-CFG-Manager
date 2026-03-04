import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os

from core.profile_service import ProfileService
from core.presets import PRESETS
from core.cfg_analyzer import parse_cfg, compare_configs


class AutoexecTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.profile_service = ProfileService()
        self.entries = {}

        self.build_ui()
        self.load_initial_profile()

    def build_ui(self):

        profile_frame = ttk.Frame(self)
        profile_frame.pack(fill="x", pady=5)

        ttk.Label(profile_frame, text="Profile:").pack(side="left")

        self.profile_var = tk.StringVar()
        self.profile_dropdown = ttk.Combobox(
            profile_frame,
            textvariable=self.profile_var,
            values=self.profile_service.list_profiles()
        )
        self.profile_dropdown.pack(side="left", padx=5)
        self.profile_dropdown.bind("<<ComboboxSelected>>", self.switch_profile)

        ttk.Button(profile_frame, text="New", command=self.create_profile).pack(side="left")
        ttk.Button(profile_frame, text="Delete", command=self.delete_profile).pack(side="left")

        preset_frame = ttk.Frame(self)
        preset_frame.pack(fill="x", pady=5)

        ttk.Label(preset_frame, text="Preset:").pack(side="left")

        self.preset_var = tk.StringVar()
        preset_dropdown = ttk.Combobox(
            preset_frame,
            textvariable=self.preset_var,
            values=list(PRESETS.keys())
        )
        preset_dropdown.pack(side="left", padx=5)
        preset_dropdown.bind("<<ComboboxSelected>>", self.apply_preset)

        config_frame = ttk.Frame(self)
        config_frame.pack(fill="both", expand=True)

        default_keys = [
            "rate", "cl_cmdrate", "cl_updaterate",
            "cl_interp", "cl_interp_ratio",
            "fps_max", "mat_queue_mode"
        ]

        for key in default_keys:
            row = ttk.Frame(config_frame)
            row.pack(fill="x", pady=2)

            ttk.Label(row, text=key, width=20).pack(side="left")
            var = tk.StringVar()
            entry = ttk.Entry(row, textvariable=var)
            entry.pack(side="left", fill="x", expand=True)

            var.trace_add("write", lambda *args: self.update_preview())
            self.entries[key] = var

        ttk.Label(self, text="autoexec.cfg Preview:").pack(anchor="w")
        self.preview = tk.Text(self, height=12)
        self.preview.pack(fill="both", expand=True, pady=5)

        button_frame = ttk.Frame(self)
        button_frame.pack(fill="x", pady=5)

        ttk.Button(button_frame, text="Save Profile", command=self.save_profile).pack(side="left")
        ttk.Button(button_frame, text="Analyze CFG", command=self.analyze_cfg).pack(side="left")

    def update_preview(self):
        text = ""
        for key, var in self.entries.items():
            value = var.get()
            if value:
                text += f"{key} {value}\n"

        self.preview.delete("1.0", tk.END)
        self.preview.insert(tk.END, text)

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

        current = parse_cfg(path)
        preset_name = self.preset_var.get()
        reference = PRESETS.get(preset_name, {})

        issues = compare_configs(current, reference)

        if not issues:
            messagebox.showinfo("Analysis", "No issues found")
        else:
            messagebox.showwarning("Analysis", "\n".join(issues))

    def load_initial_profile(self):
        profiles = self.profile_service.list_profiles()
        if profiles:
            self.profile_var.set(profiles[0])
            self.switch_profile()