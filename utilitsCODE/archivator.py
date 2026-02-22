import os
from tkinter import *
from tkinter import ttk,messagebox,filedialog
import zipfile
from PIL import Image, ImageTk
import customtkinter as ctk
from logtofile import log_to_file

files = []
flag = False
flag_button = False

def open_archivator(actives_programs,root,lang,start_time_,global_bg,global_fg,GlobalAlpha):
    def reset_variables():
        global files, flag, flag_button
        files = []
        flag = False
        flag_button = False
    def refresh_ui():
        global flag_button
        for widget in Win.winfo_children():
            if isinstance(widget, ttk.Combobox) or \
                    (isinstance(widget, Label) and widget not in static_labels):
                widget.destroy()
        if files:
            label = Label(Win, text=lang["selected_files"], font=("Arial", 13, "bold"),bg = global_bg,fg = global_fg)
            label.pack()
            combo = ttk.Combobox(Win, values=files)
            combo.pack()
            if not flag_button:
                ttk.Button(Win, text=lang["create_zip"], command=lambda: create(files, name_entry.get())).pack()
                flag_button = True
        else:
            label = Label(Win, text=lang["no_files_to_arh"], font=("Arial", 15, "bold"),bg = global_bg,fg = global_fg)
            label.pack()
    def add():
        global files,flag
        files += filedialog.askopenfilenames(parent = Win,title=lang["select_files"],filetypes=[(lang["all_files"], "*.*")])
        flag = True if files else False
        refresh_ui()
    def create(files,name):
        if len(name) == 0:
            messagebox.showerror(lang["error"],lang["name_pust"])
        else:
            save_dir = "user_files"
            if not name.endswith(".zip"):
                name += ".zip"
            zip_path = os.path.join(save_dir, name)
            try:
                with zipfile.ZipFile(zip_path, "w") as my_zip:
                    for file_name in files:
                        arcname = os.path.basename(file_name)
                        my_zip.write(file_name, arcname)
                messagebox.showinfo(lang["success"], lang["zip_created"] + str(zip_path))
                reset_variables()
            except Exception as e:
                messagebox.showerror(lang["error"], str(e))
                reset_variables()
    def on_closing():
        global flag_button,flag,files
        files = []
        flag_button = False
        flag = False
        Win.destroy()
    global files,flag
    log_to_file("SVB Archiver launch",start_time_ = start_time_)
    actives_programs.append("SVB Archiver")
    Win = Toplevel(root)
    Win.attributes("-alpha", float(GlobalAlpha))
    Win.config(bg=global_bg)
    Win.title(lang["archiver"])
    Win.geometry("600x300")
    img = Image.open("icons/Archiver.png")
    icon_image = ImageTk.PhotoImage(img)
    Win.iconphoto(False, icon_image)

    static_labels = []

    lbl1 = Label(Win, text=lang["enter_name_for_zip"],bg = global_bg,fg = global_fg)
    lbl1.pack()
    static_labels.append(lbl1)

    name_entry = ctk.CTkEntry(Win,placeholder_text = lang['enter_name_for_zip'])
    name_entry.pack()

    lbl2 = Label(Win, text=lang["select_files_to_arh"],bg = global_bg,fg = global_fg)
    lbl2.pack()
    static_labels.append(lbl2)

    ttk.Button(Win, text=lang["add_files_to_arh"], command=add).pack()
    Win.protocol("WM_DELETE_WINDOW", on_closing)





