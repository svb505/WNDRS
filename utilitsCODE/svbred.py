from tkinter import *
from tkinter import font, filedialog, colorchooser, simpledialog, ttk
import json
from PIL import Image, ImageTk
import os
from create_window import create_window

os.makedirs("MyTextFiles", exist_ok=True)
SAVE_DIR = os.path.join(os.getcwd(), "MyTextFiles")
os.makedirs(SAVE_DIR, exist_ok=True)  # Создать если не существует
tooltip = None

def show_tooltip(event, txt):
    global tooltip
    if tooltip:
        return

    x = event.widget.winfo_rootx() + 20
    y = event.widget.winfo_rooty() + event.widget.winfo_height() + 10

    tooltip = Toplevel()
    tooltip.wm_overrideredirect(True)
    tooltip.wm_geometry(f"+{x}+{y}")
    tooltip.configure(bg="#333333")

    label = Label(tooltip,
                  text=txt,
                  background="#fcfcfa",
                  foreground="#000000",  # чёрный текст
                  font=("Segoe UI", 10),
                  relief="solid",
                  borderwidth=1,
                  padx=8, pady=4)

    label.pack()

    # Добавим скругление и лёгкую тень — опционально через Windows 11 эффекты (визуально)
    try:
        tooltip.attributes("-alpha", 0.97)
        tooltip.attributes("-topmost", True)
    except:
        pass
def hide_tooltip(event):
    global tooltip
    if tooltip:
        tooltip.destroy()
        tooltip = None
def redactor(root, lang,start_time_,global_bg,global_fg,GlobalAlpha):
    def apply_tag(tag):
        try:
            start = text.index("sel.first")
            end = text.index("sel.last")
            text.tag_add(tag, start, end)
        except TclError:
            pass
    def make_bold(event=None):
        apply_tag("bold");
        return "break"
    def make_italic(event=None):
        apply_tag("italic");
        return "break"
    def make_underline(event=None):
        apply_tag("underline");
        return "break"
    def save_file(event=None):
        # Предлагаем имя по умолчанию и сохраняем только в SAVE_DIR
        file_path = filedialog.asksaveasfilename(
            initialdir=SAVE_DIR,
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")],
            title=lang["savefile"]
        )
        if not file_path:
            return

        content = text.get("1.0", "end-1c")
        tags_data = []
        for tag in text.tag_names():
            tag_config = text.tag_cget(tag, "foreground") if tag.startswith("color_") else None
            for start, end in zip(text.tag_ranges(tag)[::2], text.tag_ranges(tag)[1::2]):
                tags_data.append({
                    "tag": tag,
                    "start": str(start),
                    "end": str(end),
                    "color": tag_config  # добавим цвет
                })

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump({"content": content, "tags": tags_data}, f, ensure_ascii=False, indent=2)
        return "break"
    def load_file(event=None):
        # Только из SAVE_DIR
        file_path = filedialog.askopenfilename(parent = roott,
            initialdir=SAVE_DIR,
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")],
            title=lang["openfile"]
        )
        if not file_path:
            return

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        text.delete("1.0", "end")
        text.insert("1.0", data["content"])
        for tag_data in data.get("tags", []):
            tag_name = tag_data["tag"]
            if tag_data.get("color"):
                text.tag_configure(tag_name, foreground=tag_data["color"])
            text.tag_add(tag_name, tag_data["start"], tag_data["end"])

        return "break"
    def cut_text(event=None):
        text.event_generate("<<Cut>>");
        return "break"
    def copy_text(event=None):
        text.event_generate("<<Copy>>");
        return "break"
    def paste_text(event=None):
        text.event_generate("<<Paste>>");
        return "break"
    def undo_action(event=None):
        text.edit_undo();
        return "break"
    def redo_action(event=None):
        text.edit_redo();
        return "break"
    def choose_text_color():
        color = colorchooser.askcolor(parent=roott)[1]

        if color:
            try:
                start = text.index("sel.first")
                end = text.index("sel.last")
                tag_name = f"color_{color}"
                text.tag_configure(tag_name, foreground=color)
                text.tag_add(tag_name, start, end)
            except:
                pass
    def find_text():
        word = simpledialog.askstring(lang["resred"], lang["whatre"])
        if word:
            text.tag_remove("highlight", "1.0", "end")
            start = "1.0"
            while True:
                pos = text.search(word, start, stopindex="end")
                if not pos: break
                end = f"{pos}+{len(word)}c"
                text.tag_add("highlight", pos, end)
                start = end
            text.tag_configure("highlight", background="yellow")
    def export_to_html():
        file_path = filedialog.asksaveasfilename(defaultextension=".html")
        if not file_path: return
        content = text.get("1.0", "end-1c").replace("\n", "<br>")
        html = f"<html><body>{content}</body></html>"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html)
    def autosave():
        autosave_path = os.path.join(SAVE_DIR, "autosave.json")
        with open(autosave_path, "w", encoding="utf-8") as f:
            content = text.get("1.0", "end-1c")
            f.write(json.dumps({"content": content}))
        roott.after(60000, autosave)  # каждые 60 секунд
    def toggle_white_mode():
        text.config(bg="white", fg="black", insertbackground="black")
    def toggle_dark_mode():
        text.config(bg="#2e2e2e", fg="#ffffff", insertbackground="white")
    def change_font(event=None):
        try:
            new_font = font.Font(family=font_box.get(), size=int(size_box.get()))
            text.configure(font=new_font)
        except:
            pass

    roott = create_window(root, lang["redactor"], global_bg, float(GlobalAlpha), 600, 600, "icons/svb txt redactor.png")
    text_font = font.Font(family="Arial", size=12)
    text = Text(roott, wrap="word", font=text_font, undo=True)
    text.pack(fill="both", expand=True)

    # Настройка тегов
    bold_font = font.Font(text, text.cget("font"));
    bold_font.configure(weight="bold")
    italic_font = font.Font(text, text.cget("font"));
    italic_font.configure(slant="italic")
    underline_font = font.Font(text, text.cget("font"));
    underline_font.configure(underline=True)

    text.tag_configure("bold", font=bold_font)
    text.tag_configure("italic", font=italic_font)
    text.tag_configure("underline", font=underline_font)

    menu = Menu(roott)
    roott.config(menu=menu)

    file_menu = Menu(menu, tearoff=0)
    menu.add_cascade(label=lang["file_re"], menu=file_menu)
    file_menu.add_command(label=lang["save_re"], command=save_file)
    file_menu.add_command(label=lang["open_re"], command=load_file)
    file_menu.add_command(label=lang["exphtml"], command=export_to_html)

    format_menu = Menu(menu, tearoff=0)
    menu.add_cascade(label=lang["format"], menu=format_menu)
    format_menu.add_command(label=lang["bold"], command=make_bold)
    format_menu.add_command(label=lang["italic"], command=make_italic)
    format_menu.add_command(label=lang["underline"], command=make_underline)
    format_menu.add_command(label=lang["textcolor"], command=choose_text_color)
    format_menu.add_command(label=lang["resred"], command=find_text)
    format_menu.add_command(label=lang["dktema"], command=toggle_dark_mode)
    format_menu.add_command(label=lang["svtema"], command=toggle_white_mode)
    # Панель инструментов
    toolbar = Frame(roott)
    toolbar.pack(fill="x")

    image = Image.open("icons//interface//bold.png")
    image = image.resize((24, 24))
    bold_img = ImageTk.PhotoImage(image)
    image = Image.open("icons//interface//italic.png")
    image = image.resize((24, 24))
    italic_img = ImageTk.PhotoImage(image)
    image = Image.open("icons//interface//underline.png")
    image = image.resize((24, 24))
    underline_img = ImageTk.PhotoImage(image)
    image = Image.open("icons//interface//search.png")
    image = image.resize((24, 24))
    find_img = ImageTk.PhotoImage(image)
    image = Image.open("icons//interface//color.png")
    image = image.resize((24, 24))
    color_img = ImageTk.PhotoImage(image)

    bold_btn = Button(toolbar, image=bold_img, command=make_bold)
    bold_btn.image = bold_img
    bold_btn.pack(side="left")
    bold_btn.bind("<Enter>", lambda event: show_tooltip(event, txt=lang["tooltip_bold"]))
    bold_btn.bind("<Leave>", hide_tooltip)

    italic_btn = Button(toolbar, image=italic_img, command=make_italic)
    italic_btn.image = italic_img
    italic_btn.pack(side="left")
    italic_btn.bind("<Enter>", lambda event: show_tooltip(event, txt=lang["tooltip_italic"]))
    italic_btn.bind("<Leave>", hide_tooltip)

    underline_btn = Button(toolbar, image=underline_img, command=make_underline)
    underline_btn.image = underline_img
    underline_btn.pack(side="left")
    underline_btn.bind("<Enter>", lambda event: show_tooltip(event, txt=lang["tooltip_underline"]))
    underline_btn.bind("<Leave>", hide_tooltip)

    color_btn = Button(toolbar, image=color_img, command=choose_text_color)
    color_btn.image = color_img
    color_btn.pack(side="left")
    color_btn.bind("<Enter>", lambda event: show_tooltip(event, txt=lang["tooltip_color"]))
    color_btn.bind("<Leave>", hide_tooltip)

    find_btn = Button(toolbar, image=find_img, command=find_text)
    find_btn.image = find_img
    find_btn.pack(side="left")
    find_btn.bind("<Enter>", lambda event: show_tooltip(event, txt=lang["tooltip_find"]))
    find_btn.bind("<Leave>", hide_tooltip)

    Label(toolbar, text=lang["policce"],bg = global_bg,fg = global_fg).pack(side="left")
    font_box = ttk.Combobox(toolbar, values=font.families(), width=15)
    font_box.set("Arial")
    font_box.pack(side="left")

    size_box = ttk.Combobox(toolbar, values=[str(s) for s in range(8, 40)], width=3)
    size_box.set("12")
    size_box.pack(side="left")

    font_box.bind("<<ComboboxSelected>>", change_font)
    size_box.bind("<<ComboboxSelected>>", change_font)

    # Бинды
    roott.bind("<Control-b>", make_bold)
    roott.bind("<Control-i>", make_italic)
    roott.bind("<Control-u>", make_underline)
    roott.bind("<Control-s>", save_file)
    roott.bind("<Control-o>", load_file)
    roott.bind("<Control-z>", undo_action)
    roott.bind("<Control-y>", redo_action)
    roott.bind("<Control-x>", cut_text)
    roott.bind("<Control-c>", copy_text)
    roott.bind("<Control-v>", paste_text)

    autosave()
