from tkinter import *
from tkinter import messagebox

def show_error(message):
    er = Tk()
    er.title("Error")
    er.withdraw()
    messagebox.showerror("Error", message)
    er.quit()