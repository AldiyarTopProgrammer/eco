from aiogram import types, Router, F
from aiogram.filters import Command
from keyboards import main_kb, aqi_inline_kb
import requests
import os

API_TOKEN = os.getenv("AQI_API_KEY")
router = Router()

# Советы по AQI
def get_advice(aqi):
    if aqi <= 50:
        return "AQI низкий — воздух чистый, можно спокойно гулять на улице."
    elif aqi <= 100:
        return "AQI умеренный — можно гулять, но чувствительные люди должны быть осторожны."
    elif aqi <= 150:
        return "AQI вреден для чувствительных групп — избегайте долгих прогулок на улице."
    elif aqi <= 200:
        return "AQI плохой — ограничьте физическую активность на улице, носите маску."
    elif aqi <= 300:
        return "AQI очень плохой — оставайтесь дома, используйте очистители воздуха."
    else:
        return "AQI опасный — максимально избегайте выхода на улицу, закройте окна и используйте маску."

# Словарь для русского -> английский
ru_to_en = {
    "темиртау": "Temirtau"
}

@router.message(Command(commands=["start"]))
async def start(message: types.Message):
    await message.answer(
        "Привет! Я бот по AQI. Нажми кнопку ниже, чтобы узнать качество воздуха.",
        reply_markup=main_kb
    )

@router.message(F.text == "Узнать AQI")
async def ask_city(message: types.Message):
    await message.answer("Введите город (на русском, например: Темиртау)")

@router.message()
async def get_aqi(message: types.Message):
    city_ru = message.text.strip().lower()

    city_en = ru_to_en.get(city_ru)
    if not city_en:
        await message.answer("Я умею показывать AQI только для Темиртау.")
        return

    url = f"https://api.waqi.info/feed/{city_en}/?token={API_TOKEN}"
    response = requests.get(url).json()

    if response.get("status") == "ok":
        aqi = response["data"]["aqi"]
        await message.answer(
            f"📍 Город: {city_ru.title()}\n🌫 AQI: {aqi}",
            reply_markup=aqi_inline_kb()
        )
    else:
        await message.answer("Не удалось получить данные AQI. Попробуйте позже.")

@router.callback_query(F.data == "advice")
async def callback_advice(callback_query: types.CallbackQuery):
    text = callback_query.message.text
    try:
        aqi = int(text.split("AQI: ")[1])
    except:
        await callback_query.answer("Не могу определить AQI для советов.")
        return

    await callback_query.message.answer(get_advice(aqi))
    await callback_query.answer()

def register_handlers(dp: Router):
    dp.include_router(router)
