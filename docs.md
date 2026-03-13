# L4D CFG Manager Plugin System

## This application supports external plugins written in Python.

**Plugins allow you to extend the functionality of the CFG Manager by adding:**
- new tabs
- tools
- script libraries
- analyzers
- custom features

PLUGIN INSTALLATION

1. Go to the "plugins" folder located next to the application.
2. Place your plugin Python file directly inside the folder.

Example structure:

L4D CFG Manager/
    main.exe
    plugins/
        my_plugin.py
        script_library.py

No subfolder is required.


PLUGIN STRUCTURE

Every plugin must contain a class named "Plugin" that inherits from BasePlugin.

Example:

from core.plugin_system import BasePlugin

class Plugin(BasePlugin):

    name = "Example Plugin"
    version = "1.0"
    author = "Your Name"

    def on_load(self, app):
        print("Example plugin loaded")


## REQUIRED ELEMENTS

The plugin class must contain:

class Plugin(BasePlugin)

Optional metadata:

*name*
*version*
*author*

Example:

name = "Script Library"
version = "1.0"
author = "Community"


ON_LOAD FUNCTION

The on_load() function is executed when the plugin is loaded.

You receive the main application instance:

def on_load(self, app):

You can use it to:
- add new tabs
- access the UI
- add tools


EXAMPLE ADDING A TAB

def on_load(self, app):

    import tkinter as tk
    from tkinter import ttk

    frame = ttk.Frame(app.notebook)

    label = ttk.Label(frame, text="Hello from plugin")
    label.pack()

    app.notebook.add(frame, text="My Plugin Tab")


## PLUGIN LOADING

When the application starts, the plugin system automatically loads every .py file inside the plugins folder.

Loaded plugins will appear in the console:

[PLUGIN LOADED] Script Library v1.0


PLUGIN ERROR HANDLING

If a plugin fails to load, an error will appear:

[PLUGIN ERROR]

**All plugins are welcome even if it is not perfect or does not work well.**
