import os
from contextlib import suppress

import pyshortcuts  # pylint: disable=import-error

from src.duplicator import Duplicator
from src.notifier import Notifier
from src.vars import Vars


class App:
    def __init__(self) -> None:
        self._vars = Vars.from_yaml('./config.yaml')
        self._notifier = Notifier(self._vars)
        self._duplicator = Duplicator(self._vars, self._notifier)
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

    def _startup(self) -> None:
        if self._vars.running_as_exe():
            self._auto_install_startup()
            with suppress(ModuleNotFoundError):
                # pylint: disable=import-error, import-outside-toplevel
                import pyi_splash

                pyi_splash.close()

        self._duplicator.init()

    def run(self) -> None:
        self._duplicator.run()

    def stop(self) -> None:
        self._duplicator.stop()


if __name__ == '__main__':
    app = App()
    try:
        app.run()
    except KeyboardInterrupt as _:
        app.stop()
