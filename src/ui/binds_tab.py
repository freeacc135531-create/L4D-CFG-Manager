import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from data.commands import CMD_DATA
import os


class BindsTab(ttk.Frame):

    def __init__(self, notebook):
        super().__init__(notebook)

        self.loaded_config_path = None
        self.existing_lines = []

        self.create_ui()

    def create_ui(self):
        ttk.Label(self, text="Bind Creator").pack(pady=10)

        ttk.Button(self, text="Load Existing config.cfg",
                   command=self.load_config).pack(pady=5)

        form = ttk.Frame(self)
        form.pack(pady=5)

        self.key_var = tk.StringVar()

        ttk.Entry(form, textvariable=self.key_var, width=10).pack(side="left", padx=5)

        self.category = ttk.Combobox(form, values=list(CMD_DATA.keys()))
        self.category.pack(side="left", padx=5)
        self.category.bind("<<ComboboxSelected>>", self.update_commands)

        self.command_list = ttk.Combobox(form)
        self.command_list.pack(side="left", padx=5)

        ttk.Button(form, text="Add",
                   command=self.add_bind).pack(side="left", padx=5)

        self.tree = ttk.Treeview(self, columns=("key", "cmd"), show="headings")
        self.tree.heading("key", text="Key")
        self.tree.heading("cmd", text="Command")
        self.tree.pack(expand=True, fill="both", pady=10)

        ttk.Button(self, text="Remove Selected",
                   command=self.remove_selected).pack(pady=5)

        ttk.Label(self, text="Preview").pack()
        self.preview = tk.Text(self, height=8)
        self.preview.pack(fill="both", expand=True)

        ttk.Button(self, text="Save / Update config.cfg",
                   command=self.save_config).pack(pady=5)


    def load_config(self):
        path = filedialog.askopenfilename(filetypes=[("CFG files", "*.cfg")])
        if not path:
            return

        self.loaded_config_path = path

        with open(path, "r", encoding="utf-8") as f:
            self.existing_lines = f.readlines()

        messagebox.showinfo("Loaded", f"Loaded: {os.path.basename(path)}")

        self.update_preview()


    def update_commands(self, event=None):
        category = self.category.get()
        commands = CMD_DATA.get(category, [])
        self.command_list["values"] = [cmd for cmd, desc in commands]

    def add_bind(self):
        key = self.key_var.get()
        cmd = self.command_list.get()
        if key and cmd:
            self.tree.insert("", "end", values=(key, cmd))
            self.update_preview()

    def remove_selected(self):
        for item in self.tree.selection():
            self.tree.delete(item)
        self.update_preview()

    def update_preview(self):
        self.preview.delete("1.0", tk.END)

        existing = []
        new_keys = set()

        for item in self.tree.get_children():
            key, _ = self.tree.item(item)["values"]
            new_keys.add(str(key).lower())

        for line in self.existing_lines:
            stripped = line.strip()
            if stripped.startswith("bind "):
                parts = stripped.split('"')
                if len(parts) >= 2 and parts[1].lower() in new_keys:
                    continue
            existing.append(line)

        for line in existing:
            self.preview.insert(tk.END, line)

        for item in self.tree.get_children():
            key, cmd = self.tree.item(item)["values"]
            self.preview.insert(tk.END, f'bind "{key}" "{cmd}"\n')


    def save_config(self):
        if self.loaded_config_path:
            path = self.loaded_config_path
        else:
            path = filedialog.asksaveasfilename(defaultextension=".cfg")

        if not path:
            return

        with open(path, "w", encoding="utf-8") as f:
            f.write(self.preview.get("1.0", tk.END))

        messagebox.showinfo("Success", "Config updated successfully!")