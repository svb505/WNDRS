import sqlite3
from save_and_load_balance import load_balance, save_balance
from server_statistick import update_file
from transactions import transactions

def check_ach(svb_coins,start_time_,lang):
    svb_coins = load_balance(start_time_)

    conn = sqlite3.connect("achievements.db")
    cursor = conn.cursor()

    cursor.execute("SELECT name, status, max, prize FROM achievements")
    rows = cursor.fetchall()

    for name, status, max_val, prize in rows:
        if status == "no" and svb_coins >= max_val:
            svb_coins += int(prize)
            transactions(f"-{prize} SVB Coins", start_time_)
            update_file("count_svbcoins.txt", int(prize))
            save_balance(svb_coins, start_time_)
            cursor.execute(
                "UPDATE achievements SET current = ?, status = ? WHERE name = ?",
                (svb_coins, "yes", name)
            )
            conn.commit()
            messagebox.showinfo(lang["success"], lang["ach_tr"] + str(prize))

    conn.close()