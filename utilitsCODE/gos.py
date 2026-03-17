from tkinter import *
from tkinter import ttk,messagebox
from datetime import datetime,date
import os
from PIL import Image, ImageTk
import random
from random import randint
from country_list import countries_for_language
import sqlite3
import customtkinter as ctk
from logtofile import log_to_file
from copy_file_to_folder import copy_file_to_folder
from send_email_template import send
from transactions import transactions
from send_email import send_email
from save_and_load_balance import save_balance,load_balance

svb_coins = 0
tooltip = None
os.makedirs("state", exist_ok=True)
def return_user_info():
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

    if users:
        user = users[0]
        n, ln, e = user[1], user[2], user[3]
    else:
        n = ln = e = "Unknown"
    return n,ln,e
def check_ach(lang,start_time_):
    global svb_coins
    svb_coins = load_balance(start_time_)

    conn = sqlite3.connect("achievements.db")
    cursor = conn.cursor()

    cursor.execute("SELECT name, status, max, prize FROM achievements")
    rows = cursor.fetchall()

    for name, status, max_val, prize in rows:
        if status == "no" and svb_coins >= max_val:
            svb_coins += int(prize)
            send('receipt', int(prize))
            save_balance(svb_coins,start_time_)

            cursor.execute(
                "UPDATE achievements SET current = ?, status = ? WHERE name = ?",
                (svb_coins, "yes", name)
            )
            conn.commit()

    conn.close()
os.makedirs("state", exist_ok=True)

def state_cache(data,edition,start_time_):

    if os.path.exists("state/logs.cache"):
        try:
            with open("state/logs.cache", "a") as file:
                file.write(f"{data}\n")
                file.close()
            if edition in ("Professional x64", "Gaming x64","Professional x32", "Gaming x32"):
                copy_file_to_folder("state/logs.cache", "backup_data",start_time_)
        except:
            pass
    else:
        try:
            with open("state/logs.cache", "w") as file:
                file.write(f"{data}\n")
                file.close()
            if edition in ("Professional x64", "Gaming x64","Professional x32", "Gaming x32"):
                copy_file_to_folder("state/logs.cache", "backup_data",start_time_)
        except:
            pass
def gosuslugi(root,lang,actives_programs,errors,edition,start_time_,global_bg,global_fg,GlobalAlpha):
    actives_programs.append("State Services")
    n,ln,e = return_user_info()
    def open_flp():
        def add_to_db(name,dateb,g,inn,regnum,adr,tel,email,vidd,syst,bank):
            conn = sqlite3.connect("state/SE.db")
            cursor = conn.cursor()
            cursor.execute("""CREATE table IF NOT EXISTS SE(
                            name TEXT,
                            date_of_b TEXT,
                            g TEXT,
                            inn TEXT,
                            regnum TEXT,
                            address TEXT,
                            tel TEXT,
                            email TEXT,
                            vidd TEXT,
                            systtax TEXT,
                            bankn TEXT)""")
            conn.commit()
            cursor.execute("INSERT INTO SE(name,date_of_b,g,inn,regnum,address,tel,email,vidd,systtax,bankn) VALUES(?,?,?,?,?,?,?,?,?,?,?)",
                           (name,dateb,g,inn,regnum,adr,tel,email,vidd,syst,bank))
            conn.commit()
            conn.close()
        def ok(name,dateb,g,inn,regnum,adr,tel,email,vidd,syst,bank):
            try:
                add_to_db(name, dateb, g, inn, regnum, adr, tel, email, vidd, syst, bank)
                today = datetime.now()
                date = today.strftime("%d.%m.%y")
                send_email(to=e, subject=lang["IPO_OPENED"], html=
                f"""
                            <html>
                            <head>
                              <meta charset="utf-8" />
                              <meta name="viewport" content="width=device-width,initial-scale=1" />
                              <title>{lang["ipo_registered"]}</title>
                              <style>
                                body{{font-family: Inter, Arial, sans-serif;background:#f4f6f9;margin:0;display:flex;align-items:center;justify-content:center;height:100vh;padding:20px}}
                                .sms{{width:100%;max-width:420px;background:#fff;border-radius:14px;box-shadow:0 8px 30px rgba(15,23,42,0.08);padding:20px}}
                                .from{{font-size:13px;color:#6b7280;margin-bottom:8px}}
                                .title{{font-size:18px;font-weight:700;margin-bottom:6px}}
                                .text{{font-size:15px;color:#111827;line-height:1.45;margin-bottom:12px}}
                                .meta{{font-size:13px;color:#6b7280;background:#f8fafc;padding:10px;border-radius:8px}}
                                .ok{{display:inline-block;margin-top:14px;padding:8px 12px;border-radius:999px;background:#ecfeff;color:#065f46;font-weight:600;font-size:13px}}
                              </style>
                            </head>
                            <body>
                              <div class="sms" role="article" aria-label={lang["ipo_message"]}>
                                <div class="from">{lang['SMS']}</div>
                                <div class="title">{lang['ipo_registered_successfully']}</div>
                                <div class="text">
                                  {lang["registered"]}<br>
                                  {lang['INN']}: <strong>{inn}</strong><br>
                                  {lang['reg_num']}: <strong>{regnum}</strong>
                                </div>
                                <div class="meta">
                                  {lang['date_']}: {date} • {lang["doc_avaible_in_PA"]}.
                                </div>
                                <div class="ok">{lang["all_success"]}</div>
                              </div>
                            </body>
                            </html> """
                           )
                messagebox.showinfo(lang["success"],lang["flp_created_sucessfully"])
            except Exception as err:
                messagebox.showerror(lang["error"],str(err))

        if not os.path.exists("state/SE.db"):
            Win = Toplevel(WIN)
            Win.title(lang["IPO_OPENED"])
            Win.geometry("500x650")
            img = Image.open("icons/interface/ipo.png")
            icon_image = ImageTk.PhotoImage(img)
            Win.iconphoto(False, icon_image)

            Label(Win, text=lang["enter_name_fname"], bg=global_bg, fg=global_fg).pack()
            name = ttk.Entry(Win)
            name.pack()
            Label(Win, text=lang["dateofb"], bg=global_bg, fg=global_fg).pack()
            dateb = ttk.Entry(Win)
            dateb.pack()
            Label(Win, text=lang["grazh"], bg=global_bg, fg=global_fg).pack()
            g = ttk.Entry(Win)
            g.pack()
            Label(Win, text=lang["enter_INN"], bg=global_bg, fg=global_fg).pack()
            inn = ttk.Entry(Win)
            inn.pack()
            Label(Win, text=lang["enter_num_passport"], bg=global_bg, fg=global_fg).pack()
            num = ttk.Entry(Win)
            num.pack()
            Label(Win, text=lang["adr__"], bg=global_bg, fg=global_fg).pack()
            adr = ttk.Entry(Win)
            adr.pack()
            Label(Win, text=lang["enter_tel_num"], bg=global_bg, fg=global_fg).pack()
            tel = ttk.Entry(Win)
            tel.pack()
            Label(Win, text=lang["enter_u_email"], bg=global_bg, fg=global_fg).pack()
            email = ttk.Entry(Win)
            email.pack()
            Label(Win, text=lang["vid_d"], bg=global_bg, fg=global_fg).pack()
            vidd = ttk.Entry(Win)
            vidd.pack()
            Label(Win, text=lang["tax_syst"], bg=global_bg, fg=global_fg).pack()
            syst = ttk.Combobox(Win, values=[lang['obsh'], lang["upr"]])
            syst.pack()
            syst.set(lang['obsh'])
            Label(Win, text=lang["bank_sc"], bg=global_bg, fg=global_fg).pack()
            bank = ttk.Entry(Win)
            bank.pack()


            ttk.Button(Win, text="Ok",
                       command=lambda: ok(name.get(), dateb.get(), g.get(), inn.get(), num.get(), adr.get(),
                                          tel.get(), email.get(), vidd.get(), syst.get(), bank.get())).pack()
        else:
            if messagebox.askyesno(lang["warning"],lang["flp_created"],parent = WIN):
                os.remove("state/SE.db")
    def open_business():
        def add_to_db(title,form,ur,post,name,kapital,vid,dopvid,director,tel,email,ID,syst):
            conn = sqlite3.connect("state/business.db")
            cursor = conn.cursor()
            cursor.execute("""CREATE table IF NOT EXISTS business(
                            title TEXT,
                            form TEXT,
                            uradr TEXT,
                            postadr TEXT,
                            name TEXT,
                            kapital INTEGER, 
                            vid TEXT,
                            dopvid TEXT, 
                            director TEXT,
                            tel TEXT, 
                            email TEXT, 
                            ID TEXT,
                            syst TEXT)""")
            conn.commit()
            cursor.execute("""INSERT INTO business(title,form,uradr,postadr,name,kapital,vid,dopvid,
                            director,tel,email,ID,syst) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                           (title,form,ur,post,name,kapital,vid,dopvid,director,tel,email,ID,syst))
            conn.commit()
            conn.close()
        def ok(title,form,ur,post,name,kapital,vid,dopvid,director,tel,email,ID,syst):
            try:
                add_to_db(title,form,ur,post,name,kapital,vid,dopvid,director,tel,email,ID,syst)
                today = datetime.now()
                date = today.strftime("%d.%m.%y")
                send_email(to=e, subject=lang["BOPENED"], html=
            f"""
           <html>
           <head>
             <meta charset="utf-8" />
             <meta name="viewport" content="width=device-width,initial-scale=1" />
             <title>{lang["business_opened"]}</title>
             <style>
               body{{font-family: Inter, Arial, sans-serif;background:#fff7ed;margin:0;display:flex;align-items:center;justify-content:center;height:100vh;padding:20px}}
               .sms{{width:100%;max-width:420px;background:#fff;border-radius:12px;box-shadow:0 6px 24px rgba(16,24,40,0.06);padding:20px}}
               .from{{font-size:13px;color:#92400e;margin-bottom:8px}}
               .title{{font-size:18px;font-weight:700;margin-bottom:6px;color:#7c2d12}}
               .text{{font-size:15px;color:#111827;line-height:1.45;margin-bottom:12px}}
               .meta{{font-size:13px;color:#6b7280;background:#fff3e0;padding:10px;border-radius:8px}}
               .ok{{display:inline-block;margin-top:14px;padding:8px 12px;border-radius:8px;background:#fff4e6;color:#92400e;font-weight:600;font-size:13px}}
             </style>
           </head>
           <body>
             <div class="sms" role="article" aria-label={lang['message_about_business']}>
               <div class="from">{lang["BSMS1"]}</div>
               <div class="title">{lang["BSMS2"]}</div>
               <div class="text">
                 {lang["BSMS3"]}<br>
                 {lang['title']}: <strong>{title}</strong><br>
                 {lang["regID"]}: <strong>{ID}</strong>
               </div>
               <div class="meta">
                 {lang['open_date']}: {date} • {lang['manager_contact']}: ---
               </div>
               <div class="ok">{lang['doc_send_in_email']}</div>
             </div>
           </body>
           </html>"""
                      )
                messagebox.showinfo(lang["success"],lang['business_created_succesfully'])
            except Exception as err:
                messagebox.showerror(lang["error"],str(err))

        if os.path.exists("state/SE.db"):
            Win = Toplevel(WIN)
            Win.title(lang["BOPENED"])
            Win.geometry("500x800")
            img = Image.open("icons/interface/business.png")
            icon_image = ImageTk.PhotoImage(img)
            Win.iconphoto(False, icon_image)
            Label(Win,text = lang["c_title"],bg = global_bg,fg = global_fg).pack()
            name = ttk.Entry(Win)
            name.pack()
            Label(Win, text=lang["form"], bg=global_bg, fg=global_fg).pack()
            form = ttk.Combobox(Win,values = [lang["OOO"],lang["TOP"],lang["SAS"],lang["IP"],
                                              lang["AO"],])
            form.pack()
            form.set(lang["OOO"])
            Label(Win, text=lang["uraddress"], bg=global_bg, fg=global_fg).pack()
            ur = ttk.Entry(Win)
            ur.pack()
            Label(Win, text=lang["poastaddress"], bg=global_bg, fg=global_fg).pack()
            post = ttk.Entry(Win)
            post.pack()
            Label(Win, text=lang["owner_name"], bg=global_bg, fg=global_fg).pack()
            ownername = ttk.Entry(Win)
            ownername.pack()
            Label(Win, text=lang["kapital"], bg=global_bg, fg=global_fg).pack()
            kapital = ttk.Spinbox(Win,from_ = 10000,to = 1000000000000)
            kapital.pack()
            kapital.set(100000)
            Label(Win, text=lang["vid_d"], bg=global_bg, fg=global_fg).pack()
            vidd = ttk.Entry(Win)
            vidd.pack()
            Label(Win, text=lang["dop_vidd"], bg=global_bg, fg=global_fg).pack()
            dopvidd = ttk.Entry(Win)
            dopvidd.pack()
            Label(Win, text=lang["director"], bg=global_bg, fg=global_fg).pack()
            director = ttk.Entry(Win)
            director.pack()
            Label(Win, text=lang["enter_tel_num"], bg=global_bg, fg=global_fg).pack()
            tel = ttk.Entry(Win)
            tel.pack()
            Label(Win, text=lang["enter_u_email"], bg=global_bg, fg=global_fg).pack()
            email = ttk.Entry(Win)
            email.pack()
            Label(Win, text=lang["bank_recv"], bg=global_bg, fg=global_fg).pack()
            bank = ttk.Entry(Win)
            bank.pack()
            Label(Win, text=lang["tax_syst"], bg=global_bg, fg=global_fg).pack()
            syst = ttk.Combobox(Win, values=[lang['obsh'], lang["upr"]])
            syst.pack()
            syst.set(lang['obsh'])
            ttk.Button(Win,text = "Ok",command = lambda:ok(name.get(),form.get(),ur.get(),post.get(),ownername.get(),
                                                           kapital.get(),vidd.get(),dopvidd.get(),
                                                           director.get(),tel.get(),email.get(),bank.get(),syst.get())).pack()
        else:
            messagebox.showwarning(lang["warning"],lang["flp_not_exists"],parent = WIN)
    def register_in_edu(type):
        def detsad():
            def add_to_db(name,dateb,sex,adr,tel,email,m_name,p_name,work,nmed,alerg,kid_group):
                conn = sqlite3.connect("state/detsad.db")
                cursor = conn.cursor()
                cursor.execute("""CREATE table IF NOT EXISTS detsad(
                        name TEXT, 
                        dateb TEXT,
                        sex TEXT,
                        adr TEXT,
                        tel TEXT,
                        email TEXT,
                        m_name TEXT,
                        p_name TEXT,
                        work TEXT,
                        nmed TEXT,
                        alerg TEXT,
                        kid_group TEXT)""")
                conn.commit()
                cursor.execute("""INSERT INTO detsad(name,dateb,sex,adr,tel,email,m_name,p_name,work,nmed,alerg,kid_group) 
                VALUES(?,?,?,?,?,?,?,?,?,?,?,?)""",
                               (name,dateb,sex,adr,tel,email,m_name,p_name,work,nmed,alerg,kid_group))
                conn.commit()
                conn.close()
            def ok(name,dateb,sex,adr,tel,email,m_name,p_name,work,nmed,alerg,kid_group):
                try:
                    today = datetime.now()
                    date = today.strftime("%d.%m.%y")
                    add_to_db(name,dateb,sex,adr,tel,email,m_name,p_name,work,nmed,alerg,kid_group)
                    prof = lang["prof1"]
                    num = "".join(random.choices('0123456789ABCDEFGHIJKLMNOPQRSTUVWYZ', k=12))
                    send_email(to=e, subject=lang["DETSAD"], html=
               f"""
               <html>
               <head>
                 <meta charset="utf-8" />
                 <meta name="viewport" content="width=device-width,initial-scale=1" />
                 <title>{lang["detsad_message"]}</title>
                 <style>
                   body{{font-family: Inter, Arial, sans-serif;background:#fef3f8;margin:0;display:flex;align-items:center;justify-content:center;height:100vh;padding:20px}}
                   .sms{{width:100%;max-width:420px;background:#fff;border-radius:12px;box-shadow:0 6px 22px rgba(236,72,153,0.06);padding:20px}}
                   .from{{font-size:13px;color:#db2777;margin-bottom:8px}}
                   .title{{font-size:18px;font-weight:700;margin-bottom:6px;color:#be185d}}
                   .text{{font-size:15px;color:#111827;line-height:1.45;margin-bottom:12px}}
                   .meta{{font-size:13px;color:#6b7280;background:#fff0f6;padding:10px;border-radius:8px}}
                   .ok{{display:inline-block;margin-top:14px;padding:8px 12px;border-radius:8px;background:#fff0f6;color:#be185d;font-weight:600;font-size:13px}}
                 </style>
               </head>
               <body>
                 <div class="sms" role="article" aria-label={lang["DSMS1"]}>
                   <div class="from">{lang["DSMS2"]}</div>
                   <div class="title">{lang["DSMS3"]}</div>
                   <div class="text">
                     {lang["kid"]}: <strong>{name}</strong><br>
                     {lang["group"]}: <strong>{kid_group}</strong><br>
                     {lang["NumBid"]}: <strong>{num}</strong>
                   </div>
                   <div class="meta">
                     {lang["date_"]}: {date} • {lang['prof_d']}: {prof}
                   </div>
                   <div class="ok">{lang["pls_takeit_docs"]}</div>
                 </div>
               </body>
               </html>"""
                          )
                    messagebox.showinfo(lang["success"],lang["detsadTRUE"])
                except Exception as err:
                    messagebox.showerror(lang["error"], str(err))
            Win = Toplevel(WIN)
            Win.title(lang["DETSAD"])
            Win.geometry("500x820")
            img = Image.open("icons/interface/detsad.png")
            icon_image = ImageTk.PhotoImage(img)
            Win.iconphoto(False, icon_image)

            Label(Win, text=lang["name_of_kid"], bg=global_bg, fg=global_fg).pack()
            name = ttk.Entry(Win)
            name.pack()
            Label(Win, text=lang["dateb_of_kid"], bg=global_bg, fg=global_fg).pack()
            dateb = ttk.Entry(Win)
            dateb.pack()
            Label(Win, text=lang["sex_of_kid"], bg=global_bg, fg=global_fg).pack()
            sex = ttk.Combobox(Win,values = [lang["M"],lang["ZH"]])
            sex.pack()
            sex.set(lang["M"])
            Label(Win, text=lang["prozh_of_kid"], bg=global_bg, fg=global_fg).pack()
            adr = ttk.Entry(Win)
            adr.pack()
            Label(Win, text=lang["tel_of_parents"], bg=global_bg, fg=global_fg).pack()
            tel = ttk.Entry(Win)
            tel.pack()
            Label(Win, text=lang["enter_parent_email"], bg=global_bg, fg=global_fg).pack()
            email = ttk.Entry(Win)
            email.pack()
            Label(Win, text=lang["enter_name_of_mom"], bg=global_bg, fg=global_fg).pack()
            m_name = ttk.Entry(Win)
            m_name.pack()
            Label(Win, text=lang["enter_name_of_dad"], bg=global_bg, fg=global_fg).pack()
            p_name = ttk.Entry(Win)
            p_name.pack()
            Label(Win, text=lang["work_of_parent"], bg=global_bg, fg=global_fg).pack()
            work = Text(Win,height = 9)
            work.pack()
            Label(Win, text=lang["n_med_sp"], bg=global_bg, fg=global_fg).pack()
            nmed = ttk.Entry(Win)
            nmed.pack()
            Label(Win, text=lang["alerg"], bg=global_bg, fg=global_fg).pack()
            alerg = ttk.Entry(Win)
            alerg.pack()
            Label(Win, text=lang["select_group"], bg=global_bg, fg=global_fg).pack()
            kid_group = ttk.Combobox(Win,values = [lang["ml"],lang["sr"],lang['starsh']])
            kid_group.pack()
            kid_group.set(lang["ml"])

            ttk.Button(Win, text='Ok', command=lambda: ok(name.get(),dateb.get(),sex.get(),adr.get(),tel.get(),email.get(),m_name.get(),
                                                          p_name.get(),work.get(1.0,END),nmed.get(),alerg.get(),kid_group.get())).pack()
        def school():
            def add_to_db(name,class_,dateb,schooln,adr,mname,pname,nmed,tel,email):
                conn = sqlite3.connect("state/school.db")
                cursor = conn.cursor()
                cursor.execute("""CREATE table IF NOT EXISTS school(
                        name TEXT,
                        class_ TEXT,
                        dateb TEXT,
                        schooln TEXT,
                        adr TEXT ,
                        mname TEXT,
                        pname TEXT,
                        nmed TEXT,
                        tel TEXT,
                        email
                )""")
                conn.commit()
                cursor.execute("""INSERT INTO school(name,class_,dateb,schooln,adr,mname,pname,nmed,tel,email)
                                VALUES(?,?,?,?,?,?,?,?,?,?)""",(name,class_,dateb,schooln,adr,mname,pname,nmed,tel,email))
                conn.commit()
                conn.close()
            def ok(name,class_,dateb,schooln,adr,mname,pname,nmed,tel,email):
                try:
                    add_to_db(name,class_,dateb,schooln,adr,mname,pname,nmed,tel,email)
                    today = datetime.now()
                    date = today.strftime("%d.%m.%y")
                    nextY = today.year + 1
                    num = "".join(random.choices('0123456789ABCDEFGHIJKLMNOPQRSTUVWYZ', k=12))

                    send_email(to=e, subject=lang["SCHOOL"], html=
                f"""
                <html>
                <head>
                  <meta charset="utf-8" />
                  <meta name="viewport" content="width=device-width,initial-scale=1" />
                  <title>{lang['SSMS1']}</title>
                  <style>
                    body{{font-family: Inter, Arial, sans-serif;background:#eef2ff;margin:0;display:flex;align-items:center;justify-content:center;height:100vh;padding:20px}}
                    .sms{{width:100%;max-width:420px;background:#fff;border-radius:12px;box-shadow:0 6px 20px rgba(59,130,246,0.08);padding:20px}}
                    .from{{font-size:13px;color:#2563eb;margin-bottom:8px}}
                    .title{{font-size:18px;font-weight:700;margin-bottom:6px;color:#1e3a8a}}
                    .text{{font-size:15px;color:#111827;line-height:1.45;margin-bottom:12px}}
                    .meta{{font-size:13px;color:#6b7280;background:#f0f7ff;padding:10px;border-radius:8px}}
                    .ok{{display:inline-block;margin-top:14px;padding:8px 12px;border-radius:8px;background:#eff6ff;color:#1e3a8a;font-weight:600;font-size:13px}}
                  </style>
                </head>
                <body>
                  <div class="sms" role="article" aria-label={lang["SSMS2"]}>
                    <div class="from">{lang['SSMS3']}</div>
                    <div class="title">{lang['SSMS4']}</div>
                    <div class="text">
                      {lang["student"]}: <strong>{name}</strong><br>
                      {lang["class"]}: <strong>{class_}</strong><br>
                      {lang["NumBid"]}: <strong>{num}</strong>
                    </div>
                    <div class="meta">
                      {lang['date_']}: {date} • {lang["l_start"]}: 01.09.{nextY}
                    </div>
                    <div class="ok">{lang["more_details_in_PA"]}</div>
                  </div>
                </body>
                </html>     """
                           )
                    messagebox.showinfo(lang["success"],lang["schoolTRUE"])
                except Exception as err:
                    messagebox.showerror(lang["error"], str(err))

            Win = Toplevel(WIN)
            Win.title(lang["SCHOOL"])
            Win.geometry("500x650")
            img = Image.open("icons/interface/school.png")
            icon_image = ImageTk.PhotoImage(img)
            Win.iconphoto(False, icon_image)

            Label(Win, text=lang["name_of_student"], bg=global_bg, fg=global_fg).pack()
            name = ttk.Entry(Win)
            name.pack()
            Label(Win, text=lang["dateb_student"], bg=global_bg, fg=global_fg).pack()
            dateb = ttk.Entry(Win)
            dateb.pack()
            Label(Win, text=lang["n_of_school"], bg=global_bg, fg=global_fg).pack()
            schooln = ttk.Entry(Win)
            schooln.pack()
            Label(Win, text=lang["adr_of_student"], bg=global_bg, fg=global_fg).pack()
            adr = ttk.Entry(Win)
            adr.pack()
            Label(Win, text=lang["enter_name_of_mom"], bg=global_bg, fg=global_fg).pack()
            mname = ttk.Entry(Win)
            mname.pack()
            Label(Win, text=lang["enter_name_of_dad"], bg=global_bg, fg=global_fg).pack()
            pname = ttk.Entry(Win)
            pname.pack()
            Label(Win, text=lang["class_post"], bg=global_bg, fg=global_fg).pack()
            class_ = ttk.Combobox(Win,values = ["1","2","3","4","5","6","7","8","9","10","11"])
            class_.pack()
            class_.set('1')
            Label(Win, text=lang["n_med_sp"], bg=global_bg, fg=global_fg).pack()
            nmed = ttk.Entry(Win)
            nmed.pack()
            Label(Win, text=lang["tel_of_parents"], bg=global_bg, fg=global_fg).pack()
            tel = ttk.Entry(Win)
            tel.pack()
            Label(Win, text=lang["enter_parent_email"], bg=global_bg, fg=global_fg).pack()
            email = ttk.Entry(Win)
            email.pack()

            ttk.Button(Win, text='Ok', command=lambda: ok(name.get(),class_.get(),dateb.get(),schooln.get(),adr.get(),mname.get(),
                                                          pname.get(),nmed.get(),tel.get(),email.get())).pack()
        def university():
            def add_to_db(name,facult,spec,dateb,id,adr,tel,email,prededu,ball,form,financ):
                conn = sqlite3.connect("state/university.db")
                cursor = conn.cursor()
                cursor.execute("""CREATE table IF NOT EXISTS university(
                            name TEXT,
                            facult TEXT,
                            spec TEXT,
                            dateb TEXT,
                            id TEXT,
                            adr TEXT,
                            tel TEXT,
                            email TEXT,
                            prededu TEXT,
                            ball TEXT,
                            form TEXT,
                            financ TEXT
                )""")
                conn.commit()
                cursor.execute("""INSERT INTO university(name,facult,spec,dateb,id,adr,tel,email,prededu,ball,form,financ)
                 VALUES(?,?,?,?,?,?,?,?,?,?,?,?)""",(name,facult,spec,dateb,id,adr,tel,email,prededu,ball,form,financ))
                conn.commit()
                conn.close()
            def ok(name,facult,spec,dateb,id,adr,tel,email,prededu,ball,form,financ):
                try:
                    add_to_db(name,facult,spec,dateb,id,adr,tel,email,prededu,ball,form,financ)
                    today = datetime.now()
                    nextY = today.year + 1
                    num = "".join(random.choices('0123456789ABCDEFGHIJKLMNOPQRSTUVWYZ', k=12))
                    send_email(to=e, subject=lang["UNIVERSITY"], html=
                f"""
                <html>
                <head>
                  <meta charset="utf-8" />
                  <meta name="viewport" content="width=device-width,initial-scale=1" />
                  <title>{lang["YSMS1"]}</title>
                  <style>
                    body{{font-family: Inter, Arial, sans-serif;background:#f0fdf4;margin:0;display:flex;align-items:center;justify-content:center;height:100vh;padding:20px}}
                    .sms{{width:100%;max-width:520px;background:#fff;border-radius:12px;box-shadow:0 8px 28px rgba(16,185,129,0.06);padding:22px}}
                    .from{{font-size:13px;color:#059669;margin-bottom:8px}}
                    .title{{font-size:18px;font-weight:700;margin-bottom:6px;color:#065f46}}
                    .text{{font-size:15px;color:#111827;line-height:1.5;margin-bottom:12px}}
                    .meta{{font-size:13px;color:#6b7280;background:#f0fdf4;padding:10px;border-radius:8px}}
                    .ok{{display:inline-block;margin-top:14px;padding:8px 12px;border-radius:8px;background:#ecfccb;color:#365314;font-weight:600;font-size:13px}}
                  </style>
                </head>
                <body>
                  <div class="sms" role="article" aria-label={lang['YSMS2']}>
                    <div class="from">{lang["YSMS3"]}</div>
                    <div class="title">{lang["YSMS4"]}</div>
                    <div class="text">
                      {lang["studentY"]}: <strong>{name}</strong><br>
                      {lang['facultet']}: <strong>{facult}</strong><br>
                      {lang['speciality']}: <strong>{spec}</strong>
                    </div>
                    <div class="meta">
                     {lang["PN"]}: <strong>{num}</strong> • {lang["date_"]}: 01.09.{nextY}
                    </div>
                    <div class="ok">{lang["more_details_in_PAU"]}</div>
                  </div>
                </body>
                </html>


                                    """
                           )
                    messagebox.showinfo(lang["success"],lang['univerTRUE'])
                except Exception as err:
                    messagebox.showerror(lang["error"], str(err))

            Win = Toplevel(WIN)
            Win.title(lang["UNIVERSITY"])
            Win.geometry("500x650")
            img = Image.open("icons/interface/university.png")
            icon_image = ImageTk.PhotoImage(img)
            Win.iconphoto(False, icon_image)

            Label(Win,text = lang["name_of_student"],bg = global_bg,fg = global_fg).pack()
            name = ttk.Entry(Win)
            name.pack()
            Label(Win, text=lang["dateb_of_student"], bg=global_bg, fg=global_fg).pack()
            dateb = ttk.Entry(Win)
            dateb.pack()
            Label(Win, text=lang["ID_of_student"], bg=global_bg, fg=global_fg).pack()
            id = ttk.Entry(Win)
            id.pack()
            Label(Win, text=lang["adr_of_student"], bg=global_bg, fg=global_fg).pack()
            adr = ttk.Entry(Win)
            adr.pack()
            Label(Win, text=lang["tel_of_student"], bg=global_bg, fg=global_fg).pack()
            tel = ttk.Entry(Win)
            tel.pack()
            Label(Win, text=lang["email_of_student"], bg=global_bg, fg=global_fg).pack()
            email = ttk.Entry(Win)
            email.pack()
            Label(Win, text=lang["pred_edu"], bg=global_bg, fg=global_fg).pack()
            prededu = ttk.Entry(Win)
            prededu.pack()
            Label(Win, text=lang["sred_bal"], bg=global_bg, fg=global_fg).pack()
            ball = ttk.Entry(Win)
            ball.pack()
            Label(Win, text=lang["spec"], bg=global_bg, fg=global_fg).pack()
            spec = ttk.Entry(Win)
            spec.pack()
            Label(Win, text=lang["form_edu"], bg=global_bg, fg=global_fg).pack()
            form = ttk.Combobox(Win,values = [lang["formedu1"],lang['formedu2'],lang["formedu3"]])
            form.pack()
            form.set(lang["formedu1"])
            Label(Win, text=lang["facultet"], bg=global_bg, fg=global_fg).pack()
            facultet = ttk.Entry(Win)
            facultet.pack()
            Label(Win, text=lang["financ_type"], bg=global_bg, fg=global_fg).pack()
            financ = ttk.Combobox(Win, values=[lang["budget&"], lang['contract']])
            financ.pack()
            financ.set(lang["budget&"])
            ttk.Button(Win,text = 'Ok',command = lambda:ok(name.get(),facultet.get(),spec.get(),dateb.get(),id.get(),adr.get(),tel.get(),
                                                           email.get(),prededu.get(),ball.get(),form.get(),financ.get())).pack()
        if type == "detsad":
            detsad()
        elif type == "school":
            school()
        else:
            university()
    def register(name, last, age, n, e, c):
        log_to_file("func register",start_time_=start_time_)
        state_cache("func register",edition,start_time_)
        if int(age) < 14:
            log_to_file('Error! Age < 14', level="error",start_time_=start_time_)
            messagebox.showerror(lang["error"], lang["error_age"],parent = WIN)
        else:
            log_to_file("User register successfully",start_time_=start_time_)
            state_cache("User register successfully",edition,start_time_)
            with open("state/acc.cfg", "w") as f:
                f.write(f"NAME={name}\nL_NAME={last}\nAGE={age}\nTEL_NUM={n}\nEMAIL={e}\nCOUNTRY={c}")
                f.close()
            if edition in ("Professional x64", "Gaming x64", "Professional x32", "Gaming x32"):
                copy_file_to_folder("state/acc.cfg", "backup_data",start_time_)
            messagebox.showinfo(lang["succes"], lang["reg_s"],parent = WIN)
            WIN.destroy()
    def create_passport():
        log_to_file("Create passport",start_time_=start_time_)
        state_cache("Create passport",edition,start_time_)

        def ok(c, name, ln, age, da, adr, g, p, img):
            check2 = len(da.strip("0123456789+/ "))
            if age.isalnum():
                pass
            else:
                log_to_file("Age is not number!",start_time_=start_time_)
                state_cache("Age is not number!",edition,start_time_)
                messagebox.showerror(lang["error"], lang["error_a"],parent = WIN)
                WIN.destroy()
            if check2 == 0:
                check2 = False
            else:
                check2 = True
            if check2:
                messagebox.showerror(lang["error"], lang["error_p"],parent = WIN)
                WIN.destroy()

            num = randint(100000, 999999)
            today = date.today().strftime("%d.%m.%Y")
            with open(f'state/passport_{today}.cfg', 'w', encoding="utf-8") as f:
                f.write(
                    f"NAME={name}\nLAST_NAME={ln}\nAGE={age}\nDATE={da}\nCOUNTRY={adr}\nCITY={c}\nCITIZENSHIP={g}\nSEX={p}\nIMG_PATH={img}\nDATE_OF_ISSUE={today}\nPASSPORT_NUM={str(num)}")
                f.close()
            log_to_file("Passport created",start_time_=start_time_)
            state_cache("Passport created",edition,start_time_)
            n,ln,e = return_user_info()
            send_email(to = e,subject=lang["passport"],html =
                       f"""
            <html>
              <body style="font-family: Arial, sans-serif; background-color: #f5f5f5; padding: 20px;">
                <div style="background-color: #ffffff; padding: 25px; border-radius: 10px; box-shadow: 0px 2px 8px rgba(0,0,0,0.15); max-width: 600px; margin: auto;">
                  <h2 style="text-align:center; color: #2c3e50;">🪪 DIGITAL PASSPORT</h2>
                  <hr style="border: none; border-top: 2px solid #007BFF; margin: 10px 0 20px 0;">

                  <div style="display: flex; align-items: center; gap: 20px;">
                    <img src="{img}" alt="{lang['passport_photo']}" style="width: 120px; height: 150px; border-radius: 5px; object-fit: cover; border: 2px solid #007BFF;">
                    <div style="flex: 1;">
                      <p style="margin: 5px 0;"><strong>{lang['p_name']}:</strong> {name}</p>
                      <p style="margin: 5px 0;"><strong>{lang['p_lname']}:</strong> {ln}</p>
                      <p style="margin: 5px 0;"><strong>{lang["gender"]}:</strong> {p}</p>
                      <p style="margin: 5px 0;"><strong>{lang["p_age"]}:</strong> {age}</p>
                      <p style="margin: 5px 0;"><strong>{lang["p_date"]}:</strong> {da}</p>
                    </div>
                  </div>

                  <div style="margin-top: 20px;">
                    <p style="margin: 5px 0;"><strong>{lang["p_country"]}:</strong> {adr}</p>
                    <p style="margin: 5px 0;"><strong>{lang["p_city"]}:</strong> {c}</p>
                    <p style="margin: 5px 0;"><strong>{lang["cityzenship"]}:</strong> {g}</p>
                    <p style="margin: 5px 0;"><strong>{lang["p_issue"]}:</strong> {today}</p>
                    <p style="margin: 5px 0;"><strong>{lang["p_num"]}:</strong> {num}</p>
                  </div>

                  <hr style="border: none; border-top: 1px solid #ccc; margin: 20px 0;">
                  <p style="font-size: 12px; color: #888; text-align:center;">
                    This document was generated automatically. Please do not reply to this email.
                  </p>
                </div>
              </body>
            </html>
            """
            )


            messagebox.showinfo(lang["success"], lang["passp_true"],parent = Win)

        Win = Toplevel(WIN)
        Win.attributes("-alpha",float(GlobalAlpha))
        Win.geometry('600x500')
        Win.config(bg=global_bg)
        img = Image.open("icons/State Services.png")
        icon_image = ImageTk.PhotoImage(img)
        Win.iconphoto(False, icon_image)
        Win.title(lang["cr_passp"])
        frame = Frame(Win,bg = global_bg)
        frame.pack()
        Label(frame, text=lang["enter_nam"],bg=global_bg,fg=global_fg).pack()
        name = ctk.CTkEntry(frame,placeholder_text=lang["enter_nam"])
        name.pack()
        Label(frame, text=lang["enter_ln"],bg=global_bg,fg=global_fg).pack()
        last_name = ctk.CTkEntry(frame,placeholder_text=lang["enter_ln"])
        last_name.pack()
        Label(frame, text=lang["enter_age"],bg=global_bg,fg=global_fg).pack()
        age = ctk.CTkEntry(frame,placeholder_text=lang["enter_age"])
        age.pack()
        Label(frame, text=lang["date"],bg=global_bg,fg=global_fg).pack()
        dat = ctk.CTkEntry(frame,placeholder_text=lang["date"])
        dat.pack()
        Label(frame, text=lang["adr"],bg=global_bg,fg=global_fg).pack()
        adr = ctk.CTkEntry(frame,placeholder_text=lang["adr"])
        adr.pack()
        Label(frame, text=lang["grazh"],bg=global_bg,fg=global_fg).pack()
        gr = ctk.CTkEntry(frame,placeholder_text=lang["grazh"])
        gr.pack()
        Label(frame, text=lang["city"],bg=global_bg,fg=global_fg).pack()
        c = ctk.CTkEntry(frame,placeholder_text=lang["city"])
        c.pack()
        Label(frame, text=lang["poll"],bg=global_bg,fg=global_fg).pack()
        p = ttk.Combobox(frame,values = [lang["man"],lang["woman"]])
        p.pack()
        p.set(lang["man"])
        Label(frame, text=lang["select_img"],bg=global_bg,fg=global_fg).pack()
        img = ctk.CTkEntry(frame,placeholder_text=lang["select_img"])
        img.pack()
        ttk.Button(frame, text=lang["Apply"],
                   command=lambda: ok(c.get(), name.get(), last_name.get(), age.get(), dat.get(), adr.get(), gr.get(),
                                      p.get(), img.get())).pack()
    def work():
        log_to_file("Work",start_time_=start_time_)
        state_cache("Work",edition,start_time_)

        def apply_job(w, s):
            log_to_file("Apply job",start_time_=start_time_)
            state_cache("Apply job",edition,start_time_)
            if os.path.exists('state/job.cfg'):
                with open("state/job.cfg", 'a', encoding="utf-8") as f:
                    f.write(f"WORK_N={w}\nSALARY={s}\n")
                    f.close()
                if edition in ("Professional x64", "Gaming x64","Professional x32", "Gaming x32"):
                    copy_file_to_folder("state/job.cfg", "backup_data",start_time_)
            else:
                with open("state/job.cfg", 'w', encoding="utf-8") as f:
                    f.write(f"WORK_N={w}\nSALARY={s}\n")
                    f.close()
                if edition in ("Professional x64", "Gaming x64","Professional x32", "Gaming x32"):
                    copy_file_to_folder("state/job.cfg", "backup_data",start_time_)
            if os.path.exists('state/dat.cfg'):
                with open("state/dat.cfg", 'a', encoding="utf-8") as f:
                    f.write(f"{datetime.today().strftime('%d.%m.%Y')}n")
                    f.close()
                if edition in ("Professional x64", "Gaming x64","Professional x32", "Gaming x32"):
                    copy_file_to_folder("state/dat.cfg", "backup_data",start_time_)
            else:
                with open("state/dat.cfg", 'w', encoding="utf-8") as f:
                    f.write(f"{datetime.today().strftime('%d.%m.%Y')}\n")
                    f.close()
                if edition in ("Professional x64", "Gaming x64","Professional x32", "Gaming x32"):
                    copy_file_to_folder("state/dat.cfg", "backup_data",start_time_)
            messagebox.showinfo(lang["success"], lang["ust_tr"] + w,parent = Win)

        def del_j():
            log_to_file("Delete job",start_time_=start_time_)
            state_cache("DElete job",edition,start_time_)
            try:
                os.remove("state/job.cfg")
                messagebox.showinfo(lang["success"], lang["del_j_tr"],parent = Win)
            except:
                messagebox.showerror(lang["error"], errors[3] + lang["nofile"],parent = Win)

        if os.path.exists("state/job.cfg"):
            Win = Toplevel(WIN)
            Win.attributes("-alpha",float(GlobalAlpha))
            Win.config(bg=global_bg)
            img = Image.open("icons/State Services.png")
            icon_image = ImageTk.PhotoImage(img)
            Win.iconphoto(False, icon_image)
            Win.geometry()
            Win.title(lang['ust_r'])
            Label(Win, text=lang["ustr_true"],bg=global_bg,fg=global_fg).pack()
            ttk.Button(Win, text=lang["uvol"], command=del_j).pack()
        else:
            Win = Toplevel(WIN)
            Win.attributes("-alpha", float(GlobalAlpha))
            Win.config(bg=global_bg)
            img = Image.open("icons/State Services.png")
            icon_image = ImageTk.PhotoImage(img)
            Win.iconphoto(False, icon_image)
            Win.geometry()
            Win.title(lang['ust_r'])
            works = [
                {"Work": lang["casse"], "Salary": "6000"},
                {"Work": lang["ub"], "Salary": "5000"},
                {"Work": lang["st"], "Salary": "7000"},
                {"Work": lang["vh"], "Salary": "5000"},
                {"Work": lang["oh"], "Salary": "5000"}
            ]
            for job in works:
                frame = Frame(Win)
                frame.pack(pady=5)
                Label(frame, text=f"{job['Work']} - {job['Salary']}",bg=global_bg,fg=global_fg).pack(side="left", padx=10)
                Button(frame, text=lang["ust"],
                       command=lambda w=job['Work'], s=job['Salary']: apply_job(w, s)).pack(side="right")
    def create_ip():
        log_to_file("Create international passport",start_time_=start_time_)
        state_cache("Create insternatinal passport",edition,start_time_)

        def ok(c, name, ln, age, da, adr, g, p, img):
            log_to_file("INP Created",start_time_=start_time_)
            state_cache("INP Created",edition,start_time_)
            num = randint(100000, 999999)
            today = date.today().strftime("%d.%m.%Y")
            with open(f'state/passport_{today}.cfg', 'w', encoding="utf-8") as f:
                f.write(
                    f"NAME={name}\nLAST_NAME={ln}\nAGE={age}\nDATE={da}\nCOUNTRY={adr}\nCITY={c}\nCITIZENSHIP={g}\nSEX={p}\nIMG_PATH={img}\nDATE_OF_ISSUE={today}\nPASSPORT_NUM={str(num)}")
                f.close()
            messagebox.showinfo(lang["success"], lang["passp_true"],parent = Win)

        Win = Toplevel(WIN)
        Win.attributes("-alpha", float(GlobalAlpha))
        Win.geometry('600x500')
        Win.config(bg=global_bg)
        img = Image.open("icons/State Services.png")
        icon_image = ImageTk.PhotoImage(img)
        Win.iconphoto(False, icon_image)
        Win.title(lang["cr_passp"])
        frame = Frame(Win)
        frame.pack()
        Label(frame, text=lang["enter_nam"],bg=global_bg,fg=global_fg).pack()
        name = ctk.CTkEntry(frame,placeholder_text=lang['enter_nam'])
        name.pack()
        Label(frame, text=lang["enter_ln"],bg=global_bg,fg=global_fg).pack()
        last_name = ctk.CTkEntry(frame,placeholder_text=lang['enter_ln'])
        last_name.pack()
        Label(frame, text=lang["enter_age"],bg=global_bg,fg=global_fg).pack()
        age = ctk.CTkEntry(frame,placeholder_text=lang['enter_age'])
        age.pack()
        Label(frame, text=lang["date"],bg=global_bg,fg=global_fg).pack()
        dat = ctk.CTkEntry(frame,placeholder_text=lang['date'])
        dat.pack()
        Label(frame, text=lang["adr"],bg=global_bg,fg=global_fg).pack()
        adr = ctk.CTkEntry(frame,placeholder_text=lang['adr'])
        adr.pack()
        Label(frame, text=lang["grazh"],bg=global_bg,fg=global_fg).pack()
        gr = ctk.CTkEntry(frame,placeholder_text=lang['grazh'])
        gr.pack()
        Label(frame, text=lang["city"],bg=global_bg,fg=global_fg).pack()
        c = ctk.CTkEntry(frame,placeholder_text=lang['city'])
        c.pack()
        Label(frame, text=lang["poll"],bg=global_bg,fg=global_fg).pack()
        p = ctk.CTkEntry(frame)
        p.pack()
        Label(frame, text=lang["select_img"],bg=global_bg,fg=global_fg).pack()
        img = ctk.CTkEntry(frame,placeholder_text=lang['select_img'])
        img.pack()
        ttk.Button(frame, text=lang["Apply"],
                   command=lambda: ok(c.get(), name.get(), last_name.get(), age.get(), dat.get(), adr.get(),
                                      gr.get(), p.get(), img.get())).pack()
    def show_acc():
        log_to_file("Show account",start_time_=start_time_)
        state_cache("Show account",edition,start_time_)
        s = Toplevel(WIN)
        s.attributes("-alpha",float(GlobalAlpha))
        s.attributes('-topmost', True)
        s.config(bg=global_bg)
        s.geometry('400x300')
        s.title(lang["acc"])
        img = Image.open("icons/State Services.png")
        icon_image = ImageTk.PhotoImage(img)
        s.iconphoto(False, icon_image)
        config = {}
        with open("state/acc.cfg", "r", encoding='utf-8') as f:
            for line in f:
                key2, value1 = line.strip().split("=")
                config[key2] = value1
        n = config.get("NAME")
        l = config.get("L_NAME")
        a = config.get("AGE")
        t = config.get("TEL_NUM")
        e = config.get("EMAIL")
        c = config.get("COUNTRY")
        Label(s, text=lang["u_acc"], font=("Times", 20, "bold"),bg=global_bg,fg=global_fg).pack()
        Label(s, text=lang["name"] + n, font=("Arial", 14, "italic"),bg=global_bg,fg=global_fg).pack()
        Label(s, text=lang["last-name"] + l, font=("Arial", 14, "italic"),bg=global_bg,fg=global_fg).pack()
        Label(s, text=lang["age"] + a, font=("Arial", 14, "italic"),bg=global_bg,fg=global_fg).pack()
        Label(s, text=lang["tel_n"] + t, font=("Arial", 14, "italic"),bg=global_bg,fg=global_fg).pack()
        Label(s, text=lang["email"] + e, font=("Arial", 14, "italic"),bg=global_bg,fg=global_fg).pack()
        Label(s, text=lang["country"] + c, font=("Arial", 14, "italic"),bg=global_bg,fg=global_fg).pack()
    def nalogi():
        log_to_file("Show tax",start_time_=start_time_)
        state_cache("Show tax",edition,start_time_)
        w = Toplevel(WIN)
        w.attributes("-alpha",float(GlobalAlpha))
        w.config(bg=global_bg)
        w.title(lang['nal'])
        w.geometry("300x300")
        img = Image.open("icons/State Services.png")
        icon_image = ImageTk.PhotoImage(img)
        w.iconphoto(False, icon_image)
        try:
            config = {}
            with open("state/job.cfg", "r", encoding='utf-8') as f:
                for line in f:
                    key2, value1 = line.strip().split("=")
                    config[key2] = value1
                s = config.get("SALARY")
                year = int(s) * 12
                tax = 0
                if year < 5000000:
                    tax = (int(s) / 100) * 13
                else:
                    tax = (int(s) / 100) * 15
                Label(w, text=f"{lang['sa']} - {int(s)}",bg=global_bg,fg=global_fg).pack()
                Label(w, text=f"{lang['y_nal']} - {tax}",bg=global_bg,fg=global_fg).pack()
        except:
            Label(w, text="NONE",bg=global_bg,fg=global_fg).pack()
    def prod():
        log_to_file("prod immovables",start_time_=start_time_)
        state_cache("prod immovables",edition,start_time_)

        def pr(index, price):
            global svb_coins
            svb_coins = load_balance(start_time_)
            svb_coins += int(price)
            send('receipt', int(price))
            transactions(f"+{int(price)} SVb Coins" + f" {datetime.now()}",start_time_)
            save_balance(svb_coins,start_time_)
            check_ach(lang,start_time_)
            with open("state/nedv.cfg", "r", encoding="utf-8") as f:
                lines = [line.strip() for line in f.readlines()]

            blocks = [lines[i:i + 3] for i in range(0, len(lines), 3)]

            if 0 <= index < len(blocks):
                del blocks[index]

            with open("state/nedv.cfg", "w", encoding="utf-8") as f:
                for block in blocks:
                    for line in block:
                        f.write(line + "\n")
            if edition in ("Professional x64", "Gaming x64","Professional x32", "Gaming x32"):
                copy_file_to_folder("state/nedv.cfg", "backup_data",start_time_)
            messagebox.showinfo(lang["success"], lang["prod_true"],parent = w)

        w = Toplevel(WIN)
        w.attributes("-alpha",float(GlobalAlpha))
        w.title(lang['nedvi'])
        w.config(bg=global_bg)
        w.geometry("500x400")
        img = Image.open("icons/State Services.png")
        icon_image = ImageTk.PhotoImage(img)
        w.iconphoto(False, icon_image)
        imgs = []
        types = []
        prices = []
        try:
            with open("state/nedv.cfg", "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("IMG="):
                        plate = line.split("=", 1)[1]
                        imgs.append(plate)
                    if line.startswith("TYPE="):
                        brand = line.split("=", 1)[1]
                        types.append(brand)
                    if line.startswith("PRICE="):
                        model = line.split("=", 1)[1]
                        prices.append(model)
        except:
            pass
        w.img_refs = []

        for i, img in enumerate(imgs):
            imgtk = ImageTk.PhotoImage(
                Image.open(img).resize((52, 52), Image.Resampling.LANCZOS)
            )
            w.img_refs.append(imgtk)

            prod_price = (int(prices[i]) / 100) * 90

            Label(w, image=imgtk).pack()
            ttk.Button(w, text=f'{lang["prod_z"]} {prod_price}', command=lambda i=i, p=prod_price: pr(i, p)).pack()
    def my_nedv():
        log_to_file("my immovables",start_time_=start_time_)
        state_cache("my immovables",edition,start_time_)
        w = Toplevel(WIN)
        w.attributes("-alpha",float(GlobalAlpha))
        w.config(bg=global_bg)
        w.title(lang['nedvi'])
        w.geometry("500x400")
        img = Image.open("icons/State Services.png")
        icon_image = ImageTk.PhotoImage(img)
        w.iconphoto(False, icon_image)
        imgs = []
        types = []
        prices = []
        try:
            with open("state/nedv.cfg", "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("IMG="):
                        plate = line.split("=", 1)[1]
                        imgs.append(plate)
                    if line.startswith("TYPE="):
                        brand = line.split("=", 1)[1]
                        types.append(brand)
                    if line.startswith("PRICE="):
                        model = line.split("=", 1)[1]
                        prices.append(model)
        except:
            pass
        w.img_refs = []

        for i, img in enumerate(imgs):
            imgtk = ImageTk.PhotoImage(
                Image.open(img).resize((52, 52), Image.Resampling.LANCZOS)
            )
            w.img_refs.append(imgtk)

            prod_price = (int(prices[i]) / 100) * 90

            lab = Label(w, image=imgtk)
            lab.pack()

            Label(w, text=f"{lang['pricep']} - {prices[i]}",bg=global_bg,fg=global_fg).pack()
            Label(w, text=f"{lang['pricepr']} - {prod_price}",bg=global_bg,fg=global_fg).pack()
    def nedv():
        def pay(price, type, img):
            log_to_file("pay immovables",start_time_=start_time_)
            state_cache("pay immovables",edition,start_time_)
            global svb_coins
            svb_coins = load_balance(start_time_)
            if svb_coins >= price:
                log_to_file("pay successfully",start_time_=start_time_)
                state_cache("pay successfully",edition,start_time_)
                svb_coins -= price
                send('payement', int(price))
                transactions(f"-{price} SVb Coins" + f" {datetime.now()}",start_time_)
                save_balance(svb_coins,start_time_)
                if os.path.exists("state/nedv.cfg"):
                    with open("state/nedv.cfg", "a") as f:
                        f.write(f"\nIMG={img}\nTYPE={type}\nPRICE={price}\n")
                    if edition in ("Professional x64", "Gaming x64","Professional x32", "Gaming x32"):
                        copy_file_to_folder("state/nedv.cfg", "backup_data",start_time_)
                else:
                    with open("state/nedv.cfg", "w") as f:
                        f.write(f"\nIMG={img}\nTYPE={type}\nPRICE={price}\n")
                    if edition in ("Professional x64", "Gaming x64","Professional x32", "Gaming x32"):
                        copy_file_to_folder("state/nedv.cfg", "backup_data",start_time_)
                messagebox.showinfo(lang["success"], lang["nedv_true"],parent = w)
            else:
                messagebox.showerror(lang["error"], lang["no_svb"],parent = w)

        log_to_file("immovables",start_time_=start_time_)
        state_cache("immovables",edition,start_time_)
        w = Toplevel(WIN)
        w.title(lang['nedvi'])
        w.attributes("-alpha", float(GlobalAlpha))
        w.config(bg=global_bg)
        w.geometry("700x600")
        img = Image.open("icons/State Services.png")
        icon_image = ImageTk.PhotoImage(img)
        w.iconphoto(False, icon_image)
        imgs = []
        types = []
        prices = []
        try:
            with open("state/nedv.cfg", "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("IMG="):
                        plate = line.split("=", 1)[1]
                        imgs.append(plate)
                    if line.startswith("TYPE="):
                        brand = line.split("=", 1)[1]
                        types.append(brand)
                    if line.startswith("PRICE="):
                        model = line.split("=", 1)[1]
                        prices.append(model)
        except:
            pass

        w.dom = ImageTk.PhotoImage(
            Image.open('icons/free-icon-house-619155.png').resize((52, 52), Image.Resampling.LANCZOS)
        )
        w.dom1 = ImageTk.PhotoImage(
            Image.open('icons/free-icon-house-619034.png').resize((52, 52), Image.Resampling.LANCZOS)
        )
        w.dom2 = ImageTk.PhotoImage(
            Image.open('icons/free-icon-apartment-building-11248197.png').resize((52, 52), Image.Resampling.LANCZOS)
        )
        w.dom3 = ImageTk.PhotoImage(
            Image.open('icons/free-icon-apartment-1824414.png').resize((52, 52), Image.Resampling.LANCZOS)
        )
        if "dom1" in types:
            Label(w, text=lang["buy_tr"],bg=global_bg,fg=global_fg).pack()
        else:
            Label(w, text=lang["dom1"],bg=global_bg,fg=global_fg).pack()
            Label(w, text=f'{lang["pr"]} 120.000 SVB Coins',bg=global_bg,fg=global_fg).pack()
            ttk.Button(w, image=w.dom, command=lambda: pay(120000, "dom1", 'icons/free-icon-house-619155.png')).pack()
        if "dom2" in types:
            Label(w, text=lang["buy_tr"],bg=global_bg,fg=global_fg).pack()
        else:
            Label(w, text=lang["dom2"],bg=global_bg,fg=global_fg).pack()
            Label(w, text=f'{lang["pr"]} 210.000 SVB Coins',bg=global_bg,fg=global_fg).pack()
            ttk.Button(w, image=w.dom1,
                       command=lambda: pay(210000, "dom2", 'icons/free-icon-house-619034.png')).pack()
        if "ap1" in types:
            Label(w, text=lang["buy_tr"],bg=global_bg,fg=global_fg).pack()
        else:
            Label(w, text=lang["ap1"],bg=global_bg,fg=global_fg).pack()
            Label(w, text=f'{lang["pr"]} 170.000 SVB Coins',bg=global_bg,fg=global_fg).pack()
            ttk.Button(w, image=w.dom2,
                       command=lambda: pay(170000, "ap1", 'icons/free-icon-apartment-building-11248197.png')).pack()
        if 'ap2' in types:
            Label(w, text=lang["buy_tr"],bg=global_bg,fg=global_fg).pack()
        else:
            Label(w, text=lang["ap2"],bg=global_bg,fg=global_fg).pack()
            Label(w, text=f'{lang["pr"]} 130.000 SVB Coins',bg=global_bg,fg=global_fg).pack()
            ttk.Button(w, image=w.dom3,
                       command=lambda: pay(130000, "ap2", 'icons/free-icon-apartment-1824414.png')).pack()
    def show_tooltip(event, txt):
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
        except:
            pass
    def hide_tooltip(event):
        global tooltip
        if tooltip:
            tooltip.destroy()
            tooltip = None
    if os.path.exists("state/acc.cfg"):
        job = False
        if os.path.exists("state/job.cfg"):
            job = True
        config = {}
        with open("state/acc.cfg", "r", encoding='utf-8') as f:
            for line in f:
                key2, value1 = line.strip().split("=")
                config[key2] = value1
        WIN = Toplevel(root)
        WIN.attributes("-alpha",float(GlobalAlpha))
        WIN.geometry("800x700")
        WIN.config(bg=global_bg)
        WIN.title("State Services")
        img = Image.open("icons/State Services.png")
        icon_image = ImageTk.PhotoImage(img)
        WIN.iconphoto(False, icon_image)

        WIN.pasp1= ImageTk.PhotoImage(
            Image.open('icons/interface/pasp1.png').resize((50, 50), Image.Resampling.LANCZOS)
        )
        WIN.pasp2 = ImageTk.PhotoImage(
            Image.open('icons/interface/pasp2.png').resize((50, 50), Image.Resampling.LANCZOS)
        )
        WIN.sellnedv= ImageTk.PhotoImage(
            Image.open('icons/interface/sellnedv.png').resize((50, 50), Image.Resampling.LANCZOS)
        )
        WIN.buynedv= ImageTk.PhotoImage(
            Image.open('icons/interface/buynedv.png').resize((50, 50), Image.Resampling.LANCZOS)
        )
        WIN.tax= ImageTk.PhotoImage(
            Image.open('icons/interface/tax.png').resize((50, 50), Image.Resampling.LANCZOS)
        )
        WIN.mynedv = ImageTk.PhotoImage(
            Image.open('icons/interface/mynedv.png').resize((50, 50), Image.Resampling.LANCZOS)
        )
        WIN.job = ImageTk.PhotoImage(
            Image.open('icons/interface/job.png').resize((50, 50), Image.Resampling.LANCZOS)
        )
        WIN.school = ImageTk.PhotoImage(
            Image.open('icons/interface/school.png').resize((50, 50), Image.Resampling.LANCZOS)
        )
        WIN.detsad = ImageTk.PhotoImage(
            Image.open('icons/interface/detsad.png').resize((50, 50), Image.Resampling.LANCZOS)
        )
        WIN.university = ImageTk.PhotoImage(
            Image.open('icons/interface/university.png').resize((50, 50), Image.Resampling.LANCZOS)
        )
        WIN.business = ImageTk.PhotoImage(
            Image.open('icons/interface/business.png').resize((50, 50), Image.Resampling.LANCZOS)
        )
        WIN.ipo = ImageTk.PhotoImage(
            Image.open('icons/interface/ipo.png').resize((50, 50), Image.Resampling.LANCZOS)
        )


        n = False
        if os.path.exists("state/nedv.cfg"):
            n = True
        try:
            acc_path = "icons//acc3.png"
            acc = ImageTk.PhotoImage(Image.open(acc_path).resize((44, 44), Image.Resampling.LANCZOS))
        except Exception as e:
            acc = None
        a = config.get("AGE")
        Label(WIN, text="STATE SERVICES", font=("Times", 23, "bold"), bg=global_bg, fg=global_fg).pack()
        btn_acc = ttk.Button(WIN, image=acc, command=show_acc)
        btn_acc.image = acc
        btn_acc.pack()
        btn_acc.bind("<Enter>", lambda event: show_tooltip(event, txt=lang["acc"]))
        btn_acc.bind("<Leave>", hide_tooltip)
        frm1 = Frame(WIN)
        frm1.pack()
        frm2 = Frame(WIN)
        frm2.pack()
        frm3 = Frame(WIN)
        frm3.pack()
        frm4 = Frame(WIN)
        frm4.pack()

        btn = ttk.Button(frm1, image=WIN.pasp1, command=create_passport)
        btn.pack(side=LEFT)
        btn.bind("<Enter>", lambda event: show_tooltip(event, txt=lang["cr_passp"]))
        btn.bind("<Leave>", hide_tooltip)

        if os.path.exists('state/international_passport.cfg'):
            Label(frm1, text=lang["passp_tr"], bg=global_bg, fg=global_fg).pack()
            btn1 = ttk.Button(frm1, image=WIN.pasp1, command=create_ip,state="disabled")
            btn1.pack(side = LEFT)
            btn1.bind("<Enter>", lambda event: show_tooltip(event, txt=lang["cr_passp_z"]))
            btn1.bind("<Leave>", hide_tooltip)
        else:
            btn1 = ttk.Button(frm1, image=WIN.pasp2, command=create_ip)
            btn1.pack(side = LEFT)
            btn1.bind("<Enter>", lambda event: show_tooltip(event, txt=lang["cr_passp_z"]))
            btn1.bind("<Leave>", hide_tooltip)
        if int(a) >= 18:
            btn2 = ttk.Button(frm2, image=WIN.job, command=work)
            btn2.pack(side = LEFT)
            btn2.bind("<Enter>", lambda event: show_tooltip(event, txt=lang["searh_w"]))
            btn2.bind("<Leave>", hide_tooltip)
        else:
            Label(frm2, text=lang["age_min18"],bg=global_bg,fg=global_fg).pack()
            btn2 = ttk.Button(frm2, image=WIN.job, command=work, state="disabled")
            btn2.pack(side = LEFT)
            btn2.bind("<Enter>", lambda event: show_tooltip(event, txt=lang["less_age"]))
            btn2.bind("<Leave>", hide_tooltip)
        if job:
            btn3 = ttk.Button(frm2, image=WIN.tax, command=nalogi)
            btn3.pack(side = LEFT)
            btn3.bind("<Enter>", lambda event: show_tooltip(event, txt=lang["nal"]))
            btn3.bind("<Leave>", hide_tooltip)
        btn4 = ttk.Button(frm3, image=WIN.buynedv, command=nedv)
        btn4.pack(side = LEFT)
        btn4.bind("<Enter>", lambda event: show_tooltip(event, txt=lang["buy_ned"]))
        btn4.bind("<Leave>", hide_tooltip)
        if n:
            btn3 = ttk.Button(frm3, image=WIN.sellnedv, command=prod)
            btn3.pack(side = LEFT)
            btn3.bind("<Enter>", lambda event: show_tooltip(event, txt=lang["prod"]))
            btn3.bind("<Leave>", hide_tooltip)
        if os.path.exists("state/nedv.cfg"):
            btn3 = ttk.Button(frm3, image=WIN.mynedv, command=my_nedv)
            btn3.pack(side = LEFT)
            btn3.bind("<Enter>", lambda event: show_tooltip(event, txt=lang["my-n"]))
            btn3.bind("<Leave>", hide_tooltip)

        btn = ttk.Button(frm3, image=WIN.ipo, command=open_flp)
        btn.pack(side=LEFT)
        btn.bind("<Enter>", lambda event: show_tooltip(event, txt=lang["IPO_OPENED"]))
        btn.bind("<Leave>", hide_tooltip)
        btn = ttk.Button(frm3, image=WIN.business, command=open_business)
        btn.pack(side=LEFT)
        btn.bind("<Enter>", lambda event: show_tooltip(event, txt=lang["BOPENED"]))
        btn.bind("<Leave>", hide_tooltip)
        btn = ttk.Button(frm4, image=WIN.detsad, command=lambda:register_in_edu("detsad"))
        btn.pack(side=LEFT)
        btn.bind("<Enter>", lambda event: show_tooltip(event, txt=lang["DETSAD"]))
        btn.bind("<Leave>", hide_tooltip)
        btn = ttk.Button(frm4, image=WIN.school, command=lambda:register_in_edu("school"))
        btn.pack(side=LEFT)
        btn.bind("<Enter>", lambda event: show_tooltip(event, txt=lang["SCHOOL"]))
        btn.bind("<Leave>", hide_tooltip)
        btn = ttk.Button(frm4, image=WIN.university, command=lambda:register_in_edu("university"))
        btn.pack(side=LEFT)
        btn.bind("<Enter>", lambda event: show_tooltip(event, txt=lang["UNIVERSITY"]))
        btn.bind("<Leave>", hide_tooltip)
    else:
        WIN = Toplevel(root)
        WIN.attributes("-alpha",float(GlobalAlpha))
        WIN.config(bg=global_bg)
        WIN.geometry("600x500")
        WIN.title("State Services")
        img = Image.open("icons/State Services.png")
        icon_image = ImageTk.PhotoImage(img)
        WIN.iconphoto(False, icon_image)
        frm = Frame(WIN)
        frm.pack()
        Label(frm, text=lang["register"], font=("Arial", 17, "bold"),bg=global_bg,fg=global_fg).pack()
        Label(frm, text=lang["enter_nam"],bg=global_bg,fg=global_fg).pack()
        name = ctk.CTkEntry(frm,placeholder_text=lang['enter_nam'])
        name.pack()
        Label(frm, text=lang["enter_ln"],bg=global_bg,fg=global_fg).pack()
        last_name = ctk.CTkEntry(frm,placeholder_text=lang['enter_ln'])
        last_name.pack()
        Label(frm, text=lang["enter_age"],bg=global_bg,fg=global_fg).pack()
        age = ctk.CTkEntry(frm,placeholder_text=lang['enter_age'])
        age.pack()
        Label(frm, text=lang["enter_num"],bg=global_bg,fg=global_fg).pack()
        num = ctk.CTkEntry(frm,placeholder_text=lang['enter_num'])
        num.pack()
        Label(frm, text=lang["enter_ema"],bg=global_bg,fg=global_fg).pack()
        email = ctk.CTkEntry(frm,placeholder_text=lang['enter_ema'])
        email.pack()
        Label(frm, text=lang["enter_country"],bg=global_bg,fg=global_fg).pack()
        countries = dict(countries_for_language('en'))
        countries_list = sorted(list(countries.values()))
        country_var = StringVar()
        country_box = ttk.Combobox(frm, textvariable=country_var, values=countries_list)
        country_box.set("Russia")
        country_box.pack(pady=10)
        ttk.Button(frm, text=lang["regg"],
                   command=lambda: register(name.get(), last_name.get(), age.get(), num.get(), email.get(),
                                            country_var.get())).pack()
