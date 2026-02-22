from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import os

paths = []
current_idx = 0

def OpenWindow(root, lang, global_bg, global_fg,alpha):
    global current_idx, paths
    current_idx = 0
    paths = []

    def load_img(pth):
        img = Image.open(pth).resize((700, 500), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(img)

    def change_img(direction, lbl_idx, lbl_img):
        global current_idx
        if not paths:
            return

        if direction == "to":
            current_idx = (current_idx + 1) % len(paths)
        elif direction == "back":
            current_idx = (current_idx - 1) % len(paths)

        lbl_idx.config(text=f'{lang["photo_per"]} {current_idx + 1}/{len(paths)}')
        img = load_img(paths[current_idx])
        lbl_img.config(image=img)
        lbl_img.image = img

    Win = Toplevel(root)
    Win.title(lang["show_screenshoots"])
    Win.geometry("800x600")
    Win.configure(bg=global_bg)
    Win.attributes('-alpha',float(alpha))

    icon_image = ImageTk.PhotoImage(Image.open("icons/interface/screenshoot.png").resize((700, 500), Image.Resampling.LANCZOS))
    image_to = ImageTk.PhotoImage(Image.open("icons/interface/to_flash.png").resize((50, 50), Image.Resampling.LANCZOS))
    image_back = ImageTk.PhotoImage(Image.open("icons/interface/back_flash.png").resize((50, 50), Image.Resampling.LANCZOS))
    Win.iconphoto(False, icon_image)

    for root_dir, dirs, files in os.walk("screenshoots"):
        for file in files:
            if file.lower().endswith((".png", ".jpg", ".jpeg")):
                paths.append(os.path.join(root_dir, file))

    if not paths:
        Label(Win, text=lang["no_screenshots"], bg=global_bg, fg=global_fg, font=("Arial", 18, "bold")).pack(pady=50)
        return

    lbl_idx = Label(Win, text=f'{lang["photo_per"]} {current_idx + 1}/{len(paths)}', bg=global_bg, fg=global_fg)
    lbl_idx.pack()

    img = load_img(paths[current_idx])
    lbl_img = Label(Win, image=img, bg=global_bg)
    lbl_img.image = img
    lbl_img.pack(pady=10)

    frame_btns = Frame(Win, bg=global_bg)
    frame_btns.pack()

    btn_back = ttk.Button(frame_btns, image=image_back, command=lambda: change_img("back", lbl_idx, lbl_img))
    btn_back.image = image_back
    btn_back.grid(row=0, column=0, padx=10)

    btn_to = ttk.Button(frame_btns, image=image_to, command=lambda: change_img("to", lbl_idx, lbl_img))
    btn_to.image = image_to
    btn_to.grid(row=0, column=1, padx=10)
