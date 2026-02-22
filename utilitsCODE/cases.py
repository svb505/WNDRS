from tkinter import *
from tkinter import messagebox
import sqlite3
from logger_setup import system_logger
import time
from copy_file_to_folder import copy_file_to_folder
import os
import logging
from datetime import datetime
import random
from PIL import Image, ImageTk
from server_statistick import update_file
from logtofile import log_to_file
from play_sound import play_sound
from send_email_template import send
from transactions import transactions
from save_and_load_balance import save_balance,load_balance

svb_coins = 0
SYSTEM_LEVEL = 25
logging.addLevelName(SYSTEM_LEVEL, "SYSTEM")
case_logger = logging.getLogger('case_logger')
case_logger.setLevel(logging.INFO)
case_handler = logging.FileHandler('case_rewards_log.log', encoding='utf-8')
case_handler.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
case_logger.addHandler(case_handler)


def check_ach(lang,start_time_):
    global svb_coins
    

    conn = sqlite3.connect("achievements.db")
    cursor = conn.cursor()

    # Получаем все достижения
    cursor.execute("SELECT name, status, max, prize FROM achievements")
    rows = cursor.fetchall()

    for name, status, max_val, prize in rows:
        if status == "no" and svb_coins >= max_val:
            svb_coins += int(prize)
            send('receipt',prize)
            update_file("count_svbcoins.txt", int(prize))
            save_balance(svb_coins,start_time_)

            cursor.execute(
                "UPDATE achievements SET current = ?, status = ? WHERE name = ?",
                (svb_coins, "yes", name)
            )
            conn.commit()
            messagebox.showinfo(lang["success"], lang["ach_tr"] + str(prize))

    conn.close()
def log_case(data):
    case_logger.info(data)
def log_system(msg,start_time_):
    try:
        elapsed = time.time() - start_time_
    except NameError:
        elapsed = 0
    formatted_msg = f"[{elapsed:.1f}] - {msg}"
    system_logger.log(SYSTEM_LEVEL, formatted_msg)
def cases(actives_programs,state_sound,volume,root,errors,edition,lang,start_time_,global_bg,global_fg,GlobalAlpha):
    actives_programs.append("Cases")
    play_sound("sound//click.mp3", volume, state_sound, start_time_)

    conn = sqlite3.connect('configurations.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS inventory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        rarity TEXT NOT NULL
    )
    ''')
    conn.commit()  # Сохраняем изменения
    if edition in ("Professional x64", "Gaming x64", "Professional x32", "Gaming x32"):
        copy_file_to_folder("configurations.db", "backup_data",start_time_)
    log_to_file('Case launch',start_time_ = start_time_)
    clr = ""
    if global_bg == 'white':
        clr = "black"
    else:
        clr = "white"
    rewards = [
        {"name": "50 SVB-Coins", "type": "coins", "value": 50, "chance": 0.35, "rarity": lang["default"],
         "color": clr},
        {"name": "100 SVB-Coins", "type": "coins", "value": 100, "chance": 0.2, "rarity": lang["default"],
         "color": clr},
        {"name": lang['theme_'], "type": "theme", "value": "dark_night", "chance": 0.1, "rarity": lang["no_def"],
         "color": "#1E90FF"},
        {"name": lang['anim'], "type": "animation", "value": "load_anim", "chance": 0.07, "rarity": lang["rare"],
         "color": "#8A2BE2"},
        {"name": lang["epick_back"], "type": "background", "value": "exclusive_wallpaper", "chance": 0.03,
         "rarity": lang["epick"], "color": "#FFD700"},
        {"name": lang['galaxy'], "type": "theme", "value": "galaxy", "chance": 0.03, "rarity": lang["epick"],
         "color": "#FFD700"},
        {"name": lang['galaxy_'], "type": "theme", "value": "galaxy", "chance": 0.01, "rarity": lang["epick"],
         "color": "#FFD700"},
        {"name": "10.000 SVB-Coins", "type": "coins", "value": 10000, "chance": 0.01, "rarity": lang["epick"],
         "color": "#FFD700"},
    ]
    log_to_file("Rewards loaded",start_time_ = start_time_)

    def get_random_reward():
        roll = random.random()
        cumulative = 0
        for reward in rewards:
            cumulative += reward["chance"]
            if roll <= cumulative:
                return reward
        return rewards[0]

    def log_reward_to_file(text):
        log_case(f'{datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")} - {text}')
        log_to_file(f'{datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")} - {text}',start_time_ = start_time_)

    def add_reward_to_inventory(reward_name, reward_rarity):
        # Проверяем, есть ли уже этот предмет в базе
        cursor.execute("SELECT * FROM inventory WHERE name = ?", (reward_name,))
        existing_item = cursor.fetchone()
        if existing_item:
            return False  # Предмет не добавлен
        else:
            # Если предмета нет, добавляем его в базу
            cursor.execute("INSERT INTO inventory (name, rarity) VALUES (?, ?)", (reward_name, reward_rarity))
            conn.commit()  # Сохраняем изменения
            return True  # Предмет добавлен

    def open_case_visual():
        def spin():
            global svb_coins
            svb_coins = load_balance(start_time_)
            if svb_coins > 100:
                svb_coins -= 100
                send("payement",100)
                transactions("-100 SVb Coins" + f" {datetime.now()}",start_time_ = start_time_)
                save_balance(svb_coins,start_time_)
                log_to_file("SVB Coins -= 100",start_time_ = start_time_)
                log_to_file("Spin",start_time_ = start_time_)
                label.config(text=lang["kr"],bg = global_bg,fg = global_fg)
                spin_button.config(state="disabled")
                balance_label.config(text=f"{lang['balance']} {svb_coins} SVB",bg = global_bg,fg = global_fg)
                spin_sequence = [random.choice(rewards) for _ in range(30)]
            else:
                messagebox.showinfo(lang["error"], lang["no_svb"],parent = window)

            def animate(index=0):
                if index < len(spin_sequence):
                    current = spin_sequence[index]
                    label.config(text=current["name"], fg=current["color"])
                    window.after(100 + index * 5, lambda: animate(index + 1))
                else:
                    reward = get_random_reward()
                    final_reward(reward)

            animate()

        def final_reward(reward):
            global svb_coins
            svb_coins = load_balance(start_time_)
            play_sound("sound//tada.mp3", volume, state_sound, start_time_)
            reward_text = ""
            if reward["type"] == "coins":
                svb_coins += reward["value"]
                send('receipt',reward["value"])
                update_file("count_svbcoins.txt", int(reward["value"]))
                transactions(f"+{reward['value']} SVb Coins" + f" {datetime.now()}",start_time_ = start_time_)
                save_balance(svb_coins,start_time_)
                check_ach(lang,start_time_)
                reward_text = f"{lang['pol']} {reward['name']} (+{reward['value']} SVB)"
                log_to_file(reward_text,start_time_ = start_time_)
                log_reward_to_file(reward_text)
            else:
                # Добавление предмета в инвентарь с проверкой на дублирование
                if not add_reward_to_inventory(reward["name"], reward["rarity"]):
                    comp_value = 75  # Компенсация
                    svb_coins += comp_value
                    send('receipt', comp_value)
                    update_file("count_svbcoins.txt", int(comp_value))
                    transactions(f"+{comp_value} SVb Coins" + f" {datetime.now()}",start_time_ = start_time_)
                    save_balance(svb_coins,start_time_)
                    check_ach(lang,start_time_)
                    reward_text = f"{reward['name']} {lang[('comp')]} {comp_value} SVB"
                    log_reward_to_file(f"{lang['dable']} {reward['name']} | {lang['cm']} {comp_value} SVB")
                    log_to_file(reward_text,start_time_ = start_time_)
                else:
                    reward_text = f"{lang['new-pr']} {reward['name']} ({reward['rarity']})"
                    log_reward_to_file(f"{lang['polucheno']} {reward['name']} | {lang['redc']} {reward['rarity']}")

            label.config(text=reward_text, fg=reward["color"])
            balance_label.config(text=f"{lang['balance']} {svb_coins} SVB",bg = global_bg,fg = global_fg)
            spin_button.config(state="normal")

        window = Toplevel(root)
        window.attributes("-alpha", float(GlobalAlpha))
        window.attributes('-topmost', True)
        window.config(bg=global_bg)
        img = Image.open("icons/cases.png")
        icon_image = ImageTk.PhotoImage(img)
        window.iconphoto(False, icon_image)
        window.geometry("550x280")
        window.title(lang["case"])

        label = Label(window, text=lang["tap"], font=("Arial", 16),bg = global_bg,fg = global_fg)
        label.pack(pady=20)

        spin_button = Button(window, text=lang["open_case"] + "\n 100 SVB Coins", command=spin, font=("Arial", 14))
        spin_button.pack(pady=10)

        global balance_label, svb_coins
        svb_coins = load_balance(start_time_)
        balance_label = Label(window, text=f"{lang['balance']} {svb_coins} SVB", font=("Arial", 12),bg = global_bg,fg = global_fg)
        balance_label.pack(pady=10)

    open_case_visual()

    # Закрываем подключение к базе данных
    conn.close()