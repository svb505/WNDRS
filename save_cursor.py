import sqlite3
from logtofile import log_to_file

def save_cursor(cursor_name,start_time_):
    log_to_file('Save cursor,start_time_ = start_time_', start_time_=start_time_)
    conn = sqlite3.connect("configurations.db")
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS cursor_table (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        cursor_name TEXT
                      )''')

    cursor.execute("DELETE FROM cursor_table")
    cursor.execute("INSERT INTO cursor_table (cursor_name) VALUES (?)", (cursor_name,))
    conn.commit()
    conn.close()

    log_to_file(f"Cursor {cursor_name} saved", start_time_=start_time_)