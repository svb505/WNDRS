from tkinter import *
from PIL import ImageTk,Image


def create_toggle(parent, command, on_image_path, off_image_path,global_bg):
    frame = Frame(parent, bg=global_bg)
    toggle_data = {"is_on": False}

    on_image = ImageTk.PhotoImage(Image.open(on_image_path).resize((60, 60)))
    off_image = ImageTk.PhotoImage(Image.open(off_image_path).resize((60, 60)))

    toggle_data["on_image"] = on_image
    toggle_data["off_image"] = off_image

    label = Label(frame, image=off_image, bg=global_bg)
    label.pack()

    def toggle(event=None):
        toggle_data["is_on"] = not toggle_data["is_on"]
        if toggle_data["is_on"]:
            label.config(image=on_image)
            label.image = on_image
        else:
            label.config(image=off_image)
            label.image = off_image
        command()

    label.bind("<Button-1>", toggle)

    frame.toggle_data = toggle_data
    frame.label = label
    return frame