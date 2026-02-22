import os
from tkinter import *
from tkinter import ttk,messagebox
import sqlite3
from PIL import Image, ImageTk
import random
from datetime import datetime
from server_statistick import update_file
import customtkinter as ctk
from logtofile import log_to_file
from send_email_template import send
from transactions import transactions
from create_window import create_window
from save_and_load_balance import save_balance,load_balance

svb_coins = 0
os.makedirs("trade", exist_ok=True)
def check_ach(lang,start_time_):
    global svb_coins
    svb_coins = load_balance(start_time_)

    conn = sqlite3.connect("achievements.db")
    cursor = conn.cursor()

    cursor.execute("SELECT name, status, max, prize FROM achievements")
    rows = cursor.fetchall()

    for name, status, max_val, prize in rows:
        if status == "no" and svb_coins >= max_val:
            svb_coins += int(prize)
            send('receipt', int(prize))
            update_file("count_svbcoins.txt", int(prize))
            save_balance(svb_coins,start_time_)

            cursor.execute(
                "UPDATE achievements SET current = ?, status = ? WHERE name = ?",
                (svb_coins, "yes", name)
            )
            conn.commit()
            messagebox.showinfo(lang["success"], lang["ach_tr"] + str(prize))

    conn.close()
os.makedirs("trade", exist_ok=True)
def trade(actives_programs,lang,root,start_time_,global_bg,global_fg,GlobalAlpha):
    crypto_labels = []
    def export_portfolio():
        if os.path.exists("trade/portfolio.cfg"):
            log_to_file("Export portfolio",start_time_ = start_time_)
            with open("trade/portfolio.cfg", "r", encoding="utf-8") as f:
                data = f.read()
            with open("trade/portfolio_export.csv", "w", encoding="utf-8") as f_out:
                f_out.write("Name,Price\n")
                lines = data.strip().split("\n")
                for i in range(0, len(lines), 2):
                    name = lines[i].split("=")[1]
                    price = lines[i + 1].split("=")[1]
                    f_out.write(f"{name},{price}\n")
            messagebox.showinfo(lang["success"], lang["exp"],parent=Win)
    def refresh_prices():
        for label, item in crypto_labels:
            try:
                item["Price"] = random.randint(item["Min"], item["Max"])
                label.config(text=f"{item['Name']} - {item['Price']} SVB Coins")
            except Exception as e:
                pass
        try:
            update_my_crypto_ui()
        except Exception as e:
            pass
        create_crypto_ui()
        Win.after(10000, refresh_prices)
    def create_crypto_ui():
        crypto_labels.clear()
        for widget in crypto_frame.winfo_children():
            widget.destroy()
        for item in crypto:
            image = Image.open(f"icons/trade/{item['Name'].lower()}.png")
            photo = ImageTk.PhotoImage(image.resize((20, 20)))
            lbl = Label(crypto_frame, image=photo, bg="white")
            lbl.image = photo
            lbl.pack()
            label = Label(crypto_frame, text=f"{item['Name']} - {item['Price']} SVB Coins", font=("Arial", 11, "bold"),bg = global_bg,fg = global_fg)
            label.pack()
            crypto_labels.append((label, item))
            ttk.Button(crypto_frame, text=lang["buy"],
                       command=lambda n=item["Name"], p=item["Price"]: buy(n, p)).pack()
    def takeprofit(name):
        def pr(name,p):
            if int(p) > 100 or int(p) < 0:
                messagebox.showerror(lang["error"],lang["profit_b"],parent=w)
            else:
                try:
                    with open(f"trade/profit_{name}.cfg","w") as f:
                        f.write(f"NAME={name}\nPROFIT={p}")

                        f.close()
                    w.destroy()
                except Exception as e:
                    messagebox.showerror(lang["error"],lang["profit_false"] + str(e),parent=w)
        w = Toplevel(Win)
        w = create_window(Win, "Take Profit", global_bg, float(GlobalAlpha), 300, 200, "icons/trade.png")
        w.resizable(False,False)
        Label(w,text = lang["enter_profit"],bg = global_bg,fg = global_fg).pack()
        p = ctk.CTkEntry(w,placeholder_text=lang['enter_profit'])
        p.pack()
        ttk.Button(w,text = lang["podtver"],command = lambda:pr(name,p.get())).pack()
    def is_profit(name):
        config = {}
        if os.path.exists(f"trade/profit_{name}.cfg"):
            with open(f"trade/profit_{name}.cfg", "r", encoding='utf-8') as f:
                for line in f:
                    key2, value1 = line.strip().split("=")
                    config[key2] = value1
            name = config.get("NAME")
            prof = config.get("PROFIT")
            return name, prof
        else:
            return "None"
    def buy(name,price):
        os.makedirs("trade", exist_ok=True)
        global svb_coins
        svb_coins = load_balance(start_time_)
        if svb_coins >= int(price):
            svb_coins -= int(price)
            send('payement', int(price))
            transactions(f"-{price} SVb Coins" + f"{datetime.now()}",start_time_)
            save_balance(svb_coins,start_time_)
            if os.path.exists('trade/portfolio.cfg'):
                try:
                    with open('trade/portfolio.cfg',"a",encoding="utf-8") as f:
                        f.write(f"NAME={name}\nPRICE={price}\n")
                        f.close()
                    messagebox.showinfo(lang["success"],lang["buy_cr_true"] + name,parent=Win)
                    try:
                        balance_label.config(text=f"{lang['balance_cr']}: {svb_coins} SVB Coins")
                    except:
                        pass
                    if messagebox.askyesno("",lang["profit"],parent=Win):
                        takeprofit(name)
                except Exception as e:
                    messagebox.showerror(lang["error"],lang["buy_cr_false"] + str(e),parent=Win)
            else:
                try:
                    with open('trade/portfolio.cfg', "w", encoding="utf-8") as f:
                        f.write(f"NAME={name}\nPRICE={price}\n")
                        f.close()
                    messagebox.showinfo(lang["success"], lang["buy_cr_true"] + name,parent=Win)
                    try:
                        balance_label.config(text=f"{lang['balance_cr']}: {svb_coins} SVB Coins")
                    except:
                        pass
                    if messagebox.askyesno("",lang["profit"],parent=Win):
                        takeprofit(name)
                except Exception as e:
                    messagebox.showerror(lang["error"],lang["buy_cr_false"] + str(e),parent=Win)

        else:
            messagebox.showerror(lang["error"],lang["no_svb"],parent=Win)
    def get_prices(crypto,name):
        for item in crypto:
            if item["Name"] == name:
                return item["Price"]
    def prod(index, price,profit=False,name="None"):
        global svb_coins
        try:
            with open("trade/portfolio.cfg", "r", encoding="utf-8") as f:
                lines = [line.strip() for line in f.readlines()]
            blocks = [lines[i:i + 3] for i in range(0, len(lines), 3)]
            if 0 <= index < len(blocks):
                del blocks[index]
            with open("trade/portfolio.cfg", "w", encoding="utf-8") as f:
                for block in blocks:
                    for line in block:
                        f.write(line + "\n")
            svb_coins = load_balance(start_time_)
            svb_coins += int(price)
            send('receipt', int(price))
            update_file("count_svbcoins.txt", int(price))
            save_balance(svb_coins,start_time_)
            check_ach(lang,start_time_)
            transactions(f"+{price} SVB Coins | {datetime.now()}",start_time_)
            messagebox.showinfo(lang["success"], lang["prod-true"],parent=Win)
            if profit:
                if os.path.exists(f"trade/profit_{name}.cfg"):
                    os.remove(f"trade/profit_{name}.cfg")

            if balance_label.winfo_exists():
                balance_label.config(text=f"{lang['balance_cr']}: {svb_coins} SVB Coins")
            else:
                pass
        except Exception as e:
            messagebox.showerror(lang["error"], lang["prod-false"] + str(e),parent=Win)
    def update_my_crypto_ui():
        for widget in my_crypto_frame.winfo_children():
            widget.destroy()
        if os.path.exists('trade/portfolio.cfg'):
            my_cr_name = []
            my_cr_price = []
            prices = []
            percents = []

            with open("trade/portfolio.cfg", "r", encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("NAME="):
                        name = line.split("=", 1)[1]
                        my_cr_name.append(name)
                    if line.startswith("PRICE="):
                        price = line.split("=", 1)[1]
                        my_cr_price.append(price)
            for n in my_cr_name:
                prices.append(get_prices(crypto, n))
            for new, old in zip(prices, my_cr_price):
                result = ((int(new) - int(old)) / int(old)) * 100
                percents.append(result)
            for index, (name, my_price, percent, market_price) in enumerate(
                    zip(my_cr_name, my_cr_price, percents, prices)):
                color = "green" if percent > 0 else "red"

                row_frame = Frame(my_crypto_frame,bg = global_bg)
                row_frame.pack(fill=X, padx=5, pady=2)

                Label(row_frame, text=f"{name} - {my_price} SVB Coins", font=("Arial", 12),bg = global_bg,fg = global_fg).pack(side=LEFT)
                Label(row_frame, text=f"{percent:.2f}%", fg=color, font=("Arial", 12),bg = global_bg).pack(side=LEFT, padx=10)
                ttk.Button(row_frame, text=lang["prodat"], command=lambda i=index, p=int(my_price): prod(i, p)).pack(side=RIGHT)

                try:
                    profit_info = is_profit(name)
                    if profit_info != "None":
                        n, p = profit_info
                        if name == n:
                            try:
                                if float(percent) >= float(p):
                                    prod(index, market_price, True, name)
                            except ValueError:
                                pass
                except Exception as e:
                    pass

            ttk.Button(my_crypto_frame, text=lang["export"], command=export_portfolio).pack()

    actives_programs.append("Trade")
    log_to_file("Trade launch",start_time_ = start_time_)
    Win = create_window(root, lang["trade"], global_bg, float(GlobalAlpha), 900, 900, "icons/trade.png")
    crypto = [
        {"Name": "BTC", "Price": random.randint(40000, 80000), "Min": 40000, "Max": 80000},
        {"Name": "ETH", "Price": random.randint(5000, 13000), "Min": 5000, "Max": 13000},
        {"Name": "USDT", "Price": random.randint(40000, 80000), "Min": 40000, "Max": 80000},
        {"Name": "BNB", "Price": random.randint(1000, 13000), "Min": 1000, "Max": 13000},
        {"Name": "SOL", "Price": random.randint(10000, 30000), "Min": 10000, "Max": 30000},
        {"Name": "XRP", "Price": random.randint(4000, 8000), "Min": 4000, "Max": 8000},
        {"Name": "USDC", "Price": random.randint(1000, 8000), "Min": 1000, "Max": 8000},
        {"Name": "ADA", "Price": random.randint(1000, 5000), "Min": 1000, "Max": 5000},
        {"Name": "DOGE", "Price": random.randint(2000, 7000), "Min": 2000, "Max": 7000},
        {"Name": "TON", "Price": random.randint(500, 1300), "Min": 500, "Max": 1300}
    ]


    crypto_frame = LabelFrame(Win,borderwidth=0.5,text=lang["crypt"],bg = global_bg,fg = global_fg)
    crypto_frame.pack(side = LEFT,fill=Y)
    my_crypto_frame = LabelFrame(Win, borderwidth=0.5,text=lang["my_crypt"],bg = global_bg,fg = global_fg)
    my_crypto_frame.pack(side = RIGHT,fill=Y)
    global svb_coins
    svb_coins = load_balance(start_time_)
    balance_label = Label(my_crypto_frame, text=f"{lang['balance_cr']} {svb_coins} SVB Coins", font=("Arial", 14, "bold"),bg = global_bg,fg = global_fg)
    balance_label.pack(pady=10)

    create_crypto_ui()
    update_my_crypto_ui()
    refresh_prices()




