from tkinter import *
from datetime import datetime

def open_bsod(code, decr, on_finish=None):  # ← Добавили on_finish
    def compl(i=1):
        if i <= 100:
            a.config(text=f"\n\n\n{i}% Complete")
            Win.after(100, lambda: compl(i + 1))
        else:
            Win.destroy()
            if on_finish:  # ← Проверяем и вызываем main()
                on_finish()
    def save_dump():
        timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        data = f"WINDOORS52 CRASH DUMP\nTIMESTAMP - {timestamp}\nSTOP CODE - {code}\nDECRYPTION - {decr}"
        with open(f".dumps/dump_CRASHDUMP_{timestamp}.dmp","w") as f:
            f.write(data)
        dmp_l.config(text = f'DUMP: DUMP SAVED IN ".dumps/dump_CRASHDUMP_{timestamp}.dmp"')
    Win = Tk()
    Win.geometry("400x300")
    Win.attributes("-fullscreen", True)
    Win.config(bg="#0078D7")

    Label(Win,text=':(', font=("Arial", 120), bg="#0078D7", fg="white").grid(row = 0,column = 0,sticky=W)
    Label(Win,
        text="\nYour PC ran into a problem and needs to restart just collecting\n some error info, and then we'll restart for you",
        font=("Arial", 30), bg="#0078D7", fg="white").grid(row = 1,column = 0)
    a = Label(Win,text = "\n\n\n",font=("Arial", 20), bg="#0078D7", fg="white")
    a.grid(row = 2,column = 0,sticky = W)
    Label(Win,text=f'\n\n\n\n\n\n\n\n\n\n\n\nDecrypt: {decr}',font=("Arial", 15), bg="#0078D7", fg='white').grid(row = 3,column = 0,sticky=W)
    Label(Win,text=f"Stop code: {code}", font=("Arial", 15), bg="#0078D7", fg='white').grid(row = 4,column = 0,sticky = W,pady = 10)
    dmp_l = Label(Win,text=f"", font=("Arial", 15), bg="#0078D7", fg='white')
    dmp_l.grid(row = 5,column = 0,sticky = W,pady = 10)
    # ← вызови запуск % после старта окна
    Win.after(500, compl)  # Дай 0.5 сек, чтобы окно точно показалось
    save_dump()
    Win.mainloop()
