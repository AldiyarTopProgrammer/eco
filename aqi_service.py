import requests
import os
from datetime import datetime, timedelta

API_KEY = os.getenv("AQI_TOKEN")

# ---------- Получение текущего AQI ----------
def get_aqi(city: str):
    url = f"https://api.waqi.info/feed/{city}/?token={API_KEY}"

    try:
        r = requests.get(url, timeout=10)
        data = r.json()

        if data.get("status") != "ok":
            return None

        return data["data"]["aqi"]

    except:
        return None


# ---------- История AQI за последние 3 дня ----------
def get_history(city: str):
    today = datetime.now()
    history = {}

    for i in range(3):
        day = today - timedelta(days=i)
        day_str = day.strftime("%Y-%m-%d")

        url = f"https://api.waqi.info/feed/{city}/?token={API_KEY}"
        r = requests.get(url).json()

        aqi = r["data"]["aqi"] if r.get("status") == "ok" else "?"

        history[day_str] = aqi

    return history


# ---------- Советы ----------
def get_advice(aqi: int):
    if aqi <= 50:
        return "Все ок. Можно спокойно гулять."
    if aqi <= 100:
        return "Немного загрязнён. Но всё ещё норм."
    if aqi <= 150:
        return "Лучше не бегать на улице. Уменьши нагрузки."
    if aqi <= 200:
        return "Плохой воздух. Надень маску, по минимуму снаружи."
    if aqi <= 300:
        return "Очень вредно. Не выходи без нужды, закрывай окна."
    return "Жесть. Сидеть дома, очиститель воздуха обязателен."
