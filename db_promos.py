import sqlite3
import random
promos = [
            "4GRKPK30", "7643DF3RF", "431TGV", "45G2F", "5GT41", "F3RCRZA", "T1FFD1", "F31C313", "81G3DB9XH",
            "P1RO3MOC1", "EXTRA2025", "SAVE4NOW", "WINNER77", "LUCKYME99", "PROMO2025", "DEALTIME22",
            "FREECODE1",
            "HOLIDAY88", "VIPBONUS7", "NEWYEAR25", "MAYSALE55", "GETREWARD", "MYPROMO33", "SPRINGFUN",
            "HELLOBONUS",
            "GIFTCODEX", "WELCOMESV", "SVB1000G", "TRYAGAIN7", "MEGABOOST", "HAPPYHOUR", "FASTREWARD",
            "UNLOCK50X",
            "SPEEDYWIN", "REDEEM2025", "TOPPROMO", "CASH4YOU", "OPENSESAME", "NICEDEAL", "CODE777", "KEY2WIN",
            "FREEENTRY", "BIGLUCK25", "DAILYTREASURE", "MYDAILYCODE", "PRIZEHUNT1", "GET50NOW", "POWERBONUS",
            "GAMETIME77", "LUCKYTICKET", "SVBGIFT", "NEXTPROMO", "WELCOME777", "HIDDENPRIZE", "PROMOMAGIC",
            "LOVECODE"
        ]

conn = sqlite3.connect("prm_c.db")
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS all_promos (codes TEXT UNIQUE)""")
conn.commit()
for i in range(200):
    pas = "".join("".join(random.choices('0123456789ABCDEFGHIJKLMNOPQRSTUVWYZ', k=2)) for _ in range(6))
    cursor.execute("INSERT INTO all_promos (codes) VALUES(?)",(pas,))
    conn.commit()
