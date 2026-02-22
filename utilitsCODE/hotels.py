import os
import sqlite3
from tkinter import *
from tkinter import ttk,messagebox
from PIL import Image, ImageTk
from tkcalendar import DateEntry
from send_email import send_email
import customtkinter as ctk
from logtofile import log_to_file
from transactions import transactions
from send_email_template import send
from create_window import create_window
from save_and_load_balance import save_balance,load_balance

cityes = []
selected_options = []
svb_coins = 0

email = ''
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
    n, ln, email = user[1], user[2], user[3]
else:
    n = ln = e = "Unknown"
def delete_vars():
    global cityes,selected_options
    cityes = []
    selected_options = []

def open_hotel_window(root,lang,global_bg,global_fg,start_time_,edition,GlobalAlpha):
    countryes = [lang["france"], lang["italy"], lang["russia"], lang["espania"]]
    def dalee(city,country):
        def set_hotel(name, price, kolvo, date, end_date, city):
            def on_check(index):
                def inner():
                    # Взаимоисключение для типа номера
                    if index in [0, 1, 2]:
                        for i in [0, 1, 2]:
                            if i != index:
                                check_vars[i].set(False)
                    # Взаимоисключение для размещения
                    if index in [3, 4]:
                        for i in [3, 4]:
                            if i != index:
                                check_vars[i].set(False)
                    # Взаимоисключение для питания
                    if index in [5, 6]:
                        for i in [5, 6]:
                            if i != index:
                                check_vars[i].set(False)
                    update_price()

                return inner

            if len(kolvo) == 0 or not kolvo.isdigit():
                delete_vars()
                messagebox.showerror(lang["error"],lang["enter_valid_kolvo"],parent = ww)
                return
            if len(date) == 0:
                delete_vars()
                messagebox.showerror(lang["error"],lang["enter_valid_date"],parent = ww)
                return
            def get_selected_options(check_vars,opt):
                selected = []
                for i, var in enumerate(check_vars):
                    if var.get():
                        selected.append(opt[i])
                return selected
            def submit_booking(check_vars,opt,price):
                global svb_coins
                selected = get_selected_options(check_vars,opt)
                total_price = price + sum(item["price"] for item in selected)
                opts = []
                for item in selected:
                    opts.append(f"- {item['type']} (+{item['price']})")
                if messagebox.askyesno(lang['podt'],f"{lang['selected_opts']}{opts}",parent = www):
                    svb_coins = load_balance(start_time_)
                    if svb_coins >= total_price:
                        svb_coins -= int(total_price)
                        send('payement', int(total_price))
                        save_balance(svb_coins,start_time_)
                        transactions(f"-{total_price} SVB Price",start_time_)
                        global email
                        send_email(
                            to=str(email),
                            subject=lang["podt_bron"],
                            html=f"""
                            <html>
                              <body style="font-family: Arial, sans-serif; background-color: #f9f9f9; padding: 20px;">
                                <div style="background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); max-width: 600px; margin: auto;">
                                  <h2 style="color: #2c3e50;">{lang["bron_podt"]}</h2>
                                  <p style="font-size: 16px; color: #555;">
                                    {lang["thanks_h"]}
                                  </p>

                                  <hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;"/>

                                  <p><strong>{lang['--hotel']}</strong> {name}</p>
                                  <p><strong>{lang['--city']}</strong> {city}</p>
                                  <p><strong>{lang['--date']}</strong> {date}</p>
                                  <p><strong>{lang['--end_date']}</strong> {end_date}</p>
                                  <p><strong>{lang["--per"]}</strong> {kolvo}</p>

                                  <h3 style="color: #34495e; margin-top: 30px;">{lang["selected_opts2"]}</h3>
                                  <ul style="color: #555; font-size: 15px;">
                                    <p>{'<br>'.join(opts)}</p>
                                  </ul>

                                  <p style="margin-top: 20px; font-size: 16px;"><strong>{lang["total_price_h"]}</strong> <span style="color: #e74c3c;">{total_price} $</span></p>

                                  <p style="font-size: 14px; color: #888; margin-top: 30px;">
                                    {lang["bron2"]}
                                  </p>
                                </div>
                              </body>
                            </html>
                            """

                        )

                        messagebox.showinfo(lang["success"],f"{lang['you_bron_otel']}{kolvo}{lang['you_bron_otel1']}{date} {lang['check_email']}",parent = www)
                    else:
                        delete_vars()
                        messagebox.showerror(lang["error"],lang["no_svb"],parent = www)
            def update_price():
                total = price
                for i, var in enumerate(check_vars):
                    if var.get():
                        total += opt[i]["price"]
                price_label.config(text=f"{lang['futur_price']}:{total}")

            www = create_window(Win, lang['hotels'], global_bg, float(GlobalAlpha), 600, 600)
            opt = [{"type":lang['h_n_type1'],"price":300*int(kolvo),"img":"icons/h_otel.png"},{"type":lang['h_n_type2'],"price":600*int(kolvo),"img":"icons/h_otel.png"},
                   {"type":lang['h_n_type3'],"price":1400*int(kolvo),"img":"icons/h_otel.png"},{'type':lang["norm"],"price":100*int(kolvo),"img":"icons/h_otel.png"},
                   {'type':lang["luks"],"price":500*int(kolvo),"img":"icons/h_otel.png"},{"type":lang["polupan"],'price':200*int(kolvo),"img":"icons/interface/pan.png"},
                   {"type":lang["pan"],'price':500*int(kolvo),"img":"icons/interface/pan.png"},{"type":lang["free_wifi"],"price":50*int(kolvo),"img":"icons/interface/h_wifi.png"},
                   {"type":lang["parking"],"price":400*int(kolvo),"img":"icons/h_parking.png"},
                   ]
            pp = price
            frm = Frame(www)
            frm.pack()
            Label(www,text = f'{lang["hotel="]}:{name},{lang["h_price"]}:{price}',font = ("Arial",14,"bold")).pack()
            Label(www,text = f'{lang["futur_price"]}:{pp}',fg = 'red').pack()

            price_label = Label(www, text=f'{lang["futur_price"]}: {price}', fg='red', font=("Arial", 12))
            price_label.pack()
            Label(www, text=lang["select_options"], font=("Arial", 12)).pack()
            check_vars = []
            photo_images = []
            for i,o in enumerate(opt):
                var = BooleanVar()
                check_vars.append(var)
                sub_frame = Frame(frm)
                sub_frame.pack(anchor='w', pady=3)
                try:
                    img = Image.open(o["img"])
                    img = img.resize((40, 40), Image.ANTIALIAS)
                    photo = ImageTk.PhotoImage(img)
                    photo_images.append(photo)
                    Label(sub_frame, image=photo).pack(side='left')
                except:
                    pass
                ttk.Checkbutton(sub_frame, text=f"{o['type']} (+{o['price']})", variable=var,
                                command=on_check(i)).pack(side='left' if i < 4 else 'right')
            check_vars[0].set(True)
            on_check(0)()
            check_vars[3].set(True)
            on_check(3)()
            check_vars[5].set(True)
            on_check(5)()
            ttk.Button(www,text = lang["oplatit"],command=lambda:submit_booking(check_vars,opt,price)).pack()
        hotels_moscow = [{"name":lang['m_otel1'],"price":23000},{"name":lang['m_otel2'],"price":11000}, {"name":lang['m_otel3'],"price":27000}]
        hotels_spb = [{"name":lang['spb_otel1'],"price":9000},{"name":lang['spb_otel2'],"price":11000},{"name":lang['spb_otel3'],"price":35000}]
        hotels_sochi = [{"name":lang["s_otel1"],"price":8000},{"name":lang["s_otel2"],"price":10000},{"name":lang["s_otel3"],"price":22000}]
        hotels_barcelona = [{"name":"W Barcelona","price":23000}, {"name":"Hotel Arts Barcelona","price":22000}, {"name":"Majestic Hotel & Spa","price":23000}]
        hotels_madrid = [{"name":"The Westin Palace","price":14000}, {"name":"Gran Meliá Palacio de los Duques","price":11000}, {"name":"URSO Hotel & Spa","price":23000}]
        hotels_bilbao = [{"name":"Hotel Carlton","price":13000}, {"name":"Gran Hotel Domine","price":21000}, {"name":"NH Collection Villa de Bilbao","price":23000}]
        hotels_paris = [{"name":"Le Meurice","price":14000}, {"name":"Ritz Paris","price":1200}, {"name":"Shangri-La Hotel Paris","price":8000}]
        hotels_nice = [{"name":"Hotel Negresco","price":10000}, {"name":"Hyatt Regency Nice","price":15000}, {"name":"Le Meridien Nice","price":19000}]
        hotels_monaco = [{"name":"Hotel de Paris Monte-Carlo","price":13000}, {"name":"Fairmont Monte Carlo","price":17000}, {"name":"Monte-Carlo Bay Hotel & Resort","price":23000}]
        hotels_venice = [{"name":"Belmond Hotel Cipriani","price":21000}, {"name":"Gritti Palace","price":19000}, {"name":"Ca' Sagredo Hotel","price":21100}]
        hotels_rome = [{"name":"Hotel de Russie","price":25000}, {"name":"Rome Cavalieri Waldorf Astoria","price":14000}, {"name":"J.K. Place Roma","price":21000}]
        hotels_pisa = [{"name":"Hotel Bologna","price":24000}, {"name":"Hotel Relais Dell'Orologio","price":14000}, {"name":"NH Pisa","price":20000}]

        ww = create_window(Win, lang['hotels'], global_bg, float(GlobalAlpha), 500, 500)

        # Словарь, сопоставляющий город и список отелей
        city_hotels = {
            lang["nicce"]: hotels_nice,
            lang["paris"]: hotels_paris,
            lang["monako"]: hotels_monaco,
            lang["venec"]: hotels_venice,
            lang["rim-"]: hotels_rome,
            lang["pisa"]: hotels_pisa,
            lang["moskow"]: hotels_moscow,
            lang["stp"]: hotels_spb,
            lang["sochi"]: hotels_sochi,
            lang["barcelona"]: hotels_barcelona,
            lang["madrid"]: hotels_madrid,
            lang["bulbao"]: hotels_bilbao,
        }

        if city in city_hotels:
            Label(ww, text=f"{lang['c']}: {country}").pack()
            Label(ww, text=lang["select_otel"], font=("Arial", 13, "bold")).pack()
            Label(ww,text = lang["enter_kolvo_per"]).pack()
            kolvo = ctk.CTkEntry(ww,placeholder_text=lang['kolich'])
            kolvo.pack()
            date = DateEntry(ww, width=30, background=global_bg, foreground=global_fg, bordercolor=global_fg,
                                   headersbackground=global_bg, headersforeground=global_fg, selectbackground='blue',
                                   selectforeground=global_bg, weekendbackground=global_bg, weekendforeground='red',
                                   date_pattern='dd.mm.yyyy', locale='en_US', )
            date.pack(pady=10)
            Label(ww, text=lang["end_date"]).pack()
            end_date = DateEntry(ww, width=30, background=global_bg, foreground=global_fg, bordercolor=global_fg,
                                 headersbackground=global_bg, headersforeground=global_fg, selectbackground='blue',
                                 selectforeground=global_bg, weekendbackground=global_bg, weekendforeground='red',
                                 date_pattern='dd.mm.yyyy', locale='en_US', )
            end_date.pack(pady=10)

            for h in city_hotels[city]:
                Label(ww, text=h['name'], font=("Arial", 9)).pack()
                Label(ww, text=f"{lang['h_price']}:{h['price']}", fg="red").pack()
                ttk.Button(ww, text=lang["dalee"], command=lambda n=h["name"], p=h["price"]: set_hotel(n, p, kolvo.get(), date.get(), end_date.get(), city)).pack()
    def set_city(combo):
        global cityes
        if combo == lang["france"]:
            for c in [lang["nicce"],lang["paris"],lang["monako"]]:
                cityes.append(c)
            combo1 = ttk.Combobox(Win, values=cityes)
            combo1.pack()
            combo1.set(lang["paris"])
            ttk.Button(Win,text = lang["dalee"],command = lambda:dalee(combo1.get(),combo)).pack()
        if combo == lang["italy"]:
            for c in [lang["venec"], lang["rim-"], lang["pisa"]]:
                cityes.append(c)
            combo1 = ttk.Combobox(Win, values=cityes)
            combo1.pack()
            combo1.set(lang["rim-"])
            ttk.Button(Win, text=lang["dalee"], command=lambda: dalee(combo1.get(),combo)).pack()
        if combo == lang["russia"]:
            for c in [lang["moskow"], lang["stp"], lang["sochi"]]:
                cityes.append(c)
            combo1 = ttk.Combobox(Win, values=cityes)
            combo1.pack()
            combo1.set(lang["moskow"])
            ttk.Button(Win, text=lang["dalee"], command=lambda: dalee(combo1.get(),combo)).pack()
        if combo == lang["espania"]:
            for c in [lang["barcelona"], lang["madrid"], lang["bulbao"]]:
                cityes.append(c)
            combo1 = ttk.Combobox(Win, values=cityes)
            combo1.pack()
            combo1.set(lang["barcelona"])
            ttk.Button(Win, text=lang["dalee"], command=lambda: dalee(combo1.get(),combo)).pack()
    global cityes

    Win = create_window(root, lang['hotels'], global_bg, float(GlobalAlpha), 500, 400,"icons/hotels.png")

    Label(Win,text = lang["select_country"],bg = global_bg,fg = global_fg).pack()
    combo = ttk.Combobox(Win,values = countryes)
    combo.pack()
    combo.bind("<<ComboboxSelected>>",lambda event:set_city(combo.get()))
    combo.set(lang["france"])
