import sqlite3


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
    else: n = ln = e = "Unknown"
    return n,ln,e