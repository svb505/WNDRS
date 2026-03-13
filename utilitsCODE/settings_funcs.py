import logging
import os
import platform
import socket
import psutil
from tkinter import *
import webbrowser
from tkinter import ttk,messagebox
import sqlite3
from PIL import Image, ImageTk
from logtofile import log_to_file,log_system
from crypto_work import load_key,read_encrypted_file
from copy_file_to_folder import copy_file_to_folder
from create_window import create_window
import json
from download_sdk import download_funcs
from readandwrite_to_files import read_file
import customtkinter as ctk
from save_and_load_balance import load_balance,save_balance
from datetime import datetime
from transactions import transactions
from crypto_work import write_encrypted_file
from load_cursor import load_cursor

SYSTEM_LEVEL = 25
logging.addLevelName(SYSTEM_LEVEL, "SYSTEM")
config = {}
tooltip = None

svb_coins = 0

def open_journal(win_p,global_bg,lang,start_time_):
    log_to_file('Journal Action launch',start_time_)
    win = create_window(win_p, lang['journal'], global_bg, 1.0, 600, 500,"icons/interface/jd.png")
    frame = Frame(win)
    frame.pack(expand=True, fill="both")

    scrollbar = Scrollbar(frame)
    scrollbar.pack(side=RIGHT, fill=Y)
    text = Text(frame, yscrollcommand=scrollbar.set)
    text.pack(side=LEFT, expand=True, fill="both")
    scrollbar.config(command=text.yview)

    with open("syst_comp/system_log.log", "r", encoding="utf-8") as f:
        content = f.read()
    text.insert(1.0, content)
    log_to_file('Logs has been inserts',start_time_)
def faq(win_p,lang,global_bg,gl_police):
    Win = create_window(win_p, "FAQ", global_bg, 1.0, 650, 500, "icons/interface/faq.png")
    container = Frame(Win, bg=global_bg)
    container.pack(fill=BOTH, expand=True)
    canvas = Canvas(container, bg=global_bg)
    canvas.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar = Scrollbar(container, orient=VERTICAL, command=canvas.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    frame = Frame(canvas, bg=global_bg)
    canvas.create_window((0, 0), window=frame, anchor="nw")

    with open ("syst_comp/faq.json") as f:
        jsonf = json.load(f)
    questions = jsonf["questionsLocales"]
    responses = jsonf["answersLocales"]

    for i, q in enumerate(questions):
        Label(frame, text=lang[q], font=(gl_police, 10, "bold"), fg="#191970", bg=global_bg).pack(anchor="w", padx=10, pady=2)
        Label(frame, text=lang[responses[i]], font=(gl_police, 10, "bold"), fg="#4682B4", bg=global_bg).pack(anchor="w",
                                                                                                      padx=10, pady=2)

    def on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    canvas.bind_all("<MouseWheel>", on_mousewheel)
def param(version,win_p,lang,start_time_,global_bg,global_fg,gl_police,edition):
    def get_pc_info():
        info = {
            lang["pc-name"]: socket.gethostname(),
            lang["OS"]: "Windoors 52",
            lang["proc"]: platform.processor(),
            lang["arch"]: platform.machine(),
            lang["yader"]: psutil.cpu_count(logical=True),
            lang["ozu"]: round(psutil.virtual_memory().total / (1024 ** 3), 2),
        }
        return info
    def show_info():
        info = get_pc_info()
        text_box.delete("1.0", END)
        for key, value in info.items():
            text_box.insert(END, f"{key}: {value}\n")
        text_box.config(state="disabled")
    def update_user(user_id, new_first_name, new_last_name, new_email):
        """Обновляет данные пользователя по id"""
        cursor.execute("""
               UPDATE users 
               SET first_name = ?, last_name = ?, email = ?
               WHERE id = ?
               """, (new_first_name, new_last_name, new_email, user_id))
        conn.commit()
        log_to_file('Data user has been changed',start_time_)
        log_to_file(f'New name - {new_first_name}',start_time_)
        log_to_file(f'New last name - {new_last_name}',start_time_)
        log_to_file(f'New email - {new_email}',start_time_)
        messagebox.showinfo(lang["success"], lang["data-changet"])
        log_to_file(f'Message {lang["data-changet"]}',start_time_)
    def update():
        log_to_file('Update data user',start_time_)
        win = Toplevel(win_p)
        win.config(bg=global_bg)
        win.geometry("200x150")
        Label(win, text="New " + lang["name"], font=(gl_police, 10), bg=global_bg, fg=global_fg).pack()
        entry_name = ttk.Entry(win)
        entry_name.pack()

        Label(win, text="New " + lang["last-name"], font=(gl_police, 10), bg=global_bg, fg=global_fg).pack()
        entry_lastname = ttk.Entry(win)
        entry_lastname.pack()

        Label(win, text="New " + lang["email"], font=(gl_police, 10), bg=global_bg, fg=global_fg).pack()
        entry_email = ttk.Entry(win)
        entry_email.pack()

        ttk.Button(win, text="Ok", command=lambda: update_user(
            1, entry_name.get(), entry_lastname.get(), entry_email.get()
        )).pack(pady=5)

    log_to_file('Parametrs launch',start_time_)
    decrypted_text = read_encrypted_file("syst_comp/parametrs.bin")
    for line in decrypted_text.strip().splitlines():
        key2, value1 = line.strip().split("=")
        config[key2] = value1
    key = load_key()
    license_kl = read_file("syst_comp/license.bin",'r')

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

    def get_selected_country():
        try:
            conn = sqlite3.connect("configurations.db")
            cur = conn.cursor()
            cur.execute("SELECT country FROM user_settings ORDER BY id DESC LIMIT 1")
            row = cur.fetchone()
            conn.close()
            if edition in ("Professional x64", "Gaming x64", "Professional x32", "Gaming x32"):
                copy_file_to_folder("configurations.db", "backup_data",start_time_)
            return row[0] if row else None
        except Exception as e:
            log_to_file(f"Error getting selected country: {e}",start_time_)
            print(f"Error getting selected country: {e}")
            return None

    country = get_selected_country()

    rom = (config.get("ROM") or "0").strip("GB")
    ram = (config.get("RAM") or "0").strip("GB")
    edit = config.get("EDITION", "N/A")
    arch = config.get("ARCH", "N/A")
    img = Image.open("icons/interface/parametrs.png")
    icon_image = ImageTk.PhotoImage(img)
    win = create_window(win_p, lang['settings'], global_bg, 1.0, 500, 500, "icons/interface/parametrs.png")
    icon_f = None

    try: icon_f = ImageTk.PhotoImage(Image.open(f"icons/flags/{country}.png").resize((60, 44), Image.Resampling.LANCZOS))
    except: pass

    win.iconphoto(False, icon_image)
    frame = LabelFrame(win, text=lang["parametr"], font=(gl_police, 10), bg=global_bg)
    frame.pack(padx=10, pady=10, fill="both", expand=True)

    Label(frame, text=lang["version"] + version, font=(gl_police, 10), bg=global_bg, fg=global_fg).pack()
    Label(frame, text=lang["key"] + license_kl, font=(gl_police, 10), bg=global_bg, fg=global_fg).pack()
    Label(frame, text=lang["name"] + n, font=(gl_police, 10), bg=global_bg, fg=global_fg).pack()
    Label(frame, text=lang["last-name"] + ln, font=(gl_police, 10), bg=global_bg, fg=global_fg).pack()
    Label(frame, text=lang["email"] + e, font=(gl_police, 10), bg=global_bg, fg=global_fg).pack()
    Label(frame, text="Country - " + country, font=(gl_police, 10), bg=global_bg, fg=global_fg).pack()
    if icon_f != None:
        lbl = Label(frame, image=icon_f)
        lbl.image = icon_f
        lbl.pack()
    Label(frame, text="ROM - " + f"{float(rom):.2f} GB", font=(gl_police, 10), bg=global_bg, fg=global_fg).pack()
    Label(frame, text="RAM - " + f"{float(ram):.2f} GB", font=(gl_police, 10), bg=global_bg, fg=global_fg).pack()
    Label(frame, text="Edition - " + edit, font=(gl_police, 10), bg=global_bg, fg=global_fg).pack()
    Label(frame, text=f"{lang['os_arc']} - " + arch, font=(gl_police, 10), bg=global_bg, fg=global_fg).pack()
    text_box = Text(frame, height=12, width=50)
    text_box.pack()
    show_info()
    ttk.Button(frame, text=lang["change_"], command=update).pack(pady=10)
def open_acc(win_p,lang,global_bg,global_fg,gl_police,edition,version,start_time_):
    log_to_file('Show account',start_time_)
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

    def get_selected_country():
        try:
            conn = sqlite3.connect("configurations.db")
            cur = conn.cursor()
            cur.execute("SELECT country FROM user_settings ORDER BY id DESC LIMIT 1")
            row = cur.fetchone()
            conn.close()
            if edition in ("Professional x64", "Gaming x64", "Professional x32", "Gaming x32"):
                copy_file_to_folder("configurations.db", "backup_data",start_time_)
            return row[0] if row else None
        except Exception as e:
            log_to_file(f"Error getting selected country: {e}",start_time_)
            print(f"Error getting selected country: {e}")
            return None

    country = get_selected_country()
    win = create_window(win_p, lang['settings'], global_bg, 1.0, 500, 300, "icons/acc1.png")
    frame = LabelFrame(win, text=lang["parametr"], font=(gl_police, 10), bg=global_bg, fg=global_fg)
    frame.pack(padx=10, pady=10, fill="both", expand=True)
    icon_f = None
    try:
        icon_f = ImageTk.PhotoImage(
            Image.open(f"icons/flags/{country}.png").resize((60, 44), Image.Resampling.LANCZOS))
    except:
        pass
    Label(frame, text=lang["version"] + version, font=(gl_police, 10), bg=global_bg, fg=global_fg).pack()
    Label(frame, text=lang["name"] + n, font=(gl_police, 10), bg=global_bg, fg=global_fg).pack()
    Label(frame, text=lang["last-name"] + ln, font=(gl_police, 10), bg=global_bg, fg=global_fg).pack()
    Label(frame, text=lang["email"] + e, font=(gl_police, 10), bg=global_bg, fg=global_fg).pack()
    Label(frame, text=f"UID: {read_encrypted_file('uid.key')}", font=(gl_police, 10), bg=global_bg, fg=global_fg).pack()
    Label(frame, text="Country - " + country, font=(gl_police, 10), bg=global_bg, fg=global_fg).pack()
    if icon_f != None:
        lbl = Label(frame, image=icon_f)
        lbl.image = icon_f
        lbl.pack()
def open_lic(win_p,lang,global_bg):
    def open_eula():
        try:
            with open("EULA.txt", 'r', encoding="utf-8") as f:
                licnn = f.read()
                f.close()
            return licnn
        except Exception as e:
            print(e)
            return "No EULA in dirrectory"

    win = create_window(win_p, lang['licn'], global_bg, 1.0, 500, 500, "icons/lic.png")
    text = Text(win, wrap="word", height=20, width=60)
    text.pack(padx=10, pady=10)
    text.insert("1.0", open_eula())
    text.config(state="disabled")
def razr(win_p,lang,global_bg,global_fg,gl_police):
    def show_tooltip(event,txt):
        global tooltip
        if tooltip:
            return

        x = event.widget.winfo_rootx() + 20
        y = event.widget.winfo_rooty() + event.widget.winfo_height() + 10

        tooltip = Toplevel()
        tooltip.wm_overrideredirect(True)
        tooltip.wm_geometry(f"+{x}+{y}")

        label = Label(tooltip, text=txt,
                      background="lightyellow", relief="solid", borderwidth=1)
        label.pack(ipadx=5, ipady=2)
    def hide_tooltip(event):
        global tooltip
        if tooltip:
            tooltip.destroy()
            tooltip = None
    def open_link(to):
        if to == "tgk":
            webbrowser.open("https://t.me/developpersvb")
        elif to == "tiktok":
            webbrowser.open("https://www.tiktok.com/@.programmersvb")
        elif to == "boosty":
            webbrowser.open("https://boosty.to/developsvb")
        elif to == 'patreon':
            webbrowser.open('https://www.patreon.com/c/SVB278?fromConcierge=true')
    Win = create_window(win_p, lang['pror'], global_bg, 1.0, 650, 500, "icons/razrab.png")

    def create_labelframe(master, text):
        frame = LabelFrame(master, text=text, bg=global_bg)
        frame.pack(fill="x", padx=10, pady=5)
        return frame
    def create_label(master, text, bold=False):
        if bold:
            Label(master, text=text, font=(gl_police, 10, 'bold'), bg=global_bg, fg=global_fg, wraplength=580,
                  justify="left").pack(anchor="w", padx=10, pady=2)
        else:
            Label(master, text=text, font=(gl_police, 10), bg=global_bg, fg=global_fg, wraplength=580,
                  justify="left").pack(anchor="w", padx=10, pady=2)

    frame = create_labelframe(Win, lang["proraz"])
    create_label(frame, lang["info"])
    create_label(frame, lang["info1"])

    frame1 = create_labelframe(Win, lang["nav"])
    create_label(frame1, lang["znan"] + 'C++ - Middle | Python - Middle | C - Junior | WLangue - Junior', True)

    frame2 = create_labelframe(Win, lang["prog"])
    create_label(frame2, lang["cetp"])
    create_label(frame2, lang["cetp1"])

    frame3 = create_labelframe(Win, lang["cib"])
    create_label(frame3, lang["mycib"])

    btn_frame = Frame(Win, bg=global_bg)
    btn_frame.pack(pady=10)
    tik = ImageTk.PhotoImage(
        Image.open('icons/interface/tiktok.png').resize((24, 24), Image.Resampling.LANCZOS)
    )
    tgk = ImageTk.PhotoImage(
        Image.open("icons/interface/tg.png").resize((24, 24), Image.Resampling.LANCZOS)
    )
    boosty = ImageTk.PhotoImage(
        Image.open("icons/interface/boosty.jpg").resize((24, 24), Image.Resampling.LANCZOS)
    )
    patreon = ImageTk.PhotoImage(
        Image.open("icons/interface/patreon.png").resize((24, 24), Image.Resampling.LANCZOS)
    )
    images = [tik,tgk,boosty,patreon]
    commands = [lambda:open_link("tiktok"),lambda:open_link("tgk"),lambda:open_link("boosty"),
                lambda:open_link("patreon")]
    texts = [lang['tt'],lang['tgk'],lang['boosty'],lang["patreon"]]

    for txt,img,comm in zip(texts,images,commands):
        btn = Button(btn_frame, image=img,command = comm)
        btn.image = img
        btn.pack(side="left", padx=5)
        btn.bind("<Enter>", lambda event, t=txt: show_tooltip(event, txt=t))
        btn.bind("<Leave>", hide_tooltip)

    btn = Button(btn_frame, text=lang["site"], state="disabled")
    btn.pack(side="left", padx=5)
    btn.bind("<Enter>", lambda event:show_tooltip(event,lang["func_in_dev"]))
    btn.bind("<Leave>", hide_tooltip)
def open_errors_codes(win_p,lang,global_bg,global_fg,errors,gl_police):
    win = create_window(win_p, lang['Inf-er'], global_bg, 1.0, 550, 300, "icons/interface/errors.png")
    Label(win, text=errors[0] + " - " + lang["nofile"], font=(gl_police, 10), fg=global_fg, bg=global_bg).pack()
    Label(win, text=errors[1] + " - " + lang["nofolder"], font=(gl_police, 10), fg=global_fg, bg=global_bg).pack()
    Label(win, text=errors[2] + " - " + lang["nodata"], font=(gl_police, 10), fg=global_fg, bg=global_bg).pack()
    Label(win, text=errors[3] + " - " + lang["nomus"], font=(gl_police, 10), fg=global_fg, bg=global_bg).pack()
    Label(win, text=errors[4] + " - " + lang["nosms"], font=(gl_police, 10), fg=global_fg, bg=global_bg).pack()
    Label(win, text=errors[5] + " - " + lang["noima"], font=(gl_police, 10), fg=global_fg, bg=global_bg).pack()
def show_hotkeys(win_p,lang,global_bg,global_fg,gl_police):
    win = Toplevel(win_p)
    win.config(bg=global_bg)
    win.title(lang["hotkeys"])
    img = Image.open("icons/interface/hotkey.png")
    icon_image = ImageTk.PhotoImage(img)
    win.iconphoto(False, icon_image)
    win.geometry("550x300")
    win.focus_set()
    Label(win, text=f"Ctrl + 1/Ctrl + Shift + 1 - {lang['volume_up']}", font=(gl_police, 10), fg=global_fg, bg=global_bg).pack()
    Label(win, text=f"Ctrl + 2/Ctrl + Shift + 2 - {lang['volume_down']}", font=(gl_police, 10), fg=global_fg, bg=global_bg).pack()
    Label(win, text=f"Ctrl + 3/Ctrl + Shift + 3 - {lang['mute']}", font=(gl_police, 10), fg=global_fg, bg=global_bg).pack()
    Label(win, text=f"Ctrl + Shift + A - {lang['open_ecran_block']}", font=(gl_police, 10), fg=global_fg,bg=global_bg).pack()
def others_dev_projects(win_p,lang,global_bg,global_fg,gl_police,GlobalAlpha):
    Win = create_window(win_p,lang["others_dev_projects"],global_bg,float(GlobalAlpha),500,400,"icons/interface/others.png")

    frm = Frame(Win,bg = global_bg)
    frm.pack()

    img = ImageTk.PhotoImage(Image.open(f"icons/logo.png").resize((120, 120), Image.Resampling.LANCZOS))

    images = [img]
    labels = [lang["svbengine_dicsr"]]

    for img,lbl in zip(images,labels):
        labelIcon = Label(frm,image = img,bg = global_bg,fg = global_fg)
        labelIcon.image = img
        labelIcon.pack()

        Label(frm,text = lbl,bg = global_bg,fg = global_fg,font = (gl_police,13)).pack()

        ttk.Button(frm,text = lang["download"],command = lambda:download_funcs(Win,lang,"engine",global_bg,GlobalAlpha)).pack()
def set_password(win_p,root,lang,start_time_,global_bg,global_fg,gl_police,GlobalAlpha):
    log_to_file('Set password', start_time_=start_time_)
    def ok():
        log_to_file(f'Set password {en.get()}', start_time_=start_time_)
        conn = sqlite3.connect("password.db")
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS password (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                password TEXT
            )
        ''')
        conn.commit()

        cursor.execute('''
            INSERT INTO password (password) VALUES (?)
        ''', (en.get(),))
        conn.commit()
        conn.close()
        messagebox.showinfo(lang["success"], lang["password_set"], parent=winn)
        log_to_file(f'Message {lang["password_set"]}', start_time_=start_time_)

    winn = Toplevel(win_p)
    winn = create_window(root, lang["settings"], global_bg, float(GlobalAlpha), 500, 300, "icons/interface/psw.png")
    lab = Label(winn, text=lang["enter_password"], font=(gl_police, 10), bg=global_bg, fg=global_fg)
    lab.pack()
    en = ctk.CTkEntry(winn, placeholder_text=lang['holder_password'])
    en.pack()
    btn = ttk.Button(winn, text=lang["Apply"], command=ok)
    btn.pack()
def change(win_p,lang,start_time_,global_bg,global_fg,GlobalAlpha,invisible_pass):
    def ch():
        log_system("Connect to password.db", start_time_)
        conn = sqlite3.connect("password.db")
        cursor = conn.cursor()

        cursor.execute('''
            SELECT password FROM password
        ''')
        stored_password = cursor.fetchone()
        conn.close()

        if stored_password and en.get() == stored_password[0]:
            log_to_file("Password correct", start_time_=start_time_)
            conn = sqlite3.connect("password.db")
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE password SET password = ?
            ''', (en1.get(),))
            conn.commit()
            conn.close()
            messagebox.showinfo(lang["success"], lang["password_changed"], parent=win)
            log_to_file('Password updated', start_time_=start_time_)
            log_to_file(f'Message {lang["password_changed"]}', start_time_=start_time_)
        else:
            messagebox.showerror(lang["error"], lang["incorrect_password"], parent=win)
            log_to_file('Password incorrect', level="error", start_time_=start_time_)
            log_to_file(f'Message: {lang["incorrect_password"]}', level="error", start_time_=start_time_)

    log_to_file('Change password', start_time_=start_time_)
    global gl_police
    win = create_window(win_p, '', global_bg, float(GlobalAlpha), 500, 300, "icons/interface/psw.png")
    win.title(lang["settings"])
    lab = Label(win, text=lang['enter_old_password'], font=(gl_police, 10), bg=global_bg, fg=global_fg)
    lab.pack()
    en = ttk.Entry(win)
    if invisible_pass: en.config(show="*")
    en.pack()
    lab = Label(win, text=lang['enter_new_password'], font=(gl_police, 10), bg=global_bg, fg=global_fg)
    lab.pack()
    en1 = ttk.Entry(win)
    if invisible_pass:  en1.config(show="*")
    en1.pack()
    btn = ttk.Button(win, text=lang["Apply"], command=ch)
    btn.pack()
def cr(win,start_time_,lang):
    global svb_coins
    svb_coins = load_balance(start_time_)
    if svb_coins > 1000:
        if messagebox.askyesnocancel("", lang["pay_cursor-"], parent=win):
            log_to_file(f"User accept: {lang['pay_cursor-']}", start_time_=start_time_)
            svb_coins -= 1000
            transactions("-1.000 SVb Coins" + f" {datetime.now()}", start_time_)
            log_to_file("SVB Coins -= 1000", start_time_=start_time_)
            save_balance(svb_coins,start_time_)
            log_to_file("Balance saved", start_time_=start_time_)
            try:
                write_encrypted_file("cr.cfg", "True")
            except Exception as e:
                log_to_file(str(e), level='error', start_time_=start_time_)
            load_cursor(start_time_)
    else:
        log_to_file(f"User refuse: {lang['pay_cursor-']}", start_time_=start_time_)
        messagebox.showerror(lang["error"], lang["no_svb"], parent=win)
        log_to_file(f"Message: {lang['no_svb']}", level="warning", start_time_=start_time_)
def delete_password(win,lang,global_bg,start_time_,GlobalAlpha):
    def check_p(en):
        conn = sqlite3.connect("password.db")
        cursor = conn.cursor()
        cursor.execute('''
                    SELECT password FROM password
                ''')
        stored_password = cursor.fetchone()
        conn.close()

        if stored_password and stored_password[0] == en:
            log_to_file("Password correct", start_time_=start_time_)

            conn = sqlite3.connect("password.db")
            cursor = conn.cursor()
            cursor.execute('''
                                DELETE FROM password
                            ''')
            conn.commit()
            conn.close()

            if os.path.exists("password.db"):
                os.remove("password.db")
                log_to_file("Password database file deleted", start_time_=start_time_)
                messagebox.showinfo(lang["success"], lang["password_deleted"], parent=w)
                log_to_file(f'Message {lang["password_deleted"]}', start_time_=start_time_)
            else:
                messagebox.showerror(lang["error"], lang["password_file_not_found"], parent=w)
                log_to_file("Error: password.db file not found", level="error", start_time_=start_time_)
        else:
            messagebox.showerror(lang['error'], lang["incorrect_password"], parent=w)
            log_to_file("Password incorrect", level="error", start_time_=start_time_)

    log_system("Connect to password.db", start_time_)
    w = create_window(win, "s", global_bg, float(GlobalAlpha), 400, 300, "icons/interface/psw.png")
    Label(w, text=lang["ent_ps"]).pack()
    en = ctk.CTkEntry(w, placeholder_text=lang["holder_password"])
    en.pack()
    btn_delete = ttk.Button(w, text=lang["Delete_password"] + "🔓", command=lambda: check_p(en.get()))
    btn_delete.pack()
def on(win,lang):
    write_encrypted_file("stexc.wndrs", 'TRUE')
    messagebox.showinfo(lang["success"], lang["on-back-true"], parent=win)
def off(win,lang):
    write_encrypted_file("stexc.wndrs", 'FALSE')
    messagebox.showinfo(lang["success"], lang["off-back-true"], parent=win)
