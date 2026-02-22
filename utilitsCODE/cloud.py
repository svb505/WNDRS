import os
import base64
import requests
from tkinter import *
from tkinter import filedialog, messagebox, ttk
import time
from PIL import Image, ImageTk
from logtofile import log_to_file
from load_env import load_env

load_env()

GITHUB_TOKEN = os.getenv("CLOUD_TOKEN")
REPO = "svb505/cloud"
BRANCH = "main"
MAX_SIZE_MB = 27
HEADERS = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
}

def cloud(root,lang,actives_programs,global_bg,global_fg,start_time_):
    def github_api_url(path=""):
        return f"https://api.github.com/repos/{REPO}/contents/{path}"
    def update_rate_limit(headers):
        remaining = headers.get("X-RateLimit-Remaining")
        limit = headers.get("X-RateLimit-Limit")
        reset = headers.get("X-RateLimit-Reset")
        if remaining is not None and limit is not None and reset is not None:
            reset_time = time.strftime("%H:%M:%S", time.localtime(int(reset)))
            rate_limit_label.config(
                text=f"{lang['api_limit']}: {remaining} {lang['iz']} {limit} {lang['zaprosov_ost']} {reset_time}"
            )
            log_to_file(f"API LIMIT - {remaining}/{limit}",start_time_)
        else:
            rate_limit_label.config(text=lang['api_info_unavailable'])
            log_to_file(f"API INFO UNAVAILABLE - {remaining}/{limit}", start_time_)
    def refresh():
        tree.delete(*tree.get_children())
        r = requests.get(github_api_url(), headers=HEADERS)
        update_rate_limit(r.headers)
        if r.status_code == 200:
            for file in r.json():
                tree.insert("", "end", values=(file["name"],))
    def upload_file():
        file_path = filedialog.askopenfilename(parent = Win)
        if not file_path:
            return

        file_size = os.path.getsize(file_path)
        if file_size > MAX_SIZE_MB * 1024 * 1024:
            messagebox.showwarning(lang['error'], f"{lang['file_is_big']} {MAX_SIZE_MB} {lang['MB']})",parent = Win)
            return

        with open(file_path, "rb") as f:
            content = base64.b64encode(f.read()).decode("utf-8")
        filename = os.path.basename(file_path)

        data = {
            "message": f"upload {filename}",
            "content": content,
            "branch": BRANCH
        }
        url = github_api_url(filename)
        r = requests.put(url, headers=HEADERS, json=data)
        update_rate_limit(r.headers)

        if r.status_code in (200, 201):
            messagebox.showinfo(lang['success'], lang["file_zagr"],parent = Win)
            refresh()
        else:
            messagebox.showerror(lang['error_zagr'], r.json().get("message", lang['neiz_error']),parent = Win)
    def get_selected_filename():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning(lang['vnim'], lang['pls_select_file'],parent = Win)
            return None
        return tree.item(selected[0])["values"][0]
    def download_file():
        filename = get_selected_filename()
        if not filename:
            log_to_file(f"ERROR: FILE NOT SELECTED", start_time_, "warning")
            return

        url = github_api_url(filename)
        r = requests.get(url, headers=HEADERS)
        update_rate_limit(r.headers)

        if r.status_code != 200:
            messagebox.showerror(lang["error"], lang['wlp_file_not_found'],parent = Win)
            log_to_file(f"ERROR: FILE NOT FOUND", start_time_,"error")
            return

        content = r.json()["content"]
        data = base64.b64decode(content)

        save_path = filedialog.asksaveasfilename(initialfile=filename)
        if not save_path:
            return

        with open(save_path, "wb") as f:
            f.write(data)
        messagebox.showinfo(lang['success'], f"{lang['file']} {filename} {lang['saved']}",parent = Win)
    def delete_file():
        filename = get_selected_filename()
        if not filename:
            return

        if not messagebox.askyesno(lang['confirmation'], f"{lang['delete']} {filename}?",parent = Win):
            return

        r = requests.get(github_api_url(filename), headers=HEADERS)
        update_rate_limit(r.headers)

        if r.status_code != 200:
            messagebox.showerror(lang['error'], lang['wlp_file_not_found'],parent = Win)
            log_to_file(f"ERROR: FILE NOT FOUND", start_time_, "error")
            return

        sha = r.json()["sha"]
        data = {
            "message": f"delete {filename}",
            "sha": sha,
            "branch": BRANCH
        }
        r = requests.delete(github_api_url(filename), headers=HEADERS, json=data)
        update_rate_limit(r.headers)

        if r.status_code == 200:
            messagebox.showinfo(lang['success'], lang['cloud_file_deleted'],parent = Win)
            refresh()
        else:
            messagebox.showerror(lang['error'], r.json().get("message", lang["failed_to_delete_file"]),parent = Win)

    Win = Toplevel(root)
    Win.title(lang['svbcloud'])
    Win.attributes("-topmost",True)
    img = Image.open("icons/interface/cloud.png")
    icon_image = ImageTk.PhotoImage(img)
    Win.iconphoto(False, icon_image)
    tree = ttk.Treeview(Win, columns=("name",), show="headings")
    tree.heading("name", text=lang['files_in_server'])
    tree.pack(fill=BOTH, expand=True)

    btn_frame = Frame(Win)
    btn_frame.pack(pady=5)

    ttk.Button(btn_frame, text=lang["update_list"], command=refresh).grid(row=0, column=0, padx=5)
    ttk.Button(btn_frame, text=lang["add_cloud_file"], command=upload_file).grid(row=0, column=1, padx=5)
    ttk.Button(btn_frame, text=lang["download_file_cloud"], command=download_file).grid(row=0, column=2, padx=5)
    ttk.Button(btn_frame, text=lang['delete_cloud_file'], command=delete_file).grid(row=0, column=3, padx=5)

    rate_limit_label = Label(Win, text=lang["ost_api_requests"])
    rate_limit_label.pack(pady=5)

    refresh()
    Win.mainloop()