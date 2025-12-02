from aiogram import Router, types
from aqi_service import get_aqi
from tips import get_tip
from config import DEFAULT_CITY

router = Router()

@router.message(commands=["start"])
async def start_cmd(msg: types.Message):
    await msg.answer(
        "Привет! Я показываю AQI, советы и скажу, когда лучше не выходить.\n"
        "Команды:\n"
        "/aqi <город> — качество воздуха\n"
        "/tip — экосовет\n"
        f"Пример: /aqi {DEFAULT_CITY}"
    )

@router.message(commands=["tip"])
async def send_tip(msg: types.Message):
    await msg.answer(f"Совет: {get_tip()}")

@router.message(commands=["aqi"])
async def aqi_cmd(msg: types.Message):
    parts = msg.text.split(maxsplit=1)
    city = parts[1] if len(parts) > 1 else DEFAULT_CITY

    data = get_aqi(city)

    if not data:
        await msg.answer("Не смог найти воздух для этого города.")
        return

    text = (
        f"🌍 Город: {city}\n"
        f"📊 AQI: {data['aqi']}\n"
        f"PM2.5: {data['pm25']}\n"
        f"PM10: {data['pm10']}\n\n"
        f"{data['status']}\n\n"
        f"♻️ Совет: {get_tip()}"
    )

    await msg.answer(text)
