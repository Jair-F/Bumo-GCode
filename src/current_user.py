
import win32security
import os 

FILE_PATH = r"C:\Users\jonik\Desktop\GCode\askdj.txt"

def get_file_owner(file_path):
    sd = win32security.GetFileSecurity(file_path, win32security.OWNER_SECURITY_INFORMATION)
    owner_sid = sd.GetSecurityDescriptorOwner()
    name, domain, type = win32security.LookupAccountSid(None, owner_sid)

    if os.getlogin() == name: return True 
        
# print(get_file_owner(FILE_PATH))