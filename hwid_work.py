import hashlib
import os
import subprocess
from logtofile import log_system
from show_error import show_error
from crypto_work import load_key
from cryptography.fernet import Fernet

DID_FILENAME = "hwid.key"

def get_disk_serial() -> str:
    try:
        output = subprocess.check_output("wmic diskdrive get SerialNumber", shell=True)
        serial = output.decode(errors="ignore").split("\n")[1].strip()
        return serial
    except Exception:
        try:
            output = subprocess.check_output("lsblk -o SERIAL", shell=True)
            lines = output.decode(errors="ignore").split("\n")
            for line in lines:
                if line.strip() and "SERIAL" not in line:
                    return line.strip()
        except Exception:
            pass
    return "UNKNOWN"
def get_hardware_id() -> str:
    serial = get_disk_serial()
    return hashlib.sha256(serial.encode()).hexdigest()
def load_or_create_key():
   key = load_key()
   return Fernet(key)
def save_encrypted_hwid(hwid: str):
    cipher = load_or_create_key()
    encrypted = cipher.encrypt(hwid.encode())
    with open(f"syst_comp/{DID_FILENAME}", "wb") as f:
        f.write(encrypted)
def load_encrypted_hwid() -> str:
    cipher = load_or_create_key()
    with open(f"syst_comp/{DID_FILENAME}", "rb") as f:
        encrypted = f.read()
    return cipher.decrypt(encrypted).decode()
def check_did(start_time_):
    current_hwid = get_hardware_id()
    if not os.path.exists(f"syst_comp/{DID_FILENAME}"):
        log_system("🔐 License not found. Binding to current PC...",start_time_)
        save_encrypted_hwid(current_hwid)
        return True
    try: saved_hwid = load_encrypted_hwid()

    except Exception:
        log_system("⚠ Error: The license file is corrupted!", start_time_)
        return False
    if saved_hwid != current_hwid:
        log_system("⛔ Error: The program is running on another PC!", start_time_)
        show_error("⛔ Error: The program is running on another PC!")
        return False

    return True