import ctypes
import os
import sys
import threading
from logtofile import log_to_file

def run_updater(start_time_):
    exe_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    updater_path = os.path.join(exe_dir, "updater.exe")
    log_to_file(f"Updater Path: {updater_path}", start_time_=start_time_)
    log_to_file(f"Exists: {os.path.exists(updater_path)}", start_time_=start_time_)
    if os.path.exists(updater_path):
        threading.Thread(target=ctypes.windll.shell32.ShellExecuteW(None, "runas", updater_path, None, None, 1))
    else:
        log_to_file(f"Updater not found", start_time_=start_time_, level="error")