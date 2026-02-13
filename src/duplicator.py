import os
import shutil
import time

import win32security  # pylint: disable=import-error

from src.notifier import Notifier
from src.vars import Vars


class Duplicator:
    def __init__(self, vars: Vars, notifier: Notifier):
        self._vars = vars
        self._notifier = notifier
        self._is_running = True
        self._already_transfered_files: dict[str, float] = {}

    def init(self) -> None:
        self._create_target_dirs()
        self._already_transfered_files = self._get_files_and_mod_times(
            self._vars.gcode_dir,
        )

    def _create_target_dirs(self) -> None:
        try:
            os.mkdir(self._vars.gcode_dir)
        except FileExistsError:
            pass

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
        except KeyError as _:
            should_copy = True
            print('new file - copying')
        return should_copy

    @classmethod
    def am_i_the_owner(cls, file_path: str) -> bool:
        sd = win32security.GetFileSecurity(
            file_path,
            win32security.OWNER_SECURITY_INFORMATION,
        )
        owner_sid = sd.GetSecurityDescriptorOwner()
        name, domain, type = win32security.LookupAccountSid(None, owner_sid)

        if os.getlogin() == name:
            return True

        return False

    def _copy_file(self, latest_file: str, new_path: str) -> None:
        shutil.copy(f'{latest_file}', f'{new_path}')

    def run(self) -> None:
        while self._is_running:
            files = self._get_files_and_mod_times(self._vars.gcode_dir)
            for file_name, mod_time in files.items():
                file_path = os.path.join(self._vars.gcode_dir, file_name)
                if self._should_copy_file(
                    file_name,
                    mod_time,
                ) and Duplicator.am_i_the_owner(file_path):
                    self._copy_file(file_path, self._vars.target_dir)
                    self._notifier.show_notification(
                        'GCode was sent successfully',
                    )
                    self._already_transfered_files[file_name] = mod_time

            time.sleep(self._vars.speed_s)

    def stop(self) -> None:
        self._is_running = False
