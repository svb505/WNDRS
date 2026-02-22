import os
import sys
import winreg
from logtofile import log_to_file


def is_in_autostart(name="WinDoors52"):
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0, winreg.KEY_READ
        )
        value, _ = winreg.QueryValueEx(key, name)
        winreg.CloseKey(key)
        return True if value else False
    except FileNotFoundError:
        return False
def add_exe_to_autostart(start_time_,name="WinDoors52", exe_path=None):
    if exe_path is None: exe_path = sys.executable
    if not os.path.exists(exe_path):
        log_to_file(f"[X] file not found: {exe_path}", level="warning", start_time_=start_time_)
        return

    if is_in_autostart(name):
        log_to_file(f"[!] '{name}' already in startup", level="warning", start_time_=start_time_)
        return

    key = winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        r"Software\Microsoft\Windows\CurrentVersion\Run",
        0, winreg.KEY_SET_VALUE
    )
    winreg.SetValueEx(key, name, 0, winreg.REG_SZ, f'"{exe_path}"')
    winreg.CloseKey(key)
    log_to_file(f"[+] Add in startup: {exe_path}", level="warning", start_time_=start_time_)
def remove_exe_from_autostart(start_time_,name="WinDoors52"):
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0, winreg.KEY_SET_VALUE
        )
        winreg.DeleteValue(key, name)
        winreg.CloseKey(key)
        log_to_file(f"[-] Deleted from startup: {name}", level="warning", start_time_=start_time_)
    except FileNotFoundError:
        log_to_file(f"[!] '{name}' not found in startup.", level="warning", start_time_=start_time_)