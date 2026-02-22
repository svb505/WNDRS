import sqlite3



def create():
    conn = sqlite3.connect("my_os_production/achievements.db")
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE if NOT EXISTS achievements(
        name TEXT,
        status TEXT,
        max INTEGER,
        current INTEGER,
        prize INTEGER
    )""")
    conn.commit()
    conn.close()

def insert():
    conn = sqlite3.connect("my_os_production/achievements.db")
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO achievements (name,status,max,current,prize) VALUES(?,?,?,?,?)""",("million","no",1000000,0,200000,))
    cursor.execute("""INSERT INTO achievements (name,status,max,current,prize) VALUES(?,?,?,?,?)""",
                   ("500tis", "no", 500000, 0,100000,))
    conn.commit()
insert()