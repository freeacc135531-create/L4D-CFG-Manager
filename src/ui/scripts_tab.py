from tkinter import ttk
import tkinter as tk
import json



class ScriptsTab(ttk.Frame):

    def __init__(self, notebook, app=None):
        super().__init__(notebook)

        self.app = app
        with open("data/scripts.json", "r", encoding="utf-8") as f:
            self.scripts = json.load(f)

        self.build_ui()


    def build_ui(self):

        container = ttk.Frame(self)
        container.pack(fill="both", expand=True, padx=10, pady=10)


        left = ttk.Frame(container)
        left.pack(side="left", fill="y")


        ttk.Label(left, text="Scripts Library").pack(anchor="w")


        self.script_list = tk.Listbox(left, height=15, width=30)
        self.script_list.pack(fill="y", expand=True)

        for script in self.scripts.keys():
            self.script_list.insert(tk.END, script)


        self.script_list.bind("<<ListboxSelect>>", self.show_script)


        right = ttk.Frame(container)
        right.pack(side="left", fill="both", expand=True, padx=10)


        ttk.Label(right, text="Script Preview").pack(anchor="w")


        self.preview = tk.Text(right, height=20)
        self.preview.pack(fill="both", expand=True)


        button_frame = ttk.Frame(right)
        button_frame.pack(fill="x", pady=5)


        ttk.Button(
            button_frame,
            text="Copy Script",
            command=self.copy_script
        ).pack(side="left")


        ttk.Button(
            button_frame,
            text="Insert into Autoexec",
            command=self.insert_autoexec
        ).pack(side="right")


    def show_script(self, event=None):

        selection = self.script_list.curselection()

        if not selection:
            return

        name = self.script_list.get(selection[0])

        script = self.scripts.get(name, "")

        self.preview.delete("1.0", tk.END)
        self.preview.insert(tk.END, script.strip())


    def copy_script(self):

        script = self.preview.get("1.0", tk.END)

        if not script.strip():
            return

        self.clipboard_clear()
        self.clipboard_append(script)


    def insert_autoexec(self):

        script = self.preview.get("1.0", tk.END)

        if not script.strip():
            return

        try:

            notebook = self.app.tabControl

            for tab_id in notebook.tabs():

                tab = notebook.nametowidget(tab_id)

                if hasattr(tab, "preview"):

                    tab.preview.insert(tk.END, "\n")
                    tab.preview.insert(tk.END, script)

                    notebook.select(tab_id)
                    return

        except Exception as e:
            print("Insert error:", e)