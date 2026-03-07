import logging
from tkinter import *
from PIL import Image, ImageTk
from logtofile import log_to_file
from play_sound import play_sound
import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView

SYSTEM_LEVEL = 25
logging.addLevelName(SYSTEM_LEVEL, "SYSTEM")

def open_browser(root,lang,state_sound,volume,start_time_,actives_programs,global_bg,global_fg,wifi_state,GlobalAlpha):
    play_sound("sound//click.mp3",volume,state_sound,start_time_)

    actives_programs.append("Browser")
    log_to_file("Browser launch",start_time_)

    if wifi_state:
        app = QApplication(sys.argv)

        window = QMainWindow()
        window.resize(1200, 800)
        window.setWindowTitle("SVB Browser")

        browser = QWebEngineView()

        browser.load(QUrl("https://google.com"))

        window.setCentralWidget(browser)
        window.show()

        app.exec_()

    else:
        win = Toplevel(root)
        win.attributes("-alpha", float(GlobalAlpha))
        win.title(lang["browser"])
        win.config(bg=global_bg)
        img = Image.open("icons/browser.png")
        icon_image = ImageTk.PhotoImage(img)
        win.iconphoto(False, icon_image)
        win.geometry("900x900")

        log_to_file('No internet connection',start_time_)
        win.config(bg="white")
        lbl = Label(win, text=lang["no_internet"] + "!", fg='red', font=("Courier", 31, "bold"))
        lbl.pack()

        image = Image.open(
            "icons//interface//nowificonn.png")
        image = image.resize((300, 300))
        photo = ImageTk.PhotoImage(image)

        label = Label(win, image=photo)
        label.image = photo
        label.pack()

        win.mainloop()
