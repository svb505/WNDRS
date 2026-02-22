from tkinter import *
from tkinter import ttk
import sqlite3
from PIL import Image, ImageTk

svb_coins = 0

def load_balance():
    global svb_coins
    #log_to_file("load_balance")
    try:
        with open("bank/balance.bin", "rb") as f:
            # Чтение 4 байт из файла и преобразование в целое число
            svb_coins = int.from_bytes(f.read(4), byteorder='little', signed=True)
    except FileNotFoundError:
        # Если файл не существует, начинаем с нулевого баланса
        svb_coins = 0

def ach(root,lang,global_bg,global_fg,GlobalAlpha):
    def get_info():
        conn = sqlite3.connect("achievements.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM achievements")
        rows = cursor.fetchall()
        conn.close()
        return [{"name": row[0], "status": row[1], "max": row[2], "current": row[3],"prize":row[4]} for row in rows]
    Win = Toplevel(root)
    Win.attributes("-alpha",float(GlobalAlpha))
    Win.title(lang["ach"])
    Win.resizable(False,False)
    Win.geometry("500x400")
    Win.configure(bg=global_bg)
    img = Image.open("icons/medal.png")
    icon_image = ImageTk.PhotoImage(img)
    Win.iconphoto(False, icon_image)
    achievement = get_info()
    global svb_coins
    load_balance()
    Label(Win,text = lang["ach"],font = ("Arial",16,"bold"),fg=global_fg,bg=global_bg).pack()
    for i in achievement:
        if i["status"] == "no":
            i["current"] = svb_coins
            if i['name'] == "million":
                Label(Win, text=lang["ach_million"],font = ("Courier",11,"bold"),fg=global_fg,bg=global_bg).pack()
            else:
                Label(Win, text=lang["ach_500"],font = ("Courier",11,"bold"),fg=global_fg,bg=global_bg).pack()
            if i["status"] == "yes":
                Label(Win, text=lang["vipolneno"],fg=global_fg,bg=global_bg).pack()
            else:
                Label(Win, text=lang["nevipolneno"],fg=global_fg,bg=global_bg).pack()
            Label(Win, text=f"{svb_coins}/{i['max']}",bg = global_bg,fg=global_fg).pack()
            ttk.Progressbar(Win, length=200, maximum=i["max"], value=i["current"]).pack()
            Label(Win, text=f"{lang['prize']}: {i['prize']}",font = ("Courier",11,"bold"),fg="red",bg=  global_bg).pack()
        else:
            i["current"] = svb_coins
            if i['name'] == "million":
                Label(Win, text=lang["ach_million"],font = ("Courier",11,"bold"),fg=global_fg,bg=global_bg).pack()
            else:
                Label(Win, text=lang["ach_500"],font = ("Courier",11,"bold"),fg=global_fg,bg=global_bg).pack()
            Label(Win, text=lang["vipolneno"],bg = global_bg,fg=global_fg).pack()
            ttk.Progressbar(Win, length=200, maximum=100, value=100).pack()
            Label(Win, text=f"{lang['prize']}: {i['prize']}",font = ("Courier",11,"bold"),fg="red",bg=global_bg).pack()

