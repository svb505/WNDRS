from datetime import datetime, timedelta

from crypto_work import read_encrypted_file,write_encrypted_file

def block_user(root,lang):
    try:
        days = int(read_encrypted_file("syst_comp/updation_days.cfg"))
    except:
        days = 1
    unblock_time = datetime.now() + timedelta(days=days)
    write_encrypted_file("syst_comp/control_nxt_date.cfg",
                         unblock_time.strftime("%d-%m-%Y %H:%M:%S"))

    messagebox.showwarning("Time limit", f"{lang['limit!2']} {days} {lang['dn']}.")
    root.destroy()