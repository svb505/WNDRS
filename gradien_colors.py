import os
import sqlite3
from logtofile import log_to_file

def load_gradient_colors(start_time_):
    if not os.path.exists("configurations.db"): return None, None
    try:
        conn = sqlite3.connect("configurations.db")
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS gradients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                      start_color TEXT NOT NULL,
                                      end_color TEXT NOT NULL)''')

        conn.commit()
        cursor.execute("SELECT start_color, end_color FROM gradients ORDER BY id DESC LIMIT 1")
        row = cursor.fetchone()
        conn.close()

        return row if row else (None, None)
    except Exception as e:
        log_to_file(f"Error loading gradient colors: {e}", level="error", start_time_=start_time_)
        return None, None