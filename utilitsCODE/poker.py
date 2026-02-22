from tkinter import *
from tkinter import ttk, messagebox, colorchooser, simpledialog
import sqlite3
import random
from datetime import datetime, timedelta
from PIL import Image, ImageTk
import tabulate
from logtofile import log_to_file
from crypto_work import decrypt_message,encrypt_message,load_key
from create_window import create_window

call_count = 0
turn = 0
score = 0
dice_canvas_ids = []
check_vars = []
roll_count = 0
players = []
scores = []
obligatory_scores = []
matches_played = []
chosen_nominals = []
chosen_combinations = []
phase = "obligatory"
background_color = ""
color_dice = ""
activefill_dice = ""
color = None
last_booster_activation_time = None
booster_active = False
dialog_roll = None
dialog_combination = None

dice_values = [random.randint(1, 6) for _ in range(5)]
points0 = [random.randint(1, 6), random.randint(1, 6), random.randint(1, 6), random.randint(1, 6), random.randint(1, 6)]
key = load_key()
with open("games/poker_settings/active_color.cfg","rb") as f:
    activefill_dice = decrypt_message(f.read(),key)
with open("games/poker_settings/dice_color.cfg","rb") as f:
    color_dice = decrypt_message(f.read(),key)
with open("games/poker_settings/bg.cfg","rb") as f:
    background_color = decrypt_message(f.read(),key)
def poker(root,lang,start_time_,global_bg,GlobalAlpha):
    def main_window():
        log_to_file("Poker launched",start_time_=start_time_)
        combinations = {
            lang["poker"]: lambda dice: 5 in [dice.count(i) for i in range(1, 7)],
            lang["para"]: lambda dice: 2 in [dice.count(i) for i in range(1, 7)],
            lang["2para"]: lambda dice: [dice.count(i) for i in range(1, 7)].count(2) == 2,
            lang["troika"]: lambda dice: 3 in [dice.count(i) for i in range(1, 7)],
            lang["little_street"]: lambda dice: [dice.count(i) for i in range(1, 7)].count(1) == 5 and
                                        [dice.count(i) for i in range(1, 7)][5] == 0,
           lang["big_street"]: lambda dice: [dice.count(i) for i in range(1, 7)].count(1) == 5 and
                                          [dice.count(i) for i in range(1, 7)][0] == 0,
            lang["chet"]: lambda dice: sum(1 for val in dice if val % 2 == 0) == 5,
            lang['nechet']: lambda dice: sum(1 for val in dice if val % 2 != 0) == 5,
            lang["fulhaus"]: lambda dice: 3 in [dice.count(i) for i in range(1, 7)] and 2 in [dice.count(i) for i in
                                                                                          range(1, 7)],
            lang["care"]: lambda dice: 4 in [dice.count(i) for i in range(1, 7)],
            lang["shans"]: lambda dice: sum(dice)
        }
        log_to_file("Combinations initialized",start_time_=start_time_)
        def on_resize(event=None):

            global points0, dice_values

            canvas.delete("all")
            if event is None:
                ChirinaWin = Win.winfo_width()
                VisotaWin = Win.winfo_height()
            else:
                ChirinaWin = event.width
                VisotaWin = event.height
            a = (ChirinaWin - 20 - 4 * 10) // 5

            centr = ChirinaWin // 2

            draw_dice(a, centr - 2 * a - 10 * 2, VisotaWin // 2, dice_values[0])
            draw_dice(a, centr - a - 10, VisotaWin // 2, dice_values[1])
            draw_dice(a, centr, VisotaWin // 2, dice_values[2])
            draw_dice(a, centr + a + 10, VisotaWin // 2, dice_values[3])
            draw_dice(a, centr + 2 * a + 10 * 2, VisotaWin // 2, dice_values[4])

            canvas.update()

        def draw_dice(a, x, y, n):
            log_to_file("Dice drawing",start_time_=start_time_)
            canvas.create_rectangle(x - a // 2, y - a // 2, x + a // 2, y + a // 2, fill=color_dice,
                                    activefill=activefill_dice)
            if n == 1: canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill="black")
            elif n == 2:
                canvas.create_oval(x - a // 2 + 10, y + a // 2 - 10, x - a // 2 + 30, y + a // 2 - 30, fill="black")
                canvas.create_oval(x + a // 2 - 10, y - a // 2 + 10, x + a // 2 - 30, y - a // 2 + 30, fill="black")
            elif n == 3:
                canvas.create_oval(x - a // 2 + 10, y + a // 2 - 10, x - a // 2 + 30, y + a // 2 - 30, fill="black")
                canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill="black")
                canvas.create_oval(x + a // 2 - 10, y - a // 2 + 10, x + a // 2 - 30, y - a // 2 + 30, fill="black")
            elif n == 4:
                canvas.create_oval(x - a // 2 + 10, y - a // 2 + 10, x - a // 2 + 30, y - a // 2 + 30, fill="black")
                canvas.create_oval(x - a // 2 + 10, y + a // 2 - 10, x - a // 2 + 30, y + a // 2 - 30, fill="black")
                canvas.create_oval(x + a // 2 - 10, y - a // 2 + 10, x + a // 2 - 30, y - a // 2 + 30, fill="black")
                canvas.create_oval(x + a // 2 - 10, y + a // 2 - 10, x + a // 2 - 30, y + a // 2 - 30, fill="black")
            elif n == 5:
                canvas.create_oval(x - a // 2 + 10, y - a // 2 + 10, x - a // 2 + 30, y - a // 2 + 30, fill="black")
                canvas.create_oval(x - a // 2 + 10, y + a // 2 - 10, x - a // 2 + 30, y + a // 2 - 30, fill="black")
                canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill="black")
                canvas.create_oval(x + a // 2 - 10, y - a // 2 + 10, x + a // 2 - 30, y - a // 2 + 30, fill="black")
                canvas.create_oval(x + a // 2 - 10, y + a // 2 - 10, x + a // 2 - 30, y + a // 2 - 30, fill="black")
            elif n == 6:
                canvas.create_oval(x - a // 2 + 10, y - a // 2 + 10, x - a // 2 + 30, y - a // 2 + 30, fill="black")
                canvas.create_oval(x - a // 2 + 10, y - 10, x - a // 2 + 30, y + 10, fill="black")
                canvas.create_oval(x - a // 2 + 10, y + a // 2 - 10, x - a // 2 + 30, y + a // 2 - 30, fill="black")
                canvas.create_oval(x + a // 2 - 10, y - a // 2 + 10, x + a // 2 - 30, y - a // 2 + 30, fill="black")
                canvas.create_oval(x + a // 2 - 10, y - 10, x + a // 2 - 30, y + 10, fill="black")
                canvas.create_oval(x + a // 2 - 10, y + a // 2 - 10, x + a // 2 - 30, y + a // 2 - 30, fill="black")
        def apply_changes(dialog):
            log_to_file('Apply changes',start_time_=start_time_)
            global roll_count, dice_values, call_count, turn
            selected_dice = [var.get() for var in check_vars]
            for i, selected in enumerate(selected_dice):
                if selected: dice_values[i] = random.randint(1, 6)
            on_resize()
            roll_count += 1
            if roll_count >= 3:
                dialog.destroy()
                if phase == "obligatory": select_nominal()
                else: select_combination()
            else:
                dialog.destroy()
                open_roll_dialog()
        def askinteger(win, title, prompt, minvalue=None, maxvalue=None):
            def on_ok():
                try:
                    value = int(entry.get())
                    if (minvalue is not None and value < minvalue) or \
                            (maxvalue is not None and value > maxvalue):
                        raise ValueError
                    result[0] = value
                    dialog.destroy()
                except ValueError:
                    messagebox.showwarning(lang["error"],
                                           f"{lang['enter_num_from']} {minvalue} {lang['to']} {maxvalue}" if minvalue is not None and maxvalue is not None else lang["enter_integer"])

            def on_cancel():
                result[0] = None
                dialog.destroy()

            result = [None]

            dialog = Toplevel(win)
            dialog.attributes('-topmost', True)
            img = Image.open("icons/poker.png")
            icon_image = ImageTk.PhotoImage(img)
            dialog.iconphoto(False, icon_image)
            dialog.title(title)
            askint_x = Win.winfo_x() + Win.winfo_width() // 2 - 135
            askint_y = Win.winfo_y() - Win.winfo_height() // 2 + 135
            if askint_x < 0: askint_x = 100
            if askint_y < 0: askint_y = 100
            dialog.geometry(f"+{askint_x}+{askint_y}")
            dialog.resizable(False, False)
            Label(dialog, text=prompt).grid(row=0, column=0, padx=10, pady=10)
            entry = Entry(dialog)
            entry.grid(row=1, column=0, padx=10, pady=10)

            Button(dialog, text="OK", command=on_ok).grid(row=2, column=0, padx=10, pady=10)
            Button(dialog, text="Cancel", command=on_cancel).grid(row=2, column=1, padx=10, pady=10, sticky=W)

            dialog.transient(win)
            dialog.grab_set()
            win.wait_window(dialog)

            return result[0]
        def select_nominal():
            global turn, roll_count, scores, obligatory_scores, call_count, chosen_nominals, phase
            roll_count = 0
            available_nominals = [i for i in range(1, 7) if i not in chosen_nominals[turn]]
            nominal = askinteger(Win, lang["vibornominal"],
                                 f"{players[turn]}, {lang['select_nominal']} ({', '.join(map(str, available_nominals))}):",
                                 1, 6)

            if nominal and nominal in available_nominals:
                chosen_nominals[turn].append(nominal)
                count = dice_values.count(nominal)
                score = count - 3
                scores[turn] += score
                obligatory_scores[turn] += score
                matches_played[turn] += 1
                if matches_played[turn] == 6 and all(match == 6 for match in matches_played):
                    show_obligatory_results()
                    phase = "main"
                    for i in range(len(matches_played)):
                        matches_played[i] = 0
                    automatic_roll()
                else:
                    next_turn()
            else:
                messagebox.showerror(lang["error"], lang["invaid_nominal"])
                select_nominal()
        def show_obligatory_results():
            results = "\n".join(f"{players[i]}: {obligatory_scores[i]}" for i in range(len(players)))
            messagebox.showinfo(lang["obyaz_finish"], f"{lang['etap_finish']}\n{results}")

        def select_combination():
            global turn, roll_count, scores, call_count, phase, dialog_combination
            if dialog_combination:dialog_combination.destroy()

            roll_count = 0
            available_combinations = [comb for comb in combinations.keys() if comb not in chosen_combinations[turn]]
            dialog_combination = Toplevel(Win)
            dialog_combination.attributes('-topmost', True)
            img = Image.open("icons/poker.png")
            icon_image = ImageTk.PhotoImage(img)
            dialog_combination.iconphoto(False, icon_image)
            dialog_combination.title(f"{players[turn]}")
            dialog_combination.geometry("200x400")
            dialog_combination.transient(Win)
            dialog_combination.grab_set()
            center_child(dialog_combination, Win)
            dialog_combination.protocol("WM_DELETE_WINDOW", lambda: dismiss(dialog_combination))

            Label(dialog_combination, text=f"{players[turn]}, {lang['select_comb']}").pack(pady=10)

            selected_combination = StringVar()
            for comb in available_combinations:
                ttk.Radiobutton(dialog_combination, text=comb, variable=selected_combination, value=comb).pack(
                    anchor='w')

            def on_ok():
                combination = selected_combination.get()
                if combination in available_combinations:
                    score = combinations[combination](dice_values)
                    if score > 0:
                        scores[turn] += score
                        matches_played[turn] += 1
                        chosen_combinations[turn].append(combination)
                        dialog_combination.destroy()
                        if matches_played[turn] == 6 and all(match == 6 for match in matches_played):
                            show_final_results()
                            return
                        next_turn()
                    else:
                        messagebox.showerror(lang["error"],
                                             lang["invalid_selected_comb"])
                else:
                    messagebox.showerror(lang["error"],
                                         lang["invalid_comb"])

            ttk.Button(dialog_combination, text=lang["okay"], width=7, command=on_ok).pack(pady=10)
            Win.wait_window(dialog_combination)
        def show_final_results():
            log_to_file("Show final results",start_time_=start_time_)
            global dialog_roll, dialog_combination
            results = "\n".join(
                f"{players[i]}: {scores[i]} {lang['vtch']} {obligatory_scores[i]})" for i in
                range(len(players)))

            Resulttt_win = create_window(Win, lang['game_finish'], global_bg, float(GlobalAlpha), 250, 250,
                              "icons/poker.png")
            center_child(Resulttt_win, Win)

            Resulttt_win.protocol("WM_DELETE_WINDOW", lambda: dismiss(Resulttt_win))

            lbl = Label(Resulttt_win, text=f"{lang['itog_score']}\n{results}")
            lbl.pack()

            btn = ttk.Button(Resulttt_win, text=lang["exit"], command=on_closing)
            btn.pack()

            Resulttt_win.grab_set()

            Win.wait_window(Resulttt_win)
        def dismiss(window):
            window.grab_release()
            window.destroy()
        def next_turn():
            global call_count, turn, roll_count, phase
            canvas.delete("all")

            if phase == "obligatory" and all(match == 6 for match in matches_played):
                phase = "main"
                for i in range(len(matches_played)):
                    matches_played[i] = 0
                show_obligatory_results()
                automatic_roll()
            else:
                turn = (turn + 1) % len(players)
                roll_count = 0
                status_label.config(text=f"{lang['hod']} {players[turn]}")
                automatic_roll()
                if phase == "main" and all(
                        len(chosen_combinations[turn]) == len(combinations) for turn in range(len(players))):
                    show_final_results()
                    return
                if matches_played[turn] < 6: open_roll_dialog()
                else: next_turn()
        def center_up(Win, parent):
            Win.update_idletasks()
            parent.update_idletasks()
            parent_width = parent.winfo_width()
            parent_x = parent.winfo_x()
            parent_y = parent.winfo_y()

            child_width = Win.winfo_width()
            child_height = Win.winfo_height()

            x = parent_x + parent_width // 2 - child_width // 2
            y = parent_y - child_height // 2

            Win.geometry(f'{child_width}x{child_height}+{x}+{y}')
        def center_child(Win, parent):
            Win.update_idletasks()
            parent.update_idletasks()
            parent_width = parent.winfo_width()
            parent_height = parent.winfo_height()
            parent_x = parent.winfo_x()
            parent_y = parent.winfo_y()

            child_width = Win.winfo_width()
            child_height = Win.winfo_height()

            x = parent_x + parent_width // 2 - child_width // 2
            y = parent_y + parent_height // 2 - child_height // 2

            Win.geometry(f'{child_width}x{child_height}+{x}+{y}')
        def automatic_roll():
            global dice_values
            dice_values = [random.randint(1, 6) for _ in range(5)]

            width = canvas.winfo_width()
            height = canvas.winfo_height()
            a = (width - 20 - 4 * 10) // 5
            centr = width // 2

            for i, value in enumerate(dice_values):
                x = centr - 2 * a + i * (a + 10)
                y = height // 2
                draw_dice(a, x, y, value)
            open_roll_dialog()
        def open_roll_dialog():
            global roll_count, check_vars, phase, dialog_roll
            if dialog_roll: dialog_roll.destroy()

            dialog_roll = Toplevel(Win)
            dialog_roll.attributes('-topmost', True)
            img = Image.open("icons/poker.png")
            icon_image = ImageTk.PhotoImage(img)
            dialog_roll.iconphoto(False, icon_image)
            dialog_roll.title(f"{lang['perebrosit']} {players[turn]}")
            dialog_roll.transient(Win)
            dialog_roll.geometry("240x200")
            dialog_roll.grab_set()
            center_up(dialog_roll, Win)
            dialog_roll.protocol("WM_DELETE_WINDOW", lambda: dismiss(dialog_roll))

            top_frame = Frame(dialog_roll)
            top_frame.pack(side="top", fill="both", expand=True, padx=10, pady=10)

            checkbox_frame = Frame(top_frame)
            checkbox_frame.pack(side="left", fill="y", anchor="n")

            label_frame = Frame(top_frame)
            label_frame.pack(side="right", fill="both", anchor="n", expand=True)

            button_frame = Frame(dialog_roll)
            button_frame.pack(side="bottom", fill="both", expand=True)

            available_nominals = [i for i in range(1, 7) if i not in chosen_nominals[turn]]
            avaible_combination = ""
            if phase == "main":
                for comb in combinations.keys():
                    if comb not in chosen_combinations[turn]:
                        avaible_combination += comb + '\n'
                Label(label_frame, text=f"{lang['dost_comb']} \n {avaible_combination}", justify="left").pack(
                    anchor="e")
            else:
                Label(label_frame, text=f"{lang['dost_nominal']} \n {', '.join(map(str, available_nominals))}",
                      justify="left").pack(anchor="e")

            check_vars = [BooleanVar() for _ in range(5)]
            for i, var in enumerate(check_vars):
                ttk.Checkbutton(checkbox_frame, text=f"{lang['kubik']} {i + 1}", variable=var).pack(anchor="w")

            ttk.Button(button_frame, text=lang["pere"], command=lambda: apply_changes(dialog_roll)).pack(side="left",
                                                                                                          padx=10,
                                                                                                          pady=10)
            ttk.Button(button_frame, text=lang["not_pere"], command=lambda: [dialog_roll.destroy(),
                                                                               select_nominal() if phase == "obligatory" else select_combination()]).pack(
                side="right", padx=10, pady=10)

            Win.wait_window(dialog_roll)
        def parametr():
            log_to_file("Open parametrs",start_time_=start_time_)
            global color_dice, activefill_dice, color, background_color, theme

            parametrs_window = create_window(Win, lang['parametr'], global_bg, float(GlobalAlpha), 550, 550,
                                         "icons/poker.png")
            parametrs_window.resizable(False, False)
            center_child(parametrs_window, Win)
            parametrs_window.protocol("WM_DELETE_WINDOW",
                                      lambda: dismiss(parametrs_window))

            frmcolor = LabelFrame(parametrs_window, borderwidth=0.5, relief=SOLID, text=lang["color_kv"])
            frmcolor.grid(row=0, column=0, padx=5, pady=5, sticky=NW)

            choose_color_button = ttk.Button(frmcolor, text=lang["select"], command=lambda: choose_color(parametrs_window))
            choose_color_button.grid(row=0, column=0, padx=10, pady=5, sticky=W)

            frmcolor = LabelFrame(parametrs_window, borderwidth=0.5, relief=SOLID, text=lang["active_color_kv"])
            frmcolor.grid(row=0, column=1, padx=5, pady=5, sticky=NW)

            choose_color_button1 = ttk.Button(frmcolor, text=lang["select"], command=lambda: choose_color1(parametrs_window))
            choose_color_button1.grid(row=0, column=1, padx=10, pady=5, sticky=W)

            frmcolor = LabelFrame(parametrs_window, borderwidth=0.5, relief=SOLID, text=lang["bg_color"])
            frmcolor.grid(row=0, column=2, padx=5, pady=5, sticky=NW)

            color_var = StringVar()

            if background_color is None: background_color = "White"
            color_var.set(background_color)

            white = ttk.Radiobutton(frmcolor, text=lang["white"], variable=color_var, value="White")
            white.grid(row=0, column=0, sticky=W)
            black = ttk.Radiobutton(frmcolor, text=lang['black'], variable=color_var, value="Black")
            black.grid(row=1, column=0, sticky=W)
            gray = ttk.Radiobutton(frmcolor, text=lang['gray'], variable=color_var, value="Gray")
            gray.grid(row=2, column=0, sticky=W)
            green = ttk.Radiobutton(frmcolor, text=lang['green'], variable=color_var, value="Green")
            green.grid(row=3, column=0, sticky=W)
            blue = ttk.Radiobutton(frmcolor, text=lang['blue'], variable=color_var, value="Blue")
            blue.grid(row=4, column=0, sticky=W)
            goluboy = ttk.Radiobutton(frmcolor, text=lang["goluboi"], variable=color_var, value="Goluboy")
            goluboy.grid(row=5, column=0, sticky=W)
            violet = ttk.Radiobutton(frmcolor, text=lang['violet'], variable=color_var, value="Violet")
            violet.grid(row=6, column=0, sticky=W)
            yellow = ttk.Radiobutton(frmcolor, text=lang['yellow'], variable=color_var, value="Yellow")
            yellow.grid(row=7, column=0, sticky=W)
            malina = ttk.Radiobutton(frmcolor, text=lang['malina'], variable=color_var, value="Malina")
            malina.grid(row=8, column=0, sticky=W)
            aliy = ttk.Radiobutton(frmcolor, text=lang['aliy'], variable=color_var, value="Alyi")
            aliy.grid(row=0, column=1, sticky=W)
            begiviy = ttk.Radiobutton(frmcolor, text=lang["bezh"], variable=color_var, value="Begiviy")
            begiviy.grid(row=1, column=1, sticky=W)
            salatoviy = ttk.Radiobutton(frmcolor, text=lang['salat'], variable=color_var, value="Salat")
            salatoviy.grid(row=2, column=1, sticky=W)
            orange = ttk.Radiobutton(frmcolor, text=lang["orange"], variable=color_var, value="Orange")
            orange.grid(row=3, column=1, sticky=W)
            aqua = ttk.Radiobutton(frmcolor, text=lang["aqua"], variable=color_var, value="Aqua")
            aqua.grid(row=4, column=1, sticky=W)

            if color == "White":color_var.set("White")
            elif color == "Black":color_var.set("Black")
            elif color == "Gray":color_var.set("Gray")
            elif color == "Green":color_var.set("Green")
            elif color == "Blue":color_var.set("Blue")
            elif color == "#1E90FF":color_var.set("Goluboy")
            elif color == "#800080":color_var.set("Violet")
            elif color == "Yellow":color_var.set("Yellow")
            elif color == "#DC143C":color_var.set("Malina")
            elif color == "ff0d00":color_var.set("Alyi")
            elif color == "#FFE4E1":color_var.set("Begiviy")
            elif color == "#ADFF2F":color_var.set("Salat")
            elif color == "#FF8C00":color_var.set("Orange")
            elif color == "#00FFFF":color_var.set("Aqua")

            ok_button = ttk.Button(parametrs_window, text=lang["okay"], command=lambda: ok_click(color_var, parametrs_window))
            ok_button.grid(row=4, column=1, padx=5, pady=5, sticky=E)
            otmena_button = ttk.Button(parametrs_window, text=lang["cancel"], command=lambda: dismiss(parametrs_window))
            otmena_button.grid(row=4, column=2, padx=5, pady=5, sticky=W)
            canvas.update()
            parametrs_window.grab_set()
        def choose_color(parameters_window):
            global color_dice
            parameters_window.grab_release()
            color_code = colorchooser.askcolor(title=lang["colorchoser"],parent=Win)[1]
            parameters_window.grab_set()
            if color_code:color_dice = color_code
            key = load_key()
            with open("games/poker_settings/dice_color.cfg", "wb") as f:
                f.write(encrypt_message(str(color_dice), key))
            canvas.update()
            on_resize()
            parameters_window.focus_set()
        def choose_color1(parameters_window):
            global activefill_dice
            parameters_window.grab_release()
            color_code = colorchooser.askcolor(title=lang["colorchoser"],parent=Win)[1]
            parameters_window.grab_set()
            if color_code:activefill_dice = color_code
            key = load_key()
            with open("games/poker_settings/active_color.cfg", "wb") as f:
                f.write(encrypt_message(str(activefill_dice), key))
            on_resize()
            canvas.update()
            parameters_window.focus_set()
        def ok_click(color_var, parametrs_window):
            global color, background_color, color_dice, activefill_dice

            background_color = color_var.get()
            color = background_color

            if color_dice is None:color_dice = "Red"
            if activefill_dice is None:activefill_dice = "Yellow"

            if color_var.get() == "White":
                color = "White"
                background_color = "White"
            elif color_var.get() == "Black":
                color = "Black"
                background_color = "Black"
            elif color_var.get() == "Gray":
                color = "Gray"
                background_color = "Gray"
            elif color_var.get() == "Blue":
                color = "Blue"
                background_color = "Blue"
            elif color_var.get() == "Yellow":
                color = "Yellow"
                background_color = "Yellow"
            elif color_var.get() == "Yellow":
                color = "Yellow"
                background_color = "Yellow"
            elif color_var.get() == "Malina":
                color = "#DC143C"
                background_color = "#DC143C"
            elif color_var.get() == "Begiviy":
                color = "#FFE4E1"
                background_color = "#FFE4E1"
            elif color_var.get() == "Goluboy":
                color = "#1E90FF"
                background_color = "#1E90FF"
            elif color_var.get() == "Violet":
                color = "#800080"
                background_color = "#800080"
            elif color_var.get() == "Alyi":
                color = "ff0d00"
                background_color = "ff0d00"
            elif color_var.get() == "Salat":
                color = "#ADFF2F"
                background_color = "#ADFF2F"
            elif color_var.get() == "Aqua":
                color = "#00FFFF"
                background_color = "#00FFFF"
            elif color_var.get() == "Orange":
                color = "#FF8C00"
                background_color = "#FF8C00"
            else:
                color = "Green"
                background_color = "Green"
            key = load_key()
            with open("games/poker_settings/bg.cfg","wb") as f:
                f.write(encrypt_message(str(background_color),key))
            parametrs_window.destroy()
            update_canvas_background()
            on_resize()
        def update_canvas_background():
            global background_color
            canvas.config(bg=background_color)
        def exit_cascade(event=None):

            def yes_button():
                global flag
                flag = True

                conn = sqlite3.connect('games/playersinfo_poker.db')

                cursor = conn.cursor()

                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS players (
                        id INTEGER PRIMARY KEY,
                        name TEXT,
                        color_dice TEXT,
                        background_color TEXT,
                        score INTEGER,
                        time TEXT
                    )
                ''')

                for player, score in zip(players, scores):
                    cursor.execute('''
                        INSERT INTO players (name, color_dice, background_color, score, time) 
                        VALUES (?, ?, ?, ?, ?)
                    ''', (player, color_dice, background_color, score, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

                cursor.execute('''SELECT * FROM players''')
                rows = cursor.fetchall()

                conn.commit()

                conn.close()
                exit_win.destroy()
                Win.destroy()

            def non_button():
                exit_win.destroy()

            exit_win = create_window(Win, lang['exit'], global_bg, float(GlobalAlpha), 250, 120,
                                     "icons/poker.png")
            exit_win.resizable(False, False)

            center_child(exit_win, Win)
            exit_win.protocol("WM_DELETE_WINDOW", lambda: dismiss(exit_win))

            label1 = Label(exit_win, text=lang["you_sure_to_exit"])
            label1.pack()
            btn1 = ttk.Button(exit_win, text=lang["yes_coor"], command=yes_button)
            btn1.pack()
            btn2 = ttk.Button(exit_win, text=lang["no_coor"], command=non_button)
            btn2.pack()
            exit_win.grab_set()
        def on_closing():
            global flag
            flag = True
            if flag == True:
                conn = sqlite3.connect('games/playersinfo_poker.db')
                cursor = conn.cursor()
                cursor.execute('''
                                        CREATE TABLE IF NOT EXISTS players (
                            id INTEGER PRIMARY KEY,
                            name TEXT,
                            color_dice INTEGER,
                            background_color INTEGER,
                            score INTEGER,
                            time TEXT
                                        )
                                    ''')
                current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                for player, score in zip(players, scores):
                    cursor.execute('''
                        INSERT INTO players (name, color_dice, background_color, score, time) 
                        VALUES (?, ?, ?, ?, ?)
                    ''', (player, color_dice, background_color, score, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
                cursor.execute('''SELECT * FROM players ''')
                conn.commit()
                conn.close()

            Win.destroy()
        def win_booster():
            def no_activ_booster():
                booster_win.destroy()

            booster_win = create_window(Win, lang['busters'], global_bg, float(GlobalAlpha), 400, 150,
                                     "icons/poker.png")
            booster_win.resizable(False, False)
            center_child(booster_win, Win)
            booster_win.protocol("WM_DELETE_WINDOW",
                                 lambda: dismiss(booster_win))
            lbl = Label(booster_win, text=lang["infobuster"])
            lbl.pack()
            lbl1 = Label(booster_win, text=lang["inof2buster"])
            lbl1.pack()
            btn1 = ttk.Button(booster_win, text=lang["activatebuster"], command=booster_activate)
            btn1.pack()
            btn2 = ttk.Button(booster_win, text=lang["notactivatebuster"], command=no_activ_booster)
            btn2.pack()
        def data_razrab():
            n = messagebox.showinfo(title=lang["developpers_data"],
                                    message=lang["developpercoor"])
        def data_game():
            messagebox.showinfo(title=lang["game_data"],
                                message=lang["infocoord_"])
        def all_data_users():
            all_data_users_win = create_window(Win, lang['all_user_data'], global_bg, float(GlobalAlpha), 650, 350,
                                        "icons/poker.png")
            all_data_users_win.resizable(False, False)

            center_child(all_data_users_win, Win)
            all_data_users_win.protocol("WM_DELETE_WINDOW",
                                        lambda: dismiss(all_data_users_win))
            n = Text(all_data_users_win)
            scrollbar = Scrollbar(all_data_users_win, command=n.yview)
            n.config(yscrollcommand=scrollbar.set)
            scrollbar.pack(side=RIGHT, fill=Y)
            n.pack()

            conn = sqlite3.connect('games/playersinfo_poker.db')
            cursor = conn.cursor()
            cursor.execute('''SELECT name,
                    score,
                   color_dice, 
                    background_color,
                   time
            FROM players
            ORDER BY name DESC;''')
            rows = cursor.fetchall()
            columns = ["Name", "Score", "Color_dice ", "Background_color", "Time"]

            results = tabulate.tabulate(rows, headers=columns, tablefmt="center")

            n.insert(1.0, str(results) + '\n')
            conn.commit()
            conn.close()
            all_data_users.grab_set()
        def data_users():
            data_users_win = create_window(Win, lang['sokr_data'], global_bg, float(GlobalAlpha), 450, 350,
                                        "icons/poker.png")
            data_users_win.resizable(False, False)
            center_child(data_users_win, Win)
            data_users_win.protocol("WM_DELETE_WINDOW",
                                    lambda: dismiss(data_users_win))
            n = Text(data_users_win)
            scrollbar = Scrollbar(data_users_win, command=n.yview)
            n.config(yscrollcommand=scrollbar.set)
            scrollbar.pack(side=RIGHT, fill=Y)
            n.pack()

            conn = sqlite3.connect('games/playersinfo_poker.db')
            cursor = conn.cursor()
            cursor.execute('''SELECT name, SUM(score) AS total_score
                    FROM players
                    GROUP BY name
                    ORDER BY total_score DESC;''')
            rows = cursor.fetchall()
            columns = ["Name", "Score"]

            results = tabulate.tabulate(rows, headers=columns, tablefmt="center")

            n.insert(1.0, str(results) + '\n')
            conn.commit()
            conn.close()
            data_users.grab_set()
        def booster_activate():
            global booster_active, last_booster_activation_time

            if last_booster_activation_time is not None:
                time_passed = datetime.now() - last_booster_activation_time
                if time_passed < timedelta(hours=6):
                    remaining_time = timedelta(hours=6) - time_passed
                    messagebox.showinfo(f"{lang['busternedos']}",
                                        f"{lang['timetoactivate']} {remaining_time}.")
                    return

            booster_active = True
            last_booster_activation_time = datetime.now()
            messagebox.showinfo(lang["boosteractivated"],
                                lang["your_scorehas_been_double"])
            Win.after(180000, booster_deactivate)
        def booster_deactivate():
            global booster_active
            booster_active = False
            messagebox.showinfo(lang["booster_deactivated"], lang["deistvie_zak"])
        def config_win1():
            Win.update_idletasks()

            screen_width = Win.winfo_screenwidth()
            screen_height = Win.winfo_screenheight()

            x = int((screen_width / 2) - (screen_width / 2))
            y = int((screen_height / 2) - (screen_height / 2))

            Win.geometry(f"{screen_width}x{screen_height}+{x}+{y}")

            Win.state('zoomed')
        def pravila():

            pravila_win = create_window(Win, lang['pravila'], global_bg, float(GlobalAlpha), 750, 400,
                          "icons/poker.png")
            pravila_win.resizable(False, False)
            center_child(pravila_win, Win)
            pravila_win.protocol("WM_DELETE_WINDOW",
                                 lambda: dismiss(pravila_win))
            font_settings = ("Arial", 15, "bold")
            lbl = Label(pravila_win,
                        text=lang["pravila1"], font=font_settings)

            lbl.pack()
            setting = ("Arial", 9, "bold")
            lbl1 = Label(pravila_win,
                         text=lang["all_pravila"],
                         font=setting)

            lbl1.pack()
            btn = ttk.Button(pravila_win, text=lang["pereiti"], command=help_user)
            btn.pack()
            pravila_win.grab_set()

        def help_user():
            help_win = create_window(Win, lang['ob_comb'], global_bg, float(GlobalAlpha), 450, 350,
                          "icons/poker.png")
            help_win.resizable(False, False)
            center_child(help_win, Win)
            help_win.protocol("WM_DELETE_WINDOW",
                              lambda: dismiss(help_win))
            lbl = Label(help_win,
                        text=lang["all_ob"])
            lbl.pack()
            help_win.grab_set()

        def start_game():
            global call_count, turn, dice_values, roll_count, players, scores, obligatory_scores, matches_played, chosen_nominals, chosen_combinations, phase
            call_count = 0
            turn = 0
            dice_values = [random.randint(1, 6) for _ in range(5)]
            num_players = simpledialog.askinteger(lang['kolvo_players'], lang["enter_players"], minvalue=2,
                                                  maxvalue=5, parent=Win)
            if num_players:
                players = [simpledialog.askstring(lang["player_name"], f"{lang['enter_name_player']} {i + 1}:", parent=Win) for i in
                           range(num_players)]

                scores = [0 for _ in range(num_players)]
                obligatory_scores = [0 for _ in range(num_players)]
                matches_played = [0 for _ in range(num_players)]
                chosen_nominals = [[] for _ in range(num_players)]
                chosen_combinations = [[] for _ in range(num_players)]
                phase = "obligatory"
                turn = 0
                call_count = 0
                dice_values = [random.randint(1, 6) for _ in range(5)]
                status_label.config(text=f"{lang['hod']} {players[turn]}")

                on_resize()
                open_roll_dialog()

        Win = Toplevel(root)
        
        img = Image.open("icons/poker.png")
        icon_image = ImageTk.PhotoImage(img)
        Win.iconphoto(False, icon_image)
        Win.title(lang["poker_na_kos"])
        Win.minsize(450, 250)
        Win.resizable(True, True)
        Win.option_add("*tearOff", FALSE)
        VisotaScreen = Win.winfo_screenheight()
        ChirinaScreen = Win.winfo_screenwidth()
        VisotaWin = 450
        ChirinaWin = 900
        Win.geometry(
            f"{ChirinaWin}x{VisotaWin}+{ChirinaScreen // 2 - ChirinaWin // 2}+{VisotaScreen // 2 - VisotaWin // 2}")

        main_menu = Menu()
        info_menu = Menu()
        file_menu = Menu(main_menu, tearoff=0)
        view_menu = Menu()
        help_menu = Menu()
        main_menu.add_cascade(label=lang["game"], underline=0, menu=file_menu)
        file_menu.add_command(label=lang["start"], command=start_game)
        main_menu.add_cascade(label=lang["vid"], menu=view_menu)
        view_menu.add_cascade(label=lang["parametr"], command=parametr)
        view_menu.add_command(label=lang["ves_ecran"], command=config_win1)
        main_menu.add_cascade(label=lang["_info_"], menu=info_menu)
        main_menu.add_command(label=lang["busters"], command=win_booster)
        main_menu.add_cascade(label=lang["pravila"], menu=help_menu)
        help_menu.add_cascade(label=lang["ob_comb"], command=help_user)
        help_menu.add_cascade(label=lang["pravila"], command=pravila)
        main_menu.add_cascade(label=lang["exit"], command=exit_cascade)
        info_menu.add_command(label=lang["developpers_data"], command=data_razrab)
        info_menu.add_command(label=lang['game_data'], command=data_game)
        info_menu.add_command(label=lang['all_user_data'], command=all_data_users)
        info_menu.add_command(label=lang["sokr_data"], command=data_users)

        canvas = Canvas(Win, bg=background_color)
        canvas.pack(fill=BOTH, expand=YES)
        canvas.bind("<Configure>", on_resize)
        Win.config(menu=main_menu)
        Win.bind('<Escape>', exit_cascade)
        Win.bind('<Alt-F4>', exit_cascade)
        Win.protocol("WM_DELETE_WINDOW", on_closing)
        status_label = Label(Win, text=lang["welcome_to_game"])
        status_label.pack()

    main_window()