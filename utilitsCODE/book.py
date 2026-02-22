import json
from tkinter import *
from tkinter import ttk,messagebox
from PIL import Image, ImageTk

page_num = 1

def load_book(filename, lang_code="RU"):
    with open(filename, "r", encoding="utf-8") as file:
        full_data = json.load(file)

    if lang_code not in full_data:
        raise ValueError(f"Язык {lang_code} не найден в книге")

    return full_data[lang_code]
def get_sorted_pages(book_data):
    sorted_keys = sorted(book_data.keys(), key=lambda x: int(x.replace("page", "")))
    return sorted_keys
def get_page_text(book_data, page_number):
    page_key = f"page{page_number}"
    return book_data.get(page_key, {}).get("text", "[Page not found]")
def bbb(actives_programs, root, lang,start_time_,global_bg,global_fg,GlobalAlpha):
    def read(name):
        def nextt(book):
            global page_num
            page_num += 1
            if page_num > len(pages):
                messagebox.showinfo(lang["books"], lang["bookf"])
                return
            lbl.config(text=get_page_text(book, page_num))
            btn.config(text = lang["nextp"] + f' {page_num+1}')

        page_num = 1
        book = load_book(f"books/{name}.json")
        pages = get_sorted_pages(book)

        w = Toplevel(root)
        w.attributes("-alpha", float(GlobalAlpha))
        w.config(bg=global_bg)
        w.geometry('500x400')
        
        w.title(lang["books"])
        img = Image.open("icons/book.png")
        icon_image = ImageTk.PhotoImage(img)
        w.iconphoto(False, icon_image)

        lbl = Label(w, text=get_page_text(book, page_num), font=('Arial', 14),bg = global_bg,fg = global_fg, wraplength=480)
        lbl.pack(pady=10)

        btn = ttk.Button(w, text=lang["nextp"] + f' {page_num+1}', command=lambda: nextt(book))
        btn.pack(pady=10)

    actives_programs.append("Books launc")

    Win = Toplevel(root)
    Win.attributes("-alpha", float(GlobalAlpha))
    Win.config(bg=global_bg)
    Win.geometry('500x400')
    Win.title(lang["books"])
    img = Image.open("icons/book.png")
    icon_image = ImageTk.PhotoImage(img)
    Win.iconphoto(False, icon_image)

    Label(Win, text=lang["books"], font=('Arial', 16),bg = global_bg,fg = global_fg).pack(pady=10)
    Label(Win, text=lang["cathst"],bg = global_bg,fg = global_fg).pack()
    ttk.Button(Win, text=lang["read"], command=lambda: read("cat_story")).pack(pady=10)
    Label(Win, text=lang["ez"],bg = global_bg,fg = global_fg).pack()
    ttk.Button(Win, text=lang["read"], command=lambda: read("history")).pack(pady=10)




