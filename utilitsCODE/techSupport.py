from PIL import Image as PilImage, ImageTk as PilImageTk
from tkinter import *
from tkinter import ttk,messagebox,filedialog
import sqlite3
from send_email import send_email
import time
import os
import customtkinter as ctk
from datetime import datetime
from logtofile import log_to_file
from create_window import create_window

paths = []
win2 = None
win3 = None
progress_window = None
progress_bar = None
pathes_programs = []
tooltip = None

def show_tooltip(event, txt,start_time_):
    global tooltip
    if tooltip:
        return

    x = event.widget.winfo_rootx() + 20
    y = event.widget.winfo_rooty() + event.widget.winfo_height() + 10

    tooltip = Toplevel()
    tooltip.wm_overrideredirect(True)
    tooltip.wm_geometry(f"+{x}+{y}")
    tooltip.configure(bg="#333333")

    label = Label(tooltip,
                  text=txt,
                  background="#fcfcfa",
                  foreground="#000000",
                  font=("Segoe UI", 10),
                  relief="solid",
                  borderwidth=1,
                  padx=8, pady=4)

    label.pack()
    try:
        tooltip.attributes("-alpha", 0.97)
        tooltip.attributes("-topmost", True)
    except Exception as e:
        log_to_file(str(e), level="error", start_time_=start_time_)
def hide_tooltip(event):
    global tooltip
    if tooltip:
        tooltip.destroy()
        tooltip = None
def save_history(t):
    timestamp = datetime.now().strftime("%d.%m.%Y")
    if os.path.exists("support_hst.txt"):
        with open("support_hst.txt",'a',encoding='utf-8') as f:
            f.write(f"[{timestamp}] - [{t}]\n")
    else:
        with open("support_hst.txt",'w',encoding='utf-8') as f:
            f.write(f"[{timestamp}] - [{t}]\n")
def techpodd(lang, root, errors, global_bg, global_fg, start_time_,GlobalAlpha):
    global paths
    def show_history():
        hstwin = create_window(root, "", global_bg, float(GlobalAlpha), 400, 400)
        if os.path.exists("support_hst.txt"):
            with open("support_hst.txt", "r") as f:
                data = f.read()
            txt = Text(hstwin)
            txt.pack(fill="both", expand=True)
            txt.insert(1.0, data)

            scrollbar = Scrollbar(hstwin, orient=VERTICAL, command=txt.yview)
            scrollbar.pack(side=RIGHT, fill=Y)
            txt.configure(yscrollcommand=scrollbar.set)
        else:
            Label(hstwin, text=lang['no_history'], font=("Arial", 25, "bold")).pack()
    def ttt():
        def close_progress():
            global progress_window
            if progress_window is not None and progress_window.winfo_exists():
                progress_window.destroy()
                progress_window = None
        def prog(val, idx=1):
            global progress_window, progress_bar

            if progress_window is None or not progress_window.winfo_exists():
                progress_window = Toplevel(win)
                progress_window.title(lang["vipo"])
                progress_window.geometry("320x60")
                progress_window.attributes('-topmost', True)

                progress_bar = ttk.Progressbar(progress_window, length=300, maximum=100)
                progress_bar.pack(pady=10, padx=10)
                progress_window.update()

            progress_bar.config(value=val)
            progress_window.update_idletasks()
        def get_text():
            text = en.get("1.0", "end-1c").strip()
            if not text:
                messagebox.showwarning(lang["warning"], lang["empty_msg"],parent=win2)
                return
            if not th.get():
                messagebox.showwarning(lang["warning"], lang["empty_th"],parent=win2)
                return
            if not messagebox.askyesno(lang["confirm"], lang["are_you_sure_send"],parent=win2):
                return

            prog(0)
            win2.update_idletasks()

            try:
                prog(25)
                win2.update_idletasks()
                time.sleep(0.5)

                conn = sqlite3.connect("configurations.db")
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        first_name TEXT,
                        last_name TEXT,
                        email TEXT
                    )
                """)
                conn.commit()
                cursor.execute("SELECT * FROM users")
                users = cursor.fetchall()

                n, ln, e = ("Unknown", "Unknown", "Unknown")
                if users:
                    n, ln, e = users[0][1], users[0][2], users[0][3]

                prog(50)
                win2.update_idletasks()
                time.sleep(0.5)

                email_body = f"""
                    <div style='font-style: italic; font-size: 20px'>
                        <p><strong>ОТ:</strong> {n} {ln} ({e})</p>
                        <p><b>ТЕМА: {th.get()}</p></b>
                        <p>ПРОБЛЕМА: {text}</p>
                    </div>
                """

                if paths:
                    send_email(
                        to="developpersvbstd22@gmail.com",
                        subject="ТЕХПОДДЕРЖКА ОС",
                        html=email_body,
                        attachments=paths
                    )
                else:
                    send_email(
                        to="developpersvbstd22@gmail.com",
                        subject="ТЕХПОДДЕРЖКА ОС",
                        html=email_body
                    )

                prog(90)
                win2.update_idletasks()
                time.sleep(0.3)

                messagebox.showinfo(lang["success"], lang["send_sms"],parent=win2)
                paths.clear()
                listbox.delete(0, END)
                en.delete("1.0", END)
                prog(100)
                win2.update_idletasks()
                time.sleep(0.3)


            except Exception as ex:
                messagebox.showerror(lang["error"], f"{errors[4]}\n\n{ex}",parent=win2)
            finally:
                prog(0)
                win2.update_idletasks()

            log_to_file("MSG send", start_time_)
            save_history(th.get())
            close_progress()
        def attach_file():
            global win2
            files = filedialog.askopenfilenames(parent = win2,title=lang["select_files_to_arh"])
            if files:
                for f in files:
                    paths.append(f)
                listbox.delete(0, END)
                for file in paths:
                    listbox.insert(END, os.path.basename(file))
        def clear_all():
            global pathsf
            if messagebox.askyesno(lang["confirm"],lang["conf_to_clear"],parent=win2):
                paths.clear()
                listbox.delete(0,END)
                en.delete("1.0", END)
                th.delete("1.0", END)
        global win2
        win2 = create_window(root, "", global_bg, float(GlobalAlpha), 500, 400)
        win2.state('zoomed')
        en = Text(win2, width=50, height=20,background='lightgray')
        en.pack(fill="both", expand=True)

        th = ctk.CTkEntry(win2,placeholder_text=lang['enter_theme'],width=150)
        th.pack()
        attach_btn = ttk.Button(win2, text=lang["attach_file"], command=attach_file)
        attach_btn.pack()
        listbox = Listbox(win2, height=4)
        listbox.pack(fill="both", expand=False, padx=10)
        btn = ttk.Button(win2, text=lang["send"], command=get_text)
        btn.pack()
        btn = ttk.Button(win2, text=lang["clear_all"], command=clear_all)
        btn.pack()
    def opros():
        def send(ots,ud,f,pon,pr):
            try:
                html_content = f"""
        <!DOCTYPE html>
        <html lang="ru">
        <head>
            <meta charset="UTF-8">
            <title>Новый отзыв о программе</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f9f9f9;
                    color: #333;
                    margin: 0;
                    padding: 0;
                }}
                .container {{
                    max-width: 600px;
                    margin: 30px auto;
                    background-color: #ffffff;
                    border-radius: 10px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                    padding: 20px;
                }}
                h2 {{
                    color: #2c3e50;
                    text-align: center;
                }}
                .section {{
                    margin-bottom: 15px;
                }}
                .label {{
                    font-weight: bold;
                    color: #555;
                }}
                .value {{
                    margin-top: 5px;
                    padding: 10px;
                    background-color: #f1f1f1;
                    border-radius: 5px;
                    word-wrap: break-word;
                }}
                .footer {{
                    text-align: center;
                    color: #999;
                    font-size: 12px;
                    margin-top: 20px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Новый отзыв о программе</h2>

                <div class="section">
                    <div class="label">Оценка программы:</div>
                    <div class="value">{ots}</div>
                </div>

                <div class="section">
                    <div class="label">Удобство использования:</div>
                    <div class="value">{ud}</div>
                </div>

                <div class="section">
                    <div class="label">Полезность функций:</div>
                    <div class="value">{f}</div>
                </div>

                <div class="section">
                    <div class="label">Что понравилось:</div>
                    <div class="value">{pon}</div>
                </div>

                <div class="section">
                    <div class="label">Предложения по улучшению:</div>
                    <div class="value">{pr}</div>
                </div>

                <div class="footer">
                    Это сообщение было автоматически сгенерировано из формы обратной связи.
                </div>
            </div>
        </body>
        </html>
        """
                send_email(
                    to="developpersvbstd22@gmail.com",
                    subject="ОТЗЫВ",
                    html=html_content
                )
                messagebox.showinfo(lang["success"],lang['mail_sentent_to_developper'],parent = w)
            except Exception as e:
                messagebox.showerror(lang["error"],str(e),parent = w)
        w = create_window(root, lang["opros"], global_bg, float(GlobalAlpha), 500, 400, "icons/tech_support.png")

        lbl = Label(w,text = lang["otsenka"],bg=global_bg,fg = global_fg)
        lbl.pack()
        ots = ttk.Combobox(w,values = [lang["ots1"],lang["ots2"],lang["ots3"],lang["ots4"],lang["ots5"]])
        ots.pack()
        ots.set(lang["ots1"])
        lbl = Label(w, text=lang["udobno"], bg=global_bg, fg=global_fg)
        lbl.pack()
        ud = ttk.Combobox(w, values=[lang["ud1"],lang["ud2"],lang["ud3"],lang["ud4"],lang["ud5"]])
        ud.pack()
        ud.set(lang["ud1"])
        lbl = Label(w, text=lang["funcs"], bg=global_bg, fg=global_fg)
        lbl.pack()
        f = ttk.Combobox(w, values=[lang["f1"],lang["f2"],lang["f3"],lang["f4"],lang["f5"]])
        f.pack()
        f.set(lang["f1"])
        lbl = Label(w, text=lang["ponr"], bg=global_bg, fg=global_fg)
        lbl.pack()
        pon = ctk.CTkEntry(w,placeholder_text=lang["vvod_suda"],width=100)
        pon.pack()
        lbl = Label(w, text=lang["predl"], bg=global_bg, fg=global_fg)
        lbl.pack()
        pr = ctk.CTkEntry(w, placeholder_text=lang["vvod_suda"], width=100)
        pr.pack()

        btn = ttk.Button(w,text = lang['send_to_developper'],command = lambda:send(ots.get(),ud.get(),f.get(),pon.get(),pr.get()))
        btn.pack()
    def send_my_prog():
        def close_progress():
            global progress_window
            if progress_window is not None and progress_window.winfo_exists():
                progress_window.destroy()
                progress_window = None
        def prog(val, idx=1):
            global progress_window, progress_bar

            if progress_window is None or not progress_window.winfo_exists():
                progress_window = Toplevel(win)
                progress_window.title(lang["vipo"])
                progress_window.geometry("320x60")
                progress_window.attributes('-topmost', True)

                progress_bar = ttk.Progressbar(progress_window, length=300, maximum=100)
                progress_bar.pack(pady=10, padx=10)
                progress_window.update()

            progress_bar.config(value=val)
            progress_window.update_idletasks()
        def attach_file():
            global win3,pathes_programs
            files = filedialog.askopenfilenames(parent=win3, title=lang["select_files_to_arh"])
            if files:
                for f in files:
                    pathes_programs.append(f)
                listbox.delete(0, END)
                for file in pathes_programs:
                    listbox.insert(END, os.path.basename(file))
        def get_text(name,email,others,sh_d,yesno,long_discr):
            global pathes_programs
            if not any([name,email,sh_d,yesno,long_discr]):
                messagebox.showwarning(lang["warning"], lang["empty_msg"],parent=win3)
                return
            if not pathes_programs:
                messagebox.showwarning(lang["warning"], lang["no_files"], parent=win3)
                return
            if not messagebox.askyesno(lang["confirm"], lang["are_you_sure_send"],parent=win3):
                return

            prog(0)
            win3.update_idletasks()

            try:
                prog(25)
                win3.update_idletasks()
                time.sleep(0.5)

                conn = sqlite3.connect("configurations.db")
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        first_name TEXT,
                        last_name TEXT,
                        email TEXT
                    )
                """)
                conn.commit()
                cursor.execute("SELECT * FROM users")
                users = cursor.fetchall()

                n, ln, e = ("Unknown", "Unknown", "Unknown")
                if users:
                    n, ln, e = users[0][1], users[0][2], users[0][3]

                prog(50)
                win3.update_idletasks()
                time.sleep(0.5)

                email_body = f"""
                    <!DOCTYPE html>
                <html lang="ru">
                <head>
                    <meta charset="UTF-8">
                    <title>Информация о юзере/программе</title>
                </head>
                <body style="font-family: Arial, sans-serif; background: #f4f4f9; padding: 20px;">
                    <div style="max-width: 600px; margin: auto; background: #fff; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); padding: 25px;">
                        <h2 style="text-align:center; color:#333; margin-bottom: 20px;">Информация о юзере/программе</h2>
                        <div style="border-bottom: 1px solid #ddd; padding: 10px 0;">
                            <strong>От:</strong> {n} {ln} (<a href="mailto:{e}" style="color:#0066cc; text-decoration:none;">{e}</a>)
                        </div>
                        <div style="border-bottom: 1px solid #ddd; padding: 10px 0;">
                            <strong>Никнейм:</strong> {name}
                        </div>
                        <div style="border-bottom: 1px solid #ddd; padding: 10px 0;">
                            <strong>Email:</strong> <a href="mailto:{email}" style="color:#0066cc; text-decoration:none;">{email}</a>
                        </div>
                        <div style="border-bottom: 1px solid #ddd; padding: 10px 0;">
                            <strong>Дополнительные контакты:</strong> {others}
                        </div>
                        <div style="border-bottom: 1px solid #ddd; padding: 10px 0;">
                            <strong>Короткое описание:</strong> {sh_d}
                        </div>
                        <div style="border-bottom: 1px solid #ddd; padding: 10px 0; color:green; font-weight:bold;">
                            {yesno}
                        </div>
                        <div style="padding: 10px 0;">
                            <strong>Полное описание:</strong><br>
                            <p style="margin-top:5px; line-height:1.5; color:#444;">{long_discr}</p>
                        </div>
                    </div>

                </body>
                </html>
                """

                send_email(
                        to="developpersvbstd22@gmail.com",
                        subject="ПРОГРАММА ДЛЯ ОС",
                        html=email_body,
                        attachments=pathes_programs
                )

                prog(90)
                win3.update_idletasks()
                time.sleep(0.3)

                messagebox.showinfo(lang["success"], lang["send_sms"],parent=win3)
                paths.clear()
                listbox.delete(0, END)
                prog(100)
                win3.update_idletasks()
                time.sleep(0.3)


            except Exception as ex:
                messagebox.showerror(lang["error"], f"{errors[4]}\n\n{ex}",parent=win3)
            finally:
                prog(0)
                win3.update_idletasks()

            log_to_file("MSG send", start_time_)
            close_progress()
        global win3
        win3 = create_window(root, "VPN", global_bg, float(GlobalAlpha), 500, 400)
        win3.state('zoomed')

        Label(win3,text = lang["*-obyaz"],fg = global_fg,bg = global_bg,font = ("Arial",15,'bold')).pack()
        name = ctk.CTkEntry(win3, placeholder_text=lang['enter_your_nickname'], width=250)
        name.pack()

        email = ctk.CTkEntry(win3, placeholder_text=lang['enter_email'], width=250)
        email.pack()

        Label(win3,text = lang["enter_others_contacts"],bg = global_bg,fg = global_fg).pack()
        others = Text(win3, width=50, height=10, background='lightgray')
        others.pack(fill="x", expand=True)

        sh_d = ctk.CTkEntry(win3, placeholder_text=lang['enter_short_discr'], width=250)
        sh_d.pack()

        Label(win3,text = lang["svbcoins?"],bg = global_bg,fg = global_fg)
        yesno = ctk.CTkEntry(win3, placeholder_text=lang["svbcoins?"], width=250)
        yesno.pack()

        Label(win3,text = lang["enter_discr"],bg = global_bg,fg = global_fg).pack()
        long_discr = Text(win3, width=50, height=20, background='lightgray')
        long_discr.pack(fill="x", expand=True)

        attach_btn = ttk.Button(win3, text=lang["attach_file"], command=attach_file)
        attach_btn.pack()
        listbox = Listbox(win3, height=4)
        listbox.pack(fill="both", expand=False, padx=10)
        btn = ttk.Button(win3, text=lang["send"], command=lambda:get_text(name.get(),email.get(),
                        others.get("1.0", "end-1c"),sh_d.get(),yesno.get(),
                        long_discr.get("1.0", "end-1c")))
        btn.pack()

    win = create_window(root, lang["pod"], global_bg, float(GlobalAlpha), 800, 600, "icons/tech_support.png")

    lbl = Label(win, text=lang["welcome_tech"] + "\n" + lang['enter_err'], font=('Arial', 15), fg=global_fg,
                bg=global_bg)
    lbl.pack()

    win.send_err = PilImageTk.PhotoImage(
        PilImage.open('icons/interface/write.png').resize((50, 50), PilImage.Resampling.LANCZOS)
    )
    win.opros = PilImageTk.PhotoImage(
        PilImage.open('icons/quiz.png').resize((50, 50), PilImage.Resampling.LANCZOS)
    )
    win.my_prog = PilImageTk.PhotoImage(
        PilImage.open('icons/program.png').resize((50, 50), PilImage.Resampling.LANCZOS)
    )
    win.hst = PilImageTk.PhotoImage(
        PilImage.open('icons/interface/hst.png').resize((50, 50), PilImage.Resampling.LANCZOS)
    )

    commands = [ttt,opros,send_my_prog,show_history]
    texts = [lang["send_err"],lang["proiti_opros"],lang["send_my_programm"],lang["show_support_hst"]]
    images = [win.send_err,win.opros,win.my_prog,win.hst]

    for text,img,comm in zip(texts,images,commands):
        btn = ttk.Button(win, image = img, command=comm)
        btn.image = img
        btn.pack(anchor = "n", padx=10)
        btn.bind("<Enter>", lambda event, t=text: show_tooltip(event, txt=t,start_time_ = start_time_))
        btn.bind("<Leave>", hide_tooltip)
