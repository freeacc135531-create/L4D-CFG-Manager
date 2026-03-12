import os
import sys
import importlib.util
import traceback

from core.logger import Logger


class BasePlugin:
    name = "Unknown Plugin"
    version = "1.0"
    author = "Unknown"

    def on_load(self, app):
        """
        Called when plugin is loaded.
        Override this method.
        """
        pass


def get_base_path():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_plugins_path():
    return os.path.join(get_base_path(), "plugins")


class PluginManager:

    def __init__(self, app):
        self.app = app
        self.plugins = []
        self.plugins_path = get_plugins_path()

    def load_plugins(self):

        if not os.path.exists(self.plugins_path):
            os.makedirs(self.plugins_path)

        for item in os.listdir(self.plugins_path):

            item_path = os.path.join(self.plugins_path, item)

            try:

                if os.path.isfile(item_path) and item.endswith(".py"):
                    self._load_plugin(item_path)

                elif os.path.isdir(item_path):

                    plugin_file = os.path.join(item_path, "plugin.py")

                    if os.path.isfile(plugin_file):
                        self._load_plugin(plugin_file)

            except Exception:
                Logger.log(f"[PLUGIN ERROR] Failed loading {item}")
                traceback.print_exc()

    def _load_plugin(self, plugin_file):

        module_name = os.path.splitext(os.path.basename(plugin_file))[0]

        spec = importlib.util.spec_from_file_location(module_name, plugin_file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        if not hasattr(module, "Plugin"):
            Logger.log(f"[PLUGIN WARNING] {module_name} has no 'Plugin' class.")
            return

        plugin_instance = module.Plugin()

        if not isinstance(plugin_instance, BasePlugin):
            Logger.log(f"[PLUGIN WARNING] {module_name} Plugin must inherit BasePlugin.")
            return

        plugin_instance.on_load(self.app)

        self.plugins.append(plugin_instance)

        Logger.log(f"[PLUGIN LOADED] {plugin_instance.name} v{plugin_instance.version} by {plugin_instance.author}")