from tkinter import *
from tkinter import ttk
import os
import time
from PIL import Image, ImageTk

def cleanup_window(root,lang,global_bg,global_fg,actives_programs,GlobalAlpha):
    actives_programs.append("Cleaning")
    Win = Toplevel(root)
    
    Win.config(bg = global_bg)
    Win.title(lang["cleaning"])
    Win.attributes("-alpha", float(GlobalAlpha))
    Win.geometry("500x200")
    img = Image.open("icons/cleaning.png")
    icon_image = ImageTk.PhotoImage(img)
    Win.iconphoto(False, icon_image)
    SEARCH_DIRS = ["./state", "./logs_session", "./browser", "./screen_recording", "./screenshoots","./.dumps"]
    FILE_EXTENSIONS = [".log", ".tmp", ".bak", ".cache", ".png", ".mp4", ".jpg",".dmp",".avi"]
    ACTIVE_THRESHOLD = 5

    def is_active(filepath):
        try:
            return (time.time() - os.path.getmtime(filepath)) < ACTIVE_THRESHOLD
        except:
            return False
    def should_delete(filename):
        if not FILE_EXTENSIONS:
            return True
        return any(filename.endswith(ext) for ext in FILE_EXTENSIONS)
    def find_deletable_files():
        deletable = []
        for Win_dir in SEARCH_DIRS:
            for dirpath, _, filenames in os.walk(Win_dir):
                for fname in filenames:
                    full_path = os.path.join(dirpath, fname)
                    if should_delete(fname) and not is_active(full_path):
                        deletable.append(full_path)
        return deletable
    def readable_size(size_bytes):
        return f"{size_bytes / (1024 * 1024):.2f} MB"
    def delete_files():
        deletable = find_deletable_files()
        total_files = len(deletable)
        total_size = sum(os.path.getsize(f) for f in deletable if os.path.exists(f))

        if total_files == 0:
            status_label.config(text=lang["no_files_for_delete"])
            return

        deleted_size = 0
        for i, path in enumerate(deletable, 1):
            try:
                fname = os.path.basename(path)
                status_label.config(text=f"{lang['deleting']}: {fname}")
                Win.update_idletasks()
                size = os.path.getsize(path)
                os.remove(path)
                deleted_size += size
                time.sleep(0.05)
            except Exception as e:
                pass
            progress['value'] = (i / total_files) * 100
            Win.update_idletasks()

        status_label.config(
            text=f"{lang['deleted_']} {total_files} {lang['clean-']} {readable_size(deleted_size)}"
        )
        progress['value'] = 100

    Button(Win, text=lang["delete-files"], command=delete_files).pack(pady=15)
    progress = ttk.Progressbar(Win, orient="horizontal", length=400, mode="determinate")
    progress.pack(pady=10)
    status_label = Label(Win, text=f"      {lang['status__']}      ",bg = global_bg,fg = global_fg)
    status_label.pack()


