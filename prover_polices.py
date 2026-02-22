import tkinter as tk
from tkinter import font

root = tk.Tk()
root.geometry("1000x1000")
# Проверь, доступен ли шрифт
#'Minecart LCD', 'Soviet Program', 'Zombie Holocaust', 'Nosifer', 'Hole-Hearted', 'PWJoyeuxNoel', 'CandyTime',
# 'Kingthings Christmas 2', 'Snowtop Caps', 'Haloberry' 'Crashed Scoreboard', 'Karnivore Black', Drawliner' 'Minisystem'
#'Jigsaw Trouserdrop', Game Bubble',
print(font.families())
font_names = [
    'SAIBA-45', 'LIBRARY 3 AM', 'Neuropol', 'Overload', 'Perfect Dark (BRK)', 'Squares Bold', "You're Gone",
    'Xirod', 'Shlop', 'Budmo Jigglish' 'Living by Numbers',"Electroharmonix"
]
frame1 = tk.Frame()
frame1.pack(side = tk.LEFT)
frame2 = tk.Frame()
frame2.pack(side = tk.LEFT)
for fname in font_names:
    try:
        label = tk.Label(frame1, text=f"{fname}: ABCD", font=(fname, 20))
        label.pack(pady=5)
    except Exception as e:
        print(f"Ошибка с шрифтом {fname}: {e}")
for fname in font_names:
    try:
        label = tk.Label(frame2, text=f"{fname}: 1234", font=(fname, 20))
        label.pack(pady=5)
    except Exception as e:
        print(f"Ошибка с шрифтом {fname}: {e}")
root.mainloop()
