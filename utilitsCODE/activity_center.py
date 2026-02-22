from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import time
from github import Github
from load_env import load_env
import os
import base64
import sqlite3

load_env()

token = os.getenv('TOKEN_FOR_USERS')
repo_name = os.getenv('STAT_REPO')
def return_user_info():
    conn = sqlite3.connect("configurations.db")
    cursor = conn.cursor()

    cursor.execute("""
                           CREATE TABLE IF NOT EXISTS users (
                               id INTEGER PRIMARY KEY AUTOINCREMENT,
                               first_name TEXT,
                               last_name TEXT,
                               email TEXT
                           )
                           """)
    conn.commit()

    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    if users:
        user = users[0]
        n, ln, e = user[1], user[2], user[3]
    else:
        n = ln = e = "Unknown"
    return n,ln,e
def get_number():
    g = Github(token)
    repo = g.get_repo(repo_name)
    n, ln, e = return_user_info()
    file_content = repo.get_contents(f"time_{e}.txt")
    decoded_content = base64.b64decode(file_content.content).decode("utf-8")
    number = int(decoded_content.strip())
    return number
def activity_center(root,lang,global_bg,global_fg,start_time_):
    def update_current_time(start_time_):
        elapsed = time.time() - start_time_
        current_lbl.config(text=f"{lang['current_seans']}: {int(elapsed)} {lang['sec']}")
        Win.after(1000, lambda: update_current_time(start_time_))

    Win = Toplevel(root)
    Win.title(lang["activity_center"])
    Win.geometry("600x500")
    img = Image.open("icons/interface/activity.png")
    icon_image = ImageTk.PhotoImage(img)
    Win.iconphoto(False, icon_image)
    num_sec = get_number()
    num_m = num_sec / 60
    num_h = (num_sec / 60) / 60

    time_frm = Frame(Win)
    time_frm.pack()
    system_frm = Frame(Win)
    system_frm.pack()

    current_lbl = Label(time_frm, text=f"{lang['current_seans']}: 0", fg=global_fg, bg=global_bg, font=("Arial", 14))
    current_lbl.pack()
    Label(time_frm, text=lang['provedeno_v'], fg=global_fg, bg=global_bg, font=("Arial", 19, "bold")).pack()

    Label(time_frm,
          text=f"{lang['time_in_sec']}: {num_sec} | {lang['time_in_m']}: {int(num_m)} | {lang['time_in_h']}: {num_h:.1f}",
          fg=global_fg, bg=global_bg).pack()
    update_current_time(start_time_)

    Label(system_frm, text=f"{lang['antvrs']} - {lang['active']}", fg='green', bg=global_bg, font=("Arial", 12)).pack()