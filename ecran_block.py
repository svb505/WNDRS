from PIL import Image as PILImage, ImageTk
from tkinter import *
from datetime import datetime
from tkinter import ttk
from excos import shutdown_animation

months_dict = {
    "ru": {
        1: "января", 2: "февраля", 3: "марта",
        4: "апреля", 5: "мая", 6: "июня",
        7: "июля", 8: "августа", 9: "сентября",
        10: "октября", 11: "ноября", 12: "декабря"
    },
    "ua": {
        1: "січня", 2: "лютого", 3: "березня",
        4: "квітня", 5: "травня", 6: "червня",
        7: "липня", 8: "серпня", 9: "вересня",
        10: "жовтня", 11: "листопада", 12: "грудня"
    },
    "en": {
        1: "January", 2: "February", 3: "March",
        4: "April", 5: "May", 6: "June",
        7: "July", 8: "August", 9: "September",
        10: "October", 11: "November", 12: "December"
    },
    "fr": {
        1: "janvier", 2: "février", 3: "mars",
        4: "avril", 5: "mai", 6: "juin",
        7: "juillet", 8: "août", 9: "septembre",
        10: "octobre", 11: "novembre", 12: "décembre"
    }
}

def format_date(dt: datetime, lang="ru") -> str:
    if lang.lower() not in ["ru","ua","en",'fr']: lang = "en"
    months = months_dict[lang.lower()]
    return f"{dt.day} {months[dt.month]} {dt.year}"
def ecran_b(root,lang,errors,state_sound,actives_programs,volume,recording_thread,is_recording,start_time_,email,lang_code):
    def update_time(time_label, date_label):
        now = datetime.now()
        time_label.config(text=now.strftime("%H:%M:%S"))
        date_label.config(text=format_date(now, lang_code))
        Win.after(1000, lambda: update_time(time_label, date_label))

    Win = Toplevel(root)
    Win.attributes("-fullscreen", True)

    image = PILImage.open(r"icons\wallpepers\wallpeper12.jpg")
    image = image.resize((Win.winfo_screenwidth(), Win.winfo_screenheight()))
    photo = ImageTk.PhotoImage(image)
    Win.photo = photo

    canvas_icon = Canvas(Win,width=Win.winfo_screenwidth(),height=Win.winfo_screenheight(),highlightthickness=0,bd=0)
    canvas_icon.pack(fill="both", expand=True)
    canvas_icon.create_image(0, 0, anchor="nw", image=photo)

    time_label = Label(Win, text="", font=("Arial", 55), bg="black", fg="white")
    time_label.pack(side=LEFT,anchor = E)

    date_label = Label(Win, text="", font=("Arial", 40), bg="black", fg="white")
    date_label.pack(side=LEFT)

    canvas_icon.create_window(Win.winfo_screenwidth() // 2 - 400, Win.winfo_screenheight() // 2 - 100, window=time_label)
    canvas_icon.create_window(Win.winfo_screenwidth() // 2 - 400, Win.winfo_screenheight() // 2, window=date_label)

    update_time(time_label, date_label)

    shutdown_img = ImageTk.PhotoImage(
        PILImage.open(f"icons/interface/shutdown.png").resize((50, 50), PILImage.Resampling.LANCZOS))
    reboot_img = ImageTk.PhotoImage(
        PILImage.open(f"icons/interface/reboot.png").resize((50, 50), PILImage.Resampling.LANCZOS))
    btn_shutdown = ttk.Button(Win, image=shutdown_img,
        command=lambda: shutdown_animation(root, "shutdown", volume, errors, lang,actives_programs,is_recording,
                                       recording_thread, start_time_, email,state_sound))
    btn_shutdown.image = shutdown_img
    btn_shutdown.pack(side=BOTTOM)

    btn_reboot = ttk.Button(Win, image=reboot_img,
        command=lambda: shutdown_animation(root, "reboot", volume, errors, lang, actives_programs,is_recording,
    recording_thread, start_time_, email,state_sound))

    btn_reboot.image = reboot_img
    btn_reboot.pack(side=BOTTOM)

    canvas_icon.create_window(Win.winfo_screenwidth() // 2 + 800 , Win.winfo_screenheight() // 2 + 500, window=btn_shutdown)
    canvas_icon.create_window(Win.winfo_screenwidth() // 2 + 860, Win.winfo_screenheight() // 2 + 500, window=btn_reboot)

    Win.mainloop()