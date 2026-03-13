from tkinter import *
from crypto_work import read_encrypted_file

def control_ecran():
    Win = Tk()
    Win.geometry("800x400")
    Win.attributes("-fullscreen",True)
    Win.config(bg="black")

    date = read_encrypted_file("syst_comp/control_nxt_date.cfg")

    Label(Win,text = "Limit reached!",fg = "white",font = ("Arial",55,"bold"),bg = "black").pack()
    Label(Win,text = f"The limit will be exhausted {date}",fg = "white",font = ("Arial",35,"bold"),bg = "black").pack()

    Win.mainloop()
control_ecran()
