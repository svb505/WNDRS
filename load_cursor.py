import sqlite3
from logtofile import log_system

def load_cursor(start_time_):
    log_system("Load cursor", start_time_)
    conn = sqlite3.connect("configurations.db")
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS cursor_table (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        cursor_name TEXT
                      )''')

    cursor.execute("SELECT cursor_name FROM cursor_table LIMIT 1")
    result = cursor.fetchone()
    conn.close()

    return result[0] if result else "arrow"