from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from crypto_work import decrypt_message,load_key

def open_hst_window(root,lang,actives_programs,start_time_,global_bg,global_fg,GlobalAlpha):
    def listen(val,l):
        w = Toplevel(root)
        w.attributes("-alpha",float(GlobalAlpha))
        w.config(bg=global_bg)
        w.title(lang["historys"])
        w.geometry('850x500')
        img = Image.open("icons/SVB History's.png")
        icon_image = ImageTk.PhotoImage(img)
        w.iconphoto(False, icon_image)

        file_name = ""
        folder_name = l
        if val == lang["hst1"]:
            file_name = 'history1_'
        elif val == lang["hst2"]:
            file_name = 'history2_'
        elif val == lang["hst3"]:
            file_name = 'history3_'
        elif val == lang["hst4"]:
            file_name = 'history4_'
        elif val == lang["hst5"]:
            file_name = 'history5_'
        path = f"history's/{folder_name}/{file_name}{l.lower()}.txt"
        with open(path,'r',encoding='utf-8') as f:
            txt = f.read()

        frame = Frame(w)
        frame.pack(fill='both', expand=True)
        text = Text(frame, wrap='word')
        text.pack(side='left', fill='both', expand=True)
        scrollbar = ttk.Scrollbar(frame, command=text.yview)
        scrollbar.pack(side='right', fill='y')
        text.config(yscrollcommand=scrollbar.set)
        text.insert(1.0, txt)
        text.config(state="disabled")

    actives_programs.append("Hisrorys")
    Win = Toplevel(root)
    Win.attributes("-alpha",float(GlobalAlpha))
    Win.config(bg=global_bg)
    Win.title(lang["historys"])
    Win.geometry("500x400")
    img = Image.open("icons/SVB History's.png")
    icon_image = ImageTk.PhotoImage(img)
    Win.iconphoto(False, icon_image)
    key = load_key()
    with open("syst_comp/lang.cfg", "rb") as f:  # читаем как бинарный
        encrypted_data = f.read()
        selected_lang = decrypt_message(encrypted_data, key).strip()
    Label(Win,text = lang[""],bg = global_bg,fg = global_fg).pack()
    combo = ttk.Combobox(Win,values = [lang["hst1"],lang["hst2"],lang["hst3"],lang["hst4"],lang["hst5"]])
    combo.pack()
    combo.set(lang["hst1"])

    ttk.Button(Win,text = lang["listen"],command = lambda:listen(combo.get(),selected_lang)).pack()

