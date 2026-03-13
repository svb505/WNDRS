import time
from tkinter import *
from create_window import create_window
from block_user import block_user
from crypto_work import read_encrypted_file

def load_activity_control():
    try:
        max_minutes = int(read_encrypted_file("syst_comp/max_minutes.cfg"))
    except:
        max_minutes = None

    try:
        next_date = read_encrypted_file("syst_comp/control_nxt_date.cfg")
    except:
        next_date = None

    try:
        updation_days = read_encrypted_file("syst_comp/updation_days.cfg")
    except:
        updation_days = None

    return max_minutes, next_date, updation_days
def block_ecran_no_act(timeoutEcran,root,lang,GlobalAlpha):
    Win = create_window(root, "", '#170E0E', float(GlobalAlpha), 100, 100, None, True)
    Label(Win,
          text=f"{lang['you_bee_inactivited']} {timeoutEcran // 1000} {lang['sec']}\n{lang['press_any_key_to_continue']}",
          bg='#170E0E', fg="white", font=("Arial", 40, "bold")).pack()
    Win.bind_all("<KeyPress>", lambda event: Win.destroy())
def check_activity_limit(root,lang,start_time_):
    max_minutes, next_date, upd_days = load_activity_control()
    if max_minutes:
        elapsed_minutes = int((time.time() - start_time_) / 60)
        if elapsed_minutes >= max_minutes:
            messagebox.showwarning("Time limit", lang["limit!"])
            block_user(root, lang)
    root.after(60000, lambda:check_activity_limit(root,lang,start_time_))
