from tkinter import *
from tkinter import ttk
import json
from tkinterweb import HtmlFrame
from PIL import Image, ImageTk
from crypto_work import write_encrypted_file

with open("versions/current_version.txt",'r') as f:
    vers = f.read()
def win_changelogs(root,selected_lang,l,file = None):
    def set_sh(var):
        if var:
            write_encrypted_file("syst_comp/showed.cfg", 'True')
        else:
            write_encrypted_file("syst_comp/showed.cfg", 'False')
    lang = selected_lang
    if file == None:
        with open(f"changelogs/changelog_{vers}.json", "r", encoding="utf-8") as f:
            data = json.load(f)[lang]
    else:
        with open(f"changelogs/{file}", "r", encoding="utf-8") as f:
            data = json.load(f)[lang]
    icons = {
        "added": "icons/interface/plus.png",
        "changed": "icons/interface/change.png",
        "fixed": "icons/interface/fix.png"
    }

    html_content = f"""
    <html>
    <head>
    <style>
    body {{ font-family: Arial, sans-serif; padding: 15px; background: #1e1e1e; color: #ddd; }}
    h2 {{ color: #4ea6f5; }}
    ul {{ list-style-type: none; padding-left: 0; }}
    li {{ margin: 10px 0; font-size: 14px; }}
    .change-block img {{ width: 20px; height: 20px; vertical-align: middle; margin-right: 8px; }}
    .added {{ color: #4CAF50; }}
    .changed {{ color: #FF9800; }}
    .fixed {{ color: #F44336; }}
    .footer {{ margin-top: 20px; font-style: italic; color: #aaa; }}
    </style>
    </head>
    <body>
    <h2>{data['title']}</h2>
    <ul>
    """
    for change in data["changes"]:
        ctype = change["type"]
        text = change["text"]
        icon = icons.get(ctype, "")
        html_content += f"""
        <li class='change-block {ctype}'>
            <img src="{icon}"/> {text}
        </li>
        """
    html_content += f"""
    </ul>
    <p class="footer">{data['footer']}</p>
    </body>
    </html>
    """

    Win = Toplevel(root)
    Win.title("Changelog")
    Win.geometry("600x700")
    img = Image.open("icons/interface/changelogs.png")
    icon_image = ImageTk.PhotoImage(img)
    Win.iconphoto(False, icon_image)
    Win.resizable(False,False)

    frame = HtmlFrame(Win, horizontal_scrollbar="auto")
    frame.pack(fill="both", expand=True)

    var = BooleanVar(value = True)
    check = ttk.Checkbutton(Win,text = l["nepokaz"],variable = var,onvalue = True,offvalue=False,
                            command = lambda:set_sh(var.get()))
    check.pack()
    set_sh(var.get())
    frame.load_html(html_content)

