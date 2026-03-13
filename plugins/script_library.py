from core.plugin_system import BasePlugin
import tkinter as tk
from tkinter import ttk


SCRIPTS = {

"Scoreboard Netgraph": '''//Netgraph on tab
alias +scoregraph "+showscores; net_graph 4"
alias -scoregraph "-showscores; net_graph 0"
bind TAB +scoregraph
''',

"flashlight Spam": '''//Flashlight spam script
alias "+21" "alias 23 +22; +22"
alias "+22" "impulse 100; wait; -22"
alias "-22" "impulse 100; wait; 23"
alias "23" "+22"

alias "-21" "alias 23 impulse 100;"

alias "+31" "impulse 100; -21"
alias "-31" "32"

alias "32" "alias -31 +21; wait 20; alias -31 32"

bind MWHEELUP +31
'''
}


class Plugin(BasePlugin):

    name = "Script Library"
    version = "1.0"
    author = "paradox32000"

    def on_load(self, app):

        self.app = app

        self.frame = ttk.Frame(app.tabControl)
        app.tabControl.add(self.frame, text="Script Library")

        self.build_ui()

    def build_ui(self):

        container = ttk.Frame(self.frame)
        container.pack(fill="both", expand=True, padx=10, pady=10)

        left = ttk.Frame(container)
        left.pack(side="left", fill="y")

        right = ttk.Frame(container)
        right.pack(side="left", fill="both", expand=True, padx=10)

        ttk.Label(left, text="Scripts").pack(anchor="w")

        self.script_list = tk.Listbox(left, width=30, exportselection=False)
        self.script_list.pack(fill="y", expand=True)

        for name in SCRIPTS.keys():
            self.script_list.insert(tk.END, name)

        self.script_list.bind("<<ListboxSelect>>", self.show_script)

        ttk.Label(right, text="Script").pack(anchor="w")

        self.script_text = tk.Text(right)
        self.script_text.pack(fill="both", expand=True)

        buttons = ttk.Frame(right)
        buttons.pack(fill="x", pady=5)

        ttk.Button(buttons, text="Copy Script", command=self.copy_script).pack(side="left")
        ttk.Button(buttons, text="Insert in Autoexec", command=self.insert_autoexec).pack(side="left", padx=5)

        self.script_list.selection_set(0)
        self.show_script(None)

    def show_script(self, event):

        selection = self.script_list.curselection()

        if not selection:
            return

        name = self.script_list.get(selection[0])
        script = SCRIPTS[name]

        self.script_text.delete("1.0", tk.END)
        self.script_text.insert(tk.END, script)

    def copy_script(self):

        script = self.script_text.get("1.0", tk.END)

        self.frame.clipboard_clear()
        self.frame.clipboard_append(script)

    def insert_autoexec(self):

        script = self.script_text.get("1.0", tk.END)

        if hasattr(self.app, "autoexec_tab"):
            preview = self.app.autoexec_tab.preview
            preview.insert(tk.END, "\n" + script + "\n")