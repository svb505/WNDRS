from tkinter import *
from tkinter import ttk
from logtofile import log_to_file
from PIL import Image, ImageTk
import json
import os
import threading

def os_diagn_win(root,lang,global_bg,global_fg,start_time_,actives_programs,GlobalAlpha):
    def start_diagn():
        log_to_file("Start diagnost",start_time_)
        def prover_json(filepath, text_widget, progressbar, lang, base_lang="RU"):
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError) as e:
                text_widget.insert(END, f"{lang['json_error']}: {e}\n", "red")
                return

            def count_keys(obj):
                if isinstance(obj, dict):
                    return len(obj) + sum(count_keys(v) for v in obj.values())
                elif isinstance(obj, list):
                    return sum(count_keys(item) for item in obj)
                return 0

            total_keys = count_keys(data)
            progressbar["maximum"] = total_keys
            progressbar["value"] = total_keys

            text_widget.insert(END, f"{lang['json_total_keys']}: {total_keys}\n")

            # --- сравниваем ключи (как во 2 варианте) ---
            base_dict = data.get(base_lang, {})
            base_keys = set(base_dict.keys())

            for current_lang, translations in data.items():
                if current_lang == base_lang:
                    continue

                current_keys = set(translations.keys())

                # отсутствующие ключи
                missing_in_lang = base_keys - current_keys
                for key in missing_in_lang:
                    text_widget.insert(
                        END,
                        f'{lang["in"]} {current_lang} {lang["nehvat"]}: {key} ["{key}": "{base_dict[key]}"]\n',
                        "red"
                    )

                # лишние ключи
                extra_in_lang = current_keys - base_keys
                for key in extra_in_lang:
                    text_widget.insert(
                        END,
                        f'{lang["in"]} {current_lang} {lang["lichn_kl"]}: {key} ["{key}": "{translations[key]}"]\n',
                        "blue"
                    )

            text_widget.insert(END, f"{lang['json_prover_fin']}\n")
        def prover_sysfiles(text):
            log_to_file("Diagnost files", start_time_)
            files = ["syst_comp/auto_upd.cfg",'syst_comp/color.cfg','syst_comp/lang.cfg',"syst_comp/lang.json",
                     "syst_comp/format_clk.cfg","syst_comp/icons.cfg","syst_comp/img_wlp.cfg",
                     "syst_comp/log_set.cfg","syst_comp/path_wlp.cfg","syst_comp/mute.cfg","syst_comp/plc_sys.cfg",
                     "syst_comp/programs.cfg","syst_comp/size.cfg","syst_comp/user_v.cfg",'syst_comp/valids/vld_l.cfg',"syst_comp/license.bin",
                     'syst_comp/valids/vld_c.cfg',"syst_comp/valids/vld_icons.cfg","syst_comp/valids/vld_wlp.cfg","syst_comp/valids/vld_path_wlp.cfg",
                     "syst_comp/volume.cfg","syst_comp/syst.key","syst_comp/taskbar_config.json",
                     "syst_comp/transactions_hst.cache","syst_comp/","syst_comp/gamebar_settings/gamebar_p.cfg",
                     "syst_comp/gamebar_settings/gamebar_shw_inf.cfg",'syst_comp/gamebar_settings/settings.json',
                     "syst_comp/gamebar_settings/gamebar_theme.cfg",'versions/current_version.txt','versions/uefiver.txt',
                     "uefi.exe","updater.exe","configurations.db","achievements.db","DLLs/trashbin.dll","DLLs/libatomic-1.dll",
                        "DLLs/libgomp-1.dll","DLLs/libgcc_s_seh-1.dll","DLLs/liblzma.dll","DLLs/libssp-0.dll",
                     "DLLs/zlibd1.dll","DLLs/libwinpthread-1.dll","DLLs/LoadFiles.dll","DLLs/libstdc++-6.dll","DLLs/ValidateImgHashe.dll",
                     "DLLs/vcruntime140.dll","DLLs/vcruntime140_1.dll","DLLs/VCRUNTIME140D.dll",
                     ]
            for f in files:
                if os.path.exists(f):
                    text.insert(END, f"{f} - {lang['file_exxist']}\n", "green")
                else:
                    text.insert(END, f"{f} - {lang['file_notexxist']}\n", "red")
                W.update_idletasks()  # обновляем GUI
        W = Toplevel(Win)
        W.attributes('-alpha',float(GlobalAlpha))
        W.title(lang['os_diagnost'])
        W.geometry('900x600')
        img = Image.open("icons/interface/diagn.png")
        icon_image = ImageTk.PhotoImage(img)
        W.iconphoto(False, icon_image)
        W.config(bg = global_bg)
        osv = ""
        uefiv = ""
        with open("versions/current_version.txt",'r') as f:
            osv = f.read()
        with open("versions/uefiver.txt",'r') as f:
            uefiv = f.read()
        os_ver_lbl = Label(W, text='', bg=global_bg, fg=global_fg)
        os_ver_lbl.pack()
        uefi_ver_lbl = Label(W, text='', bg=global_bg, fg=global_fg)
        uefi_ver_lbl.pack()

        frame1 = Frame(W)
        frame1.pack(fill=BOTH, expand=True)
        text_w = Text(frame1, height=10)
        text_w.pack(side=LEFT, fill=BOTH, expand=True)
        scrollw = Scrollbar(frame1, orient=VERTICAL, command=text_w.yview)
        scrollw.pack(side=RIGHT, fill=Y)
        text_w.config(yscrollcommand=scrollw.set)
        json_progress = ttk.Progressbar(W, orient="horizontal", mode="determinate", length=400)
        json_progress.pack(pady=5)
        frame2 = Frame(W)
        frame2.pack(fill=BOTH, expand=True)
        text = Text(frame2, height=10)
        text.pack(side=LEFT, fill=BOTH, expand=True)
        scroll = Scrollbar(frame2, orient=VERTICAL, command=text.yview)
        scroll.pack(side=RIGHT, fill=Y)
        text.config(yscrollcommand=scroll.set)
        # Настройка цветов для text
        text.tag_config("red", foreground="red")
        text.tag_config("black", foreground="black")

        os_ver_lbl.config(text = f"{lang['osver']} - {osv}")
        uefi_ver_lbl.config(text=f"{lang['uefiver']} - {uefiv}")
        threading.Thread(target=lambda: prover_json("syst_comp/lang.json", text_w, json_progress, lang),
                         daemon=True).start()
        threading.Thread(target=lambda: prover_sysfiles(text), daemon=True).start()
    actives_programs.append("OS Diagnost")
    Win = Toplevel(root)
    Win.attributes('-alpha',float(GlobalAlpha))
    Win.config(bg = global_bg)
    Win.geometry('500x400')
    Win.title(lang['os_diagnost'])
    img = Image.open("icons/interface/diagn.png")
    icon_image = ImageTk.PhotoImage(img)
    Win.iconphoto(False, icon_image)

    Label(Win,text = lang["os_diagnost"],bg = global_bg,fg = global_fg).pack()
    runbtn = ttk.Button(Win,text = lang["start_diang?"],command = start_diagn)
    runbtn.pack()
