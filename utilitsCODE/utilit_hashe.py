from tkinter import *
from tkinter import ttk,filedialog
import hashlib
from create_window import create_window

hashe = ""

def open_window(root,lang,global_bg,global_fg,globalalpha):
    def open_filedialog():
        global hashe
        file = filedialog.askopenfile("rb")

        data = file.read()
        hash_object = hashlib.sha256(data)
        hashe = hash_object.hexdigest()
        lbl_hashe.config(text = f"{lang['hashe']}: {hashe}")
    def calc(text):
        global hashe
        hash_object = hashlib.sha256(text.encode())
        hashe = hash_object.hexdigest()

        lbl_hashe.config(text=f"{lang['hashe']}: {hashe}")

    def copy_text(text):
        root.clipboard_clear()
        root.clipboard_append(text)
    Win = create_window(root,lang["hashecalculator"],global_bg,globalalpha,600,500,"icons/Hashe Calculator.png")

    lbl_hashe = Label(Win,text = f"{lang['hashe']}: ", font = ("Arial",6),background=global_bg,foreground=global_fg)
    lbl_hashe.pack()

    Label(Win,text = lang['calc_str_hashe'],background=global_bg,foreground=global_fg).pack()
    entry = ttk.Entry(Win)
    entry.pack()

    btn = ttk.Button(Win, text=lang["calc_hashe"], command=lambda: calc(entry.get()))
    btn.pack()
    btn_hashe_file = ttk.Button(Win,text = lang["calc_file_hashe"],command = open_filedialog)
    btn_hashe_file.pack()
    btn_copy = ttk.Button(Win,text = lang["copy"],command = lambda:copy_text(hashe))
    btn_copy.pack()