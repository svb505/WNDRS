import logging
from server_statistick import update_file
from logger_setup import system_logger
import time
from tkinter import *
from tkinter import messagebox
import random
from PIL import Image, ImageTk
from transactions import transactions
import sqlite3
from datetime import datetime
from logtofile import log_to_file
from play_sound import play_sound
from send_email_template import send
from save_and_load_balance import save_balance,load_balance

SYSTEM_LEVEL = 25
logging.addLevelName(SYSTEM_LEVEL, "SYSTEM")
count_casino = 5

def check_ach(lang,start_time_):
    global svb_coins
    load_balance(start_time_ = start_time_)

    conn = sqlite3.connect("achievements.db")
    cursor = conn.cursor()

    cursor.execute("SELECT name, status, max, prize FROM achievements")
    rows = cursor.fetchall()

    for name, status, max_val, prize in rows:
        if status == "no" and svb_coins >= max_val:
            svb_coins += int(prize)
            send('receipt', int(prize))
            update_file("count_svbcoins.txt", int(prize))
            save_balance(start_time_ = start_time_)

            # Обновляем достижение в базе
            cursor.execute(
                "UPDATE achievements SET current = ?, status = ? WHERE name = ?",
                (svb_coins, "yes", name)
            )
            conn.commit()
            messagebox.showinfo(lang["success"], lang["ach_tr"] + str(prize))

    conn.close()
def log_system(msg,start_time_):
    try:
        elapsed = time.time() - start_time_
    except NameError:
        elapsed = 0  # Если start_time_ нет, пишем 0 секунд
    formatted_msg = f"[{elapsed:.1f}] - {msg}"
    system_logger.log(SYSTEM_LEVEL, formatted_msg)
def open_casino(state_sound,volume,root,actives_programs,errors,lang,edition,start_time_,global_bg,global_fg,GlobalAlpha):
    play_sound("sound//click.mp3",volume,state_sound,start_time_)
    global count_casino
    actives_programs.append("Casino")
    symbols = ["🍒", "🍋", "🍊", "🍉", "⭐", "7️⃣"]
    log_to_file("Casino launch",start_time_ = start_time_)
    log_to_file(f'Attemps: {count_casino}',start_time_ = start_time_)
    messagebox.showinfo("", lang["chance"])

    def spin_reels():
        def animate_spin(step=0, max_steps=20):
            if step < max_steps:
                rdm()
                win.after(100, lambda: animate_spin(step + 1, max_steps))
            else:
                finish_spin()

        def rdm():
            label1.config(text=random.choice(symbols))
            label2.config(text=random.choice(symbols))
            label3.config(text=random.choice(symbols))

        def finish_spin():
            result = [random.choice(symbols) for _ in range(3)]
            label1.config(text=result[0])
            label2.config(text=result[1])
            label3.config(text=result[2])
            log_to_file(f"Result: {result[0]} {result[1]} {result[2]}",start_time_ = start_time_)
            win.after(500, lambda: show_result(result))  # Задержка перед результатом

        global count_casino
        if count_casino > 0:
            count_casino -= 1
            lbl.config(text=lang["popitka"] + ": " + str(count_casino))
            log_to_file(f'Attempts left: {count_casino}',start_time_ = start_time_)
            animate_spin()
        else:
            messagebox.showerror(lang["error"], lang["popitka_zak"],parent = win)
            log_to_file(f'Message: {lang["error"]}, {lang["popitka_zak"]}', level="warning",start_time_ = start_time_)
            log_to_file('Attempts over',start_time_ = start_time_)
    def show_result(result):
        global svb_coins
        if result[0] == result[1] == result[2]:
            play_sound("sound//win.mp3",volume,state_sound,start_time_)
            messagebox.showinfo(lang['win'], lang["message_win"] + " " + result[0] + " " + result[1] + " " + result[2],parent = win)
            messagebox.showinfo(lang['win'], "YOU WIN 10.000 SVB Coins",parent = win)
            log_to_file('Message: YOU WIN 10.000 SVB Coins',start_time_ = start_time_)
            log_to_file(f'Message: {lang["message_win"] + " " + result[0] + " " + result[1] + " " + result[2]}',start_time_ = start_time_)
            log_to_file("Win",start_time_ = start_time_)
            svb_coins = load_balance(start_time_)
            svb_coins += 10000
            send('receipt', 10000)
            update_file("count_svbcoins.txt", 10000)

            transactions("+10.000 SVb Coins" + f" {datetime.now()}",start_time_ = start_time_)
            save_balance(svb_coins,start_time_)
            check_ach(lang,start_time_)
            log_to_file('SVB coins += 10.000',start_time_ = start_time_)
        elif result[0] == result[1] or result[1] == result[2]:
            play_sound("sound//win.mp3",volume,state_sound,start_time_)
            messagebox.showinfo(lang['win'], lang["message_win"] + " " + result[0] + " " + result[1] + " " + result[2],parent = win)
            messagebox.showinfo(lang['win'], "YOU WIN 1.000 SVB Coins",parent = win)
            log_to_file('Message: YOU WIN 1.000 SVB Coins',start_time_ = start_time_)
            log_to_file(f'Message: {lang["message_win"] + " " + result[0] + " " + result[1] + " " + result[2]}',start_time_ = start_time_)
            log_to_file("Win",start_time_ = start_time_)
            load_balance(start_time_ = start_time_)
            svb_coins += 1000
            send('receipt', 1000)
            update_file("count_svbcoins.txt", 1000)

            transactions("+1.000 SVb Coins" + f" {datetime.now()}",start_time_ = start_time_)
            save_balance(start_time_ = start_time_)
            check_ach(lang,start_time_)
            log_to_file('SVB coins += 1.000',start_time_ = start_time_)
        else:
            play_sound("sound//Bubble5.mp3", volume, state_sound, start_time_)
            messagebox.showinfo(lang["lose"], lang['try_again'] + ' -100 SVB coins',parent = win)
            load_balance(start_time_ = start_time_)
            svb_coins -= 100
            send('payement', 100)
            transactions("-100 SVb Coins" + f" {datetime.now()}",start_time_ = start_time_)
            save_balance(start_time_ = start_time_)
            log_to_file(f"Message: {lang['try_again'] + ' -100 SVB coins'}",start_time_ = start_time_)
            log_to_file('Lose',start_time_ = start_time_)
    def kupit():
        log_to_file("Pay attemps with svb coins",start_time_ = start_time_)
        play_sound("sound//oldspice.mp3",volume,state_sound,start_time_)
        global svb_coins, count_casino
        load_balance(start_time_ = start_time_)
        if svb_coins > 300:
            svb_coins -= 300
            send('payement', 300)
            transactions("-300 SVb Coins" + f" {datetime.now()}",start_time_ = start_time_)
            log_to_file("Svb coins -= 300",start_time_ = start_time_)
            save_balance(start_time_ = start_time_)
            log_to_file("Balance saved",start_time_ = start_time_)
            count_casino += 5
            log_to_file("Attemps += 5",start_time_ = start_time_)
            messagebox.showinfo(lang["success"], lang["add_count"],parent = win)
            log_to_file(f"Message: {lang['add_count']}",start_time_ = start_time_)
        else:
            messagebox.showerror(lang["error"], lang["no_svb"],parent = win)
            log_to_file(f'Massage {lang["no_svb"]}', level="warning",start_time_ = start_time_)

    win = Toplevel(root)
    win.attributes("-alpha", float(GlobalAlpha))
    win.config(bg=global_bg)
    win.title(lang["__casino__"])
    win.geometry("400x300")
    img = Image.open("icons/casino.png")
    icon_image = ImageTk.PhotoImage(img)
    win.iconphoto(False, icon_image)
    # Метки для слотов
    label1 = Label(win, text="❓", font=("Arial", 32),bg = global_bg,fg = global_fg)
    label2 = Label(win, text="❓", font=("Arial", 32),bg = global_bg,fg = global_fg)
    label3 = Label(win, text="❓", font=("Arial", 32),bg = global_bg,fg = global_fg)

    # Кнопка SPIN
    spin_button = Button(win, text="SPIN", font=("Arial", 16), command=spin_reels)
    lbl = Label(win, text=lang["popitka"] + ": " + str(count_casino),bg = global_bg,fg = global_fg)
    lbl.pack()
    if count_casino == 0:
        spin_button = Button(win, text=lang["kupit"], font=("Arial", 16), command=kupit).pack()
    # Размещение элементов
    label1.pack(side=LEFT, expand=True)
    label2.pack(side=LEFT, expand=True)
    label3.pack(side=LEFT, expand=True)
    spin_button.pack(pady=10)