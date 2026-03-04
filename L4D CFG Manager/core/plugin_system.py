import os
import sys
import importlib.util
import traceback



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

        for folder in os.listdir(self.plugins_path):
            plugin_dir = os.path.join(self.plugins_path, folder)

            if not os.path.isdir(plugin_dir):
                continue

            plugin_file = os.path.join(plugin_dir, "plugin.py")

            if not os.path.isfile(plugin_file):
                continue

            try:
                self._load_plugin(plugin_file)
            except Exception:
                print(f"[PLUGIN ERROR] Failed loading {folder}")
                traceback.print_exc()

    def _load_plugin(self, plugin_file):
        module_name = os.path.basename(os.path.dirname(plugin_file))

        spec = importlib.util.spec_from_file_location(module_name, plugin_file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        if not hasattr(module, "Plugin"):
            print(f"[PLUGIN WARNING] {module_name} has no 'Plugin' class.")
            return

        plugin_instance = module.Plugin()

        if not isinstance(plugin_instance, BasePlugin):
            print(f"[PLUGIN WARNING] {module_name} Plugin must inherit BasePlugin.")
            return

        plugin_instance.on_load(self.app)

        self.plugins.append(plugin_instance)

        print(f"[PLUGIN LOADED] {plugin_instance.name} v{plugin_instance.version} by {plugin_instance.author}")