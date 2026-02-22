import random
from tkinter import *
from tkinter import ttk,messagebox
import sqlite3
from PIL import Image, ImageTk
import os
import json
from send_email import send_email
from logtofile import log_to_file
from crypto_work import decrypt_message,encrypt_message,load_key
from create_window import create_window
from send_email_template import send
from transactions import transactions
from save_and_load_balance import save_balance,load_balance

def check_activated():
    with open("store/prms.cfg","rb") as f:
        key = load_key()
        activated = decrypt_message(f.read().strip(),key)
    return activated

svb_coins = 0
SYSTEM_LEVEL = 25
sale = 1
bonus_promos = [
                "4GRKPK30", "7643DF3RF", "431TGV", "45G2F", "5GT41", "F3RCRZA", "T1FFD1", "F31C313", "81G3DB9XH",
                "P1RO3MOC1", "EXTRA2025", "SAVE4NOW", "WINNER77", "LUCKYME99", "PROMO2025", "DEALTIME22",
                "FREECODE1",
                "HOLIDAY88", "VIPBONUS7", "NEWYEAR25", "MAYSALE55", "GETREWARD", "MYPROMO33", "SPRINGFUN",
                "HELLOBONUS",
                "GIFTCODEX", "WELCOMESV", "SVB1000G", "TRYAGAIN7", "MEGABOOST", "HAPPYHOUR", "FASTREWARD",
                "UNLOCK50X",
                "SPEEDYWIN", "REDEEM2025", "TOPPROMO", "CASH4YOU", "OPENSESAME", "NICEDEAL", "CODE777", "KEY2WIN",
                "FREEENTRY", "BIGLUCK25", "DAILYTREASURE", "MYDAILYCODE", "PRIZEHUNT1", "GET50NOW", "POWERBONUS",
                "GAMETIME77", "LUCKYTICKET", "SVBGIFT", "NEXTPROMO", "WELCOME777", "HIDDENPRIZE", "PROMOMAGIC",
                "LOVECODE"
            ]
activated = check_activated()
conn = sqlite3.connect("configurations.db")
cursor = conn.cursor()
tooltip = None

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
    n, ln, email = user[1], user[2], user[3]
else:
    n = ln = email = "Unknown"
sale_percent = 0
cart = []
CART_FILE = "store/cart.json"


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
                  foreground="#000000",  # чёрный текст
                  font=("Segoe UI", 10),
                  relief="solid",
                  borderwidth=1,
                  padx=8, pady=4)

    label.pack()

    # Добавим скругление и лёгкую тень — опционально через Windows 11 эффекты (визуально)
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
def main_w(root,lang,edition,start_time_,global_bg,global_fg,GlobalAlpha):
    def open_products_window(root, lang, global_bg, global_fg, GlobalAlpha,title_key, window_icon,products_data):
        global sale_percent

        W = create_window(
            root,
            lang[title_key],
            global_bg,
            float(GlobalAlpha),
            600, 600,
            window_icon
        )

        sale = (100 - sale_percent) / 100

        frm1 = Frame(W)
        frm2 = Frame(W)
        frm3 = Frame(W)

        frm1.pack(side=LEFT, anchor="n")
        frm2.pack(side=LEFT, anchor="n")
        frm3.pack(side=LEFT, anchor="n")

        frames = [frm1, frm2, frm3]

        for idx, product in enumerate(products_data):
            frm = frames[idx // 3]

            img = ImageTk.PhotoImage(
                Image.open(product["icon"]).resize((52, 52), Image.Resampling.LANCZOS)
            )
            var = IntVar(value=1)
            price_value = int(product["price"] // sale)

            Label(frm, image=img).pack()
            Label(frm, text=lang[product["lang"]], bg=global_bg, fg=global_fg).pack()

            price_lbl = Label(
                frm,
                text=f"{lang['price_magaz']}:{price_value}",
                bg=global_bg,
                fg=global_fg
            )
            price_lbl.pack()

            base_price = int(product["price"] // sale)

            ttk.Spinbox(
                frm,
                from_=1,
                to=999,
                textvariable=var,
                command=lambda v=var, p=price_lbl, bp=base_price:
                change_price(p, bp, v.get())
            ).pack()

            ttk.Button(
                frm,
                text=lang["pay_prod"],
                command=lambda v=var, pid=product["id"], bp=base_price:
                pay(pid, v.get(), bp)
            ).pack()

            ttk.Button(
                frm,
                text=lang["add_cart"],
                command=lambda v=var, bp=base_price, name=lang[product["lang"]]:
                save_to_corz(name, bp, v.get())
            ).pack()


            setattr(W, f"_img_{idx}", img)
    def buy_all_cart():
        global svb_coins, email  # если они глобальные
        cart = load_cart()
        if not cart:
            messagebox.showinfo("", lang["cart_pust"],parent=Win)
            return

        svb_coins = load_balance(start_time_)
        total_sum = 0
        # Считаем итоговую сумму по всем товарам
        for item in cart:
            price = float(item.get("price", 0))
            kolvo = int(item.get("kolvo", 1))
            total_sum += price * kolvo

        if svb_coins < total_sum:
            messagebox.showerror(lang["error"], lang["no_svb"],parent=Win)
            return

        svb_coins -= int(total_sum)
        send('payement', int(total_sum))
        save_balance(svb_coins,start_time_)
        transactions(f'- {total_sum} SVB Coins',start_time_=start_time_)

        # Отправляем чек — например, все товары в одном письме
        # Собираем список товаров для письма
        products_info = ""
        for item in cart:
            name = item.get("name", "")
            kolvo = int(item.get("kolvo", 1))
            price = float(item.get("price", 0))
            products_info += f"<div>{name} — {kolvo} x {price}$ = {kolvo * price}$</div>"

        from datetime import datetime
        date = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

        send_email(
            to=str(email),
            subject=f"🧾 {lang['your_check']}",
            html= f"""
            <html>
              <body style="font-family: monospace; background-color: #f9f9f9; padding: 20px;">
                <div style="background-color: #fff; width: 400px; padding: 20px; border: 1px dashed #000; margin: auto;">
                  <h2 style="text-align: center;">{lang['store_name']}</h2>
                  <div style="text-align: center; font-size: 14px; margin-bottom: 10px;">{lang['date_']}: {date}</div>
                  {products_info}
                  <div style="margin-top: 20px; border-top: 1px dashed #000; padding-top: 10px; font-weight: bold;">
                    {lang["itogo"]}: {total_sum}$
                  </div>
                </div>
              </body>
            </html>
            """
        )

        save_cart([])

        messagebox.showinfo(lang["success"], lang["payement_succedd"],parent=Win)
    def load_cart():
        if os.path.exists(CART_FILE):
            with open(CART_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    def save_cart(cart_data):
        with open(CART_FILE, 'w', encoding='utf-8') as f:
            json.dump(cart_data, f, ensure_ascii=False, indent=2)
    def save_to_corz(name, price, kolvo):
        cart = load_cart()
        cart.append({"name": name, "price": price, "kolvo": kolvo})
        save_cart(cart)
        messagebox.showinfo(lang["success"],lang["saved_to_cart"],parent=Win)
    def open_corz():
        cart = load_cart()
        if not cart:
            messagebox.showinfo("", lang["cart_pust"], parent=Win)
            return

        window = create_window(root, lang['cart'], global_bg, float(GlobalAlpha), 600, 500)
        window.attributes('-topmost', True)

        window.grid_rowconfigure(0, weight=1)
        window.grid_columnconfigure(0, weight=1)

        # ===== Frame для Treeview + Scrollbar =====
        frame = ttk.Frame(window)
        frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        # ===== Treeview =====
        tree = ttk.Treeview(
            frame,
            columns=("name", "price", "kolvo", "sum"),
            show="headings"
        )

        tree.heading("name", text=lang["nazv"])
        tree.heading("price", text=lang["price"])
        tree.heading("kolvo", text=lang["kolvo_"])
        tree.heading("sum", text=lang["sum"])

        tree.column("name", width=200, anchor="w")
        tree.column("price", width=80, anchor="center")
        tree.column("kolvo", width=60, anchor="center")
        tree.column("sum", width=100, anchor="center")

        tree.grid(row=0, column=0, sticky="nsew")

        # ===== Scrollbar =====
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")

        tree.configure(yscrollcommand=scrollbar.set)

        # ===== Заполнение =====
        total_sum = 0
        for item in cart:
            name = item.get("name", "")
            price = float(item.get("price", 0))
            kolvo = int(item.get("kolvo", 1))
            summ = price * kolvo
            total_sum += summ

            tree.insert("", "end", values=(name, price, kolvo, summ))

        # ===== Итого =====
        label_total = Label(
            window,
            text=f"{lang['itogo']}: {total_sum:.2f} $",
            font=("Arial", 14, "bold"),
            bg=global_bg,
            fg=global_fg
        )
        label_total.grid(row=1, column=0, sticky="e", pady=10, padx=10)

        ttk.Button(window, text=lang['pay_all'], command=buy_all_cart).grid(row=2, column=0)
    def send_(email, name, qty, price, total):
        from datetime import datetime
        date = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

        send_email(
            to = str(email),
            subject = f"🧾 {lang['your_check']}",
            html =  f"""
            <html>
              <body style="font-family: monospace; background-color: #f9f9f9; padding: 20px;">
                <div style="background-color: #fff; width: 300px; padding: 20px; border: 1px dashed #000; margin: auto;">
                  <div style="text-align: center; margin-bottom: 20px;">
                    <h2 style="margin: 0;">{lang['store_name']}</h2>
                  </div>
                  <div style="text-align: center; font-size: 14px; margin-bottom: 10px;">{lang['date_']}: {date}</div>
                  <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                    <span>{name}</span>
                    <span> {qty} x {price}$</span>
                  </div>
                  <div style="margin-top: 20px; border-top: 1px dashed #000; padding-top: 10px; font-weight: bold;">
                    {lang["itogo"]}: {total}$
                  </div>
                </div>
              </body>
            </html>
            """
        )
    def pay(product_id, qty, base_price):
        global svb_coins, email
        load_balance(start_time_)

        total_price = int(base_price * qty)

        if svb_coins >= total_price:
            svb_coins -= total_price
            transactions(f'- {total_price} SVB Coins', start_time_=start_time_)
            save_balance(svb_coins,start_time_)
            send_(email, lang[product_id], qty, base_price, total_price)
            messagebox.showinfo(lang["success"], lang["payement_succedd"], parent=Win)
        else:
            messagebox.showerror(lang["error"], lang["no_svb"], parent=Win)
    def change_price(lbl, base_price, qty):
        total_price = int(base_price * qty)
        lbl.config(text=f"{lang['price_magaz']}:{total_price}")
    def promo():
        def polu():
            global bonus_promos,activated
            count = 0
            for b in bonus_promos:
                count += 1
            available = [b for b in bonus_promos if b not in activated]
            if not available:
                messagebox.showinfo(lang["error"], lang["no_bonus_left"],parent=Win)
                return
            bonus = random.choice(available)

            key = load_key()
            data = f"{bonus}\n"
            if os.path.exists("store/mypromos.cfg"):
                with open("store/mypromos.cfg",'ab') as f:
                    f.write(encrypt_message(data,key))
            else:
                with open("store/mypromos.cfg",'wb') as f:
                    f.write(encrypt_message(data,key))
            messagebox.showinfo(lang["success"],lang["bonus_activated"],parent=Win)
        def activate():
            def act(bns):
                global sale,sale_percent
                sale =  random.randint(2,20)
                sale_percent = sale
                key = load_key()
                with open("store/mypromos.cfg", "rb") as f:
                    data = decrypt_message(f.read().strip(), key)
                data = data.strip(bns)
                with open("store/mypromos.cfg", "wb") as f:
                    f.write(encrypt_message(data,key))
                messagebox.showinfo(lang["success"],lang["you_have_sale"] + str(sale_percent) + "%",parent=Win)
            www = create_window(root, lang['enter_bonus'], global_bg, float(GlobalAlpha), 300, 300)
            www.attributes('-topmost', True)

            Label(www,text = lang["enter_your_bonus"],bg = global_bg,fg= global_fg).pack()
            bns = ttk.Entry(www)
            bns.pack()

            ttk.Button(www,text = lang["activate2"],command = lambda:act(bns.get())).pack()
        w = create_window(root, lang['promo_mag'], global_bg, float(GlobalAlpha), 400, 300,"icons/products/promo.png")

        Label(w,text = lang["enter_promo_mag"],bg = global_bg,fg= global_fg).pack()
        promo = ttk.Entry(w)
        promo.pack()
        ttk.Button(w,text = lang["activate"],command = activate).pack()

        Label(w, text=lang["have_no_promos"],font = ('Arial',16,'bold'),bg = global_bg,fg= global_fg).pack()
        ttk.Button(w,text = lang["polu"],command = polu).pack()
    def show():
        w = create_window(Win, lang['show_promo'], global_bg, float(GlobalAlpha), 400, 300)

        key = load_key()
        with open("store/mypromos.cfg",'rb') as f:
            data = decrypt_message(f.read(),key).strip()

        text = Text(w,bg = global_bg,fg = global_fg)
        text.pack(expand = True,fill = BOTH)

        text.insert(1.0,data)
    def the():
        PRODUCTS = [
            {"id": "the1",
             "lang": "the1",
             "price": 150,
             "icon": "icons/products/the_1.png"},
            {"id": "the2",
             "lang": "the2",
             "price": 160,
             "icon": "icons/products/the_2.png"},
            {"id": "the3",
             "lang": "the3",
             "price": 120,
             "icon": "icons/products/the_3.png"},
            {"id": "the4",
             "lang": "the4",
             "price": 70,
             "icon": "icons/products/tea4.png"},
            {"id": "the5",
             "lang": "the5",
             "price": 88,
             "icon": "icons/products/tea5.png"},
            {"id": "the6",
             "lang": "the6",
             "price": 90,
             "icon": "icons/products/tea6.png"},
            {"id": "the7",
             "lang": "the7",
             "price": 430,
             "icon": "icons/products/tea7.png"},
            {"id": "the8",
             "lang": "the8",
             "price": 30,
             "icon": "icons/products/tea8.png"},
            {"id": "the9",
             "lang": "the9",
             "price": 155,
             "icon": "icons/products/tea9.png"},
        ]

        open_products_window(root, lang, global_bg, global_fg, GlobalAlpha, title_key="prod_mag",
                             window_icon="icons/products/tea4.png", products_data=PRODUCTS)
    def bitov():
        PRODUCTS = [
            {"id": "bitov1",
             "lang": "bitov1",
             "price": 1250,
             "icon": "icons/products/bitov_1.png"},
            {"id": "bitov2",
             "lang": "bitov2",
             "price": 3150,
             "icon": "icons/products/bitov_2.png"},
            {"id": "bitov3",
             "lang": "bitov3",
             "price": 1350,
             "icon": "icons/products/bitov_3.png"},
            {"id": "bitov4",
             "lang": "bitov4",
             "price": 1320,
             "icon": "icons/products/bitov4.png"},
            {"id": "bitov5",
             "lang": "bitov5",
             "price": 1210,
             "icon": "icons/products/bitov5.png"},
            {"id": "bitov6",
             "lang": "bitov6",
             "price": 1233,
             "icon": "icons/products/bitov6.png"},
            {"id": "bitov7",
             "lang": "bitov7",
             "price": 5430,
             "icon": "icons/products/bitov7.png"},
            {"id": "bitov8",
             "lang": "bitov8",
             "price": 3450,
             "icon": "icons/products/bitov8.png"},
            {"id": "bitov9",
             "lang": "bitov9",
             "price": 6350,
             "icon": "icons/products/bitov9.png"},
        ]

        open_products_window(root, lang, global_bg, global_fg, GlobalAlpha, title_key="prod_mag",
                             window_icon="icons/products/bitov4.png", products_data=PRODUCTS)
    def cofe():
        PRODUCTS = [
            {"id": "cofe1",
             "lang": "cofe1",
             "price": 150,
             "icon": "icons/products/cofe_1.png"},
            {"id": "cofe2",
             "lang": "cofe2",
             "price": 180,
             "icon": "icons/products/cofe_2.png"},
            {"id": "cofe3",
             "lang": "cofe3",
             "price": 50,
             "icon": "icons/products/cofe_3.png"},
            {"id": "cofe4",
             "lang": "cofe4",
             "price": 15,
             "icon": "icons/products/cofe4.png"},
            {"id": "cofe5",
             "lang": "cofe5",
             "price": 55,
             "icon": "icons/products/cofe5.png"},
            {"id": "cofe6",
             "lang": "cofe6",
             "price": 220,
             "icon": "icons/products/cofe6.png"},
            {"id": "cofe7",
             "lang": "cofe7",
             "price": 350,
             "icon": "icons/products/cofe7.png"},
            {"id": "cofe8",
             "lang": "cofe8",
             "price": 40,
             "icon": "icons/products/cofe8.png"},
            {"id": "cofe9",
             "lang": "cofe9",
             "price": 350,
             "icon": "icons/products/cofe9.png"},
        ]

        open_products_window(root, lang, global_bg, global_fg, GlobalAlpha, title_key="prod_mag",
                             window_icon="icons/products/cofe.png", products_data=PRODUCTS)
    def meat():
        PRODUCTS = [
            {"id": "meat1",
             "lang": "meat1",
             "price": 230,
             "icon": "icons/products/meat_1.png"},
            {"id": "meat",
             "lang": "meat2",
             "price": 320,
             "icon": "icons/products/meat_2.png"},
            {"id": "meat3",
             "lang": "meat3",
             "price": 856,
             "icon": "icons/products/meat_3.png"},
            {"id": "fish",
             "lang": "fish",
             "price": 430,
             "icon": "icons/products/fish.png"},
            {"id": "turkey",
             "lang": "turkey",
             "price": 570,
             "icon": "icons/products/turkey.png"},
            {"id": "pig",
             "lang": "pig",
             "price": 440,
             "icon": "icons/products/pig.png"},
            {"id": "salami",
             "lang": "salami",
             "price": 980,
             "icon": "icons/products/salami.png"},
            {"id": "rabbit",
             "lang": "rabbit",
             "price": 460,
             "icon": "icons/products/rabbit.png"},
            {"id": "cow",
             "lang": "cow",
             "price": 650,
             "icon": "icons/products/cow.png"}
        ]

        open_products_window(root, lang, global_bg, global_fg, GlobalAlpha, title_key="prod_mag",
                             window_icon="icons/products/meat.png", products_data=PRODUCTS)
    def ovo():
        PRODUCTS = [
            {"id": "ovo1",
             "lang": "ovo1",
             "price": 50,
             "icon": "icons/products/ovo_1.png"},
            {"id": "ovo",
             "lang": "ovo2",
             "price": 20,
             "icon": "icons/products/ovo_2.png"},
            {"id": "ovo3",
             "lang": "ovo3",
             "price": 30,
             "icon": "icons/products/ovo_3.png"},
            {"id": "potato",
             "lang": "potato",
             "price": 40,
             "icon": "icons/products/potato.png"},
            {"id": "pepper",
             "lang": "pepper",
             "price": 44,
             "icon": "icons/products/pepper.png"},
            {"id": "corn",
             "lang": "corn",
             "price": 55,
             "icon": "icons/products/corn.png"},
            {"id": "tomato",
             "lang": "tomato",
             "price":32,
             "icon": "icons/products/tomato.png"},
            {"id": "cucumber",
             "lang": "cucumber",
             "price": 21,
             "icon": "icons/products/cucumber.png"},
            {"id": "pumpkin",
             "lang": "pumpkin",
             "price": 75,
             "icon": "icons/products/pumpkin.png"}
        ]

        open_products_window(root, lang, global_bg, global_fg, GlobalAlpha, title_key="prod_mag",
                             window_icon="icons/products/ovo.png", products_data=PRODUCTS)
    def fructs():
        PRODUCTS = [
            {"id": "fruct1",
             "lang": "fruct1",
             "price":23,
             "icon": "icons/products/fruct_1.png"},
            {"id": "fruct2",
             "lang": "fruct2",
             "price": 54,
             "icon": "icons/products/fruct_2.png"},
            {"id": "fruct3",
             "lang": "fruct3",
             "price": 23,
             "icon": "icons/products/fruct_3.png"},
            {"id": "kiwi",
             "lang": "kiwi",
             "price": 75,
             "icon": "icons/products/kiwi.png"},
            {"id": "mango",
             "lang": "mango",
             "price": 79,
             "icon": "icons/products/mango.png"},
            {"id": "pear",
             "lang": "pear",
             "price": 22,
             "icon": "icons/products/pear.png"},
            {"id": "fig",
             "lang": "fig",
             "price": 54,
             "icon": "icons/products/fig.png"},
            {"id": "apple",
             "lang": "apple",
             "price": 12,
             "icon": "icons/products/apple.png"},
            {"id": "granate",
             "lang": "granate",
             "price": 43,
             "icon": "icons/products/granate.png"}
        ]

        open_products_window(root, lang, global_bg, global_fg, GlobalAlpha, title_key="prod_mag",
                             window_icon="icons/products/fruct.png", products_data=PRODUCTS)
    def sladost():
        PRODUCTS = [
            {"id": "slad1",
             "lang": "slad1",
             "price": 170,
             "icon": "icons/products/slad_1.png"},
            {"id": "slad2",
             "lang": "slad2",
             "price": 640,
             "icon": "icons/products/slad_2.png"},
            {"id": "slad3",
             "lang": "slad3",
             "price":430,
             "icon": "icons/products/slad_3.png"},
            {"id": "macaroni",
             "lang": "macaroni",
             "price": 450,
             "icon": "icons/products/macaroni.png"},
            {"id": "donut",
             "lang": "donut",
             "price": 564,
             "icon": "icons/products/donut.png"},
            {"id": "cotton_candy",
             "lang": "ccandy",
             "price": 230,
             "icon": "icons/products/cotton_candy.png"},
            {"id": "pudding",
             "lang": "pudding",
             "price": 240,
             "icon": "icons/products/pudding.png"},
            {"id": "candys",
             "lang": "candys",
             "price": 640,
             "icon": "icons/products/candys.png"},
            {"id": "puncake",
             "lang": "puncake",
             "price": 440,
             "icon": "icons/products/puncake.png"}
        ]

        open_products_window(root, lang, global_bg, global_fg, GlobalAlpha, title_key="prod_mag",
                             window_icon="icons/products/slad.png", products_data=PRODUCTS)
    def pc():
        PRODUCTS = [
            {"id": "pc1",
             "lang": "pc1",
             "price": 1150,
             "icon": "icons/products/pc_1.png"},
            {"id": "pc2",
             "lang": "pc2",
             "price": 2340,
             "icon": "icons/products/pc_2.png"},
            {"id": "pc3",
             "lang": "pc3",
             "price": 3210,
             "icon": "icons/products/pc_3.png"},
        ]

        open_products_window(root, lang, global_bg, global_fg, GlobalAlpha, title_key="prod_mag",
                             window_icon="icons/products/pc.png", products_data=PRODUCTS)
    def tel():
        PRODUCTS = [
            {"id": "tel1",
             "lang": "tel1",
             "price": 1120,
             "icon": "icons/products/tel_1.png"},
            {"id": "tel2",
             "lang": "tel2",
             "price": 1320,
             "icon": "icons/products/tel_2.png"},
            {"id": "tel3",
             "lang": "tel3",
             "price": 1320,
             "icon": "icons/products/tel_3.png"},
            {"id": "samsung",
             "lang": "samsung",
             "price": 4530,
             "icon": "icons/products/samsung.png"},
            {"id": "xiaomi",
             "lang": "xiaomi",
             "price": 2350,
             "icon": "icons/products/xiaomi.png"},
            {"id": "iphone10",
             "lang": "iphone10",
             "price": 7864,
             "icon": "icons/products/iphone10.png"},
            {"id": "iphone11",
             "lang": "iphone11",
             "price": 8453,
             "icon": "icons/products/iphone11.png"}
        ]

        open_products_window(root, lang, global_bg, global_fg, GlobalAlpha, title_key="prod_mag",
                             window_icon="icons/products/samsung.png", products_data=PRODUCTS)
    def wind():
        PRODUCTS = [
            {"id": "wind1",
             "lang": "wind1",
             "price": 1100,
             "icon": "icons/products/wind_1.png"},
            {"id": "wind2",
             "lang": "wind2",
             "price": 1000,
             "icon": "icons/products/wind_2.png"},
            {"id": "wind3",
             "lang": "wind3",
             "price": 1030,
             "icon": "icons/products/wind_3.png"},
        ]

        open_products_window(root, lang, global_bg, global_fg, GlobalAlpha, title_key="prod_mag",
                             window_icon="icons/products/wind.png", products_data=PRODUCTS)
    def ant():
        PRODUCTS = [
            {"id": "ant1",
             "lang": "ant1",
             "price": 150,
             "icon": "icons/products/ant_1.png"},
            {"id": "ant2",
             "lang": "ant2",
             "price": 250,
             "icon": "icons/products/ant_2.png"},
            {"id": "ant3",
             "lang": "ant3",
             "price": 256,
             "icon": "icons/products/ant_3.png"},
        ]

        open_products_window(root, lang, global_bg, global_fg, GlobalAlpha, title_key="prod_mag",
                             window_icon="icons/products/ant.png", products_data=PRODUCTS)
    def sft():
        PRODUCTS = [
            {"id": "sft1",
             "lang": "sft1",
             "price": 155,
             "icon": "icons/products/sft_1.png"},
            {"id": "sft2",
             "lang": "sft2",
             "price": 340,
             "icon": "icons/products/sft_2.png"},
            {"id": "sft3",
             "lang": "sft3",
             "price": 420,
             "icon": "icons/products/sft_3.png"},
        ]

        open_products_window(root, lang, global_bg, global_fg, GlobalAlpha, title_key="prod_mag",
                             window_icon="icons/products/sft.png", products_data=PRODUCTS)
    def drinks():
        PRODUCTS = [
            {"id": "g_water",
             "lang": "g_water",
             "price": 50,
             "icon": "icons/products/g_water.png"},
            {"id": "water",
             "lang": "waterP",
             "price": 43,
             "icon": "icons/products/water.png"},
            {"id": "peach_juice",
             "lang": "peach_juice",
             "price": 150,
             "icon": "icons/products/peach_juice.png"},
            {"id": "apple_juice",
             "lang": "apple_juice",
             "price": 160,
             "icon": "icons/products/apple_juice.png"},
            {"id": "orange_juice",
             "lang": "orange_juice",
             "price": 422,
             "icon": "icons/products/orange_juice.png"},
            {"id": "limonade",
             "lang": "limonade",
             "price": 230,
             "icon": "icons/products/limonade.png"},
            {"id": "energy",
             "lang": "energy",
             "price": 250,
             "icon": "icons/products/energy.png"},
            {"id": "pepsi",
             "lang": "pepsi",
             "price": 150,
             "icon": "icons/products/pepsi.png"},
            {"id": "cola",
             "lang": "colaP",
             "price": 160,
             "icon": "icons/products/cola.png"}
        ]

        open_products_window(root, lang, global_bg, global_fg, GlobalAlpha, title_key="prod_mag",
                             window_icon="icons/products/pepsi.png", products_data=PRODUCTS)
    def alcohol():
        PRODUCTS = [
            {"id": "beerL",
             "lang": "beerL",
             "price": 230,
             "icon": "icons/products/beer.png"},
            {"id": "beerD",
             "lang": "beerD",
             "price": 240,
             "icon": "icons/products/beer.png"},
            {"id": "whiskey",
             "lang": "whiskey",
             "price": 450,
             "icon": "icons/products/whiskey.png"},
            {"id": "vodka",
             "lang": "vodka",
             "price": 250,
             "icon": "icons/products/vodka.png"},
            {"id": "cognac",
             "lang": "cognac",
             "price":530,
             "icon": "icons/products/cognac.png"},
            {"id": "wine",
             "lang": "wine",
             "price": 450,
             "icon": "icons/products/wine.png"},
            {"id": "champagne",
             "lang": "champagne",
             "price": 120,
             "icon": "icons/products/champagne.png"},
            {"id": "rum",
             "lang": "rum",
             "price": 650,
             "icon": "icons/products/rum.png"},
            {"id": "cider",
             "lang": "cider",
             "price": 50,
             "icon": "icons/products/cider.png"}
        ]

        open_products_window(root, lang, global_bg, global_fg, GlobalAlpha, title_key="prod_mag",
                             window_icon="icons/products/pepsi.png", products_data=PRODUCTS)
    def poluf():
        PRODUCTS = [
            {"id": "chebureki",
             "lang": "chebureki",
             "price": 50,
             "icon": "icons/products/chebureki.png"},
            {"id": "pelmeni",
             "lang": "pelmeni",
             "price": 40,
             "icon": "icons/products/pelmeni.png"},
            {"id": "nuggets",
             "lang": "nuggets",
             "price": 45,
             "icon": "icons/products/nuggets.png"},
            {"id": "meatbal",
             "lang": "meatbal",
             "price": 43,
             "icon": "icons/products/meatbal.png"},
            {"id": "khinkali",
             "lang": "khinkali",
             "price": 65,
             "icon": "icons/products/khinkali.png"},
            {"id": "vareniki",
             "lang": "vareniki",
             "price": 77,
             "icon": "icons/products/vareniki.png"},
            {"id": "kotleta",
             "lang": "kotleta",
             "price": 85,
             "icon": "icons/products/kotleta.png"},
        ]

        open_products_window(root, lang, global_bg, global_fg, GlobalAlpha, title_key="prod_mag",
                             window_icon="icons/products/nuggets.png", products_data=PRODUCTS)
    def morep():
        PRODUCTS = [
            {"id": "squid",
             "lang": "squid",
             "price": 870,
             "icon": "icons/products/squid.png"},
            {"id": "salmon",
             "lang": "salmon",
             "price": 650,
             "icon": "icons/products/salmon.png"},
            {"id": "rak",
             "lang": "rak",
             "price": 450,
             "icon": "icons/products/rak.png"},
            {"id": "crab",
             "lang": "crab",
             "price": 550,
             "icon": "icons/products/crab.png"},
            {"id": "morskoi_yezh",
             "lang": "morskoi_yezh",
             "price": 780,
             "icon": "icons/products/morskoi_yezh.png"},
            {"id": "midii",
             "lang": "midii",
             "price": 530,
             "icon": "icons/products/midii.png"},
            {"id": "krevet",
             "lang": "krevet",
             "price": 450,
             "icon": "icons/products/krevet.png"},
            {"id": "g_krevet",
             "lang": "g_krevet",
             "price":500,
             "icon": "icons/products/g_krevet.png"},
            {"id": "kilka",
             "lang": "kilka",
             "price": 150,
             "icon": "icons/products/kilka.png"},
        ]

        open_products_window(root, lang, global_bg, global_fg, GlobalAlpha, title_key="prod_mag",
                             window_icon="icons/products/squid.png", products_data=PRODUCTS)
    def torts():
        PRODUCTS = [
            {"id": "cake_chocolate_nuts",
             "lang": "cake_chocolate_nuts",
             "price": 140,
             "icon": "icons/products/cake_chocolate_nuts.png"},
            {"id": "cake_nuts",
             "lang": "cake_nuts",
             "price": 170,
             "icon": "icons/products/cake_nuts.png"},
            {"id": "cake_chocolat",
             "lang": "cake_chocolat",
             "price": 130,
             "icon": "icons/products/cake_chocolat.png"},
            {"id": "cake_strawberry",
             "lang": "cake_strawberry",
             "price": 230,
             "icon": "icons/products/cake_strawberry.png"},
            {"id": "cake_golubika",
             "lang": "cake_golubika",
             "price": 430,
             "icon": "icons/products/cake_golubika.png"},
            {"id": "cake_yagodi",
             "lang": "cake_yagodi",
             "price": 420,
             "icon": "icons/products/cake_yagodi.png"},
            {"id": "cake_yagodi2",
             "lang": "cake_yagodi2",
             "price": 120,
             "icon": "icons/products/cake_yagodi2.png"},
            {"id": "cake_piannaya_vishnya",
             "lang": "cake_piannaya_vishnya",
             "price": 110,
             "icon": "icons/products/cake_piannaya_vishnya.png"},
            {"id": "cake_vishnya",
             "lang": "cake_vishnya",
             "price": 180,
             "icon": "icons/products/cake_vishnya.png"},
        ]

        open_products_window(root, lang, global_bg, global_fg, GlobalAlpha, title_key="prod_mag",
                             window_icon="icons/products/cake_chocolate_nuts.png", products_data=PRODUCTS)
    def tv():
        PRODUCTS = [
            {"id": "tv1",
             "lang": "tv1",
             "price": 1540,
             "icon": "icons/products/tv1.png"},
            {"id": "tv2",
             "lang": "tv2",
             "price": 1150,
             "icon": "icons/products/tv2.png"},
            {"id": "tv3",
             "lang": "tv3",
             "price": 3250,
             "icon": "icons/products/tv3.png"},
            {"id": "tv4",
             "lang": "tv4",
             "price": 4350,
             "icon": "icons/products/tv4.png"},
            {"id": "tv5",
             "lang": "tv5",
             "price": 2350,
             "icon": "icons/products/tv5.png"},
            {"id": "tv6",
             "lang": "tv6",
             "price": 2950,
             "icon": "icons/products/tv6.png"},
            {"id": "tv7",
             "lang": "tv7",
             "price": 2760,
             "icon": "icons/products/tv7.png"},
            {"id": "tv",
             "lang": "tv8",
             "price": 8450,
             "icon": "icons/products/tv8.png"},
            {"id": "tv9",
             "lang": "tv9",
             "price": 6550,
             "icon": "icons/products/tv9.png"},
        ]

        open_products_window(root, lang, global_bg, global_fg, GlobalAlpha, title_key="prod_mag",
                             window_icon="icons/products/tv1.png", products_data=PRODUCTS)
    def books():
        PRODUCTS = [
            {"id": "book1",
             "lang": "book1",
             "price": 23,
             "icon": "icons/products/book1.png"},
            {"id": "book2",
             "lang": "book2",
             "price": 33,
             "icon": "icons/products/book2.png"},
            {"id": "book3",
             "lang": "book3",
             "price": 25,
             "icon": "icons/products/book3.png"},
            {"id": "book4",
             "lang": "book4",
             "price": 65,
             "icon": "icons/products/book4.png"},
            {"id": "book5",
             "lang": "book5",
             "price": 64,
             "icon": "icons/products/book5.png"},
            {"id": "book6",
             "lang": "book6",
             "price": 54,
             "icon": "icons/products/book6.png"},
            {"id": "book7",
             "lang": "book7",
             "price": 24,
             "icon": "icons/products/book7.png"},
            {"id": "book8",
             "lang": "book8",
             "price": 88,
             "icon": "icons/products/book8.png"},
            {"id": "book9",
             "lang": "book9",
             "price": 65,
             "icon": "icons/products/book9.png"},
        ]

        open_products_window(root, lang, global_bg, global_fg, GlobalAlpha, title_key="prod_mag",
                             window_icon="icons/products/book1.png", products_data=PRODUCTS)
    def instr():
        PRODUCTS = [
            {"id": "instr1",
             "lang": "instr1",
             "price": 150,
             "icon": "icons/products/instr1.png"},
            {"id": "instr2",
             "lang": "instr2",
             "price": 150,
             "icon": "icons/products/instr2.png"},
            {"id": "instr3",
             "lang": "instr3",
             "price": 170,
             "icon": "icons/products/instr3.png"},
            {"id": "instr4",
             "lang": "instr4",
             "price": 430,
             "icon": "icons/products/instr4.png"},
            {"id": "instr5",
             "lang": "instr5",
             "price": 324,
             "icon": "icons/products/instr5.png"},
            {"id": "instr6",
             "lang": "instr6",
             "price": 430,
             "icon": "icons/products/instr6.png"},
            {"id": "instr7",
             "lang": "instr7",
             "price": 540,
             "icon": "icons/products/instr7.png"},
            {"id": "instr8",
             "lang": "instr8",
             "price": 50,
             "icon": "icons/products/instr8.png"},
            {"id": "instr9",
             "lang": "instr9",
             "price": 180,
             "icon": "icons/products/instr9.png"},
        ]

        open_products_window(root, lang, global_bg, global_fg, GlobalAlpha, title_key="prod_mag",
                             window_icon="icons/products/instr1.png", products_data=PRODUCTS)
    def pc_k():
        PRODUCTS = [
            {"id": "cpu1",
             "lang": "cpu1",
             "price": 3450,
             "icon": "icons/products/cpu1.png"},
            {"id": "cpu2",
             "lang": "cpu2",
             "price": 3670,
             "icon": "icons/products/cpu2.png"},
            {"id": "g_card1",
             "lang": "g_card1",
             "price": 5640,
             "icon": "icons/products/g_card1.png"},
            {"id": "g_card2",
             "lang": "g_card2",
             "price": 6420,
             "icon": "icons/products/g_card2.png"},
            {"id": "ram",
             "lang": "ram",
             "price": 3450,
             "icon": "icons/products/ram.png"},
            {"id": "cooler",
             "lang": "cooler",
             "price": 960,
             "icon": "icons/products/cooler.png"},
            {"id": "mainboard",
             "lang": "mainboard",
             "price": 4670,
             "icon": "icons/products/mainboard.png"},
            {"id": "power_s",
             "lang": "power_s",
             "price": 674,
             "icon": "icons/products/power_s.png"},
            {"id": "ssd",
             "lang": "ssd",
             "price": 753,
             "icon": "icons/products/ssd.png"},
        ]

        open_products_window(root, lang, global_bg, global_fg, GlobalAlpha, title_key="prod_mag",
                             window_icon="icons/products/cpu1.png", products_data=PRODUCTS)
    def clocks():
        PRODUCTS = [
            {"id": "clock1",
             "lang": "clock1",
             "price": 150,
             "icon": "icons/products/clock1.png"},
            {"id": "clock2",
             "lang": "clock2",
             "price": 160,
             "icon": "icons/products/clock2.png"},
            {"id": "clock3",
             "lang": "clock3",
             "price": 140,
             "icon": "icons/products/clock3.png"},
            {"id": "clock4",
             "lang": "clock4",
             "price": 155,
             "icon": "icons/products/clock4.png"},
            {"id": "digital_clock1",
             "lang": "digital_clock1",
             "price": 234,
             "icon": "icons/products/digital_clock1.png"},
            {"id": "digital_clock2",
             "lang": "digital_clock2",
             "price": 268,
             "icon": "icons/products/digital_clock2.png"},
            {"id": "digital_clock3",
             "lang": "digital_clock3",
             "price": 200,
             "icon": "icons/products/digital_clock3.png"},
            {"id": "smart_clock1",
             "lang": "smart_clock1",
             "price": 690,
             "icon": "icons/products/smart_clock1.png"},
            {"id": "smart_clock2",
             "lang": "smart_clock2",
             "price": 743,
             "icon": "icons/products/smart_clock2.png"},
        ]

        open_products_window(root, lang, global_bg, global_fg, GlobalAlpha, title_key="prod_mag",
                             window_icon="icons/products/cpu1.png", products_data=PRODUCTS)
    def cameras():
        PRODUCTS = [
            {"id": "photo1",
             "lang": "photo1",
             "price": 3250,
             "icon": "icons/products/photo1.png"},
            {"id": "photo2",
             "lang": "photo2",
             "price": 6530,
             "icon": "icons/products/photo2.png"},
            {"id": "photo3",
             "lang": "photo3",
             "price": 4350,
             "icon": "icons/products/photo3.png"},
            {"id": "camera",
             "lang": "camera",
             "price": 3450,
             "icon": "icons/products/camera.png"},
            {"id": "cctv1",
             "lang": "cctv1",
             "price": 4350,
             "icon": "icons/products/cctv1.png"},
            {"id": "cctv2",
             "lang": "cctv2",
             "price": 2150,
             "icon": "icons/products/cctv2.png"},
            {"id": "gopro1",
             "lang": "gopro1",
             "price": 2350,
             "icon": "icons/products/gopro1.png"},
            {"id": "gopro2",
             "lang": "gopro2",
             "price": 3350,
             "icon": "icons/products/gopro2.png"},
            {"id": "gopro3",
             "lang": "gopro3",
             "price": 3250,
             "icon": "icons/products/gopro3.png"},
        ]

        open_products_window(root, lang, global_bg, global_fg, GlobalAlpha, title_key="prod_mag",
                             window_icon="icons/products/cctv1.png", products_data=PRODUCTS)
    def posuda():
        PRODUCTS = [
            {"id": "glass",
             "lang": "glass",
             "price": 50,
             "icon": "icons/products/glass.png"},
            {"id": "kruzhka",
             "lang": "kruzhka",
             "price": 55,
             "icon": "icons/products/kruzhka.png"},
            {"id": "nozh",
             "lang": "nozh",
             "price": 34,
             "icon": "icons/products/nozh.png"},
            {"id": "vilka",
             "lang": "vilka",
             "price": 22,
             "icon": "icons/products/vilka.png"},
            {"id": "lozhka",
             "lang": "lozhka",
             "price": 30,
             "icon": "icons/products/lozhka.png"},
            {"id": "thermos",
             "lang": "thermos",
             "price": 150,
             "icon": "icons/products/thermos.png"},
            {"id": "skovorodka",
             "lang": "skovorodka",
             "price": 100,
             "icon": "icons/products/skovorodka.png"},
            {"id": "castr",
             "lang": "castr",
             "price": 170,
             "icon": "icons/products/castr.png"},
            {"id": "tarelka",
             "lang": "tarelka",
             "price": 80,
             "icon": "icons/products/tarelka.png"},
        ]

        open_products_window(root, lang, global_bg, global_fg, GlobalAlpha, title_key="prod_mag",
                             window_icon="icons/products/glass.png", products_data=PRODUCTS)
    def monitor():
        PRODUCTS = [
            {"id": "monitor1",
             "lang": "monitor1",
             "price": 1450,
             "icon": "icons/products/monitor1.png"},
            {"id": "monitor2",
             "lang": "monitor2",
             "price": 5450,
             "icon": "icons/products/monitor2.png"},
            {"id": "monitor3",
             "lang": "monitor3",
             "price": 4350,
             "icon": "icons/products/monitor3.png"},
            {"id": "monitor4",
             "lang": "monitor4",
             "price": 5450,
             "icon": "icons/products/monitor4.png"},
            {"id": "monitor5",
             "lang": "monitor5",
             "price": 4350,
             "icon": "icons/products/monitor5.png"},
            {"id": "monitor6",
             "lang": "monitor6",
             "price": 5450,
             "icon": "icons/products/monitor6.png"},
            {"id": "monitor7",
             "lang": "monitor7",
             "price": 3540,
             "icon": "icons/products/monitor7.png"},
            {"id": "monitor8",
             "lang": "monitor8",
             "price": 5430,
             "icon": "icons/products/monitor8.png"},
            {"id": "monitor9",
             "lang": "monitor9",
             "price": 7540,
             "icon": "icons/products/monitor9.png"},
        ]

        open_products_window(root, lang, global_bg, global_fg, GlobalAlpha, title_key="prod_mag",
                             window_icon="icons/products/monitor4.png", products_data=PRODUCTS)
    def micro():
        PRODUCTS = [
            {"id": "micro1",
             "lang": "micro1",
             "price": 1440,
             "icon": "icons/products/micro1.png"},
            {"id": "micro2",
             "lang": "micro2",
             "price": 4350,
             "icon": "icons/products/micro2.png"},
            {"id": "micro3",
             "lang": "micro3",
             "price": 4370,
             "icon": "icons/products/micro3.png"},
            {"id": "micro4",
             "lang": "micro4",
             "price": 2434,
             "icon": "icons/products/micro4.png"},
            {"id": "micro5",
             "lang": "micro5",
             "price": 1330,
             "icon": "icons/products/micro5.png"},
            {"id": "micro6",
             "lang": "micro6",
             "price": 2760,
             "icon": "icons/products/micro6.png"},
            {"id": "micro7",
             "lang": "micro7",
             "price": 1050,
             "icon": "icons/products/micro7.png"},
            {"id": "micro8",
             "lang": "micro8",
             "price": 1570,
             "icon": "icons/products/micro8.png"},
            {"id": "micro9",
             "lang": "micro9",
             "price": 1590,
             "icon": "icons/products/micro9.png"},
        ]

        open_products_window(root, lang, global_bg, global_fg, GlobalAlpha, title_key="prod_mag",
                             window_icon="icons/products/micro4.png", products_data=PRODUCTS)
    def headphones():
        PRODUCTS = [
            {"id": "headphones1",
             "lang": "headphones1",
             "price": 450,
             "icon": "icons/products/headphones1.png"},
            {"id": "headphones2",
             "lang": "headphones2",
             "price": 460,
             "icon": "icons/products/headphones2.png"},
            {"id": "headphones3",
             "lang": "headphones3",
             "price": 430,
             "icon": "icons/products/headphones3.png"},
            {"id": "headphones4",
             "lang": "headphones4",
             "price": 740,
             "icon": "icons/products/headphones4.png"},
            {"id": "headphones5",
             "lang": "headphones5",
             "price": 640,
             "icon": "icons/products/headphones5.png"},
            {"id": "headphones6",
             "lang": "headphones6",
             "price": 480,
             "icon": "icons/products/headphones6.png"},
            {"id": "headphones7",
             "lang": "headphones7",
             "price": 640,
             "icon": "icons/products/headphones7.png"},
            {"id": "headphones8",
             "lang": "headphones8",
             "price": 970,
             "icon": "icons/products/headphones8.png"},
            {"id": "headphones9",
             "lang": "headphones9",
             "price": 657,
             "icon": "icons/products/headphones9.png"},
            {"id": "headphones10",
             "lang": "headphones10",
             "price": 980,
             "icon": "icons/products/headphones10.png"}
        ]

        open_products_window(root, lang, global_bg, global_fg, GlobalAlpha, title_key="prod_mag",
                             window_icon="icons/products/headphones1.png", products_data=PRODUCTS)
    def playstations():
        PRODUCTS = [
            {"id": "plays1",
             "lang": "plays1",
             "price": 10493,
             "icon": "icons/products/plays1.png"},
            {"id": "plays2",
             "lang": "plays2",
             "price": 12533,
             "icon": "icons/products/plays2.png"},
            {"id": "plays3",
             "lang": "plays3",
             "price": 5436,
             "icon": "icons/products/plays3.png"},
            {"id": "plays4",
             "lang": "plays4",
             "price": 6435,
             "icon": "icons/products/plays4.png"},
            {"id": "plays5",
             "lang": "plays5",
             "price": 7540,
             "icon": "icons/products/plays5.png"},
            {"id": "plays6",
             "lang": "plays6",
             "price": 5346,
             "icon": "icons/products/plays6.png"},
            {"id": "plays7",
             "lang": "plays7",
             "price": 6433,
             "icon": "icons/products/plays7.png"},
            {"id": "plays8",
             "lang": "plays8",
             "price": 3463,
             "icon": "icons/products/plays8.png"},
            {"id": "plays9",
             "lang": "plays9",
             "price": 3453,
             "icon": "icons/products/plays9.png"}]

        open_products_window(root, lang, global_bg, global_fg, GlobalAlpha, title_key="prod_mag",
                             window_icon="icons/products/plays1.png", products_data=PRODUCTS)
    def bitov_tech():
        PRODUCTS = [
            {"id": "bitov_tech1",
            "lang": "bitov_tech1",
            "price": 5430,
            "icon": "icons/products/bitov_tech1.png"},
            {"id": "bitov_tech2",
            "lang": "bitov_tech2",
            "price": 6330,
            "icon": "icons/products/bitov_tech2.png"},
            {"id": "bitov_tech3",
            "lang": "bitov_tech3",
            "price": 5350,
            "icon": "icons/products/bitov_tech3.png"},
            {"id": "bitov_tech4",
            "lang": "bitov_tech4",
            "price": 3550,
            "icon": "icons/products/bitov_tech4.png"},
            {"id": "bitov_tech5",
            "lang": "bitov_tech5",
            "price": 5360,
            "icon": "icons/products/bitov_tech5.png"},
            {"id": "bitov_tech6",
            "lang": "bitov_tech6",
            "price": 6460,
            "icon": "icons/products/bitov_tech6.png"},
            {"id": "bitov_tech7",
            "lang": "bitov_tech7",
            "price": 6464,
            "icon": "icons/products/bitov_tech7.png"},
            {"id": "bitov_tech8",
            "lang": "bitov_tech8",
            "price": 3664,
            "icon": "icons/products/bitov_tech8.png"},
            {"id": "bitov_tech9",
            "lang": "bitov_tech9",
            "price": 1655,
            "icon": "icons/products/bitov_tech9.png"},
        ]
        open_products_window(root, lang, global_bg, global_fg, GlobalAlpha, title_key="prod_mag",
                             window_icon="icons/products/bitov_tech9.png", products_data=PRODUCTS)

    Win = create_window(root, lang['prod_mag'], global_bg, float(GlobalAlpha), 600, 600,
                      "icons/products/products.png")
    Win.prod1 = ImageTk.PhotoImage(Image.open(f'icons/products/the.png').resize((52, 52), Image.Resampling.LANCZOS))
    Win.prod2 = ImageTk.PhotoImage(Image.open('icons/products/cofe.png').resize((52, 52), Image.Resampling.LANCZOS))
    Win.prod8 = ImageTk.PhotoImage(Image.open('icons/products/bitov.png').resize((52, 52), Image.Resampling.LANCZOS))
    Win.prod3 = ImageTk.PhotoImage(Image.open('icons/products/sladost.png').resize((52, 52), Image.Resampling.LANCZOS))
    Win.prod4 = ImageTk.PhotoImage(Image.open('icons/products/ovo.png').resize((52, 52), Image.Resampling.LANCZOS))
    Win.prod5 = ImageTk.PhotoImage(Image.open('icons/products/fruct.png').resize((52, 52), Image.Resampling.LANCZOS))
    Win.prod6 = ImageTk.PhotoImage(Image.open('icons/products/meat.png').resize((52, 52), Image.Resampling.LANCZOS))
    Win.prod7 = ImageTk.PhotoImage(Image.open('icons/products/sft.png').resize((52, 52), Image.Resampling.LANCZOS))
    Win.prod9 = ImageTk.PhotoImage(Image.open('icons/products/wind.png').resize((52, 52), Image.Resampling.LANCZOS))
    Win.prod10 = ImageTk.PhotoImage(Image.open('icons/products/ant.png').resize((52, 52), Image.Resampling.LANCZOS))
    Win.prod11 = ImageTk.PhotoImage(Image.open('icons/products/pc.png').resize((52, 52), Image.Resampling.LANCZOS))
    Win.prod12 = ImageTk.PhotoImage(Image.open('icons/products/tel.png').resize((52, 52), Image.Resampling.LANCZOS))
    Win.card = ImageTk.PhotoImage(Image.open('icons/interface/cart.png').resize((52, 52), Image.Resampling.LANCZOS))
    Win.alco = ImageTk.PhotoImage(Image.open('icons/products/beer.png').resize((52, 52), Image.Resampling.LANCZOS))
    Win.drink = ImageTk.PhotoImage(Image.open('icons/products/cola.png').resize((52, 52), Image.Resampling.LANCZOS))
    Win.tort = ImageTk.PhotoImage(Image.open('icons/products/cake_chocolate_nuts.png').resize((52, 52), Image.Resampling.LANCZOS))
    Win.poluf = ImageTk.PhotoImage(Image.open('icons/products/pelmeni.png').resize((52, 52), Image.Resampling.LANCZOS))
    Win.morep = ImageTk.PhotoImage(Image.open('icons/products/krevet.png').resize((52, 52), Image.Resampling.LANCZOS))
    Win.tv = ImageTk.PhotoImage(Image.open('icons/products/tv1.png').resize((52, 52), Image.Resampling.LANCZOS))
    Win.book = ImageTk.PhotoImage(Image.open('icons/products/book1.png').resize((52, 52), Image.Resampling.LANCZOS))
    Win.instr = ImageTk.PhotoImage(Image.open('icons/products/instr9.png').resize((52, 52), Image.Resampling.LANCZOS))
    Win.pck = ImageTk.PhotoImage(Image.open('icons/products/cpu1.png').resize((52, 52), Image.Resampling.LANCZOS))
    Win.clocks = ImageTk.PhotoImage(Image.open('icons/products/digital_clock1.png').resize((52, 52), Image.Resampling.LANCZOS))
    Win.cameras = ImageTk.PhotoImage(Image.open('icons/products/cctv1.png').resize((52, 52), Image.Resampling.LANCZOS))
    Win.posuda = ImageTk.PhotoImage(Image.open('icons/products/tarelka.png').resize((52, 52), Image.Resampling.LANCZOS))
    Win.monitor = ImageTk.PhotoImage(Image.open('icons/products/monitor8.png').resize((52, 52), Image.Resampling.LANCZOS))
    Win.micro = ImageTk.PhotoImage(Image.open('icons/products/micro5.png').resize((52, 52), Image.Resampling.LANCZOS))
    Win.headphones = ImageTk.PhotoImage(Image.open('icons/products/headphones3.png').resize((52, 52), Image.Resampling.LANCZOS))
    Win.plays = ImageTk.PhotoImage(Image.open('icons/products/plays2.png').resize((52, 52), Image.Resampling.LANCZOS))
    Win.bitovt = ImageTk.PhotoImage(Image.open('icons/products/bitov_tech1.png').resize((52, 52), Image.Resampling.LANCZOS))

    top_frame = Frame(Win,bg=global_bg)
    top_frame.pack(side = TOP)
    left_frame = Frame(Win)
    left_frame.pack(side = LEFT)
    right_frame1 = Frame(Win)
    right_frame1.pack(side = LEFT)
    right_frame2 = Frame(Win)
    right_frame2.pack(side=LEFT)
    right_frame3 = Frame(Win)
    right_frame3.pack(side=LEFT)
    right_frame4 = Frame(Win)
    right_frame4.pack(side=LEFT)
    right_frame5 = Frame(Win)
    right_frame5.pack(side=LEFT)
    right_frame6 = Frame(Win)
    right_frame6.pack(side=LEFT)
    right_frame7 = Frame(Win)
    right_frame7.pack(side=LEFT)

    ttk.Button(top_frame,text = lang["add_promo"],command = promo).pack()
    if os.path.exists("store/mypromos.cfg"):
        ttk.Button(top_frame, text=lang["show_promo"], command=show).pack()
    c = ttk.Button(top_frame,image=Win.card,command = open_corz)
    c.pack()
    c.bind("<Enter>", lambda event: show_tooltip(event, txt=lang["show_cart"]))
    c.bind("<Leave>", hide_tooltip)

    tooltips = [lang["tooltip_the"],lang["tooltip_cofe"],lang["tooltip_sl"],lang["tooltip_ovo"],lang["tooltip_fr"],
                lang["tooltip_m"],lang["tooltip_sft"],lang["tooltip_b"],lang["tooltip_ant"],lang["tooltip_wind"],
                lang["tooltip_pc"],lang["tooltip_tel"],lang["tooltip_drink"],lang["tooltip_alco"],lang["tooltip_tort"],
                lang["tooltip_poluf"],lang["tooltip_morep"],lang["tooltip_tv"],lang["tooltip_book"],lang["tooltip_instr"],
                lang["tooltip_pck"],lang["tooltip_clocks"],lang["tooltip_cameras"],lang["tooltip_posuda"],
                lang['tooltip_monitor'],lang['tooltip_micro'],lang['tooltip_headf'],lang['tooltip_plays'],lang['tooltip_bitovt']]
    images = [Win.prod1,Win.prod2,Win.prod3,Win.prod4,Win.prod5,Win.prod6,Win.prod7,Win.prod8,Win.prod9,Win.prod10,
              Win.prod11,Win.prod12,Win.drink,Win.alco,Win.tort,Win.poluf,Win.morep,Win.tv,Win.book,Win.instr,Win.pck,
              Win.clocks,Win.cameras,Win.posuda,Win.monitor,Win.micro,Win.headphones,Win.plays,Win.bitovt]
    commands = [the,cofe,sladost,ovo,fructs,meat,sft,bitov,ant,wind,pc,tel,drinks,alcohol,torts,poluf,morep,tv,
                books,instr,pc_k,clocks,cameras,posuda,monitor,micro,headphones,playstations,bitov_tech]

    for i,(img,comm,tooltip) in enumerate(zip(images,commands,tooltips)):
        frm = ""
        if i <= 3:
            frm = left_frame
        elif i <= 7:
            frm = right_frame1
        elif i <= 11:
            frm = right_frame2
        elif i <= 15:
            frm = right_frame3
        elif i < 20:
            frm = right_frame4
        elif i < 24:
            frm = right_frame5
        elif i < 28:
            frm = right_frame6
        elif i < 32:
            frm = right_frame7
        btn = Button(frm, image=img, command=comm)
        btn.pack()
        btn.bind("<Enter>", lambda event,t = tooltip: show_tooltip(event, txt=t))
        btn.bind("<Leave>", hide_tooltip)