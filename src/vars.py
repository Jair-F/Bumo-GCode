import os
import sys
from pathlib import Path
import time
from typing import Any

from src.notifier import Notifier
import yaml  # pylint: disable=import-error


class Vars:
    def __init__(self, **kwargs: Any) -> None:
        self._last_config_read_time = time.time()

        self.startup_shortcut_name = 'BumoAutostart.lnk'
        self.user_home = os.getenv('userprofile') or os.path.expanduser('~')
        self.auto_start_dir = os.path.join(
            self.user_home,
            r'AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup',
        )
        self.gcode_dir = './GCode_dir'
        self.icon_file_name = r'data\splash.png'
        self.target_dir = './target_dir'
        self.loop_speed_s = 2

        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def inject_notifier(self, notifier: Notifier) -> None:
        self._notifier = notifier

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

    def auto_reload_config(self, config_file:str = 'config.yaml'):
        config_last_mod_time = os.path.getmtime(config_file)
        if config_last_mod_time > self._last_config_read_time:
            new_vars = Vars.from_yaml(config_file)
            self.__dict__.update(new_vars.__dict__)
            self._last_config_read_time = time.time()

            self._notifier.show_notification("config hot-reloaded")
            print("config hot reloaded")
