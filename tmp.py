import os
import time

from winotify import Notification


class Notifier:  # pylint: disable=too-few-public-methods
    def __init__(self):
        pass

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
            icon=os.path.abspath("./data/splash.png"),
        )
        toast.show()
        time.sleep(2)

if __name__ == "__main__":
    toast = Notification(
            app_id="app_id",
            title="title",
            msg="msg",
            duration="short",
            icon="./data/splash.png",
        )
    toast.show()

    notifier = Notifier()
    notifier.show_notification("HI")