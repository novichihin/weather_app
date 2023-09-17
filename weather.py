import requests
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt


# Функция для получения данных о погоде
def get_weather(city, source):
    api_key = {
        "Weatherstack": "22e2b4eb1f7843d934fc6b944c5b0a1e",
        "OpenWeatherMap": "98ef130f7440ca17108c2f707d1ad6be",
    }
    url = ""
    if source == "Weatherstack":
        url = f"http://api.weatherstack.com/current?access_key={api_key[source]}&query={city}"
    elif source == "OpenWeatherMap":
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key[source]}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()

        if source == "Weatherstack" and "current" in data:
            weather_info = data["current"]
            messagebox.showinfo(
                "Погода",
                f"Температура: {weather_info['temperature']}°C\nОщущается как: {weather_info['feelslike']}°C\n{weather_info['weather_descriptions'][0]}",
            )
        elif source == "OpenWeatherMap" and "main" in data:
            weather_info = data["main"]
            messagebox.showinfo(
                "Погода",
                f"Температура: {weather_info['temp']}°C\nОщущается как: {weather_info['feels_like']}°C\n{data['weather'][0]['description']}",
            )
        else:
            messagebox.showerror("Ошибка", "Не удалось получить данные о погоде.")

    except requests.exceptions.RequestException:
        messagebox.showerror("Ошибка", "Не удалось установить соединение с сервером.")


# Функция для получения прогноза погоды на несколько дней
def get_forecast(city, source):
    api_key = {"Weatherstack": "YOUR_API_KEY1", "OpenWeatherMap": "YOUR_API_KEY2"}
    url = ""
    if source == "Weatherstack":
        url = f"http://api.weatherstack.com/forecast?access_key={api_key[source]}&query={city}"
    elif source == "OpenWeatherMap":
        url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key[source]}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()

        if source == "Weatherstack" and "forecast" in data:
            forecast = data["forecast"]
            temperatures = [day["temperature"] for day in forecast["daily"]]
            days = [day["date"] for day in forecast["daily"]]

            plt.plot(days, temperatures, marker="o")
            plt.xlabel("День")
            plt.ylabel("Температура (°C)")
            plt.title("Прогноз погоды")
            plt.xticks(rotation=45)
            plt.show()

        elif source == "OpenWeatherMap" and "list" in data:
            forecast_list = data["list"]
            temperatures = [entry["main"]["temp"] for entry in forecast_list]
            times = [entry["dt_txt"] for entry in forecast_list]

            plt.plot(times, temperatures, marker="o")
            plt.xlabel("Время")
            plt.ylabel("Температура (°C)")
            plt.title("Прогноз погоды")
            plt.xticks(rotation=45)
            plt.show()

        else:
            messagebox.showerror("Ошибка", "Не удалось получить прогноз погоды.")

    except requests.exceptions.RequestException:
        messagebox.showerror("Ошибка", "Не удалось установить соединение с сервером.")


# Создание графического интерфейса с использованием tkinter
window = tk.Tk()

window.title("Приложение погоды")
window.geometry("400x200")

label1 = tk.Label(window, text="Введите город:")
label1.pack()

entry = tk.Entry(window)
entry.pack()

label2 = tk.Label(window, text="Выберите источник погоды:")
label2.pack()

var = tk.StringVar(window)
var.set("Weatherstack")  # Значение по умолчанию
option = tk.OptionMenu(window, var, "Weatherstack", "OpenWeatherMap")
option.pack()

button1 = tk.Button(
    window, text="Узнать погоду", command=lambda: get_weather(entry.get(), var.get())
)
button1.pack(pady=5)

button2 = tk.Button(
    window, text="Прогноз погоды", command=lambda: get_forecast(entry.get(), var.get())
)
button2.pack(pady=5)

window.mainloop()
