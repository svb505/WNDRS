import sqlite3
import os
from crypto_work import load_key,encrypt_message,decrypt_message

VIRUSES_MAINS_PATHS = ["syst_comp/sh.dat","syst_comp/t00r.dat","syst_comp/001.dat"]
VIRUS_CURRENT_PATHS = ""


def get_user_info():
    key = load_key()
    user_data,card_infos,cars,trade,svbtube = [],[],[],[],[]
    secret,parametrs,license,passport,state_acc,user_key,user_passwords = "","","",'',"","",""

    conn = sqlite3.connect("configurations.db")
    cursor = conn.cursor()

    data1 = cursor.execute("SELECT * FROM users").fetchall()
    data2 = cursor.execute("SELECT * FROM user_settings").fetchall()
    user_data = [data1[0][1], data1[0][2], data1[0][3],data2[0][1]]
    conn.close()
    with open("syst_comp/syst.key",encoding='utf-8') as f:
        secret = f.read()
    with open("syst_comp/parametrs.bin",encoding='utf-8') as f:
        parametrs = decrypt_message(f.read(),key)
    with open("syst_comp/license.bin",encoding='utf-8') as f:
        license = decrypt_message(f.read(),key)
    if os.path.exists("card.db"):
        conn = sqlite3.connect("card.db")
        cursor = conn.cursor()
        data3 = cursor.execute("SELECT * FROM card_info").fetchall()
        for row in data3:
            card_infos.append({"name":row[0],'num':row[1],"cvv":row[2],"date":row[3]})
    else:
        cards_infos = ["NONE"]
    if os.path.exists("plate.cfg"):
        with open("plate.cfg",encoding='utf-8') as f:
            cars = f.read()
    else:
        cars = ["NONE"]
    if os.path.exists("trade/portfolio.cfg"):
        with open("trade/portfolio.cfg",encoding='utf-8') as f:
           trade = f.read()
    else:
        trade = ["NONE"]
    if os.path.exists("svbtube/account.db"):
        conn = sqlite3.connect("svbtube/account.db")
        cursor = conn.cursor()
        data4 = cursor.execute("SELECT * FROM account").fetchall()
        for row in data4:
            svbtube.append(row[0])
    else:
        svbtube = "NONE"
    if os.path.exists('state/passport.cfg'):
        with open("state/passport.cfg",encoding='utf-8') as f:
            passport = f.read()
    else:
        passport = "NONE"
    if os.path.exists('state/acc.cfg'):
        with open("state/acc.cfg",encoding='utf-8') as f:
            state_acc = f.read()
    else:
        state_acc = "NONE"
    if os.path.exists("passmanager/user_key.cfg"):
        with open("passmanager/user_key.cfg") as f:
            user_key = decrypt_message(f.read(),key)
    else:
        user_key = "NONE"
    if os.path.exists("passmanager/passwords.cfg"):
        with open("passmanager/passwords.cfg") as f:
            user_passwords = decrypt_message(f.read(),key)
    else:
        user_passwords = "NONE"
    return user_data,card_infos,cars,trade,svbtube,secret,parametrs,license,passport,state_acc,user_key,user_passwords
def shpion():
    all_data = [get_user_info()]
    single_entry = all_data[0]
    data_for_save = ''
    for i, item in enumerate(single_entry):
        if i+1 == 1:
            string = '---ACCOUNT---'
            data_for_save += f"{string}\n{item}\n"
        if i+1 == 2:
            string = '---CARDS---'
            data_for_save += f"{string}\n{item}\n"
        if i+1 == 3:
            string = '---PLATES---'
            data_for_save += f"{string}\n{item}\n"
        if i+1 == 4:
            string = '---TRADE---'
            data_for_save += f"{string}\n{item}\n"
        if i+1 == 5:
            string = '---SVBTUBE---'
            data_for_save += f"{string}\n{item}\n"
        if i+1 == 6:
            string = '---KEY---'
            data_for_save += f"{string}\n{item}\n"
        if i+1 == 7:
            string = '---PARAMETRS---'
            data_for_save += f"{string}\n{item}\n"
        if i+1 == 8:
            string = '---LICENSE---'
            data_for_save += f"{string}\n{item}\n"
        if i+1 == 9:
            string = '---PASSPORT---'
            data_for_save += f"{string}\n{item}\n"
        if i+1 == 10:
            string = '---STATE ACCOUNT---'
            data_for_save += f"{string}\n{item}\n"
        if i+1 == 11:
            string = '---PS_MANAGER KEY---'
            data_for_save += f"{string}\n{item}\n"
        if i+1 == 12:
            string = '---PASSWORDS---'
            data_for_save += f"{string}\n{item}\n"

    print(data_for_save)
    with open(VIRUSES_MAINS_PATHS[1],"wb") as f:
        key = load_key()
        f.write(encrypt_message(data_for_save,key))
def delete_sys():
    paths = ["syst_comp/color.cfg","syst_comp/format_clk.cfg","syst_comp/lang.cfg","syst_comp/size.cfg","syst_comp/volume.cfg",
             "syst_comp/img_wlp.cfg","syst_comp/icons.cfg","syst_comp/valids/vld_icons.cfg","syst_comp/path_wlp.cfg","syst_comp/plc_sys.cfg",
             "syst_comp/plc_clk.cfg",
             "syst_comp/programs.cfg","syst_comp/taskbar_config.json","syst_comp/valids/vld_l.cfg","syst_comp/valids/vld_c.cfg"]
    for path in paths:
        if os.path.exists(path):
            os.remove(path)
