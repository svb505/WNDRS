from tkinter import *
from tkinter import filedialog, messagebox, simpledialog,ttk
from pptx import Presentation
from create_window import create_window

prs = Presentation()
current_file = None

def svbpptx(root,lang,global_bg,alpha):
    def new_presentation():
        global prs, current_file
        prs = Presentation()
        current_file = None
        update_slide_list()
        preview_text.delete("1.0",END)
    def open_presentation():
        global prs, current_file
        file_path = filedialog.askopenfilename(filetypes=[("PowerPoint files", "*.pptx")])
        if file_path:
            prs = Presentation(file_path)
            current_file = file_path
            update_slide_list()
            preview_text.delete("1.0", END)
    def add_slide_dialog():
        title = simpledialog.askstring(lang["slide"], lang["enter_slide_title"])
        text = simpledialog.askstring(lang["slide"], lang["enter_slide_text"])
        if title is not None and text is not None:
            add_slide(title, text)
            update_slide_list()
    def add_slide(title, text):
        slide_layout = prs.slide_layouts[1]  # Заголовок + текст
        slide = prs.slides.add_slide(slide_layout)
        slide.shapes.title.text = title
        slide.placeholders[1].text = text
    def update_slide_list():
        slide_list.delete(0, END)
        for idx, slide in enumerate(prs.slides, start=1):
            title = slide.shapes.title.text if slide.shapes.title else lang["withnout_title"]
            slide_list.insert(END, f"{idx}. {title}")
    def show_slide_preview(event):
        selection = slide_list.curselection()
        if selection:
            index = selection[0]
            slide = prs.slides[index]
            title = slide.shapes.title.text if slide.shapes.title else ""
            text = slide.placeholders[1].text if len(slide.placeholders) > 1 else ""
            preview_text.delete("1.0",END)
            preview_text.insert(END, f"{lang['title']}: {title}\n\n{text}")
    def save_file():
        global current_file
        if current_file:
            prs.save(current_file)
            messagebox.showinfo(lang["success"], f"{lang['pres_saved']}: {current_file}")
        else:
            save_as_file()
    def save_as_file():
        global current_file
        file_path = filedialog.asksaveasfilename(defaultextension=".pptx", filetypes=[("PowerPoint files", "*.pptx")])
        if file_path:
            current_file = file_path
            prs.save(file_path)
            messagebox.showinfo(lang["success"], f"{lang['pres_saved']}: {file_path}")

    Win = create_window(root,"SVB PowerPoint",global_bg,alpha,800,600,"icons/pptx.png")

    toolbar = ttk.Frame(Win)
    toolbar.pack(side=TOP, fill=X)

    ttk.Button(toolbar, text=lang["create_pres"], command=new_presentation).pack(side=LEFT, padx=2)
    ttk.Button(toolbar, text=lang['open_pres'], command=open_presentation).pack(side=LEFT, padx=2)
    ttk.Button(toolbar, text=lang["save_file"], command=save_file).pack(side=LEFT, padx=2)
    ttk.Button(toolbar, text=lang["save_how"], command=save_as_file).pack(side=LEFT, padx=2)
    ttk.Button(toolbar, text=lang['add_slide'], command=add_slide_dialog).pack(side=LEFT, padx=2)

    slide_list = Listbox(Win)
    slide_list.pack(side=LEFT, fill=Y)
    slide_list.bind("<<ListboxSelect>>", show_slide_preview)

    preview_text = Text(Win)
    preview_text.pack(side=RIGHT, expand=True, fill=BOTH)

    Win.mainloop()