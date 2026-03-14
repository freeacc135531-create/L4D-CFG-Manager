import os
import json
from datetime import datetime


class ProfileService:

    def __init__(self):

        self.profile_dir = "profiles"
        self.backup_dir = os.path.join(self.profile_dir, "backups")

        os.makedirs(self.profile_dir, exist_ok=True)
        os.makedirs(self.backup_dir, exist_ok=True)

        self.ensure_default_profile()


    def ensure_default_profile(self):

        if not self.list_profiles():

            self.create_profile("Default", {})


    def list_profiles(self):

        profiles = []

        for file in os.listdir(self.profile_dir):

            if file.endswith(".json"):
                profiles.append(file.replace(".json", ""))

        return sorted(profiles)


    def sanitize_name(self, name):

        invalid = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']

        for char in invalid:
            name = name.replace(char, "")

        return name.strip()


    def create_profile(self, name, data):

        name = self.sanitize_name(name)

        profile = {
            "meta": {
                "name": name,
                "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "version": "0.5"
            },
            "config": data
        }

        path = os.path.join(self.profile_dir, f"{name}.json")

        with open(path, "w", encoding="utf-8") as f:
            json.dump(profile, f, indent=4)


    def save_profile(self, name, data):

        name = self.sanitize_name(name)

        path = os.path.join(self.profile_dir, f"{name}.json")

        if os.path.exists(path):

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            backup_path = os.path.join(
                self.backup_dir,
                f"{name}_{timestamp}.json"
            )

            try:
                with open(path, "r", encoding="utf-8") as f:
                    old_data = json.load(f)

                with open(backup_path, "w", encoding="utf-8") as f:
                    json.dump(old_data, f, indent=4)

            except:
                pass

        profile = {
            "meta": {
                "name": name,
                "updated": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "version": "0.5"
            },
            "config": data
        }

        with open(path, "w", encoding="utf-8") as f:
            json.dump(profile, f, indent=4)


    def load_profile(self, name):

        path = os.path.join(self.profile_dir, f"{name}.json")

        if not os.path.exists(path):
            return {}

        try:

            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)

            if "config" in data:
                return data["config"]

            return data

        except:

            return {}


    def delete_profile(self, name):

        path = os.path.join(self.profile_dir, f"{name}.json")

        if os.path.exists(path):
            os.remove(path)


    def duplicate_profile(self, name):

        data = self.load_profile(name)

        new_name = f"{name}_copy"

        self.create_profile(new_name, data)

        return new_name