from tkinter import *
from tkinter import font, filedialog, colorchooser, simpledialog, ttk
from docx import Document
from docx.shared import RGBColor
from PIL import Image, ImageTk
import os

import create_window

SAVE_DIR = "MyTextFiles"
os.makedirs(SAVE_DIR, exist_ok=True)
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
    label = Label(tooltip, text=txt, background="#fcfcfa", foreground="#000000",
                  font=("Segoe UI", 10), relief="solid", borderwidth=1, padx=8, pady=4)
    label.pack()


def hide_tooltip(event):
    global tooltip
    if tooltip:
        tooltip.destroy()
        tooltip = None


def redactor(root, lang, start_time_, global_bg, global_fg, GlobalAlpha):
    roott = create_window.create_window(root,lang["redactor"],global_bg,GlobalAlpha,900,600,
                                        "icons/SVB TxT Redactor.png")

    text_font = font.Font(family="Arial", size=12)
    text = Text(roott, wrap="word", font=text_font, undo=True)
    text.pack(fill="both", expand=True)

    bold_font = font.Font(text, text.cget("font"))
    bold_font.configure(weight="bold")
    italic_font = font.Font(text, text.cget("font"))
    italic_font.configure(slant="italic")
    underline_font = font.Font(text, text.cget("font"))
    underline_font.configure(underline=True)

    text.tag_configure("bold", font=bold_font)
    text.tag_configure("italic", font=italic_font)
    text.tag_configure("underline", font=underline_font)

    def apply_tag(tag):
        try:
            start = text.index("sel.first")
            end = text.index("sel.last")
            text.tag_add(tag, start, end)
        except:
            pass

    def make_bold(event=None):
        apply_tag("bold"); return "break"

    def make_italic(event=None):
        apply_tag("italic"); return "break"

    def make_underline(event=None):
        apply_tag("underline"); return "break"

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

    def save_file(event=None):
        file_path = filedialog.asksaveasfilename(initialdir=SAVE_DIR, defaultextension=".docx",
                                                 filetypes=[("Word Document", "*.docx")])
        if not file_path: return
        document = Document()
        dump = text.dump("1.0", "end-1c", tag=True, text=True)
        paragraph = document.add_paragraph()
        active_tags = set()
        for item in dump:
            kind = item[0]
            if kind == "tagon":
                active_tags.add(item[1])
            elif kind == "tagoff":
                active_tags.discard(item[1])
            elif kind == "text":
                value = item[1]
                if "\n" in value:
                    parts = value.split("\n")
                    for i, part in enumerate(parts):
                        if part:
                            run = paragraph.add_run(part)
                            if "bold" in active_tags: run.bold = True
                            if "italic" in active_tags: run.italic = True
                            if "underline" in active_tags: run.underline = True
                            for tag in active_tags:
                                if tag.startswith("color_"):
                                    color = tag.replace("color_", "").lstrip("#")
                                    r = int(color[0:2], 16)
                                    g = int(color[2:4], 16)
                                    b = int(color[4:6], 16)
                                    run.font.color.rgb = RGBColor(r, g, b)
                        if i != len(parts) - 1: paragraph = document.add_paragraph()
                else:
                    run = paragraph.add_run(value)
                    if "bold" in active_tags: run.bold = True
                    if "italic" in active_tags: run.italic = True
                    if "underline" in active_tags: run.underline = True
                    for tag in active_tags:
                        if tag.startswith("color_"):
                            color = tag.replace("color_", "").lstrip("#")
                            r = int(color[0:2], 16)
                            g = int(color[2:4], 16)
                            b = int(color[4:6], 16)
                            run.font.color.rgb = RGBColor(r, g, b)
        document.save(file_path)

    def load_file(event=None):
        file_path = filedialog.askopenfilename(initialdir=SAVE_DIR, filetypes=[("Word Document", "*.docx")])
        if not file_path: return
        document = Document(file_path)
        text.delete("1.0", "end")
        for paragraph in document.paragraphs:
            for run in paragraph.runs:
                start = text.index("end-1c")
                text.insert("end", run.text)
                end = text.index("end-1c")
                if run.bold: text.tag_add("bold", start, end)
                if run.italic: text.tag_add("italic", start, end)
                if run.underline: text.tag_add("underline", start, end)
                if run.font.color and run.font.color.rgb:
                    rgb = run.font.color.rgb
                    color = f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"
                    tag_name = f"color_{color}"
                    text.tag_configure(tag_name, foreground=color)
                    text.tag_add(tag_name, start, end)
            text.insert("end", "\n")

    def find_text():
        word = simpledialog.askstring(lang["resred"], lang["whatre"])
        if not word: return
        text.tag_remove("highlight", "1.0", "end")
        start = "1.0"
        while True:
            pos = text.search(word, start, stopindex="end")
            if not pos: break
            end = f"{pos}+{len(word)}c"
            text.tag_add("highlight", pos, end)
            start = end
        text.tag_configure("highlight", background="yellow")

    menu = Menu(roott)
    roott.config(menu=menu)
    file_menu = Menu(menu, tearoff=0)
    menu.add_cascade(label=lang["file_re"], menu=file_menu)
    file_menu.add_command(label=lang["open_re"], command=load_file)
    file_menu.add_command(label=lang["save_re"], command=save_file)
    format_menu = Menu(menu, tearoff=0)
    menu.add_cascade(label=lang["format"], menu=format_menu)
    format_menu.add_command(label=lang["bold"], command=make_bold)
    format_menu.add_command(label=lang["italic"], command=make_italic)
    format_menu.add_command(label=lang["underline"], command=make_underline)
    format_menu.add_command(label=lang["textcolor"], command=choose_text_color)
    menu.add_command(label=lang["resred"], command=find_text)

    toolbar = Frame(roott)
    toolbar.pack(fill="x")

    def load_icon(path, size=(24, 24)):
        img = Image.open(path).resize(size)
        return ImageTk.PhotoImage(img)

    bold_img = load_icon("icons/interface/bold.png")
    italic_img = load_icon("icons/interface/italic.png")
    underline_img = load_icon("icons/interface/underline.png")
    color_img = load_icon("icons/interface/color.png")
    find_img = load_icon("icons/interface/search.png")

    bold_btn = Button(toolbar, image=bold_img, command=make_bold)
    bold_btn.image = bold_img
    bold_btn.pack(side="left")
    bold_btn.bind("<Enter>", lambda e: show_tooltip(e, lang["tooltip_bold"]))
    bold_btn.bind("<Leave>", hide_tooltip)

    italic_btn = Button(toolbar, image=italic_img, command=make_italic)
    italic_btn.image = italic_img
    italic_btn.pack(side="left")
    italic_btn.bind("<Enter>", lambda e: show_tooltip(e, lang["tooltip_italic"]))
    italic_btn.bind("<Leave>", hide_tooltip)

    underline_btn = Button(toolbar, image=underline_img, command=make_underline)
    underline_btn.image = underline_img
    underline_btn.pack(side="left")
    underline_btn.bind("<Enter>", lambda e: show_tooltip(e, lang["tooltip_underline"]))
    underline_btn.bind("<Leave>", hide_tooltip)

    color_btn = Button(toolbar, image=color_img, command=choose_text_color)
    color_btn.image = color_img
    color_btn.pack(side="left")
    color_btn.bind("<Enter>", lambda e: show_tooltip(e, lang["tooltip_color"]))
    color_btn.bind("<Leave>", hide_tooltip)

    find_btn = Button(toolbar, image=find_img, command=find_text)
    find_btn.image = find_img
    find_btn.pack(side="left")
    find_btn.bind("<Enter>", lambda e: show_tooltip(e, lang["tooltip_find"]))
    find_btn.bind("<Leave>", hide_tooltip)

    Label(toolbar, text=lang["policce"], bg=global_bg, fg=global_fg).pack(side="left")
    font_box = ttk.Combobox(toolbar, values=font.families(), width=15)
    font_box.set("Arial")
    font_box.pack(side="left")
    size_box = ttk.Combobox(toolbar, values=[str(s) for s in range(8, 40)], width=3)
    size_box.set("12")
    size_box.pack(side="left")

    def change_font(event=None):
        try:
            new_font = font.Font(family=font_box.get(), size=int(size_box.get()))
            text.configure(font=new_font)
        except:
            pass

    font_box.bind("<<ComboboxSelected>>", change_font)
    size_box.bind("<<ComboboxSelected>>", change_font)

    roott.bind("<Control-b>", make_bold)
    roott.bind("<Control-i>", make_italic)
    roott.bind("<Control-u>", make_underline)
    roott.bind("<Control-s>", save_file)
    roott.bind("<Control-o>", load_file)