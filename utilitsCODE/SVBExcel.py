import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from openpyxl import Workbook, load_workbook
from create_window import create_window

workbook = Workbook()
sheet = workbook.active
current_file = None
tree = None

def svbexcel(root,lang,global_bg,alpha):
    def setup_table(rows, cols):
        global tree
        tree.delete(*tree.get_children())
        tree["columns"] = [str(i + 1) for i in range(cols)]
        for col in tree["columns"]:
            tree.heading(col, text=f"{lang['colon']} {col}")
            tree.column(col, width=100)
        for r in range(rows):
            tree.insert("", "end", values=["" for _ in range(cols)])
    def edit_cell(event):
        item = tree.selection()[0]
        col = tree.identify_column(event.x)
        col_index = int(col.replace("#", "")) - 1

        old_value = tree.item(item, "values")[col_index]

        edit_win = tk.Toplevel(Win)
        edit_win.title(lang["redact_col"])

        tk.Label(edit_win, text=lang["new_data"]).pack(padx=10, pady=5)
        entry = tk.Entry(edit_win)
        entry.pack(padx=10, pady=5)
        entry.insert(0, old_value)
        entry.focus()

        def save_edit():
            new_value = entry.get()
            values = list(tree.item(item, "values"))
            values[col_index] = new_value
            tree.item(item, values=values)
            edit_win.destroy()

        ttk.Button(edit_win, text=lang["save_file"], command=save_edit).pack(pady=5)
    def new_file():
        global workbook, sheet, current_file
        workbook = Workbook()
        sheet = workbook.active
        current_file = None
        setup_table(10, 10)
    def open_file():
        global workbook, sheet, current_file
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            workbook = load_workbook(file_path)
            sheet = workbook.active
            current_file = file_path
            load_sheet_to_table()
    def load_sheet_to_table():
        rows = sheet.max_row
        cols = sheet.max_column
        setup_table(rows, cols)
        for r in range(1, rows + 1):
            values = []
            for c in range(1, cols + 1):
                values.append(str(sheet.cell(row=r, column=c).value or ""))
            tree.item(tree.get_children()[r - 1], values=values)
    def save_file():
        if current_file: save_to_file(current_file)
        else: save_as_file()
    def save_as_file():
        global current_file
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            current_file = file_path
            save_to_file(file_path)
    def save_to_file(path):
        for r_index, item in enumerate(tree.get_children(), start=1):
            values = tree.item(item, "values")
            for c_index, val in enumerate(values, start=1):
                sheet.cell(row=r_index, column=c_index, value=val)
        workbook.save(path)
        messagebox.showinfo(lang["success"], f"{lang['file_saved']}: {path}")

    Win = create_window(root,"SVBExcel",global_bg,alpha,800,600,"icons/svbexcel.png")

    toolbar = ttk.Frame(Win)
    toolbar.pack(side=tk.TOP, fill=tk.X)

    ttk.Button(toolbar, text=lang["create_new_file"], command=new_file).pack(side=tk.LEFT, padx=2)
    ttk.Button(toolbar, text=lang["open_file_excel"], command=open_file).pack(side=tk.LEFT, padx=2)
    ttk.Button(toolbar, text=lang["save_file"], command=save_file).pack(side=tk.LEFT, padx=2)
    ttk.Button(toolbar, text=lang["save_how"], command=save_as_file).pack(side=tk.LEFT, padx=2)

    tree = ttk.Treeview(Win, show="headings")
    tree.pack(expand=True, fill=tk.BOTH)
    tree.bind("<Double-1>", edit_cell)

    setup_table(10, 10)
