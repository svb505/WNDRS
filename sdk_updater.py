import requests
import zipfile
import shutil
import os
import threading
import subprocess
import psutil
import time
from tkinter import Tk, Toplevel, Label, ttk, messagebox
import traceback

VERSION_URL = "https://raw.githubusercontent.com/svb505/sdk_version/main/version.txt"
UPDATE_ZIP_URL = "https://www.dropbox.com/scl/fi/t7mwascfa8rjvh5ypsj41/sdk_updater.zip?rlkey=6ehyxkl56482f4qrdtr1iaxoh&st=g9khxded&dl=0"
LOCAL_VERSION_FILE = "sdk_version.txt"

def log_to_file(msg, start_time_, level="info"):
    elapsed = time.time() - start_time_ if start_time_ else 0
    print(f"[{elapsed:.1f}] {level.upper()}: {msg}")

def update_log(msg, start_time_, level="info"):
    elapsed = time.time() - start_time_ if start_time_ else 0
    log_path = os.path.join("sdk_settings", "updates_logs.cfg")
    os.makedirs("sdk_settings", exist_ok=True)
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"[{elapsed:.1f}] {level.upper()}: {msg}\n")

def kill_process_if_running(process_name, start_time_):
    killed = False
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if process_name.lower() in proc.info['name'].lower():
                log_to_file(f"[process] Found running process: {proc.info['name']} (PID {proc.info['pid']})", start_time_)
                update_log(f"[process] Found running process: {proc.info['name']} (PID {proc.info['pid']})", start_time_)
                proc.terminate()
                try:
                    proc.wait(timeout=10)
                except psutil.TimeoutExpired:
                    log_to_file(f"[process] Timeout expired. Killing process {proc.info['name']}", start_time_, level="warning")
                    proc.kill()
                killed = True
                log_to_file(f"[process] Process {proc.info['name']} terminated", start_time_)
                update_log(f"[process] Process {proc.info['name']} terminated", start_time_)
        except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
            log_to_file(f"[process] Error terminating process: {e}", start_time_, level="error")
            update_log(f"[process] Error terminating process: {e}", start_time_, level="error")
    return killed

def read_local_version():
    if os.path.exists(LOCAL_VERSION_FILE):
        with open(LOCAL_VERSION_FILE, "r") as f:
            return f.read().strip()
    return None

def write_local_version(ver, start_time_):
    with open(LOCAL_VERSION_FILE, "w") as f:
        f.write(ver)
    log_to_file(f"[write_local_version] New version written: {ver}", start_time_)
    update_log(f"[write_local_version] New version written: {ver}", start_time_)

def check_update(auto_update_enabled, lang, start_time_):
    root = Tk()
    root.withdraw()  # Ð ÐÐ ÑÐ¡ÐÐ¡â¹Ð ÐÐ Â°Ð ÂµÐ Ñ Ð ÑÐ Â»Ð Â°Ð ÐÐ ÐÐ ÑÐ Âµ Ð ÑÐ ÑÐ ÐÐ Ñ

    log_to_file("[check_update] Started checking for updates", start_time_)
    update_log("[check_update] Started checking for updates", start_time_)

    try:
        response = requests.get(VERSION_URL, timeout=10)
        response.raise_for_status()
        remote_version = response.text.strip()
        local_version = read_local_version()

        log_to_file(f"[update] local: {local_version}, remote: {remote_version}", start_time_)
        update_log(f"[update] local: {local_version}, remote: {remote_version}", start_time_)

        if remote_version == local_version:
            log_to_file("[update] Already latest.", start_time_)
            update_log("[update] Already latest.", start_time_)
            root.destroy()
            return
        if remote_version != local_version:
            # 📌 Сохраняем флаг наличия обновы для my_os.py
            try:
                with open("sdk_settings/update_flag.cache", "w", encoding="utf-8") as f:
                    f.write(remote_version)
            except Exception as e:
                log_to_file(f"[flag] Could not write update flag: {e}", start_time_, level="error")
                update_log(f"[flag] Could not write update flag: {e}", start_time_, level="error")

        def download_and_apply_update():
            win = Toplevel()
            win.title(lang["update"])
            win.geometry("400x130")

            Label(win, text=f" {lang['update_download']}").pack(pady=10)
            pb = ttk.Progressbar(win, orient="horizontal", mode="determinate")
            pb.pack(fill="x", padx=10, pady=5)
            progress_label = Label(win, text="0%")
            progress_label.pack()
            stage_label = Label(win, text=lang["ogidanie"])
            stage_label.pack()

            def do_update():
                try:
                    r = requests.get(UPDATE_ZIP_URL, stream=True)
                    r.raise_for_status()
                    total = int(r.headers.get('content-length', 0))
                    downloaded = 0
                    log_to_file("[download] Starting ZIP download...", start_time_)
                    update_log("[download] Starting ZIP download...", start_time_)
                    with open("update.zip", "wb") as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                                downloaded += len(chunk)
                                percent = int(downloaded * 100 / total) if total else 0
                                pb["value"] = percent
                                progress_label.config(text=f"{percent}%")
                                win.update_idletasks()

                    kill_process_if_running("WD SDK.exe", start_time_)

                    stage_label.config(text=lang["rasp"])
                    with zipfile.ZipFile("update.zip", "r") as zip_ref:
                        root_folder = None
                        for name in zip_ref.namelist():
                            if name.endswith('/') and len(name.split('/')) == 2:
                                root_folder = name.strip('/')
                                break
                        if not root_folder:
                            raise Exception(lang["not_corn_folder"])

                        manifest_path = f"{root_folder}/manifest.txt"
                        version_path = f"{root_folder}/version.txt"

                        if manifest_path not in zip_ref.namelist():
                            raise Exception(lang["not_manifest"])
                        if version_path not in zip_ref.namelist():
                            raise Exception(lang["not_version"])

                        manifest_lines = zip_ref.read(manifest_path).decode("utf-8").splitlines()
                        manifest_lines = [line for line in manifest_lines if "->" in line]
                        stage_label.config(text=lang["downloading_files"])
                        pb["maximum"] = len(manifest_lines)

                        for idx, line in enumerate(manifest_lines, start=1):
                            src_entry, dst_dir = map(str.strip, line.split("->"))
                            archive_entry = f"{root_folder}/{src_entry}".replace("\\", "/")
                            dst_dir = dst_dir.strip().rstrip("/\\")
                            copied_count = 0

                            if archive_entry.endswith("/"):
                                # Копируем папку
                                for member in zip_ref.namelist():
                                    if member.startswith(archive_entry) and not member.endswith("/"):
                                        relative_path = os.path.relpath(member, archive_entry)
                                        dst_path = os.path.join(dst_dir, relative_path)
                                        os.makedirs(os.path.dirname(dst_path), exist_ok=True)
                                        with zip_ref.open(member) as src, open(dst_path, "wb") as dst:
                                            shutil.copyfileobj(src, dst)
                                        log_to_file(f"[extract] Folder file: {member} -> {dst_path}", start_time_)
                                        update_log(f"[extract] Folder file: {member} -> {dst_path}", start_time_)
                                        copied_count += 1
                            else:
                                # Копируем файл
                                if archive_entry not in zip_ref.namelist():
                                    log_to_file(f"[warning] File not found in archive: {archive_entry}", start_time_)
                                    continue
                                dst_path = os.path.join(dst_dir, os.path.basename(src_entry))
                                os.makedirs(os.path.dirname(dst_path), exist_ok=True)
                                with zip_ref.open(archive_entry) as src, open(dst_path, "wb") as dst:
                                    shutil.copyfileobj(src, dst)
                                log_to_file(f"[extract] File: {archive_entry} -> {dst_path}", start_time_)
                                update_log(f"[extract] File: {archive_entry} -> {dst_path}", start_time_)
                                copied_count += 1

                            pb["value"] = idx
                            progress_label.config(
                                text=f"{int(idx / len(manifest_lines) * 100)}% ({copied_count} files)")
                            win.update_idletasks()

                        new_version = zip_ref.read(version_path).decode('utf-8').strip()
                        write_local_version(new_version, start_time_)

                    os.remove("update.zip")
                    log_to_file("[cleanup] Removing update.zip", start_time_)
                    update_log("[cleanup] Removing update.zip", start_time_)

                    win.destroy()
                    root.destroy()

                    main_exe_path = os.path.join(os.getcwd(), "WD SDK.exe")
                    subprocess.Popen([main_exe_path], shell=False)

                    messagebox.showinfo(lang['update'], lang["upd_finish"])
                    log_to_file(f"[update] Update complete", start_time_)
                    update_log(f"[update] Update complete", start_time_)
                    # Удаляем флаг
                    try:
                        os.remove("sdk_settings/update_flag.cache")
                    except Exception as e:
                        log_to_file(f"[flag] Could not remove update flag: {e}", start_time_, level="warning")


                except Exception as e:
                    win.destroy()
                    root.destroy()
                    err = traceback.format_exc()
                    messagebox.showerror(lang['error'], f"{lang['upd_error']}\n{e}\n{err}")
                    log_to_file(f"[update]  Error during update: {e}\n{err}", start_time_, level='error')
                    update_log(f"[update]  Error during update: {e}\n{err}", start_time_, level='error')

            threading.Thread(target=do_update, daemon=True).start()

        if auto_update_enabled:
            messagebox.showinfo(lang['update'], f"{lang['avaible2_version']} {remote_version}. {lang['start_ust']}")
            log_to_file("[update] Start updating", start_time_)
            update_log("[update] Start updating", start_time_)
            download_and_apply_update()
        else:
            if messagebox.askyesno(lang['avaible_update'], f"{lang['obn_new_ver']} {remote_version}. {lang['update?']}"):
                log_to_file("[update] The user agreed to update", start_time_)
                update_log("[update] The user agreed to update", start_time_)
                download_and_apply_update()
            else:
                log_to_file("[update] The user refused to update", start_time_)
                update_log("[update] The user refused to update", start_time_)

    except Exception as e:
        err = traceback.format_exc()
        log_to_file(f"[Error checking for updates]: {e}\n{err}", start_time_, level='error')
        update_log(f"[Error checking for updates]: {e}\n{err}", start_time_, level='error')
        root.destroy()

    log_to_file("[check_update] Finished checking for updates", start_time_)
    update_log("[check_update] Finished checking for updates", start_time_)
    root.mainloop()


if __name__ == "__main__":
    lang = {
        "update": "Update",
        "update_download": "Downloading update...",
        "ogidanie": "Waiting...",
        "rasp": "Extracting files...",
        "not_corn_folder": "Root folder is missing in the archive",
        "not_manifest": "manifest.txt is missing in the archive",
        "not_version": "version.txt is missing in the archive",
        "downloading_files": "Copying files...",
        "download_usp": "Update completed",
        "upd_finish": "Update successfully completed!",
        "error": "Error",
        "upd_error": "An error occurred during update",
        "avaible2_version": "Available version",
        "start_ust": "Starting installation...",
        "avaible_update": "Update available",
        "obn_new_ver": "A new version is available",
        "update?": "Update now?",
    }

    start_time = time.time()
    auto_update_enabled = False  # True Ð ÑÐ Â»Ð Ñ False
    check_update(auto_update_enabled, lang, start_time)
