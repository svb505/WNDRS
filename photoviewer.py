from tkinter import *
from tkinter import ttk,messagebox,filedialog
from PIL import Image, ImageTk


def photo_viewer(root,lang,global_bg,start_time_,actives_programs,GlobalAlpha):
    def load_img():
        path = filedialog.askopenfilename(parent=Win,title=lang["select_photo"],
                                          filetypes=[(lang['photo_files'], "*.jpg *.png"),(lang['all_files'], "*.*")])
        if not path:
            messagebox.showwarning(lang["warning"],lang["selectphoto!"],parent=Win)
            return
        img = Image.open(path)
        w,h = img.size
        if w > h:
            img.resize((200, 150), Image.Resampling.LANCZOS)
        elif h > w:
            img.resize((150, 200), Image.Resampling.LANCZOS)
        else:
            img.resize((200, 200), Image.Resampling.LANCZOS)
        tk_img = ImageTk.PhotoImage(img)
        lbl.config(image = tk_img)
        lbl.image = tk_img
    actives_programs.append("SVB Photo")
    Win = Toplevel(root)
    Win.attributes("-alpha",float(GlobalAlpha))
    Win.title(lang['photov'])
    Win.geometry('600x600')
    Win.attributes('-topmost',True)
    img = Image.open("icons/svb_photo.png")
    icon_image = ImageTk.PhotoImage(img)
    Win.iconphoto(False, icon_image)
    frame = Frame(Win,bg = global_bg)
    frame.pack()
    lbl = Label(frame,bg = global_bg)
    lbl.pack()

    ttk.Button(Win,text = lang["load_img"],command = load_img).pack()