import json
from tkinter import *
from PIL import Image,ImageTk
from tkcalendar import Calendar
from fadeinout import fade_in

def date_c(root,lang,taskbar_fg,global_bg,taskbar,global_fg,calendar_win, date_label, taskbar_height,selected_lang):
    date_label.config(bg=taskbar_fg)
    calendar_win = Toplevel(root)
    calendar_win.title(lang['calendar'])
    calendar_win.config(bg=global_bg)
    calendar_win.attributes('-alpha', 0.0)
    fade_in(calendar_win, 0.0)
    screen_width = root.winfo_screenwidth()
    x = screen_width - 300 - 100
    offset = 50
    taskbar_screen_y = root.winfo_rooty() + taskbar.winfo_y()
    y = taskbar_screen_y - offset - 250
    calendar_win.overrideredirect(True)
    calendar_win.geometry(f"300x250+{x}+{y}")
    img = Image.open("icons/interface/kalen.png")
    icon_image = ImageTk.PhotoImage(img)
    calendar_win.iconphoto(False, icon_image)
    with open("syst_comp/locales.json", "r") as f:
        lcls = json.load(f)
    date_entry = Calendar(calendar_win, width=30, background=global_bg, foreground=global_fg,
                          bordercolor=global_fg,
                          headersbackground=global_bg, headersforeground=global_fg, selectbackground='blue',
                          selectforeground=global_bg, weekendbackground=global_bg, weekendforeground='red',
                          date_pattern='dd.mm.yyyy',
                          locale=lcls[selected_lang])
    date_entry.pack(pady=10)