import os
import shutil
import time

from src.tools import i_am_the_owner, show_notification
from src.vars import Vars


class Duplicator:
    def __init__(self, vars: Vars):
        self._vars = vars
        self._is_running = True
        self._already_transfered_files = {'': 0.0}

    def init(self):
        self._create_target_dirs()
        self._already_transfered_files = self._get_files_and_mod_times(
            self._vars.gcode_dir,
        )

    def _create_target_dirs(self) -> None:
        try:
            os.mkdir(self._vars.gcode_dir)
        except FileExistsError:
            ' '

    def _get_files_and_mod_times(self, directory_path: str) -> dict[str, float]:
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

    def _should_copy_file(
        self,
        file_name: str,
        last_mode_time: float,
    ) -> bool:
        should_copy = False
        try:
            mod_time = self._already_transfered_files[file_name]
            if last_mode_time > mod_time:
                should_copy = True
        except Exception as _:
            should_copy = True
            print('new file - copying')
        return should_copy

    def _copy_file(self, latest_file: str, new_path: str):
        shutil.copy(f'{latest_file}', f'{new_path}')

    def run(self):
        while self._is_running:
            files = self._get_files_and_mod_times(self._vars.gcode_dir)
            for file_name in files:
                mod_time = files[file_name]
                file_path = os.path.join(self._vars.gcode_dir, file_name)
                if self._should_copy_file(
                    file_name,
                    mod_time,
                ) and i_am_the_owner(file_path):
                    self._copy_file(file_path, new_path=self._vars.target_dir)
                    show_notification(
                        self._vars.get_data_file_path(self._vars.icon_file_name),
                    )
                    self._already_transfered_files[file_name] = mod_time

            time.sleep(self._vars.speed_s)

    def stop(self):
        self._is_running = False
