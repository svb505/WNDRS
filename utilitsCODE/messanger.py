from tkinter import *
from tkinter import ttk,messagebox
from logtofile import log_to_file
from PIL import Image, ImageTk
import os
import customtkinter as ctk
import random
import time
import threading
from play_sound import play_sound
from create_window import create_window

config = {}
os.makedirs("chat", exist_ok=True)
def open_mes(lang, root, actives_programs, volume, state_sound, errors, start_time_, global_bg, global_fg,GlobalAlpha):
    response_patterns = {
        lang['template1']: [lang['responce_ab1'], lang['responce_ab1-2'], lang['responce_ab1-3']],
        lang['template2']: [lang['responce_ab2'], lang['responce_ab2-2'], lang['responce_ab2-3']],
        lang['template3']: [lang['responce_ab3'], lang['responce_ab3-2'], lang['responce_ab3-3']],
        lang['template4']: [lang['responce_ab4'], lang['responce_ab4-2'], lang['responce_ab4-3']]
    }

    default_responses = [lang["responce_ab_default1"], lang["responce_ab_default2"],lang["responce_ab_default3"]]
    actives_programs.append("Telegrom")
    play_sound("sound//click.mp3", volume, state_sound, start_time_)

    def add_cont():
        def add(n, nam, ln):
            log_to_file('Contact added', start_time_=start_time_)
            with open("contacts.bin", "a") as f:
                f.write(f"NUMBER= {n}\nNAME= {nam}\nFAMILLY= {ln}\n")
                f.close()
            messagebox.showinfo(lang["success"], lang["contact_added"], parent=win1)
            log_to_file(f"Message: {lang['contact_added']}", start_time_=start_time_)

        log_to_file('Add contact', start_time_=start_time_)
        win1 = create_window(win, "Telegrom", global_bg, float(GlobalAlpha), 400, 300)
        lbl = Label(win1, text=lang["enter_number"], font=("Arial", 15), bg=global_bg, fg=global_fg)
        lbl.pack()
        en = ctk.CTkEntry(win1, placeholder_text=lang['enter_number'])
        en.pack()
        lbl1 = Label(win1, text=lang["enter_name"], font=("Arial", 15), bg=global_bg, fg=global_fg)
        lbl1.pack()
        en1 = ctk.CTkEntry(win1, placeholder_text=lang['enter_name'])
        en1.pack()
        lbl2 = Label(win1, text=lang["enter_lastname"], font=("Arial", 15), bg=global_bg, fg=global_fg)
        lbl2.pack()
        en2 = ctk.CTkEntry(win1, placeholder_text=lang['enter_lastname'])
        en2.pack()
        btn = ttk.Button(win1, text=lang["add"], command=lambda: add(en.get(), en1.get(), en2.get()))
        btn.pack()
    def load_chat_hst(contact):
        if os.path.exists(f'chat/chathst_{contact}.txt'):
            with open(f'chat/chathst_{contact}.txt',"r",encoding='utf-8') as f:
                file_data = f.read()
            return file_data
        else:
            return None
    def shw_chat(contact):
        def update_chat_hst(contact,data):
            if os.path.exists(f'chat/chathst_{contact}.txt'):
                with open(f'chat/chathst_{contact}.txt', "a",encoding='utf-8') as f:
                    f.write(data+"\n")
            else:
                with open(f'chat/chathst_{contact}.txt', "w",encoding='utf-8') as f:
                    f.write(data+"\n")
        def insert_to_text():
            if load_chat_hst(contact) != None:
                text.config(state = "normal")
                text.insert(END,load_chat_hst(contact)+'\n')
                text.config(state="disabled")

        def abonent_responce(msg):
            def respond():
                time.sleep(random.uniform(0.5, 1.5))  # имитация задержки ответа
                lower_msg = msg.lower()
                response = None
                for pattern, responses in response_patterns.items():
                    if pattern in lower_msg:
                        response = random.choice(responses)
                        break
                if response is None:
                    response = random.choice(default_responses)

                text.config(state="normal")
                text.insert("end", f"[{contact}] - {response}\n", "them")
                text.see("end")
                text.config(state="disabled")
                update_chat_hst(contact, f"[{contact}]" + response)

            # запустить в отдельном потоке, чтобы UI не зависал
            threading.Thread(target=respond).start()
        def send_msg(msg):
            update_chat_hst(contact,"[me]" + msg)
            text.config(state = "normal")
            text.insert(END,f"[me] - {msg}\n","me")
            text.config(state="disabled")
            abonent_responce(msg)
        Win = create_window(root, "Telegrom", global_bg, float(GlobalAlpha), 600, 500,"icons/telegrom.png")
        btn_img = Image.open("icons/interface/send.png").resize((25, 25), resample=Image.Resampling.LANCZOS)
        btn_image = ImageTk.PhotoImage(btn_img)

        text_frm = Frame(Win)
        text_frm.pack()
        ui_frame = Frame(Win)
        ui_frame.pack()

        text = Text(text_frm)
        text.pack()
        text.tag_configure("me", foreground="blue", font=("Arial", 11, "bold"))
        text.tag_configure("them", foreground="gray", font=("Arial", 11, "italic"))
        text.config(state = "disabled")

        entry = ctk.CTkEntry(ui_frame,placeholder_text=lang["enter_mess"],width=250)
        entry.pack(side = LEFT)
        send = ttk.Button(ui_frame,image=btn_image,command=lambda:send_msg(entry.get()))
        send.image = btn_image
        send.pack(side = RIGHT)
        insert_to_text()
    actives_programs.append("Telegrom")
    log_to_file('Telegrom launch', start_time_=start_time_)
    win = create_window(root, "Telegrom", global_bg, float(GlobalAlpha), 400, 300,"icons/telegrom.png")

    style = ttk.Style()
    style.configure("Accent.TButton", font=("Arial", 12, "bold"), padding=6, background="#1E90FF")
    frame = LabelFrame(win, text=lang["contact"], bg=global_bg)
    frame.pack()
    if os.path.exists("contacts.bin"):  # Проверяем, существует ли файл
        log_to_file('Contacts exist', start_time_=start_time_)
        with open("contacts.bin", "rb") as f:
            for line in f:
                key1, value = line.decode("utf-8").strip().split("=")
                config[key1] = value
        cont_name = config.get("NAME")
        with (open("contacts.bin", "r") as f):
            for c in f:
                if "NAME" in c:
                    lab = ttk.Button(frame, text=lang["contact"] + cont_name, command=lambda c = cont_name: shw_chat(c))
                    lab.pack()

    lbl = Label(frame, text=lang["add_contact"], font=("Arial", 15), bg=global_bg,
                    fg=global_fg)
    lbl.pack()
    ttk.Button(frame, text=lang["add"], style="Accent.TButton", command=add_cont).pack(pady=10)