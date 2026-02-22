from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
from PIL import Image, ImageTk
from send_email import send_email
from logtofile import log_to_file
from transactions import transactions
from save_and_load_balance import save_balance,load_balance

svb_coins = 0

def add_tooltip(widget, text):
    tooltip = None
    def enter(event):
        nonlocal tooltip
        tooltip = Toplevel(widget)
        tooltip.wm_overrideredirect(True)
        x = event.x_root + 10
        y = event.y_root + 10
        tooltip.geometry(f"+{x}+{y}")
        label = Label(tooltip, text=text, bg="#fcfcfa")
        label.pack()
    def leave(event):
        nonlocal tooltip
        if tooltip:
            tooltip.destroy()
            tooltip = None
    widget.bind("<Enter>", enter)
    widget.bind("<Leave>", leave)
def send_delivery(lang, title, image):
    conn = sqlite3.connect("configurations.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            first_name TEXT,
            last_name TEXT,
            email TEXT
        )
    """)
    cur.execute("SELECT email FROM users LIMIT 1")
    row = cur.fetchone()
    conn.close()

    email = row[0] if row else "unknown@mail.com"

    send_email(
        to=email,
        subject=lang["deliv"],
        html=f"""
        <html>
        <body style="font-family:Arial;text-align:center">
            <h2>{title}</h2>
            <img src="{image}" width="400">
        </body>
        </html>
        """
    )
def pay_and_send(pizza, menu, winn, lang, start_time_):
    global svb_coins

    svb_coins = load_balance(start_time_)

    if svb_coins < 400:
        messagebox.showerror(lang["error"], lang["no_svb"], parent=winn)
        return

    svb_coins -= 400
    save_balance(svb_coins,start_time_)
    transactions(f"-400 SVb Coins {datetime.now()}", start_time_)
    log_to_file(f"User paid: {pizza}", start_time_=start_time_)

    key, image = menu[pizza]
    send_delivery(lang, lang[key], image)
    messagebox.showinfo(lang["success"], lang["yes_dos"])
def open_menu(win,title, lang,items, menu, global_bg, global_fg, alpha, start_time_):
    winn = Toplevel(win)
    winn.geometry("750x550")
    winn.title(title)
    winn.config(bg=global_bg)
    winn.attributes("-alpha", float(alpha))
    winn.resizable(False, False)

    frames = [Frame(winn, bg=global_bg) for _ in range(3)]
    for f in frames:
        f.pack(side="left", padx=20, pady=20)

    winn.images = []

    for i, item in enumerate(items):
        frame = frames[i // 4]

        img = ImageTk.PhotoImage(
            Image.open(item["icon"]).resize((52, 52), Image.Resampling.LANCZOS)
        )
        winn.images.append(img)

        Label(frame, image=img, bg=global_bg).pack()
        Label(frame, text=lang[item["lang"]], bg=global_bg, fg=global_fg).pack()

        ttk.Button(frame,text=lang["pay_piz"],command=lambda k=item["key"]:pay_and_send(k, menu, winn, lang, start_time_)).pack()

SAND_MENU = {
    "items": [
        {"key": "pes", "lang": "sand1", "icon": "icons/dost/sand1.png"},
        {"key": "bulkabum", "lang": "sand2", "icon": "icons/dost/sand2.png"},
        {"key": "sos", "lang": "sand3", "icon": "icons/dost/sand3.png"},
        {"key": "dogster", "lang": "sand4", "icon": "icons/dost/sand4.png"},
        {"key": "ame", "lang": "sand5", "icon": "icons/dost/sand5.png"},
        {"key": "kol", "lang": "sand6", "icon": "icons/dost/sand6.png"},
        {"key": "pes1", "lang": "sand7", "icon": "icons/dost/sand7.png"},
        {"key": "bulka_roc", "lang": "sand8", "icon": "icons/dost/sand8.png"},
        {"key": "chili", "lang": "sand9", "icon": "icons/dost/sand9.png"},
        {"key": "bbq", "lang": "sand10", "icon": "icons/dost/sand10.png"},
        {"key": "slivv", "lang": "sand11", "icon": "icons/dost/sand11.png"},
        {"key": "gr_b", "lang": "sand12", "icon": "icons/dost/sand12.png"},
    ],
    "map": {
        "pes": ("sand1", "https://i.imgur.com/N7o15Qf.png"),
        "bulkabum": ("sand2", "https://i.imgur.com/E0mkgYg.png"),
        "sos": ("sand3", "https://i.imgur.com/tMcxw2t.png"),
        "dogster": ("sand4", "https://i.imgur.com/bXYjzgz.png"),
        "ame": ("sand5", "https://i.imgur.com/s13vRJE.png"),
        "kol": ("sand6", "https://i.imgur.com/4sBVVTE.png"),
        "pes1": ("sand7", "https://i.imgur.com/6yprpIG.png"),
        "bulka_roc": ("sand8", "https://i.imgur.com/Do8ICzF.png"),
        "chili": ("sand9", "https://i.imgur.com/TMzNH2L.png"),
        "bbq": ("sand10", "https://i.imgur.com/7hYDIEH.png"),
        "slivv": ("sand11", "https://i.imgur.com/h48qh1h.png"),
        "gr_b": ("sand12", "https://i.imgur.com/yzs9mn9.png"),
    }
}
ICE_MENU = {
    "items": [
        {"key": "pes", "lang": "ice1", "icon": "icons/dost/ice1.png"},
        {"key": "bulkabum", "lang": "ice2", "icon": "icons/dost/ice2.png"},
        {"key": "sos", "lang": "ice3", "icon": "icons/dost/ice3.png"},
        {"key": "dogster", "lang": "ice4", "icon": "icons/dost/ice4.png"},
        {"key": "ame", "lang": "ice5", "icon": "icons/dost/ice5.png"},
        {"key": "kol", "lang": "ice6", "icon": "icons/dost/ice6.png"},
        {"key": "pes1", "lang": "ice7", "icon": "icons/dost/ice7.png"},
        {"key": "bulka_roc", "lang": "ice8", "icon": "icons/dost/ice8.png"},
        {"key": "chili", "lang": "ice9", "icon": "icons/dost/ice9.png"},
        {"key": "bbq", "lang": "ice10", "icon": "icons/dost/ice10.png"},
        {"key": "slivv", "lang": "ice11", "icon": "icons/dost/ice11.png"},
        {"key": "gr_b", "lang": "ice12", "icon": "icons/dost/ice12.png"},
    ],
    "map": {
        "pes": ("ice1", "https://i.imgur.com/SsgVfeG.png"),
        "bulkabum": ("ice2", "https://i.imgur.com/esdjAfu.png"),
        "sos": ("ice3", "https://i.imgur.com/SYozQOV.png"),
        "dogster": ("ice4", "https://i.imgur.com/miukyMn.png"),
        "ame": ("ice5", "https://i.imgur.com/abXixRm.png"),
        "kol": ("ice6", "https://i.imgur.com/A0GkBi2.png"),
        "pes1": ("ice7", "https://i.imgur.com/TyeP6eU.png"),
        "bulka_roc": ("ice8", "https://i.imgur.com/fHT3Q1n.png"),
        "chili": ("ice9", "https://i.imgur.com/0r6HHV3.png"),
        "bbq": ("ice10", "https://i.imgur.com/Bb9q8Ou.png"),
        "slivv": ("ice11", "https://i.imgur.com/ZihT3oh.png"),
        "gr_b": ("ice12", "https://i.imgur.com/y4x5Z3z.png"),
    }
}
SUSHI_MENU = {
    "items": [
        {"key": "sakura", "lang": "sakura", "icon": "icons/dost/sushi4.png"},
        {"key": "tokio", "lang": "tokio", "icon": "icons/dost/sushi1.png"},
        {"key": "samurai", "lang": "sam", "icon": "icons/dost/sushi3.png"},
        {"key": "uramaki", "lang": "uramaki", "icon": "icons/dost/sushi6.png"},
        {"key": "hirosima", "lang": "hirosima", "icon": "icons/dost/sushi7.png"},
        {"key": "nagasaki", "lang": "nagasaki", "icon": "icons/dost/sushi2.png"},
        {"key": "sakura_roll", "lang": "sakura_roll", "icon": "icons/dost/roll1.png"},
        {"key": "morsk", "lang": "morsk", "icon": "icons/dost/morsk.png"},
        {"key": "ohdra", "lang": "ohdra", "icon": "icons/dost/ohdra.png"},
        {"key": "phila", "lang": "phila", "icon": "icons/dost/phila.png"},
        {"key": "ocean", "lang": "oceanroll", "icon": "icons/dost/oceanroll.png"},
        {"key": "yapon", "lang": "yapon", "icon": "icons/dost/yap.png"},
    ],
    "map": {
        "sakura": ("sakura", "https://i.imgur.com/Q1VfFFH.png"),
        "tokio": ("tokio", "https://i.imgur.com/MaJKrNc.png"),
        "samurai": ("sam", "https://i.imgur.com/6aWS4nW.png"),
        "uramaki": ("uramaki", "https://i.imgur.com/UHFnuPS.png"),
        "hirosima": ("hirosima", "https://i.imgur.com/56Iz7XD.png"),
        "nagasaki": ("nagasaki", "https://i.imgur.com/7pP6LQS.png"),
        "sakura_roll": ("sakura_roll", "https://i.imgur.com/ZKUYNYO.png"),
        "morsk": ("morsk", "https://i.imgur.com/NRIq8ff.png"),
        "ohdra": ("ohdra", "https://i.imgur.com/TVIX8m5.png"),
        "phila": ("phila", "https://i.imgur.com/2KkbM9J.png"),
        "ocean": ("oceanroll", "https://i.imgur.com/YfiyFCx.png"),
        "yapon": ("yapon", "https://i.imgur.com/Ngfr9lA.png"),
    }
}
PIZZA_MENU = {
    "items": [
        {"key": "salami", "lang": "salami", "icon": "icons/dost/pizza12.png"},
        {"key": "pepperoni", "lang": "pep", "icon": "icons/dost/pizza8.png"},
        {"key": "cheese", "lang": "che", "icon": "icons/dost/pizza5.png"},
        {"key": "italian", "lang": "italian", "icon": "icons/dost/pizza3.png"},
        {"key": "grec", "lang": "grec", "icon": "icons/dost/pizza6.png"},
        {"key": "veg", "lang": "veg", "icon": "icons/dost/pizza4.png"},
        {"key": "rim", "lang": "rim", "icon": "icons/dost/pizza1.png"},
        {"key": "gav", "lang": "gav", "icon": "icons/dost/pizza7.png"},
        {"key": "sea", "lang": "sea", "icon": "icons/dost/pizza2.png"},
        {"key": "mar", "lang": "mar", "icon": "icons/dost/pizza11.png"},
        {"key": "chelentano", "lang": "chelentano", "icon": "icons/dost/pizza9.png"},
        {"key": "bol", "lang": "bol", "icon": "icons/dost/pizza13.png"},
    ],
    "map": {
        "salami": ("salami", "https://i.imgur.com/PTX9n1I.png"),
        "pepperoni": ("pep", "https://i.imgur.com/6RwTjSw.png"),
        "cheese": ("che", "https://i.imgur.com/RjAjztg.png"),
        "italian": ("italian", "https://i.imgur.com/k4dLGlo.png"),
        "grec": ("grec", "https://i.imgur.com/rbkT8iA.png"),
        "veg": ("veg", "https://i.imgur.com/QKAXb9U.png"),
        "rim": ("rim", "https://i.imgur.com/AXPAFlY.png"),
        "gav": ("gav", "https://i.imgur.com/alrCBsK.png"),
        "sea": ("sea", "https://i.imgur.com/vSWNRnT.png"),
        "mar": ("mar", "https://i.imgur.com/6kBzo15.png"),
        "chelentano": ("chelentano", "https://i.imgur.com/iJ18P7a.png"),
        "bol": ("bol", "https://i.imgur.com/l4wRS2c.png"),
    }
}
SUP_MENU = {
    "items": [
        {"key": "pes", "lang": "sup1", "icon": "icons/dost/sup1.png"},
        {"key": "bulkabum", "lang": "sup2", "icon": "icons/dost/sup2.png"},
        {"key": "sos", "lang": "sup3", "icon": "icons/dost/sup3.png"},
        {"key": "dogster", "lang": "sup4", "icon": "icons/dost/sup4.png"},
        {"key": "ame", "lang": "sup5", "icon": "icons/dost/sup5.png"},
        {"key": "kol", "lang": "sup6", "icon": "icons/dost/sup6.png"},
        {"key": "pes1", "lang": "sup7", "icon": "icons/dost/sup7.png"},
        {"key": "bulka_roc", "lang": "sup8", "icon": "icons/dost/sup8.png"},
        {"key": "chili", "lang": "sup9", "icon": "icons/dost/sup9.png"},
        {"key": "bbq", "lang": "sup10", "icon": "icons/dost/sup10.png"},
        {"key": "slivv", "lang": "sup11", "icon": "icons/dost/sup11.png"},
        {"key": "other", "lang": "sup12", "icon": "icons/dost/sup12.png"},
    ],
    "map": {
        "pes": ("sup1", "https://i.imgur.com/Fyk4zQ7.png"),
        "bulkabum": ("sup2", "https://i.imgur.com/LizjksI.png"),
        "sos": ("sup3", "https://i.imgur.com/YAudAO1.png"),
        "dogster": ("sup4", "https://i.imgur.com/19QW7pn.png"),
        "ame": ("sup5", "https://i.imgur.com/7wEtUOi.png"),
        "kol": ("sup6", "https://i.imgur.com/f3NBYyU.png"),
        "pes1": ("sup7", "https://i.imgur.com/a7gDoit.png"),
        "bulka_roc": ("sup8", "https://i.imgur.com/q4EINVz.png"),
        "chili": ("sup9", "https://i.imgur.com/7GbYdE3.png"),
        "bbq": ("sup10", "https://i.imgur.com/80sAIvt.png"),
        "slivv": ("sup11", "https://i.imgur.com/tFighqf.png"),
        "other": ("sup12", "https://i.imgur.com/cQe8Ik6.png"),
    }
}
PON_MENU = {
    "items": [
        {"key": "pes", "lang": "pon1", "icon": "icons/dost/pon1.png"},
        {"key": "bulkabum", "lang": "pon2", "icon": "icons/dost/pon2.png"},
        {"key": "sos", "lang": "pon3", "icon": "icons/dost/pon3.png"},
        {"key": "dogster", "lang": "pon4", "icon": "icons/dost/pon4.png"},
        {"key": "ame", "lang": "pon5", "icon": "icons/dost/pon5.png"},
        {"key": "kol", "lang": "pon6", "icon": "icons/dost/pon6.png"},
        {"key": "pes1", "lang": "pon7", "icon": "icons/dost/pon7.png"},
        {"key": "bulka_roc", "lang": "pon8", "icon": "icons/dost/pon8.png"},
        {"key": "chili", "lang": "pon9", "icon": "icons/dost/pon9.png"},
        {"key": "bbq", "lang": "pon10", "icon": "icons/dost/pon10.png"},
        {"key": "slivv", "lang": "pon11", "icon": "icons/dost/pon11.png"},
        {"key": "other", "lang": "pon12", "icon": "icons/dost/pon12.png"},
    ],
    "map": {
        "pes": ("pon1", "https://i.imgur.com/spwxwJi.png"),
        "bulkabum": ("pon2", "https://i.imgur.com/Mb0AfG0.png"),
        "sos": ("pon3", "https://i.imgur.com/adryiFa.png"),
        "dogster": ("pon4", "https://i.imgur.com/tSzOuBA.png"),
        "ame": ("pon5", "https://i.imgur.com/cKCJqIN.png"),
        "kol": ("pon6", "https://i.imgur.com/f44egqa.png"),
        "pes1": ("pon7", "https://i.imgur.com/5xzXu2j.png"),
        "bulka_roc": ("pon8", "https://i.imgur.com/0OGlinr.png"),
        "chili": ("pon9", "https://i.imgur.com/6PebIeT.png"),
        "bbq": ("pon10", "https://i.imgur.com/0psqRUd.png"),
        "slivv": ("pon11", "https://i.imgur.com/DvBEJJy.png"),
        "other": ("pon12", "https://i.imgur.com/6aTNiR6.png"),
    }
}
BREAK_MENU = {
    "items": [
        {"key": "ya", "lang": "ya", "icon": "icons/dost/ya.png"},
        {"key": "ya_t", "lang": "ya_t", "icon": "icons/dost/ya_t.png"},
        {"key": "oml", "lang": "oml", "icon": "icons/dost/oml.png"},
        {"key": "musl", "lang": "musl", "icon": "icons/dost/musl.png"},
        {"key": "ya_b", "lang": "ya_b", "icon": "icons/dost/ya_b.png"},
        {"key": "cr", "lang": "cr", "icon": "icons/dost/cr.png"},
        {"key": "ovs", "lang": "ovs", "icon": "icons/dost/ovs.png"},
        {"key": "sl", "lang": "sl", "icon": "icons/dost/sloyka.png"},
        {"key": "pir", "lang": "pir", "icon": "icons/dost/pir.png"},
        {"key": "pud", "lang": "pud", "icon": "icons/dost/pudding.png"},
        {"key": "tost", "lang": "tost", "icon": "icons/dost/toast.png"},
        {"key": "gr", "lang": "gr", "icon": "icons/dost/gr.png"},
    ],
    "map": {
        "ya": ("ya", "https://i.imgur.com/dapyuV6.png"),
        "ya_t": ("ya_t", "https://i.imgur.com/8iYSaQ7.png"),
        "oml": ("oml", "https://i.imgur.com/ouH0uqY.png"),
        "musl": ("musl", "https://i.imgur.com/ouH0uqY.png"),
        "ya_b": ("ya_b", "https://i.imgur.com/Nf09vqq.png"),
        "cr": ("cr", "https://i.imgur.com/yvU44tX.png"),
        "ovs": ("ovs", "https://i.imgur.com/NmBluOj.png"),
        "sl": ("sl", "https://i.imgur.com/08gK50l.png"),
        "pir": ("pir", "https://i.imgur.com/DZajGuz.png"),
        "pud": ("pud", "https://i.imgur.com/KxA1Vt0.png"),
        "tost": ("tost", "https://i.imgur.com/dIAHK8H.png"),
        "gr": ("gr", "https://i.imgur.com/j4MBwL8.png"),
    }
}
PANK_MENU = {
    "items": [
        {"key": "kl", "lang": "kl", "icon": "icons/dost/kl.png"},
        {"key": "klen", "lang": "klen", "icon": "icons/dost/klen.png"},
        {"key": "yag", "lang": "yag", "icon": "icons/dost/yag.png"},
        {"key": "blin1", "lang": "blin1", "icon": "icons/dost/blin1.png"},
        {"key": "blin2", "lang": "blin2", "icon": "icons/dost/blin2.png"},
        {"key": "blin3", "lang": "blin3", "icon": "icons/dost/blin3.png"},
        {"key": "blin4", "lang": "blin4", "icon": "icons/dost/blin4.png"},
        {"key": "blin5", "lang": "blin5", "icon": "icons/dost/blin5.png"},
        {"key": "blin6", "lang": "blin6", "icon": "icons/dost/blin6.png"},
        {"key": "blin7", "lang": "blin7", "icon": "icons/dost/blin7.png"},
        {"key": "blin8", "lang": "blin8", "icon": "icons/dost/blin8.png"},
        {"key": "nut", "lang": "nut", "icon": "icons/dost/nut.png"},
    ],
    "map": {
        "kl": ("kl", "https://i.imgur.com/iMo6seF.png"),
        "klen": ("klen", "https://i.imgur.com/VHTBlAo.png"),
        "yag": ("yag", "https://i.imgur.com/lKEukM7.png"),
        "blin1": ("blin1", "https://i.imgur.com/Da4E0Hm.png"),
        "blin2": ("blin2", "https://i.imgur.com/0dstu5j.png"),
        "blin3": ("blin3", "https://i.imgur.com/XBpkQWc.png"),
        "blin4": ("blin4", "https://i.imgur.com/HIVKvmr.png"),
        "blin5": ("blin5", "https://i.imgur.com/CqZnJc7.png"),
        "blin6": ("blin6", "https://i.imgur.com/P81mu27.png"),
        "blin7": ("blin7", "https://i.imgur.com/n4uC1C9.png"),
        "blin8": ("blin8", "https://i.imgur.com/XSd4Olc.png"),
        "nut": ("nut", "https://i.imgur.com/9nz0Bvp.png"),
    }
}
FASTFOOD_MENU = {
    "items": [
        {"key": "free", "lang": "free", "icon": "icons/dost/free.png"},
        {"key": "nug", "lang": "nug", "icon": "icons/dost/nug.png"},
        {"key": "nog", "lang": "nog", "icon": "icons/dost/nog.png"},
        {"key": "ring", "lang": "ring", "icon": "icons/dost/ring.png"},
        {"key": "1myas", "lang": "1myas", "icon": "icons/dost/1myas.png"},
        {"key": "2myas", "lang": "2myas", "icon": "icons/dost/2myas.png"},
        {"key": "tacofi", "lang": "tacofi", "icon": "icons/dost/tacofi.png"},
        {"key": "tacomi", "lang": "tacomi", "icon": "icons/dost/tacomi.png"},
        {"key": "bur", "lang": "bur", "icon": "icons/dost/bur.png"},
        {"key": "keb", "lang": "keb", "icon": "icons/dost/keb.png"},
        {"key": "che_", "lang": "che_", "icon": "icons/dost/che.png"},
        {"key": "krl", "lang": "krl", "icon": "icons/dost/krl.png"},
    ],
    "map": {
        "free": ("free", "https://i.imgur.com/s9M0GXD.png"),
        "nug": ("nug", "https://i.imgur.com/ad4Cuz0.png"),
        "nog": ("nog", "https://i.imgur.com/WQd8p2d.png"),
        "ring": ("ring", "https://i.imgur.com/ixjiFKB.png"),
        "1myas": ("1myas", "https://i.imgur.com/egxqbe0.png"),
        "2myas": ("2myas", "https://i.imgur.com/vVlSBfQ.png"),
        "tacofi": ("tacofi", "https://i.imgur.com/XCRTMg5.png"),
        "tacomi": ("tacomi", "https://i.imgur.com/NFwIAhb.png"),
        "bur": ("bur", "https://i.imgur.com/ADayzcx.png"),
        "keb": ("keb", "https://i.imgur.com/4Mt0XnJ.png"),
        "che_": ("che_", "https://i.imgur.com/henGMSZ.png"),
        "krl": ("krl", "https://i.imgur.com/rDJaH8h.png"),
    }
}
HOTDOG_MENU = {
    "items": [
        {"key": "pes", "lang": "pes", "icon": "icons/dost/sosiskin.png"},
        {"key": "bulkabum", "lang": "bulkabum", "icon": "icons/dost/bulkabum.png"},
        {"key": "sos", "lang": "sos", "icon": "icons/dost/ame.png"},
        {"key": "dogster", "lang": "dogster", "icon": "icons/dost/pes.png"},
        {"key": "ame", "lang": "ame", "icon": "icons/dost/dogster.png"},
        {"key": "kol", "lang": "kol", "icon": "icons/dost/kolb.png"},
        {"key": "pes1", "lang": "pes1", "icon": "icons/dost/pes1.png"},
        {"key": "bulka_roc", "lang": "bulka_roc", "icon": "icons/dost/bulk.png"},
        {"key": "chili", "lang": "chili", "icon": "icons/dost/chili.png"},
        {"key": "bbq", "lang": "bbq", "icon": "icons/dost/bbq.png"},
        {"key": "slivv", "lang": "slivv", "icon": "icons/dost/slivv.png"},
        {"key": "gr_b", "lang": "gr_b", "icon": "icons/dost/gr_b.png"},
    ],
    "map": {
        "pes": ("pes", "https://i.imgur.com/GbEmDTx.png"),
        "bulkabum": ("bulkabum", "https://i.imgur.com/MHKKxiY.png"),
        "sos": ("sos", "https://i.imgur.com/OVaVaPi.png"),
        "dogster": ("dogster", "https://i.imgur.com/jrTC5x8.png"),
        "ame": ("ame", "https://i.imgur.com/BUNvrMo.png"),
        "kol": ("kol", "https://i.imgur.com/Ft2EaKx.png"),
        "pes1": ("pes1", "https://i.imgur.com/aTm1Boc.png"),
        "bulka_roc": ("bulka_roc", "https://i.imgur.com/rrONWPp.png"),
        "chili": ("chili", "https://i.imgur.com/42K7E23.png"),
        "bbq": ("bbq", "https://i.imgur.com/McpHQX8.png"),
        "slivv": ("slivv", "https://i.imgur.com/XcX9Jy4.png"),
        "gr_b": ("gr_b", "https://i.imgur.com/cyeL8KI.png"),
    }
}
SALAD_MENU = {
    "items": [
        {"key": "ceesar", "lang": "ceesar", "icon": "icons/dost/caessar.png"},
        {"key": "ol", "lang": "ol", "icon": "icons/dost/ol.png"},
        {"key": "grec", "lang": "grec_", "icon": "icons/dost/grec.png"},
        {"key": "zelen", "lang": "zelen", "icon": "icons/dost/zelen.png"},
        {"key": "azi", "lang": "azi", "icon": "icons/dost/azi.png"},
        {"key": "sred", "lang": "sred", "icon": "icons/dost/sred.png"},
        {"key": "tsar", "lang": "tsar", "icon": "icons/dost/tsar.png"},
        {"key": "kra", "lang": "kra", "icon": "icons/dost/kra.png"},
        {"key": "sred2", "lang": "sred2", "icon": "icons/dost/sred2.png"},
        {"key": "vol", "lang": "vol", "icon": "icons/dost/vol.png"},
        {"key": "bli", "lang": "bli", "icon": "icons/dost/bli.png"},
        {"key": "fre", "lang": "fre", "icon": "icons/dost/fre.png"},
    ],
    "map": {
        "ceesar": ("ceesar", "https://i.imgur.com/WUmdLIW.png"),
        "ol": ("ol", "https://i.imgur.com/XzovZuq.png"),
        "grec": ("grec_", "https://i.imgur.com/UVj7dqn.png"),
        "zelen": ("zelen", "https://i.imgur.com/lE6JcLb.png"),
        "azi": ("azi", "https://i.imgur.com/SEXU0kI.png"),
        "sred": ("sred", "https://i.imgur.com/EbDnCFB.png"),
        "tsar": ("tsar", "https://i.imgur.com/loGHMhY.png"),
        "kra": ("kra", "https://i.imgur.com/Kmndezi.png"),
        "sred2": ("sred2", "https://i.imgur.com/LrTfgW8.png"),
        "vol": ("vol", "https://i.imgur.com/CWL1Kye.png"),
        "bli": ("bli", "https://i.imgur.com/Vqq39Xf.png"),
        "fre": ("fre", "https://i.imgur.com/aBItivd.png"),
    }
}
BURGER_MENU = {
    "items": [
        {"key": "cheese_udar", "lang": "cheese_udar", "icon": "icons/dost/burger5.png"},
        {"key": "chicken_boom", "lang": "chicken_boom", "icon": "icons/dost/burger3.png"},
        {"key": "myaso", "lang": "myaso", "icon": "icons/dost/burger4.png"},
        {"key": "becon", "lang": "becon", "icon": "icons/dost/burger2.png"},
        {"key": "cheese", "lang": "cheeseburger", "icon": "icons/dost/cheeseburger.png"},
        {"key": "wopper", "lang": "wopper", "icon": "icons/dost/wopper.png"},
        {"key": "ost", "lang": "ost", "icon": "icons/dost/ost.png"},
        {"key": "veggy", "lang": "veggy", "icon": "icons/dost/veggy.png"},
        {"key": "grillboss", "lang": "grillboss", "icon": "icons/dost/grillboss.png"},
        {"key": "chicken_bus", "lang": "chicken_bus", "icon": "icons/dost/chicken_bust.png"},
        {"key": "grillmania", "lang": "grillmania", "icon": "icons/dost/grillmania.png"},
        {"key": "hamburger", "lang": "hamburger", "icon": "icons/dost/hamburger.png"},
    ],
    "map": {
        "cheese_udar": ("cheese_udar", "https://i.imgur.com/jcDh840.png"),
        "chicken_boom": ("chicken_boom", "https://i.imgur.com/TQJdN7I.png"),
        "myaso": ("myaso", "https://i.imgur.com/AQLCNwG.png"),
        "becon": ("becon", "https://i.imgur.com/xiDWvd6.png"),
        "cheese": ("cheeseburger", "https://i.imgur.com/bgf3F8w.png"),
        "wopper": ("wopper", "https://i.imgur.com/xiDWvd6.png"),
        "ost": ("ost", "https://i.imgur.com/bgf3F8w.png"),
        "veggy": ("veggy", "https://i.imgur.com/BEdwzbc.png"),
        "grillboss": ("grillboss", "https://i.imgur.com/w1E59RX.png"),
        "chicken_bus": ("chicken_bus", "https://i.imgur.com/snwZ0d7.png"),
        "grillmania": ("grillmania", "https://i.imgur.com/wlPZFVJ.png"),
        "hamburger": ("hamburger", "https://i.imgur.com/j4ZN8W8.png"),
    }
}
LAPSHA_MENU = {
    "items": [
        {"key": "udon", "lang": "udon", "icon": "icons/dost/pasta1.png"},
        {"key": "fire_ramen", "lang": "fire_ramen", "icon": "icons/dost/pasta2.png"},
        {"key": "dracon", "lang": "dracon", "icon": "icons/dost/pasta3.png"},
        {"key": "imperator", "lang": "imperator", "icon": "icons/dost/ramen3.png"},
        {"key": "naruto", "lang": "naruto", "icon": "icons/dost/ramen1.png"},
        {"key": "yamato", "lang": "yamato", "icon": "icons/dost/ramen4.png"},
        {"key": "yamakudi", "lang": "yamakudi", "icon": "icons/dost/ramen2.png"},
    ],
    "map": {
        "udon": ("udon", "https://i.imgur.com/EFCMFF2.png"),
        "fire_ramen": ("fire_ramen", "https://i.imgur.com/ZQWT535.png"),
        "dracon": ("dracon", "https://i.imgur.com/hgbIVeq.png"),
        "imperator": ("imperator", "https://i.imgur.com/JLm6awX.png"),
        "naruto": ("naruto", "https://i.imgur.com/NjawRrO.png"),
        "yamato": ("yamato", "https://i.imgur.com/H5AcrAf.png"),
        "yamakudi": ("yamakudi", "https://i.imgur.com/0ZtaUrp.png"),
    }
}
DESERT_MENU = {
    "items": [
        {"key": "choco1", "lang": "choco1", "icon": "icons/dost/cake1.png"},
        {"key": "strawberry", "lang": "strawberry", "icon": "icons/dost/cake2.png"},
        {"key": "strawberry1", "lang": "strawberry1", "icon": "icons/dost/cake4.png"},
        {"key": "cupkake", "lang": "cupcake", "icon": "icons/dost/cupcake1.png"},
        {"key": "icecr", "lang": "icecr", "icon": "icons/dost/icecream1.png"},
        {"key": "vafl", "lang": "vafl", "icon": "icons/dost/waffle.png"},
        {"key": "pon", "lang": "pon", "icon": "icons/dost/donut1.png"},
        {"key": "tir", "lang": "tir", "icon": "icons/dost/dessert1.png"},
        {"key": "polos", "lang": "polos", "icon": "icons/dost/dessert3.png"},
        {"key": "cook", "lang": "cook", "icon": "icons/dost/cookies1.png"},
        {"key": "med", "lang": "med", "icon": "icons/dost/honey.png"},
        {"key": "jele", "lang": "jele", "icon": "icons/dost/jelly1.png"},
    ],
    "map": {
        "choco1": ("choco1", "https://i.imgur.com/pi1zhSy.png"),
        "strawberry": ("strawberry", "https://i.imgur.com/ygqJljc.png"),
        "strawberry1": ("strawberry1", "https://i.imgur.com/UO5hh3y.png"),
        "cupkake": ("cupcake", "https://i.imgur.com/NENmCfn.png"),
        "icecr": ("icecr", "https://i.imgur.com/oEyiKCv.png"),
        "vafl": ("vafl", "https://i.imgur.com/fYtSdDy.png"),
        "pon": ("pon", "https://i.imgur.com/1XmuhEy.png"),
        "tir": ("tir", "https://i.imgur.com/ZjeANR2.png"),
        "polos": ("polos", "https://i.imgur.com/Yr4AMkP.png"),
        "cook": ("cook", "https://i.imgur.com/rs88GCQ.png"),
        "med": ("med", "https://i.imgur.com/wZYMddJ.png"),
        "jele": ("jele", "https://i.imgur.com/IdiaHVF.png"),
    }
}
SODA_MENU = {
    "items": [
        {"key": "cocacola", "lang": "colaP", "icon": "icons/dost/cola.png"},
        {"key": "pepsi", "lang": "pepsi", "icon": "icons/dost/icons8-pepsi-24.png"},
        {"key": "fanta", "lang": "fanta", "icon": "icons/dost/icons8-fanta-24.png"},
        {"key": "jus", "lang": "jus", "icon": "icons/dost/orangeJ.png"},
        {"key": "cofe", "lang": "cofe", "icon": "icons/dost/coffe.png"},
        {"key": "tea", "lang": "tea", "icon": "icons/dost/tea1.png"},
        {"key": "cacao", "lang": "cacao", "icon": "icons/dost/cacao1.png"},
        {"key": "vine", "lang": "vine", "icon": "icons/dost/vine.png"},
        {"key": "beer", "lang": "beer", "icon": "icons/dost/beer.png"},
        {"key": "water", "lang": "water", "icon": "icons/dost/mineralw.png"},
        {"key": "kokt1", "lang": "kokt1", "icon": "icons/dost/milkshake1.png"},
        {"key": "kokt", "lang": "kokt", "icon": "icons/dost/milkshake2.png"},
    ],
    "map": {
        "cocacola": ("Cucacula", "https://i.imgur.com/mfN6Nrb.png"),
        "pepsi": ("Bebsi", "https://i.imgur.com/SxmUIuR.png"),
        "fanta": ("Funta", "https://i.imgur.com/M0zkNyA.png"),
        "jus": ("jus", "https://i.imgur.com/syuYW9N.png"),
        "cofe": ("cofe", "https://i.imgur.com/ABpbAdQ.png"),
        "tea": ("tea", "https://i.imgur.com/4IFU6DY.png"),
        "cacao": ("cacao", "https://i.imgur.com/rI3tkX0.png"),
        "vine": ("vine", "https://i.imgur.com/FyaWjbk.png"),
        "beer": ("beer", "https://i.imgur.com/xpeA1i3.png"),
        "water": ("water", "https://i.imgur.com/uYnsRon.png"),
        "kokt1": ("kokt1", "https://i.imgur.com/DaVEcco.png"),
        "kokt": ("kokt", "https://i.imgur.com/3QZyOTx.png"),
    }
}

def delivery(root,lang,actives_programs,start_time_,global_bg,global_fg,alpha):
    actives_programs.append("Delivery")

    win = Toplevel(root)
    win.attributes("-alpha", float(alpha))
    win.geometry("750x500")
    win.config(bg=global_bg)
    win.title(lang["deliv"])
    img = Image.open("icons/delivery.png")
    icon_image = ImageTk.PhotoImage(img)
    win.iconphoto(False, icon_image)
    win.resizable(False, False)

    win.piza_img = ImageTk.PhotoImage(Image.open('icons/dost/pizza10.png').resize((79, 79), Image.Resampling.LANCZOS))
    win.roll_img = ImageTk.PhotoImage(Image.open('icons/dost/sushi5.png').resize((79, 79), Image.Resampling.LANCZOS))
    win.burg_img = ImageTk.PhotoImage(Image.open('icons/dost/burger1.png').resize((79, 79), Image.Resampling.LANCZOS))
    win.lap_img = ImageTk.PhotoImage(Image.open('icons/dost/pasta4.png').resize((79, 79), Image.Resampling.LANCZOS))
    win.des_img = ImageTk.PhotoImage(Image.open('icons/dost/dessert2.png').resize((79, 79), Image.Resampling.LANCZOS))
    win.soda_img = ImageTk.PhotoImage(Image.open('icons/dost/drinks.png').resize((79, 79), Image.Resampling.LANCZOS))
    win.salad_img = ImageTk.PhotoImage(Image.open('icons/dost/grec.png').resize((79, 79), Image.Resampling.LANCZOS))
    win.fast_img = ImageTk.PhotoImage(Image.open('icons/dost/free.png').resize((79, 79), Image.Resampling.LANCZOS))
    win.hot_img = ImageTk.PhotoImage(Image.open('icons/dost/bulk.png').resize((79, 79), Image.Resampling.LANCZOS))
    win.pank_img = ImageTk.PhotoImage(Image.open('icons/dost/klen.png').resize((79, 79), Image.Resampling.LANCZOS))
    win.break_f_img = ImageTk.PhotoImage(Image.open('icons/dost/ya_t.png').resize((79, 79), Image.Resampling.LANCZOS))
    win.ice = ImageTk.PhotoImage(Image.open('icons/dost/ice1.png').resize((79, 79), Image.Resampling.LANCZOS))
    win.sand = ImageTk.PhotoImage(Image.open('icons/dost/sand1.png').resize((79, 79), Image.Resampling.LANCZOS))
    win.sup = ImageTk.PhotoImage(Image.open('icons/dost/sup1.png').resize((79, 79), Image.Resampling.LANCZOS))
    win.pon = ImageTk.PhotoImage(Image.open('icons/dost/pon1.png').resize((79, 79), Image.Resampling.LANCZOS))

    left_frame = Frame(win, bg=global_bg)
    right_frame = Frame(win, bg=global_bg)
    right_frame1 = Frame(win, bg=global_bg)
    right_frame2 = Frame(win, bg=global_bg)
    right_frame3 = Frame(win, bg=global_bg)

    left_frame.pack(side="left", anchor="n", padx=20, pady=20)
    right_frame.pack(side="left", anchor="n", padx=20, pady=20)
    right_frame1.pack(side="left", anchor="n", padx=20, pady=20)
    right_frame2.pack(side="left", anchor="n", padx=20, pady=20)
    right_frame3.pack(side="left", anchor="n", padx=20, pady=20)

    images = [win.piza_img,win.roll_img,win.burg_img,win.lap_img,win.des_img,win.soda_img,win.salad_img,win.fast_img,
              win.hot_img,win.pank_img,win.break_f_img,win.ice,win.sand,win.sup,win.pon]
    menus = [PIZZA_MENU,SUSHI_MENU,BURGER_MENU,LAPSHA_MENU,DESERT_MENU,SODA_MENU,SALAD_MENU,FASTFOOD_MENU,HOTDOG_MENU,
             PANK_MENU,BREAK_MENU,ICE_MENU,SAND_MENU,SUP_MENU,PON_MENU]
    tooltips = [lang["tool_piza"],lang["tool_suchi"],lang["tool_burger"],lang["tool_lap"],lang["tool_des"],lang["tool_soda"],
                lang["tool_salad"],lang["tool_fast"],lang["tool_hotdog"],lang["tool_pank"],lang["tool_break_f"],
                lang["tool_ice"],lang["tool_sand"],lang["tool_sup"],lang["tool_pon"]]

    for i,(img,men,toolt) in enumerate(zip(images,menus,tooltips)):
        frm = ''
        if i <= 4:
            frm = left_frame
        elif i > 4 and i <= 8:
            frm = right_frame1
        elif i > 8 and i <= 12:
            frm = right_frame2
        elif i > 12 and i <= 16:
            frm = right_frame3

        btn = Button(frm, image=img,
               command=lambda m = men:open_menu(win,lang["deliv"],lang,m["items"],m["map"],global_bg,global_fg,alpha,start_time_))
        btn.pack()
        add_tooltip(btn, toolt)


