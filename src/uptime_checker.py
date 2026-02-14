
import os
import time
from src.notifier import Notifier
from src.vars import Vars


class UptimeChecker:
    def __init__(self, vars:Vars, notifier:Notifier):
        self._vars = vars
        self._notifier = notifier
        self._last_loop_server_down = False
        self._running = True
    
    def _all_directories_exist(self) -> bool:
        check_dirs = self._vars.gcode_dirs + [self._vars.target_dir]
        for dir in check_dirs:
            if not os.path.exists(dir):
                return False
        return True

    def run(self):
        while self._running:
            all_exist = self._all_directories_exist()
            if not all_exist and not self._last_loop_server_down:
                self._notifier.show_notification('server down', title='Uptime Checker - Error')
                self._last_loop_server_down = True
            
            if all_exist:
                self._last_loop_server_down = False
            time.sleep(5)
        
    def stop(self):
        self._running = False