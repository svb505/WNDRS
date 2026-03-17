from send_email import send_email
from tkinter import *
from tkinter import messagebox,filedialog,ttk
import webbrowser
from tkhtmlview import HTMLLabel

files = []

def openWin(root,lang):
    pages = {lang['style1']: f"""<div style="max-width:600px; margin:20px auto; padding:20px; border:1px solid #ccc; border-radius:8px; background-color:#f9f9f9; font-family:Arial, sans-serif; color:#333;">
      <p>Hello, [Name]!</p>
      <p>Just wanted to drop a line and say hi. Hope you're doing well!</p>
      <p>Sincerely,<br>[Your name]</p>
    </div>""", lang['style2']: f"""<div style="max-width:600px; margin:20px auto; padding:20px; border-radius:10px; background-color:#e0f7fa; font-family:Arial, sans-serif; color:#006064;">
      <p>Hello, [Name]!</p>
      <p>I decided to write you a few words in this short block. It's simple and stylish :)</p>
      <p>[Your name]</p>
    </div>""", lang['style3']: f"""<div style="max-width:600px; margin:20px auto; padding:20px; border-radius:8px; background-color:#333; font-family:Arial, sans-serif; color:#fff;">
      <p>Hello, [Name]!</p>
      <p>I decided to write you a few words in this short block. It's simple and stylish :)</p>
      <p>[Your name]</p>
    </div>""", lang["style4"]: f"""<div style="max-width:600px; margin:20px auto; padding:20px; border-left:5px solid #1a73e8; border-radius:5px; background-color:#f1f8ff; font-family:Arial, sans-serif; color:#333;">
      <p>Hello, [Name]!</p>
      <p>I decided to write you a few words in this short block. It's simple and stylish :)</p>
      <p>[Your name]</p>
    </div>""", lang['style5']: f"""<div style="max-width:600px; margin:20px auto; padding:20px; border:1px solid #ddd; border-radius:8px; box-shadow:0 2px 5px rgba(0,0,0,0.1); background-color:#fff; font-family:Arial, sans-serif; color:#333;">
      <p>Hello, [Name]!</p>
      <p>I decided to write you a few words in this short block. It's simple and stylish :)</p>
      <p>[Your name]</p>
    </div>"""}
    def return_style(msg,var):
        pages_withnout = {lang['style1']:
                f"""<div style="max-width:600px; margin:20px auto; padding:20px; border:1px solid #ccc; border-radius:8px; background-color:#f9f9f9; font-family:Arial, sans-serif; color:#333;">
                {msg}</div>""",
            lang['style2']:
            f"""<div style="max-width:600px; margin:20px auto; padding:20px; border-radius:10px; background-color:#e0f7fa; font-family:Arial, sans-serif; color:#006064;">
                {msg}</div>""",
                lang['style3']:
            f"""<div style="max-width:600px; margin:20px auto; padding:20px; border-radius:8px; background-color:#333; font-family:Arial, sans-serif; color:#fff;">
                {msg}</div>""",
                          lang["style4"]:
            f"""<div style="max-width:600px; margin:20px auto; padding:20px; border-left:5px solid #1a73e8; border-radius:5px; background-color:#f1f8ff; font-family:Arial, sans-serif; color:#333;">
                {msg}</div>""",
                          lang['style5']:
            f"""<div style="max-width:600px; margin:20px auto; padding:20px; border:1px solid #ddd; border-radius:8px; box-shadow:0 2px 5px rgba(0,0,0,0.1); background-color:#fff; font-family:Arial, sans-serif; color:#333;">
                {msg}</div>"""}
        return pages_withnout[var]
    def select_files():
        global files
        files = filedialog.askopenfilenames(filetypes=[("All files", "*")])
        files_list.delete(0, END)
        for f in files:
            files_list.insert(END, f)

    def open_html(sel, html_label):
        html = pages.get(sel.get())
        html_label.set_html(html)

    def send():
        email_from = u_email.get()
        email_to = to_email.get()
        password = u_code.get()
        subject = sub.get()
        message = msg.get()
        style_html = return_style(message,var.get())
        try:
            send_email(email_to,subject,style_html,list(files),password,email_from)
            messagebox.showinfo(lang['success'], lang["email_sent"])
        except Exception as e:
            messagebox.showerror(lang['error'], str(e))

    Win = Toplevel(root)
    Win.geometry("600x650")
    Win.title(lang['email_sender'])

    main_frm = Frame(Win)
    main_frm.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)
    html_frm = Frame(Win)
    html_frm.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)

    Label(main_frm, text=lang["enter_your_email"]).pack()
    u_email = ttk.Entry(main_frm)
    u_email.pack()
    Label(main_frm, text=lang["enter_to_email"]).pack()
    to_email = ttk.Entry(main_frm)
    to_email.pack()
    Label(main_frm, text=lang["enter_your_code"]).pack()
    ttk.Button(main_frm, text=lang["pol_po_ss"], command=lambda: webbrowser.open(
        "https://myaccount.google.com/apppasswords?utm_source=chatgpt.com")).pack()
    u_code = ttk.Entry(main_frm)
    u_code.pack()
    Label(main_frm, text=lang["enter_sub"]).pack()
    sub = ttk.Entry(main_frm)
    sub.pack()
    Label(main_frm, text=lang["enter_msg"]).pack()
    msg = ttk.Entry(main_frm)
    msg.pack()

    Label(main_frm, text=lang["select_style"]).pack()
    var = StringVar()
    cbx = ttk.Combobox(main_frm,
                       values=[lang['style1'], lang['style2'], lang['style3'], lang['style4'], lang['style5']],
                       textvariable=var)
    cbx.pack()

    html_label = HTMLLabel(html_frm, html="")
    html_label.pack(fill=BOTH, expand=True, padx=10, pady=10)
    cbx.bind("<<ComboboxSelected>>", lambda event: open_html(var, html_label))

    var.set(lang['style1'])
    open_html(var, html_label)

    # Кнопка для выбора файлов
    ttk.Button(main_frm, text=lang["select_files&"], command=select_files).pack(pady=5)
    files_list = Listbox(main_frm, height=5)
    files_list.pack(fill=BOTH, expand=True)

    # Кнопка отправки
    ttk.Button(main_frm, text=lang["send_email&"], command=send).pack(pady=10)