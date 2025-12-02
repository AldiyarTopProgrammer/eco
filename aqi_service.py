from pwaqi import AQI
from config import AQI_TOKEN

aqi_client = AQI(AQI_TOKEN)

def get_aqi(city: str):
    """Возвращает словарь: AQI, PM2.5, PM10, статус."""
    data = aqi_client.get_city_aqi(city)

    if not data:
        return None

    aqi = int(data["aqi"])
    status = ""

    if aqi <= 50:
        status = "Отлично — воздух чистый 😃"
    elif aqi <= 100:
        status = "Нормально — можно гулять 🙂"
    elif aqi <= 150:
        status = "Слабое загрязнение ⚠️"
    elif aqi <= 200:
        status = "Плохо — лучше не гулять 😷"
    elif aqi <= 300:
        status = "Очень плохо — без причины не выходи 🤢"
    else:
        status = "Опасно — оставайся дома ☠️"

    return {
        "aqi": aqi,
        "pm25": data.get("iaqi", {}).get("pm25", {}).get("v"),
        "pm10": data.get("iaqi", {}).get("pm10", {}).get("v"),
        "status": status,
    }
