# nuitka-project: --standalone
# nuitka-project: --onefile
# nuitka-project: --assume-yes-for-downloads
# nuitka-project: --mingw64
# nuitka-project: --lto=no
# nuitka-project: --remove-output
# nuitka-project: --onefile-windows-splash-screen-image=data/splash.png
# nuitka-project: --output-filename=app.exe

import os
import tempfile
import threading
import time

import pyshortcuts  # pylint: disable=import-error

from src.duplicator import Duplicator
from src.notifier import Notifier
from src.uptime_checker import UptimeChecker
from src.vars import Vars


class App:
    def __init__(self) -> None:
        self._vars = Vars.from_yaml('./config.yaml')
        self._notifier = Notifier(self._vars.get_data_file_path(self._vars.icon_file_name))
        self._duplicators = Duplicator(self._vars, self._notifier)
        self._uptime_checker = UptimeChecker(self._vars, self._notifier)

        self._vars.inject_notifier(self._notifier)

        self._duplicator_thread = threading.Thread(target=self._duplicators.run)
        self._uptime_checker_thread = threading.Thread(target=self._uptime_checker.run)
        self._duplicator_thread.daemon = True
        self._uptime_checker_thread.daemon = True

        self._startup()

    def _auto_install_startup(self) -> bool:
        os.makedirs(self._vars.auto_start_dir, exist_ok=True)

        pyshortcuts.make_shortcut(
            script=self._vars.get_exe_path(),
            name=self._vars.startup_shortcut_name,
            folder=self._vars.auto_start_dir,
            icon=self._vars.icon_file_name,
            description=None,
        )
        print(f"Shortcut '{self._vars.startup_shortcut_name}' created.")
        return True

    def _close_splash(self) -> None:
        if 'NUITKA_ONEFILE_PARENT' in os.environ:
            splash_filename = os.path.join(
                tempfile.gettempdir(),
                'onefile_%d_splash_feedback.tmp',
            )
            if os.path.exists(splash_filename):
                os.unlink(splash_filename)

    def _startup(self) -> None:
        if self._vars.running_as_exe():
            print('auto installing in startup folder')
            self._auto_install_startup()
            self._close_splash()

        self._duplicators.init()

    def run(self) -> None:
        self._duplicator_thread.start()
        self._uptime_checker_thread.start()

        while True:
            if self._vars.auto_reload_config():
                self._duplicators.init()
            time.sleep(5)

    def stop(self) -> None:
        self._duplicators.stop()
        self._uptime_checker.stop()

        self._duplicator_thread.join()
        self._uptime_checker_thread.join()


if __name__ == '__main__':
    app = App()
    try:
        app.run()
    except KeyboardInterrupt as _:
        app.stop()
