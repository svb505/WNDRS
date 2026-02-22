import os
from tkinter.colorchooser import askcolor
from PIL import Image as PilImage
from PIL import ImageDraw, ImageFont,ImageFilter
import piexif
from datetime import datetime
from tkinter import *
from tkinter import ttk,messagebox,simpledialog,filedialog
from math import sqrt
import math
from PIL import Image, ImageTk

path = ""
color = ""
shw_coords = True
def open_editor_win(root,lang,global_bg,global_fg,actives_programs):
    actives_programs.append("Photo Editor")
    def rotation(path):
        def rotate_image():
            global tk_img

            if not path:
                return

            try:
                angle = float(angle_entry.get())
            except ValueError:
                messagebox.showerror(lang["error"], lang["enter_valid_gra"],parent = window)
                return

            direction = direction_combo.get()
            if direction == lang["po_chasovoi"]:
                angle = -angle

            image = Image.open(path)
            width, height = image.size
            if width > height:
                image = image.resize(tuple([200, 150]))
            elif width < height:
                image = image.resize(tuple([150, 200]))
            else:
                image = image.resize(tuple([200, 200]))
            rotated = image.rotate(angle, expand=True)

            image_for_saving = Image.open(path)
            rotated_for_saving = image_for_saving.rotate(angle, expand=True)

            tk_img = ImageTk.PhotoImage(rotated)
            label.config(image=tk_img)
            label.image = tk_img

            now = datetime.today()
            name = f"rotated_example_{now.strftime('%d-%m-%Y-%H_%M_%S')}"
            rotated_for_saving.save(f"user_files/{name}.png")
            messagebox.showinfo(lang['success'], f"{lang['photo_saved_with_name']} user_files/{name}",parent = window)


        window = Toplevel(Win)
        window.attributes('-topmost', True)
        window.config(bg = global_bg)
        window.title(lang["image_rotation"])
        window.geometry("500x400")
        Label(window, text=lang["enter_angle_rotation"],bg = global_bg,fg = global_fg).grid(row = 0,column = 0)
        angle_entry = Entry(window)
        angle_entry.insert(0, "90")
        angle_entry.grid(row =1,column = 0)

        Label(window, text=lang["naprav"],bg = global_bg,fg = global_fg).grid(row = 2,column = 0)
        direction_combo = ttk.Combobox(window, values=[lang["po_chasovoi"], lang["protiv_chasovoi"]], state="readonly")
        direction_combo.set(lang["po_chasovoi"])
        direction_combo.grid(row = 3,column = 0)

        ttk.Button(window, text=lang["rotate"], command=rotate_image).grid(row = 4,column = 0)

        label = Label(window)
        label.grid(row = 5,column = 0)

        tk_img = None
    def open_window(path):
        def pick_color():
            global color
            color = askcolor(parent = Win,title=lang["select_color"])[1]  # [1] — hex-значение

        def update(path, label, size, text, x, y):
            global color
            if not color:
                color = "#000000"
            img = Image.open(path)
            draw = ImageDraw.Draw(img)
            font = ImageFont.truetype("arial.ttf", size=int(size))
            position = (int(x), int(y))
            draw.text(position, text, fill=color, font=font)

            # Масштабируем для предпросмотра (как и раньше)
            width, height = img.size
            if width > height:
                img = img.resize((200, 150))
            elif width < height:
                img = img.resize((150, 200))
            else:
                img = img.resize((200, 200))

            # Преобразуем в формат для Tkinter
            img_tk = ImageTk.PhotoImage(img)

            # Обновляем Label
            label.config(image=img_tk)
            label.image = img_tk  # Обязательно сохранить ссылку
        def save(path, label, size, text, x, y):
            global color
            image = Image.open(path).convert("RGB")
            draw = ImageDraw.Draw(image)
            font = ImageFont.truetype("arial.ttf", size=int(size))  # Убедись, что arial.ttf существует
            position = (int(x), int(y))

            now = datetime.today()
            name = f"text_overlay_{now.strftime('%d-%m-%Y-%H_%M_%S')}"
            draw.text(position, text, fill=color, font=font)
            image.save(f"user_files/{name}.png")
            messagebox.showinfo(lang["success"], f"{lang['photo_saved_with_name']} user_files/{name}",parent = window)
            image.show()

        window = Toplevel(Win)
        window.attributes('-topmost', True)
        window.config(bg=global_bg)
        window.geometry("500x550")
        window.title(lang["nakl"])

        preview = LabelFrame(window, text=lang["_preview"],bg = global_bg)
        preview.grid(row=0, column=2)

        img1 = Image.open(path)
        width, height = img1.size
        if width > height:
            img1 = img1.resize(tuple([200, 150]))
        elif width < height:
            img1 = img1.resize(tuple([150, 200]))
        else:
            img1 = img1.resize(tuple([200, 200]))
        img2 = ImageTk.PhotoImage(img1)
        lbl = Label(preview, image=img2)
        lbl.image = img2
        lbl.grid(row=1, column=2)
        Label(window, text=lang["write_your_text"],bg = global_bg,fg = global_fg).grid(row=2, column=2)
        text = ttk.Entry(window)
        text.grid(row=3, column=2)
        text.insert(0, "Hello")
        Label(window, text=lang["write_text_size"],bg = global_bg,fg = global_fg).grid(row=4, column=2)
        size = ttk.Entry(window)
        size.grid(row=5, column=2)
        size.insert(0, "15")
        Label(window, text=lang["enter_positionX"],bg = global_bg,fg = global_fg).grid(row=6, column=2)
        x = ttk.Entry(window)
        x.grid(row=7, column=2)
        x.insert(0, "10")
        Label(window, text=lang["enter_positionY"],bg = global_bg,fg = global_fg).grid(row=8, column=2)
        y = ttk.Entry(window)
        y.grid(row=9, column=2)
        y.insert(0, "10")

        ttk.Button(window, text=lang["select_color"], command=pick_color).grid(row=10, column=2)
        ttk.Button(window, text=lang["update_ui"],
                   command=lambda: update(path, lbl, size.get(), text.get(), x.get(), y.get())).grid(row=11, column=2)
        ttk.Button(window, text=lang["save"],
                   command=lambda: save(path, lbl, size.get(), text.get(), x.get(), y.get())).grid(row=12, column=2)
    def oblast_blur(file_path, Win):
        def draw_coordsystem(img):
            draw = ImageDraw.Draw(img)
            width, height = img.size
            try:
                font = ImageFont.truetype("arial.ttf", 11)
                font1 = ImageFont.truetype("arial.ttf", 14)
            except:
                font = font1 = None

            def draw_arrow(start, end, arrow_length=10, arrow_angle=30, fill="blue", width=3):
                draw.line([start, end], fill=fill, width=width)
                angle = math.atan2(end[1] - start[1], end[0] - start[0])
                angle1 = angle + math.radians(arrow_angle)
                angle2 = angle - math.radians(arrow_angle)
                x1 = end[0] - arrow_length * math.cos(angle1)
                y1 = end[1] - arrow_length * math.sin(angle1)
                x2 = end[0] - arrow_length * math.cos(angle2)
                y2 = end[1] - arrow_length * math.sin(angle2)
                draw.line([end, (x1, y1)], fill=fill, width=width)
                draw.line([end, (x2, y2)], fill=fill, width=width)

            draw_arrow((5, 5), (width - 4, 4))
            draw_arrow((5, 5), (4, height - 4))
            draw.line((5, 5, width - 5, 5), fill="blue", width=3)
            draw.line((5, 5, 5, height - 5), fill="blue", width=3)

            if font1:
                draw.text((25, 3), "x1", font=font1, fill="red")
                draw.text((7, 25), "y1", font=font1, fill="red")

            step_x = width // 10
            step_y = height // 10
            for i in range(10):
                y = 5 + i * step_y
                x = 5 + i * step_x
                draw.line((5, y, width - 5, y), fill="gray", width=1)
                draw.line((x, 5, x, height - 5), fill="gray", width=1)
                if font:
                    draw.text((7, y), str(y), font=font, fill="red")
                    draw.text((x, 7), str(x), font=font, fill="red")
            return img

        def center_window(root):
            root.update_idletasks()
            w = root.winfo_width()
            h = root.winfo_height()
            ws = root.winfo_screenwidth()
            hs = root.winfo_screenheight()
            x = (ws // 2) - (w // 2)
            y = (hs // 2) - (h // 2)
            root.geometry(f'{w}x{h}+{x}+{y}')

        def open_image(file_path):
            global img_tk, original_img, image, shw_coords
            image = file_path
            if not file_path:
                return

            original_img = Image.open(file_path)
            image_to_show = original_img.copy()

            if shw_coords:
                image_to_show = draw_coordsystem(image_to_show)

            img_tk = ImageTk.PhotoImage(image_to_show)
            canvas.delete("all")

            canvas.create_image(0, 0, anchor="nw", image=img_tk)
            canvas.img = img_tk
            canvas.config(scrollregion=canvas.bbox("all"))

        def toggle_coords():
            global shw_coords
            shw_coords = show_coords.get()
            open_image(file_path)

        def show_mouse_coords(event):
            if original_img is None:
                return

            img_x = int(canvas.canvasx(event.x))
            img_y = int(canvas.canvasy(event.y))

            coords_label.config(text=f"X: {img_x}, Y: {img_y}")

        def prepare_data():
            now = datetime.today()
            return now.strftime("%d-%m-%Y-%H_%M_%S")

        def save_data():
            global image, radius
            radius = radius_var.get()
            formatted = prepare_data()
            img = Image.open(image)
            region = img.crop((int(x1.get()), int(y1.get()), int(x2.get()), int(y2.get())))
            blurred_region = region.filter(ImageFilter.GaussianBlur(radius=radius))

            img.paste(blurred_region, (int(x1.get()), int(y1.get())))
            img.save(f"user_files/particular_blured-{formatted}.png")
            data = f"x1: {x1.get()}, y1: {y1.get()}, x2: {x2.get()}, y2: {y2.get()}"
            messagebox.showinfo(lang["success"],lang["photo_saved__"] + f" user_files/particular_blured-{formatted}.png",parent = roott)

        roott = Toplevel(Win)
        
        roott.config(bg=global_bg)
        roott.title(lang["oblast_blur"])
        roott.geometry("800x600")
        center_window(roott)
        show_coords =BooleanVar()
        show_coords.set(True)
        # Переменные

        # Сетка
        roott.columnconfigure(0, weight=3)
        roott.columnconfigure(1, weight=1)
        roott.rowconfigure(0, weight=1)

        # --- Scrollable Canvas ---
        canvas_frame = Frame(roott)
        canvas_frame.grid(row=0, column=0, sticky="nsew")

        canvas = Canvas(canvas_frame, bg="gray")
        canvas.grid(row=0, column=0, sticky="nsew")

        x_scroll = Scrollbar(canvas_frame, orient="horizontal", command=canvas.xview)
        x_scroll.grid(row=1, column=0, sticky="ew")

        y_scroll = Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        y_scroll.grid(row=0, column=1, sticky="ns")

        canvas.configure(xscrollcommand=x_scroll.set, yscrollcommand=y_scroll.set)

        canvas_frame.rowconfigure(0, weight=1)
        canvas_frame.columnconfigure(0, weight=1)

        canvas.bind("<Motion>", show_mouse_coords)

        # --- Панель управления ---
        controls = ttk.Frame(roott, padding=10)
        controls.grid(row=0, column=1, sticky="nsew")
        controls.columnconfigure(1, weight=1)

        ttk.Checkbutton(controls, text=lang["show_coor_setka"], variable=show_coords,
                        command=toggle_coords).grid(
            row=1, column=0, columnspan=2, sticky="w", pady=5)
        coords_label = Label(controls, text="X: -, Y: -",bg = global_bg,fg = global_fg)
        coords_label.grid(row=2, column=0, columnspan=2, sticky="w", pady=5)

        Label(controls, text="x1:",bg = global_bg,fg = global_fg).grid(row=3, column=0, sticky="e")
        x1 = ttk.Entry(controls)
        x1.grid(row=3, column=1, sticky="ew")

        Label(controls, text="y1:",bg = global_bg,fg = global_fg).grid(row=4, column=0, sticky="e")
        y1 = ttk.Entry(controls)
        y1.grid(row=4, column=1, sticky="ew")

        Label(controls, text="x2:",bg = global_bg,fg = global_fg).grid(row=5, column=0, sticky="e")
        x2 = ttk.Entry(controls)
        x2.grid(row=5, column=1, sticky="ew")

        Label(controls, text="y2:",bg = global_bg,fg = global_fg).grid(row=6, column=0, sticky="e")
        y2 = ttk.Entry(controls)
        y2.grid(row=6, column=1, sticky="ew")
        Label(controls, text=lang["blur_level"]).grid(row=7, column=1)

        radius_var = IntVar()
        radius_var.set(1)
        scale = Scale(controls, from_=0, to=6, length=50, variable=radius_var, orient="horizontal")
        scale.grid(row=8, column=1)
        ttk.Button(controls, text=lang['save'], command=save_data).grid(row=9, column=0, columnspan=2, sticky="ew",
                                                                       pady=10)
        ttk.Button(controls, text=lang['__exit__'], command=roott.destroy).grid(row=10, column=0, columnspan=2, sticky="ew", pady=10)
        open_image(file_path)
    def dms_to_deg(dms, ref):
        """Преобразует координаты из DMS в градусы"""
        degrees = dms[0][0] / dms[0][1]
        minutes = dms[1][0] / dms[1][1]
        seconds = dms[2][0] / dms[2][1]
        result = degrees + (minutes / 60) + (seconds / 3600)
        if ref in ['S', 'W']:
            result *= -1
        return result
    def prepare_data():
        now = datetime.today()
        return now.strftime("%d-%m-%Y-%H_%M_%S")
    def get_image_metadata(path):
        img = PilImage.open(path)
        width, height = img.size
        dpi = img.info.get("dpi", (None, None))
        filename = os.path.basename(path)

        # Разрешение
        resolution = f"{width}x{height}"

        # EXIF через piexif
        try:
            exif_dict = piexif.load(img.info["exif"])
        except (KeyError, ValueError):
            exif_dict = {}

        gps_info = exif_dict.get("GPS", {})
        gps_lat = gps_lon = None

        if gps_info:
            lat = gps_info.get(piexif.GPSIFD.GPSLatitude)
            lat_ref = gps_info.get(piexif.GPSIFD.GPSLatitudeRef, b'').decode()

            lon = gps_info.get(piexif.GPSIFD.GPSLongitude)
            lon_ref = gps_info.get(piexif.GPSIFD.GPSLongitudeRef, b'').decode()

            if lat and lon and lat_ref and lon_ref:
                gps_lat = dms_to_deg(lat, lat_ref)
                gps_lon = dms_to_deg(lon, lon_ref)

        return {
            "Название файла": filename,
            "Ширина": width,
            "Высота": height,
            "DPI": dpi,
            "Разрешение": resolution,
            "Геолокация": (gps_lat, gps_lon) if gps_lat and gps_lon else None
        }
    def golden_ratio(file):
        image_files = file
        img = PilImage.open(f"{image_files}")
        width, height = img.size
        f = (1 + sqrt(5)) / 2

        new_width = int(height * f)
        new_height = int(width / f)
        box = ()
        if width > height:
            if new_width > width:
                new_width = width
                new_height = int(width / f)
                top = (height - new_height) // 2
                left = 0
            else:
                left = (width - new_width) // 2
                top = 0
                new_height = height
            box = (left, top, left + new_width, top + new_height)
        else:
            if new_height > height:
                new_height = height
                new_width = int(height / f)
                left = (width - new_width) // 2
                top = 0
            else:
                top = (height - new_height) // 2
                left = 0
                new_width = width
            box = (left, top, left + new_width, top + new_height)
        cropped = img.crop((box))
        formatted = prepare_data()
        filename = os.path.basename(image_files)
        cropped.save(f"user_files/cropped_test-{formatted}-{filename}.png")
        messagebox.showinfo(lang['success'], f"{lang['photo_saved_with_name']}: user_files/cropped_test-{formatted}-{filename}.png",parent = Win)
    def bblur(path):
        def save(radius, path):
            formatted = prepare_data()
            img = PilImage.open(path)
            blur = img.filter(ImageFilter.BoxBlur(radius=int(radius)))
            filename = os.path.basename(path)
            blur.save(f"user_files/box_blured-{formatted}-{filename}")
            messagebox.showinfo(lang['success'], f"{lang['photo_saved_with_name']}: user_files/box_blured--{formatted}-{filename}",parent = w)

        w = Toplevel(Win)
        
        w.config(bg=global_bg)
        w.title("Box Blur")
        w.geometry("300x300")

        Label(w, text=lang["enter_radius"],bg = global_bg,fg = global_fg).grid(row=0, column=0)
        radius = ttk.Entry(w)
        radius.grid(row=1, column=0)

        ttk.Button(w, text=lang["save"], command=lambda: save(radius.get(), path)).grid(row=2, column=0)
    def gblur(path):
        def save(radius, path):
            formatted = prepare_data()
            img = PilImage.open(path)
            gaussian = img.filter(ImageFilter.GaussianBlur(radius=int(radius)))
            filename = os.path.basename(path)
            gaussian.save(f"user_files/g_blured-{formatted}-{filename}")
            messagebox.showinfo(lang['success'], f"{lang['photo_saved_with_name']}: user_files/g_blured-{formatted}-{filename}",parent = w)

        w = Toplevel(Win)
        
        w.config(bg=global_bg)
        w.title("Gaussian Blur")
        w.geometry("300x300")

        Label(w, text=lang['enter_radius'],bg = global_bg,fg = global_fg).grid(row=0, column=0)
        radius = ttk.Entry(w)
        radius.grid(row=1, column=0)

        ttk.Button(w, text=lang["save"], command=lambda: save(radius.get(), path)).grid(row=2, column=0)
    def crop(path):
        def save(left, top, right, bottom, path):
            info = get_image_metadata(f"{path}")
            w = info["Ширина"]
            h = info["Высота"]
            x1 = int(left)
            y1 = int(top)
            x2 = int(right)
            y2 = int(bottom)
            if any(coord < 0 for coord in [x1, y1, x2, y2]):
                messagebox.showerror(lang["error"], lang["radius_less_0"],parent = Win)
                return
            if x2 <= x1 or y2 <= y1:
                messagebox.showerror(lang["error"],
                                     lang["raduis1"])
                return

            if x2 > w or y2 > h:
                messagebox.showerror(lang["error"],
                                     f"{lang['radius_2-1']} {w}, {lang['radius_2-2']} {h})",parent = Win)
                return
            else:
                img = PilImage.open(f"{path}")
                box = (
                    int(left),
                    int(top),
                    int(right),
                    int(bottom)
                )
                cropped = img.crop((box))
                formatted = prepare_data()
                filename = os.path.basename(path)
                cropped.save(f"user_files/cropped-{formatted}-{filename}")
                messagebox.showinfo(lang["success"], f"{lang['photo_saved_with_name']}: user_files/cropped-{formatted}-{filename}",parent = Win)

        w = Toplevel(Win)
        
        w.config(bg=global_bg)
        w.title("Crop")
        w.geometry("300x300")

        Label(w, text=lang["enter_left"],bg = global_bg,fg = global_fg).grid(row=0, column=0)
        left = ttk.Entry(w)
        left.grid(row=1, column=0)
        Label(w, text=lang["enter_top"],bg = global_bg,fg = global_fg).grid(row=2, column=0)
        top = ttk.Entry(w)
        top.grid(row=3, column=0)
        Label(w, text=lang["enter_right"],bg = global_bg,fg = global_fg).grid(row=4, column=0)
        right = ttk.Entry(w)
        right.grid(row=5, column=0)
        Label(w, text=lang["enter_bottom"],bg = global_bg,fg = global_fg).grid(row=6, column=0)
        bottom = ttk.Entry(w)
        bottom.grid(row=7, column=0)

        ttk.Button(w, text=lang["save"],
                   command=lambda: save(left.get(), top.get(), right.get(), bottom.get(), path)).grid(row=8, column=0)
    def resize(path):
        def save(width, height, path):
            info = get_image_metadata(f"{path}")
            img_w = info["Ширина"]
            img_h = info["Высота"]
            if img_w / img_h == int(width) / int(height):
                img = PilImage.open(path)
                resized = img.resize(tuple([int(width), int(height)]))
                formatted = prepare_data()
                filename = os.path.basename(path)
                resized.save(f"user_files/resized-{formatted}-{filename}")
                messagebox.showinfo(lang['success'], f"{lang['photo_saved_with_name']}: user_files/resized-{formatted}-{filename}",parent = Win)
            else:
                inp = simpledialog.askinteger("",
                                              lang["invalid-resize"],
                                              minvalue=1, maxvalue=3, parent=w)
                if inp == 1:
                    new_w = simpledialog.askinteger("", lang["enter_new_height"])
                    new_h = info["Ширина"] * new_w / info["Высота"]
                    tpl = tuple([int(new_w), int(new_h)])
                elif inp == 2:
                    new_h = simpledialog.askinteger("", lang["enter_new_width"])
                    new_w = info["Высота"] * new_h / info["Ширина"]
                    tpl = tuple([int(new_w), int(new_h)])
                elif inp == 3:
                    koof = simpledialog.askinteger("", lang["enter_coof"])
                    tpl = tuple([info["Ширина"] * koof, info["Высота"] * koof])
                else:
                    messagebox.showerror(lang['error'], lang["plus_3"],parent = Win)
                img = PilImage.open(f"{path}")
                resized = img.resize(tpl)
                formatted = prepare_data()
                filename = os.path.basename(path)
                resized.save(f"user_files/resized-{formatted}-{filename}")
                messagebox.showinfo(lang['success'], f"{lang['photo_saved_with_name']}:user_files/resized-{formatted}-{filename}",parent = Win)

        w = Toplevel(Win)
        w.config(bg=global_bg)
        
        w.title("Resize")
        w.geometry("300x300")

        Label(w, text=lang["enter_width"],bg = global_bg,fg = global_fg).grid(row=0, column=0)
        width = ttk.Entry(w)
        width.grid(row=1, column=0)
        Label(w, text=lang["enter_height"],bg = global_bg,fg = global_fg).grid(row=2, column=0)
        height = ttk.Entry(w)
        height.grid(row=3, column=0)

        ttk.Button(w, text=lang["save"], command=lambda: save(width.get(), height.get(), path)).grid(row=4, column=0)
    def select(command, path):
        if command == "resize":
            resize(path)
        elif command == "crop":
            crop(path)
        elif command == "rotate":
            rotation(path)
        elif command == "Gaussian Blur":
            gblur(path)
        elif command == "Box blur":
            bblur(path)
        elif command == "Golden Ratio":
            golden_ratio(path)
        elif command == lang["oblast_blur"]:
            oblast_blur(path, Win)
        elif command == lang["nakl"]:
            open_window(path)
    def open_filedialog():
        global path
        path = filedialog.askopenfilename(parent = Win,filetypes=[("Images", "*.png;*.png;*.jpeg;*.bmp")])

    Win = Toplevel(root)
    
    Win.config(bg=global_bg)
    Win.title(lang["photo_redactor"])
    Win.geometry("500x400")
    img = Image.open("icons/SVB PhotoEditor.png")
    icon_image = ImageTk.PhotoImage(img)
    Win.iconphoto(False, icon_image)
    ttk.Button(Win, text=lang["select_image"], command=open_filedialog).pack(pady=5)

    Label(Win, text=lang["select_dei"], bg=global_bg, fg=global_fg).pack(pady=5)

    combo = ttk.Combobox(
        Win,
        values=["resize", "crop", "rotate", "Gaussian Blur", "Box blur", "Golden Ratio", lang["oblast_blur"],
                lang["nakl"]]
    )
    combo.pack(pady=5)
    combo.set("resize")

    ttk.Button(Win, text=lang["--select--"], command=lambda: select(combo.get(), path)).pack(pady=10)

