import tkinter as tk
from tkinter import ttk, messagebox

from ui.autoexec_tab import AutoexecTab
from ui.binds_tab import BindsTab
from ui.scripts_tab import ScriptsTab
from ui.console_tab import ConsoleTab
from ui.glow_tab import GlowTab
from core.theme_manager import ThemeManager

from core.plugin_system import PluginManager


class L4DConfigApp:

    def __init__(self, root):

        self.root = root
        self.root.title("L4D CFG Manager")
        self.root.geometry("900x700")
        self.theme_manager = ThemeManager(root)

        self._init_menu()

        self.tabControl = ttk.Notebook(self.root)
        self.tabControl.pack(expand=1, fill="both")

        self._init_tabs()

        self.plugin_manager = PluginManager(self)
        self.plugin_manager.load_plugins()

    def _init_menu(self):

        menubar = tk.Menu(self.root)

        help_menu = tk.Menu(menubar, tearoff=0)

        help_menu.add_command(label="About", command=self.show_about)
        help_menu.add_command(label="Plugin Development", command=self.show_plugins_help)
        help_menu.add_command(
            label="Toggle Theme",
            command=self.theme_manager.toggle
        )

        menubar.add_cascade(label="Help", menu=help_menu)

        self.root.config(menu=menubar)

    def show_about(self):

        message = (
            "L4D CFG Manager 0.8\n\n"
            "Created by: paradox32000\n\n"
            "with the help of: WarHeRo\n\n"
            "L4D CFG Manager is a configuration tool designed to help players\n"
            "manage autoexec.cfg, config.cfg and scripts for Left 4 Dead.\n\n"
            "The application also supports a plugin system allowing the\n"
            "community to extend the tool with new tabs, script libraries\n"
            "and utilities."
        )

        messagebox.showinfo("About", message)

    def show_plugins_help(self):

        message = (
            "L4D CFG Manager Plugin System\n\n"
            "This application supports external plugins written in Python.\n\n"
            "Plugins allow you to extend the functionality of the CFG Manager\n"
            "by adding new tabs, tools or script libraries.\n\n"
            "PLUGIN INSTALLATION\n\n"
            "Place your plugin Python file inside the 'plugins' folder\n"
            "located next to the application.\n\n"
            "Example structure:\n\n"
            "L4D CFG Manager/\n"
            "    main.exe\n"
            "    plugins/\n"
            "        my_plugin.py\n\n"
            "PLUGIN STRUCTURE\n\n"
            "Every plugin must contain a class named 'Plugin'\n"
            "that inherits from BasePlugin.\n\n"
            "Example:\n\n"
            "from core.plugin_system import BasePlugin\n\n"
            "class Plugin(BasePlugin):\n"
            "    name = \"Example Plugin\"\n"
            "    version = \"1.0\"\n"
            "    author = \"Your Name\"\n\n"
            "    def on_load(self, app):\n"
            "        print(\"Plugin loaded\")\n\n"
            "The name and version fields help identify the plugin\n"
            "when it is loaded by the application.\n\n"
            "All plugins inside the plugins folder are automatically\n"
            "loaded when the application starts."
        )

        messagebox.showinfo("Plugin Development", message)

    def _init_tabs(self):

        self.autoexec_tab = AutoexecTab(self.tabControl)
        self.tabControl.add(self.autoexec_tab, text="Autoexec")
        
        self.scripts_tab = ScriptsTab(self.tabControl, self)
        self.tabControl.add(self.scripts_tab, text="Scripts")
        
        self.glow_tab = GlowTab(self.tabControl, self)
        self.tabControl.add(self.glow_tab, text="Glow")

        self.binds_tab = BindsTab(self.tabControl)
        self.tabControl.add(self.binds_tab, text="Binds")
        
        self.console_tab = ConsoleTab(self.tabControl)
        self.tabControl.add(self.console_tab, text="Console")