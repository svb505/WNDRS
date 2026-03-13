import os
import sqlite3
from logtofile import log_system


def initialize_db():
    conn = sqlite3.connect("configurations.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS states (
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        vpn TEXT,
                        wifi TEXT,
                        bluetooth TEXT
                    )''')

    cursor.execute('''SELECT COUNT(*) FROM states''')
    row_count = cursor.fetchone()[0]
    if row_count == 0:
        cursor.execute('''INSERT INTO states (vpn, wifi, bluetooth) VALUES (?, ?, ?)''', ("off", "off", "off"))
        conn.commit()

    conn.close()
def create_database(start_time_):
    log_system('CREATE "CONFIGURATIONS.DB"', start_time_)
    if not os.path.exists('configurations.db'):
        log_system('DB not EXIST', start_time_)
        conn = sqlite3.connect('configurations.db')
        cursor = conn.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS inventory (
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          name TEXT NOT NULL,
                          rarity TEXT NOT NULL)''')

        conn.commit()
        conn.close()
        log_system("DB Created", start_time_)
    else:
        conn = sqlite3.connect('configurations.db')
        cursor = conn.cursor()
        log_system("Connect to configurations.db", start_time_)
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='inventory';")
        table_exists = cursor.fetchone()
        if not table_exists:
            cursor.execute('''CREATE TABLE inventory (
                              id INTEGER PRIMARY KEY AUTOINCREMENT,
                              name TEXT NOT NULL,
                              rarity TEXT NOT NULL)''')
            conn.commit()
        conn.close()
