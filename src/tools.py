import os
import shutil

import win32security
from winotify import Notification


def i_am_the_owner(file_path: str) -> bool:
    sd = win32security.GetFileSecurity(
        file_path,
        win32security.OWNER_SECURITY_INFORMATION,
    )
    owner_sid = sd.GetSecurityDescriptorOwner()
    name, domain, type = win32security.LookupAccountSid(None, owner_sid)

    if os.getlogin() == name:
        return True


def copy_file(latest_file: str, new_path: str):
    shutil.copy(f"{latest_file}", f"{new_path}")


def show_notification(icon: str):
    toast = Notification(
        app_id="Bumotec 2",
        title="",
        msg="GCode was sent successfully",
        duration="short",
        icon=get_data_path(ICON_FILE_NAME),
    )
    toast.show()
