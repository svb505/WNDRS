from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
import os

paths = []
current_idx = 0
cap = None
playing = True

def OpenWindowRec(root, lang, global_bg, global_fg, alpha):
    global current_idx, paths, cap, playing
    current_idx = 0
    paths = []

    def play_video(lbl_video):
        if not cap:
            return
        ret, frame = cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (600, 400))
            img = ImageTk.PhotoImage(Image.fromarray(frame))
            lbl_video.config(image=img)
            lbl_video.image = img
        else:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        if playing:
            lbl_video.after(30, play_video, lbl_video)

    def load_video(index, lbl_video):
        global cap
        if cap:
            cap.release()
        cap = cv2.VideoCapture(paths[index])
        lbl_idx.config(text=f'{lang["video_per"]} {index + 1}/{len(paths)}')
        play_video(lbl_video)

    def change_video(direction, lbl_video):
        global current_idx
        if not paths:
            return
        if direction == "to":
            current_idx = (current_idx + 1) % len(paths)
        elif direction == "back":
            current_idx = (current_idx - 1) % len(paths)
        load_video(current_idx, lbl_video)

    def toggle_play():
        global playing
        playing = not playing
        if playing:
            play_video(lbl_video)

    Win = Toplevel(root)
    Win.title(lang["show_screenrecords"])
    Win.geometry("800x600")
    Win.configure(bg=global_bg)
    Win.attributes('-alpha', float(alpha))

    icon_image = PhotoImage(file="icons/interface/rec.png")
    image_to = ImageTk.PhotoImage(Image.open("icons/interface/to_flash.png").resize((50, 50), Image.Resampling.LANCZOS))
    image_back = ImageTk.PhotoImage(Image.open("icons/interface/back_flash.png").resize((50, 50), Image.Resampling.LANCZOS))

    Win.iconphoto(False, icon_image)

    for root_dir, dirs, files in os.walk("screen_recording"):
        for file in files:
            if file.lower().endswith((".mp4", ".avi", ".mkv", ".mov")):
                paths.append(os.path.join(root_dir, file))

    if not paths:
        Label(Win, text=lang["no_screenrecords"], bg=global_bg, fg=global_fg, font=("Arial", 18, "bold")).pack(pady=50)
        return

    lbl_idx = Label(Win, text=f'{lang["video_per"]} {current_idx + 1}/{len(paths)}', bg=global_bg, fg=global_fg)
    lbl_idx.pack()

    lbl_video = Label(Win, bg=global_bg, width=600, height=400)
    lbl_video.pack(pady=20)

    frame_btns = Frame(Win, bg=global_bg)
    frame_btns.pack(pady=10)

    btn_back = ttk.Button(frame_btns, image=image_back, command=lambda: change_video("back", lbl_video))
    btn_back.image = image_back
    btn_back.grid(row=0, column=0, padx=10)

    btn_to = ttk.Button(frame_btns, image=image_to, command=lambda: change_video("to", lbl_video))
    btn_to.image = image_to
    btn_to.grid(row=0, column=1, padx=10)

    btn_playpause = ttk.Button(frame_btns, text="⏯", width=4, command=toggle_play)
    btn_playpause.grid(row=0, column=2, padx=10)

    load_video(current_idx, lbl_video)

    def on_close():
        global cap
        if cap:
            cap.release()
        Win.destroy()

    Win.protocol("WM_DELETE_WINDOW", on_close)
