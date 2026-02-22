import random
from datetime import datetime
from tkinter import *
from tkinter import ttk,messagebox
import sqlite3
import tabulate
from crypto_work import encrypt_message,decrypt_message,load_key
from create_window import create_window

pika = "♠"
kresta = "♣"
bubna = "♦"
chirva = "♥"
masti = ["♠","♣","♦","♥"]
koloda = []
player1 = []
player2 = []
attack = [False,False]
hodplayer = [False,False]
otboy = []
round_attack = []
round_defender = []
background_color = ''
koloda2 = []
ind = False
name1 =""
name2 = ""
shrift = ''
text_color = ''
win = False
score = 0
ident = ""

key = load_key()
with open("games/durak_settings/txt_color.cfg", "rb") as f:
    text_color = decrypt_message(f.read(),key)
with open("games/durak_settings/police.cfg", "rb") as f:
    shrift = decrypt_message(f.read(),key)
with open("games/durak_settings/bg.cfg", "rb") as f:
    background_color = decrypt_message(f.read(),key)
def durak(root,lang,start_time_,global_bg,GlobalAlpha):
    def on_enter(event):
        canvas.itemconfig(event.widget.find_withtag("current"), fill="#D3D3D3")

    def on_leave(event):
        canvas.itemconfig(event.widget.find_withtag("current"), fill="white")

    def comparison_cart(cart1, cart2, koz):
        a = False
        if cart2[1] == cart1[1]:
            if cart2[0] > cart1[0]:
                a = True
        else:
            if cart2[1] == koz[1]:
                a = True
        return a

    def draw_all_carts():
        global player1, player2, round_attack, round_defender
        masht = 1
        width = canvas.winfo_width()
        player = hod_player()

        card_width = 190
        max_cards_per_row = int((width - 10) / (card_width * masht))

        if len(player) > max_cards_per_row:
            masht = (width - 10) / (card_width * len(player))

        canvas.delete("all")
        x = 10
        y = 10
        for card in player:
            if x > (width - 100):
                x = 10
                y += 150
            draw_cart(card[0], card[1], x, y, masht)
            x += 190 * masht

        if len(koloda) > 0:
            draw_cart(koloda[len(koloda) - 1][0], koloda[len(koloda) - 1][1], 10, 510, 1)
            if background_color == "black":
                canvas.create_rectangle(10, 400, 170, 500, fill="gray")
            else:
                canvas.create_rectangle(10, 400, 170, 500, fill="black")
            canvas.create_text(90, 450, text=len(koloda), font=("Arial 35"), fill="white")

        x = 300
        y = 300
        for card in round_attack:
            draw_cart(card[0], card[1], x, y, 1)
            x += 190
        x = 300
        for card in round_defender:
            draw_cart(card[0], card[1], x + 10, y + 130, 1)
            x += 190

    def draw_cart(n, m, x, y, k):
        width = 160 * k
        height = 210 * k

        rect_id = canvas.create_rectangle(x, y, x + width, y + height, activefill="#D3D3D3", fill="white")
        canvas.tag_bind(rect_id, "<Enter>", on_enter)
        canvas.tag_bind(rect_id, "<Leave>", on_leave)

        if n == 11:
            n = "J"
        elif n == 12:
            n = "Q"
        elif n == 13:
            n = "K"
        elif n == 14:
            n = "A"

        color = "red" if m in [bubna, chirva] else "black"
        canvas.create_text(
            x + 10 * k,
            y + 10 * k,
            text=str(n),
            font=("Arial", int(10 * k)),
            fill=color
        )
        canvas.create_text(
            x + width // 2,
            y + height // 2,
            text=m,
            font=("Arial", int(35 * k)),
            fill=color
        )
        canvas.create_text(
            x + width - 10 * k,
            y + height - 10 * k,
            text=str(n),
            font=("Arial", int(10 * k)),
            fill=color
        )

    def dismiss(window):
        window.grab_release()
        window.destroy()

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

    def show_selected_cards(hod, selected_card):
        def proverka():
            if round_attack:
                if show_attack_player() == hod_player():
                    flag = False
                    for card in round_attack:
                        if player[selected_card][0] == card[0]:
                            flag = True
                            break
                    if not flag:
                        for card in round_defender:
                            if player[selected_card][0] == card[0]:
                                flag = True
                                break
                    return flag
                else:
                    return True
            else:
                return True

        def proverka2():
            if hod_player() != show_attack_player():
                if round_attack:
                    return comparison_cart(round_attack[len(round_attack) - 1], player[selected_card],
                                           koloda2[len(koloda2) - 1])
                else:
                    return True
            else:
                return True

        global otboy_round, round_attack, hodplayer
        change_hod()
        player = hod_player()

        if proverka():
            if proverka2():
                if (attack[0] and hodplayer[0]) or (attack[1] and hodplayer[1]):
                    round_attack.append(player[selected_card])
                else:
                    round_defender.append(player[selected_card])
                player.remove(player[selected_card])
                change_hod()
                dismiss(hod)
                if finish():
                    finish1()
                else:
                    draw_all_carts()
                    choice_card()
            else:
                messagebox.showerror(lang['error'], lang["invalid_card"])
                choice_card()
        else:
            messagebox.showerror(lang['error'], f"{player[selected_card]} {lang['nemo_podk']}")
            choice_card()

    def show_attack_player():
        global player1, player2, attack

        if attack[0]:
            return player1
        else:
            return player2

    def change_hod():
        global hodplayer
        if hodplayer[1]:
            hodplayer[0] = True
            hodplayer[1] = False
        else:
            hodplayer[0] = False
            hodplayer[1] = True

    def change_player(player):
        global hodplayer
        if player == player1:
            hodplayer[0] = False
            hodplayer[1] = True
            return player2
        else:
            hodplayer[0] = True
            hodplayer[1] = False
            return player1

    def hod_player():
        global hodplayer
        if hodplayer[0]:
            return player1
        else:
            return player2

    def otboy_(hod):
        global round_attack, round_defender, otboy, player1, player2, koloda, attack, hodplayer
        dismiss(hod)
        for card in round_attack:
            otboy.append(card)
        for card in round_defender:
            otboy.append(card)
        round_attack.clear()
        round_defender.clear()

        while len(player1) < 6 and len(koloda) > 0:
            player1.append(koloda[0])
            koloda.remove(koloda[0])

        while len(player2) < 6 and len(koloda) > 0:
            player2.append(koloda[0])
            koloda.remove(koloda[0])
        change_attack()
        draw_all_carts()
        choice_card()

    def vzyat(hod):
        dismiss(hod)
        global round_attack, round_defender, otboy, hodplayer, attack
        player = show_attack_player()
        player = change_player(player)
        for card in round_attack:
            player.append(card)
        for card in round_defender:
            player.append(card)
        if len(player1) < 6:
            while len(player1) < 6 and len(koloda) > 0:
                player1.append(koloda[0])
                koloda.remove(koloda[0])
        if len(player2) < 6:
            while len(player2) < 6 and len(koloda) > 0:
                player2.append(koloda[0])
                koloda.remove(koloda[0])
        canvas.delete("all")
        round_attack.clear()
        round_defender.clear()
        change_hod()
        draw_all_carts()
        choice_card()

    def prom(player, selected_card, batl):
        global round_attack, round_defender, koloda, player1, player2
        vibor = player[selected_card]
        if comparison_cart(round_attack[len(round_attack) - 1], vibor, koloda2[len(koloda2) - 1]):
            # messagebox.showinfo("Игра в дурака", "Карта побита")
            player.remove(vibor)
            round_defender.append(vibor)
            dismiss(batl)
            canvas.delete("all")
            draw_all_carts()
        else:
            messagebox.showerror(lang['error'], lang["invalidcard1"])
            choice_card()

    def change_attack():
        global attack
        if attack[0]:
            attack[0] = False
            attack[1] = True
        else:
            attack[0] = True
            attack[1] = False

    def choice_card():
        global hodplayern, langue
        player = hod_player()
        if player == player1:
            hodplayer[0] = False
            hodplayer[1] = True
        else:
            hodplayer[0] = True
            hodplayer[1] = False
        if win:
            pass
        else:

            if player == player1:
                canvas.create_text(100, 300, text=f"{lang['play']} {name1}", tags="player", font=(shrift, 20),
                                       fill=text_color)
            else:
                canvas.create_text(100, 300, text=f"{lang['play']} {name2}", tags="player", font=(shrift, 20),
                                       fill=text_color)

            hod = create_window(win, lang["game_durak"], global_bg, float(GlobalAlpha), 300, 200, "icons/interface/durak.png")
            hod.resizable(False, True)
            center_child(hod, Win)
            hod.protocol("WM_DELETE_WINDOW", lambda: None)
            lbl = Label(hod, text=lang["select_card"])
            lbl.pack()
            selected_card = IntVar(value=0)

            for i, card in enumerate(player):
                if card[0] == 11:
                    text = "J" + str(card[1])
                elif card[0] == 12:
                    text = "Q" + str(card[1])
                elif card[0] == 13:
                    text = "K" + str(card[1])
                elif card[0] == 14:
                    text = "A" + str(card[1])
                else:
                    text = str(card[0]) + str(card[1])

                ttk.Radiobutton(hod, text=text, value=i, variable=selected_card).pack()
            btn = ttk.Button(hod, text=lang['okay'], command=lambda: show_selected_cards(hod, selected_card.get()))
            btn.pack()
            if (hodplayer[0] and attack[0]) or (hodplayer[1] and attack[1]):
                btn1 = ttk.Button(hod, text=lang["vzyat"], command=lambda: vzyat(hod))
                btn1.pack()
            else:
                btn1 = ttk.Button(hod, text=lang["otboi"], command=lambda: otboy_(hod))
                btn1.pack()
            hod.grab_set()

    def pr():
        canvas.delete("welcome_text")
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()
        message = lang["welcome_in_durak"]
        canvas.create_text(
            canvas_width // 2,
            canvas_height // 2 - 80,
            text=message,
            font=(shrift, 55),
            tags="welcome_text",
            fill=text_color,
            anchor='center'
        )

    def start_game():
        def start(pole, pole1):
            global ind, player1, player2, name1, name2, attack
            ind = True
            canvas.delete("welcome_text")

            pl.destroy()
            global koloda, player1, player2, koloda2

            for i in range(4):
                for j in range(6, 15):
                    koloda.append((j, masti[i]))

            random.shuffle(koloda)
            koloda2 = koloda.copy()
            koz1 = []
            koz2 = []
            for k in range(6):
                player1.append(koloda[0])
                if koloda[0][1] == koloda[len(koloda) - 1][1]:
                    koz1.append(koloda[0])
                koloda.remove(koloda[0])
                player2.append(koloda[0])
                if koloda[0][1] == koloda[len(koloda) - 1][1]:
                    koz2.append(koloda[0])
                koloda.remove(koloda[0])
            if len(koz1) > 0:
                koz1.sort(key=lambda x: x[0])
            if len(koz2) > 0:
                koz2.sort(key=lambda x: x[0])

            if len(koz1) > 0 and len(koz2) > 0:
                if koz1[0] < koz2[0]:
                    attack[0] = True
                    attack[1] = False
                else:
                    attack[0] = False
                    attack[1] = True
            elif len(koz1) == 0 and len(koz2) == 0:
                player1.sort(key=lambda x: x[0])
                player2.sort(key=lambda x: x[0])
                if player1[0][0] != player2[0][0]:
                    if player1[0][0] < player2[0][0]:
                        attack[0] = True
                        attack[1] = False
                    else:
                        attack[0] = False
                        attack[1] = True
                else:
                    if player1[1][0] < player2[1][0]:
                        attack[0] = True
                        attack[1] = False
                    else:
                        attack[0] = False
                        attack[1] = True
            elif len(koz1) == 0:
                attack[0] = False
                attack[1] = True
            else:
                attack[0] = True
                attack[1] = False
            if attack[0]:
                hodplayer[0] = True
                hodplayer[1] = False
            else:
                hodplayer[0] = False
                hodplayer[1] = True
            name1 = pole
            name2 = pole1
            draw_all_carts()
            choice_card()

        pl = create_window(win, lang["game_durak"], global_bg, float(GlobalAlpha), 300, 200, "icons/interface/durak.png")
        pl.resizable(False, False)
        center_child(pl, Win)
        pl.protocol("WM_DELETE_WINDOW",
                    lambda: dismiss(pl))
        lbl = Label(pl, text=lang['enter_name_1_player'])
        lbl.pack()
        pole = ttk.Entry(pl)
        pole.pack()
        lbl1 = Label(pl, text=lang['enter_name_2_player'])
        lbl1.pack()
        pole1 = ttk.Entry(pl)
        pole1.pack()
        btn = ttk.Button(pl, text=lang["okay"], command=lambda: start(pole.get(), pole1.get()))
        btn.pack()
        pl.grab_set()
    def parametrs():
        global background_color, shrift, text_color

        def close():
            dismiss(parametrs_window)

        def prim():
            parametrs_window.destroy()
            global background_color, shrift, text_color

            if color_var.get() == "white":
                background_color = "white"
            elif color_var.get() == "black":
                background_color = "black"
            elif color_var.get() == "green":
                background_color = "#008000"
            elif color_var.get() == "lime":
                background_color = "#00FF00"
            elif color_var.get() == "darkgreen":
                background_color = "#006400"
            elif color_var.get() == "blue":
                background_color = "#0000FF"
            elif color_var.get() == "goluboy":
                background_color = "#00FFFF"
            elif color_var.get() == "orange":
                background_color = "#FF8C00"
            elif color_var.get() == "pink":
                background_color = "#FF1493"
            elif color_var.get() == "gold":
                background_color = "#DAA520"
            elif color_var.get() == "violet":
                background_color = "#800080"
            elif color_var.get() == "darkred":
                background_color = "#8B0000"
            elif color_var.get() == "khaki":
                background_color = "#F0E68C"
            elif color_var.get() == "olive":
                background_color = "#808000"
            elif color_var.get() == "darkolive":
                background_color = "#556B2F"
            elif color_var.get() == "chocolate":
                background_color = "#D2691E"
            elif color_var.get() == "brown":
                background_color = "#800000"
            elif color_var.get() == "aquamarine":
                background_color = "#7FFFD4"
            elif color_var.get() == "indigo":
                background_color = "#4B0082"
            elif color_var.get() == "skay":
                background_color = "#87CEEB"
            elif color_var.get() == "tomat":
                background_color = "#FF6347"
            elif color_var.get() == "coral":
                background_color = "#FF7F50"
            elif color_var.get() == "lightcoral":
                background_color = "#F08080"
            elif color_var.get() == "indian":
                background_color = "#CD5C5C"
            elif color_var.get() == "azur":
                background_color = "#F0FFFF"
            elif color_var.get() == "snow":
                background_color = "#FFFAFA"
            elif color_var.get() == "salmon":
                background_color = "#FA8072"
            elif color_var.get() == "lavan":
                background_color = "#E6E6FA"
            elif color_var.get() == "medo":
                background_color = "#F0FFF0"
            elif color_var.get() == "bordov":
                background_color = "#32CD32"
            else:
                background_color = "gray"

            if shrift_var.get() == "1":
                shrift = "Arial"
            elif shrift_var.get() == "2":
                shrift = "Georgia"
            elif shrift_var.get() == "3":
                shrift = "Comic Sans MS"
            elif shrift_var.get() == "4":
                shrift = "Courier New"
            elif shrift_var.get() == "5":
                shrift = "Times New Roman"
            elif shrift_var.get() == "6":
                shrift = "Fixedsys"
            elif shrift_var.get() == "7":
                shrift = "Verdana Pro Black"
            elif shrift_var.get() == "8":
                shrift = "Montserrat Black"
            else:
                shrift = "Impact"
            if text_var.get() == "1":
                text_color = "Black"
            elif text_var.get() == "2":
                text_color = "White"
            elif text_var.get() == "3":
                text_color = "Red"
            elif text_var.get() == "4":
                text_color = "Yellow"
            elif text_var.get() == "5":
                text_color = "Orange"
            elif text_var.get() == "6":
                text_color = "Blue"
            elif text_var.get() == "7":
                text_color = "#00BFFF"
            elif text_var.get() == "8":
                text_color = "#FF00FF"
            elif text_var.get() == "10":
                text_color = "#4B0082"
            elif text_var.get() == "11":
                text_color = "#800000"
            elif text_var.get() == "12":
                text_color = "#DAA520"
            elif text_var.get() == "13":
                text_color = "#808000"
            elif text_var.get() == "14":
                text_color = "#00FF00"
            elif text_var.get() == "15":
                text_color = "#8B0000"
            elif text_var.get() == "16":
                text_color = "#7FFFD4"
            elif text_var.get() == "17":
                text_color = "#87CEEB"
            elif text_var.get() == "18":
                text_color = "#9ACD32"
            else:
                text_color = "#800080"
            key = load_key()
            with open("games/durak_settings/txt_color.cfg","wb") as f:
                f.write(encrypt_message(str(text_color),key))
            with open("games/durak_settings/police.cfg","wb") as f:
                f.write(encrypt_message(str(shrift),key))
            with open("games/durak_settings/bg.cfg","wb") as f:
                f.write(encrypt_message(str(background_color),key))
            canvas.config(bg=background_color)
            update_menu()
            Win.update_idletasks()
            pr()

        parametrs_window = create_window(win, lang["game_durak"], global_bg, float(GlobalAlpha), 900, 400, "icons/durak.png")
        parametrs_window.resizable(False, False)
        center_child(parametrs_window, Win)
        parametrs_window.protocol("WM_DELETE_WINDOW",
                                  lambda: dismiss(parametrs_window))

        backgroundfrm = LabelFrame(parametrs_window, text=lang["bg_color"], cursor="target")
        backgroundfrm.grid(row=0, column=0)
        color_var = StringVar(
            value=background_color)

        wh = ttk.Radiobutton(backgroundfrm, text=lang["white"], variable=color_var, value="white")
        wh.grid(row=1, column=0, sticky=W)

        bl = ttk.Radiobutton(backgroundfrm, text=lang["black"], variable=color_var, value="black")
        bl.grid(row=2, column=0, sticky=W)

        gr = ttk.Radiobutton(backgroundfrm, text=lang["green"], variable=color_var, value="green")
        gr.grid(row=3, column=0, sticky=W)

        bl = ttk.Radiobutton(backgroundfrm, text=lang['lime_'], variable=color_var, value="lime")
        bl.grid(row=4, column=0, sticky=W)

        gr = ttk.Radiobutton(backgroundfrm, text=lang['darkgreen'], variable=color_var, value="darkgreen")
        gr.grid(row=5, column=0, sticky=W)

        blu = ttk.Radiobutton(backgroundfrm, text=lang["blue"], variable=color_var, value="blue")
        blu.grid(row=6, column=0, sticky=W)

        gl = ttk.Radiobutton(backgroundfrm, text=lang["goluboi"], variable=color_var, value="goluboy")
        gl.grid(row=7, column=0, sticky=W)

        gra = ttk.Radiobutton(backgroundfrm, text=lang["gray"], variable=color_var, value="gray")
        gra.grid(row=8, column=0, sticky=W)
        ora = ttk.Radiobutton(backgroundfrm, text=lang["orange"], variable=color_var, value="orange")
        ora.grid(row=9, column=0, sticky=W)
        ora = ttk.Radiobutton(backgroundfrm, text=lang['green_lime'], variable=color_var, value="bordov")
        ora.grid(row=10, column=0, sticky=W)
        pin = ttk.Radiobutton(backgroundfrm, text=lang["pink"], variable=color_var, value="pink")
        pin.grid(row=1, column=1, sticky=W)
        viol = ttk.Radiobutton(backgroundfrm, text=lang["violet"], variable=color_var, value="violet")
        viol.grid(row=2, column=1, sticky=W)
        gol = ttk.Radiobutton(backgroundfrm, text=lang['gold_'], variable=color_var, value="gold")
        gol.grid(row=3, column=1, sticky=W)
        viol = ttk.Radiobutton(backgroundfrm, text=lang['darkred'], variable=color_var, value="darkred")
        viol.grid(row=4, column=1, sticky=W)
        gol = ttk.Radiobutton(backgroundfrm, text=lang["khaki"], variable=color_var, value="khaki")
        gol.grid(row=5, column=1, sticky=W)
        viol = ttk.Radiobutton(backgroundfrm, text=lang['olive_'], variable=color_var, value="olive")
        viol.grid(row=6, column=1, sticky=W)
        gol = ttk.Radiobutton(backgroundfrm, text=lang["darkolive"], variable=color_var, value="darkolive")
        gol.grid(row=7, column=1, sticky=W)
        gol = ttk.Radiobutton(backgroundfrm, text=lang["choco"], variable=color_var, value="chocolate")
        gol.grid(row=8, column=1, sticky=W)
        gol = ttk.Radiobutton(backgroundfrm, text=lang["marron"], variable=color_var, value="brown")
        gol.grid(row=9, column=1, sticky=W)
        gol = ttk.Radiobutton(backgroundfrm, text=lang['-med-'], variable=color_var, value="medo")
        gol.grid(row=10, column=1, sticky=W)
        ar = ttk.Radiobutton(backgroundfrm, text=lang['indigo'], variable=color_var, value="indigo")
        ar.grid(row=1, column=2, sticky=W)
        fyx = ttk.Radiobutton(backgroundfrm, text=lang['aquamarine'], variable=color_var, value="aquamarine")
        fyx.grid(row=2, column=2, sticky=W)
        fyx = ttk.Radiobutton(backgroundfrm, text=lang['tomat_'], variable=color_var, value="tomat")
        fyx.grid(row=3, column=2, sticky=W)
        fyx = ttk.Radiobutton(backgroundfrm, text=lang['coral'], variable=color_var, value="coral")
        fyx.grid(row=4, column=2, sticky=W)
        fyx = ttk.Radiobutton(backgroundfrm, text=lang['light_coral'], variable=color_var, value="lightcoral")
        fyx.grid(row=5, column=2, sticky=W)
        fyx = ttk.Radiobutton(backgroundfrm, text=lang['indian_viol'], variable=color_var, value="indian")
        fyx.grid(row=6, column=2, sticky=W)
        fyx = ttk.Radiobutton(backgroundfrm, text=lang['azure'], variable=color_var, value="azur")
        fyx.grid(row=7, column=2, sticky=W)
        fyx = ttk.Radiobutton(backgroundfrm, text=lang['sneg'], variable=color_var, value="snow")
        fyx.grid(row=8, column=2, sticky=W)
        fyx = ttk.Radiobutton(backgroundfrm, text=lang['losos'], variable=color_var, value="salmon")
        fyx.grid(row=9, column=2, sticky=W)
        fyx = ttk.Radiobutton(backgroundfrm, text=lang['lavande'], variable=color_var, value="lavan")
        fyx.grid(row=10, column=2, sticky=W)
        textfrm = LabelFrame(parametrs_window, text=lang['text_color'], cursor="target")
        textfrm.grid(row=0, column=3)

        text_var = StringVar(value=shrift)

        ar = ttk.Radiobutton(textfrm, text=lang['black'], variable=text_var, value="1")
        ar.grid(row=0, column=3, sticky=W)

        geo = ttk.Radiobutton(textfrm, text=lang['white'], variable=text_var, value="2")
        geo.grid(row=1, column=3, sticky=W)

        comic = ttk.Radiobutton(textfrm, text=lang['red'], variable=text_var, value="3")
        comic.grid(row=2, column=3, sticky=W)

        courier = ttk.Radiobutton(textfrm, text=lang['yellow'], variable=text_var, value="4")
        courier.grid(row=3, column=3, sticky=W)
        timess = ttk.Radiobutton(textfrm, text=lang['orange'], variable=text_var, value="5")
        timess.grid(row=4, column=3, sticky=W)

        fyx = ttk.Radiobutton(textfrm, text=lang['blue'], variable=text_var, value="6")
        fyx.grid(row=5, column=3, sticky=W)

        courier = ttk.Radiobutton(textfrm, text=lang['goluboi'], variable=text_var, value="7")
        courier.grid(row=6, column=3, sticky=W)
        timess = ttk.Radiobutton(textfrm, text=lang['pink'], variable=text_var, value="8")
        timess.grid(row=7, column=3, sticky=W)

        fyx = ttk.Radiobutton(textfrm, text=lang['violet'], variable=text_var, value="9")
        fyx.grid(row=8, column=3, sticky=W)
        ar = ttk.Radiobutton(textfrm, text=lang['indigo'], variable=text_var, value="10")
        ar.grid(row=0, column=4, sticky=W)

        geo = ttk.Radiobutton(textfrm, text=lang['marron'], variable=text_var, value="11")
        geo.grid(row=1, column=4, sticky=W)

        comic = ttk.Radiobutton(textfrm, text=lang['gold'], variable=text_var, value="12")
        comic.grid(row=2, column=4, sticky=W)

        courier = ttk.Radiobutton(textfrm, text=lang['olive_'], variable=text_var, value="13")
        courier.grid(row=3, column=4, sticky=W)
        timess = ttk.Radiobutton(textfrm, text=lang['lime_'], variable=text_var, value="14")
        timess.grid(row=4, column=4, sticky=W)

        fyx = ttk.Radiobutton(textfrm, text=lang['darkred'], variable=text_var, value="15")
        fyx.grid(row=5, column=4, sticky=W)
        fyx = ttk.Radiobutton(textfrm, text=lang['aquamarine'], variable=text_var, value="16")
        fyx.grid(row=6, column=4, sticky=W)
        fyx = ttk.Radiobutton(textfrm, text=lang['sky'], variable=text_var, value="17")
        fyx.grid(row=7, column=4, sticky=W)
        fyx = ttk.Radiobutton(textfrm, text=lang['green_yellow'], variable=text_var, value="18")
        fyx.grid(row=8, column=4, sticky=W)
        shriftfrm = LabelFrame(parametrs_window, text=lang['police_'], cursor="target")
        shriftfrm.grid(row=0, column=4)
        shrift_var = StringVar(value=shrift)

        ar = ttk.Radiobutton(shriftfrm, text="Arial", variable=shrift_var, value="1")
        ar.grid(row=0, column=4, sticky=W)

        geo = ttk.Radiobutton(shriftfrm, text="Georgia", variable=shrift_var, value="2")
        geo.grid(row=1, column=4, sticky=W)

        comic = ttk.Radiobutton(shriftfrm, text="Comic Sans MS", variable=shrift_var, value="3")
        comic.grid(row=2, column=4, sticky=W)

        courier = ttk.Radiobutton(shriftfrm, text="Courier New", variable=shrift_var, value="4")
        courier.grid(row=3, column=4, sticky=W)
        timess = ttk.Radiobutton(shriftfrm, text="Times New Roman", variable=shrift_var, value="5")
        timess.grid(row=4, column=4, sticky=W)

        fyx = ttk.Radiobutton(shriftfrm, text="Fixedsys", variable=shrift_var, value="6")
        fyx.grid(row=5, column=4, sticky=W)

        ar = ttk.Radiobutton(shriftfrm, text="Verdana Pro Black", variable=shrift_var, value="7")
        ar.grid(row=6, column=4, sticky=W)

        geo = ttk.Radiobutton(shriftfrm, text="Montserrat Black", variable=shrift_var, value="8")
        geo.grid(row=7, column=4, sticky=W)

        comic = ttk.Radiobutton(shriftfrm, text="Impact", variable=shrift_var, value="9")
        comic.grid(row=8, column=4, sticky=W)

        btn = ttk.Button(parametrs_window, text=lang['Apply'], width=50, command=prim)
        btn.grid(row=10, column=0)
        btn = ttk.Button(parametrs_window, text=lang['cancel'], width=50, command=close)
        btn.grid(row=11, column=0)
        parametrs_window.grab_set()

        if color_var.get() == "white":
            color_var.set("white")
        elif color_var.get() == "black":
            color_var.set("black")
        elif color_var.get() == "#008000":
            color_var.set("green")
        elif color_var.get() == "#00FF00":
            color_var.set("lime")
        elif color_var.get() == "#006400":
            color_var.set("darkgreen")
        elif color_var.get() == "#0000FF":
            color_var.set("blue")
        elif color_var.get() == "#00FFFF":
            color_var.set("goluboy")
        elif color_var.get() == "gray":
            color_var.set("gray")
        elif color_var.get() == "#FF8C00":
            color_var.set("orange")
        elif color_var.get() == "#FF1493":
            color_var.set("pink")
        elif color_var.get() == "#800080":
            color_var.set("violet")
        elif color_var.get() == "#F0E68C":
            color_var.set("khaki")
        elif color_var.get() == "#8B0000":
            color_var.set("darkred")
        elif color_var.get() == "#808000":
            color_var.set("olive")
        elif color_var.get() == "#556B2F":
            color_var.set("darkolive")
        elif color_var.get() == "#D2691E":
            color_var.set("chocolate")
        elif color_var.get() == "#800000":
            color_var.set("brown")
        elif color_var.get() == "#7FFFD4":
            color_var.set("aquamarine")
        elif color_var.get() == "#87CEEB":
            color_var.set("skay")
        elif color_var.get() == "#4B0082":
            color_var.set("indigo")
        elif color_var.get() == "#FF6347":
            color_var.set("tomat")
        elif color_var.get() == "#FF7F50":
            color_var.set("coral")
        elif color_var.get() == "#F08080":
            color_var.set("lightcoral")
        elif color_var.get() == "#CD5C5C":
            color_var.set("indian")
        elif color_var.get() == "#F0FFFF":
            color_var.set("azur")
        elif color_var.get() == "#FFFAFA":
            color_var.set("snow")
        elif color_var.get() == "#FA8072":
            color_var.set("salmon")
        elif color_var.get() == "#E6E6FA":
            color_var.set("lavan")
        elif color_var.get() == "#F0FFF0":
            color_var.set("medo")
        elif color_var.get() == "#32CD32":
            color_var.set("bordov")
        else:
            color_var.set("gold")
        if shrift == "Arial":
            shrift_var.set("1")
        elif shrift == "Georgia":
            shrift_var.set("2")
        elif shrift == "Comic Sans MS":
            shrift_var.set("3")
        elif shrift == "Courier New":
            shrift_var.set("4")
        elif shrift == "Times New Roman":
            shrift_var.set("5")
        elif shrift == "Fixedsys":
            shrift_var.set("6")
        elif shrift == "Verdana Pro Black":
            shrift_var.set("7")
        elif shrift == "Montserrat Black":
            shrift_var.set("8")
        else:
            shrift_var.set("9")
        if text_color == "Black":
            text_var.set("1")
        elif text_color == "White":
            text_var.set("2")
        elif text_color == "Red":
            text_var.set("3")
        elif text_color == "Yellow":
            text_var.set("4")
        elif text_color == "Orange":
            text_var.set("5")
        elif text_color == "Blue":
            text_var.set("6")
        elif text_color == "#00BFFF":
            text_var.set("7")
        elif text_color == "#FF00FF":
            text_var.set("8")
        elif text_color == "#4B0082":
            text_var.set("10")
        elif text_color == "#800000":
            text_var.set("11")
        elif text_color == "#DAA520":
            text_var.set("12")
        elif text_color == "#808000":
            text_var.set("13")
        elif text_color == "#00FF00":
            text_var.set("14")
        elif text_color == "#8B0000":
            text_var.set("15")
        elif text_color == "#7FFFD4":
            text_var.set("16")
        elif text_color == "#87CEEB":
            text_var.set("17")
        elif text_color == "#9ACD32":
            text_var.set("18")
        else:
            text_var.set("9")
    def on_closing(event=None):
        def exitt():
            global name1, name2, background_color, text_color, ident,score
            if ident:
                conn = sqlite3.connect('games/players_game_durak.db')

                cursor = conn.cursor()
                cursor.execute('''
                                CREATE TABLE IF NOT EXISTS players (
                                    id INTEGER PRIMARY KEY,
                                    name TEXT,
                                    score INTEGER,
                                    background_color TEXT,
                                    text_color TEXT,
                                    time TEXT
                            )
                        ''')
                current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                cursor.execute('''
                            INSERT INTO players (name, score,background_color,text_color,time) VALUES (?,?,?,?,?)
                        ''', (ident, score, background_color, text_color, current_time))
                cursor.execute('''SELECT * FROM players ''')

                conn.commit()

                conn.close()
                exx.destroy()
                Win.destroy()
            else:
                Win.destroy()

        def no():
            exx.destroy()

        exx = create_window(win, lang["game_durak"], global_bg, float(GlobalAlpha), 300, 100, "icons/durak.png")
        exx.resizable(False, False)
        center_child(exx, Win)
        exx.protocol("WM_DELETE_WINDOW",
                     lambda: dismiss(exx))
        global langue

        lbl = Label(exx, text=lang['you_sure_to_exit'])
        lbl.pack()

        btn = ttk.Button(exx, text=lang["yes_coor"], command=exitt)
        btn.pack()
        btn1 = ttk.Button(exx, text=lang["no_coor"], command=no)
        btn1.pack()
        exx.grab_set()
    def sort_alf():

        information_win = create_window(Win, lang["info_"], global_bg, float(GlobalAlpha), 700, 350, "icons/interface/durak.png")
        information_win.resizable(False, False)
        center_child(information_win, Win)
        information_win.protocol("WM_DELETE_WINDOW",
                                 lambda: dismiss(information_win))
        n = Text(information_win)
        scrollbar = Scrollbar(information_win, command=n.yview)
        n.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=RIGHT, fill=Y)
        n.pack()

        conn = sqlite3.connect('games/players_game_durak.db')
        cursor = conn.cursor()
        cursor.execute('''SELECT name,
                          score, 
                          background_color,
                          text_color,
                          time
                   FROM players
                   ORDER BY name ASC;''')
        rows = cursor.fetchall()

        columns = ["Name", "Wins", "Background_Color", "Text_Color", "Time"]

        results = tabulate.tabulate(rows, headers=columns, tablefmt="center")

        n.insert(1.0, str(results) + '\n')
        conn.commit()
        conn.close()

    def sort_score():
        information_win = create_window(root, lang["game_durak"], global_bg, float(GlobalAlpha), 600, 500,
                            "icons/interface/durak.png")
        information_win.resizable(False, False)
        center_child(information_win, Win)
        information_win.protocol("WM_DELETE_WINDOW",
                                 lambda: dismiss(information_win))
        n = Text(information_win)
        scrollbar = Scrollbar(information_win, command=n.yview)
        n.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=RIGHT, fill=Y)
        n.pack()

        conn = sqlite3.connect('games/players_game_durak.db')
        cursor = conn.cursor()
        cursor.execute('''SELECT name,
                          score, 
                          background_color,
                          text_color,
                          time
                   FROM players
                   ORDER BY score DESC;''')
        rows = cursor.fetchall()

        columns = ["Name", "Wins", "Background_Color", "Text_Color", "Time"]

        results = tabulate.tabulate(rows, headers=columns, tablefmt="center")

        n.insert(1.0, str(results) + '\n')
        conn.commit()
        conn.close()

    def data_raz():
        messagebox.showinfo(lang["info_"], lang["developpercoor"])
    def datagame():
        messagebox.showinfo(lang["info_"],
                                lang["infocoord_"])

    def finish():
        global player1, player2, koloda
        if (len(player1) == 0 and len(koloda) == 0) or (len(player2) == 0 and len(koloda) == 0):
            return True
        else:
            return False

    def finish1():
        global name1, name2, win, ind, score, ident
        ind = False
        win = True

        if len(player1) == 0:
            messagebox.showinfo(lang['win_'], f"{lang['player_won']} '{name1}'")
            score = 1
            ident = name1
            canvas.delete("all")
            pr()
        else:
            messagebox.showinfo(lang['win_'], f"{lang['player_won']} '{name2}'")
            score = 1
            ident = name2
            canvas.delete("all")
            pr()
    def update_menu():
        main_menu = Menu()
        info_menu = Menu()
        data = Menu()
        main_menu.add_cascade(label=lang['play'], command=start_game)
        main_menu.add_cascade(label=lang['parametr'], command=parametrs)
        main_menu.add_cascade(label=lang['info_'], menu=info_menu)
        main_menu.add_cascade(label=lang["turnir"], menu=data)
        data.add_cascade(label=lang["sort_alp"], command=sort_alf)
        data.add_cascade(label=lang["sort_score"], command=sort_score)
        info_menu.add_cascade(label=lang['developpers_data'], command=data_raz)
        info_menu.add_cascade(label=lang['game_data'], command=datagame)
        main_menu.add_cascade(label=lang["exit"], command=on_closing)
        Win.config(menu=main_menu)

    Win = create_window(root, lang["game_durak"], global_bg, float(GlobalAlpha), 600, 500, "icons/interface/durak.png")
    Win.bind('<Escape>', on_closing)
    Win.bind('<Alt-F4>', on_closing)
    Win.protocol("WM_DELETE_WINDOW", on_closing)

    icon_image = PhotoImage(file="icons/interface/durak.png")
    Win.iconphoto(True, icon_image)

    update_menu()

    canvas = Canvas(Win, bg=background_color, width=480, height=480)
    canvas.pack(expand=True, fill=BOTH, padx=10, pady=10)
    Win.update_idletasks()
    Win.update()
    pr()