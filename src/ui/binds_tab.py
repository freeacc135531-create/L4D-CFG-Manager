import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import json
from core.profile_service import ProfileService


with open("data/commands.json", encoding="utf-8") as f:
    CMD_DATA = json.load(f)
    
with open("data/key_names.json", encoding="utf-8") as f:
    KEY_NAMES = json.load(f)
    
ALL_KEYS = []
    
for group in KEY_NAMES.values():
    ALL_KEYS.extend(group)


class BindsTab(ttk.Frame):
    
    def show_key_dictionary(self):

        win = tk.Toplevel(self)
        win.title("Key Names Dictionary")
        win.geometry("400x400")

        text = tk.Text(win)
        text.pack(fill="both", expand=True)

        for category, keys in KEY_NAMES.items():

            text.insert("end", f"{category.upper()}\n")
            text.insert("end", "-"*30 + "\n")

            for k in keys:
                text.insert("end", f"{k}\n")

            text.insert("end", "\n")

        text.insert("end", f"{category.upper()}\n")
        text.insert("end", "-"*30 + "\n")

        for k in keys:
            text.insert("end", f"{k}\n")

        text.insert("end", "\n")

    def __init__(self, notebook):
        super().__init__(notebook)

        self.loaded_config_path = None
        self.existing_lines = []

        self.profile_service = ProfileService()
        self.create_ui()

    def create_ui(self):
        ttk.Label(self, text="Bind Creator").pack(pady=10)

        ttk.Button(self, text="Load Existing config.cfg",
                   command=self.load_config).pack(pady=5)

        form = ttk.Frame(self)
        form.pack(pady=5)

        self.key_var = tk.StringVar()

        ttk.Combobox(
            form,
            textvariable=self.key_var,
            values=ALL_KEYS,
            width=12
        ).pack(side="left", padx=5)

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

        ttk.Button(
            form,
            text="Key Dictionary",
            command=self.show_key_dictionary
        ).pack(side="left", padx=5)
        
        profile_frame = ttk.Frame(self)
        profile_frame.pack(pady=5)

        ttk.Label(profile_frame, text="Profile:").pack(side="left")

        self.profile_var = tk.StringVar()

        self.profile_dropdown = ttk.Combobox(
            profile_frame,
            textvariable=self.profile_var,
            values=self.profile_service.list_profiles(),
            width=20
        )
        self.profile_dropdown.pack(side="left", padx=5)
        self.profile_dropdown.bind("<<ComboboxSelected>>", self.load_profile)

        ttk.Button(profile_frame, text="New", command=self.create_profile).pack(side="left")
        ttk.Button(profile_frame, text="Save", command=self.save_profile).pack(side="left")
        ttk.Button(profile_frame, text="Delete", command=self.delete_profile).pack(side="left")
        
    def save_profile(self):
        name = self.profile_var.get()

        if not name:
            messagebox.showerror("Error", "No profile selected")
            return

        binds = []

        for item in self.tree.get_children():
            key, cmd = self.tree.item(item)["values"]
            binds.append({"key": key, "command": cmd})

        data = {"binds": binds}

        self.profile_service.save_profile(name, data)

        messagebox.showinfo("Saved", "Profile saved")
        
    def load_profile(self, event=None):
        name = self.profile_var.get()
        data = self.profile_service.load_profile(name)

        self.tree.delete(*self.tree.get_children())

        binds = data.get("binds", [])

        for b in binds:
            self.tree.insert("", "end", values=(b["key"], b["command"]))

        self.update_preview()
        
    def create_profile(self):
        name = tk.simpledialog.askstring("New Profile", "Profile name:")

        if name:
            self.profile_service.create_profile(name, {"binds": []})
            self.profile_dropdown["values"] = self.profile_service.list_profiles()
            
    def delete_profile(self):
        name = self.profile_var.get()

        if name:
            self.profile_service.delete_profile(name)
            self.profile_dropdown["values"] = self.profile_service.list_profiles()

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