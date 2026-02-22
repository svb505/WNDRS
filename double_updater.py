import requests
import zipfile
import shutil
import os
import subprocess
import psutil
import time
from tkinter import Tk, Label, ttk, messagebox
import traceback

SOURCES = [
    {
        "id": "system",
        "name": "WinDoors",
        "version_url": "https://raw.githubusercontent.com/svb505/updater_server/main/version.txt",
        "update_zip_url": "https://www.dropbox.com/scl/fi/gduiepqvqx6iiwzrg0ynw/update.zip?rlkey=w6knel2sie8ocd3lh9mu2tz1w&st=777fg6gm&dl=1",
        "local_version_file": "versions/current_version.txt",
        "main_exe": "WinDoors52.exe",
    },
    {
        "id": "uefi",
        "name": "UEFI",
        "version_url": "https://raw.githubusercontent.com/svb505/uefiupdate/main/version.txt",
        "update_zip_url": "https://www.dropbox.com/scl/fi/beisr13ejgx6o4954ofyq/uefiupd.zip?rlkey=j0eaf3es73lv030j27rfiagpe&st=injq7q34&dl=1",
        "local_version_file": "versions/uefiver.txt",
        "main_exe": "uefi.exe",
    }
]

LOG_DIR = "syst_comp"
LOG_FILE = os.path.join(LOG_DIR, "updates_logs.cfg")
UPDATE_FLAG = os.path.join(LOG_DIR, "updates", "update_flag_uefi.cache")

DEFAULT_LANG = {
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

class UpdaterUI:
    def __init__(self, root, lang):
        self.root = root
        self.lang = lang
        self.root.title("Unified Updater")
        self.root.geometry("520x220")

        Label(self.root, text="Unified Updater", font=("Arial", 18, "bold")).pack(pady=8)
        self.stage_label = Label(self.root, text=lang['ogidanie'], font=("Arial", 12))
        self.stage_label.pack()

        self.pb = ttk.Progressbar(self.root, orient="horizontal", mode="determinate", length=480)
        self.pb.pack(pady=12)

        self.progress_label = Label(self.root, text="0%")
        self.progress_label.pack()

        self.module_label = Label(self.root, text="-", font=("Arial", 11))
        self.module_label.pack(pady=6)

        self.pb['maximum'] = 100
    def set_stage(self, text):
        try:
            self.stage_label.config(text=text)
            self.root.update_idletasks()
        except Exception:
            pass
    def set_progress(self, value):
        try:
            self.pb['value'] = value
            maxv = self.pb['maximum'] if self.pb['maximum'] else 100
            percent = int(value * 100 / maxv) if maxv else 0
            self.progress_label.config(text=f"{percent}%")
            self.root.update_idletasks()
        except Exception:
            pass
    def set_progress_max(self, maximum):
        try:
            self.pb['maximum'] = maximum if maximum > 0 else 100
        except Exception:
            pass
    def set_module(self, text):
        try:
            self.module_label.config(text=text)
            self.root.update_idletasks()
        except Exception:
            pass
def ensure_dirs():
    os.makedirs(LOG_DIR, exist_ok=True)
    os.makedirs(os.path.dirname(UPDATE_FLAG), exist_ok=True)
    os.makedirs(os.path.dirname(SOURCES[0]["local_version_file"]), exist_ok=True)
    os.makedirs(os.path.dirname(SOURCES[1]["local_version_file"]), exist_ok=True)
def log_to_file(msg, start_time_, level="info", tag=None):
    elapsed = time.time() - start_time_ if start_time_ else 0
    prefix = f"[{elapsed:.1f}]"
    if tag:
        prefix += f"[{tag}]"
    print(f"{prefix} {level.upper()}: {msg}")
def update_log(msg, start_time_, level="info", tag=None):
    elapsed = time.time() - start_time_ if start_time_ else 0
    ensure_dirs()
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        if tag:
            f.write(f"[{elapsed:.1f}][{tag}] {level.upper()}: {msg}\n")
        else:
            f.write(f"[{elapsed:.1f}] {level.upper()}: {msg}\n")
def kill_process_if_running(process_name, start_time_):
    killed = False
    if not process_name:
        return False
    for proc in psutil.process_iter(["pid", "name"]):
        try:
            pname = proc.info.get('name') or ''
            if process_name.lower() in pname.lower():
                log_to_file(f"[process] Found running process: {pname} (PID {proc.info['pid']})", start_time_, tag=process_name)
                update_log(f"[process] Found running process: {pname} (PID {proc.info['pid']})", start_time_, tag=process_name)
                proc.terminate()
                try:
                    proc.wait(timeout=10)
                except psutil.TimeoutExpired:
                    log_to_file(f"[process] Timeout expired. Killing {pname}", start_time_, level="warning", tag=process_name)
                    proc.kill()
                killed = True
                log_to_file(f"[process] Process {pname} terminated", start_time_, tag=process_name)
                update_log(f"[process] Process {pname} terminated", start_time_, tag=process_name)
        except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
            log_to_file(f"[process] Error terminating process: {e}", start_time_, level="error", tag=process_name)
            update_log(f"[process] Error terminating process: {e}", start_time_, level="error", tag=process_name)
    return killed
def read_local_version(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip()
    return None
def write_local_version(path, ver, start_time_):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(ver)
    log_to_file(f"[write_local_version] New version written: {ver} -> {path}", start_time_)
    update_log(f"[write_local_version] New version written: {ver} -> {path}", start_time_)
def download_and_apply_update(entry, ui, start_time_):
    """Download entry['update_zip_url'], extract by manifest and write new version file.
    Returns a dict with result info including whether main_exe was present in the archive.
    """
    res = {"updated": False, "main_exe_in_archive": False, "new_version": None}
    try:
        ui.set_stage(f"{entry['name']}: {DEFAULT_LANG['update_download']}")
        r = requests.get(entry['update_zip_url'], stream=True, timeout=30)
        r.raise_for_status()
        total = int(r.headers.get('content-length', 0))
        downloaded = 0
        tmp_zip = f"update_{entry['id']}.zip"
        log_to_file(f"[download] Starting ZIP download for {entry['name']}", start_time_, tag=entry['id'])
        update_log(f"[download] Starting ZIP download for {entry['name']}", start_time_, tag=entry['id'])
        with open(tmp_zip, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    percent = int(downloaded * 100 / total) if total else 0
                    ui.set_progress(percent)
        ui.set_stage(DEFAULT_LANG['rasp'])

        with zipfile.ZipFile(tmp_zip, "r") as zip_ref:
            root_folder = None
            for name in zip_ref.namelist():
                if name.endswith('/') and len(name.split('/')) == 2:
                    root_folder = name.strip('/')
                    break
            if not root_folder:
                raise Exception(DEFAULT_LANG['not_corn_folder'])

            manifest_path = f"{root_folder}/manifest.txt"
            version_path = f"{root_folder}/version.txt"

            if manifest_path not in zip_ref.namelist():
                raise Exception(DEFAULT_LANG['not_manifest'])
            if version_path not in zip_ref.namelist():
                raise Exception(DEFAULT_LANG['not_version'])

            manifest_lines = zip_ref.read(manifest_path).decode("utf-8").splitlines()
            manifest_lines = [line for line in manifest_lines if "->" in line]
            ui.set_stage(DEFAULT_LANG['downloading_files'])
            ui.set_progress(0)
            ui.set_progress_max(len(manifest_lines))

            for idx, line in enumerate(manifest_lines, start=1):
                src_file, dst_dir = map(str.strip, line.split("->"))
                archive_file = f"{root_folder}/{src_file}"

                if archive_file not in zip_ref.namelist():
                    update_log(f"[extract] {archive_file} not found in archive", start_time_, tag=entry['id'])
                    continue

                dst_path = os.path.join(dst_dir, os.path.basename(src_file))
                os.makedirs(os.path.dirname(dst_path), exist_ok=True)

                with zip_ref.open(archive_file) as src, open(dst_path, "wb") as dst:
                    shutil.copyfileobj(src, dst)

                update_log(f"[extract] Copying {archive_file} -> {dst_path}", start_time_, tag=entry['id'])
                if entry.get('main_exe') and os.path.basename(src_file).lower() == entry['main_exe'].lower():
                    res['main_exe_in_archive'] = True
                ui.set_progress(idx)

            new_version = zip_ref.read(version_path).decode('utf-8').strip()
            write_local_version(entry['local_version_file'], new_version, start_time_)
            res['updated'] = True
            res['new_version'] = new_version

        os.remove(tmp_zip)
        update_log(f"[cleanup] Removed {tmp_zip}", start_time_, tag=entry['id'])
        try:
            if os.path.exists(UPDATE_FLAG):
                os.remove(UPDATE_FLAG)
        except Exception:
            pass

    except Exception as e:
        err = traceback.format_exc()
        update_log(f"[update] Error during update {entry['id']}: {e}\n{err}", start_time_, level='error', tag=entry['id'])
        log_to_file(f"[update] Error during update {entry['id']}: {e}", start_time_, level='error', tag=entry['id'])
        raise

    return res
def check_and_apply_all(auto_update_enabled, lang, start_time_):
    log_to_file("[check_all] Started checking for updates", start_time_)
    update_log("[check_all] Started checking for updates", start_time_)

    updates_available = False
    remote_versions = {}
    for entry in SOURCES:
        try:
            resp = requests.get(entry['version_url'], timeout=10)
            resp.raise_for_status()
            remote_version = resp.text.strip()
        except Exception as e:
            update_log(f"[precheck] Could not fetch version for {entry['id']}: {e}", start_time_, level='error', tag=entry['id'])
            continue

        local_version = read_local_version(entry['local_version_file'])
        update_log(f"[precheck] {entry['name']} local={local_version}, remote={remote_version}", start_time_, tag=entry['id'])

        if remote_version and remote_version != local_version:
            updates_available = True
        remote_versions[entry['id']] = remote_version
    if not updates_available:
        log_to_file("[check_all] No updates available — exiting", start_time_)
        update_log("[check_all] No updates available — exiting", start_time_)
        return
    root = Tk()
    ui = UpdaterUI(root, lang)
    root.withdraw()

    try:
        overall_results = []
        restart_required = False
        log_to_file("[check_all] Updates found, opening UI", start_time_)
        update_log("[check_all] Updates found, opening UI", start_time_)

        for entry in SOURCES:
            ui.set_module(entry['name'])
            ui.set_stage("Checking version...")
            root.deiconify()

            remote_version = remote_versions.get(entry['id'])
            local_version = read_local_version(entry['local_version_file'])

            if not remote_version:
                ui.set_stage("Could not check updates")
                overall_results.append({'entry': entry, 'checked': False})
                continue

            if remote_version == local_version:
                log_to_file(f"[update] {entry['name']} already latest.", start_time_, tag=entry['id'])
                update_log(f"[update] {entry['name']} already latest.", start_time_, tag=entry['id'])
                overall_results.append({'entry': entry, 'updated': False})
                continue

            try:
                os.makedirs(os.path.dirname(UPDATE_FLAG), exist_ok=True)
                with open(UPDATE_FLAG, "w", encoding='utf-8') as f:
                    f.write(remote_version)
            except Exception as e:
                update_log(f"[flag] Could not write update flag: {e}", start_time_, level='error', tag=entry['id'])
            if auto_update_enabled:
                ui.set_stage(f"{entry['name']}: {lang['start_ust']}")
                time.sleep(0.5)
                try:
                    result = download_and_apply_update(entry, ui, start_time_)
                    if result.get('main_exe_in_archive') and entry.get('main_exe'):
                        restart_required = True
                    overall_results.append({'entry': entry, 'updated': result.get('updated'), 'new_version': result.get('new_version')})
                except Exception as e:
                    messagebox.showerror(lang['error'], f"{lang['upd_error']}\n{e}")
                    overall_results.append({'entry': entry, 'updated': False, 'error': str(e)})
            else:
                answer = messagebox.askyesno(lang['avaible_update'], f"{lang['obn_new_ver']} {remote_version}. {lang['update?']}")
                if answer:
                    try:
                        result = download_and_apply_update(entry, ui, start_time_)
                        if result.get('main_exe_in_archive') and entry.get('main_exe'):
                            restart_required = True
                        overall_results.append({'entry': entry, 'updated': result.get('updated'), 'new_version': result.get('new_version')})
                    except Exception as e:
                        messagebox.showerror(lang['error'], f"{lang['upd_error']}\n{e}")
                        overall_results.append({'entry': entry, 'updated': False, 'error': str(e)})
                else:
                    overall_results.append({'entry': entry, 'updated': False})

            time.sleep(0.3)

        ui.set_stage("All checks complete")
        update_log("[check_all] Finished checking for updates", start_time_)
        log_to_file("[check_all] Finished checking for updates", start_time_)
        if restart_required:
            exe_path = os.path.join(os.getcwd(), SOURCES[0]['main_exe'])
            if os.path.exists(exe_path):
                try:
                    subprocess.Popen([exe_path], shell=False)
                    update_log(f"[restart] Restarted {exe_path}", start_time_)
                except Exception as e:
                    update_log(f"[restart] Failed to restart {exe_path}: {e}", start_time_, level='error')

        msg_lines = []
        for r in overall_results:
            name = r['entry']['name']
            if r.get('updated'):
                msg_lines.append(f"{name}: updated to {r.get('new_version')}")
            elif r.get('checked') is False:
                msg_lines.append(f"{name}: check failed")
            else:
                msg_lines.append(f"{name}: no update")

        messagebox.showinfo(lang['update'], "\n".join(msg_lines))

    except Exception as e:
        err = traceback.format_exc()
        update_log(f"[Error check_all]: {e}\n{err}", start_time_, level='error')
        log_to_file(f"[Error check_all]: {e}", start_time_, level='error')
        messagebox.showerror(lang['error'], f"{lang['upd_error']}\n{e}")
    finally:
        try:
            root.destroy()
        except Exception:
            pass

if __name__ == "__main__":
    ensure_dirs()
    lang = DEFAULT_LANG
    start_time = time.time()
    auto_update_enabled = False
    try:
        with open("syst_comp/auto_upd.cfg", "rb") as f:
            data = f.read().decode('utf-8')
            auto_update_enabled = data.strip() == "True"
    except Exception:
        auto_update_enabled = False
    check_and_apply_all(auto_update_enabled, lang, start_time)
