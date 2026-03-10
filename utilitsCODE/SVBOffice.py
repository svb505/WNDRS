from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk, ImageGrab
from create_window import create_window
import os
from utilits import SVBWord,SVBExcel,SVBPPTX

def SVBOffice(root, lang,  global_bg, global_fg,GlobalAlpha,start_time_):
    Win = create_window(root,"SVB Office",global_bg,GlobalAlpha, 600,500,"icons/svb office.png")

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    frm = Frame(Win)
    frm.pack(fill=X, side=TOP)

    Win.excel = ImageTk.PhotoImage(
        Image.open(os.path.join(BASE_DIR, 'icons/svbexcel.png')).resize((65, 65), Image.Resampling.LANCZOS)
    )
    Win.word = ImageTk.PhotoImage(
        Image.open(os.path.join(BASE_DIR, 'icons/svbword.png')).resize((65, 65), Image.Resampling.LANCZOS)
    )
    Win.pptx = ImageTk.PhotoImage(
        Image.open(os.path.join(BASE_DIR, 'icons/pptx.png')).resize((65, 65), Image.Resampling.LANCZOS)
    )

    images = [Win.excel, Win.word, Win.pptx]
    names = ["SVBExcel","SVBWord","SVB PowerPoint"]
    commands = [lambda:SVBExcel.svbexcel(root,lang,global_bg,GlobalAlpha),
                lambda: SVBWord.redactor(root,lang,start_time_,global_bg,global_fg,GlobalAlpha),
                lambda: SVBPPTX.svbpptx(root,lang,global_bg,GlobalAlpha)
        ]

    Label(frm, text="SVBOffice", font=("Arial", 15, "bold"), bg=global_bg, fg=global_fg).pack()

    for i, (name, image, com) in enumerate(zip(names, images, commands)):
        Label(frm, image=image, bg=global_bg, fg=global_fg).pack()
        ttk.Button(frm, text=name, command=com).pack()
