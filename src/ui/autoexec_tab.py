import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os

from core.profile_service import ProfileService
from core.presets import PRESETS
from core.cfg_analyzer import parse_cfg
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
"cl_drawhud": "Enable HUD",
"cl_showfps": "Display FPS counter",
"hud_fastswitch": "Fast weapon switching",
"cl_autohelp": "Enable help tips",
"cl_timeout": "Server timeout value",
"net_maxroutable": "Max packet size",
"cl_predict": "Client prediction",
"cl_predictweapons": "Weapon prediction",
"cl_lagcompensation": "Enables lag compensation for the player",
"sv_region": "0 =  US East, 1 = US West, 2 = South America, 3 = Europe, 4 = Asia, 5 = Australia, 6 = Middle East, 7 = Africa",
"voice_vox": "Enables voice activation (VOX)",
"voice_threshold": "Sets the microphone activation threshold level",
"voice_forcerecord": "Forces voice recording",
"voice_modenable": "Allows voice communication between player",
"voice_enable": "Enables or disables voice chat",
"joystick": "Enables or disables joystick input",
"sv_pausable": "Allows the server to be paused",
"sv_consistency": "Ensures client files match the server’s files",
"cl_crosshair_red": "Sets the red color component of the crosshair",
"cl_crosshair_green": "Sets the green color component of the crosshair",
"cl_crosshair_blue": "Sets the blue color component of the crosshair",
"cl_colorblind": "Enables colorblind mode adjustments",
"cl_crosshair_thickness": "Controls the thickness of the crosshair lines",
"cl_crosshair_dynamic": "Enables dynamic crosshair that expands when moving or shooting",
"cl_crosshair_alpha": "Sets the transparency of the crosshair",
"crosshair": "Enables or disables the crosshair",
"c_thirdpersonshoulder": "Enables third-person shoulder camera view",
"cl_viewmodel_fovsurvivor": "Sets the field of view for the viewmodel (weapon model)",
"fov_desired": "Sets the player's desired field of view",
"m_customaccel": "Enables custom mouse acceleration settings",
"m_mouseaccel1": "First parameter controlling mouse acceleration",
"m_mouseaccel2": "Second parameter controlling mouse acceleration",
"m_mousespeed": "Sets Windows mouse acceleration usage",
"snd_legacy_surround": "Enables legacy surround sound processing.",
"cl_showpos": "Displays player position and velocity on screen",
"cc_lang": "Sets the language for closed captions",
"cc_linger_time": "Duration captions remain visible",
"cc_predisplay_time": "Time captions appear before the sound event",
"gameinstructor_enable": "Enables the in-game tutorial instructor system",
"net_graph": "Displays network performance statistics",
"net_graphpos": "Sets the screen position of the net_graph display",
"net_graphheight": "Adjusts vertical offset of the net_graph",
"net_graphproportionalfont": "Uses proportional fonts in net_graph display",
"con_enable": "Allows the developer console",
"net_allow_multicast": "Allows multicast network packets",
"snd_musicvolume": "Volume level for in-game music"
}


DROPDOWNS = {
"mat_queue_mode": ["-1", "0", "1", "2"],
"cl_forcepreload": ["0", "1"],
"m_rawinput": ["0", "1"],
"m_filter": ["0", "1"],
"cl_drawhud": ["0", "1"],
"cl_showfps": ["0", "1"],
"hud_fastswitch": ["0", "1"],
"cl_autohelp": ["0", "1"],
"cl_predict": ["0", "1"],
"cl_predictweapons": ["0", "1"],
"cl_lagcompensation": ["0", "1"],
"net_graph": ["0", "1", "2", "3", "4"],
"net_graphpos": ["0", "1", "2", "3"],
"net_graphproportionalfont": ["0", "1"],
"voice_enable": ["0", "1"],
"voice_modenable": ["0", "1"],
"sv_region": ["0", "1", "2", "3", "4", "5", "6", "7"],
"cc_lang": ["english", "french", "german", "spanish", "italian", "japanese", "korean", "russian"],
"cl_colorblind": ["0", "1", "2"],
"sv_consistency": ["0", "1"],
"crosshair": ["0", "1"],
"cl_predict": ["0", "1"],
"cl_predictweapons": ["0", "1"],
"cl_lagcompensation": ["0", "1"],
"cl_crosshair_dynamic": ["0", "1"],
"joystick": ["0", "1"],
"voice_vox": ["0", "1"],
"m_customaccel": ["0", "1", "2", "3"],
"snd_legacy_surround": ["0", "1"],
"cl_showpos": ["0", "1"],
"gameinstructor_enable": ["0", "1"],
"con_enable": ["0", "1"],
"net_allow_multicast": ["0", "1"],
"sv_pausable": ["0", "1"]
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


        container = ttk.Frame(self)
        container.pack(fill="both", expand=True)

        canvas = tk.Canvas(container)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)

        self.scroll_frame = ttk.Frame(canvas)

        self.scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")


        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))


        config_frame = ttk.Frame(self.scroll_frame)
        config_frame.pack(fill="both", expand=True, padx=10, pady=5)


        left_frame = ttk.Frame(config_frame)
        left_frame.pack(side="left", fill="both", expand=True, padx=10)

        right_frame = ttk.Frame(config_frame)
        right_frame.pack(side="left", fill="both", expand=True, padx=10)


        left_keys = [
            "rate",
            "cl_cmdrate",
            "cl_updaterate",
            "cl_interp",
            "cl_interp_ratio",
            "cl_timeout",
            "net_maxroutable",
            "cl_predict",
            "cl_predictweapons",
            "cl_lagcompensation",
            "fps_max",
            "mat_queue_mode",
            "fov_desired",
            "cl_viewmodelfovsurvivor",
            "c_thirdpersonshoulder",
            "crosshair",
            "cl_crosshair_alpha",
            "cl_crosshair_dynamic",
            "cl_crosshair_thickness",
            "cl_colorblind",
            "cl_crosshair_blue",
            "cl_crosshair_green",
            "cl_crosshair_red",
            "sv_consistency",
            "sv_pausable",
            "cl_forcepreload",
            "joystick",
            "voice_enable",
            "voice_modenable",
            "voice_forcerecord",
            "voice_threshold",
            "voice_vox"
        ]


        right_keys = [
            "cl_forcepreload",
            "m_customaccel",
            "m_mouseaccel1",
            "m_mouseaccel2",
            "m_mousespeed",
            "m_rawinput",
            "m_filter",
            "sensitivity",
            "snd_mixahead",
            "volume",
            "snd_musicvolume",
            "snd_legacy_surround",
            "cl_drawhud",
            "cl_showfps",
            "hud_fastswitch",
            "cl_autohelp",
            "cl_showpos",
            "cl_autohelp",
            "cl_showhelp",
            "cc_lang",
            "cc_linger_time",
            "cc_predisplay_time",
            "gameinstructor_enable",
            "net_graph",
            "net_graphpos",
            "net_graphheight",
            "net_graphproportionalfont",
            "sv_region",
            "cl_lagcompensation",
            "cl_timeout",
            "con_enable",
            "net_allow_multicast"
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

            self.preview.insert(tk.END, key, "cmd")
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

                if line.startswith("wait") or " wait " in f" {line} ":
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