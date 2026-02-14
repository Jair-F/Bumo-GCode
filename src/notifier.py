import os
import time
from winotify import Notification  # pylint: disable=import-error


class Notifier:  # pylint: disable=too-few-public-methods
    def __init__(self, icon_file_path:str):
        self._vars = vars
        self.icon_file_path = icon_file_path

    def show_notification(
        self,
        msg: str,
        title: str = '',
        app_id: str = 'Bumotec 2',
        duration: str = 'short',
    ) -> None:
        toast = Notification(
            app_id=app_id,
            title=title,
            msg=msg,
            duration=duration,
            icon=os.path.abspath(self.icon_file_path),
        )
        toast.show()
