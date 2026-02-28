import argparse
import os
import pathlib
import sys
import tempfile
import threading
import time
from contextlib import ExitStack

import pidfile  # pylint: disable=import-error
import pyshortcuts  # pylint: disable=import-error

from src.duplicator import Duplicator
from src.notifier import Notifier
from src.uptime_checker import UptimeChecker
from src.vars import Vars


class App:
    def __init__(self, force_run: bool = False) -> None:
        self._stack = ExitStack()
        self._vars = Vars.from_yaml('./config.yaml')
        self._notifier = Notifier(self._vars.get_data_file_path(self._vars.icon_file_name))

        self._exit_if_already_running(force_run)

        self._duplicators = Duplicator(self._vars, self._notifier)
        self._uptime_checker = UptimeChecker(self._vars, self._notifier)

        self._vars.inject_notifier(self._notifier)

        self._duplicator_thread = threading.Thread(target=self._duplicators.run)
        self._uptime_checker_thread = threading.Thread(target=self._uptime_checker.run)
        self._duplicator_thread.daemon = True
        self._uptime_checker_thread.daemon = True

        print(self._vars.running_as_exe())
        print(self._vars.get_data_file_path('..\\icon\\icon.ico'))

        self._startup()

    def _exit_if_already_running(self, force_run: bool = False) -> None:
        program_data_path = os.path.expandvars('%APPDATA%')
        pid_file_path = os.path.join(program_data_path, 'Bumo_GCode\\app.pidfile')

        if force_run:
            try:
                os.remove(pid_file_path)
                self._notifier.show_notification(
                    title='Program already running',
                    msg='force removed pidfile of already running instance',
                )
            except FileNotFoundError:
                pass

        pathlib.Path(os.path.dirname(pid_file_path)).mkdir(
            parents=True,
            exist_ok=True,
        )

        try:
            self._pid_file = self._stack.enter_context(pidfile.PIDFile(pid_file_path))
        except pidfile.AlreadyRunningError:
            self._notifier.show_notification(
                title='Program already running',
                msg='exiting - please close first the already running one.',
            )
            time.sleep(2)
            sys.exit(-1)

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
                f'onefile_{int(os.environ["NUITKA_ONEFILE_PARENT"])}_splash_feedback.tmp',
            )
            if os.path.exists(splash_filename):
                try:
                    os.unlink(splash_filename)
                except OSError:
                    print('no splash configured or splash already closed.')

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

        self._stack.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Copier')
    parser.add_argument('--force', action='store_true', help='Forcefully run even if an instance is already running')
    args = parser.parse_args()

    app = App(args.force)
    try:
        app.run()
    except KeyboardInterrupt as _:
        app.stop()
