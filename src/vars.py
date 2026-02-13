import os
import sys

import yaml  # pylint: disable=import-error
from box import Box  # pylint: disable=import-error


def load_config(filename: str = './config.yaml') -> Box | None:
    try:
        # Use yaml.safe_load for security when loading from untrusted sources
        config = Box.from_yaml(filename=filename, Loader=yaml.SafeLoader)
        return config
    except yaml.YAMLError as e:
        print(f'Error reading YAML file: {e}')
    return None


class Vars:
    def __init__(self) -> None:
        self._read_config()
        self.startup_shortcut_name = 'BumoAutostart.lnk'
        self.user_home = os.getenv('userprofile')
        self.auto_start_dir = os.path.join(
            self.user_home,
            r'AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup',
        )
        self.gcode_dir = os.path.join(self.user_home, r'Desktop\GCode')
        self.icon_file_name = r'data\splash.png'
        self.target_dir = 'C:\\ankommen'
        self.speed_s = 2

    def get_exe_path(self) -> str:
        application_path = 'unknown'
        if self.running_as_exe():
            application_path = os.path.dirname(sys.executable)
        elif __file__:
            application_path = os.path.dirname(__file__)
        return application_path

    def running_as_exe(self) -> bool:
        return getattr(sys, 'frozen', False)

    def get_data_file_path(self, relative_path: str) -> str:
        bundle_dir = None
        if self.running_as_exe():
            bundle_dir = sys._MEIPASS  # pylint: disable=protected-access
        else:
            bundle_dir = os.path.dirname(os.path.abspath(__file__))

        return os.path.join(bundle_dir, relative_path)

    def _read_config(self) -> None:
        # global CONFIG, TUNNEL_COMMANDS
        # with open("./config.yaml", encoding="utf-8") as file:
        #     CONFIG = box.Box(yaml.safe_load(file))
        # print("config read")
        # update_global_var()
        pass
