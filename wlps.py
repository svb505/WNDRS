import math
import random


NUM_STARS = 1000
SPEED = 0.01
stars = []
WIDTH = 1200
HEIGHT = 900
CENTER_X = WIDTH // 2
CENTER_Y = HEIGHT // 2

def anim_galaxy(canvas,root):
    def create_stars():
        for _ in range(NUM_STARS):
            radius = random.randint(50, 250)
            angle = random.uniform(0, 2 * math.pi)
            size = random.randint(1, 3)
            speed = SPEED * random.uniform(0.5, 2)
            stars.append([radius, angle, size, speed])

    def update_stars():
        canvas.delete("all")
        for star in stars:
            radius, angle, size, speed = star
            x = CENTER_X + math.cos(angle) * radius
            y = CENTER_Y + math.sin(angle) * radius
            brightness = random.randint(180, 255)
            red = random.randint(100, 255)
            blue = random.randint(100, 255)
            color = f'#{red:02x}{random.randint(100, 200):02x}{blue:02x}'
            canvas.create_oval(x - size, y - size, x + size, y + size, fill=color, outline="")
            star[1] += speed  # Update angle

        canvas.create_oval(CENTER_X - 4, CENTER_Y - 4, CENTER_X + 4, CENTER_Y + 4, fill="red",
                           outline="")  # Центр галактики
        root.after(33, update_stars)

    canvas.config(bg="darkblue")
    create_stars()
    update_stars()
def draw_gradient(canvas, color1, color2,root,lang):
    # Получаем размеры экрана
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    limit = height

    # Функция для перевода цвета в формат, который Tkinter понимает
    def translate_color(name):
        if name is None:
            return "black"  # или другой цвет по умолчанию
        mapping = {
            lang["red"]: "red",
            lang["yellow"]: "yellow",
            lang["gray"]: "#808080",
            lang["violet"]: "#800080",
            lang["black"]: "black",
            lang["white"]: "white",
            lang["orange"]: "orange",
            lang["pink"]: "#FF1493",
            lang["olive"]: "#808000",
            lang["green"]: "green"
        }
        # Переходим к Hex значению для Tkinter
        return mapping.get(name.strip(), name)

    # Переводим цвета в формат, который Tkinter поддерживает
    start_color = translate_color(color1)
    end_color = translate_color(color2)

    # Получаем RGB значения для обоих цветов
    r1, g1, b1 = root.winfo_rgb(start_color)
    r2, g2, b2 = root.winfo_rgb(end_color)

    # Переводим цвета в диапазон от 0 до 255
    r1, g1, b1 = r1 // 256, g1 // 256, b1 // 256
    r2, g2, b2 = r2 // 256, g2 // 256, b2 // 256

    # Вычисляем разницу для плавного градиента
    r_ratio = float(r2 - r1) / limit
    g_ratio = float(g2 - g1) / limit
    b_ratio = float(b2 - b1) / limit

    # Рисуем линии для градиента
    for i in range(limit):
        nr = int(r1 + (r_ratio * i))
        ng = int(g1 + (g_ratio * i))
        nb = int(b1 + (b_ratio * i))
        hex_color = f'#{nr:02x}{ng:02x}{nb:02x}'  # Преобразуем в HEX
        canvas.create_line(0, i, width, i, fill=hex_color)
def draw_night_sky(canvas, width, height, stars=200):
    # Очистка холста
    canvas.delete("all")

    # Градиент неба — от темно-синего к черному
    for i in range(height):
        color = f'#{int(0):02x}{int(0):02x}{int(30 + (25 * (1 - i / height))):02x}'
        canvas.create_line(0, i, width, i, fill=color)

    # Рисуем звезды
    for _ in range(stars):
        x = random.randint(0, width)
        y = random.randint(0, height)
        size = random.choice([1, 1, 1, 2])  # Большинство звёзд маленькие
        brightness = random.randint(180, 255)
        color = f'#{brightness:02x}{brightness:02x}{brightness:02x}'
        canvas.create_oval(x, y, x + size, y + size, fill=color, outline="")
def draw_galaxy(canvas, width, height, num_stars=218900, arms=8):
    canvas.delete("all")
    canvas.create_rectangle(0, 0, width, height, fill='black')

    center_x, center_y = width // 2, height // 2

    # Ядро галактики
    canvas.create_oval(center_x - 25, center_y - 25, center_x + 25, center_y + 25,
                       fill="yellow", outline="orange")

    for _ in range(num_stars):
        # Радиальное расстояние с логарифмическим распределением
        r = random.uniform(10, min(width, height) // 2 - 10)
        angle = random.uniform(0, 2 * math.pi)

        # Эффект спиральных рук
        spiral_arm = random.randint(0, arms - 1)
        arm_offset = random.uniform(-0.2, 0.2)
        angle += spiral_arm * (2 * math.pi / arms) + arm_offset

        # Координаты звезды
        x = center_x + r * math.cos(angle) * (1 + 0.3 * math.log1p(r))  # Спиральное смещение
        y = center_y + r * math.sin(angle) * (1 + 0.3 * math.log1p(r))

        # Цвет звезды: переход от белого к синему и красному
        brightness = random.randint(180, 255)
        red = random.randint(100, 255)
        blue = random.randint(100, 255)
        color = f'#{red:02x}{random.randint(100, 200):02x}{blue:02x}'

        # Размер звезды
        size = random.choice([1, 2, 3])

        # Рисуем звезды
        canvas.create_oval(x, y, x + size, y + size, fill=color, outline="")