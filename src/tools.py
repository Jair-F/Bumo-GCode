import os

import win32security  # pylint: disable=import-error
from winotify import Notification  # pylint: disable=import-error


def i_am_the_owner(file_path: str) -> bool:
    sd = win32security.GetFileSecurity(
        file_path,
        win32security.OWNER_SECURITY_INFORMATION,
    )
    owner_sid = sd.GetSecurityDescriptorOwner()
    name, domain, type = win32security.LookupAccountSid(None, owner_sid)

    if os.getlogin() == name:
        return True

    return False


def show_notification(icon: str) -> None:
    toast = Notification(
        app_id='Bumotec 2',
        title='',
        msg='GCode was sent successfully',
        duration='short',
        icon=icon,
    )
    toast.show()
