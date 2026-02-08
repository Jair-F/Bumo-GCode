import os

import yaml
from box import Box


def load_config(filename="./config.yaml") -> Box | None:
    try:
        # Use yaml.safe_load for security when loading from untrusted sources
        config = Box.from_yaml(filename=filename, Loader=yaml.SafeLoader)
        return config
    except yaml.YAMLError as e:
        print(f"Error reading YAML file: {e}")
        return None


class ConfigManager:
    def __init__(self):
        self._readConfig()
        self.startup_shortcut_name = "BumoAutostart.lnk"
        self.user_home = os.getenv("userprofile")
        self.auto_start_dir = os.path.join(
            self.user_home,
            r"AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup",
        )
        self.gcode_dir = os.path.join(self.user_home, r"Desktop\GCode")
        self.icon_file_name = r"data\splash.png"
        self.target_dir = "C:\\ankommen"
        self.speed_s = 2

    def _readConfig(self):
        # global CONFIG, TUNNEL_COMMANDS
        # with open("./config.yaml", encoding="utf-8") as file:
        #     CONFIG = box.Box(yaml.safe_load(file))
        # print("config read")
        # update_global_var()
        pass
