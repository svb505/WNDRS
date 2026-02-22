from datetime import datetime
from tkinter import *
from tkinter import ttk, messagebox
from server_statistick import update_file
from send_email import send_email
from logger_setup import system_logger
import time
from PIL import Image, ImageTk
import random
import logging
import os
import sqlite3
import customtkinter as ctk
from logtofile import log_to_file
from copy_file_to_folder import copy_file_to_folder
from send_email_template import send
from transactions import transactions
from save_and_load_balance import save_balance,load_balance

SYSTEM_LEVEL = 25
logging.addLevelName(SYSTEM_LEVEL, "SYSTEM")
svb_coins = 0
flag = False
deposit_sum = 0

os.makedirs("bookmaker_settings", exist_ok=True)

if os.path.exists("bookmaker_settings/account.db"):
    flag = True
    conn = sqlite3.connect("bookmaker_settings/account.db")
    cursor = conn.cursor()

    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS account (
                    name TEXT,
                    email TEXT,
                    balance INTEGER
                    )
            """)
    conn.commit()

    cursor.execute("SELECT * FROM account")
    acc = cursor.fetchall()

    if acc:
        ac = acc[0]
        n, e, b = ac[0], ac[1], ac[2]
    else:
        n = e = b = "Unknown"
    deposit_sum = b


def log_system(msg, start_time_):
    try:
        elapsed = time.time() - start_time_
    except NameError:
        elapsed = 0
    formatted_msg = f"[{elapsed:.1f}] - {msg}"
    system_logger.log(SYSTEM_LEVEL, formatted_msg)

def history(data, start_time_):
    log_to_file("History saved", start_time_=start_time_)
    if os.path.exists("bookmaker_settings/history.cfg"):
        with open("bookmaker_settings/history.cfg", 'wb') as f:
            f.write((data + "\n").encode("utf-8"))
    else:
        with open("bookmaker_settings/history.cfg", 'ab') as f:
            f.write((data + "\n").encode("utf-8"))


def open_win(root, lang, actives_programs, edition, start_time_, global_bg, global_fg,GlobalAlpha):
    def post(n1, n2, img1, img2):
        def p(name, d, coof, img1, img2, n1, n2):
            global svb_coins, deposit_sum
            if not d.isdigit() or int(d) <= 0:
                messagebox.showerror(lang["error"], lang["not_isdigit"], parent=Win)
                log_to_file(lang["not_isdigit"], level="error", start_time_=start_time_)
                return
            if deposit_sum >= int(d):
                deposit_sum -= int(d)
                conn = sqlite3.connect("bookmaker_settings/account.db")
                cursor = conn.cursor()
                s = cursor.execute("SELECT balance FROM account").fetchone()
                total = int(s[0]) - int(d)
                cursor.execute("UPDATE account SET balance = ?", (int(total),))
                conn.commit()
                conn.close()
            else:
                messagebox.showerror(lang["error"], lang["no_deposit"], parent=Win)
                log_to_file(lang["no_deposit"], level="error", start_time_=start_time_)
                return
            win = Toplevel(Win)
            win.attributes("-alpha", float(GlobalAlpha))
            win.config(bg=global_bg)
            win.geometry('500x400')
            win.title(lang["bukm"])
            image = Image.open("icons/interface/fc.png")
            icon_image = ImageTk.PhotoImage(image)
            win.iconphoto(False, icon_image)

            points1 = random.randint(0, 10)
            points2 = random.randint(0, 10)

            frame = Frame(win, bg=global_bg)
            frame.pack()

            lbl = Label(frame, image=img1)
            lbl.image = img1
            lbl.pack(side=LEFT)
            Label(frame, text=str(points1), font=("Arial", 12, "bold"), bg=global_bg, fg=global_fg).pack(side=LEFT)

            lbl1 = Label(frame, image=img2)
            lbl1.image = img2
            lbl1.pack(side=RIGHT)
            Label(frame, text=str(points2), font=("Arial", 12, "bold"), bg=global_bg, fg=global_fg).pack(side=RIGHT)
            conn = sqlite3.connect("bookmaker_settings/account.db")
            cursor = conn.cursor()

            cursor.execute("""
                                CREATE TABLE IF NOT EXISTS account (
                                name TEXT,
                                email TEXT,
                                balance INTEGER
                                )
                        """)
            conn.commit()

            cursor.execute("SELECT * FROM account")
            acc = cursor.fetchall()

            if acc:
                ac = acc[0]
                n, email, b = ac[0], ac[1], ac[2]
            else:
                n = email = b = "Unknown"
            match = f"{n1} VS {n2}"
            stake = d
            odds = coof
            payout = int(d) * float(coof)
            timestamp = datetime.now().strftime("%Y-%m-%d")
            if name == n1 and points1 > points2:
                send_email(
                    to=str(email),
                    subject=lang["win_ticket"],
                    html=f"""
                <html>
                  <body style="font-family: Arial, sans-serif; background-color: #f2f2f2; padding: 30px;">
                    <div style="background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); max-width: 600px; margin: auto;">
                      <h2 style="color: #2c3e50; text-align: center;">{lang["win_ticket1"]}</h2>
                      <hr style="border: none; border-top: 1px solid #ddd;">
                      <p style="font-size: 16px; color: #444;">
                        {lang["info_ticket"]}
                      </p>
                      <table style="width: 100%; border-collapse: collapse; margin-top: 20px;">
                        <tr>
                          <td style="padding: 10px; border: 1px solid #eee;"><strong>{lang["sob"]}</strong></td>
                          <td style="padding: 10px; border: 1px solid #eee;">{match}</td>
                        </tr>
                        <tr>
                          <td style="padding: 10px; border: 1px solid #eee;"><strong>{lang["stavka"]}</strong></td>
                          <td style="padding: 10px; border: 1px solid #eee;">{stake} $</td>
                        </tr>
                        <tr>
                          <td style="padding: 10px; border: 1px solid #eee;"><strong>{lang["coof__"]}</strong></td>
                          <td style="padding: 10px; border: 1px solid #eee;">{odds}</td>
                        </tr>
                        <tr>
                          <td style="padding: 10px; border: 1px solid #eee;"><strong>{lang["win_sum_"]}</strong></td>
                          <td style="padding: 10px; border: 1px solid #eee; color: green; font-weight: bold;">{payout} $</td>
                        </tr>
                        <tr>
                          <td style="padding: 10px; border: 1px solid #eee;"><strong>{lang["date_"]}</strong></td>
                          <td style="padding: 10px; border: 1px solid #eee;">{timestamp}</td>
                        </tr>
                      </table>
                      <p style="font-size: 14px; color: #888; margin-top: 30px;">
                        {lang["thanks"]}
                      </p>
                    </div>
                  </body>
                </html>
                """
                )

                total_sum = int(d) * float(coof)
                svb_coins += int(total_sum)
                send('receipt', int(total_sum))
                update_file("count_svbcoins.txt", int(total_sum))
                save_balance(svb_coins,start_time_)
                transactions(f'+{total_sum} Svb Coins', start_time_)
                Label(win, text=f"{lang['pozd']}{lang['stavka_v']}:{total_sum} SVb Coins", bg=global_bg,
                      fg=global_fg).pack()
                Label(win, text=lang["verify_email"]).pack()
                history(f"[{datetime.now().strftime('%m-%d')}] {n1} VS {n2}:{d} $ @{coof} - ✅{total_sum}", start_time_)
            elif name == n2 and points2 > points1:
                send_email(
                    to=str(email),
                    subject=lang["win_ticket"],
                    html=f"""
                                <html>
                                  <body style="font-family: Arial, sans-serif; background-color: #f2f2f2; padding: 30px;">
                                    <div style="background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); max-width: 600px; margin: auto;">
                                      <h2 style="color: #2c3e50; text-align: center;">{lang["win_ticket1"]}</h2>
                                      <hr style="border: none; border-top: 1px solid #ddd;">
                                      <p style="font-size: 16px; color: #444;">
                                        {lang["info_ticket"]}
                                      </p>
                                      <table style="width: 100%; border-collapse: collapse; margin-top: 20px;">
                                        <tr>
                                          <td style="padding: 10px; border: 1px solid #eee;"><strong>{lang["sob"]}</strong></td>
                                          <td style="padding: 10px; border: 1px solid #eee;">{match}</td>
                                        </tr>
                                        <tr>
                                          <td style="padding: 10px; border: 1px solid #eee;"><strong>{lang["stavka"]}</strong></td>
                                          <td style="padding: 10px; border: 1px solid #eee;">{stake} $</td>
                                        </tr>
                                        <tr>
                                          <td style="padding: 10px; border: 1px solid #eee;"><strong>{lang["coof__"]}</strong></td>
                                          <td style="padding: 10px; border: 1px solid #eee;">{odds}</td>
                                        </tr>
                                        <tr>
                                          <td style="padding: 10px; border: 1px solid #eee;"><strong>{lang["win_sum_"]}</strong></td>
                                          <td style="padding: 10px; border: 1px solid #eee; color: green; font-weight: bold;">{payout} $</td>
                                        </tr>
                                        <tr>
                                          <td style="padding: 10px; border: 1px solid #eee;"><strong>{lang["date_"]}</strong></td>
                                          <td style="padding: 10px; border: 1px solid #eee;">{timestamp}</td>
                                        </tr>
                                      </table>
                                      <p style="font-size: 14px; color: #888; margin-top: 30px;">
                                        {lang["thanks"]}
                                      </p>
                                    </div>
                                  </body>
                                </html>
                                """
                )

                total_sum = int(d) * float(coof)
                svb_coins += int(total_sum)
                send('receipt', int(total_sum))
                update_file("count_svbcoins.txt", int(total_sum))
                save_balance(svb_coins,start_time_)
                transactions(f'+{total_sum} Svb Coins', start_time_)
                Label(win, text=f"{lang['pozd']}{lang['stavka_v']}:{total_sum} SVb Coins", bg=global_bg,
                      fg=global_fg).pack()
                Label(win, text=lang["verify_email"], bg=global_bg, fg=global_fg).pack()
                history(f"[{datetime.now().strftime('%m-%d')}] {n1} VS {n2}:{d} $ @{coof} - ✅{total_sum}", start_time_)
            elif name == "n" and points1 == points2:
                send_email(
                    to=str(email),
                    subject=lang["win_ticket"],
                    html=f"""
                                <html>
                                  <body style="font-family: Arial, sans-serif; background-color: #f2f2f2; padding: 30px;">
                                    <div style="background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); max-width: 600px; margin: auto;">
                                      <h2 style="color: #2c3e50; text-align: center;">{lang["win_ticket1"]}</h2>
                                      <hr style="border: none; border-top: 1px solid #ddd;">
                                      <p style="font-size: 16px; color: #444;">
                                        {lang["info_ticket"]}
                                      </p>
                                      <table style="width: 100%; border-collapse: collapse; margin-top: 20px;">
                                        <tr>
                                          <td style="padding: 10px; border: 1px solid #eee;"><strong>{lang["sob"]}</strong></td>
                                          <td style="padding: 10px; border: 1px solid #eee;">{match}</td>
                                        </tr>
                                        <tr>
                                          <td style="padding: 10px; border: 1px solid #eee;"><strong>{lang["stavka"]}</strong></td>
                                          <td style="padding: 10px; border: 1px solid #eee;">{stake} $</td>
                                        </tr>
                                        <tr>
                                          <td style="padding: 10px; border: 1px solid #eee;"><strong>{lang["coof__"]}</strong></td>
                                          <td style="padding: 10px; border: 1px solid #eee;">{odds}</td>
                                        </tr>
                                        <tr>
                                          <td style="padding: 10px; border: 1px solid #eee;"><strong>{lang["win_sum_"]}</strong></td>
                                          <td style="padding: 10px; border: 1px solid #eee; color: green; font-weight: bold;">{payout} $</td>
                                        </tr>
                                        <tr>
                                          <td style="padding: 10px; border: 1px solid #eee;"><strong>{lang["date_"]}</strong></td>
                                          <td style="padding: 10px; border: 1px solid #eee;">{timestamp}</td>
                                        </tr>
                                      </table>
                                      <p style="font-size: 14px; color: #888; margin-top: 30px;">
                                        {lang["thanks"]}
                                      </p>
                                    </div>
                                  </body>
                                </html>
                                """
                )

                total_sum = int(d) * float(coof)
                svb_coins += int(total_sum)
                send('receipt', int(total_sum))
                update_file("count_svbcoins.txt", int(total_sum))
                save_balance(svb_coins,start_time_)
                transactions(f'+{total_sum} Svb Coins', start_time_)
                Label(win, text=f"{lang['pozd']}{lang['stavka_v']}:{total_sum} SVb Coins", bg=global_bg,
                      fg=global_fg).pack()
                Label(win, text=lang["verify_email"], bg=global_bg, fg=global_fg).pack()
                history(f"[{datetime.now().strftime('%m-%d')}] {n1} VS {n2}:{d} $ @{coof} - ✅{total_sum}", start_time_)
            else:
                send_email(
                    to=str(email),
                    subject=lang["billet_sub"],
                    html=f"""
                <html>
                  <body style="font-family: Arial, sans-serif; background-color: #f8f8f8; padding: 30px;">
                    <div style="background-color: #ffffff; padding: 25px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.05); max-width: 600px; margin: auto;">
                      <h2 style="color: #e74c3c; text-align: center;">{lang["not_win2__"]}</h2>
                      <hr style="border: none; border-top: 1px solid #eee;">
                      <p style="font-size: 16px; color: #555;">
                       {lang['not_win1__']}
                      </p>
                      <table style="width: 100%; border-collapse: collapse; margin-top: 20px;">
                        <tr>
                          <td style="padding: 10px; border: 1px solid #eee;"><strong>{lang["sob"]}</strong></td>
                          <td style="padding: 10px; border: 1px solid #eee;">{match}</td>
                        </tr>
                        <tr>
                          <td style="padding: 10px; border: 1px solid #eee;"><strong>{lang["stavka"]}</strong></td>
                          <td style="padding: 10px; border: 1px solid #eee;">{stake} $</td>
                        </tr>
                        <tr>
                          <td style="padding: 10px; border: 1px solid #eee;"><strong>{lang["coof__"]}</strong></td>
                          <td style="padding: 10px; border: 1px solid #eee;">{odds}</td>
                        </tr>
                        <tr>
                          <td style="padding: 10px; border: 1px solid #eee;"><strong>{lang["_resultat_"]}</strong></td>
                          <td style="padding: 10px; border: 1px solid #eee; color: #e74c3c; font-weight: bold;">{lang["proig"]}</td>
                        </tr>
                        <tr>
                          <td style="padding: 10px; border: 1px solid #eee;"><strong>{lang["date_"]}</strong></td>
                          <td style="padding: 10px; border: 1px solid #eee;">{timestamp}</td>
                        </tr>
                      </table>
                      <p style="font-size: 14px; color: #888; margin-top: 30px;">
                        {lang["not_win__"]}
                      </p>
                    </div>
                  </body>
                </html>
                """
                )

                Label(win, text=f"{lang['ne']} {lang['ne_']}", bg=global_bg, fg=global_fg).pack()
                Label(win, text=lang["verify_email"], bg=global_bg, fg=global_fg).pack()
                history(f"[{datetime.now().strftime('%m-%d')}] {n1} VS {n2}:{d} $ @{coof} - ❌")

        def show(lbl, coof, m):
            lbl.config(text=f'{lang["vash_v"]}:{int(m) * float(coof)}')

        w = Toplevel(Win)
        w.attributes("-alpha", float(GlobalAlpha))
        w.config(bg=global_bg)
        w.geometry('500x400')
        w.title(lang["bukm"])
        image = Image.open("icons/interface/fc.png")
        icon_image = ImageTk.PhotoImage(image)
        w.iconphoto(False, icon_image)

        if flag:
            lbl = Label(w, text=f"{lang['vash_v']}:None", bg=global_bg, fg=global_fg)
            lbl.pack()
            Label(w, text=lang["ishod"], bg=global_bg, fg=global_fg).pack()
            frm1 = Frame(w)
            frm1.pack()
            frm = Frame(w)
            frm.pack()

            var1 = StringVar()
            coof = StringVar()
            coof.set("1.2")

            label1 = Label(frm1, image=img1)
            label1.image = img1
            label1.pack(side=LEFT)

            label2 = Label(frm1, image=img2)
            label2.image = img2
            label2.pack(side=RIGHT)

            ttk.Radiobutton(frm, text=n1, variable=var1, value=n1).pack(side=LEFT)
            ttk.Radiobutton(frm, text=lang["nich"], variable=var1, value="n").pack(side=LEFT)
            ttk.Radiobutton(frm, text=n2, variable=var1, value=n2).pack(side=LEFT)

            Label(w, text=lang["sum_"], bg=global_bg, fg=global_fg).pack()
            m = ctk.CTkEntry(w, placeholder_text=lang['sum_'])
            m.pack()

            Label(w, text=lang["coof"], bg=global_bg, fg=global_fg).pack()
            c = ttk.Combobox(w, values=["1.2", "1.5", "1.9", "2.3", "3.8", "5.5"], textvariable=coof)
            c.pack()
            c.config(state="readonly")
            c.bind("<<ComboboxSelected>>", lambda event: show(lbl, coof.get(), m.get()))

            ttk.Button(w, text=lang["postavit"],
                       command=lambda: p(var1.get(), m.get(), coof.get(), img1, img2, n1, n2)).pack()
        else:
            Label(w, text=lang["you_no_have_acc"], font=("Arial", 17, "bold"), bg=global_bg, fg=global_fg).pack()
            ttk.Button(w, text=lang["register_"], command=register).pack()

    def register():
        def register1(name, email, dep):
            global flag, svb_coins, deposit_sum
            if len(name) < 3:
                messagebox.showwarning(lang["warning_"], lang["invalidname"], parent=Win)
                return
            if int(dep) < 0 or not dep.isdigit():
                messagebox.showwarning(lang["warning_"], lang["enter_valid_balance"], parent=Win)
                return
            svb_coins = load_balance(start_time_)
            if svb_coins >= int(dep):
                deposit_sum += int(dep)
                svb_coins -= int(dep)
                send("payement", int(dep))
                transactions(f"-{dep} SVB Coins", start_time_)
                save_balance(svb_coins,start_time_)
            else:
                messagebox.showerror(lang["error"], lang["no_svb"], parent=Win)
                return
            conn = sqlite3.connect("bookmaker_settings/account.db")
            cursor = conn.cursor()
            cursor.execute("""CREATE table IF NOT EXISTS account(
                        name TEXT,
                        email TEXT,
                        balance INTEGER
                    )""")
            conn.commit()
            cursor.execute("INSERT INTO account (name,email,balance) VALUES(?, ?, ?)", (name, email, int(dep),))
            conn.commit()
            conn.close()
            flag = True
            messagebox.showinfo(lang["success"], lang["register_tr"], parent=Win)

        log_to_file("Register", start_time_=start_time_)
        W = Toplevel(root)
        W.config(bg=global_bg)
        W.attributes("-alpha", float(GlobalAlpha))
        W.geometry('500x500')
        W.title(lang["bukm"])
        image = Image.open("icons/interface/fc.png")
        icon_image = ImageTk.PhotoImage(image)
        W.iconphoto(False, icon_image)
        Label(W, text=lang["enter_name"], bg=global_bg, fg=global_fg).pack()
        name = ctk.CTkEntry(W, placeholder_text=lang['eter_name'])
        name.pack()
        Label(W, text=lang["enter_email"], bg=global_bg, fg=global_fg).pack()
        email = ctk.CTkEntry(W, placeholder_text=lang['enter_email'])
        email.pack()
        Label(W, text=lang["enter_start_dep"], bg=global_bg, fg=global_fg).pack()
        deposit = ctk.CTkEntry(W, placeholder_text=lang["enter_start_dep"])
        deposit.pack()

        ttk.Button(W, text=lang['register_'], command=lambda: register1(name.get(), email.get(), deposit.get())).pack()

    def account():
        def popol():
            def ok(sum):
                global svb_coins, deposit_sum
                if int(sum) < 0 or not sum.isdigit():
                    messagebox.showwarning(lang["warning_"], lang["enter_valid_balance"], parent=Win)
                    return
                svb_coins = load_balance(start_time_)
                if svb_coins >= int(sum):
                    deposit_sum += int(sum)
                    svb_coins -= int(sum)
                    send("payament", int(sum))
                    transactions(f"-{sum} SVB Coins", start_time_)
                    save_balance(start_time_=start_time_)
                    log_to_file(f"-{sum} SVB Coins", start_time_=start_time_)
                else:
                    messagebox.showerror(lang["error"], lang["no_svb"], parent=Win)
                    log_to_file(lang["no_svb"], level="error", start_time_=start_time_)
                    return
                conn = sqlite3.connect("bookmaker_settings/account.db")
                cursor = conn.cursor()
                s = cursor.execute("SELECT balance FROM account").fetchone()
                total = int(s[0]) + int(sum)
                cursor.execute("UPDATE account SET balance = ?", (int(total),))
                conn.commit()
                conn.close()
                messagebox.showinfo(lang["success"], f"{lang['popol_tr']}{sum} SVB Coins", parent=Win)

            w = Toplevel(W)
            w.attributes("-alpha", float(GlobalAlpha))
            w.config(bg=global_bg)
            w.geometry('300x200')
            w.title(lang["bukm"])
            image = Image.open("icons/interface/fc.png")
            icon_image = ImageTk.PhotoImage(image)
            w.iconphoto(False, icon_image)

            Label(w, text=lang["enter_sum_"], bg=global_bg, fg=global_fg).pack()
            bal = ctk.CTkEntry(w, placeholder_text=lang['enter_sum_'])
            bal.pack()
            ttk.Button(w, text=lang["popol"], command=lambda: ok(bal.get())).pack()

        W = Toplevel(root)
        W.attributes("-alpha", float(GlobalAlpha))
        W.config(bg=global_bg)
        W.geometry('550x350')
        W.title(lang["bukm"])
        image = Image.open("icons/interface/fc.png")
        icon_image = ImageTk.PhotoImage(image)
        W.iconphoto(False, icon_image)
        log_to_file('Open account', start_time_=start_time_)
        conn = sqlite3.connect("bookmaker_settings/account.db")
        cursor = conn.cursor()

        cursor.execute("""
                CREATE TABLE IF NOT EXISTS account (
                name TEXT,
                email TEXT,
                balance INTEGER
                )
        """)
        conn.commit()

        cursor.execute("SELECT * FROM account")
        acc = cursor.fetchall()

        if acc:
            ac = acc[0]
            n, e, b = ac[0], ac[1], ac[2]
        else:
            n = e = b = "Unknown"
        Label(W, text=f"{lang['name=']}{n}", font=("Arial", 14, "bold"), bg=global_bg, fg=global_fg).pack()
        Label(W, text=f"{lang['email=']}{e}", font=("Arial", 14, "bold"), bg=global_bg, fg=global_fg).pack()
        Label(W, text=f"{lang['balance=']}{b}", font=("Arial", 14, "bold"), bg=global_bg, fg=global_fg).pack()
        ttk.Button(W, text=lang["popol_balance"], command=popol).pack()

    actives_programs.append("SVB Bookmaker Window")
    log_to_file('Opened SVB Bookmaker', start_time_=start_time_)

    Win = Toplevel(root)
    Win.attributes("-alpha", float(GlobalAlpha))
    Win.config(bg=global_bg)
    Win.geometry('1000x500')
    Win.title(lang["bukm"])
    image = Image.open("icons/interface/fc.png")
    icon_image = ImageTk.PhotoImage(image)
    Win.iconphoto(False, icon_image)

    img1 = ImageTk.PhotoImage(Image.open("icons//fc/spartak.png").resize((50, 55), Image.Resampling.LANCZOS))
    img2 = ImageTk.PhotoImage(Image.open("icons//fc/shakhtar.png").resize((50, 55), Image.Resampling.LANCZOS))
    img3 = ImageTk.PhotoImage(Image.open("icons//fc/real-madrid.png").resize((50, 55), Image.Resampling.LANCZOS))
    img4 = ImageTk.PhotoImage(Image.open("icons//fc/manchester.png").resize((50, 55), Image.Resampling.LANCZOS))
    img5 = ImageTk.PhotoImage(Image.open("icons//fc/ol_marseille.png").resize((50, 55), Image.Resampling.LANCZOS))
    img6 = ImageTk.PhotoImage(Image.open("icons//fc/bayen-munchen.png").resize((50, 55), Image.Resampling.LANCZOS))
    img7 = ImageTk.PhotoImage(Image.open("icons//fc/dynamo.png").resize((50, 55), Image.Resampling.LANCZOS))
    img8 = ImageTk.PhotoImage(Image.open("icons//fc/dnipro1.png").resize((50, 55), Image.Resampling.LANCZOS))
    img9 = ImageTk.PhotoImage(Image.open("icons//fc/barcelona.png").resize((50, 55), Image.Resampling.LANCZOS))
    img10 = ImageTk.PhotoImage(Image.open("icons//fc/arsenal.png").resize((50, 55), Image.Resampling.LANCZOS))
    img11 = ImageTk.PhotoImage(Image.open("icons//fc/valencia.png").resize((50, 55), Image.Resampling.LANCZOS))
    img12 = ImageTk.PhotoImage(Image.open("icons//fc/cska.png").resize((50, 55), Image.Resampling.LANCZOS))
    img13 = ImageTk.PhotoImage(Image.open("icons//fc/porto.jpg").resize((50, 55), Image.Resampling.LANCZOS))
    img14 = ImageTk.PhotoImage(Image.open("icons//fc/psg.png").resize((50, 55), Image.Resampling.LANCZOS))

    images = [img1, img2, img3, img4, img5, img6, img7, img8, img9, img10, img11, img12, img13, img14]
    labels = [lang['spartak'], lang['shakhtar'], lang['real_mad'], lang['manc'], lang['ol_m'], lang['bayen'],
              lang['dynamo'],
              lang['dnipro1'], lang['barc'], lang['ars'], lang['valen'], lang['cska'], lang['porto'], lang['psg']]
    combined = list(zip(images, labels))

    random.shuffle(combined)

    images_shuffled, labels_shuffled = zip(*combined)
    images_shuffled = list(images_shuffled)
    labels_shuffled = list(labels_shuffled)
    if os.path.exists("bookmaker_settings/account.db"):
        ttk.Button(Win, text=lang["account"], command=account).pack()
    else:
        ttk.Button(Win, text=lang["register_"], command=register).pack()
    Label(Win, text=lang["tek"], font=("Arial", 15, "bold"), bg=global_bg, fg=global_fg).pack()

    scroll_canvas = Canvas(Win)
    scroll_canvas.pack(side=LEFT, fill=BOTH, expand=True)

    scrollbar = Scrollbar(Win, command=scroll_canvas.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    scroll_canvas.configure(yscrollcommand=scrollbar.set)

    match_frame_container = Frame(scroll_canvas)
    scroll_canvas.create_window((0, 0), window=match_frame_container, anchor='nw')

    def on_frame_configure(event):
        scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all"))

    def resize_canvas(event):
        scroll_canvas.itemconfig("all", width=event.width)

    match_frame_container.bind("<Configure>", on_frame_configure)
    scroll_canvas.bind("<Configure>", resize_canvas)

    for i in range(7):
        if global_bg == "white":
            bg_color = "#ffffff" if i % 2 == 0 else "#e6e6e6"
        else:
            bg_color = "black" if i % 2 == 0 else "#323441"
        match_block = Frame(match_frame_container, bd=2, relief="groove", padx=10, pady=10, bg=bg_color)

        match_block.pack(fill=X, pady=5, padx=10)
        Label(match_block, text=f"{lang['match']} {i + 1}", font=("Arial", 10, "bold"), bg=global_bg, fg=global_fg) \
            .grid(row=0, column=0, columnspan=6, sticky=W)
        Label(match_block, text=labels_shuffled[i], font=("Arial", 12), bg=global_bg, fg=global_fg) \
            .grid(row=1, column=1, padx=5, sticky=W)

        l1 = Label(match_block, image=images_shuffled[i])
        l1.image = images_shuffled[i]
        l1.grid(row=1, column=2, padx=5)

        Label(match_block, text="VS", font=("Arial", 12, "bold"), bg=global_bg, fg=global_fg).grid(row=1, column=3,
                                                                                                   padx=5)
        l2 = Label(match_block, image=images_shuffled[i + 7])
        l2.image = images_shuffled[i + 7]
        l2.grid(row=1, column=4, padx=5)

        Label(match_block, text=labels_shuffled[i + 7], font=("Arial", 12)) \
            .grid(row=1, column=5, padx=5, sticky=E)
        ttk.Button(match_block, text=lang["sdel"],
                   command=lambda i=i: post(labels_shuffled[i], labels_shuffled[i + 7],
                                            images_shuffled[i], images_shuffled[i + 7])
                   ).grid(row=2, column=0, columnspan=6, pady=5)
        score_label = Label(match_block, text="0:0", font=("Arial", 10), bg=global_bg, fg=global_fg)
        score_label.grid(row=3, column=0, columnspan=6)



