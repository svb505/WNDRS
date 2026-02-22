from tkinter import *
from tkinter import ttk,messagebox
from datetime import datetime, timedelta
from PIL import Image, ImageTk
from crypto_work import write_encrypted_file
import os

def control_window(root,lang,actives_programs,global_bg,global_fg):
    actives_programs.append('activity control')
    def apply(date,min):
        date.strip(f" {lang['day']}")
        if min.isdigit():
            days_to_wait = int(date.split()[0])  # берем число (1,2,3...)
            unblock_time = datetime.now() + timedelta(days=days_to_wait)

            # записываем файлы
            write_encrypted_file("syst_comp/control_nxt_date.cfg",
                                 unblock_time.strftime("%d-%m-%Y %H:%M:%S"))
            write_encrypted_file("syst_comp/updation_days.cfg", str(date))
            write_encrypted_file("syst_comp/max_minutes.cfg", str(min))
            messagebox.showinfo(lang["success"],lang["control_applyed"])
        else:
            messagebox.showerror(lang["error"],lang["invalid_minutes"])
    def disable():
        if os.path.exists("syst_comp/control_nxt_date.cfg"):
            os.remove("syst_comp/control_nxt_date.cfg")
        if os.path.exists("syst_comp/updation_days.cfg"):
            os.remove("syst_comp/updation_days.cfg")
        if os.path.exists("syst_comp/max_minutes.cfg"):
            os.remove("syst_comp/max_minutes.cfg")
        messagebox.showinfo(lang["success"],lang["control_disabled"])
    Win = Toplevel(root)
    Win.geometry('500x400')
    Win.title(lang["activity_control"])
    Win.config(bg = global_bg)
    img = Image.open("icons/interface/activity.png")
    icon_image = ImageTk.PhotoImage(img)
    Win.iconphoto(False, icon_image)

    Label(Win,text = lang["activity_control"],font = ("Arial",20,"bold"),fg = 'red',bg=global_bg).pack()

    Label(Win, text=lang["date_updation"], font=("Arial", 20, "bold"), fg=global_fg, bg=global_bg).pack()
    date_upd = ttk.Combobox(Win,values=[f"1 {lang['day']}",f"2 {lang['day']}",f"3 {lang['day']}",f"4 {lang['day']}",
                                        f"5 {lang['day']}",f"6 {lang['day']}",f"7 {lang['day']}"])
    date_upd.pack()


    Label(Win, text=lang["activity_minutes"], font=("Arial", 20, "bold"), fg=global_fg, bg=global_bg).pack()

    minutes = ttk.Entry(Win)
    minutes.pack()

    ttk.Button(Win,text = lang["apply_control"],command = lambda:apply(date_upd.get(),minutes.get())).pack()
    ttk.Button(Win,text = lang["disable_control"],command=disable).pack()


