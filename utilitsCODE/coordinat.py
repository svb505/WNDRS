import sqlite3
from tkinter import*
from tkinter import ttk,messagebox,colorchooser
from datetime import datetime,timedelta
import tabulate
import random
from PIL import Image, ImageTk
from crypto_work import load_key,decrypt_message,encrypt_message
from create_window import create_window

current_step = 50
background_color = ''
main_line_color = "black"
line_color = "grey"
text_color = "black"
fill_line = "red"
fill_text = "blue"
color_dot = "blue"
global_color = None
color = None
score = 0
main_theme = ''
chif_x = True
chif_y = True
level = "2"
booster_active = False
last_booster_activation_time = None
flag = False

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
username = n


key = load_key()
with open("games/coordinat_settings/step.cfg","rb") as f:
    current_step = int(decrypt_message(f.read(),key))
with open("games/coordinat_settings/theme.cfg", "rb") as f:
    main_theme = decrypt_message(f.read(),key)
    if main_theme == "Black":
        background_color = "Black"
        main_line_color = "White"
        line_color = "grey"
        fill_line = "red"
        fill_text = "blue"
        text_color = "White"
        main_theme = "Black"
    if main_theme == "White":
        background_color = "White"
        main_line_color = "Black"
        line_color = "grey"
        text_color = "Black"
        fill_line = "red"
        fill_text = "blue"
        main_theme = "White"
    if main_theme == "Rainbow":
        background_color = "#00008B"
        main_line_color = "#FFFF00"
        line_color = "#00FFFF"
        text_color = "#FFFFFF"
        fill_text = "white"
        main_theme = "Rainbow"
    if main_theme  == "Leto":
        background_color = "#FF0000"
        main_line_color = "#FFFF00"
        line_color = "#FF8C00"
        text_color = "#FFFFFF"
        fill_text = "white"
        fill_line = "white"
        main_theme = "Leto"
with open("games/coordinat_settings/chiffres.cfg", "rb") as f:
    c = decrypt_message(f.read(),key)
    if c == "x":
        chif_x = False
        chif_y = True
    if c == "y":
        chif_x = True
        chif_y = False
    if c == "all":
        chif_x = False
        chif_y = False
    if c == ("true"):
        chif_x = True
        chif_y = True
with open("games/coordinat_settings/lvl.cfg", "rb") as f:
    level = decrypt_message(f.read(),key)
with open("games/coordinat_settings/color.cfg","rb")as f:
    color_dot = decrypt_message(f.read(),key)

def main_window(root,lang,start_time_,GlobalAlpha,global_bg):
    global username
    def resize(event=None):
        global current_step,background_color,line_color,main_line_color,text_color,fill_line,fill_text,color_dot,chif_y,chif_x

        new_width = canvas.winfo_width()
        new_height = canvas.winfo_height()
        if new_width == 1 or new_height == 1:
            new_width = Win.winfo_width() - 20
            new_height = Win.winfo_height() - 20
        canvas.config(width=new_width, height=new_height, bg=background_color)
        canvas.delete("all")
        step = current_step

        canvas.create_line(0, new_height // 2, new_width, new_height // 2, activefill=fill_line, fill=main_line_color,
                           arrow="last", width=2)
        canvas.create_line(new_width // 2, new_height, new_width // 2, 0, activefill=fill_line, fill=main_line_color,
                           arrow="last", width=2)
        canvas.create_text(new_width - 10, new_height // 2 + 13, text="X", activefill=fill_text, fill=text_color)

        canvas.create_text(new_width // 2 - 10, 10, text="Y", activefill=fill_text, fill=text_color)
        x1 = new_width // 2 + step
        x2 = new_width // 2 - step
        while x1 < new_width:
            canvas.create_line(x1, 0, x1, new_height, fill=line_color)
            canvas.create_line(x2, 0, x2, new_height, fill=line_color)
            x1 += step
            x2 -= step
        y1 = new_height // 2 + step
        y2 = new_height // 2 - step
        while y1 < new_height:
            canvas.create_line(0, y1, new_width, y1, fill=line_color)
            canvas.create_line(0, y2, new_width, y2, fill=line_color)
            y1 += step
            y2 -= step

        if chif_x:
            x = new_width // 2 + step
            num = step
            while x < new_width:
                canvas.create_text(x, new_height // 2 + 13, text=num, activefill=fill_text, fill=text_color)
                canvas.create_text(new_width // 2 - num, new_height // 2 + 13, text=-num, activefill=fill_text,
                                   fill=text_color)
                num += step
                x += step
            canvas.create_text(new_width // 2 - 10, new_height // 2 + 13, text="0", activefill=fill_text,
                               fill=text_color)

        if chif_y:
            x = new_width // 2 - 15
            y = new_height // 2 - step
            num = step
            while y > 0:
                canvas.create_text(x, y + 10, text=num, activefill=fill_text, fill=text_color)
                canvas.create_text(x, new_height // 2 + num, text=-num, activefill=fill_text, fill=text_color)
                num += step
                y -= step
    def help_click():
        messagebox.showinfo(lang["coordinat"], lang["developpercoor"])
    def help_game():
        messagebox.showinfo(lang["coordinat"],
                            lang["infocoord1"])
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
    def parametr():
        global parametrs_window, color, current_step, main_theme, level
        parametrs_window = create_window(Win, lang['parametr'], global_bg, float(GlobalAlpha), 600, 600,"icons/coordinat.png")
        parametrs_window.resizable(False, False)
        center_child(parametrs_window, Win)
        parametrs_window.protocol("WM_DELETE_WINDOW",
                                  lambda: dismiss(parametrs_window))

        lbl1 = Label(parametrs_window, text=lang["sizeklet"])
        lbl1.grid(row=0, column=0)

        sttep = ["25", "50", "75", "100"]
        step = StringVar()

        combobox = ttk.Combobox(parametrs_window, values=sttep, textvariable=step, state="readonly", width=3)
        combobox.grid(row=1, column=0, sticky=N, padx=10, pady=10)

        def set_initial_value():
            combobox.set(str(current_step))

        parametrs_window.after(100, set_initial_value)

        frmtheme = LabelFrame(parametrs_window, borderwidth=0.5, relief=SOLID, text=lang["themes"])
        frmtheme.grid(row=2, column=0, padx=5, sticky=NW)

        theme_var = StringVar()

        Blacktheme = ttk.Radiobutton(frmtheme, text=lang["darktheme"], variable=theme_var, value="Black")
        Blacktheme.grid(row=0, column=0, padx=10, pady=5, sticky=W)

        Whitetheme = ttk.Radiobutton(frmtheme, text=lang["whitetheme"], variable=theme_var, value="White")
        Whitetheme.grid(row=1, column=0, padx=10, pady=5, sticky=W)

        Standarttheme = ttk.Radiobutton(frmtheme, text=lang["wintertheme"], variable=theme_var, value="Rainbow")
        Standarttheme.grid(row=2, column=0, padx=10, pady=5, sticky=W)

        Letotheme = ttk.Radiobutton(frmtheme, text=lang["summertheme"], variable=theme_var, value="Leto")
        Letotheme.grid(row=3, column=0, padx=10, pady=5, sticky=W)

        if main_theme == "Black":
            theme_var.set("Black")
        elif main_theme == "White":
            theme_var.set("White")
        elif main_theme == "Rainbow":
            theme_var.set("Rainbow")
        else:
            theme_var.set("Leto")

        frmcheckboks = LabelFrame(parametrs_window, borderwidth=0.5, relief=SOLID, text=lang["metki"])
        frmcheckboks.grid(row=2, column=1, padx=5, pady=5, sticky=NW)

        chiffres_var = StringVar()

        vkl = ttk.Radiobutton(frmcheckboks, text=lang["show_all"], variable=chiffres_var, value="true")
        vkl.grid(row=0, column=1, sticky=W)
        skill_x = ttk.Radiobutton(frmcheckboks, text=lang["show_x"], variable=chiffres_var, value="x")
        skill_x.grid(row=1, column=1, sticky=W)

        skill_y = ttk.Radiobutton(frmcheckboks, text=lang["show_y"], variable=chiffres_var, value="y")
        skill_y.grid(row=2, column=1, sticky=W)

        skill_all = ttk.Radiobutton(frmcheckboks, text=lang["not_show"], variable=chiffres_var, value="all")
        skill_all.grid(row=3, column=1, sticky=W)

        if chif_x and chif_y:
            chiffres_var.set("true")
        elif chif_x:
            chiffres_var.set("y")
        elif chif_y:
            chiffres_var.set("x")
        else:
            chiffres_var.set("all")

        frmcolor = LabelFrame(parametrs_window, borderwidth=0.5, relief=SOLID, text=lang["color_dot"])
        frmcolor.grid(row=2, column=2, padx=5, pady=5, sticky=NW)

        choose_color_button = ttk.Button(frmcolor, text=lang["select_coord"], command=lambda: choose_color(parametrs_window))
        choose_color_button.grid(row=1, column=3, padx=10, pady=5, sticky=W)

        frmlevel = LabelFrame(parametrs_window, borderwidth=0.5, relief=SOLID, text=lang["level_coordi"])
        frmlevel.grid(row=3, column=0, padx=5, pady=5, sticky=NW)

        level_var = StringVar()

        level1 = ttk.Radiobutton(frmlevel, text=lang["level1"], variable=level_var, value="1")
        level1.grid(row=0, column=0, sticky=W)
        level2 = ttk.Radiobutton(frmlevel, text=lang["level2"], variable=level_var, value="2")
        level2.grid(row=1, column=0, sticky=W)
        level3 = ttk.Radiobutton(frmlevel, text=lang["level3"], variable=level_var, value="3")
        level3.grid(row=2, column=0, sticky=W)

        if level == "1":
            level_var.set("1")
        elif level == "2":
            level_var.set("2")
        else:
            level_var.set("3")

        ok_button = ttk.Button(parametrs_window, text=lang["okay"],
                               command=lambda: ok_click(combobox, parametrs_window, theme_var, chiffres_var, level_var))
        ok_button.grid(row=4, column=1, padx=5, pady=5, sticky=E)
        otmena_button = ttk.Button(parametrs_window, text=lang["cancel_coor"], command=lambda: dismiss(parametrs_window))
        otmena_button.grid(row=4, column=2, padx=5, pady=5, sticky=W)

        parametrs_window.grab_set()
    def choose_color(parameters_window):
        global color_dot
        parameters_window.grab_release()
        color_code = colorchooser.askcolor(title=lang["selected_color_coor"],parent = Win)[1]
        parameters_window.grab_set()
        if color_code:
            color_dot = color_code
        key = load_key()
        with open("games/coordinat_settings/color.cfg","wb")as f:
            f.write(encrypt_message(str(color_dot),key))
        parameters_window.focus_set()
    def ok_click(combobox, parameters_window, theme_var, chiffres_var, level_var):
        global current_step
        global background_color
        global main_line_color
        global line_color
        global text_color
        global fill_line
        global fill_text
        global color_dot
        global global_color
        global color
        global main_theme
        global chif_x
        global chif_y
        global level
        if combobox.get() != '':
            current_step = int(combobox.get())
        with open("games/coordinat_settings/step.cfg","wb") as f:
            key = load_key()
            f.write(encrypt_message(str(current_step),key))

        if theme_var.get() == "Black":
            background_color = "Black"
            main_line_color = "White"
            line_color = "grey"
            fill_line = "red"
            fill_text = "blue"
            text_color = "White"
            main_theme = "Black"
        if theme_var.get() == "White":
            background_color = "White"
            main_line_color = "Black"
            line_color = "grey"
            text_color = "Black"
            fill_line = "red"
            fill_text = "blue"
            main_theme = "White"
        if theme_var.get() == "Rainbow":
            background_color = "#00008B"
            main_line_color = "#FFFF00"
            line_color = "#00FFFF"
            text_color = "#FFFFFF"
            fill_text = "white"
            main_theme = "Rainbow"
        if theme_var.get() == "Leto":
            background_color = "#FF0000"
            main_line_color = "#FFFF00"
            line_color = "#FF8C00"
            text_color = "#FFFFFF"
            fill_text = "white"
            fill_line = "white"
            main_theme = "Leto"
        if color:
            pass

        if chiffres_var.get() == "x":
            chif_x = False
            chif_y = True
        if chiffres_var.get() == "y":
            chif_x = True
            chif_y = False
        if chiffres_var.get() == "all":
            chif_x = False
            chif_y = False
        if chiffres_var.get() == ("true"):
            chif_x = True
            chif_y = True
        if level_var.get() == "1":
            level = "1"
        elif level_var.get() == "2":
            level = "2"
        else:
            level = "3"
        key = load_key()
        tema = theme_var.get()
        ch = chiffres_var.get()
        lvl = level_var.get()
        with open("games/coordinat_settings/theme.cfg","wb") as f:
            f.write(encrypt_message(str(tema),key))
        with open("games/coordinat_settings/chiffres.cfg","wb") as f:
            f.write(encrypt_message(str(ch),key))
        with open("games/coordinat_settings/lvl.cfg","wb") as f:
            f.write(encrypt_message(str(lvl),key))
        parametrs_window.destroy()
        resize()
    def config_win1():
        Win.update_idletasks()

        screen_width = Win.winfo_screenwidth()
        screen_height = Win.winfo_screenheight()

        x = int((screen_width / 2) - (screen_width / 2))
        y = int((screen_height / 2) - (screen_height / 2))

        Win.geometry(f"{screen_width}x{screen_height}+{x}+{y}")

        Win.state('zoomed')
    def info_win():

        information_win = create_window(Win, lang['infocoord'], global_bg, float(GlobalAlpha), 150, 100, "icons/coordinat.png")
        center_child(information_win, Win)
        information_win.protocol("WM_DELETE_WINDOW",
                                 lambda: dismiss(information_win))

        label1 = Label(information_win, text=f"{lang['youre_score_coor']}: {score}")
        label1.pack()

        information_win.grab_set()
    def exit_cascade(event = None):
        def yes_button():

            conn = sqlite3.connect('games/playersinffo.db')

            cursor = conn.cursor()

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS players (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    score INTEGER,
                    theme TEXT,
                    square_size INTEGER,
                    visible_numbers CHAR,
                    level CHAR,
                    color_point TEXT,
                    time TEXT
                )
            ''')
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            cursor.execute('''
                INSERT INTO players (name, score,theme,square_size,visible_numbers,level,color_point,time) VALUES (?,?,?,?,?,?,?,?)
            ''', (username, score, main_theme, current_step, chif_x, level, color_dot, current_time))

            cursor.execute('''SELECT * FROM players ''')

            conn.commit()
            conn.close()
            exit_win.destroy()
            Win.destroy()

        def non_button():
            exit_win.destroy()


        exit_win = create_window(Win, lang['exit_coor'], global_bg, float(GlobalAlpha), 250, 120, "icons/coordinat.png")
        exit_win.resizable(False, False)
        center_child(exit_win, Win)
        exit_win.protocol("WM_DELETE_WINDOW", lambda: dismiss(exit_win))


        labbl = Label(exit_win, text=f"{lang['you_zarabotal']} {score} {lang['ochkov']}")
        labbl.pack()
        label1 = Label(exit_win, text=lang["you_sure_to_exit"])
        label1.pack()
        btn1 = ttk.Button(exit_win, text=lang["yes_coor"], command=yes_button)
        btn1.pack()
        btn2 = ttk.Button(exit_win, text=lang["no_coor"], command=non_button)
        btn2.pack()
        exit_win.grab_set()
    def on_closing():
        if flag == True:
            conn = sqlite3.connect('games/playersinffo.db')
            cursor = conn.cursor()
            cursor.execute('''
                                CREATE TABLE IF NOT EXISTS players (
                                    id INTEGER PRIMARY KEY,
                                    name TEXT,
                                    score INTEGER,
                                    theme TEXT,
                                    square_size INTEGER,
                                    visible_numbers CHAR,
                                    level CHAR,
                                    color_point TEXT,
                                    time TEXT
                                )
                            ''')
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute('''
                        INSERT INTO players (name, score,theme,square_size,visible_numbers,level,color_point,time) VALUES (?,?,?,?,?,?,?,?)
                    ''', (username, score, main_theme, current_step, chif_x, level, color_dot, current_time))
            cursor.execute('''SELECT * FROM players ''')
            conn.commit()
            conn.close()

        Win.destroy()
    def infoplayers():
        information_win = create_window(Win, lang['infocoord'], global_bg, float(GlobalAlpha), 550, 350,"icons/coordinat.png")
        information_win.resizable(False, False)
        center_child(information_win, Win)
        information_win.protocol("WM_DELETE_WINDOW",
                                 lambda: dismiss(information_win))

        n = Text(information_win)
        scrollbar = Scrollbar(information_win, command=n.yview)
        n.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=RIGHT, fill=Y)
        n.pack()

        conn = sqlite3.connect('playersinffo.db')
        cursor = conn.cursor()
        cursor.execute('''SELECT name, SUM(score) AS total_score
    FROM players
    GROUP BY name
    ORDER BY total_score DESC;''')
        rows = cursor.fetchall()

        columns = ["Name", "Score"]

        results = tabulate.tabulate(rows, headers=columns, tablefmt="center")

        n.insert(1.0, str(results) + '\n')
        conn.commit()
        conn.close()
    def win_booster():
        def no_activ_booster():
            booster_win.destroy()
        booster_win = create_window(Win, lang['booster'], global_bg, float(GlobalAlpha), 400, 150,"icons/coordinat.png")
        booster_win.resizable(False, False)
        center_child(booster_win, Win)
        booster_win.protocol("WM_DELETE_WINDOW",
                                 lambda: dismiss(booster_win))
        lbl = Label(booster_win,text = lang["infobuster"])
        lbl.pack()
        lbl1 = Label(booster_win,text=lang["info2buster"])
        lbl1.pack()
        btn1 = ttk.Button(booster_win,text = lang["activatebuster"], command = booster_activate)
        btn1.pack()
        btn2 = ttk.Button(booster_win,text=lang["notactivatebuster"],command = no_activ_booster)
        btn2.pack()
    def booster_activate():
        global booster_active, last_booster_activation_time

        if last_booster_activation_time is not None:
            time_passed = datetime.now() - last_booster_activation_time
            if time_passed < timedelta(hours=6):
                remaining_time = timedelta(hours=6) - time_passed
                messagebox.showinfo(lang["busternedos"],
                                    f"{lang['timetoactivate']} {remaining_time}.")
                return

        booster_active = True
        last_booster_activation_time = datetime.now()
        messagebox.showinfo(lang["boosteractivated"],
                            lang["your_score_has_been_double"])
        Win.after(180000, booster_deactivate)
    def booster_deactivate():
        global booster_active
        booster_active = False
        messagebox.showinfo(lang["buster_deactivated"], lang["deistvie_zak"])
    def level_state():
        information_win = create_window(Win, lang['infocoord'], global_bg, float(GlobalAlpha), 700, 350, "icons/coordinat.png")
        information_win.resizable(False, False)
        center_child(information_win, Win)
        information_win.protocol("WM_DELETE_WINDOW",
                                 lambda: dismiss(information_win))
        n = Text(information_win)
        scrollbar = Scrollbar(information_win, command=n.yview)
        n.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=RIGHT, fill=Y)
        n.pack()
        n.tag_configure('custom_font', font=('Helvetica', 10, 'bold'))
        n.insert(1.0, f"{lang['levels_stat']} \n", 'custom_font')
        conn = sqlite3.connect('games/playersinffo.db')
        cursor = conn.cursor()
        cursor.execute('''SELECT level,COUNT(level)
                            FROM players
                            GROUP BY level
                            ORDER BY level ASC;
                        ''')
        rows = cursor.fetchall()

        columns = ["Level's", "Count"]
        results = tabulate.tabulate(rows, headers=columns, tablefmt="center")

        n.insert(END, str(results) + '\n \n' )
        cursor.execute('''SELECT theme,COUNT(theme)
                                    FROM players
                                    GROUP BY theme
                                    ORDER BY theme DESC;
                                ''')
        rows = cursor.fetchall()
        columns = ["Theme's", "Count"]
        results = tabulate.tabulate(rows, headers=columns, tablefmt="center")
        n.insert(END, f"{lang['themes_stat']}\n", 'custom_font')
        n.insert(END, str(results) + '\n\n')
        cursor.execute('''SELECT name,AVG(score) as score
                                            FROM players
                                            GROUP BY name
                                            ORDER BY score DESC;
                                        ''')
        rows = cursor.fetchall()

        columns = ["Name","Average"]

        results = tabulate.tabulate(rows, headers=columns, tablefmt="center")
        n.insert(END, f"{lang['avg_score']}\n", 'custom_font')
        n.insert(END, str(results) + '\n')
        conn.commit()
        conn.close()
    def all_users_parametr():
        information_win = create_window(Win, lang['infocoord'], global_bg, float(GlobalAlpha), 700, 350, "icons/coordinat.png")
        information_win.resizable(False, False)
        center_child(information_win, Win)
        information_win.protocol("WM_DELETE_WINDOW",
                                 lambda: dismiss(information_win))
        n = Text(information_win)
        scrollbar = Scrollbar(information_win, command=n.yview)
        n.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=RIGHT, fill=Y)
        n.pack()

        conn = sqlite3.connect('games/playersinffo.db')
        cursor = conn.cursor()
        cursor.execute('''SELECT name,
           score, 
            theme,
           square_size,
           level,
           color_point,
           time
    FROM players
    ORDER BY name DESC;''')
        rows = cursor.fetchall()
        columns = ["Name", "Score", "Theme","Square", "Level", "Dot Color", "Time"]

        results = tabulate.tabulate(rows, headers=columns, tablefmt="center")

        n.insert(1.0, str(results) + '\n')
        conn.commit()
        conn.close()
    def game():
        global flag
        flag = False
        def validate_entry(char, entry_value):
            if char in '0123456789-' or char == '\b':
                return True
            return False

        def send_x_y():
            global score
            global level
            global booster_active
            X = x - canvas.winfo_width() // 2
            Y = canvas.winfo_height() // 2 - y
            input1 = pole_x.get()
            input2 = pole_y.get()
            count = 0

            if level == "1":
                eps = 25
            elif level == "2":
                eps = 10
            else:
                eps = 5
            stroka = ""
            if booster_active:
                if abs(int(input1) - X) > eps:
                    count -= 1
                    stroka += lang["x_neug"]
                else:
                    count += 2
                if abs(int(input2) - Y) > eps:
                    count -= 1
                    stroka += lang['y_neug']
                else:
                    count += 2
                if count == -2:
                    score -= 2
                    stroka = lang["all_neug"]
                elif count == 0:
                    score += 2
                else:
                    score += 4
                    stroka = lang["all_ug"]
            else:
                if abs(int(input1) - X) > eps:
                    count -= 1
                    stroka += lang["x_neug"]
                else:
                    count += 1
                if abs(int(input2) - Y) > eps:
                    count -= 1
                    stroka += lang['y_neug']
                else:
                    count += 1
                if count == -2:
                    score -= 2
                    stroka = lang["all_neug"]
                elif count == 0:
                    score += 1
                else:
                    score += 2
                    stroka = lang["all_ug"]
            dot_win.destroy()
            messagebox.showinfo(title=lang['results'], message=stroka)

        global color_dot

        x = random.randint(5, int(canvas.winfo_width()))
        y = random.randint(5, int(canvas.winfo_height()))
        canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill=color_dot)

        dot_win = create_window(Win, lang['enter_coordinats'], global_bg, float(GlobalAlpha), 320, 200,"icons/coordinat.png")
        center_child(dot_win, Win)
        dot_win.protocol("WM_DELETE_WINDOW", lambda: dismiss(dot_win))
        vcmd = (dot_win.register(validate_entry), '%S', '%P')

        lbl_dot = Label(dot_win, text=lang["enter_x"])
        lbl_dot.pack(pady=5)

        pole_x = ttk.Entry(dot_win, validatecommand=vcmd, validate='key')
        pole_x.pack()

        lbl_y = Label(dot_win, text=lang["enter_y"])
        lbl_y.pack(pady=5)

        pole_y = ttk.Entry(dot_win, validatecommand=vcmd, validate='key')
        pole_y.pack(pady=5)

        btn_1 = ttk.Button(dot_win, text=lang["okay"], command=send_x_y)
        btn_1.pack(pady=5)


    Win = create_window(root, f"{lang['coordinat_tre']} - {username}", global_bg, float(GlobalAlpha), 700, 700,"icons/coordinat.png")
    Win.option_add("*tearOff", FALSE)

    main_menu = Menu(Win)
    view_menu = Menu(main_menu, tearoff=False)
    help_menu = Menu(main_menu)
    hlp_menu = Menu(view_menu)
    main_menu.add_cascade(label=lang["start"], command=game)
    main_menu.add_cascade(label=lang["vid"], menu=view_menu)
    main_menu.add_cascade(label=lang["spravka"], menu=help_menu)
    help_menu.add_cascade(label=lang['menu_score'], command=info_win)
    main_menu.add_command(label=lang["busters"], command=win_booster)
    main_menu.add_cascade(label=lang["exit"], command=exit_cascade)
    help_menu.add_cascade(label=lang["developpers_data"], command=help_click)
    help_menu.add_cascade(label=lang["game_data"], command=help_game)
    help_menu.add_cascade(label=lang['users_data'], menu = hlp_menu)
    hlp_menu.add_command(label = lang["all_param"], command = all_users_parametr)
    hlp_menu.add_command(label = lang["not_all_param"], command = infoplayers)
    hlp_menu.add_command(label=lang["stat"], command=level_state)
    view_menu.add_cascade(label=lang["parametr"], command=parametr)
    view_menu.add_command(label=lang["ves_ecran"], command=config_win1)

    Win.config(menu=main_menu)

    canvas = Canvas(Win, bg=background_color, width=480, height=480)
    canvas.pack(expand=True, fill=BOTH, padx=10, pady=10)
    Win.bind("<Configure>", resize)
    Win.protocol("WM_DELETE_WINDOW", on_closing)
    Win.focus_set()
    Win.update_idletasks()
    Win.bind('<Escape>', exit_cascade)
    Win.bind('<Alt-F4>', exit_cascade)