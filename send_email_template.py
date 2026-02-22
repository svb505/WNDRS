from send_email import send_email
from datetime import datetime
from runinthread import run_in_thread
import sqlite3
from crypto_work import read_encrypted_file
import json

def load_language(lang_code=""):
    with open("syst_comp/lang.json", "r", encoding="utf-8") as file:
        langs = json.load(file)
    if lang_code not in langs:
        return langs["RU"]
    return langs[lang_code]
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
n,ln,email = return_user_info()
def send(type,amount,card_from = None,card_to = None):
    if read_encrypted_file('syst_comp/email_state.cfg') == 'True':
        selected_lang = read_encrypted_file("syst_comp/lang.cfg").strip()
        lang = load_language(selected_lang)

        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if type == "transaction":
            run_in_thread(send_email(
                to=str(email),
                subject=f"🔄 {lang['transaction_det']}",
                html=f"""
                    <html>
                      <body style="font-family: Arial, sans-serif; background-color:#f5f5f5; padding:20px;">
                        <div style="background-color:#ffffff; padding:20px; border-radius:10px; 
                                    box-shadow:0px 2px 6px rgba(0,0,0,0.1); max-width:500px; margin:auto;">
                          <h2 style="color:#333;">🔄 {lang['transaction_f']}</h2>
                          <p style="font-size:16px; color:#555;">
                            {lang['transfer_f']}
                          </p>
                          <div style="background-color:#f9f9f9; padding:15px; border-radius:8px; 
                                      font-size:15px; color:#333; line-height:1.6;">
                            <b>{lang['transfer_sum']}:</b> {amount}$<br>
                            <b>{lang['from_']}:</b> {card_from}<br>
                            <b>{lang['to_']}:</b> {card_to}<br>
                            <b>{lang['d']}:</b> {date}
                          </div>
                          <p style="font-size:14px; color:#888; margin-top:20px;">
                            {lang['keep_conf']}
                          </p>
                        </div>
                      </body>
                    </html>
                    """
            ))
        elif type == "receipt":
            run_in_thread(send_email(
                to=str(email),
                subject=f"💰 {lang['p_received']}",
                html=f"""
                    <html>
                      <body style="font-family: Arial, sans-serif; background-color:#f5f5f5; padding:20px;">
                        <div style="background-color:#ffffff; padding:20px; border-radius:10px; 
                                    box-shadow:0px 2px 6px rgba(0,0,0,0.1); max-width:500px; margin:auto;">
                          <h2 style="color:#007bff;">💰 {lang['you_received']}</h2>
                          <p style="font-size:16px; color:#555;">
                            {lang['new_received']}
                          </p>
                          <div style="background-color:#f9f9f9; padding:15px; border-radius:8px; 
                                      font-size:15px; color:#333; line-height:1.6;">
                            <b>{lang['transfer_sum']}:</b> {amount}$<br>
                            <b>{lang["d"]}:</b> {date}
                          </div>
                          <p style="font-size:14px; color:#888; margin-top:20px;">
                            {lang['funds']}
                          </p>
                        </div>
                      </body>
                    </html>
                    """
            ))
        elif type == 'payement':
            run_in_thread(send_email(
                to=str(email),
                subject=f"✅ {lang['p_conf']}",
                html=f"""
                    <html>
                      <body style="font-family: Arial, sans-serif; background-color:#f5f5f5; padding:20px;">
                        <div style="background-color:#ffffff; padding:20px; border-radius:10px; 
                                    box-shadow:0px 2px 6px rgba(0,0,0,0.1); max-width:500px; margin:auto;">
                          <h2 style="color:#28a745;">✅ {lang['p_successfull']}</h2>
                          <p style="font-size:16px; color:#555;">
                            {lang['p_comp']}:
                          </p>
                          <div style="background-color:#f9f9f9; padding:15px; border-radius:8px; 
                                      font-size:15px; color:#333; line-height:1.6;">
                            <b>{lang['transfer_sum']}:</b> {amount}$<br>
                            <b>{lang['d']}:</b> {date}
                          </div>
                          <p style="font-size:14px; color:#888; margin-top:20px;">
                            {lang['thx_for_p']}
                          </p>
                        </div>
                      </body>
                    </html>
                    """
            ))
