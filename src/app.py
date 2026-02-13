import os
import sys
import time
from contextlib import suppress

import pyshortcuts
from src.tools import copy_file
from src.tools import i_am_the_owner
from src.tools import show_notification

from src.config import ConfigManager


class App:
    def __init__(self):
        self._config = ConfigManager()
        self._startup()
        self.already_transfered_files = {}

    def _create_target_dirs(self) -> None:
        try:
            os.mkdir(self._config.gcode_dir)
        except FileExistsError:
            " "

    def _auto_install_startup(self) -> bool:
        pyshortcuts.make_shortcut(
            script=self._get_exe_path(),
            name=self._config.startup_shortcut_name,
            folder=self._config.auto_start_dir,
            icon=self._config.icon_file_name,
            description=None,
        )
        print(f"Shortcut '{self._config.startup_shortcut_name}' created.")
        return True

    def _get_exe_path(self) -> str:
        application_path = "unknown"
        if self._running_as_exe():
            application_path = os.path.dirname(sys.executable)
        elif __file__:
            application_path = os.path.dirname(__file__)
        return application_path

    def _running_as_exe(self) -> bool:
        return getattr(sys, "frozen", False)

    def _get_files_and_mod_times(directory_path: str) -> dict[str, float]:
        files = {}
        for fn in os.listdir(directory_path):
            file_path = os.path.join(directory_path, fn)
            if os.path.isfile(file_path):
                try:
                    mod_time = os.path.getmtime(file_path)
                    files[fn] = mod_time
                except OSError as _:
                    pass
        return files

    def _startup(self):
        self._create_target_dirs()
        if self._running_as_exe():
            # self._auto_install_startup()
            with suppress(ModuleNotFoundError):
                import pyi_splash

                pyi_splash.close()

        self.already_transfered_files = self._get_files_and_mod_times(
            self._config.gcode_dir,
        )

    def _should_copy_file(
        already_copied_files: dict[str, float],
        file_name: str,
        last_mode_time: float,
    ) -> bool:
        should_copy = False
        try:
            mod_time = already_copied_files[file_name]
            if last_mode_time > mod_time:
                should_copy = True
        except Exception as _:
            should_copy = True
            print("new file - copying")
        return should_copy

    def _get_data_path(relative_path: str) -> str:
        bundle_dir = None
        if getattr(sys, "frozen", False):
            bundle_dir = sys._MEIPASS
        else:
            bundle_dir = os.path.dirname(os.path.abspath(__file__))

        return os.path.join(bundle_dir, relative_path)

    def run(self):
        while True:
            files = self._get_files_and_mod_times(self._config.gcode_dir)
            for file_name in files:
                mod_time = files[file_name]
                file_path = os.path.join(self._config.gcode_dir, file_name)
                if self._should_copy_file(
                    self.already_transfered_files,
                    file_name,
                    mod_time,
                ) and i_am_the_owner(file_path):
                    copy_file(file_path, new_path=self._config.target_dir)
                    show_notification(self._get_data_path())
                    self.already_transfered_files[file_name] = mod_time

            time.sleep(self._config.speed_s)
