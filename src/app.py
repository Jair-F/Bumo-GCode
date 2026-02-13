from contextlib import suppress

import pyshortcuts

from src.duplicator import Duplicator
from src.vars import Vars


class App:
    def __init__(self):
        self._vars = Vars()
        self._duplicator = Duplicator(self._vars)
        self._startup()

    def _auto_install_startup(self) -> bool:
        return True
        pyshortcuts.make_shortcut(
            script=self._get_exe_path(),
            name=self._vars.startup_shortcut_name,
            folder=self._vars.auto_start_dir,
            icon=self._vars.icon_file_name,
            description=None,
        )
        print(f"Shortcut '{self._vars.startup_shortcut_name}' created.")
        return True

    def _startup(self):
        if self._vars.running_as_exe():
            self._auto_install_startup()
            with suppress(ModuleNotFoundError):
                import pyi_splash

                pyi_splash.close()

        self._duplicator.init()

    def run(self):
        self._duplicator.run()


if __name__ == '__main__':
    app = App()
    app.run()
