import sqlite3
from logtofile import log_to_file


def read_inventory_from_db(start_time_,lang):
    log_to_file("READ INVENTORY", start_time_=start_time_)
    conn = sqlite3.connect('configurations.db')
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM inventory WHERE name = ?", (lang["theme_"],))
    result_nebo = cursor.fetchone()
    cursor.execute("SELECT name FROM inventory WHERE name = ?", (lang["galaxy"],))
    result_galaxy = cursor.fetchone()
    cursor.execute("SELECT name FROM inventory WHERE name = ?", (lang["galaxy_"],))
    result_galaxy_ = cursor.fetchone()
    nebo = result_nebo is not None
    galaxy = result_galaxy is not None
    galaxy_ = result_galaxy_ is not None
    conn.close()

    return galaxy, nebo, galaxy_