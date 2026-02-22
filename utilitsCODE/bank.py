from tkinter import *
from tkinter import ttk,messagebox,simpledialog
import logging
from PIL import Image, ImageTk, ImageDraw
import os
from datetime import datetime
import sqlite3
from send_email import send_email
import customtkinter as ctk
from play_sound import play_sound
from copy_file_to_folder import copy_file_to_folder
from crypto_work import load_key,decrypt_message,encrypt_message
from logtofile import log_to_file
from send_email_template import send
from transactions import transactions
from save_and_load_balance import save_balance,load_balance

target = 0
target_s = 0
count = 0
level_svb = 0
SYSTEM_LEVEL = 25
logging.addLevelName(SYSTEM_LEVEL, "SYSTEM")
svb_coins = 0
os.makedirs("bank", exist_ok=True)
tooltip = None
def show_tooltip(event, txt):
    global tooltip
    if tooltip:
        return

    x = event.widget.winfo_rootx() + 20
    y = event.widget.winfo_rooty() + event.widget.winfo_height() + 10

    tooltip = Toplevel()
    tooltip.wm_overrideredirect(True)
    tooltip.wm_geometry(f"+{x}+{y}")
    tooltip.configure(bg="#333333")

    label = Label(tooltip,
                  text=txt,
                  background="#fcfcfa",
                  foreground="#000000",
                  font=("Segoe UI", 10),
                  relief="solid",
                  borderwidth=1,
                  padx=8, pady=4)

    label.pack()

    try:
        tooltip.attributes("-alpha", 0.97)
        tooltip.attributes("-topmost", True)
    except:
        pass
def hide_tooltip(event):
    global tooltip
    if tooltip:
        tooltip.destroy()
        tooltip = None
def check_ach(lang,start_time_):
    global svb_coins
    

    conn = sqlite3.connect("achievements.db")
    cursor = conn.cursor()

    cursor.execute("SELECT name, status, max, prize FROM achievements")
    rows = cursor.fetchall()

    for name, status, max_val, prize in rows:
        if status == "no" and svb_coins >= max_val:
            svb_coins += int(prize)
            send('receipt', int(prize))
            save_balance(svb_coins,start_time_)

            cursor.execute(
                "UPDATE achievements SET current = ?, status = ? WHERE name = ?",
                (svb_coins, "yes", name)
            )
            conn.commit()
            messagebox.showinfo(lang["success"], lang["ach_tr"] + str(prize))

    conn.close()
def load_target():
    global target,target_s
    if os.path.exists("bank/target.cfg"):
        try:
            with open("bank/target.cfg", "r") as f:
                target = int(f.read())
                f.close()
            with open("bank/target_s.cfg","r") as f:
                target_s = int(f.read())
                f.close()
        except:
            pass
def save_card_balance(numer, balan):
    os.makedirs("bank", exist_ok=True)
    with open(f"bank/balance-{numer}.bin", "wb") as f:
        f.write(balan.to_bytes(4, byteorder='little', signed=True))

def level_dohod(act):
    try:
        key = load_key()
        with open('bank/updt.cfg', "rb") as f:
            encrypted_data = f.read()
        lvl = decrypt_message(encrypted_data, key)
    except Exception:
        pass

    level = 0
    dohod = 0

    if lvl and lvl.startswith("LEVEL="):
        try:
            level = int(lvl.split("=")[1])
            dohod = level * 1.75
        except ValueError:
            level = 0
            dohod = level * 1.75
    else:
        dohod = level * 1.75
    if act == "lvl":
        return level
    else:
        return dohod
def load_card_balance(num):
    try:
        with open(f"bank/balance-{num}.bin", "rb") as f:
            return int.from_bytes(f.read(4), byteorder='little', signed=True)
    except FileNotFoundError:
        return 0
def svbcoins(state_sound,volume,lang,root,errors,gl_police,actives_programs,edition,start_time_,global_bg,global_fg,GlobalAlpha):
    play_sound("sound//click.mp3", volume, state_sound, start_time_)
    def draw_gauge(size, value, maximum=100, start_angle=90, indicator_color='#00FF00', trough_color='#DCDCDC',
                   thickness=20):
        im = Image.new('RGBA', (size * 10, size * 10))
        draw = ImageDraw.Draw(im)
        bbox = (0, 0, size * 10 - 10, size * 10 - 10)
        draw.ellipse(bbox, outline=trough_color, width=thickness * 10)
        end_angle = int(value / maximum * 360) + start_angle
        draw.arc(bbox, start_angle, end_angle, fill=indicator_color, width=thickness * 10)
        return ImageTk.PhotoImage(im.resize((size, size), Image.BICUBIC))
    def kopilka():
        def create():
            def create2(target_):
                global target, target_s
                if target_.isdecimal():
                    with open('bank/target.cfg', "w") as f:
                        f.write(str(target_))
                    target = target_
                    target_s = 0
                    messagebox.showinfo(lang["success"], lang["target_created"],parent=w)
                else:
                    messagebox.showerror(lang["error"], lang["target_n"],parent=w)

            w = Toplevel(win)
            w.attributes("-alpha", float(GlobalAlpha))
            w.configure(bg=global_bg)
            w.geometry("400x300")
            w.title(lang["kopilka"])
            img = Image.open("icons/interface/kop.png")
            icon_image = ImageTk.PhotoImage(img)
            w.iconphoto(False, icon_image)
            Label(w, text=lang["enter_target"] + " SVB Coins", fg=global_fg, bg=global_bg).pack()
            target_entry = ctk.CTkEntry(w,placeholder_text=lang['enter_target'])
            target_entry.pack()
            ttk.Button(w, text=lang["create_kop"], command=lambda: create2(target_entry.get())).pack()

        def vivesti():
            global svb_coins, target_s, target
            try:
                svb_coins = load_balance(start_time_)
                svb_coins += target_s
                send('receipt', target_s)
                transactions(f"+{target_s} SVB Coins {datetime.now()}",start_time_)
                log_to_file(f'Svb coins += {target_s}', start_time_=start_time_)
                save_balance(svb_coins,start_time_)
                check_ach(lang, start_time_)
                os.remove("bank/target.cfg")
                os.remove("bank/target_s.cfg")
                messagebox.showinfo(lang["error"], lang["viv_tr"],parent=w)
            except Exception as e:
                messagebox.showerror(lang["error"], lang["error"] + ": " + str(e),parent=w)
                log_to_file("Error", level="error", start_time_=start_time_)

        if os.path.exists("bank/target.cfg"):
            global target, target_s
            w = Toplevel(win)
            w.configure(bg=global_bg)
            w.attributes("-alpha", float(GlobalAlpha))
            img = Image.open("icons/interface/kop.png")
            icon_image = ImageTk.PhotoImage(img)
            w.iconphoto(False, icon_image)
            w.title(lang['kopilka'])
            w.geometry('400x300')

            target_val = int(target)
            target_s_val = int(target_s)

            if target_s_val < target_val:
                gauge_img = draw_gauge(200, target_s_val, maximum=target_val, start_angle=90,thickness=20)
                label_gauge = Label(w, image=gauge_img, bg=global_bg)
                label_gauge.image = gauge_img
                label_gauge.pack()

                Label(w, text=lang["vipoln"] + str(target_s) + lang["iz"] + str(target), font=(gl_police, 13),
                      fg=global_fg, bg=global_bg).pack()
                Label(w, text=f"{target_s}/{target}", font=(gl_police, 13, "bold"), fg=global_fg, bg=global_bg).pack()
            else:
                Label(w, text=lang["target_v"], fg=global_fg, bg=global_bg).pack()
                Label(w, text=f"{target_s}/{target}", font=("Arial", 10, "bold"), fg=global_fg, bg=global_bg).pack()
                ttk.Button(w, text=lang["viv"], command=vivesti).pack()
        else:
            Win = Toplevel(win)
            Win.configure(bg=global_bg)
            Win.attributes("-alpha", float(GlobalAlpha))
            Win.geometry("500x400")
            Win.title(lang["kopilka"])
            img = Image.open("icons/interface/kop.png")
            icon_image = ImageTk.PhotoImage(img)
            Win.iconphoto(False, icon_image)
            Label(Win, text=lang["kopilka"], font=(gl_police, 13, "bold"), fg=global_fg, bg=global_bg).pack()
            ttk.Button(Win, text=lang["create_kop"], command=create).pack()
    def show_tr():
        w = Toplevel()
        w.title(lang["shw_tr"])
        w.geometry("500x400")
        w.attributes("-alpha", float(GlobalAlpha))
        w.configure(bg=global_bg)
        img = Image.open("icons/interface/transakt.png")
        icon_image = ImageTk.PhotoImage(img)
        w.iconphoto(False, icon_image)
        scrollbar = Scrollbar(w)
        scrollbar.pack(side=RIGHT, fill=Y)
        text = Text(w)
        text.pack()
        scrollbar.config(command=text.yview)
        content = ""
        if os.path.exists("syst_comp/transactions_hst.cache"):
            with open("syst_comp/transactions_hst.cache", "r") as f:
                content = f.read()
                f.close()
            text.insert(1.0, '--TRANSACTION HISTORY--\n')
            text.insert(END, str(content))
            text.config(state="disabled")
        else:
            text.insert(1.0, lang['no_hst'])
            text.config(state="disabled")
    def pop_kopilku():
        def popolnit(pr):
            global svb_coins, target_s
            svb_coins = load_balance(start_time_)
            if pr.isdecimal():
                if svb_coins >= int(pr):
                    svb_coins -= int(pr)
                    send('payement', int(pr))
                    transactions(f'{pr} SVB Coins' + f" {datetime.now()}",start_time_)
                    save_balance(svb_coins,start_time_)
                    target_s += int(pr)
                    try:
                        with open("bank/target_s.cfg", "w") as f:
                            f.write(str(target_s))
                            f.close()
                        messagebox.showinfo(lang["success"], lang["po_tr"] + str(pr),parent=w)
                    except Exception as e:
                        messagebox.showerror(lang["error"], lang["error"] + ": " + str(e),parent=w)
                else:
                    messagebox.showerror(lang["error"], lang["no_svb"],parent=w)
            else:
                messagebox.showerror(lang["error"], lang["ins"],parent=w)

        w = Toplevel(win)
        w.configure(bg=global_bg)
        w.title(lang['pop_kopilku'])
        w.attributes("-alpha", float(GlobalAlpha))
        w.geometry('400x300')
        img = Image.open("icons/interface/kop.png")
        icon_image = ImageTk.PhotoImage(img)
        w.iconphoto(False, icon_image)
        Label(w, text=lang["ent_summ"],fg = global_fg,bg = global_bg).pack()
        pr = ctk.CTkEntry(w,placeholder_text=lang['ent_summ'])
        pr.pack()
        ttk.Button(w, text=lang['pop_kopilku'], command=lambda: popolnit(pr.get())).pack()
    def add_card():
        log_to_file("ADD CARD",start_time_ = start_time_)
        global svb_coins
        svb_coins = load_balance(start_time_)
        from random import randint
        if svb_coins >= 5000:
            kolvo = 0
            if os.path.exists("card.db"):
                with open("bank/count.cfg", "r") as f:
                    kolvo = f.read().strip()
            if int(kolvo) == 8:
                messagebox.showerror(lang["error"], lang["max_card"],parent=win)
                log_to_file(f"Message: {lang['max_card']}", level="warning",start_time_ = start_time_)
            else:
                svb_coins -= 5000
                send('payement', 5000)
                transactions("-5.000 SVb Coins" + f" {datetime.now()}",start_time_)
                save_balance(svb_coins,start_time_)
                name_card = simpledialog.askstring(lang["add_c"], lang["card_n"])
                numer = randint(1000000000000000, 9999999999999999)
                cvv = randint(100, 999)
                da = f"{str(randint(1, 12)).zfill(2)}/{str(randint(1, 28)).zfill(2)}"
                log_to_file("number;cvv and date generated",start_time_ = start_time_)
                conn = sqlite3.connect("card.db")
                cursor = conn.cursor()
                cursor.execute("""INSERT INTO card_info (name, num, cvv, date) VALUES (?, ?, ?, ?)""",
                               (name_card, numer, cvv, da))
                conn.commit()
                log_to_file("Saved in DB",start_time_ = start_time_)
                with open('bank/count.cfg', "w") as f:
                    c = int(kolvo) + 1
                    f.write(str(c))
                log_to_file("Count updated",start_time_ = start_time_)
                save_card_balance(numer, 0)
                log_to_file("Global balance saved",start_time_ = start_time_)
                html_front = f"""
                    <div style="width:370px;height:220px;background:linear-gradient(135deg,#1e3c72,#2a5298);border-radius:20px;padding:25px;color:#fff;box-shadow:0 8px 25px rgba(0,0,0,0.3);border:4px solid #ffffff50;margin-bottom:40px;position:relative;">
                        <div style="position:absolute;top:20px;right:25px;font-size:20px;font-weight:bold;text-shadow:1px 1px 2px rgba(0,0,0,0.4);">SVB Bank</div>
                        <div style="width:50px;height:35px;background:linear-gradient(#ccc,#888);border-radius:6px;margin-bottom:25px;box-shadow:inset 0 0 3px #666;">
                            <div style="width:36px;height:4px;background:#666;margin:5px auto;border-radius:2px;"></div>
                            <div style="width:36px;height:4px;background:#666;margin:5px auto;border-radius:2px;"></div>
                            <div style="width:36px;height:4px;background:#666;margin:5px auto;border-radius:2px;"></div>
                        </div>
                        <h2 style="margin:0 0 20px 0;">VIRTUAL CARD</h2>
                        <div style="font-size:20px;margin-bottom:25px;letter-spacing:3px;">{numer}</div>
                        <div style="display:flex;justify-content:space-between;font-size:16px;">
                            <div>
                                <div style="opacity:0.8;">Valid Thru</div>
                                <div style="font-weight:bold;">{da}</div>
                            </div>
                            <div>
                                <div style="opacity:0.8;">CVV</div>
                                <div style="font-weight:bold;">{cvv}</div>
                            </div>
                        </div>
                    </div>
                """
                html_back = f"""
                    <div style="width:370px;height:220px;background:linear-gradient(135deg,#2a2a2a,#1e1e1e);border-radius:20px;padding:20px;color:#fff;box-shadow:0 8px 25px rgba(0,0,0,0.3);position:relative;">
                        <div style="width:100%;height:40px;background:#000;margin-bottom:30px;border-radius:4px;"></div>
                        <div style="background:#fff;color:#000;height:40px;border-radius:6px;padding:5px 10px;display:flex;justify-content:space-between;align-items:center;box-shadow:inset 0 0 4px rgba(0,0,0,0.2);">
                            <div style="font-style:italic;font-size:14px;">Authorized Signature</div>
                            <div style="font-weight:bold;color:#d00;font-size:16px;">{cvv}</div>
                        </div>
                        <div style="position:absolute;bottom:20px;left:20px;font-size:12px;opacity:0.6;line-height:1.4;">
                            If found, please contact your bank.<br>
                            SVB Bank Customer Service: 1-800-123-4567
                        </div>
                    </div>
                """
                conn = sqlite3.connect("configurations.db")
                cursor = conn.cursor()
                cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        first_name TEXT,
                                        last_name TEXT,
                                        email TEXT)""")
                conn.commit()
                cursor.execute("SELECT * FROM users")
                users = cursor.fetchall()
                if users:
                    user = users[0]
                    n, ln, e = user[1], user[2], user[3]
                else:
                    n = ln = e = "Unknown"
                try:
                    send_email(
                        to=str(e),
                        subject='SVB Bank',
                        html= f"""
                    <!DOCTYPE html>
                    <html>
                    <body style="font-family:sans-serif;background:#f3f3f3;padding:20px;">
                        <h2 style="text-align:center;">SVB Card</h2>
                        {html_front}
                        {html_back}
                    </body>
                    </html>""")
                    messagebox.showinfo(lang["success"], lang["card_buy"],parent=win)
                except Exception as ex:
                    messagebox.showerror(lang["error"], f"{errors[4]}\n\n{ex}")
                log_to_file("MSG send",start_time_ = start_time_)
                messagebox.showinfo(lang["success"], lang["card_buy"],parent=win)
                log_to_file(f"Messge: {lang['card_buy']}",start_time_ = start_time_)
        else:
            messagebox.showerror(lang["error"], lang["no_svb"],parent=win)
            log_to_file(f"Messge: {lang['no_svb']}", level="warning",start_time_ = start_time_)
    def delete_card():
        log_to_file("DELETE CARD",start_time_ = start_time_)
        name = simpledialog.askstring(lang["del_c"], lang["enter_cn"])
        if messagebox.askyesnocancel(lang['del_c'], lang["del_ask"],parent=win):
            conn = sqlite3.connect('card.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM card_info WHERE num=?", (name,))
            conn.commit()
            log_to_file("INFO CARD DELETED",start_time_ = start_time_)
            balance = load_card_balance(name)

            global svb_coins
            svb_coins = load_balance(start_time_)
            svb_coins += balance
            send('receipt', int(balance))
            transactions(f"+{balance} SVb Coins" + f" {datetime.now()}",start_time_)
            save_balance(svb_coins,start_time_)
            check_ach(lang,start_time_)
            log_to_file("Global balance saved",start_time_ = start_time_)
            try:
                os.remove(f"bank/balance-{name}.bin")
                log_to_file(f"File 'balance-{name}.bin' has been deleted",start_time_ = start_time_)
            except:
                pass
            with open("bank/count.cfg", "r") as f:
                kolvo = f.read().strip()
            kolvo = int(kolvo) - 1
            with open("bank/count.cfg", "w") as f:
                f.write(str(kolvo))
            log_to_file("Count updated",start_time_ = start_time_)
            messagebox.showinfo(lang["success"], lang["card_deleted_s"],parent=win)
            log_to_file(f'Message: {lang["card_deleted_s"]}',start_time_ = start_time_)
    def show_card():
        log_to_file("SHOW CARDS",start_time_ = start_time_)
        sh_win = Toplevel(win)
        sh_win.attributes("-alpha", float(GlobalAlpha))
        sh_win.configure(bg=global_bg)
        sh_win.geometry("500x500")
        img = Image.open("icons/interface/cardss.png")
        icon_image = ImageTk.PhotoImage(img)
        sh_win.iconphoto(False, icon_image)
        sh_win.title(lang["show_c"])
        sp = [lang["name"], lang["n"], "CVV", lang["d"]]
        balances = []
        conn = sqlite3.connect('card.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM card_info")
        rows = cursor.fetchall()
        log_to_file("INFO cards downloaded",start_time_ = start_time_)
        text = Text(sh_win)
        text.pack(expand=True, fill=BOTH)
        for row in rows:
            try:
                with open(f'bank/balance-{row[1]}.bin', "r") as f:
                    b = load_card_balance(row[1])
                    balances.append(str(b))
            except:
                balances.append("N/A")

        for i, row in enumerate(rows):
            name, number, cvv, date = row[0], row[1], row[2], row[3]
            text.insert(1.0, f'{lang["name"]} - {name}\n')
            text.insert(1.0, f'{lang["n"]} - {number}\n')
            text.insert(1.0, f'CVV - {cvv}\n')
            text.insert(1.0, f'{lang["d"]} - {date}\n')
            text.insert(1.0, f'{lang["bal"]} {balances[i]} \n')
            text.insert(1.0, '--------------------\n')
            log_to_file(f"INFO CARD {i} insert",start_time_ = start_time_)
        text.config(state="disabled")
    def perevod():
        log_to_file("PEREVOD (global-->card)",start_time_ = start_time_)
        global svb_coins
        svb_coins = load_balance(start_time_)
        num = simpledialog.askinteger(lang["enter_cn"], lang["enter_cn"])
        summa = simpledialog.askinteger(lang["enter_cn"], lang["suma"])
        log_to_file(f"CARD NUMBER = {num}",start_time_ = start_time_)
        log_to_file(f'SUMMA = {summa}',start_time_ = start_time_)
        if svb_coins >= summa:
            svb_coins -= summa
            send("receipt", summa)
            send('transaction', summa,card_from = "GLOBAL BALANCE",card_to = num)
            transactions(f"-{summa} SVb Coins" + f" {datetime.now()}",start_time_)
            log_to_file(f'SVB COINS -= {summa}',start_time_ = start_time_)
            save_balance(svb_coins,start_time_)
            log_to_file("Global balance saved",start_time_ = start_time_)
            save_card_balance(num, summa)
            messagebox.showinfo(lang["success"], lang["s"],parent=win)
        else:
            messagebox.showerror(lang["error"], lang["no_svb"],parent=win)
            log_to_file(f'Message {lang["no_svb"]}', level="warning",start_time_ = start_time_)
    def perevod_c_c():
        log_to_file("PEREVOD (CARD --> CARD)",start_time_ = start_time_)
        num = simpledialog.askinteger(lang["enter_cn"], lang["enter_cn"])
        num1 = simpledialog.askinteger(lang["enter_cn"], lang["enter_cn1"])
        summa = simpledialog.askinteger(lang["enter_cn"], lang["suma"])
        nummer1 = load_card_balance(num)
        log_to_file(f"CARD 1 NUMBER = {num}",start_time_ = start_time_)
        log_to_file(f"CARD 2 NUMBER = {num1}",start_time_ = start_time_)
        log_to_file(f'SUMMA = {summa}',start_time_ = start_time_)
        if nummer1 >= summa:
            nummer1 -= summa
            send("transaction", summa, card_from=num, card_to=num1)
            save_card_balance(num, nummer1)
            log_to_file(f"Balance of CARD-{num} saved",start_time_ = start_time_)
            try:
                with open(f'bank/balance-{num1}.bin', "r") as f:
                    s = f.read()
                su = summa + int(s)
                save_card_balance(num1, su)
            except:
                save_card_balance(num1, summa)

            messagebox.showinfo(lang["success"], lang["s"],parent=win)
            log_to_file(f'Message: {lang["s"]}',start_time_ = start_time_)
        else:
            messagebox.showerror(lang["error"], lang["no_svb"],parent=win)
            log_to_file(f'Message: {lang["no_svb"]}', level="warning",start_time_ = start_time_)
    def perevod_global():
        global svb_coins
        log_to_file("PEREVOD (CARD-->GLOBAL)",start_time_ = start_time_)
        svb_coins = load_balance(start_time_)
        num = simpledialog.askinteger(lang["enter_cn"], lang["enter_cn"])
        summa = simpledialog.askinteger(lang["enter_cn"], lang["suma"])
        log_to_file(f"CARD NUMBER = {num}",start_time_ = start_time_)
        log_to_file(f'SUMMA = {summa}',start_time_ = start_time_)
        nummer1 = load_card_balance(num)
        if nummer1 >= summa:
            nummer1 -= summa
            svb_coins += summa
            send("receipt",summa)
            send("transaction", summa,card_from = num,card_to = 'GLOBAL BALANCE')
            transactions(f"+{summa} SVb Coins" + f" {datetime.now()}",start_time_)
            save_balance(svb_coins,start_time_)
            check_ach(lang,start_time_)
            log_to_file("Global balace saved",start_time_ = start_time_)
            save_card_balance(num, nummer1)
            log_to_file('Card balance saved',start_time_ = start_time_)
            messagebox.showinfo(lang["success"], lang["s"],parent=win)
            log_to_file(f'Message: {lang["s"]}',start_time_ = start_time_)
        else:
            messagebox.showerror(lang["error"], lang["no_svb"],parent=win)
            log_to_file(f"Message: {lang['no_svb']}", level="warning",start_time_ = start_time_)
    def updt():
        def update(l, doh, curr, prc, c_lvl):
            global svb_coins, level_svb
            svb_coins = load_balance(start_time_)
            price_ = l * 10 * 1.8
            if svb_coins >= int(price_):
                t = l * 1.75
                dohod = level_dohod("d")
                svb_coins -= int(price_)
                send("payement", int(price_))
                transactions(f"-{int(price_)} SVb Coins" + f" {datetime.now()}",start_time_)
                save_balance(svb_coins,start_time_)
                try:
                    key = load_key()
                    encrypted_data = encrypt_message("LEVEL=" + str(l), key)
                    with open("bank/updt.cfg", "wb") as f:
                        f.write(encrypted_data)
                except Exception:
                    pass

                level_svb = l
                doh.config(text=lang['doh'] + " " + str(t))
                curr.config(text=lang['curr_doh'] + " " + str(dohod))
                prc.config(text=lang["prc_upd"] + f'{price_}')
                c_lvl.config(text=lang["curr_lvl"] + f' - {l}')
                winn.destroy()
                updt()
            else:
                messagebox.showerror(lang["error"], lang["no_svb"],parent=winn)
                log_to_file(f"Messge: {lang['no_svb']}", level="warning",start_time_ = start_time_)

        level = level_dohod("lvl")
        dohod = level_dohod("d")
        ftr_lvl = level + 1
        price = level * 10 * 1.8
        total_lvl = 55
        winn = Toplevel(win)
        winn.attributes("-alpha",float(GlobalAlpha))
        winn.configure(bg=global_bg)
        winn.geometry("500x400")
        winn.title(lang["upd"])
        img = Image.open("icons/interface/ul.png")
        icon_image = ImageTk.PhotoImage(img)
        winn.iconphoto(False, icon_image)
        Label(winn, text=lang["curr_lvl"] + ": " + str(level),fg = global_fg,bg = global_bg)
        if level < 55:
            Label(winn, text=str(level) + " / " + str(total_lvl), font=("Times", 12, "italic"),fg = global_fg,bg = global_bg).pack()
            doh = Label(winn, text=lang['doh'] + " " + str((level + 1) * 1.75), font=("Times", 11, "bold"),fg = global_fg,bg = global_bg)
            doh.pack()
            curr = Label(winn, text=lang['curr_doh'] + " " + str(dohod),fg = global_fg,bg = global_bg)
            curr.pack()
            prc = Label(winn, text=lang["prc_upd"] + f'{price}', font=("Times", 14, "bold"),fg = global_fg,bg = global_bg)
            prc.pack()
            c_lvl = Label(winn, text=f'{lang["curr_lvl"]}  - {level}', font=("Times", 19, "bold"),fg = global_fg,bg = global_bg)
            c_lvl.pack()
            ttk.Button(winn, text=lang["upd_btn"] + str(level + 1),
                       command=lambda: update(ftr_lvl, doh, curr, prc, c_lvl)).pack()
        else:
            Label(winn, text=str(level) + " / " + str(total_lvl), font=("Times", 9, "italic"),fg = global_fg,bg = global_bg).pack()
            Label(winn, text=lang['doh'] + " " + str((level + 1) * 1.75), font=("Times", 11, "bold"),fg = global_fg,bg = global_bg).pack()
            Label(winn, text=lang['curr_doh'] + " " + str(dohod),fg = global_fg,bg = global_bg).pack()
            Label(winn, text=f'{lang["curr_lvl"]}  - {level}', font=("Times", 19, "bold"),fg = global_fg,bg = global_bg).pack()
            Label(winn, text=lang['mxim'], font=("Arial", 22, "bold"),fg = global_fg,bg = global_bg).pack()
    def open_clicker():
        global svb_coins, count
        Winn = Toplevel(win)
        Winn.configure(bg=global_bg)
        Winn.attributes("-alpha",float(GlobalAlpha))
        Winn.geometry("300x300")
        Winn.title(lang["clicker"])
        img = Image.open("icons/b.png")
        icon_image = ImageTk.PhotoImage(img)
        Winn.iconphoto(False, icon_image)
        log_to_file("Clicker opened",start_time_ = start_time_)

        def vivod():
            global svb_coins, count
            svb_coins += int(count)
            send("receipt", int(count))
            transactions(f"+{int(count)} SVb Coins" + f" {datetime.now()}",start_time_)
            log_to_file(f"Withdrawal of funds: {count}",start_time_ = start_time_)
            messagebox.showinfo("", f'{lang["count_svb"]} {str(count)} {lang["coins"]}',parent=Winn)
            log_to_file(f"Message: {lang['count_svb'] + str(count) + lang['coins']}",start_time_ = start_time_)
            save_balance(svb_coins,start_time_)
            check_ach(lang,start_time_)
            count = 0
            log_to_file('Balance saved and counter reset',start_time_ = start_time_)
            lbl.config(text=lang["balance"] + str(svb_coins))
            Winn.destroy()

        def func(event):
            global count
            count += level_dohod('d')
            label.config(text=f"{lang['count_cl']}: {count}")

        label = Label(Winn, text=f"{lang['count_cl']}: 0", font=("Arial", 24),fg = global_fg,bg = global_bg)
        label.pack(expand=True)
        btn = ttk.Button(Winn, text=lang["viv"], command=vivod)
        btn.pack()
        Winn.bind("<Button-1>", func)

    global svb_coins, level_svb
    style1 = ttk.Style()
    style1.configure("Red1.TButton", background="darkred", foreground="red")
    style2 = ttk.Style()
    style2.configure("Blue1.TButton", background="darkblue", foreground="blue")
    style3 = ttk.Style()
    style3.configure("Violet1.TButton", background="#4B0082", foreground="#4B0082")
    style4 = ttk.Style()
    style4.configure("Violet2.TButton", background="#800080", foreground="#800080")

    counttt = 0
    total_count = 8
    level_svb = level_dohod("lvl")
    actives_programs.append("Bank")
    log_to_file("Bank launch",start_time_ = start_time_)
    svb_coins = load_balance(start_time_)
    log_to_file("Balance loaded",start_time_ = start_time_)
    win = Toplevel(root)
    win.attributes("-alpha",float(GlobalAlpha))
    win.configure(bg=global_bg)
    win.title(lang["bank"])
    img = Image.open("icons/b.png")
    icon_image = ImageTk.PhotoImage(img)
    win.iconphoto(False, icon_image)
    win.geometry("600x500")
    win.configure(background="white")

    win.trns = ImageTk.PhotoImage(Image.open("icons//interface//trns.png").resize((50, 50), Image.Resampling.LANCZOS))
    win.trns_hst = ImageTk.PhotoImage(Image.open("icons//interface//trns_hst.png").resize((50, 50), Image.Resampling.LANCZOS))
    win.kop = ImageTk.PhotoImage(Image.open("icons//interface//kopilka.png").resize((50, 50), Image.Resampling.LANCZOS))
    win.crds = ImageTk.PhotoImage(Image.open("icons//interface//cards.png").resize((50, 50), Image.Resampling.LANCZOS))
    win.topup = ImageTk.PhotoImage(Image.open("icons//interface//top_up.png").resize((50, 50), Image.Resampling.LANCZOS))
    win.delc = ImageTk.PhotoImage(Image.open("icons//interface//delete_card.png").resize((50, 50), Image.Resampling.LANCZOS))
    win.addc = ImageTk.PhotoImage(Image.open("icons//interface//add_card.png").resize((50, 50), Image.Resampling.LANCZOS))
    win.imp = ImageTk.PhotoImage(Image.open("icons//interface//improvement.png").resize((50, 50), Image.Resampling.LANCZOS))

    if os.path.exists("bank/count.cfg"):
        with open("bank/count.cfg", "r") as f:
            counttt = f.read()

    Label(win, text=lang["my_cards"] + str(counttt) + "/" + str(total_count),fg = global_fg,bg = global_bg).pack()
    formatted = f"{svb_coins:,}".replace(",", ".")
    lbl = Label(win, text=lang["balance"] + formatted + "$", font=("Arial", 24, "bold"),fg = global_fg,bg = global_bg)
    lbl.pack()
    main_frm = LabelFrame(win,text = lang["main_frm"])
    main_frm.pack()
    kop_frm = LabelFrame(win, text=lang["kop_frm"])
    kop_frm.pack()
    card_frm = LabelFrame(win, text=lang["card_frm"])
    card_frm.pack()

    btn = ttk.Button(main_frm, image=win.topup, command=open_clicker)
    btn.pack(side = LEFT)
    btn.bind("<Enter>", lambda event: show_tooltip(event, txt=lang["top_up"] + "💸"))
    btn.bind("<Leave>", hide_tooltip)
    btn1 = ttk.Button(main_frm, image=win.imp, command=updt)
    btn1.pack(side = LEFT)
    btn1.bind("<Enter>", lambda event: show_tooltip(event, txt=lang["upd"] + "📈"))
    btn1.bind("<Leave>", hide_tooltip)
    btn2 = ttk.Button(main_frm, image=win.addc, command=add_card)
    btn2.pack(side = LEFT)
    btn2.bind("<Enter>", lambda event: show_tooltip(event, txt=lang["add_c"] + "💳"))
    btn2.bind("<Leave>", hide_tooltip)
    btn3 = ttk.Button(main_frm, image=win.trns_hst, command=show_tr)
    btn3.pack(side = LEFT)
    btn3.bind("<Enter>", lambda event: show_tooltip(event, txt=f'{lang["shw_tr"]}🪙'))
    btn3.bind("<Leave>", hide_tooltip)
    btn4 = ttk.Button(main_frm, image=win.kop,command=kopilka)
    btn4.pack(side = LEFT)
    btn4.bind("<Enter>", lambda event: show_tooltip(event, txt=lang["kopilka"]))
    btn4.bind("<Leave>", hide_tooltip)

    if os.path.exists("bank/target.cfg"):
        btn5 = ttk.Button(kop_frm, image=win.kop, command=pop_kopilku)
        btn5.pack(side = LEFT)
        btn5.bind("<Enter>", lambda event: show_tooltip(event, txt=lang["pop_kopilku"]))
        btn5.bind("<Leave>", hide_tooltip)
    if os.path.exists("card.db"):
        btn6 = ttk.Button(card_frm, image=win.crds, command=show_card)
        btn6.pack(side = LEFT)
        btn6.bind("<Enter>", lambda event: show_tooltip(event, txt=lang["show_c"] + "💳"))
        btn6.bind("<Leave>", hide_tooltip)

        btn7 = ttk.Button(card_frm, image=win.trns, command=perevod)
        btn7.pack(side = LEFT)
        btn7.bind("<Enter>", lambda event: show_tooltip(event, txt=lang["perevod"] + "💰"))
        btn7.bind("<Leave>", hide_tooltip)

        btn8 = ttk.Button(card_frm, image=win.trns, command=perevod_c_c)
        btn8.pack(side = LEFT)
        btn8.bind("<Enter>", lambda event: show_tooltip(event, txt=lang["per_c_c"] + "💰"))
        btn8.bind("<Leave>", hide_tooltip)

        btn9 = ttk.Button(card_frm, image=win.trns, command=perevod_global)
        btn9.pack(side = LEFT)
        btn9.bind("<Enter>", lambda event: show_tooltip(event, txt=lang["per_gl"] + "💰"))
        btn9.bind("<Leave>", hide_tooltip)

        btn10 = ttk.Button(card_frm, image=win.delc, command=delete_card)
        btn10.pack(side = LEFT)
        btn10.bind("<Enter>", lambda event: show_tooltip(event, txt=lang["del_c"] + "🗑️"))
        btn10.bind("<Leave>", hide_tooltip)
load_target()