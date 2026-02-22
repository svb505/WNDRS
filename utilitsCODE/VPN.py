from tkinter import *
from tkinter import ttk,messagebox
from PIL import Image, ImageTk
from runinthread import run_in_thread
from play_sound import play_sound
from logtofile import log_to_file
from readandwrite_to_files import write_file
import sqlite3
from copy_file_to_folder import copy_file_to_folder
from create_window import create_window


def open_vpn(root,lang,actives_programs,start_time_,volume,state_sound,edition,global_bg,global_fg,reg,GlobalAlpha):
    actives_programs.append("VPN")
    run_in_thread(play_sound("sound//click.mp3", volume, state_sound, start_time_))

    def on():
        run_in_thread(play_sound("sound//click.mp3", volume, state_sound, start_time_))
        log_to_file('VPN on', start_time_=start_time_)
        if var1.get() == lang["usa"]:
            regg = "usa"
            run_in_thread(play_sound("sound//am.mp3", volume, state_sound, start_time_))
        elif var1.get() == lang["netherlans"]:
            regg = "netherlans"
        elif var1.get() == lang["france"]:
            regg = "france"
        elif var1.get() == lang["russia"]:
            regg = "russia"
        elif var1.get() == lang["hungry"]:
            regg = "hungry"
        elif var1.get() == lang["italia"]:
            regg = "italia"
        elif var1.get() == lang["canada"]:
            regg = "canada"
        else:
            regg = 'australia'
        conn = sqlite3.connect("configurations.db")
        cursor = conn.cursor()
        cursor.execute("""UPDATE states 
                          SET vpn = ? WHERE ID = 1""", ("on",))
        conn.commit()
        if edition in ("Professional x64", "Gaming x64", "Professional x32", "Gaming x32"):
            copy_file_to_folder("configurations.db", "backup_data", start_time_)
        write_file("syst_comp/region.cfg", "w", regg)
        if edition in ("Professional x64", "Gaming x64", "Professional x32", "Gaming x32"):
            copy_file_to_folder("syst_comp/region.cfg", "backup_data", start_time_)

        messagebox.showinfo(lang["success"], lang["vpn_state_on"], parent=vpn_win)
        log_to_file(f"Message: {lang['vpn_state_on']}", start_time_=start_time_)
        log_to_file(f'Region: {var1.get()}', start_time_=start_time_)

    def off():
        run_in_thread(play_sound("sound//click.mp3", volume, state_sound, start_time_))
        conn = sqlite3.connect("configurations.db")
        cursor = conn.cursor()
        cursor.execute("""UPDATE states
                          SET vpn = ? WHERE ID = 1""", ("off",))
        conn.commit()
        if edition in ("Professional x64", "Gaming x64", "Professional x32", "Gaming x32"):
            copy_file_to_folder("configurations.db", "backup_data", start_time_)
        messagebox.showinfo(lang["success"], lang["vpn_state_off"], parent=vpn_win)
        log_to_file(f"Message: {lang['vpn_state_off']}", start_time_=start_time_)

    actives_programs.append("VPN")
    log_to_file('VPN launch', start_time_=start_time_)
    global vpn_win
    vpn_win = create_window(root, "VPN", global_bg, float(GlobalAlpha), 400, 300, "icons/interface/vvppnn.png")
    img1 = Image.open('icons/interface/vvppnn.png')
    img1 = img1.resize((60, 60), Image.Resampling.LANCZOS)
    icon1 = ImageTk.PhotoImage(img1)
    l = Label(vpn_win, image=icon1)
    l.image = icon1
    l.pack()

    regions = [lang["usa"], lang["netherlans"], lang["france"], lang["australia"], lang["russia"],
               lang["hungry"], lang["canada"], lang["italia"]]

    var1 = StringVar(value=reg)
    conn = sqlite3.connect("configurations.db")
    cursor = conn.cursor()
    cursor.execute("SELECT vpn FROM states WHERE ID = 1")
    vpn_state = cursor.fetchone()
    conn.commit()
    if edition in ("Professional x64", "Gaming x64", "Professional x32", "Gaming x32"):
        copy_file_to_folder("configurations.db", "backup_data", start_time_)
    if vpn_state[0] == "off":
        image = Image.open("icons//interface//power_on.png")
        image = image.resize((64, 64), Image.Resampling.LANCZOS)
        icon = ImageTk.PhotoImage(image)
        label = Label(vpn_win, text=lang["vpn_state_off"], font=("Courier", 15), fg="red", bg=global_bg)
        label.pack()
        region_ = ttk.Combobox(vpn_win, textvariable=var1, values=regions, state="readonly")
        region_.pack()
        btn = Button(vpn_win, image=icon, command=on, bg="#2C3E50", bd=0)
        btn.image = icon  # Важно: сохраняем ссылку, чтобы не удалилось сборщиком мусора
        btn.pack()
    else:
        image = Image.open("icons//interface//power_off.png")
        image = image.resize((64, 64), Image.Resampling.LANCZOS)
        icon = ImageTk.PhotoImage(image)
        label = Label(vpn_win, text=lang["vpn_state_on"], font=("Courier", 15), fg="green", bg=global_bg)
        label.pack()
        label1 = Label(vpn_win, text=lang["region"] + " - " + reg, font=("Courier", 15), fg=global_fg, bg=global_bg)
        label1.pack()
        btn = Button(vpn_win, image=icon, command=off, bg="#2C3E50", bd=0)
        btn.image = icon  # Важно: сохраняем ссылку, чтобы не удалилось сборщиком мусора
        btn.pack()

    conn = sqlite3.connect("configurations.db")
    cursor = conn.cursor()
    cursor.execute('''SELECT COUNT(*) FROM states''')
    row_count = cursor.fetchone()[0]
    if row_count == 0:
        cursor.execute('''INSERT INTO states (vpn, wifi, bluetooth) VALUES (?, ?, ?)''', ("off", "off", "off"))
        conn.commit()
    conn.close()
    if edition in ("Professional x64", "Gaming x64", "Professional x32", "Gaming x32"):
        copy_file_to_folder("configurations.db", "backup_data", start_time_)