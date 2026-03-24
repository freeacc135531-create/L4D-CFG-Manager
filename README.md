# L4D CFG Manager

A powerful and modern configuration manager for Left 4 Dead.

## Description

L4D CFG Manager is a Python-based tool designed to help players manage, edit and optimize their Left 4 Dead configuration files.

This project is currently in beta.

## Features

*Autoexec editor*

* 64 predefined commands
* Scripts generator
* Glows customizer
* Import and export autoexec
* Presets
* Autoexec preview

*Binds editor*

* 45 commands to bind on any key
* Predefined keys
* Import and export config

*Others*

* Plugin system
* Profile system
* CFG analyzer
* CFG stats
* Theme

core/ – Core logic and services

ui/ – User interface components

data/ – Command definitions and tooltips

## Plugins

You can install additional plugins by dropping .py files inside the /plugins folder.

## Requirements

- Python 3.10+

## How to Run

```bash
python main.py
```

## Requirements to Compile

```bash
pip install pyinstaller
```

## How to Compile

Move logo.ico and main.spec in the src folder then write this command in cmd
```bash
pyinstaller main.spec
```
