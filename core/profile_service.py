import os
import json


class ProfileService:

    def __init__(self):
        self.profile_dir = "profiles"
        os.makedirs(self.profile_dir, exist_ok=True)

    def list_profiles(self):
        profiles = []

        for file in os.listdir(self.profile_dir):
            if file.endswith(".json"):
                profiles.append(file.replace(".json", ""))

        return profiles

    def create_profile(self, name, data):
        path = os.path.join(self.profile_dir, f"{name}.json")

        with open(path, "w") as f:
            json.dump(data, f, indent=4)

    def save_profile(self, name, data):
        path = os.path.join(self.profile_dir, f"{name}.json")

        with open(path, "w") as f:
            json.dump(data, f, indent=4)

    def load_profile(self, name):
        path = os.path.join(self.profile_dir, f"{name}.json")

        if not os.path.exists(path):
            return {}

        with open(path, "r") as f:
            return json.load(f)

    def delete_profile(self, name):
        path = os.path.join(self.profile_dir, f"{name}.json")

        if os.path.exists(path):
            os.remove(path)