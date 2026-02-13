from winotify import Notification  # pylint: disable=import-error

from src.vars import Vars


class Notifier:  # pylint: disable=too-few-public-methods
    def __init__(self, vars: Vars):
        self._vars = vars

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
            icon=self._vars.icon_file_name,
        )
        toast.show()
