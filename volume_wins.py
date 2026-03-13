from tkinter import *
from tkinter import ttk
from PIL import Image,ImageTk
from crypto_work import read_encrypted_file, write_encrypted_file

def volume_plus(event, n,root,global_bg,global_fg,GlobalAlpha,taskbar,sound_b):
    def close_win():
        Win.destroy()

    Win = Toplevel(root)
    Win.attributes("-alpha", float(GlobalAlpha))
    Win.title("")
    Win.configure(bg=global_bg)
    Win.attributes("-topmost", True)
    screen_width = root.winfo_screenwidth()
    x = screen_width - 400 - 700
    offset = 50
    taskbar_screen_y = root.winfo_rooty() + taskbar.winfo_y()
    y = taskbar_screen_y - offset
    Win.overrideredirect(True)
    Win.geometry(f"400x50+{x}+{y}")
    img = Image.open("icons/interface/sound.png")
    icon_image = ImageTk.PhotoImage(img)
    Win.iconphoto(False, icon_image)

    sound = ImageTk.PhotoImage(Image.open("icons//interface//sound.png").resize((32, 32), Image.Resampling.LANCZOS))
    sound_off = ImageTk.PhotoImage(
        Image.open("icons//interface//soundoff.png").resize((32, 32), Image.Resampling.LANCZOS))
    sound_low = ImageTk.PhotoImage(
        Image.open("icons//interface//soundlow.png").resize((32, 32), Image.Resampling.LANCZOS))

    try:
        content = read_encrypted_file("syst_comp/volume.cfg")
        v = float(content)
    except Exception:
        v = 50.0
    v += float(n)
    if int(v) == 0:
        sound_b.config(image=sound_off)
        sound_b.image = sound_off
    elif 0.01 < float(v) <= 49.0:
        sound_b.config(image=sound_low)
        sound_b.image = sound_low
    else:
        sound_b.config(image=sound)
        sound_b.image = sound

    write_encrypted_file("syst_comp/volume.cfg", str(v))
    gr = Label(Win, text=f'{v:.2f}', font=("Arial", 13), bg=global_bg, fg=global_fg)
    gr.pack()
    volume_slider = ttk.Scale(Win, from_=0, to=100, orient='horizontal')
    volume_slider.set(v)
    volume_slider.pack(side="top", padx=10)
    volume_slider.config(state="disabled")

    Win.after(3000, lambda: close_win())
def volume_min(event, n,root,GlobalAlpha,global_bg,global_fg, taskbar,sound_b):
    def close_win():
        Win.destroy()

    Win = Toplevel(root)
    Win.attributes("-alpha", float(GlobalAlpha))
    Win.title("")
    Win.configure(bg=global_bg)
    Win.attributes("-topmost", True)
    screen_width = root.winfo_screenwidth()
    x = screen_width - 400 - 700
    offset = 50
    taskbar_screen_y = root.winfo_rooty() + taskbar.winfo_y()
    y = taskbar_screen_y - offset
    Win.overrideredirect(True)
    Win.geometry(f"400x50+{x}+{y}")
    img = Image.open("icons/interface/sound.png")
    icon_image = ImageTk.PhotoImage(img)
    Win.iconphoto(False, icon_image)

    sound = ImageTk.PhotoImage(Image.open("icons//interface//sound.png").resize((32, 32), Image.Resampling.LANCZOS))
    sound_off = ImageTk.PhotoImage(
        Image.open("icons//interface//soundoff.png").resize((32, 32), Image.Resampling.LANCZOS))
    sound_low = ImageTk.PhotoImage(
        Image.open("icons//interface//soundlow.png").resize((32, 32), Image.Resampling.LANCZOS))

    try:
        content = read_encrypted_file("syst_comp/volume.cfg")
        v = float(content)
    except Exception:
        v = 50.0
    v -= float(n)
    if int(v) == 0:
        sound_b.config(image=sound_off)
        sound_b.image = sound_off
    elif 0.01 < float(v) <= 49.0:
        sound_b.config(image=sound_low)
        sound_b.image = sound_low
    else:
        sound_b.config(image=sound)
        sound_b.image = sound

    write_encrypted_file("syst_comp/volume.cfg", str(v))
    gr = Label(Win, text=f'{v:.2f}', font=("Arial", 13), bg=global_bg, fg=global_fg)
    gr.pack()
    volume_slider = ttk.Scale(Win, from_=0, to=100, orient='horizontal')
    volume_slider.set(v)
    volume_slider.pack(side="top", padx=10)
    volume_slider.config(state="disabled")

    Win.after(3000, lambda: close_win())
def mute(event,root,global_bg,global_fg,GlobalAlpha,taskbar,sound_b,mute_state,user_volume):
    def close_win():
        Win.destroy()

    Win = Toplevel(root)
    Win.attributes("-alpha", float(GlobalAlpha))
    Win.title("")
    Win.configure(bg=global_bg)
    Win.attributes("-topmost", True)
    screen_width = root.winfo_screenwidth()
    x = screen_width - 400 - 700
    offset = 50
    taskbar_screen_y = root.winfo_rooty() + taskbar.winfo_y()
    y = taskbar_screen_y - offset
    Win.overrideredirect(True)
    Win.geometry(f"400x50+{x}+{y}")
    img = Image.open("icons/interface/sound.png")
    icon_image = ImageTk.PhotoImage(img)
    Win.iconphoto(False, icon_image)

    sound = ImageTk.PhotoImage(Image.open("icons//interface//sound.png").resize((32, 32), Image.Resampling.LANCZOS))
    sound_off = ImageTk.PhotoImage(
        Image.open("icons//interface//soundoff.png").resize((32, 32), Image.Resampling.LANCZOS))
    sound_low = ImageTk.PhotoImage(
        Image.open("icons//interface//soundlow.png").resize((32, 32), Image.Resampling.LANCZOS))

    if mute_state == "False":
        mute_state = "True"
        write_encrypted_file("syst_comp/mute.cfg", "True")
        try:
            content = read_encrypted_file("syst_comp/volume.cfg")
            v = float(content)
        except Exception:
            v = 50.0
        user_volume = v
        write_encrypted_file("syst_comp/user_v.cfg", str(user_volume))
        v = 0.0
        write_encrypted_file("syst_comp/volume.cfg", str(v))
    else:
        mute_state = "False"
        write_encrypted_file("syst_comp/mute.cfg", "False")
        try:
            content = read_encrypted_file("syst_comp/user_v.cfg")
            v = float(content)
        except Exception:
            v = 50.0
    if int(v) == 0:
        sound_b.config(image=sound_off)
        sound_b.image = sound_off
    elif 0.01 < float(v) <= 49.0:
        sound_b.config(image=sound_low)
        sound_b.image = sound_low
    else:
        sound_b.config(image=sound)
        sound_b.image = sound

    write_encrypted_file("syst_comp/volume.cfg", str(v))
    gr = Label(Win, text=f'{v:.2f}', font=("Arial", 13), bg=global_bg, fg=global_fg)
    gr.pack()
    volume_slider = ttk.Scale(Win, from_=0, to=100, orient='horizontal')
    volume_slider.set(v)
    volume_slider.pack(side="top", padx=10)
    volume_slider.config(state="disabled")

    Win.after(3000, lambda: close_win())