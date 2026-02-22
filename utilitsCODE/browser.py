import logging
import os
import random
from tkinter import *
from tkinter import ttk
from tkhtmlview import HTMLLabel
from PIL import Image, ImageTk
import customtkinter as ctk
from logtofile import log_to_file
from play_sound import play_sound
from copy_file_to_folder import copy_file_to_folder
import wikipedia

SYSTEM_LEVEL = 25
logging.addLevelName(SYSTEM_LEVEL, "SYSTEM")

def open_browser(root,selected_lang,lang,state_sound,volume,errors,edition,start_time_,actives_programs,news_list_,global_bg,global_fg,wifi_state,GlobalAlpha):
    play_sound("sound//click.mp3",volume,state_sound,start_time_)

    def load_wiki(data, html_label):
        wikipedia.set_lang(selected_lang.lower())
        v = data[9:-1]
        try:
            res = wikipedia.summary(v, auto_suggest=False)
        except wikipedia.exceptions.PageError:
            res = "Page not found."
        except wikipedia.exceptions.DisambiguationError as e:
            options = ", ".join(e.options[:5])
            res = f"{lang['much_results']}: {options}"

        html = f"""
            <div style="background: #ffffff; color: #202122; font-family: 'Linux Libertine','Georgia','Times','serif'; max-width: 900px; margin: auto; padding: 20px; line-height: 1.6;">
                <h1 style="font-size: 1.8em; font-weight: normal; border-bottom: 1px solid #a2a9b1; padding-bottom: 0.2em; margin-bottom: 0.5em;">
                    Wikipedia
                </h1>
                <p style="font-size: 0.95em; margin-top: 0.5em;">
                    <b>{res}</b>
                </p>
                <p style="margin-top: 1em; font-size: 0.9em; color: #54595d;">
                    wiki
                </p>
            </div>
        """
        html_label.set_html(html)

    def load_page(url, html_label):
        temp = random.randint(1, 39)
        temp_ = random.randint(1, 39)
        pages = {
            "home": f"""
                   <h1 style="color: steelblue; text-align: center;">{lang["welc_browser"]}</h1>
                   <p style="font-size: 16px; text-align: center;"><b>{lang["fake_br"]}</b></p>
               """,
            "about": f"""
                   <h1 style="color: darkgreen;">{lang["opro"]}</h1>
                   <p style="font-size: 14px;">{lang["svbbrow"]}</p>
               """,
            "help": f"""
                   <h1 style="color: darkred;">{lang["hhelp"]}</h1>
                   <ul style="font-size: 14px;">
                       <li><b>home</b> — {lang["glav"]}</li>
                       <li><b>about</b> — {lang["opro"]}</li>
                       <li><b>news</b> — {lang["nn"]}</li>
                       <li><b>weather</b> — {lang["weat"]}</li>
                       <li><b>faq</b> — {lang["ffaaqq"]}</li>
                   </ul>
               """,
            "news": f"""
                   <h1 style="color: navy;">{lang["nn"]}</h1>
                   <div style="padding: 10px; background-color: #eef; border-left: 4px solid #88c;">
                       <p><b>[03.06.2025]</b> {lang["no_upd"]}</p>
                   </div>
               """,
            "weather": f"""
                   <h1 style="color: dodgerblue;">{lang["weat"]}</h1>
                   <p style="font-size: 18px;">{lang['pog']} +{temp}°C, {lang['pog_st']}</p>
                   <p style="color: gray;">{lang["vech"]}, +{temp_}°C</p>
               """,
            "jokes": f"""
                   <h1 style="color: purple;">{lang["joke"]}</h1>
                   <p style="font-style: italic;">{lang["joke_"]}</p>
               """,
            "settings": f"""
                   <h1 style="color: darkorange;">{lang["br_set"]}</h1>
                   <p>{lang["no_set_br"]}</p>
               """,
            "profile": f"""
                   <h1 style="color: teal;">{lang["us-pr"]}</h1>
                   <p><b>Имя:</b>{lang["gostt"]}<br><b>{lang["rrank"]}:</b> {lang["noob"]}</p>
               """,
            "games": f"""
                   <h1 style="color: indigo;">{lang["games"]}</h1>
                   <ul>
                       <li>🎮 {lang["zmeika"]}</li>
                       <li>🧠 {lang["2048"]}</li>
                       <li>🃏 {lang["pasians"]}</li>
                   </ul>
               """,
            "notepad": f"""
                   <h1 style="color: brown;">{lang["zametki"]}</h1>
                   <p>{lang["no_zam"]}</p>
               """,
            "update": f"""
                   <h1 style="color: green;">{lang["obnov"]}</h1>
                   <p>{lang["lastv"]}</p>
               """,
            "404": f"""
                   <h1 style="color: red; text-align: center;">{lang["error404"]}</h1>
                   <p style="text-align: center;">{lang["pagenof"]}</p>
               """,
            "status": f"""
                   <h1 style="color: darkblue;">{lang["sys_s"]}</h1>
                   <p>{lang["alln"]}</p>
               """,
            "contact": f"""
                   <h1 style="color: darkmagenta;">{lang["contactsb"]}</h1>
                   <p>Email: <a href="#">developpersvbstd22@gmail.com</a></p>
               """,
            "faq": f"""
                   <h1 style="color: gray;">{lang["quist"]}</h1>
                   <ul>
                       <li>{lang["ex"]}</li>
                       <li>{lang["ni"]}</li>
                   </ul>
               """,
            "search": f"""
                   <h1 style="color: darkcyan;">{lang['search_']}</h1>
                   <p>{lang["funcni"]}</p>
               """,
            "music": f"""
                   <h1 style="color: tomato;">{lang["mus_bro"]}</h1>
                   <p>{lang["no_music"]}</p>
               """,
            "terminal": f"""
                   <h1 style="color: black;">{lang["cons"]}</h1>
                   <p style="font-family: monospace;">$ sudo rm -rf /*<br><b>{lang["errord"]}</b></p>
               """,
            "credits": f"""
                   <h1 style="color: olive;">{lang["creators"]}</h1>
                   <p><code>SVB</code> 😎</p>
               """,
            "social": f"""
                   <h1 style="color: #4267B2;">{lang["social"]}</h1>
                   <p>{lang['social_false']}</p>
               """
        }

        html = pages.get(url, pages["404"])
        html_label.set_html(html)
    def search(data, html_label):
        os.makedirs("browser", exist_ok=True)
        if os.path.exists("browser/cookies.cache"):
            try:
                with open("browser/cookies.cache", "a") as file:
                    file.write(f"$search - {data}\n")
                    file.close()
                if edition in ("Professional x64", "Gaming x64", "Professional x32", "Gaming x32"):
                    copy_file_to_folder("brower/cookies.cache", "backup_data",start_time_)
            except:
                pass
        else:
            try:
                with open("browser/cookies.cache", "w") as file:
                    file.write(f"$search - {data}\n")
                    file.close()
                if edition in ("Professional x64", "Gaming x64", "Professional x32", "Gaming x32"):
                    copy_file_to_folder("browser/cookies.cache", "backup_data",start_time_)
            except:
                pass
        for widget in win.winfo_children():
            if isinstance(widget, HTMLLabel):
                widget.destroy()
        if data.strip().lower().startswith("wiki -q"):
            load_wiki(data,html_label)
        else:
            load_page(en_search.get().strip().lower(), html_label)

        if edition in ("Professional x64", "Gaming x64", "Professional x32", "Gaming x32"):
            copy_file_to_folder("browser/cookies.cache", "backup_data",start_time_)
            log_to_file('Cookiesd copied',start_time_)

    actives_programs.append("Browser")
    log_to_file("Browser launch",start_time_)
    win = Toplevel(root)
    win.attributes("-alpha", float(GlobalAlpha))
    win.title(lang["browser"])
    win.config(bg=global_bg)
    img = Image.open("icons/browser.png")
    icon_image = ImageTk.PhotoImage(img)
    win.iconphoto(False, icon_image)
    win.geometry("900x900")
    commands = ["home", f'wiki -q "{lang["quest"]}"',"about", "help", "news", "weather", "jokes", "settings", "profile",
                "games", "notepad", "update", "status", "contact", "faq", "search", "music",
                "terminal", "credits", "social"]
    if wifi_state:
        frame_search = Frame(win, bg=global_bg)
        frame_search.pack(pady=5, fill=X, padx=20)

        lab1 = Label(frame_search, text=lang["enter_query"], fg=global_fg, bg=global_bg, font=("Arial", 12, "bold"))
        lab1.pack(side=LEFT, padx=5)

        en_search = ctk.CTkEntry(frame_search, width=50,placeholder_text = lang['enter_zapr'])
        en_search.pack(side=RIGHT, fill=X, expand=True)
        html_label = HTMLLabel(win, html="")
        html_label.pack(fill=BOTH, expand=True, padx=10, pady=10)

        btn = ttk.Button(win, text=lang["search"], style="TButton", command=lambda: search(en_search.get(), html_label))
        btn.pack(pady=10)

        news_frame = LabelFrame(win, text=lang["news"], font=("Arial", 12, "bold"), bg=global_bg, padx=10, pady=5)
        news_frame.pack(pady=10, padx=20, side=LEFT)
        frame1 = LabelFrame(win, text=lang["dost_c"], font=("Arial", 12, "bold"), bg=global_bg, padx=10, pady=5)
        frame1.pack(pady=10, padx=20, side=RIGHT)

        scrollbar = Scrollbar(news_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        news_list = Listbox(news_frame, yscrollcommand=scrollbar.set, font=("Arial", 11), height=10)
        news_list.pack(fill=X, expand=True)
        scrollbar.config(command=news_list.yview)

        for n in news_list_:
            log_to_file(f"News {n} loaded",start_time_)
            news_list.insert(END, str(n))
        scrollbar1 = Scrollbar(frame1)
        scrollbar1.pack(side=RIGHT, fill=Y)
        l = Listbox(frame1, yscrollcommand=scrollbar1.set)
        l.pack(fill=X, expand=True)
        scrollbar1.config(command=l.yview)

        for c in commands:
            l.insert(END, str(c))

    else:
        log_to_file('No internet connection',start_time_)
        win.config(bg="white")
        lbl = Label(win, text=lang["no_internet"] + "!", fg='red', font=("Courier", 31, "bold"))
        lbl.pack()

        image = Image.open(
            "icons//interface//nowificonn.png")
        image = image.resize((300, 300))
        photo = ImageTk.PhotoImage(image)

        label = Label(win, image=photo)
        label.image = photo
        label.pack()
    win.mainloop()
