import ctypes
from utilits import hashes
from logtofile import log_to_file
from show_error import show_error

dll = ctypes.CDLL("DLLs/ValidateImgHashe.dll")

class Result(ctypes.Structure):
    _fields_ = [("code", ctypes.c_int),
                ("file", ctypes.c_char_p)]

def check(start_time_):
    dll.checkIntegrity.restype = Result
    dll.checkIntegrity.argtypes = [ctypes.c_char_p, ctypes.c_char_p]

    res = dll.checkIntegrity(b"icons", hashes.return_hashes().encode())

    if res.code == 0:
        log_to_file("All files are intact", start_time_)
    elif res.code == 1:
        log_to_file(f"Integrity error: {res.file.decode()}", start_time_,level="error")
        show_error(f"Integrity error: {res.file.decode()}")
    else:
        show_error(f"DLL Error: {res.file.decode()}")
        log_to_file(f"DLL Error: {res.file.decode()}", start_time_,level = 'error')
