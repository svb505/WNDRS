import os
from tkinter import *
from tkinter import ttk
import requests
from PIL import Image, ImageTk
from io import BytesIO
from load_env import load_env

load_env()

API_KEY = os.getenv("WEATHER_API")

def get_weather():
    city = entry_city.get()

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=ru"

    response = requests.get(url,timeout=5)
    data = response.json()

    if str(data["cod"]) != "200":
        print(data)
        lbl_result.config(text="Ошибка API")
        return

    temp = data["main"]["temp"]
    weather = data["weather"][0]["description"]
    icon = data["weather"][0]["icon"]

    lbl_result.config(text=f"{city}\n{temp}°C\n{weather}")

    icon_url = f"http://openweathermap.org/img/wn/{icon}@2x.png"
    img_data = requests.get(icon_url).content

    img = Image.open(BytesIO(img_data))
    photo = ImageTk.PhotoImage(img)

    lbl_icon.config(image=photo)
    lbl_icon.image = photo

root = Tk()
root.title("Погода")
root.geometry("300x350")

entry_city = ttk.Entry(root, font=15)
entry_city.pack(pady=10)

btn = ttk.Button(root, text="Узнать погоду", command=get_weather)
btn.pack(pady=5)

lbl_result = ttk.Label(root, text="", font=14)
lbl_result.pack(pady=10)

lbl_icon = ttk.Label(root)
lbl_icon.pack()

root.mainloop()
