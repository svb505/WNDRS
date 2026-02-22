from tkinter import *
from PIL import Image, ImageTk

def create_window(parent,title,bg,alpha,w,h,imgpath = None,fullscreen = False,resizable = [True,True]):
    Win = Toplevel(parent)
    Win.title(title)
    Win.configure(bg=bg)
    Win.geometry(f'{w}x{h}')
    Win.attributes("-topmost", True)
    Win.attributes('-alpha', alpha)

    if imgpath != None:
        image = Image.open(imgpath)
        icon_image = ImageTk.PhotoImage(image)
        Win.icon_img_ref = icon_image
        Win.iconphoto(False, Win.icon_img_ref)
    if fullscreen:
        Win.attributes('-fullscreen',True)

    Win.resizable(resizable[0],resizable[1])

    return Win