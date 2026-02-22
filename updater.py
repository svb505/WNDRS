import os
import zipfile
import shutil
import requests
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import time
from logger_setup import system_logger, system_logger1

start_time_ = time.time()

CURRENT_VERSION_FILE = 'versions/current_version.txt'
BACKUP_DIR = 'backup'
UPDATE_CHECK_URL = "https://raw.githubusercontent.com/svb505/updater_server/main/version.txt"
UPDATE_ZIP_URL = "https://github.com/svb505/updater_server/raw/main/update.zip"

def log_to_file(msg, start_time_, level="info"):
    try:
        elapsed = time.time() - start_time_
    except NameError:
        elapsed = 0
    formatted_msg = f"[{elapsed:.1f}] - {msg}"
    if level == "info":
        system_logger.info(formatted_msg)
        system_logger1.info(formatted_msg)
    elif level == "warning":
        system_logger.warning(formatted_msg)
        system_logger1.warning(formatted_msg)
    elif level == "error":
        system_logger.error(formatted_msg)
        system_logger1.error(formatted_msg)
    else:
        system_logger.debug(formatted_msg)
        system_logger1.debug(formatted_msg)

def update_log(msg, start_time_):
    try:
        elapsed = time.time() - start_time_
    except NameError:
        elapsed = 0
    formatted_msg = f"[{elapsed:.1f}] - {msg}"
    os.makedirs("syst_comp", exist_ok=True)
    with open("syst_comp/updates_logs.cfg", "a") as f:
        f.write(f"SVB Updater - {formatted_msg}\n")

Win = Tk()
Win.geometry('600x600')
Win.title("SVB Updater")
Win.resizable(False, False)

image = Image.open("icons/updater.png")
icon_image = ImageTk.PhotoImage(image)
Win.icon_img_ref = icon_image
Win.iconphoto(True, Win.icon_img_ref)

log_box = Text(Win, wrap=WORD, font=("Consolas", 11))
log_box.pack(expand=True, fill=BOTH, padx=10, pady=10)

progress = ttk.Progressbar(Win, orient="horizontal", mode="determinate")
progress.pack(fill=X, padx=10, pady=(0, 5))
progress_label = Label(Win, text="0%", font=("Arial", 10))
progress_label.pack()
stage_label = Label(Win, text="⏳ Waiting for launch...", font=("Arial", 11, "italic"))
stage_label.pack(pady=(0, 10))

def log(msg):
    log_box.insert(END, msg + '\n')
    log_box.see(END)
def read_current_version():
    if os.path.exists(CURRENT_VERSION_FILE):
        with open(CURRENT_VERSION_FILE, 'r') as f:
            return f.read().strip()
    return None
def write_current_version(version):
    with open(CURRENT_VERSION_FILE, 'w') as f:
        f.write(version)
def backup_file(target_path):
    backup_path = os.path.join(BACKUP_DIR, target_path)
    os.makedirs(os.path.dirname(backup_path), exist_ok=True)
    shutil.copy2(target_path, backup_path)
    log(f"🛡 Backed up: {target_path}")
    log_to_file(f"Backed up: {target_path}", start_time_)
    update_log(f"Backed up: {target_path}", start_time_)
def restore_backup():
    stage_label.config(text="⏪ Rolling back update...")
    log("⚠ Rolling back from backup...")
    log_to_file("Rolling back from backup...", start_time_, level="warning")
    update_log("Rolling back from backup...", start_time_)
    for root, _, files in os.walk(BACKUP_DIR):
        for file in files:
            src = os.path.join(root, file)
            rel_path = os.path.relpath(src, BACKUP_DIR)
            dst = os.path.join('.', rel_path)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)
            log(f"⏪ Restored: {rel_path}")
    log("✅ Rollback completed.")
    log_to_file("Rollback completed.", start_time_)
    update_log("Rollback completed.", start_time_)
    stage_label.config(text="⏪ Rollback completed.")
def apply_update(zip_path='update.zip'):
    log("[UI] Starting update process...")
    log_to_file("[UI] Starting update process...", start_time_)
    update_log("[UI] Starting update process...", start_time_)

    stage_label.config(text="📦 Extracting archive...")
    progress["value"] = 0
    progress_label.config(text="0%")
    Win.update_idletasks()

    if not zipfile.is_zipfile(zip_path):
        log("❌ Error: ZIP archive not found or invalid.")
        log_to_file("ZIP archive is invalid.", start_time_, level="error")
        return

    try:
        log("[UI] Valid ZIP archive detected.")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            root_folder = None
            for name in zip_ref.namelist():
                if name.endswith('/'):
                    parts = name.split('/')
                    if len(parts) == 2:
                        root_folder = parts[0]
                        break

            if not root_folder:
                log("❌ Error: Archive must contain a single root folder.")
                log_to_file("No root folder in archive.", start_time_, level="error")
                return

            manifest_path = f"{root_folder}/manifest.txt"
            version_path = f"{root_folder}/version.txt"

            if manifest_path not in zip_ref.namelist() or version_path not in zip_ref.namelist():
                log("❌ Archive missing manifest or version.txt")
                log_to_file("Missing manifest or version.txt", start_time_, level="error")
                return

            update_version = zip_ref.read(version_path).decode('utf-8').strip()
            current_version = read_current_version()

            log(f"📦 Update version: {update_version}")
            log_to_file(f"Update version: {update_version}", start_time_)

            if current_version == update_version:
                log("🟡 You already have the latest version. No update needed.")
                log_to_file("Already up-to-date.", start_time_)
                return

            manifest_lines = zip_ref.read(manifest_path).decode('utf-8').strip().splitlines()
            manifest_lines = [line for line in manifest_lines if '->' in line]

            progress["maximum"] = len(manifest_lines)
            stage_label.config(text="📁 Updating files...")

            for idx, line in enumerate(manifest_lines, start=1):
                src_file, dest_dir = map(str.strip, line.split('->'))
                archive_path = f"{root_folder}/{src_file}"

                if archive_path not in zip_ref.namelist():
                    log(f"⚠ Skipped: {src_file} not found in archive.")
                    continue

                dest_path = os.path.join(dest_dir, os.path.basename(src_file))
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)

                if os.path.exists(dest_path):
                    backup_file(dest_path)

                with zip_ref.open(archive_path) as src, open(dest_path, 'wb') as dst:
                    shutil.copyfileobj(src, dst)

                log(f"✔ Installed: {src_file} → {dest_path}")
                progress["value"] = idx
                percent = int((idx / len(manifest_lines)) * 100)
                progress_label.config(text=f"{percent}%")
                Win.update_idletasks()

            write_current_version(update_version)
            log(f"🆕 Updated to version: {update_version}")
            log_to_file(f"Updated to version: {update_version}", start_time_)
            update_log(f"Updated to version: {update_version}", start_time_)

            stage_label.config(text="✅ Update completed.")
            log("✅ Update completed successfully.")
            log_to_file("Update completed successfully.", start_time_)
            update_log("Update completed successfully.", start_time_)

        os.remove(zip_path)
        log(f"🧹 Archive deleted: {zip_path}")
        log_to_file(f"Archive deleted: {zip_path}", start_time_)
        update_log(f"Archive deleted: {zip_path}", start_time_)

    except Exception as e:
        log(f"❌ Installation error: {e}")
        log_to_file(f"Installation error: {e}", start_time_, level="error")
        update_log(f"Installation error: {e}", start_time_)
        restore_backup()
        stage_label.config(text="❌ Error occurred. Rollback performed.")
def check_for_update_from_server():
    stage_label.config(text="🌐 Checking for updates...")
    log("🌐 Checking for updates...")
    log_to_file("Checking for updates...", start_time_)
    update_log("Checking for updates...", start_time_)

    try:
        response = requests.get(UPDATE_CHECK_URL, timeout=10)
        if response.status_code != 200:
            log("⚠ Failed to get version from server.")
            log_to_file("Failed to get version from server.", start_time_, level="warning")
            return

        server_version = response.text.strip()
        current_version = read_current_version()

        log(f"🌐 Server version: {server_version}")
        log_to_file(f"Server version: {server_version}", start_time_)
        update_log(f"Server version: {server_version}", start_time_)

        if current_version:
            log(f"💻 Local version: {current_version}")
            log_to_file(f"Local version: {current_version}", start_time_)
            update_log(f"Local version: {current_version}", start_time_)

        if current_version == server_version:
            log("🟢 You have the latest version.")
            log_to_file("Latest version confirmed.", start_time_)
            update_log("Latest version confirmed.", start_time_)
            stage_label.config(text="✅ No updates found.")
            return

        log("🔄 Update available. Downloading...")
        log_to_file("Update available. Downloading...", start_time_)
        update_log("Update available. Downloading...", start_time_)
        stage_label.config(text="⬇ Downloading update...")

        zip_response = requests.get(UPDATE_ZIP_URL, stream=True)
        if zip_response.status_code != 200:
            log("❌ Error downloading update archive.")
            log_to_file("Error downloading archive.", start_time_, level="error")
            return

        total_size = int(zip_response.headers.get('content-length', 0))
        downloaded = 0
        chunk_size = 1024 * 128

        with open("update.zip", "wb") as f:
            for chunk in zip_response.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    percent = int(downloaded * 100 / total_size) if total_size else 0
                    progress["value"] = percent
                    progress_label.config(text=f"{percent}%")
                    Win.update_idletasks()

        log("✅ Update archive downloaded.")
        log_to_file("Update archive downloaded.", start_time_)
        update_log("Update archive downloaded.", start_time_)

        apply_update("update.zip")

    except Exception as e:
        log(f"❌ Error checking for updates: {e}")
        log_to_file(f"Error checking for updates: {e}", start_time_, level="error")
        update_log(f"Error checking for updates: {e}", start_time_)
        stage_label.config(text="❌ Connection error.")

btn = ttk.Button(Win, text="🔁 Check and update", command=check_for_update_from_server)
btn.pack(pady=10)

Win.mainloop()
