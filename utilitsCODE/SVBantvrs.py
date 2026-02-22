import webbrowser
from datetime import datetime
import random
from tkinter import *
from tkinter import ttk, messagebox, font,scrolledtext
from random import choice, randint
import os
from plyer import notification
import time
import sqlite3
import platform
import psutil
from send_email import send_email
from dateutil.relativedelta import relativedelta
from PIL import Image, ImageTk
from crypto_work import write_encrypted_file,read_encrypted_file
from logtofile import log_to_file
from send_email_template import send
from transactions import transactions
from create_window import create_window

viruses = []
names = ["Virus","Trojan32"]
name_virus = ""
known_files = ["sh.dat", "t00r.dat", "001.dat"]
passw = ""
kl = ""
DIR = "syst_comp/svbantivirus"
progress_value = 0
progress_prob = 0
ugr = 0
a = 0
count = 0
running = False
display_label = None
virus = False
progress_bar = None
progress_bar_prob = None
ug_label = None
kl = False
security = "Включена"
keylic = ""
prov = "1"
filles = "1"
supkl1 = "34765"
supkl2 = "35468"
supkl3 = "98001"
supkl4 = "01010"
supkl5 = "77707"
supkl6 = "11100"
supkl7 = "12345"
supkl8 = "01234"
supkl9 = "42310"
supkl10 = "12120"
keys = [supkl1, supkl2, supkl3, supkl4, supkl5, supkl6, supkl7, supkl8, supkl9, supkl10]
contenttt = ""
svb_coins = 0

def svb_ant(root,lang,start_time_,svb_coins,GlobalAlpha,global_bg):
    global contenttt,keys,keylic,kl
    def delete_vrs(path):
        total_path = path
        if os.path.exists(total_path):
            os.remove(total_path)
            messagebox.showinfo(lang['success'], lang["virus_deleted"],parent = Win)
        else:
            messagebox.showwarning(lang['warning'], lang['path_not_exists'],parent = Win)
    def scan_folder():
        viruses.clear()
        scanned_files_text.delete("1.0", END)

        folder_selected = os.getcwd()  # 📁 Текущая директория

        file_paths = []
        for dirpath, _, files in os.walk(folder_selected):
            for file in files:
                file_path = os.path.join(dirpath, file)
                file_paths.append(file_path)

        progress_bar.config(mode="determinate", maximum=len(file_paths))

        for i, path in enumerate(file_paths):
            scanned_files_text.insert(END, path + "\n")
            scanned_files_text.see(END)
            scanned_files_text.update()

            progress_bar['value'] = i
            Win.update_idletasks()

            if os.path.basename(path) in known_files:
                viruses.append(path)
                log_to_file(f"Virus (known file) found: {path}", start_time_=start_time_)

                try:
                    notification.notify(
                        title=lang["virus_detected"],
                        message=f"{lang['virus_detected']}: {path}",
                        timeout=5
                    )
                except Exception as e:
                    log_to_file(f"Notification error: {e}", level="error", start_time_=start_time_)

        if viruses:
            messagebox.showwarning(lang["virus_detected"], "\n".join(viruses),parent = Win)
            w = create_window(root, "Antivirus", global_bg, float(GlobalAlpha), 600, 300)
            vrs_type = ""
            Label(w, text=f"{lang['virus_detected']}", font=("Arial", 13, "bold"), fg="black").pack()
            Label(w, text=f"{lang['vrs_path']}: {viruses[0]}", font=("Arial", 13, "bold"), fg="red").pack()
            Label(w, text=f"{lang['vrs_type']}: {vrs_type}", font=("Arial", 13, "bold"), fg="red").pack()
            ttk.Button(w, text=lang["delete_virus"], command=lambda: delete_vrs(viruses[0])).pack()
        else:
            messagebox.showinfo(lang["security"], lang["file_not_found"],parent = Win)
    version = "v.3.2.01b(BETA)"
    svb_coins = svb_coins
    Win = Tk()
    Win.configure(bg='darkblue')
    Win.title(f"SVB AntiVirus - {version}")
    Win.geometry("800x600")
    Win.resizable(False, False)
    config = {}
    icon_image = PhotoImage(file="icons/SVB.png")
    try:
        with open(f"{DIR}/status.bin", "r") as file:
            contenttt = file.read()
            file.close()
    except:
        pass
    style1 = ttk.Style()
    style1.configure("Red1.TButton", background="darkred", foreground="red")
    style2 = ttk.Style()
    style2.configure("Blue1.TButton", background="darkblue", foreground="blue")
    style3 = ttk.Style()
    style3.configure("Violet1.TButton", background="#4B0082", foreground="#4B0082")
    style4 = ttk.Style()
    style4.configure("Violet2.TButton", background="#800080", foreground="#800080")
    fontPremium = ("Arial", 20, "bold")
    font_prem = ("Arial", 20, "bold")
    font_prey = ("Arial", 10)

    conn = sqlite3.connect(f'{DIR}/date_antvrss.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS dates (
            id INTEGER PRIMARY KEY,
            year INTEGER,
            month INTEGER,
            day INTEGER
        )
    ''')

    cursor.execute("SELECT * FROM dates")
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO dates (year, month, day) VALUES (?, ?, ?)", (2025, 1, 5))
        conn.commit()
    conn.close()

    def load_target_date():
        conn = sqlite3.connect(f'{DIR}/date_antvrss.db')
        cursor = conn.cursor()
        cursor.execute("SELECT year, month, day FROM dates ORDER BY id LIMIT 1")
        row = cursor.fetchone()
        conn.close()
        if row:
            return datetime(row[0], row[1], row[2]).date()
        return None
    def change_date():
        def okay():
            messagebox.showinfo(lang['success'], lang["you_prod_licence"],parent = Win)

            current_target = load_target_date()
            print(current_target)

            new_date = current_target + relativedelta(months=+6)
            global target_date
            target_date = new_date
            print(new_date)
            update_target_date(new_date)


        def prover(passw, Plle):
            if passw == Plle.get():
                okay()
            else:
                messagebox.showerror(lang['error'], lang["invalid_code"],parent = Win)
        def prodl(pole4):
            global passw
            carantinn_window = create_window(root,lang["activ_code"],global_bg,float(GlobalAlpha),300,250)
            carantinn_window.resizable(False, False)

            passw = ""
            for i in range(4):
                for j in range(4):
                    passw += random.choice(list('0123456789ABCDEFGHIJKLMNOPQRSTUVWYZ'))
                if i < 3:
                    passw += "-"
            receiver_email = pole4.get()
            subject = lang["activ_code"]
            html_message = f"""
            <div style="
                font-family: Arial, sans-serif;
                background: linear-gradient(135deg, #f5f7fa, #e4ebf1);
                border: 1px solid #d0d7de;
                border-radius: 12px;
                padding: 20px;
                max-width: 400px;
                margin: 10px auto;
                text-align: center;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            ">
                <h2 style="
                    color: #2c3e50;
                    font-size: 22px;
                    margin-bottom: 12px;
                ">
                    {lang['your_antvrs_code']}
                </h2>
                <p style="
                    font-size: 20px;
                    font-weight: bold;
                    color: #2980b9;
                    margin: 0;
                ">
                    {passw}
                </p>
            </div>
            """

            key_bytes = passw.encode('utf-8')
            if os.path.exists(f"{DIR}/licence_key.bin"):
                write_encrypted_file(f"{DIR}/licence_key.bin",key_bytes)
            send_email(to = str(receiver_email),subject = subject,
                       html = html_message)

            Lbl = Label(carantinn_window, text=lang["enter_antvrs_code"])
            Lbl.pack()
            Plle = ttk.Entry(carantinn_window)
            Plle.pack()

            Btn = ttk.Button(carantinn_window, text=lang["send"], command=lambda: prover(passw, Plle))
            Btn.pack()

        messagebox.showwarning(lang["srok_ist1"],
                                lang["srok_ist2"],parent = Win)
        carantinnn_window = create_window(Win,lang["prodl_licence"],global_bg,float(GlobalAlpha),400,250)
        carantinnn_window.resizable(False, False)

        lbl1 = Label(carantinnn_window, text=lang["enter_card_num"])
        lbl1.pack()
        pole1 = ttk.Entry(carantinnn_window, width=20)
        pole1.pack()
        lbl2 = Label(carantinnn_window, text=lang['enter_srok_deis'])
        lbl2.pack()
        pole2 = ttk.Entry(carantinnn_window, width=20)
        pole2.pack()

        lbl3 = Label(carantinnn_window, text=lang["enter_cvv"])
        lbl3.pack()
        pole3 = ttk.Entry(carantinnn_window, width=20)
        pole3.pack()

        lbl4 = Label(carantinnn_window, text=lang["enter_email"])
        lbl4.pack()
        if not os.path.exists("user.bin"):
            pole4 = ttk.Entry(carantinnn_window, width=20)
            pole4.pack()
        else:
            pole4 = ttk.Entry(carantinnn_window, width=20)
            pole4.pack()
            with open(f"{DIR}/user.bin", "rb") as f:
                for line in f:
                    key1, value = line.decode("utf-8").strip().split("=")
                    config[key1] = value
            user_email = config.get("Email")
            print(config)
            pole4.insert(0, user_email)

        style1 = ttk.Style()
        style1.configure("Green1.TButton", background="green", foreground="darkgreen")
        btn = ttk.Button(carantinnn_window, text=lang['prodl'], style="Green1.TButton", command=lambda: prodl(pole4))
        btn.pack()
        carantinnn_window.grab_set()

    target_date = load_target_date()
    print(target_date)
    current_date = datetime.now().date()
    print(current_date)
    if current_date >= target_date:
        change_date()
    def securr():
        with open(f"{DIR}/security.bin", "r") as file:
            content = file.read()
            if "Yes" in content:
                title_label = Label(frame1, text=lang['your_pc_in_security'], font=("Arial", 16), bg="green")
                title_label.grid(row=0, column=0)
            elif "Off" in content:

                title_label = Label(frame1, text=lang['security_offed'], font=("Arial", 16), bg="orange")
                title_label.grid(row=0, column=0)
            else:
                title_label = Label(frame1, text=lang['viruses:yes'], font=("Arial", 16), bg="red")
                title_label.grid(row=0, column=0)
        proverka_userdata()
    def update_target_date(new_date):
        conn = sqlite3.connect(f'{DIR}/date_antvrss.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE dates SET year = ?, month = ?, day = ? WHERE id = 1",
                       (new_date.year, new_date.month, new_date.day))
        conn.commit()
        conn.close()

    pas = ""
    for i in range(4):
        for j in range(4):
            pas += random.choice(list('0123456789ABCDEFGHIJKLMNOPQRSTUVWYZ'))
        if i < 3:
            pas += "-"

    with open(f"{DIR}/st.bin", "r") as file:
        content = file.read()
        if content == "True":
            kl = True
        file.close()
    if kl:
        pass
    else:
        write_encrypted_file(f"{DIR}/st.bin",'True')
        with open(f"{DIR}/kluch.txt", "w") as file:
            file.write(pas)
            file.close()
    def func():
        pass
    def update_progress_bar():
        global progress_value
        if progress_value < 100:
            progress_value += 0.6
            progress_bar['value'] = progress_value
            Win.after(10000, update_progress_bar)
    def drav():
        messagebox.showerror(lang["drivers"], lang["drivers_upd_no"],parent = Win)
    def csh():
        messagebox.showinfo(lang['cesh'], lang['clean_cesh...'],parent = Win)
        time.sleep(6)
        messagebox.showinfo(lang['cesh'], lang["cesh_cleanuped"],parent = Win)
    def seti():
        messagebox.showinfo(lang["internet_security"], lang['secur_int_enable'],parent = Win)
    def sitt():
        messagebox.showinfo(lang["site_prov"], lang["sites_provTRUE"],parent = Win)
    def rek():
        messagebox.showerror(lang["addvert"], lang["rekl_otkl"],parent = Win)
    def center_child(window, parent):
        parent.update_idletasks()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()
        parent_x = parent.winfo_x()
        parent_y = parent.winfo_y()

        child_width = window.winfo_width()
        child_height = window.winfo_height()

        x = parent_x + parent_width // 2 - child_width // 2
        y = parent_y + parent_height // 2 - child_height // 2

        window.geometry(f'{child_width}x{child_height}+{x}+{y}')
    def dismiss(window):
        window.grab_release()
        window.destroy()
    def carantin():
        carantin_window = create_window(Win,lang["carantin"],global_bg,float(GlobalAlpha),250,250)

        carantin_window.resizable(False, False)
        center_child(carantin_window, Win)
        carantin_window.protocol("WM_DELETE_WINDOW",
                                 lambda: dismiss(carantin_window))
        nad = Label(carantin_window, text=lang["carantinNO"])
        nad.pack()
    nadp_var = StringVar()
    if os.path.exists(f"{DIR}/label.bin"):
        prem_l = read_encrypted_file(f"{DIR}/label.bin").decode("utf-8").strip()
        Premiump = False
        Premiumlabel = Label(text=prem_l, font=fontPremium, fg="orange")
    try:
        with open(f"{DIR}/status.bin", "r") as file:
            content = file.read()
            if "active" in content:
                Premiumlabel = Label(text=prem_l, font=fontPremium, fg="orange")
            elif "Gold" in content:
                Premiumlabel = Label(text=prem_l, font=fontPremium, fg="#00BFFF")
    except FileNotFoundError:
        pass

    def delete_user():
        def confirmation(pole1):
            if passw == pole1:
                if os.path.exists("user.bin"):
                    os.remove("user.bin")
                    print(f"Файл user.bin удалён.")
                    messagebox.showinfo(lang['deleting_account'], lang["account_delete_w_success"],parent = Win)
                    proverka_userdata()
                else:
                    print("Файл не найден.")
            else:
                messagebox.showerror(lang['error'], lang["invalid_code"],parent = Win)

        passw = str(randint(10000, 100000))
        with open(f"{DIR}/user.bin", "rb") as f:
            for line in f:
                key1, value = line.decode("utf-8").strip().split("=")
                config[key1] = value
        user_email = config.get("Email")
        receiver_email = user_email
        subject = lang["podtverzh"]
        html_message =html_message = f"""
<div style="
    font-family: Arial, sans-serif;
    background: linear-gradient(135deg, #f5f7fa, #e4ebf1);
    border: 1px solid #d0d7de;
    border-radius: 12px;
    padding: 20px;
    max-width: 400px;
    margin: 10px auto;
    text-align: center;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
">
    <h2 style="
        color: #2c3e50;
        font-size: 22px;
        margin-bottom: 12px;
    ">
        {lang['your_code']}
    </h2>
    <p style="
        font-size: 20px;
        font-weight: bold;
        color: #2980b9;
        margin: 0;
    ">
        {passw}
    </p>
</div>
"""

        send_email(to=str(receiver_email), subject=subject,
                   html=html_message)


        carantinnn_window = create_window(Win,lang["deleting_account"],global_bg,float(GlobalAlpha),400,250)

        carantinnn_window.resizable(False, False)
        center_child(carantinnn_window, Win)
        carantinnn_window.protocol("WM_DELETE_WINDOW", lambda: dismiss(carantinnn_window))
        lbl1 = Label(carantinnn_window, text=lang["enter_code"])
        lbl1.pack()
        pole1 = ttk.Entry(carantinnn_window, width=20)
        pole1.pack()
        btn = ttk.Button(carantinnn_window, text="Ok", command=lambda: confirmation(pole1.get()))
        btn.pack()
    def changelab():
        premium = ""
        if nadp_var.get() == "1":
            Premiumlabel.config(text="★Premium★", font=fontPremium, fg="orange")
            premium = "★Premium★"
        elif nadp_var.get() == "2":
            Premiumlabel.config(text="☻Premium☻", font=fontPremium, fg="orange")
            premium = "☻Premium☻"
        elif nadp_var.get() == "3":
            Premiumlabel.config(text="⍟Premium⍟", font=fontPremium, fg="orange")
            premium = "⍟Premium⍟"
        elif nadp_var.get() == "4":
            Premiumlabel.config(text="$Premium$", font=fontPremium, fg="orange")
            premium = "$Premium$"
        elif nadp_var.get() == "5":
            Premiumlabel.config(text="↯Premium↯", font=fontPremium, fg="orange")
            premium = "↯Premium↯"
        elif nadp_var.get() == "6":
            Premiumlabel.config(text="♔Premium♔", font=fontPremium, fg="orange")
            premium = "♔Premium♔"
        elif nadp_var.get() == "8":
            Premiumlabel.config(text="✿Premium✿", font=fontPremium, fg="orange")
            premium = "✿Premium✿"
        elif nadp_var.get() == "9":
            Premiumlabel.config(text="♜Premium♜", font=fontPremium, fg="orange")
            premium = "♜Premium♜"
        elif nadp_var.get() == "10":
            Premiumlabel.config(text="♞Premium♞", font=fontPremium, fg="orange")
            premium = "♞Premium♞"
        elif nadp_var.get() == "11":
            Premiumlabel.config(text="♥Premium♥", font=fontPremium, fg="orange")
            premium = "♥Premium♥"
        elif nadp_var.get() == "12":
            Premiumlabel.config(text="♬Premium♬", font=fontPremium, fg="orange")
            premium = "♬Premium♬"
        else:
            Premiumlabel.config(text="☄Premium☄", font=fontPremium, fg="orange")
            premium = "☄Premium☄"
        config_data = premium
        write_encrypted_file(f"{DIR}/label.bin", config_data)
    def changelabGold():
        premium = ""
        if nadp_var.get() == "1":
            Premiumlabel.config(text="★Premium Gold★", font=fontPremium, fg="#00BFFF")
            premium = "★Premium Gold★"
        elif nadp_var.get() == "2":
            Premiumlabel.config(text="☻Premium Gold☻", font=fontPremium, fg="#00BFFF")
            premium = "☻Premium Gold☻"
        elif nadp_var.get() == "3":
            Premiumlabel.config(text="⍟Premium Gold⍟", font=fontPremium, fg="#00BFFF")
            premium = "⍟Premium Gold⍟"
        elif nadp_var.get() == "4":
            Premiumlabel.config(text="$Premium Gold$", font=fontPremium, fg="#00BFFF")
            premium = "$Premium Gold$"
        elif nadp_var.get() == "5":
            Premiumlabel.config(text="↯Premium Gold↯", font=fontPremium, fg="#00BFFF")
            premium = "↯Premium Gold↯"
        elif nadp_var.get() == "6":
            Premiumlabel.config(text="♔Premium Gold♔", font=fontPremium, fg="#00BFFF")
            premium = "♔Premium Gold♔"
        elif nadp_var.get() == "8":
            Premiumlabel.config(text="✿Premium Gold✿", font=fontPremium, fg="#00BFFF")
            premium = "✿Premium Gold✿"
        elif nadp_var.get() == "9":
            Premiumlabel.config(text="♜Premium Gold♜", font=fontPremium, fg="#00BFFF")
            premium = "♜Premium Gold♜"
        elif nadp_var.get() == "10":
            Premiumlabel.config(text="♞Premium Gold♞", font=fontPremium, fg="#00BFFF")
            premium = "♞Premium Gold♞"
        elif nadp_var.get() == "11":
            Premiumlabel.config(text="♥Premium Gold♥", font=fontPremium, fg="#00BFFF")
            premium = "♥Premium Gold♥"
        elif nadp_var.get() == "12":
            Premiumlabel.config(text="♬Premium Gold♬", font=fontPremium, fg="#00BFFF")
            premium = "♬Premium Gold♬"
        else:
            Premiumlabel.config(text="☄Premium Gold☄", font=fontPremium, fg="#00BFFF")
            premium = "☄Premium Gold☄"

        config_data = premium
        write_encrypted_file(f"{DIR}/label.bin", config_data)
    def opfile():
        try:
            with open(f"{DIR}/status.bin", "r") as file:
                content = file.read()
                if "active" in content:
                    act()
                elif "Gold" in content:
                    act()
        except FileNotFoundError:
            pass
    def act():
        global Premiumlabel
        Premiumlabel.grid(row=2, column=0)
    def supPremium():
        global Premiump
        write_encrypted_file(f"{DIR}/status.bin", 'Gold')
        write_encrypted_file(f"{DIR}/label.bin", "★Premium Gold★")
        Premiump = True
        messagebox.showinfo(lang["success"],lang["you_got_superPREM"],parent = Win)
        act()
    def podp():
        try:
            with open(f"{DIR}/status.bin", "r") as file:
                content = file.read()
                if "active" in content:

                    ug = Label(inf_frame, text="Premium  Подписка: Активна")
                    ug.pack()
                if "Gold" in content:
                    i
                    ug = Label(inf_frame, text="Premium  Подписка: Активна Gold Premium")
                    ug.pack()
        except FileNotFoundError:

            ug = Label(inf_frame, text=lang["prem:not"])
            ug.pack()
    def pay():
        def prover(passw, Plle):
            if passw == Plle.get():
                pay1()
            elif Plle.get() == supkl1 or Plle.get() == supkl2 or Plle.get() == supkl3 or Plle.get() == supkl4 or Plle.get() == supkl5 or Plle.get() == supkl6 or Plle.get() == supkl7 or Plle.get() == supkl8 or Plle.get() == supkl9 or Plle.get() == supkl10:
                supPremium()
            else:
                messagebox.showerror(lang['error'], lang['invalid_code'],parent = Win)
        def pay2(pole4):
            global passw

            carantinn_window = create_window(Win,lang["activ_code"],global_bg,float(GlobalAlpha),350,250)

            carantinn_window.resizable(False, False)
            center_child(carantinn_window, Win)
            carantinn_window.protocol("WM_DELETE_WINDOW", lambda: dismiss(carantinn_window))

            passw = str(randint(10000, 100000))
            receiver_email = pole4.get()
            subject = lang["activ_code"]
            html_message = f"""
            <div style="
                font-family: Arial, sans-serif;
                background: linear-gradient(135deg, #f5f7fa, #e4ebf1);
                border: 1px solid #d0d7de;
                border-radius: 12px;
                padding: 20px;
                max-width: 400px;
                margin: 10px auto;
                text-align: center;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            ">
                <h2 style="
                    color: #2c3e50;
                    font-size: 22px;
                    margin-bottom: 12px;
                ">
                    {lang['your_antvrs_code']}
                </h2>
                <p style="
                    font-size: 20px;
                    font-weight: bold;
                    color: #2980b9;
                    margin: 0;
                ">
                    {passw}
                </p>
            </div>
            """

            send_email(to=str(receiver_email), subject=subject,
                       html=html_message)

            Lbl = Label(carantinn_window, text=lang["enter_antvrs_code"])
            Lbl.pack()
            Plle = ttk.Entry(carantinn_window)
            Plle.pack()

            Btn = ttk.Button(carantinn_window, text=lang['send'], command=lambda: prover(passw, Plle))
            Btn.pack()
            carantinn_window.grab_set()
        def pay1():
            global Premiump
            with open(f"{DIR}/status.bin", "w") as file:
                file.write("active")
                Premiump = True

                messagebox.showinfo(lang['success'], lang['you_got_PREM'],parent = Win)

                write_encrypted_file(f"{DIR}/label.bin", "★Premium★")

                act()
                podp()

        carantinnn_window = create_window(Win,"",global_bg,float(GlobalAlpha),450,250)

        center_child(carantinnn_window, Win)
        carantinnn_window.protocol("WM_DELETE_WINDOW", lambda: dismiss(carantinnn_window))

        lbl1 = Label(carantinnn_window, text=lang["enter_card_num"])
        lbl1.pack()
        pole1 = ttk.Entry(carantinnn_window, width=20)
        pole1.pack()

        lbl2 = Label(carantinnn_window, text=lang["enter_srok_deis"])
        lbl2.pack()
        pole2 = ttk.Entry(carantinnn_window, width=20)
        pole2.pack()

        lbl3 = Label(carantinnn_window, text=lang["enter_cvv"])
        lbl3.pack()
        pole3 = ttk.Entry(carantinnn_window, width=20)
        pole3.pack()

        lbl4 = Label(carantinnn_window, text=lang['enter_email'])
        lbl4.pack()
        if not os.path.exists("user.bin"):
            pole4 = ttk.Entry(carantinnn_window, width=20)
            pole4.pack()
        else:
            pole4 = ttk.Entry(carantinnn_window, width=20)
            pole4.pack()
            with open(f"{DIR}/user.bin", "rb") as f:
                for line in f:
                    key1, value = line.decode("utf-8").strip().split("=")
                    config[key1] = value
            user_email = config.get("Email")
            pole4.insert(0, user_email)

        style1 = ttk.Style()
        style1.configure("Green1.TButton", background="green", foreground="darkgreen")
        btn = ttk.Button(carantinnn_window, text=lang['activate'], style="Green1.TButton",
                             command=lambda: pay2(pole4))
        btn.pack()
        carantinnn_window.grab_set()
    def pay_with_svb():
        if svb_coins < 10000:
            messagebox.showerror(lang['error'], lang['no_svb'],parent = Win)
        else:
            global Premiump
            with open(f"{DIR}/status.bin", "w") as file:
                file.write("active")
                Premiump = True
                messagebox.showinfo("", lang["you_gotPREM"],parent = Win)

                write_encrypted_file(f"{DIR}/label.bin", "★Premium★")

                act()
                podp()
    Win.rowconfigure(0, weight=1)
    Win.columnconfigure(0, weight=1)


    notebook = ttk.Notebook(Win)
    notebook.pack()

    frame1 = ttk.Frame(notebook, padding=10)
    frame2 = ttk.Frame(notebook, padding=10)
    frame3 = ttk.Frame(notebook, padding=10)
    frame4 = ttk.Frame(notebook, padding=10)
    frame5 = ttk.Frame(notebook, padding=10)
    frame6 = ttk.Frame(notebook, padding=10)
    frame7 = ttk.Frame(notebook, padding=10)
    frame8 = ttk.Frame(notebook, padding=10)
    frame9 = ttk.Frame(notebook, padding=10)
    frame10 = ttk.Frame(notebook, padding=10)
    frame11 = ttk.Frame(notebook, padding=10)

    frame1.rowconfigure(0, weight=1)
    frame1.rowconfigure(1, weight=1)
    frame1.rowconfigure(2, weight=1)
    frame1.columnconfigure(0, weight=1)
    scanned_files_text = scrolledtext.ScrolledText(frame2, height=15, width=80, wrap="none")
    scanned_files_text.pack(pady=10, fill="both", expand=True)

    green_frame = Frame(frame1, bg="green", padx=20, pady=20)
    green_frame.grid()

    prem = Label(frame6, text="", font=font_prem)
    prem.pack()
    prey = Label(frame6,
                     text=lang['preims'],
                     font=font_prey
                     )


    prey.pack()

    try:
        with open(f"{DIR}/status.bin", "r") as file:
            content = file.read()
            if "active" in content:
                lbl_Premium_active = Label(frame6, text="Подписка уже оформлена")
                lbl_Premium_active.pack()
                lbl_choice = Label(frame6, text="Выберите стиль надписи:")
                lbl_choice.pack()
                vari1 = ttk.Radiobutton(frame6, text="★Premium★", variable=nadp_var, value="1")
                vari1.pack()
                vari2 = ttk.Radiobutton(frame6, text="☻Premium☻", variable=nadp_var, value="2")
                vari2.pack()
                vari3 = ttk.Radiobutton(frame6, text="⍟Premium⍟", variable=nadp_var, value="3")
                vari3.pack()
                vari4 = ttk.Radiobutton(frame6, text="$Premium$", variable=nadp_var, value="4")
                vari4.pack()
                vari5 = ttk.Radiobutton(frame6, text="↯Premium↯", variable=nadp_var, value="5")
                vari5.pack()
                vari6 = ttk.Radiobutton(frame6, text="♔Premium♔", variable=nadp_var, value="6")
                vari6.pack()
                vari7 = ttk.Radiobutton(frame6, text="☄Premium☄", variable=nadp_var, value="7")
                vari7.pack()
                vari2 = ttk.Radiobutton(frame6, text="✿Premium✿", variable=nadp_var, value="8")
                vari2.pack()
                vari3 = ttk.Radiobutton(frame6, text="♜Premium♜", variable=nadp_var, value="9")
                vari3.pack()
                vari4 = ttk.Radiobutton(frame6, text="♞Premium♞", variable=nadp_var, value="10")
                vari4.pack()
                vari5 = ttk.Radiobutton(frame6, text="♥Premium♥", variable=nadp_var, value="11")
                vari5.pack()
                vari6 = ttk.Radiobutton(frame6, text="♬Premium♬", variable=nadp_var, value="12")
                vari6.pack()
                if os.path.exists(f"{DIR}/label.bin"):
                    t = read_encrypted_file(f"{DIR}/label.bin").decode("utf-8").strip()
                if t == "★Premium★":
                    nadp_var.set("1")
                elif t == "☻Premium☻":
                    nadp_var.set("2")
                elif t == "⍟Premium⍟":
                    nadp_var.set("3")
                elif t == "$Premium$":
                    nadp_var.set("4")
                elif t == "↯Premium↯":
                    nadp_var.set("5")
                elif t == "♔Premium♔":
                    nadp_var.set("6")
                elif t == "☄Premium☄":
                    nadp_var.set("7")
                elif t == "✿Premium✿":
                    nadp_var.set("8")
                elif t == "♜Premium♜":
                    nadp_var.set("9")
                elif t == "♞Premium♞":
                    nadp_var.set("10")
                elif t == "♥Premium♥":
                    nadp_var.set("11")
                elif t == "♬Premium♬":
                    nadp_var.set("12")
                apply_button = ttk.Button(frame6, text=lang["Apply"], command=changelab, style="Blue1.TButton")
                apply_button.pack()
            elif "Gold" in content:
                lbl_Premium_active = Label(frame6, text="Подписка уже оформлена")
                lbl_Premium_active.pack()
                lbl_choice = Label(frame6, text="Выберите стиль надписи:")
                lbl_choice.pack()
                vari1 = ttk.Radiobutton(frame6, text="★Premium Gold★", variable=nadp_var, value="1")
                vari1.pack()
                vari2 = ttk.Radiobutton(frame6, text="☻Premium Gold☻", variable=nadp_var, value="2")
                vari2.pack()
                vari3 = ttk.Radiobutton(frame6, text="⍟Premium Gold⍟", variable=nadp_var, value="3")
                vari3.pack()
                vari4 = ttk.Radiobutton(frame6, text="$Premium Gold$", variable=nadp_var, value="4")
                vari4.pack()
                vari5 = ttk.Radiobutton(frame6, text="↯Premium Gold↯", variable=nadp_var, value="5")
                vari5.pack()
                vari6 = ttk.Radiobutton(frame6, text="♔Premium Gold♔", variable=nadp_var, value="6")
                vari6.pack()
                vari7 = ttk.Radiobutton(frame6, text="☄Premium Gold☄", variable=nadp_var, value="7")
                vari7.pack()
                vari3 = ttk.Radiobutton(frame6, text="✿Premium Gold✿", variable=nadp_var, value="8")
                vari3.pack()
                vari4 = ttk.Radiobutton(frame6, text="♜Premium Gold♜", variable=nadp_var, value="9")
                vari4.pack()
                vari5 = ttk.Radiobutton(frame6, text="♞Premium Gold♞", variable=nadp_var, value="10")
                vari5.pack()
                vari6 = ttk.Radiobutton(frame6, text="♥Premium Gold♥", variable=nadp_var, value="11")
                vari6.pack()
                vari7 = ttk.Radiobutton(frame6, text="♬Premium Gold♬", variable=nadp_var, value="12")
                vari7.pack()
                if os.path.exists(f"{DIR}/label.bin"):
                    t = read_encrypted_file(f"{DIR}/label.bin").decode("utf-8").strip()
                if t == "★Premium★":
                    nadp_var.set("1")
                elif t == "☻Premium Gold☻":
                    nadp_var.set("2")
                elif t == "⍟Premium Gold⍟":
                    nadp_var.set("3")
                elif t == "$Premium Gold$":
                    nadp_var.set("4")
                elif t == "↯Premium Gold↯":
                    nadp_var.set("5")
                elif t == "♔Premium Gold♔":
                    nadp_var.set("6")
                elif t == "☄Premium Gold☄":
                    nadp_var.set("7")
                elif t == "✿Premium Gold✿":
                    nadp_var.set("8")
                elif t == "♜Premium Gold♜":
                    nadp_var.set("9")
                elif t == "♞Premium Gold♞":
                    nadp_var.set("10")
                elif t == "♥Premium Gold♥":
                    nadp_var.set("11")
                elif t == "♬Premium Gold♬":
                    nadp_var.set("12")
                apply_button = ttk.Button(frame6, text=lang["Apply"], command=changelabGold, style="Blue1.TButton")
                apply_button.pack()
    except:

        kup = ttk.Button(frame6, text=lang['oform'], width=27, style="Green1.TButton", command=pay)
        kup.pack()
        kup = ttk.Button(frame6, text=lang['pay_with_svb'], width=27, style="Green1.TButton",
                             command=pay_with_svb)
        kup.pack()

    try:
        with open(f"{DIR}/status.bin", "r") as file:
            content = file.read()
            if "active" in content:
                # Виджеты, использованные в нескольких функциях
                Premiumlabel = Label(frame1, text=prem_l, font=fontPremium, fg="orange")
            elif "Gold" in content:
                # Виджеты, использованные в нескольких функциях
                Premiumlabel = Label(frame1, text=prem_l, font=fontPremium, fg="#00BFFF")
    except FileNotFoundError:
        pass

    # Создаем прогресс-бар
    progress_bar = ttk.Progressbar(frame2, orient='horizontal', length=250, mode='determinate')
    progress_bar.pack()
    if contenttt == "Gold":
        btn1 = ttk.Button(frame2, text=lang['super_check'], command=scan_folder, style="Violet1.TButton")
        btn1.pack()

    btn1 = ttk.Button(frame2, text=lang['quick_check'], command=scan_folder, style="Violet1.TButton")
    btn1.pack()
    btn2 = ttk.Button(frame2, text=lang["full_check"], command=scan_folder, style="Violet2.TButton")
    btn2.pack()
    btn3 = ttk.Button(frame2, text=lang["open_carantin"],command=carantin)
    btn3.pack()
    inf_frame = LabelFrame(frame1, text=lang["antvrs_info"])
    inf_frame.grid(row=3, column=0)

    try:
        with open(f"{DIR}/kluch.txt", "r") as file:
            content = file.read()
    except FileNotFoundError:
        pass

    # Версия Windows
    windows_version = platform.version()
    windows_name = platform.system()
    windows_release = platform.release()

    # Общий объем и доступная оперативная память
    ram_total = round(psutil.virtual_memory().total / (1024 ** 3), 2)
    ram_available = round(psutil.virtual_memory().available / (1024 ** 3), 2)

    # Общий объем и доступное место на диске C:
    disk_total = round(psutil.disk_usage("C:\\").total / (1024 ** 3), 2)
    disk_free = round(psutil.disk_usage("C:\\").free / (1024 ** 3), 2)
    if os.path.exists(f"{DIR}/licence_key.bin"):
        with open(f"{DIR}/licence_key.bin", "r") as file:
            keylic = file.read()
            file.close()

    inf_frame = LabelFrame(frame1, text=lang["antvrs_info"])
    inf_frame.grid(row=3, column=0)
    labell = Label(inf_frame, text=lang['info_ant1'], font=("Arial", 10, "bold"))
    labell.pack()
    lbbll = Label(inf_frame, text=f"{lang['info_ant2']} {security}")
    lbbll.pack()
    lits = Label(inf_frame, text=f"{lang['info_ant3']}: {target_date}")
    lits.pack()
    lits = Label(inf_frame, text=f"{lang['info_ant4']}: {keylic}")
    lits.pack()
    ug = Label(inf_frame, text=lang['info_ant5'])
    ug.pack()
    occ = Label(inf_frame, text=lang['info_ant6'])
    occ.pack()
    ozu = Label(inf_frame, text=f"{lang['OZU']}: {ram_total} {lang['GB']}")
    ozu.pack()
    pa = Label(inf_frame, text=f"{lang['DISKC']}: {disk_total} {lang['GB']}")
    pa.pack()

    try:
        with open(f"{DIR}/status.bin", "r") as file:
            content = file.read()
            if "active" in content:
                ug = Label(inf_frame, text="Premium  Подписка: Активна")
                ug.pack()
            if "Gold" in content:
                ug = Label(inf_frame, text="Premium  Подписка: Активна Gold Premium")
                ug.pack()
    except FileNotFoundError:
        ug = Label(inf_frame, text=lang['prem:not'])
        ug.pack()

    # Создаем фрейм для заливки зеленым цветом
    green_frame = Frame(frame3, bg="gray", padx=180, pady=20)  # Отступы 20 пикселей
    green_frame.pack()


    title_label = Label(green_frame, text=lang['settings'], font=("Arial", 16),
                            bg="gray")  # Фоновый цвет соответствует фрейму
    title_label.pack()  # Используем pack для фрейма

    var2 = BooleanVar()
    var6 = BooleanVar()
    var9 = BooleanVar()
    var10 = BooleanVar()
    dr = ttk.Checkbutton(frame3, text=lang['update_drivers'], variable=var2, command=drav)
    dr.pack()
    inte = ttk.Checkbutton(frame3, text=lang['enable_internet_s'], variable=var6, command=seti)
    inte.pack()
    sit = ttk.Checkbutton(frame3, text=lang['enable_prover_sites'], variable=var9, command=sitt)
    sit.pack()
    rek = ttk.Checkbutton(frame3, text=lang['block_add'], variable=var10, command=rek)
    rek.pack()

    prim = ttk.Button(frame3, width=20, text=lang['Apply'], command=func, style="Blue1.TButton")
    prim.pack()

    my_font = font.Font(family="Helvetica", size=16, weight="bold")
    my_font2 = font.Font(family="Helvetica", size=12)
    my_font3 = font.Font(family="Helvetica", size=12, weight="bold")
    labbe = Label(frame4, text="SVB AntiVirus \n ", font=my_font)
    labbe.pack()

    labb = Label(frame4,
                    text=f"{version} \n {lang['INFO_SVBANT']}",
                    font=my_font2)
    labb.pack()

    var5 = BooleanVar()
    usc = Label(frame5, text=lang["speed_up_pc"], font=my_font3)
    usc.pack()
    sy = ttk.Checkbutton(frame5, text=lang["cleanup_cesh"], variable=var5, command=csh)
    sy.pack()
    if not os.path.exists("user.bin"):
        lbl = Label(frame8, text=lang['you_not_have_uch'])
        lbl.pack()
    else:
        with open(f"{DIR}/user.bin", "rb") as f:
            for line in f:
                key1, value = line.decode("utf-8").strip().split("=")
                config[key1] = value
        name = config.get("Name")
        lastname = config.get("Last name")
        number = config.get("Phone number")
        email = config.get("Email")
        image = Image.open(
            "icons/interface/profile.png")
        image = image.resize((200, 200))
        photo = ImageTk.PhotoImage(image)

        label = Label(frame8, image=photo)
        label.pack()

        lbl = Label(frame8, text=f"{lang['name']}", font=("Arial", 16, "bold"))
        lbl.pack()
        lbl = Label(frame8, text=f"{name}", font=("Arial", 12, "italic"))
        lbl.pack()
        lbl = Label(frame8, text=f"{lang['last-name']}", font=("Arial", 16, "bold"))
        lbl.pack()
        lbl = Label(frame8, text=f"{lastname}", font=("Arial", 12, "italic"))
        lbl.pack()
        lbl = Label(frame8, text=f"{lang['tel_n']}:", font=("Arial", 16, "bold"))
        lbl.pack()
        lbl = Label(frame8, text=f"{number}", font=("Arial", 12, "italic"))
        lbl.pack()
        lbl = Label(frame8, text=f"Email:", font=("Arial", 16, "bold"))
        lbl.pack()
        lbl = Label(frame8, text=f"{email}", font=("Arial", 12, "italic"))
        lbl.pack()

        btn = ttk.Button(frame8, text=lang['btn_delete_account'], command=delete_user, style="Red1.TButton")
        btn.pack()

    def create_user():
        def prodl(pole1, pole2, pole3, pole4):
            carantinnn_window.destroy()
            with open(f"{DIR}/user.bin", "wb") as config_file:
                config_data = f"Name={pole1}\nLast name={pole2}\nPhone number={pole3}\nEmail={pole4}"
                config_file.write(config_data.encode("utf-8"))

            messagebox.showinfo(lang["acc"], lang['you_regestered_account'],parent = Win)
            proverka_userdata()

        carantinnn_window = create_window(root, lang["creation_of_account"], global_bg, float(GlobalAlpha), 400, 250)
        carantinnn_window.resizable(False, False)

        lbl1 = Label(carantinnn_window, text=lang["enter_name"])
        lbl1.pack()
        pole1 = ttk.Entry(carantinnn_window, width=20)
        pole1.pack()

        lbl2 = Label(carantinnn_window, text=lang["enter_last_name"])
        lbl2.pack()
        pole2 = ttk.Entry(carantinnn_window, width=20)
        pole2.pack()

        lbl3 = Label(carantinnn_window, text=lang["enter_telep"])
        lbl3.pack()
        pole3 = ttk.Entry(carantinnn_window, width=20)
        pole3.pack()

        lbl4 = Label(carantinnn_window, text=lang["enter_email"])
        lbl4.pack()
        pole4 = ttk.Entry(carantinnn_window, width=20)
        pole4.pack()

        style1 = ttk.Style()
        style1.configure("Green1.TButton", background="green", foreground="darkgreen")

        btn = ttk.Button(carantinnn_window, text=lang['cre'], style="Green1.TButton",
                             command=lambda: prodl(pole1.get(), pole2.get(), pole3.get(), pole4.get()))
        btn.pack()
        carantinnn_window.grab_set()
    def casino():
        def try_get():
            global keys,svb_coins
            if svb_coins > 1000:
                svb_coins -= 1000
                transactions('-1000 SVB Coins',start_time_)
                send('payement', 1000)
                rand = random.randint(10000, 100000)
                for i in keys:
                    if rand == i:
                        supPremium()
                        break
                    else:
                        messagebox.showerror("", lang['neud'],parent = Win)
            else:
                messagebox.showerror(lang['error'], lang["no_svb"],parent = Win)

        lbl = ttk.Label(frame11, text=f"{lang['balance']} {svb_coins}", font=("Arial", 24, "bold"))
        lbl.pack()
        lbl = ttk.Label(frame11, text=f"{lang['buy_super_key_info']}",
                            font=("Arial", 14, "bold"))
        lbl.pack()
        btn = ttk.Button(frame11, text=lang['try_buy_super_key'], command=try_get)
        btn.pack()
    def zachita_pol():
        messagebox.showinfo("", lang['all_your_data_saved'],parent = Win)
    def open_link(url):
        # Указываем браузер Chrome
        chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'
        webbrowser.get(chrome_path).open(url)


    link_text = lang['open_svbant_site']

    url = "file:///D:/programar/%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5/%D0%BF%D1%80%D0%BE%D0%B5%D0%BA%D1%82%D1%8B/index.html"

    # Создание метки с текстом ссылки
    label = Label(frame4, text=link_text, fg="blue", cursor="hand2")
    label.pack()

    # Привязываем обработчик события к метке
    label.bind("<Button-1>", lambda e: open_link(url))

    notebook.add(frame1, text=lang['main'])
    notebook.add(frame2, text=lang["MENU_security"])
    notebook.add(frame5, text=lang["MENU_speedup"])
    notebook.add(frame6, text=lang["MENU_prem"])
    notebook.add(frame3, text=lang["settings"])
    notebook.add(frame8, text=lang["acc"])
    notebook.add(frame4, text=lang['about'])
    Win.iconphoto(True, icon_image)

    def proverka_userdata():
        if not os.path.exists("user.bin"):

            user_label = Label(frame1, text=lang['you_no_created_account'], font=("Arial", 16))
            user_label.grid(row=2, column=3)
            btn = ttk.Button(frame1, text=lang["cre"], command=create_user)
            btn.grid(row=2, column=4)
        else:
            with open(f"{DIR}/user.bin", "rb") as f:
                for line in f:
                    key1, value = line.decode("utf-8").strip().split("=")
                    config[key1] = value
            user_name = config.get("Name")
            user_last_name = config.get("Last name")

            user_label = Label(frame1, text=f"{lang['uchet_zap']}: {user_last_name} {user_name}", font=("Arial", 16),
                                   bg="gray")
            user_label.grid(row=1, column=0)
            btn = ttk.Button(frame1, text=lang['btn_delete_account'], style="Red1.TButton", command=delete_user)
            btn.grid(row=4, column=0)

    opfile()
    securr()
    casino()
    zachita_pol()
    Win.mainloop()

