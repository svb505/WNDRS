from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from create_change_log import win_changelogs
import os

def WinDow(root,lang,selected_lang,GlobalAlpha):
    Win = Toplevel(root)
    Win.title(lang["changelogs"])
    Win.geometry("300x400")
    Win.attributes("-alpha",float(GlobalAlpha))
    img = Image.open("icons/interface/changelogs.png")
    icon_image = ImageTk.PhotoImage(img)
    Win.iconphoto(False, icon_image)
    Win.resizable(False,False)

    left_frm = Frame(Win)
    left_frm.pack(side = LEFT)
    right_frm = Frame(Win)
    right_frm.pack(side=LEFT)


    names = []
    paths = []
    for fn in os.listdir("changelogs"):
        paths.append(fn)
        names.append(fn[10:-5])

    for i,(name,path) in enumerate(zip(names,paths)):
        frm = left_frm if i < 13 else right_frm
        btn = ttk.Button(frm,text = name,command = lambda p = path:win_changelogs(root,selected_lang,lang,p))
        btn.pack()
