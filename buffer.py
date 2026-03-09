import pyttsx3

def textToSpeech(text, filename="output.mp3"):
    engine = pyttsx3.init()

    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate + 1)  # Скорость

    volume = engine.getProperty('volume')
    engine.setProperty('volume', volume + 0.1)  # Громкость

    engine.save_to_file(text, filename)  # Сохранение в файл
    engine.runAndWait()

text = input("Введите текст для озвучки: ")
textToSpeech(text)