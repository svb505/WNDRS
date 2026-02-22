import os
import threading
from create_window import create_window
import requests
import zipfile
from tkinter import *
from tkinter import messagebox, ttk

VERSION_URL = "https://raw.githubusercontent.com/svb505/sdk_version/main/version.txt"
UPDATE_ZIP_URL = "https://www.dropbox.com/scl/fi/15wn5y65d89p5poxxwmij/sdk_installer.zip?rlkey=yum6e9cfq3f7sw3rgx786ss2z&st=utp30tff&dl=1"
DOCS_ZIP_URL = "https://www.dropbox.com/scl/fi/abcd1234efgh5678/docs.zip?rlkey=xxxx&st=yyyy&dl=1"
SVBENGINE_URL = "https://www.dropbox.com/scl/fi/xzew2uor3gij6g3eki3y3/SVBEngineSetup.zip?rlkey=80ny46w6od054vxzve0rz8wgr&st=6yyq974o&dl=1"
SVBENGINE_FILENAME = "SVBEngineSetup.zip"
LOCAL_VERSION_FILE = "sdk_version.txt"
MAIN_EXECUTABLE = "WD SDK.exe"
ZIP_FILENAME = "sdk_installer.zip"
DOCS_FILENAME = "docs.zip"

def download_funcs(root, lang, type,global_bg,GlobalAlpha):
    def read_local_version():
        if os.path.exists(LOCAL_VERSION_FILE):
            with open(LOCAL_VERSION_FILE, "r") as f:
                return f.read().strip()
        return None
    def write_local_version(ver):
        with open(LOCAL_VERSION_FILE, "w") as f:
            f.write(ver)
    def main_exe_exists():
        return os.path.exists(MAIN_EXECUTABLE)
    def download_and_extract_zip(url, filename, progress_callback, stage_callback, extract_to="."):
        stage_callback(lang["download_file"] + filename)

        response = requests.get(url, stream=True)
        response.raise_for_status()
        total_size = int(response.headers.get('content-length', 0))
        downloaded_size = 0

        with open(filename, 'wb') as f:
            for chunk in response.iter_content(8192):
                if chunk:
                    f.write(chunk)
                    downloaded_size += len(chunk)
                    progress = int((downloaded_size / total_size) * 100)
                    progress_callback(progress)

        stage_callback(lang["rasp_arh"])
        with zipfile.ZipFile(filename, 'r') as zip_ref:
            zip_ref.extractall(extract_to)

        os.remove(filename)
    def run_gui_download(url, filename, extract_to=".", save_version=None, success_msg=None):
        Win = create_window(root,lang['download_sdk'] if type == "sdk" else lang['dwn_doc'],global_bg,GlobalAlpha,450,220,
        "icons/interface/download.png",False,[False,False])

        Win.attributes("-topmost",True)
        Win.resizable(False, False)

        Label(Win, text=lang['download_dost']).pack(pady=5)

        stage_label = Label(Win, text=lang["ozidanie_zagr"])
        stage_label.pack()

        pb = ttk.Progressbar(Win, orient="horizontal", mode="determinate", length=300)
        pb.pack(pady=10)
        pb["maximum"] = 100

        percent_label = Label(Win, text="0%")
        percent_label.pack()

        def update_progress(percent):
            pb["value"] = percent
            percent_label.config(text=f"{percent}%")
            Win.update_idletasks()
        def update_stage(text):
            stage_label.config(text=text)
            Win.update_idletasks()
        def on_download_finished():
            update_stage(lang["download_finish"])
            messagebox.showinfo(lang['success'],success_msg or lang["download_finish_with_success"])

            exe_path = os.path.join(extract_to, "SVBEngine Setup.exe")

            if filename == "SVBEngineSetup.zip" and os.path.exists(exe_path):
                os.startfile(exe_path)

            Win.destroy()

        def download_thread():
            try:
                download_and_extract_zip(url,filename,update_progress,update_stage,extract_to=extract_to)

                if save_version: write_local_version(save_version)

                Win.after(0, on_download_finished)

            except Exception as e:
                Win.after(0, lambda: messagebox.showerror(lang['error'],f"{lang['error_pri_obn']}\n{e}"))

        t = threading.Thread(target=download_thread, daemon=True)
        t.start()
        Win.mainloop()
    def check_for_update():
        try:
            remote_version = requests.get(VERSION_URL, timeout=5).text.strip()
            local_version = read_local_version()

            if remote_version == local_version:
                messagebox.showinfo("", lang["sdk_version_already"])
                return

            if main_exe_exists():
                messagebox.showinfo("", lang["sdk_already"])
                return

            run_gui_download(UPDATE_ZIP_URL, ZIP_FILENAME, save_version=remote_version)
        except Exception as e:
            messagebox.showerror(lang["error"], f"{lang['error_with_prov']}\n{e}")
    if type == "sdk":
        check_for_update()
    elif type == "docs":
        run_gui_download(DOCS_ZIP_URL, DOCS_FILENAME, extract_to="docs", success_msg=lang["docs_finish_with_success"])
    elif type == 'engine':
        run_gui_download(SVBENGINE_URL,SVBENGINE_FILENAME, extract_to="SVBEngineSetup", success_msg=lang["engine_finish_with_success"])
    else:
        messagebox.showerror(lang["error"], f"{lang['unknown_type']}: {type}")
