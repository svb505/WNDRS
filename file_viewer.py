from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
from crypto_work import load_key, decrypt_message, encrypt_message

version = "1.4.40"

def read_cfg(path, encrypted=False, mode="r"):
    key = load_key()
    with open(path, "rb" if encrypted else mode) as f:
        data = f.read()
    return decrypt_message(data, key).strip() if encrypted else data.strip()
def write_cfg(path, value, encrypted=False):
    key = load_key()
    data = encrypt_message(value, key) if encrypted else value
    with open(path, "wb" if encrypted else "w") as f:
        f.write(data)

valid_lang = {"RU", "EN", "FR", "UA", "BY","DE","ALB","IT","SRB","ES","PL","PT","CS","BG","HU","TUR","RO","CN","JP"}
valid_colors = {"#2C3E50","red","yellow","green","#808000","#D2691E","#00BFFF","#DAA520","#FF6347","#FF1493","#800080","#FFA500","#00FF00"}
valid_icons = {"icons//acc1.png","icons//acc2.png","icons//acc3.png","icons//acc4.png","icons//acc5.png",
               "icons//acc6.png","icons//acc7.png","icons//acc8.png","icons//accicon.png",}
valid_region = {"netherlans","usa","france","russia","hungry","italia",'australia',"canada"}
valid_size = {"32","42","52","64","76","84"}
valid_p = {1.0,0.9,0.8,0.7,0.6,0.5,0.4,0.3,0.2,0.1,0.0}
valid_shw = {1,0}
valid_theme = {"d","s"}

CONFIG_RULES = {
    "syst_comp/antvrs_state.cfg": {"valid": {"True","False"}, "encrypted": True},
    "syst_comp/auto_upd.cfg": {"valid": {"True","False"}},
    "syst_comp/lang.cfg": {"valid": valid_lang, "encrypted": True},
    "syst_comp/color.cfg": {"valid": valid_colors},
    "syst_comp/icons.cfg": {"valid": valid_icons},
    "syst_comp/size.cfg": {"valid": valid_size},
    "syst_comp/volume.cfg": {"type": "float", "encrypted": True},
    "syst_comp/gamebar_settings/gamebar_theme.cfg": {"valid": valid_theme, "encrypted": True},
    "syst_comp/gamebar_settings/gamebar_p.cfg": {"type": "float", "valid": valid_p, "encrypted": True},
    "syst_comp/mute.cfg": {"valid": {"True","False"}, "encrypted": True},
    "syst_comp/invisible_pass.cfg": {"valid": {"True","False"},"encrypted": True}
}
DEFAULT_VALUES = {
    "syst_comp/antvrs_state.cfg": "True",
    "syst_comp/auto_upd.cfg": "False",
    "syst_comp/lang.cfg": "EN",
    "syst_comp/color.cfg": "#2C3E50",
    "syst_comp/icons.cfg": "icons//acc1.png",
    "syst_comp/size.cfg": "64",
    "syst_comp/volume.cfg": "50.0",
    "syst_comp/gamebar_settings/gamebar_theme.cfg": "d",
    "syst_comp/gamebar_settings/gamebar_p.cfg": "1.0",
    "syst_comp/mute.cfg": "False",
    "syst_comp/invisible_pass.cfg": "True",
}
errors, missing = [], []

for path, rule in CONFIG_RULES.items():
    if not os.path.exists(path):
        missing.append(path)
        continue

    try:
        val = read_cfg(path, encrypted=rule.get("encrypted", False))
        if rule.get("type") == "float":
            val = float(val)
        elif rule.get("type") == "int":
            val = int(val)

        if "valid" in rule and val not in rule["valid"]:
            errors.append(path)
    except Exception as e:
        errors.append(path)

def recover_files(files, mode):
    for path in files:
        rule = CONFIG_RULES.get(path)
        if not rule:
            continue
        default = DEFAULT_VALUES.get(path, "")
        write_cfg(path, str(default), encrypted=rule.get("encrypted", False))
    messagebox.showinfo("Success", f"All {mode} files recovered.")

Win = Tk()
Win.geometry("300x300")
Win.title(f"SVB File Viewer - {version}")
Win.resizable(False, False)
Win.iconphoto(True, ImageTk.PhotoImage(Image.open("icons/fileviewer.png")))

Label(text=f"Version - {version}").pack()

if errors:
    Label(text="Files with incorrect data:", font=("Arial", 15)).pack()
    for f in errors:
        Label(text=f).pack()
    ttk.Button(text="Recover invalid", command=lambda: recover_files(errors, "invalid")).pack()
if missing:
    Label(text="Missing files:", font=("Arial", 15)).pack()
    for f in missing:
        Label(text=f).pack()
    ttk.Button(text="Recover missing", command=lambda: recover_files(missing, "missing")).pack()
if not errors and not missing:
    Label(text="All files are OK", font=("Arial", 15)).pack()

Win.mainloop()
