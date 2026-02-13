import os
import sys
from pathlib import Path
from typing import Any

import yaml  # pylint: disable=import-error


class Vars:
    def __init__(self, **kwargs: Any) -> None:
        # self.load_config()
        self.startup_shortcut_name = 'BumoAutostart.lnk'
        self.user_home = os.getenv('userprofile') or os.path.expanduser('~')
        self.auto_start_dir = os.path.join(
            self.user_home,
            r'AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup',
        )
        self.gcode_dir = os.path.join(
            self.user_home,
            r'Desktop\GCode',
        )
        self.icon_file_name = r'data\splash.png'
        self.target_dir = 'C:\\ankommen'
        self.speed_s = 2

        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

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
        base_path = None
        if self.running_as_exe():
            base_path = sys._MEIPASS  # type: ignore[attr-defined] # pylint: disable=protected-access
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))

        return os.path.join(base_path, relative_path)

    @classmethod
    def from_yaml(cls, filename: str = './config.yaml') -> 'Vars':
        path = Path(filename)
        if path.exists():
            try:
                with open(path, encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                if isinstance(data, dict):
                    return cls(**data)

            except Exception as e:  # pylint: disable=broad-exception-caught
                print(f'Error loading config, using defaults: {e}')

        return cls()
