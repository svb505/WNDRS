import sqlite3
from logger_setup import system_logger
from tkinter import *
from tkinter import ttk, messagebox, filedialog, colorchooser
import time
import os
import logging
import random
from datetime import datetime
from PIL import Image, ImageTk
import requests
from io import BytesIO
from server_statistick import update_file
import customtkinter as ctk
from logtofile import log_to_file
from play_sound import play_sound
from copy_file_to_folder import copy_file_to_folder
from send_email_template import send
from transactions import transactions
import math
from save_and_load_balance import save_balance,load_balance
from create_window import create_window
import pyttsx3
from pytubefix import YouTube
from load_env import load_env

svb_coins = 0
SYSTEM_LEVEL = 25
logging.addLevelName(SYSTEM_LEVEL, "SYSTEM")
config = {}
count = 0

load_env()

API_KEY = os.getenv("WEATHER_API")

def open_notepad(state_sound,lang,root,volume,errors,actives_programs,global_fg,global_bg,start_time_,GlobalAlpha):
    play_sound("sound//click.mp3", volume, state_sound, start_time_)
    actives_programs.append("Notepad")
    log_to_file("Notepad launch",start_time_)

    def save():
        file_name = filedialog.asksaveasfilename(parent = Win,defaultextension=".txt",
                                                 filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if not file_name:
            return

        text_content = txtt.get("1.0", END).strip()

        if not text_content:
            messagebox.showwarning(lang["error"], lang["enter_text"],parent=Win)
            return

        try:
            with open(file_name, "w", encoding="utf-8") as file:
                file.write(text_content)
            messagebox.showinfo(lang["success"], f"{lang['text-saved']} '{file_name}'",parent=Win)
        except Exception as e:
            messagebox.showerror(lang["error"], f"{lang['error-saved']} {e}",parent=Win)
            log_to_file(f"Messge: {lang['error-saved']}",start_time_, level="error")
    def otk():
        file_name = filedialog.askopenfilename(parent = Win,filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if not file_name:
            return

        try:
            with open(file_name, "r", encoding="utf-8") as file:
                txtt.delete("1.0", END)
                txtt.insert(END, file.read())
            messagebox.showinfo(lang["success"], f"{lang['file']} '{file_name}' {lang['opened']}",parent=Win)
        except Exception as e:
            messagebox.showerror(lang["error"], f"{lang['error-open']} {e}",parent=Win)
            log_to_file(f"Messge: {lang['error-open']}",start_time_, level="error")

    Win = Toplevel(root)
    Win.attributes("-alpha",float(GlobalAlpha))
    Win.geometry("1200x600")
    Win.title(lang["notepad"])
    Win.config(bg=global_bg)
    img = Image.open("icons/notebook.png")
    icon_image = ImageTk.PhotoImage(img)
    Win.iconphoto(False, icon_image)
    txtt = Text(Win, width=1000, height=300, fg=global_fg, bg=global_bg)
    txtt.pack()

    main_menu = Menu(Win)
    main_menu.add_cascade(label=lang["save"], command=save)
    main_menu.add_cascade(label=lang["open"], command=otk)
    Win.config(menu=main_menu)
def open_paint(state_sound,volume,actives_programs,errors,lang,root,start_time_,GlobalAlpha):
    play_sound("sound//click.mp3", volume, state_sound, start_time_)
    actives_programs.append("Paint")
    log_to_file("paint launch",start_time_)
    def start_paint(event):
        global last_x, last_y
        last_x, last_y = event.x, event.y
    def paint(event):
        global last_x, last_y
        canvas.create_line(last_x, last_y, event.x, event.y, fill=color_, width=3)
        last_x, last_y = event.x, event.y
    def clear_canvas():
        canvas.delete("all")
    def choose_color():
        global color_
        color_ = colorchooser.askcolor(parent=roott)[1]

    roott = Toplevel(root)
    roott.attributes("-alpha",float(GlobalAlpha))
    roott.title("Paint")
    img = Image.open("icons/paint.png")
    icon_image = ImageTk.PhotoImage(img)
    roott.iconphoto(False, icon_image)
    canvas = Canvas(roott, bg="white", width=600, height=400)
    canvas.pack(fill=BOTH, expand=True)

    color_ = "black"

    canvas.bind("<Button-1>", start_paint)
    canvas.bind("<B1-Motion>", paint)

    frame = Frame(roott)
    frame.pack()

    clear_btn = Button(frame, text=lang["clear"], command=clear_canvas)
    clear_btn.pack(side=LEFT, padx=5)

    color_btn = Button(frame, text=lang["select_color"], command=choose_color)
    color_btn.pack(side=LEFT, padx=5)

    root.mainloop()
def translate(root,actives_programs,state_sound,volume,errors,lang,global_fg,global_bg,start_time_,GlobalAlpha):
    actives_programs.append("Translator")
    play_sound("sound//click.mp3", volume, state_sound, start_time_)
    """def translate_text():
        text = input_text.get("1.0", END).strip()
        src_lang = src_lang_var.get()
        dest_lang = dest_lang_var.get()

        async def do_translate():
            try:
                translated = await translator.translate(text, src=languages[src_lang], dest=languages[dest_lang])
                output_text.delete("1.0", END)
                output_text.insert(END, translated.text)
            except Exception as e:
                output_text.delete("1.0", END)
                output_text.insert(END, f"Ошибка перевода: {e}")

        asyncio.run(do_translate())"""

    languages = {
        lang["auto"]: 'auto',
        lang["english"]: 'en',
        lang["russian"]: 'ru',
        lang["german"]: 'de',
        lang["french"]: 'fr',
        lang["espan"]: 'es',
        lang["chin"]: 'zh-cn',
        lang["jap"]: 'ja'
    }

    roott = Toplevel(root)
    roott.attributes("-alpha",float(GlobalAlpha))
    roott.title(lang['translate'])
    roott.geometry("600x400")
    roott.configure(bg=global_bg)
    img = Image.open("icons/translator.png")
    icon_image = ImageTk.PhotoImage(img)
    roott.iconphoto(False, icon_image)

    src_lang_var = StringVar(value='auto')
    dest_lang_var = StringVar(value='ru')

    Label(roott, text=lang["lan1"], fg=global_fg, bg=global_bg).pack()
    ttk.Combobox(roott, textvariable=src_lang_var, values=list(languages.keys()), state='readonly').pack()

    Label(roott, text=lang["lan2"], fg=global_fg, bg=global_bg).pack()
    ttk.Combobox(roott, textvariable=dest_lang_var, values=list(languages.keys()), state='readonly').pack()

    input_text = Text(roott, height=6)
    input_text.pack(padx=10, pady=10, fill=BOTH)

    #ttk.Button(roott, text=lang["translate-"], command=translate_text).pack(pady=10)

    output_text = Text(roott, height=6)
    output_text.pack(padx=10, pady=10, fill=BOTH)
def open_calc(state_sound,volume,errors,lang,root,actives_programs,color,special_frames,start_time_,GlobalAlpha):
    play_sound("sound//click.mp3", volume, state_sound, start_time_)
    actives_programs.append("Calculator")

    def evaluate():
        try:
            expression = entry.get()
            result = eval(expression, {"__builtins__": None}, math.__dict__)

            entry.delete(0, END)
            entry.insert(END, str(result))

        except:
            messagebox.showerror(lang["error"], lang["incorrect_ex"], parent=win)
            log_to_file(f'Message:  {lang["incorrect_ex"]}', start_time_, level="warning")

    def on_click(ch):
        if ch == '=':
            evaluate()
        elif ch == 'C':
            entry.delete(0, END)
        elif ch in ('sin', 'cos', 'tan'):
            entry.insert(END, f"{ch}(")
        else:
            entry.insert(END, ch)

    log_to_file('Calculator launch',start_time_)
    win = Toplevel(root)
    win.attributes("-alpha",float(GlobalAlpha))
    win.title(lang["calculator"])
    win.geometry("300x500")
    win.configure(bg="#ecf0f1")
    img = Image.open("icons/calculator.png")
    icon_image = ImageTk.PhotoImage(img)
    win.iconphoto(False, icon_image)
    entry = ctk.CTkEntry(win, font=("Arial", 18),width=200,placeholder_text=lang['holder_result'])
    entry.pack(pady=10)

    btn_frame = Frame(win, bg="#ecf0f1")
    btn_frame.pack()

    buttons = [
        ('sin', 'cos', 'tan', 'C'),
        ('7', '8', '9', '/'),
        ('4', '5', '6', '*'),
        ('1', '2', '3', '-'),
        ('(', '0', ')', '+'),
        (".","=")
    ]

    for row in buttons:
        frame = Frame(btn_frame, bg=str(color))
        frame.pack()
        special_frames.append(frame)

        for char in row:
            btn = Button(frame, text=char, font=("Arial", 14), width=5, height=2,
                         command=lambda ch=char: on_click(ch))
            btn.pack(side=LEFT, padx=2, pady=2)
def gener_photo(root,lang,global_bg,global_fg,GlobalAlpha):
    def create(prompt):
        try:
            width = 1104
            height = 1734
            seed = random.randint(1, 10000)
            model = 'flux-pro'
            image_url = f"https://pollinations.ai/p/{prompt}?width={width}&height={height}&seed={seed}&model={model}"
            response = requests.get(image_url)
            img = Image.open(BytesIO(response.content))
            img = img.crop((0, 0, width, height - 70))
            path = f"photo_{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.png"
            img.save(f'user_files/{path}')
            img.show()
            messagebox.showinfo(lang["success"],lang["photo_saved__"] + str(path),parent=Win)
        except Exception as e:
            messagebox.showerror(lang["error"],str(e),parent=Win)

    Win = Toplevel(root)
    Win.attributes("-alpha",float(GlobalAlpha))
    Win.title(lang["photo_gener"])
    Win.configure(bg=global_bg)
    Win.geometry('400x400')
    img = Image.open("icons/generator.png")
    icon_image = ImageTk.PhotoImage(img)
    Win.iconphoto(False, icon_image)

    Label(Win,text = lang["enter_prompt"],bg=global_bg,fg=global_fg).pack()
    prompt = ctk.CTkEntry(Win,placeholder_text='enter_promt')
    prompt.pack()

    ttk.Button(Win,text = lang["create_photo"],command = lambda:create(prompt.get())).pack()
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
def log_system(msg,start_time_):
    try:
        elapsed = time.time() - start_time_
    except NameError:
        elapsed = 0
    formatted_msg = f"[{elapsed:.1f}] - {msg}"
    system_logger.log(SYSTEM_LEVEL, formatted_msg)
def lotereya(actives_programs,lang,root,edition,start_time_,global_bg,global_fg,GlobalAlpha):
    actives_programs.append("lotereya")
    log_to_file("Loterry launch",start_time_ = start_time_)

    def buy(stavka):
        global svb_coins
        svb_coins = load_balance(start_time_)
        if svb_coins >= 1000:
            svb_coins -= 1000
            send('payement', 1000)
            transactions("- 1000 SVB Coins" + f" {datetime.now()}",start_time_)
            log_to_file("-= 1000 Svb Coins",start_time_ = start_time_)
            save_balance(svb_coins,start_time_)
            nagr = 0
            chance_to_win = 0
            if stavka == "1.000":
                chance_to_win = 0.5
            elif stavka == "5.000":
                chance_to_win = 0.3
            elif stavka == "10.000":
                chance_to_win = 0.2
            elif stavka == "100.000":
                chance_to_win = 0.05
            elif stavka == "1.000.000":
                chance_to_win = 0.01
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
            cursor.execute("SELECT * FROM users")
            users = cursor.fetchall()
            if users:
                user = users[0]
                n, ln, e = user[1], user[2], user[3]
            else:
                n = ln = e = "Unknown"
            conn.close()
            ticket_number = random.randint(100000, 999999)
            is_winner = random.random() < chance_to_win
            if is_winner:
                if stavka == "1.000":
                    nagr = 1000
                elif stavka == "5.000":
                    nagr = 5000
                elif stavka == "10.000":
                    nagr = 10000
                elif stavka == "100.000":
                    nagr = 100000
                elif stavka == "1.000.000":
                    nagr = 1000000

            svb_coins += nagr
            send('receipt', nagr)
            update_file("count_svbcoins.txt", int(nagr))

            save_balance(svb_coins,start_time_)
            check_ach(lang,start_time_)
            transactions(f"+ {nagr} SVB Coins" + f" {datetime.now()}",start_time_)
            log_to_file(f"+= {nagr} Svb Coins",start_time_ = start_time_)
            subject = lang['you_win'] if is_winner else lang['your_lot']
            html = f"""
                <html>
                <head>
                    <style>
                        body {{
                            font-family: Arial, sans-serif;
                            background-color: #f0f8ff;
                            padding: 20px;
                        }}
                        .ticket {{
                            max-width: 600px;
                            margin: auto;
                            background: #fff;
                            border-radius: 10px;
                            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
                            padding: 30px;
                            text-align: center;
                        }}
                        .number {{
                            font-size: 36px;
                            color: #e74c3c;
                            margin: 20px 0;
                            border: 2px dashed #e74c3c;
                            padding: 10px 20px;
                            display: inline-block;
                        }}
                        .status {{
                            font-size: 18px;
                            color: {('#27ae60' if is_winner else '#34495e')};
                            margin-top: 15px;
                        }}
                    </style>
                </head>
                <body>
                    <div class="ticket">
                        <h2>{subject}</h2>
                        <div class="number">{ticket_number}</div>
                        <div class="status">{lang['lot_win'] if is_winner else lang['lot_lose']}</div>
                    </div>
                </body>
                </html>
                """

            requests.post("https://server-os.onrender.com/send_email", json={
                "to": str(e),
                "subject": subject,
                "html": html
            })
            mes = f"{lang['you_win']} {str(nagr)} SVB Coins" if is_winner else lang['lot_lose']
            messagebox.showinfo(lang['success'], mes,parent=Win)
            messagebox.showinfo(lang['success'], lang["check_email"],parent=Win)
        else:
            messagebox.showerror(lang["error"], lang["no_svb"],parent=Win)

    Win = Toplevel(root)
    Win.attributes("-alpha",float(GlobalAlpha))
    Win.configure(bg=global_bg)
    Win.title(lang["lot"])
    img = Image.open("icons/lottery.png")
    icon_image = ImageTk.PhotoImage(img)
    Win.iconphoto(False, icon_image)
    Win.geometry("500x400")
    Label(Win, text=lang["select_"],bg=global_bg,fg=global_fg).pack()
    combo = ttk.Combobox(Win, values=["1.000", "5.000", "10.000", "100.000", "1.000.000"])
    combo.set("1.000")
    combo.config(state="readonly")
    combo.pack()
    ttk.Button(Win, text=lang["kup"], command=lambda: buy(combo.get())).pack()
def promocodes(lang,root,edition,start_time_,global_bg,global_fg,GlobalAlpha):
    def my_promos():
        W = Toplevel(Win)
        W.attributes("-alpha",float(GlobalAlpha))
        W.configure(bg=global_bg)
        W.title(lang["promoc"])
        W.geometry('400x300')
        text = Text(W)
        text.pack(expand=True, fill=BOTH)
        text.insert(1.0, '--MY PROMOS--\n')

        conn = sqlite3.connect("prm_c.db")
        cursor = conn.cursor()
        cursor.execute("SELECT codes FROM my_codes")
        codes = cursor.fetchall()
        conn.close()

        if not codes:
            text.insert(END, lang.get("no_codes", "Нет кодов.") + '\n')
        else:
            for row in codes:
                if row[0] == "ACZ3423":
                    text.insert(END, f"{row[0]} - {lang['all-pr']}\n")
                else:
                    text.insert(END, f"{row[0]} - {lang['others']}\n")

        text.config(state="disabled")
    def pol(promos):
        def generate_promo(promos):
            return random.choice(promos)

        global svb_coins
        svb_coins = load_balance(start_time_)

        if svb_coins < 500:
            messagebox.showerror(lang["error"], lang["no_svb"],parent=Win)
            return

        conn = sqlite3.connect("prm_c.db")
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS my_codes (codes TEXT)""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS actives_c (codes TEXT)""")
        conn.commit()

        cursor.execute("SELECT codes FROM my_codes")
        myc = [row[0] for row in cursor.fetchall()]
        cursor.execute("SELECT codes FROM actives_c")
        act = [row[0] for row in cursor.fetchall()]
        conn.close()

        used_promos = set(myc + act)
        available_promos = [p for p in promos if p not in used_promos]

        if not available_promos:
            messagebox.showinfo("info", lang["no_new_promos"],parent=Win)
            return

        promo = generate_promo(available_promos)

        svb_coins -= 500
        send('payement', 500)
        transactions('-500 SVB Coins' + f" {datetime.now()}",start_time_)
        save_balance(svb_coins,start_time_)

        conn = sqlite3.connect("prm_c.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO my_codes (codes) VALUES (?)", (promo,))
        conn.commit()
        conn.close()

        messagebox.showinfo(lang['success'], lang["true_promo"],parent=Win)
    def activate(promos, uin):
        global count
        if count >= 3:
            messagebox.showerror(lang["error"],lang["nepitaisa"],parent=Win)
        if uin not in promos:
            count += 1
            messagebox.showerror(lang["error"], lang["incorrect_promo"],parent=Win)
            return

        conn = sqlite3.connect("prm_c.db")
        cursor = conn.cursor()
        cursor.execute("SELECT codes FROM actives_c")
        act = [row[0] for row in cursor.fetchall()]
        cursor.execute("SELECT codes FROM my_codes")
        myc = [row[0] for row in cursor.fetchall()]

        if uin in act:
            messagebox.showerror(lang["error"], lang["code_act_"],parent=Win)
            conn.close()
            return

        if uin not in myc:
            messagebox.showerror(lang["error"], lang["code_notdef"],parent=Win)
            conn.close()
            return

        cursor.execute("DELETE FROM my_codes WHERE codes = ?", (uin,))
        cursor.execute("INSERT INTO actives_c (codes) VALUES (?)", (uin,))
        conn.commit()

        if uin == "ACZ3423":
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

            cursor.execute("SELECT codes FROM my_codes")
            existing_codes = set(row[0] for row in cursor.fetchall())

            for p in bonus_promos:
                if p not in existing_codes:
                    cursor.execute("INSERT INTO my_codes (codes) VALUES (?)", (p,))

            conn.commit()
            conn.close()
            messagebox.showinfo(lang["success"], lang["all_promos"],parent=Win)
        else:
            conn.close()
            global svb_coins
            svb_coins = load_balance(start_time_)
            n = random.randint(1, 3)
            if n == 1:
                money = random.randint(1000, 10000)
            elif n == 2:
                money = random.randint(10000, 100000)
            else:
                money = 100000

            svb_coins += money
            send('receipt', money)
            update_file("count_svbcoins.txt", int(money))
            transactions(f"-{money} SVB Coins" + f" {datetime.now()}",start_time_)
            save_balance(svb_coins,start_time_)
            check_ach(lang,start_time_)
            messagebox.showinfo(lang["success"], f"{lang['mon']}{money} SVB Coins",parent=Win)

    conn = sqlite3.connect("prm_c.db")
    cursor = conn.cursor()
    cursor.execute("SELECT codes FROM all_promos")
    promos = [row[0] for row in cursor.fetchall()]
    conn.close()

    Win = Toplevel(root)
    Win.attributes("-alpha",float(GlobalAlpha))
    Win.configure(bg=global_bg)
    Win.title(lang["promoc"])
    Win.geometry('400x300')
    img = Image.open("icons/promocodes.png")
    icon_image = ImageTk.PhotoImage(img)
    Win.iconphoto(False, icon_image)
    Label(Win, text=lang["enter_p"],bg=global_bg,fg=global_fg).pack()
    ent = ctk.CTkEntry(Win,placeholder_text=lang['enter_p'])
    ent.pack()

    ttk.Button(Win, text=lang["act_c"], command=lambda: activate(promos, ent.get())).pack()
    ttk.Button(Win, text=lang["pol_c"], command=lambda: pol(promos)).pack()

    if os.path.exists("prm_c.db"):
        ttk.Button(Win, text=lang["my_c"], command=my_promos).pack()
def millioner(lang,root,start_time_,global_bg,global_fg,GlobalAlpha):
    def start_game():
        state = {
            'level': 1,
            'count': 0,
            'money': 50,
            'questions': [
                lang["q1"], lang["q2"], lang["q3"], lang["q4"], lang["q5"],
                lang["q6"], lang["q7"], lang["q8"], lang["q9"], lang["q10"],
                lang["q11"], lang["q12"], lang["q13"], lang["q14"], lang["q15"]
            ],
            'var1': [
                lang["c1"], lang["c2"], lang["c3"], lang["c4"], lang["c5"],
                lang["c6"], lang["c7"], lang["c8"], lang["c9"], lang["c10"],
                lang["c11"], lang["c12"], lang["c13"], lang["c14"], lang["c15"]
            ],
            'var2': [
                # q1
                lang["a1"], lang["a2"], lang["a3"], lang["c1"],
                # q2
                lang["a5"], lang["a6"], lang["a7"], lang["c2"],
                # q3
                lang["a8"], lang["a9"], lang["a10"], lang["c3"],
                # q4
                lang["a11"], lang["a12"], lang["a13"], lang["c4"],
                # q5
                lang["a14"], lang["a15"], lang["a16"], lang["c5"],
                # q6
                lang["a17"], lang["a18"], lang["a19"], lang["c6"],
                # q7
                lang["a20"], lang["a21"], lang["a22"], lang["c7"],
                # q8
                lang["a23"], lang["a24"], lang["a25"], lang["c8"],
                # q9
                lang["a26"], lang["a27"], lang["a28"], lang["c9"],
                # q10
                lang["a29"], lang["a30"], lang["a31"], lang["c10"],
                # q11
                lang["a32"], lang["a33"], lang["a34"], lang["c11"],
                # q12
                lang["a35"], lang["a36"], lang["a37"], lang["c12"],
                # q13
                lang["a38"], lang["a39"], lang["a40"], lang["c13"],
                # q14
                lang["a41"], lang["a42"], lang["a43"], lang["c14"],
                # q15
                lang["a44"], lang["a45"], lang["a46"], lang["c15"]
            ]
        }
        def center_child(window, parent):
            parent.update_idletasks()
            pw, ph, px, py = parent.winfo_width(), parent.winfo_height(), parent.winfo_x(), parent.winfo_y()
            ww, wh = window.winfo_width(), window.winfo_height()
            x, y = px + pw // 2 - ww // 2, py + ph // 2 - wh // 2
            window.geometry(f'{ww}x{wh}+{x}+{y}')
        def clear_window():
            for widget in Win.winfo_children():
                widget.destroy()
        def prover(answer, correct_answer, state):
            if answer == correct_answer:
                if state['level'] == 2:
                    state['money'] = 300
                elif state['level'] == 3:
                    state['money'] = 500
                elif state['level'] == 11:
                    state['money'] = 125000
                else:
                    state['money'] *= 2
                show_continue_window(state)
            else:
                messagebox.showerror(lang['nepr'], lang["answer_nepr"],parent=Win)
                Win.destroy()

        def show_continue_window(state):
            def yes():
                state['level'] += 1
                state['count'] += 1
                start(state)

            def no():
                global svb_coins
                svb_coins = load_balance(start_time_)
                svb_coins += int(state["money"])
                send('receipt', int(state["money"]))
                update_file("count_svbcoins.txt", int(state["money"]))
                save_balance(svb_coins,start_time_)
                check_ach(lang,start_time_)
                transactions(f"+{state['money']} SVB Coins",start_time_)
                messagebox.showinfo(lang["exit"], f"{lang['you_w']} {state['money']}SVB Coins",parent=Win)
                Win.destroy()

            w = Toplevel(Win)
            w.attributes("-alpha",float(GlobalAlpha))
            w.configure(bg=global_bg)
            w.geometry("300x100")
            center_child(w, Win)
            img = Image.open("icons/millionaire.png")
            icon_image = ImageTk.PhotoImage(img)
            w.iconphoto(False, icon_image)
            if state['count'] >= len(state['questions']) - 1:
                messagebox.showinfo(lang['pozdr'], lang["vigr"],parent=Win)
                Win.destroy()
            else:
                Label(w, text=lang["ans-ver"],bg=global_bg,fg=global_fg).pack()
                ttk.Button(w, text=lang["__yes__"], command=yes).pack()
                ttk.Button(w, text=lang["__no__"], command=no).pack()

        def start(state):
            clear_window()

            Label(Win, text=f"{lang['y_b']} {state['money']}$",bg=global_bg,fg=global_fg).pack()
            Label(Win, text=f"{state['count'] + 1}. {state['questions'][state['count']]}",bg=global_bg,fg=global_fg).pack()
            quist = StringVar()

            correct = state['var1'][state['count']]
            start_idx = state['count'] * 4
            options = state['var2'][start_idx:start_idx + 4]

            if correct not in options:
                options[0] = correct

            random.shuffle(options)

            for opt in options:
                ttk.Radiobutton(Win, text=opt, variable=quist, value=opt).pack()

            ttk.Button(Win, text=lang["rep"], command=lambda: prover(quist.get(), correct, state)).pack()

        Win = Toplevel(root)
        Win.attributes("-alpha",float(GlobalAlpha))
        Win.title(lang["mill"])
        Win.configure(bg=global_bg)
        Win.geometry("500x300")
        img = Image.open("icons/millionaire.png")
        icon_image = ImageTk.PhotoImage(img)
        Win.iconphoto(False, icon_image)
        ttk.Button(Win, text=lang['st_game'], command=lambda: start(state)).pack(pady=20)

    start_game()
def pokup_nomer(lang,root,edition,start_time_,global_bg,global_fg,GlobalAlpha):
    os.makedirs("tel", exist_ok=True)
    def tarif(operator):
        def sel(tarif, price):
            global svb_coins
            svb_coins = load_balance(start_time_)
            if svb_coins >= int(price):
                svb_coins -= int(price)
                send('payement', int(price))
                transactions(f"-{int(price)} SVb Coins" + f" {datetime.now()}",start_time_)
                save_balance(svb_coins,start_time_)
                n = ""
                number = []
                for i in range(2):
                    number.append(random.randint(1, 5))
                for i in range(7):
                    number.append(random.randint(0, 7))
                number.insert(0, "+")
                for nu in number:
                    n += str(nu)
                for name, details in tarifs.items():
                    parts = details.split("\n")
                    gb = parts[0].strip()
                    minu = parts[1].strip()
                    sms = parts[2].strip()
                with open("tel/confnum.cfg", "w", encoding='utf-8') as f:
                    f.write(
                        f"OPERATOR={operator} \n TARIF={tarif} \n INTERNET={str(gb)}\nSMS={str(sms)}\nMINUTES={str(minu)}")
                    f.close()
                if edition in ("Professional x64", "Gaming x64", "Professional x32", "Gaming x32"):
                    copy_file_to_folder("tel/number.cfg", "backup_data",start_time_ = start_time_)
                with open("tel/number.cfg", "w", encoding='utf-8') as f:
                    f.write(n)
                    f.close()
                if edition in ("Professional x64", "Gaming x64", "Professional x32", "Gaming x32"):
                    copy_file_to_folder("tel/number.cfg", "backup_data",start_time_ = start_time_)
                messagebox.showinfo(lang["success"], lang["pay-num"] + f'{tarif} - {n}',parent=winn)
            else:
                messagebox.showerror(lang["error"], lang["no_svb"],parent=winn)
                log_to_file(f"Message: {lang['no_svb']}", level="warning",start_time_ = start_time_)

        price = ["400", "700", "1300"]
        tarifs = {"Lite": f'4{lang["gb"]} \n 40{lang["minu"]} \n 50{lang["sms"]}',
                  "Standart": f'10{lang["gb"]} \n 70{lang["minu"]} \n 100{lang["sms"]}',
                  "Pro": f'∞{lang["gb"]} \n ∞{lang["minu"]} \n 350{lang["sms"]}'}
        winn = Toplevel(win)
        winn.attributes("-alpha",float(GlobalAlpha))
        winn.geometry("600x500")
        winn.title(lang["pok"])
        winn.configure(bg=global_bg)
        Label(winn, text=lang["tarifs_for"] + ' ' + operator,bg=global_bg,fg=global_fg).pack()
        for i, (name, description) in enumerate(tarifs.items()):
            Label(winn, text=f"{lang['tarif']} {name}:\n{description}\n{lang['price']} {price[i]} SVB Coins",
                  font=("Times", 15, "bold"),bg=global_bg,fg=global_fg).pack()

            ttk.Button(winn, text=lang["select"], command=lambda n=name, p=price[i]: sel(n, p)).pack()
    def change():
        def ch(op, tar):
            global svb_coins
            svb_coins = load_balance(start_time_)
            tarifs = {"Lite": f'4{lang["gb"]} \n 40{lang["minu"]} \n 50{lang["sms"]}',
                      "Standart": f'10{lang["gb"]} \n 70{lang["minu"]} \n 100{lang["sms"]}',
                      "Pro": f'∞{lang["gb"]} \n ∞{lang["minu"]} \n 350{lang["sms"]}'}
            if tar == "Lite":
                price = 400
            elif tar == "Standart":
                price = 700
            else:
                price = 1700
            if svb_coins >= price:
                svb_coins -= price
                send('payement', int(price))
                transactions(f"-{price} SVb Coins" + f" {datetime.now()}",start_time_)
                save_balance(svb_coins,start_time_)
                n = ""
                number = []
                for i in range(2):
                    number.append(random.randint(1, 5))
                for i in range(7):
                    number.append(random.randint(0, 7))
                number.insert(0, "+")
                for nu in number:
                    n += str(nu)
                for t_name, details in tarifs.items():
                    if t_name == tar:
                        parts = details.split("\n")
                        gb = parts[0].strip()
                        minu = parts[1].strip()
                        sms = parts[2].strip()
                        break

                with open("tel/confnum.cfg", "w", encoding="utf-8") as f:
                    f.write(
                        f"OPERATOR={op} \nTARIF={tar} \nINTERNET={str(gb)}\nSMS={str(sms)}\nMINUTES={str(minu)}")
                    f.close()
                if edition in ("Professional x64", "Gaming x64", "Professional x32", "Gaming x32"):
                    copy_file_to_folder("tel/confnum.cfg", "backup_data",start_time_ = start_time_)
                with open("tel/number.cfg", "w", encoding='utf-8') as f:
                    f.write(n)
                    f.close()
                if edition in ("Professional x64", "Gaming x64", "Professional x32", "Gaming x32"):
                    copy_file_to_folder("tel/confnum.cfg", "backup_data",start_time_ = start_time_)
                messagebox.showinfo(lang["success"], lang["pay-num"] + f' {tar} - {n}',parent=winn)
            else:
                messagebox.showerror(lang["error"], lang["no_svb"],parent=winn)
                log_to_file(f"Message: {lang['no_svb']}", level="warning",start_time_ = start_time_)

        winn = Toplevel(win)
        
        winn.geometry("600x500")
        winn.title(lang["pok"])
        winn.configure(bg=global_bg)
        with open("tel/confnum.cfg", "r", encoding='utf-8') as f:
            for line in f:
                key2, value1 = line.strip().split("=")
                config[key2] = value1
        t = config.get("TARIF")
        o = config.get("OPERATOR")
        oper = ["MBC", 'Tievstar', 'Bibline', "Lifebell"]
        var = StringVar(value='Tievstar')
        ttk.Combobox(winn, values=oper, textvariable=var, state="readonly").pack()
        trf = ["Lite", 'Standart', 'Pro']
        var1 = StringVar(value="Standart")
        ttk.Combobox(winn, values=trf, textvariable=var1, state="readonly").pack()
        ttk.Button(winn, text=lang["select"], command=lambda: ch(var.get(), var1.get())).pack()

    win = Toplevel(root)
    win.attributes("-alpha",float(GlobalAlpha))
    win.geometry("600x500")
    win.title(lang["pok"])
    win.configure(bg=global_bg)
    img = Image.open("icons/telephone.png")
    icon_image = ImageTk.PhotoImage(img)
    win.iconphoto(False, icon_image)
    win.salami = ImageTk.PhotoImage(
        Image.open('icons/tel/unnamed.png').resize((52, 52), Image.Resampling.LANCZOS)
    )
    win.pep = ImageTk.PhotoImage(
        Image.open('icons/tel/lifecell_logo_FKQVHlq.png').resize((52, 52), Image.Resampling.LANCZOS)
    )
    win.che = ImageTk.PhotoImage(
        Image.open('icons/tel/haafv9rx.jpg').resize((52, 52), Image.Resampling.LANCZOS)
    )
    win.che1 = ImageTk.PhotoImage(
        Image.open('icons/tel/com.kyivstar.mykyivstar.icon.2024-02-19-01-42-34.png').resize((52, 52),
                                                                                            Image.Resampling.LANCZOS)
    )
    left_frame = Frame(win)
    right_frame = Frame(win)
    if os.path.exists("tel/number.cfg"):
        with open("tel/confnum.cfg", "r", encoding='utf-8') as f:
            for line in f:
                key2, value1 = line.strip().split("=")
                config[key2] = value1
            try:
                with open("tel/number.cfg", "r") as f:
                    num = f.read()
                    f.close()
            except:
                pass
            tarif = config.get("TARIF")
            ope = config.get("OPERATOR")
            inter = config.get("INTERNET")
            sms = config.get("SMS")
            mint = config.get("MINUTES")

            Label(win, text=lang["your_ph"] + f' {num}', font=("Arial", 13, "bold"),bg=global_bg,fg=global_fg).pack()
            Label(win,
                  text=f"{lang['ope']} - {ope} \n {lang['tar']} - {tarif} \n {lang['min']} - {mint} \n {lang['smss']} - {sms} \n {lang['int']} - {inter} \n",
                  font=("Times", 15, "bold"),bg=global_bg,fg=global_fg).pack()
            ttk.Button(win, text=lang["change_op"], command=change).pack()
    else:
        left_frame.pack(side="left", anchor="n", padx=20, pady=20)
        right_frame.pack(side="left", anchor="n", padx=20, pady=20)
        Label(left_frame, image=win.salami).pack()
        Label(left_frame, text="MBC",bg=global_bg,fg=global_fg).pack()
        ttk.Button(left_frame, text=lang["select"], command=lambda: tarif("mbc")).pack()

        Label(left_frame, image=win.pep).pack()
        Label(left_frame, text='Lifebell',bg=global_bg,fg=global_fg).pack()
        ttk.Button(left_frame, text=lang["select"], command=lambda: tarif("Lifebell")).pack()

        Label(left_frame, image=win.che).pack()
        Label(left_frame, text='Bibline',bg=global_bg,fg=global_fg).pack()
        ttk.Button(left_frame, text=lang["select"], command=lambda: tarif("Bibline")).pack()

        Label(left_frame, image=win.che1).pack()
        Label(left_frame, text='Tievstar',bg=global_bg,fg=global_fg).pack()
        ttk.Button(left_frame, text=lang["select"], command=lambda: tarif("Tievstar")).pack()
def open_mus(lang,root,actives_programs,volume,state_sound,errors,start_time_,global_bg,global_fg,GlobalAlpha):
    actives_programs.append("Musical player")
    global playlists, current_playlist, paused
    import os
    import json
    from tkinter import filedialog, messagebox, ttk
    import pygame
    import random
    pygame.mixer.init()
    play_sound("sound//click.mp3",volume,state_sound,start_time_)

    os.makedirs("music", exist_ok=True)
    if os.path.exists("music/playlists.json"):
        with open("music/playlists.json", "r") as f:
            playlists = json.load(f)
    else:
        playlists = {}

    def save_playlists():
        os.makedirs("music", exist_ok=True)
        with open("music/playlists.json", "w") as f:
            json.dump(playlists, f)

    def add_songs():
        global current_playlist
        if not current_playlist:
            messagebox.showwarning(lang["error"], lang["select_pl"],parent=Winn)
            return

        files = filedialog.askopenfilenames(filetypes=[("MP3 files", "*.mp3")])
        if files:
            playlists[current_playlist].extend(files)
            update_playlist()
            save_playlists()
        else:
            messagebox.showwarning(lang["error"], lang["sel"],parent=Winn)

    def create_playlist():
        global current_playlist
        name = playlist_entry.get().strip()
        if name == "":
            messagebox.showwarning(lang["error"], lang["no_pus"],parent=Winn)
            return
        if name in playlists:
            messagebox.showwarning(lang["error"], lang["suchect"],parent=Winn)
            return
        playlists[name] = []
        playlist_listbox.insert(END, name)
        current_playlist = name
        save_playlists()
        messagebox.showinfo(lang["success"], f"{lang['playlist']} '{name}' {lang['creat_succesfully']}",parent=Winn)

    def select_playlist():
        global current_playlist
        try:
            current_playlist = playlist_listbox.get(playlist_listbox.curselection())
            update_playlist()
        except:
            pass

    def update_playlist():
        song_listbox.delete(0, END)
        for song in playlists.get(current_playlist, []):
            song_listbox.insert(END, os.path.basename(song))

    def play_song():
        global current_song
        try:
            selected_index = song_listbox.curselection()[0]
            current_song = playlists[current_playlist][selected_index]
            pygame.mixer.music.load(current_song)
            pygame.mixer.music.play()
            animate_beats()
        except IndexError:
            messagebox.showwarning(lang["error"], lang["select_mus"],parent=Winn)

    def toggle_pause():
        global paused
        if pygame.mixer.music.get_busy():
            if paused:
                pygame.mixer.music.unpause()
            else:
                pygame.mixer.music.pause()
            paused = not paused

    def stop_song():
        pygame.mixer.music.stop()
        canvas.delete("all")

    def remove_song():
        try:
            selected_index = song_listbox.curselection()[0]
            del playlists[current_playlist][selected_index]
            update_playlist()
            save_playlists()
        except IndexError:
            messagebox.showwarning(lang["error"], lang["select_mus_del"],parent=Winn)

    def animate_beats():
        if not pygame.mixer.music.get_busy():
            return

        canvas.delete("all")
        volume = random.randint(10, 100)
        for i in range(22):
            x = 20 + i * 38
            height = max(5, (volume / 100) * random.randint(10, 100))
            canvas.create_rectangle(x, 200 - height, x + 20, 200, fill="white")

        root.after(100, animate_beats)

    Winn = Toplevel(root)
    Winn.attributes("-alpha",float(GlobalAlpha))
    Winn.title(lang["mus_pl"])
    Winn.geometry(f"1200x800")
    Winn.configure(bg=global_bg)
    img = Image.open("icons/mediaplayer.png")
    icon_image = ImageTk.PhotoImage(img)
    Winn.iconphoto(False, icon_image)
    playlist_frame = Frame(Winn)
    playlist_frame.pack()

    playlist_entry = Entry(playlist_frame, bg="gray", fg="black")
    playlist_entry.pack(side=LEFT)

    style1 = ttk.Style()
    style1.configure("Green1.TButton")

    create_playlist_button = ttk.Button(playlist_frame, text=lang["create-pl"], command=create_playlist,
                                        style="Green1.TButton")
    create_playlist_button.pack(side=RIGHT)

    playlist_listbox = Listbox(Winn, fg="black")
    playlist_listbox.pack(fill=X)
    playlist_listbox.bind("<<ListboxSelect>>", lambda e: select_playlist())

    song_listbox = Listbox(Winn)
    song_listbox.pack(fill=BOTH, expand=True, padx=10, pady=10)

    add_button = ttk.Button(Winn, text=lang["add-mus"], command=add_songs, style="Green1.TButton")
    add_button.pack(fill=X)

    play_button = ttk.Button(Winn, text=lang["pllay"], command=play_song, style="Green1.TButton")
    play_button.pack(fill=X)

    pause_button = ttk.Button(Winn, text=lang["pause-mus"], command=toggle_pause, style="Green1.TButton")
    pause_button.pack(fill=X)

    stop_button = ttk.Button(Winn, text=lang["dell_mus"], command=stop_song, style="Green1.TButton")
    stop_button.pack(fill=X)

    remove_button = ttk.Button(Winn, text=lang["delete_mus"], command=remove_song, style="Green1.TButton")
    remove_button.pack(fill=X)

    canvas = Canvas(Winn, width=900, height=200)
    canvas.pack()

    for name in playlists.keys():
        playlist_listbox.insert(END, name)

    Winn.mainloop()
def textSpeech(root,lang,global_bg,global_fg,globalalpha):
    def textToSpeech(text, filename):
        engine = pyttsx3.init()

        rate = engine.getProperty('rate')
        engine.setProperty('rate', rate + 1)

        volume = engine.getProperty('volume')
        engine.setProperty('volume', volume + 0.1)

        engine.save_to_file(text, filename)
        engine.runAndWait()

        messagebox.showinfo(lang["success"], lang["text_speeched_successfully"] + filename)
    Win = create_window(root,lang["textSpeech"],global_bg,globalalpha,500,400,"icons/Text Speech.png")

    Label(Win,text = lang["enter_text_to_speech"],background=global_bg,foreground=global_fg).pack()
    text = ttk.Entry(Win)
    text.pack()

    Label(Win, text=lang["enter_path_to_save"], background=global_bg, foreground=global_fg).pack()
    path = ttk.Entry(Win)
    path.pack()

    btn = ttk.Button(Win,text = "OK",command = lambda: textToSpeech(text.get()))
    btn.pack()
def ytDownloader(root,lang,global_bg,global_fg,globalalpha):
    def download(link):
        yt = YouTube(link)

        try:
            stream = yt.streams.get_highest_resolution()
            stream.download()

            messagebox.showinfo(lang["success"],lang["video_downloaded_successfully"])
        except Exception as e:
            messagebox.showerror(lang['error'],str(e))
    Win = create_window(root, lang["ytDownloader"], global_bg, globalalpha, 300, 300,"icons/Youtube Downloader.png")

    Label(Win,text = lang['enter_link_for_video']).pack()

    link = ttk.Entry(Win)
    link.pack()

    btn = ttk.Button(Win,text = lang["download_video"],command = lambda:download(link.get()))
    btn.pack()
def weatherWin(root,lang,global_bg,global_fg,globalalpha,start_time_):
    def get_weather():
        city = entry_city.get()

        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=ru"

        response = requests.get(url, timeout=5)
        data = response.json()

        if str(data["cod"]) != "200":
            log_to_file(data,start_time_,"error")
            lbl_result.config(text=lang["api_error"])
            return

        temp = data["main"]["temp"]
        weather = data["weather"][0]["description"]
        icon = data["weather"][0]["icon"]

        lbl_result.config(text=f"{city}\n{temp}°C\n{weather}")

        icon_url = f"http://openweathermap.org/img/wn/{icon}@2x.png"
        img_data = requests.get(icon_url).content

        img = Image.open(BytesIO(img_data))
        photo = ImageTk.PhotoImage(img)

        lbl_icon.config(image=photo)
        lbl_icon.image = photo
    Win = create_window(root,lang["weather"],global_bg,globalalpha,350,300,"icons/weather.png")

    entry_city = ttk.Entry(Win, font=15)
    entry_city.pack(pady=10)

    btn = ttk.Button(Win, text=lang["get_weather"], command=get_weather)
    btn.pack(pady=5)

    lbl_result = ttk.Label(Win, text="", font=14,background=global_bg,foreground=global_fg)
    lbl_result.pack(pady=10)

    lbl_icon = ttk.Label(Win,background=global_bg,foreground=global_fg)
    lbl_icon.pack()
