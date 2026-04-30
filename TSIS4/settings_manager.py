import json
import os

class SettingsManager:
    def __init__(self, filename="settings.json"):
        self.filename = filename
        self.default_settings = {
            "snake_color": [0, 255, 0],  # RGB
            "grid_overlay": True,
            "sound": True
        }
        self.settings = self.load_settings()
    
    def load_settings(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                return json.load(f)
        else:
            return self.default_settings.copy()
    
    def save_settings(self):
        with open(self.filename, 'w') as f:
            json.dump(self.settings, f, indent=4)
    
    def get(self, key):
        return self.settings.get(key, self.default_settings.get(key))
    
    def set(self, key, value):
        self.settings[key] = value
        self.save_settings()