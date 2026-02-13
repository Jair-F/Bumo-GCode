import os

import win32security
from winotify import Notification

from tmp.send_gcode import ICON_FILE_NAME, get_data_path


def i_am_the_owner(file_path: str) -> bool:
    sd = win32security.GetFileSecurity(
        file_path,
        win32security.OWNER_SECURITY_INFORMATION,
    )
    owner_sid = sd.GetSecurityDescriptorOwner()
    name, domain, type = win32security.LookupAccountSid(None, owner_sid)

    if os.getlogin() == name:
        return True


def show_notification(icon: str):
    toast = Notification(
        app_id='Bumotec 2',
        title='',
        msg='GCode was sent successfully',
        duration='short',
        icon=get_data_path(ICON_FILE_NAME),
    )
    toast.show()
