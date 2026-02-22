from tkinter import *
from tkinter import ttk,messagebox
from logger_setup import system_logger
import logging
import time
from datetime import datetime
import os
import random
import sqlite3
from PIL import Image, ImageTk
import string
from send_email import send_email
import customtkinter as ctk
from logtofile import log_to_file
from copy_file_to_folder import copy_file_to_folder
from send_email_template import send
from transactions import transactions
from create_window import create_window
from save_and_load_balance import save_balance,load_balance

SYSTEM_LEVEL = 25
logging.addLevelName(SYSTEM_LEVEL, "SYSTEM")
svb_coins = 0


def log_system(msg,start_time_):
    try:
        elapsed = time.time() - start_time_
    except NameError:
        elapsed = 0
    formatted_msg = f"[{elapsed:.1f}] - {msg}"
    system_logger.log(SYSTEM_LEVEL, formatted_msg)
def buy_num(lang,root,edition,errors,start_time_,global_bg,global_fg,GlobalAlpha):
    def confirm(var, brand, model, year, vin):
        global svb_coins
        from faker import Faker
        svb_coins = load_balance(start_time_)
        if svb_coins >= 3000:
            svb_coins -= 3000
            send('payement', 3000)
            transactions("-3.000 SVb Coins" + f" {datetime.now()}",start_time_ = start_time_)
            save_balance(svb_coins,start_time_)
            if var == "Україна":
                faker = Faker("uk_UA")
                numer = faker.license_plate()
                plate_class = "ukraine"
            elif var == "Россия":
                numer = f"{random.choice('АВЕКМНОРСТУХ')}{random.randint(100, 999)}{random.choice('АВЕКМНОРСТУХ')}{random.choice('АВЕКМНОРСТУХ')} {random.randint(1, 99)}"
                plate_class = "russia"
            elif var == "Britan":
                faker = Faker("en_GB")
                numer = f"{faker.random_uppercase_letter()}{faker.random_uppercase_letter()}{random.randint(10, 99)} {faker.random_uppercase_letter()}{faker.random_uppercase_letter()}{faker.random_uppercase_letter()}"
                plate_class = "uk"
            elif var == "France":
                faker = Faker("fr_FR")
                numer = f"{faker.random_uppercase_letter()}{faker.random_uppercase_letter()}-{random.randint(100, 999)}-{faker.random_uppercase_letter()}{faker.random_uppercase_letter()}"
                plate_class = "france"
            else:
                return

            if os.path.exists("plate.cfg"):
                with open("plate.cfg", "a", encoding='utf-8') as f:
                    f.write(f'PLATE={numer}\nBRAND={brand}\nMODEL={model}\nYEAR={year}\nVIN={vin}\n')
                if edition in ("Professional", "Gaming"):
                    copy_file_to_folder("plate.cfg", "backup_data",start_time_ = start_time_)
            else:
                with open("plate.cfg", "w", encoding='utf-8') as f:
                    f.write(f'PLATE={numer}\nBRAND={brand}\nMODEL={model}\nYEAR={year}\nVIN={vin}\n')
                if edition in ("Professional", "Gaming"):
                    copy_file_to_folder("plate.cfg", "backup_data",start_time_ = start_time_)
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
            try:
                send_email(
                    to=str(e),
                    subject="🔐 Your Plate",
                    html= f"""
                    <!DOCTYPE html>
                    <html lang="uk">
                    <head>
                        <meta charset="UTF-8">
                        <style>
                            .plate {{
                                display: inline-block;
                                padding: 10px 20px;
                                margin: 10px;
                                font-size: 24px;
                                font-family: 'Arial Black', sans-serif;
                                border: 2px solid #000;
                                border-radius: 8px;
                                background: #fff;
                            }}
                            .ukraine {{
                                background: linear-gradient(to right, #0057b7 0 10%, #ffd700 10% 20%, #fff 20% 100%);
                                color: #000;
                            }}
                            .uk {{
                                background-color: #fff;
                                color: #000;
                                border-left: 10px solid #00247d;
                            }}
                            .russia {{
                                background-color: #fff;
                                color: #000;
                                position: relative;
                            }}
                            .russia::after {{
                                content: "RUS";
                                position: absolute;
                                right: 10px;
                                bottom: 2px;
                                font-size: 12px;
                            }}
                            .france {{
                                background-color: #fff;
                                color: #000;
                                border-left: 10px solid #0055A4;
                                border-right: 10px solid #EF4135;
                            }}
                        </style>
                    </head>
                    <body>
                        <h2>Your plate ({var}):</h2>
                        <div class="plate {plate_class}">{numer}</div>
                        <p>
                            <strong>Brand:</strong> {brand}<br>
                            <strong>Model:</strong> {model}<br>
                            <strong>Year:</strong> {year}<br>
                            <strong>VIN:</strong> {vin}
                        </p>
                    </body>
                    </html>
                    """
                )
                messagebox.showinfo(lang["success"], lang["buy_s"],parent = win)
            except Exception as ex:
                messagebox.showerror(lang["error"], f"{errors[4]}\n\n{ex}",parent = win)
    def confirm1(var, brand, model, year, vin):
        def generate_russian_plate():
            letters = ''.join(random.choices(CYRILLIC_LETTERS, k=2))
            numbers = str(random.randint(1, 999)).zfill(3)
            region = str(random.choice([77, 78, 99, 97, 98]))
            last_letter = random.choice(CYRILLIC_LETTERS)
            return f"{letters}{numbers}{last_letter} {region}"
        def generate_ukrainian_plate():
            prefix = random.choice(["АА", "КА", "ВС", "СА", "ВН"])
            numbers = str(random.randint(0, 9999)).zfill(4)
            suffix = random.choice(["АА", "КН", "ІК", "СВ"])
            return f"{prefix}{numbers}{suffix}"
        def generate_uk_plate():
            area_code = ''.join(random.choices(LATIN_LETTERS, k=2))
            year_code = str(random.randint(0, 99)).zfill(2)
            random_letters = ''.join(random.choices(string.ascii_uppercase, k=3))
            return f"{area_code}{year_code} {random_letters}"

        def generate_french_plate():
            letters = ''.join(random.choices(string.ascii_uppercase, k=2))
            numbers = str(random.randint(0, 999)).zfill(3)
            suffix = ''.join(random.choices(string.ascii_uppercase, k=2))
            return f"{letters}-{numbers}-{suffix}"

        global svb_coins
        from faker import Faker
        CYRILLIC_LETTERS = "ЙЦУКЕНГШЩЗХФЫВАПРОЛДЖЯЧСМИТЬБЮ"
        LATIN_LETTERS = "AZERTYUIOPQSDFGHJKLMWXCVBN"

        svb_coins = load_balance(start_time_)
        if svb_coins >= 10000:
            svb_coins -= 10000
            send('payement', 10000)
            transactions("-10.000 SVb Coins" + f" {datetime.now()}",start_time_ = start_time_)
            save_balance(svb_coins,start_time_)
            if var == "Україна":
                faker = Faker("uk_UA")
                numer = generate_ukrainian_plate()
                plate_class = "ukraine"
            elif var == "Русский":
                numer = generate_russian_plate()
                plate_class = "russia"
            elif var == "Britan":
                faker = Faker("en_GB")
                numer = generate_uk_plate()
                plate_class = "uk"
            elif var == "France":
                numer = generate_french_plate()
                plate_class = "france"
            else:
                return

            if os.path.exists("plate.cfg"):
                with open("plate.cfg", "a", encoding='utf-8') as f:
                    f.write(f'PLATE={numer}\nBRAND={brand}\nMODEL={model}\nYEAR={year}\nVIN={vin}\n')
                if edition in ("Professional", "Gaming"):
                    copy_file_to_folder("plate.cfg", "backup_data",start_time_ = start_time_)
            else:
                with open("plate.cfg", "w", encoding='utf-8') as f:
                    f.write(f'PLATE={numer}\nBRAND={brand}\nMODEL={model}\nYEAR={year}\nVIN={vin}\n')
                if edition in ("Professional", "Gaming"):
                    copy_file_to_folder("plate.cfg", "backup_data",start_time_ = start_time_)
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
            try:
                send_email(
                    to=str(e),
                    subject="🔐 Your Plate",
                    html= f"""
                                   <!DOCTYPE html>
                                   <html lang="uk">
                                   <head>
                                       <meta charset="UTF-8">
                                       <style>
                                           .plate {{
                                               display: inline-block;
                                               padding: 10px 20px;
                                               margin: 10px;
                                               font-size: 24px;
                                               font-family: 'Arial Black', sans-serif;
                                               border: 2px solid #000;
                                               border-radius: 8px;
                                               background: #fff;
                                           }}
                                           .ukraine {{
                                               background: linear-gradient(to right, #0057b7 0 10%, #ffd700 10% 20%, #fff 20% 100%);
                                               color: #000;
                                           }}
                                           .uk {{
                                               background-color: #fff;
                                               color: #000;
                                               border-left: 10px solid #00247d;
                                           }}
                                           .russia {{
                                               background-color: #fff;
                                               color: #000;
                                               position: relative;
                                           }}
                                           .russia::after {{
                                               content: "RUS";
                                               position: absolute;
                                               right: 10px;
                                               bottom: 2px;
                                               font-size: 12px;
                                           }}
                                           .france {{
                                               background-color: #fff;
                                               color: #000;
                                               border-left: 10px solid #0055A4;
                                               border-right: 10px solid #EF4135;
                                           }}
                                       </style>
                                   </head>
                                   <body>
                                       <h2>Your plate ({var}):</h2>
                                       <div class="plate {plate_class}">{numer}</div>
                                       <p>
                                           <strong>Brand:</strong> {brand}<br>
                                           <strong>Model:</strong> {model}<br>
                                           <strong>Year:</strong> {year}<br>
                                           <strong>VIN:</strong> {vin}
                                       </p>
                                   </body>
                                   </html>
                                   """
                )
                messagebox.showinfo(lang["success"], lang["buy_s"],parent = win)
            except Exception as ex:
                messagebox.showerror(lang["error"], f"{errors[4]}\n\n{ex}",parent = win)
        else:
            messagebox.showerror(lang["error"], lang["no_svb"],parent = win)
            log_to_file(f"Message: {lang['no_svb']}", level="warning",start_time_ = start_time_)
    def confirm2(reg, brand, model, year, vin):
        def ok(n, reg, brand, model, year, vin):
            global svb_coins
            svb_coins = load_balance(start_time_)
            if svb_coins >= 15000:
                svb_coins -= 15000
                send('payement', 15000)
                transactions("-15.000 SVb Coins" + f" {datetime.now()}",start_time_ = start_time_)
                save_balance(svb_coins,start_time_)
                if var == "Україна":
                    plate_class = "ukraine"
                elif var == "Россия":
                    plate_class = "russia"
                elif var == "Britan":
                    plate_class = "uk"
                elif var == "France":
                    plate_class = "france"
                if os.path.exists("plate.cfg"):
                    with open("plate.cfg", "a", encoding='utf-8') as f:
                        f.write(f'PLATE={n}\nBRAND={brand}\nMODEL={model}\nYEAR={year}\nVIN={vin}\n')
                    if edition in ("Professional", "Gaming"):
                        copy_file_to_folder("plate.cfg", "backup_data",start_time_ = start_time_)
                else:
                    with open("plate.cfg", "w", encoding='utf-8') as f:
                        f.write(f'PLATE={n}\nBRAND={brand}\nMODEL={model}\nYEAR={year}\nVIN={vin}\n')
                    if edition in ("Professional", "Gaming"):
                        copy_file_to_folder("plate.cfg", "backup_data",start_time_ = start_time_)
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
                try:
                    send_email(
                        to=str(e),
                        subject="🔐 Your Plate",
                        html= f"""
                                   <!DOCTYPE html>
                                   <html lang="uk">
                                   <head>
                                       <meta charset="UTF-8">
                                       <style>
                                           .plate {{
                                               display: inline-block;
                                               padding: 10px 20px;
                                               margin: 10px;
                                               font-size: 24px;
                                               font-family: 'Arial Black', sans-serif;
                                               border: 2px solid #000;
                                               border-radius: 8px;
                                               background: #fff;
                                           }}
                                           .ukraine {{
                                               background: linear-gradient(to right, #0057b7 0 10%, #ffd700 10% 20%, #fff 20% 100%);
                                               color: #000;
                                           }}
                                           .uk {{
                                               background-color: #fff;
                                               color: #000;
                                               border-left: 10px solid #00247d;
                                           }}
                                           .russia {{
                                               background-color: #fff;
                                               color: #000;
                                               position: relative;
                                           }}
                                           .russia::after {{
                                               content: "RUS";
                                               position: absolute;
                                               right: 10px;
                                               bottom: 2px;
                                               font-size: 12px;
                                           }}
                                           .france {{
                                               background-color: #fff;
                                               color: #000;
                                               border-left: 10px solid #0055A4;
                                               border-right: 10px solid #EF4135;
                                           }}
                                       </style>
                                   </head>
                                   <body>
                                       <h2>Your plate ({var}):</h2>
                                       <div class="plate {plate_class}">{n}</div>
                                       <p>
                                           <strong>Brand:</strong> {brand}<br>
                                           <strong>Model:</strong> {model}<br>
                                           <strong>Year:</strong> {year}<br>
                                           <strong>VIN:</strong> {vin}
                                       </p>
                                   </body>
                                   </html>
                                   """
                    )
                    messagebox.showinfo(lang["success"], lang["buy_s"],parent = winn)
                except Exception as ex:
                    messagebox.showerror(lang["error"], f"{errors[4]}\n\n{ex}",parent = winn)
            else:
                messagebox.showerror(lang["error"], lang["no_svb"],parent = winn)
                log_to_file(f"Message: {lang['no_svb']}", level="warning",start_time_ = start_time_)

        winn = create_window(win,lang["pokup_n"],global_bg,float(GlobalAlpha),300,200,"icons/auto plate.png")
        Label(winn, text=lang["enter_number"],bg=global_bg,fg=global_fg).pack()
        n = ctk.CTkEntry(winn,placeholder_text=lang['enter_number'])
        n.pack()
        ttk.Button(winn, text=lang["Apply"], command=lambda: ok(n.get(), reg, brand, model, year, vin))
    def show():
        winn = create_window(win,'',global_bg,float(GlobalAlpha),500,400,"icons/auto plate.png")
        plates = []
        vins = []
        models = []
        brands = []
        years = []
        text = Text(winn)
        text.pack()
        with open("plate.cfg", "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("PLATE="):
                    plate = line.split("=", 1)[1]
                    plates.append(plate)
                if line.startswith("BRAND="):
                    brand = line.split("=", 1)[1]
                    brands.append(brand)
                if line.startswith("MODEL="):
                    model = line.split("=", 1)[1]
                    models.append(model)
                if line.startswith("YEAR="):
                    y = line.split("=", 1)[1]
                    years.append(y)
                if line.startswith("VIN="):
                    vin = line.split("=", 1)[1]
                    vins.append(vin)

        for i, plate in enumerate(plates):
            text.insert(1.0,
                        f"Plate-{plates[i]} \n Brand-{brands[i]} \nModel-{models[i]} \nYear-{years[i]} \nVIN-{vins[i]} \n")
    win = create_window(root,lang["pokup_n"],global_bg,float(GlobalAlpha),600,500,"icons/auto plate.png")
    if os.path.exists("plate.cfg"):
        ttk.Button(win, text=lang["y_plates"], command=show).pack()
    reg = ["Русский", "Україна", "France", "Britan"]
    var = StringVar(value='Britan')
    Label(win, text=lang["reg"], font=("Arial", 16, "bold"),bg=global_bg,fg=global_fg).pack()
    Label(win, text=lang["brand"], font=("Arial", 16, "bold"),bg=global_bg,fg=global_fg).pack()
    en = ctk.CTkEntry(win,placeholder_text=lang['brand'])
    en.pack()
    Label(win, text=lang["model"], font=("Arial", 16, "bold"),bg=global_bg,fg=global_fg).pack()
    en1 = ctk.CTkEntry(win,placeholder_text=lang['model'])
    en1.pack()
    Label(win, text=lang["year"], font=("Arial", 16, "bold"),bg=global_bg,fg=global_fg).pack()
    en2 = ctk.CTkEntry(win,placeholder_text=lang['year'])
    en2.pack()
    Label(win, text=lang["vin"], font=("Arial", 16, "bold"),bg=global_bg,fg=global_fg).pack()
    en3 = ctk.CTkEntry(win,placeholder_text=lang['vin'])
    en3.pack()
    ttk.Combobox(win, values=reg, textvariable=var).pack()
    ttk.Button(win, text=lang["b_num"],
               command=lambda: confirm(var.get(), en.get(), en1.get(), en2.get(), en3.get())).pack()
    ttk.Button(win, text=lang["b_num1"],
               command=lambda: confirm1(var.get(), en.get(), en1.get(), en2.get(), en3.get())).pack()
    ttk.Button(win, text=lang["b_num2"],
               command=lambda: confirm2(var.get(), en.get(), en1.get(), en2.get(), en3.get())).pack()