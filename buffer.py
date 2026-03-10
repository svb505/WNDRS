import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from openpyxl import Workbook, load_workbook

class ExcelApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SVBExcel")
        self.workbook = Workbook()
        self.sheet = self.workbook.active
        self.current_file = None

        toolbar = tk.Frame(root)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        tk.Button(toolbar, text=lang["create_new_file"], command=self.new_file).pack(side=tk.LEFT, padx=2)
        tk.Button(toolbar, text=lang["open_file_excel"], command=self.open_file).pack(side=tk.LEFT, padx=2)
        tk.Button(toolbar, text=lang["save_file"], command=self.save_file).pack(side=tk.LEFT, padx=2)
        tk.Button(toolbar, text=lang["save_how"], command=self.save_as_file).pack(side=tk.LEFT, padx=2)

        self.tree = ttk.Treeview(root, show="headings")
        self.tree.pack(expand=True, fill=tk.BOTH)
        self.tree.bind("<Double-1>", self.edit_cell)

        self.setup_table(10, 10)
    def setup_table(self, rows, cols):
        self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = [str(i+1) for i in range(cols)]
        for col in self.tree["columns"]:
            self.tree.heading(col, text=f"{lang['colon']} {col}")
            self.tree.column(col, width=100)
        for r in range(rows):
            self.tree.insert("", "end", values=["" for _ in range(cols)])
    def edit_cell(self, event):
        item = self.tree.selection()[0]
        col = self.tree.identify_column(event.x)
        col_index = int(col.replace("#","")) - 1

        old_value = self.tree.item(item, "values")[col_index]

        edit_win = tk.Toplevel(self.root)
        edit_win.title("Редактировать ячейку")

        tk.Label(edit_win, text="Новое значение:").pack(padx=10, pady=5)
        entry = tk.Entry(edit_win)
        entry.pack(padx=10, pady=5)
        entry.insert(0, old_value)
        entry.focus()

        def save_edit():
            new_value = entry.get()
            values = list(self.tree.item(item, "values"))
            values[col_index] = new_value
            self.tree.item(item, values=values)
            edit_win.destroy()

        tk.Button(edit_win, text="Сохранить", command=save_edit).pack(pady=5)

    def new_file(self):
        self.workbook = Workbook()
        self.sheet = self.workbook.active
        self.current_file = None
        self.setup_table(10, 10)

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            self.workbook = load_workbook(file_path)
            self.sheet = self.workbook.active
            self.current_file = file_path
            self.load_sheet_to_table()

    def load_sheet_to_table(self):
        rows = self.sheet.max_row
        cols = self.sheet.max_column
        self.setup_table(rows, cols)
        for r in range(1, rows+1):
            values = []
            for c in range(1, cols+1):
                values.append(str(self.sheet.cell(row=r, column=c).value or ""))
            self.tree.item(self.tree.get_children()[r-1], values=values)

    def save_file(self):
        if self.current_file:
            self.save_to_file(self.current_file)
        else:
            self.save_as_file()

    def save_as_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            self.current_file = file_path
            self.save_to_file(file_path)

    def save_to_file(self, path):
        for r_index, item in enumerate(self.tree.get_children(), start=1):
            values = self.tree.item(item, "values")
            for c_index, val in enumerate(values, start=1):
                self.sheet.cell(row=r_index, column=c_index, value=val)
        self.workbook.save(path)
        messagebox.showinfo("Сохранено", f"Файл сохранен: {path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ExcelApp(root)
    root.geometry("800x600")
    root.mainloop()