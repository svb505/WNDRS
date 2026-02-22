import re
from tkinter import *
import threading
from tkinter import ttk,messagebox
import requests
import subprocess
import time
from PIL import Image, ImageTk
from datetime import datetime
import os
from logtofile import log_to_file

def internet_log(msg):
    if os.path.exists("syst_comp/internet_logs.cfg"):
        with open("syst_comp/internet_logs.cfg","a") as f:
            f.write(f"{msg}\n")
    else:
        with open("syst_comp/internet_logs.cfg","w") as f:
            f.write(f"{msg}\n")


def speedtest(root,lang,actives_programs,start_time_,global_bg,global_fg,GlobalAlpha):
    actives_programs.append("SVB SpeedTest")
    def get_ping(host="google.com"):
        try:
            result = subprocess.run(["ping", "-n", "1", host], capture_output=True, text=True)
            output = result.stdout

            # Ищем "время=123мс" или "time=123ms"
            match = re.search(r"(время|time)[=< ]+(\d+)", output)
            if match:
                return match.group(2)
            return "N/A"
        except Exception as e:
            messagebox.showerror(lang["error"],f"{lang['ping_error']}:{e}",parent=Win)
            log_to_file(f"Ping error:{e}",start_time_,level="error")
            return lang["error"]
    def download_speed_test():
        try:
            url = "http://ipv4.download.thinkbroadband.com/10MB.zip"
            start_time = time.time()
            r = requests.get(url, stream=True, timeout=10)
            total_length = 0
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    total_length += len(chunk)
            end_time = time.time()
            duration = end_time - start_time
            speed_mbps = (total_length * 8) / (duration * 1024 * 1024)
            return speed_mbps
        except Exception as e:
            messagebox.showerror(lang["error"], f"{lang['down_error']}:{e}",parent=Win)
            log_to_file(f"Download error:{e}", start_time_, level="error")
            return 0
    def upload_speed_test():
        try:
            data = b"x" * 5_000_000  # 5MB
            start_time = time.time()
            r = requests.post("https://httpbin.org/post", data=data, timeout=10)
            end_time = time.time()
            duration = end_time - start_time
            speed_mbps = (len(data) * 8) / (duration * 1024 * 1024)
            return speed_mbps
        except Exception as e:
            messagebox.showerror(lang["error"], f"{lang['send_error']}:{e}",parent=Win)
            log_to_file(f"Send error:{e}", start_time_, level="error")
            return 0
    def run_test():
        btn_start.config(state=DISABLED)
        lbl_status.config(text=lang["pls_wait"])

        def test():
            # Пинг
            ping = get_ping()
            if ping.isdigit():
                if int(ping) < 100:
                    lbl_ping_val.config(text=f"{ping} {lang['ms']}", fg="green")
                elif int(ping) > 100 and ping < 350:
                    lbl_ping_val.config(text=f"{ping} {lang['ms']}", fg="orange")
                else:
                    lbl_ping_val.config(text=f"{ping} {lang['ms']}", fg="red")

            # Загрузка
            download = download_speed_test()
            if int(download) < 10:
                lbl_download_val.config(text=f"{download:.2f} {lang['mbit']}",fg = "red")
            elif int(download) > 10 and download < 25:
                lbl_download_val.config(text=f"{download:.2f} {lang['mbit']}",fg = "orange")
            else:
                lbl_download_val.config(text=f"{download:.2f} {lang['mbit']}",fg = "green")

            # Отдача
            upload = upload_speed_test()
            if int(upload) < 10:
                lbl_download_val.config(text=f"{upload:.2f} {lang['mbit']}",fg = "red")
            elif int(upload) > 10 and download < 25:
                lbl_download_val.config(text=f"{upload:.2f} {lang['mbit']}",fg = "orange")
            else:
                lbl_download_val.config(text=f"{upload:.2f} {lang['mbit']}",fg = "green")

            lbl_status.config(text=lang["gotovo"])
            btn_start.config(state=NORMAL)
            timestamp = datetime.today().strftime("%Y-%m-%d_%H-%M-%S")
            internet_log(f'TIME:{timestamp}')
            internet_log(f'PING:{ping}')
            internet_log(f'DOWNLOAD:{download}')
            internet_log(f'UPLOAD:{upload}')
        threading.Thread(target=test).start()

    Win = Toplevel(root)
    Win.attributes("-alpha",float(GlobalAlpha))
    Win.title("SVB SpeedTest")
    Win.geometry("400x260")
    Win.resizable(False, False)
    img = Image.open("icons/interface/speed.png")
    icon_image = ImageTk.PhotoImage(img)
    Win.iconphoto(False, icon_image)
    Win.attributes("-topmost",True)

    Label(Win, text=lang['izm_skor'], font=("Arial", 14, "bold"),bg=global_bg,fg=global_fg).pack(pady=10)
    btn_start = ttk.Button(Win, text=lang["start_prover"], command=run_test)
    btn_start.pack(pady=5)
    lbl_status = Label(Win, text=lang['waiting'], font=("Arial", 10, "italic"),bg=global_bg,fg=global_fg)
    lbl_status.pack()

    frame = Frame(Win,bg=global_bg)
    frame.pack(pady=10)

    Label(frame, text=lang['ping'], font=("Arial", 12),bg=global_bg,fg=global_fg).grid(row=0, column=0, sticky=W, padx=5)
    lbl_ping_val = Label(frame, text="--", font=("Arial", 12, "bold"),bg=global_bg,fg=global_fg)
    lbl_ping_val.grid(row=0, column=1, padx=5)

    Label(frame, text=lang['down_speed'], font=("Arial", 12),bg=global_bg,fg=global_fg).grid(row=1, column=0, sticky=W, padx=5)
    lbl_download_val = Label(frame, text="--", font=("Arial", 12, "bold"),bg=global_bg,fg=global_fg)
    lbl_download_val.grid(row=1, column=1, padx=5)

    Label(frame, text=lang['upl_speed'], font=("Arial", 12),bg=global_bg,fg=global_fg).grid(row=2, column=0, sticky=W, padx=5)
    lbl_upload_val = Label(frame, text="--", font=("Arial", 12, "bold"),bg=global_bg,fg=global_fg)
    lbl_upload_val.grid(row=2, column=1, padx=5)

