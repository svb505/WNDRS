import os
from tkinter import *
from tkinter import ttk,messagebox,filedialog
from logtofile import log_to_file
import requests
from random import randint
import PIL.Image
import PIL.ImageTk
from crypto_work import decrypt_message,encrypt_message,load_key

os.makedirs("passmanager", exist_ok=True)

def is_service_exist(service, key):
    try:
        with open("passmanager/passwords.cfg", "rb") as f:
            data = f.read().split(b'gAAAAAB')
            data = [b'gAAAAAB' + d for d in data if d.strip()]
            for line in data:
                decrypted = decrypt_message(line, key)
                if decrypted.startswith(service + " ="):
                    return True
    except Exception:
        pass
    return False
def import_passwords(lang):
    key = load_key()
    path = filedialog.askopenfilename(filetypes=[("Encrypted files", "*.enc")])
    if path:
        with open(path, "rb") as f:
            data = f.read()
        with open("passmanager/passwords.cfg", "wb") as f:
            f.write(data)
        messagebox.showinfo("✅", lang['import_fin'])
def export_passwords(lang):
    key = load_key()
    with open("passmanager/passwords.cfg", "rb") as f:
        encrypted = f.read()
    with open("passmanager/backup.enc", "wb") as f:
        f.write(encrypted)
    messagebox.showinfo("✅", lang["export_finish"])
def delete_selected(tree, key,lang):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("⚠️", lang['select_service_for_delete'])
        return

    if not messagebox.askyesno(lang['confirm'], lang['do_you_want_delete_service']):
        return
    if selected_item:
        values = tree.item(selected_item, 'values')
        service_to_delete = values[0]

        # Загружаем, расшифровываем, фильтруем
        with open("passmanager/passwords.cfg", "rb") as f:
            lines = f.read().split(b'gAAAAAB')
            lines = [b'gAAAAAB' + l for l in lines if l.strip()]

        new_data = []
        for line in lines:
            try:
                decrypted = decrypt_message(line, key)
                if not decrypted.startswith(service_to_delete + " ="):
                    new_data.append(line)
            except:
                new_data.append(line)

        # Перезаписываем
        with open("passmanager/passwords.cfg", "wb") as f:
            for l in new_data:
                f.write(l)

        tree.delete(selected_item)
        messagebox.showinfo("✅", lang["service_deleted"])
def copy_password(tree,lang,root):
    selected_item = tree.selection()
    if selected_item:
        password = tree.item(selected_item, 'values')[1]
        root.clipboard_clear()
        root.clipboard_append(password)
        messagebox.showinfo("✅", lang["pass_copy"])

def manager(lang,actives_programs,root,errors,start_time_,global_bg,global_fg,GlobalAlpha):
    def create():
        def create1(service,password,user_key):
            if not service or not password:
                messagebox.showerror(lang["error"], lang["fields_required"],parent = w)
                return

            key = load_key()
            if is_service_exist(service, key):
                messagebox.showwarning(lang["error"], lang["service_already_exists"],parent = w)
                return

            if user_key != "111":
                if len(user_key) < 6:
                    messagebox.showerror(lang["error"],lang["len_less_6"],parent = w)
                else:
                    key = load_key()
                    data_to_encrypt = user_key
                    encrypted_data = encrypt_message(data_to_encrypt, key)
                    try:
                        with open('passmanager/user_key.cfg', "wb") as f:
                            f.write(encrypted_data)
                    except Exception as e:
                        messagebox.showerror(lang["error"], lang["save_key_false"] + str(e),parent = w)
                        return
                    data_to_encrypt = f"{service} = {password}\n"
                    encrypted_data = encrypt_message(data_to_encrypt, key)
                    try:
                        if os.path.exists("passmanager/passwords.cfg"):
                            with open('passmanager/passwords.cfg', "ab") as f:
                                f.write(encrypted_data)
                        else:
                            with open('passmanager/passwords.cfg', "wb") as f:
                                f.write(encrypted_data)
                        messagebox.showinfo(lang["success"], lang["save_p_true"],parent = w)
                    except Exception as e:
                        messagebox.showerror(lang["error"], lang["save_p_false"] + str(e),parent = w)
            else:
                key = load_key()
                data_to_encrypt = f"{service} = {password}\n"
                encrypted_data = encrypt_message(data_to_encrypt, key)
                try:
                    if os.path.exists("passmanager/passwords.cfg"):
                        with open('passmanager/passwords.cfg', "ab") as f:
                            f.write(encrypted_data)
                    else:
                        with open('passmanager/passwords.cfg', "wb") as f:
                            f.write(encrypted_data)
                    messagebox.showinfo(lang["success"], lang["save_p_true"],parent = w)
                except Exception as e:
                    messagebox.showerror(lang["error"], lang["save_p_false"] + str(e),parent = w)

        w = Toplevel(Win)
        w.attributes("-alpha",float(GlobalAlpha))
        w.config(bg=global_bg)
        w.geometry('400x300')
        w.title(lang["passmanager"])
        img = PIL.Image.open("icons/passmanager.png")
        icon_image = PIL.ImageTk.PhotoImage(img)
        Win.iconphoto(False, icon_image)

        Label(w,text = lang["enter_service"],bg = global_bg,fg = global_fg).pack()
        service = ttk.Entry(w)
        service.pack()
        Label(w, text=lang["enter_pass"],bg = global_bg,fg = global_fg).pack()
        passw = ttk.Entry(w)
        passw.pack()
        if not os.path.exists('passmanager/user_key.cfg'):
            Label(w,text = lang["enter_user_key"],bg = global_bg,fg = global_fg).pack()
            user_key = ttk.Entry(w)
            user_key.pack()
            ttk.Button(w, text=lang["save_pass"] + " 🔒",
                       command=lambda: create1(service.get(), passw.get(), user_key.get())).pack()
        else:
            ttk.Button(w, text=lang["save_pass"] + " 🔒",
                       command=lambda: create1(service.get(), passw.get(), "111")).pack()
    def show():
        def show_pass():
            config = {}
            win = Toplevel(Win)
            win.attributes("-alpha",float(GlobalAlpha))
            win.config(bg=global_bg)
            win.geometry('400x300')
            win.title(lang["passmanager"])
            img = PIL.Image.open("icons/passmanager.png")
            icon_image = PIL.ImageTk.PhotoImage(img)
            Win.iconphoto(False, icon_image)
            tree = ttk.Treeview(win, columns=("param", "value"), show='headings', height=7)
            tree.heading("param", text=lang['serv'])
            tree.heading("value", text=lang["pass"])
            tree.pack(fill='both', expand=True)
            ttk.Button(win, text=lang["delete_selected"], command=lambda: delete_selected(tree, key,lang)).pack(pady=5)
            ttk.Button(win, text="Скопировать пароль", command=lambda: copy_password(tree,lang,root)).pack(pady=5)
            key = load_key()

            entries = []
            with open("passmanager/passwords.cfg", "rb") as f:
                lines = f.read().split(b'gAAAAAB')  # Разделяем по сигнатуре начала Fernet-токена
                lines = [b'gAAAAAB' + l for l in lines if l.strip()]  # Восстанавливаем заголовки и фильтруем пустые

                for encrypted_line in lines:
                    try:
                        decrypted_line = decrypt_message(encrypted_line, key)
                        if "=" in decrypted_line:
                            k, v = decrypted_line.strip().split("=", 1)
                            entries.append((k.strip(), v.strip()))
                    except Exception as e:
                        log_to_file(f"Error to decode string: {e}",level='error',start_time_=start_time_)

            for key, value in entries:
                tree.insert("", "end", values=(key, value))
        def zabil():
            def zb(email):
                pas = randint(100000, 9999999)
                key = load_key()
                data_to_encrypt = str(pas)
                encrypted_data = encrypt_message(data_to_encrypt, key)
                with open('passmanager/user_key.cfg', "wb") as f:
                    f.write(encrypted_data)
                try:
                    r = requests.post("https://server-os.onrender.com/send_email", json={
                        "to": str(email),
                        "subject": "🔐 Your User Code",
                        "html": f"""
                <html>
                  <body style="font-family: Arial, sans-serif; background-color: #f5f5f5; padding: 20px;">
                    <div style="background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0px 2px 6px rgba(0,0,0,0.1); max-width: 500px; margin: auto;">
                      <h2 style="color: #333;">🚀 User Code</h2>
                      <div style="background-color: #f0f0f0; padding: 15px; border-radius: 5px; text-align: center; font-size: 24px; letter-spacing: 2px; font-weight: bold; color: #007BFF;">
                        {pas}
                      </div>
                      <p style="font-size: 14px; color: #888; margin-top: 20px;">
                        If you did not request this code, please ignore this email.
                      </p>
                    </div>
                  </body>
                </html>
                """

                    })
                except Exception as ex:
                    messagebox.showerror('Error', f"{errors[4]}\n\n{ex}",parent = ww)
            ww = Toplevel(w)
            ww.attributes("-alpha",float(GlobalAlpha))
            ww.attributes('-topmost', True)
            ww.config(bg=global_bg)
            ww.geometry("200x200")
            ttk.Label(ww, text=lang["enter_e"], font=("Arial", 12), background="#2C3E50",
                      foreground="white").pack()
            email1 = ttk.Entry(ww, font=("Arial", 12))
            email1.pack(pady=5)
            ttk.Button(ww,text = lang["zbros"] + " 🗑️",command = lambda:zb(email1.get())).pack()
        def confirm(us_key):
            key = load_key()
            with open("passmanager/user_key.cfg") as f:
                encrypted_data = f.read()
            k = decrypt_message(encrypted_data,key)
            if str(k) == str(us_key):
                w.destroy()
                show_pass()
            else:
                log_to_file("Invalid key","error",start_time_ = start_time_)
                messagebox.showerror(lang["error"],lang["invalid_key"],parent = w)
        w = Toplevel(Win)
        w.attributes("-alpha",float(GlobalAlpha))
        w.config(bg=global_bg)
        w.geometry('400x300')
        w.title(lang["passmanager"])
        img = PIL.Image.open("icons/passmanager.png")
        icon_image = PIL.ImageTk.PhotoImage(img)
        Win.iconphoto(False, icon_image)
        Label(w,text = lang["enter_user_key_"],bg = global_bg,fg = global_fg).pack()
        p = ttk.Entry(w)
        p.pack()
        ttk.Button(w,text = lang["confirm"],command = lambda:confirm(p.get())).pack()
        ttk.Button(w, text=lang["zabil"],command = zabil).pack()
    def change():
        def ch(last,new):
            key = load_key()
            with open("passmanager/user_key.cfg") as f:
                encrypted_data = f.read()
            k = decrypt_message(encrypted_data, key)
            if str(k) != str(last):
                messagebox.showerror(lang["error"],lang["inv_key"],parent = w)
                return
            else:
                data_to_encrypt = str(new)
                encrypted_data = encrypt_message(data_to_encrypt,key)
                try:
                    with open("passmanager/user_key.cfg", "wb") as f:
                        f.write(encrypted_data)
                    messagebox.showinfo(lang["success"],lang["usp"],parent = w)
                except Exception as e:
                    messagebox.showerror(lang["error"],lang["error_new_k"] + str(e),parent = w)


        w = Toplevel(Win)
        w.attributes("-alpha",float(GlobalAlpha))
        w.config(bg=global_bg)
        w.geometry('400x300')
        w.title(lang["passmanager"])
        img = PIL.Image.open("icons/passmanager.png")
        icon_image = PIL.ImageTk.PhotoImage(img)
        Win.iconphoto(False, icon_image)
        Label(w,text = lang["last-p"],bg = global_bg,fg = global_fg).pack()
        last = ttk.Entry(w)
        last.pack()
        Label(w,text = lang["new-p"],bg = global_bg,fg = global_fg).pack()
        new = ttk.Entry(w)
        new.pack()
        ttk.Button(w,text = lang["ch_key"],command = lambda:ch(last.get(),new.get())).pack()
    log_to_file("Password manager launch",start_time_ = start_time_)
    actives_programs.append("Password Manager")
    Win = Toplevel(root)
    Win.attributes("-alpha",float(GlobalAlpha))
    Win.config(bg=global_bg)
    Win.geometry('600x500')
    Win.title(lang["passmanager"])
    img = PIL.Image.open("icons/passmanager.png")
    icon_image = PIL.ImageTk.PhotoImage(img)
    Win.iconphoto(False, icon_image)

    img = PIL.Image.open('icons/interface/passm.png')
    img = img.resize((120, 120))
    icon = PIL.ImageTk.PhotoImage(img)
    lbl = Label(Win,image = icon)
    lbl.image = icon
    lbl.pack()
    Label(Win,text = lang["priv_manager"],font = ("Arial",17,"bold"),bg = global_bg,fg = global_fg).pack()
    ttk.Button(Win, text=lang["create-pass"] + " 💾",command = create).pack()
    if os.path.exists("passmanager/passwords.cfg"):
        ttk.Button(Win,text = lang["show_passwords"] + " 👁️",command = show).pack()
    else:
        Label(Win,text = lang["no_saved_pas"],font = ("Arial",18,"bold"),bg = global_bg,fg = global_fg).pack()
    ttk.Button(Win, text=lang["sb_pass"] + " 🔄", command=change).pack()
    ttk.Button(Win, text=lang["import-pass"] + " 📥", command=lambda:import_passwords(lang)).pack()
    ttk.Button(Win, text=lang["export-pass"] + " 📤", command=lambda:export_passwords(lang)).pack()



