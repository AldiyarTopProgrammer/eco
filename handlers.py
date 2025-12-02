from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Text
from keyboards import main_kb, aqi_inline_kb
import requests
import os

API_TOKEN = os.getenv("AQI_API_KEY")  # ключ API AQI

# Функция для советов по уровню AQI
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

# Словарь для хранения последнего AQI на сообщение (временное)
last_aqi = {}

async def start(message: types.Message):
    await message.answer("Привет! Я бот по AQI. Нажми кнопку ниже, чтобы узнать качество воздуха.", reply_markup=main_kb)

async def ask_city(message: types.Message):
    if message.text == "Узнать AQI":
        await message.answer("Введите город (пока работает только Темиртау)")

async def get_aqi(message: types.Message):
    city_ru = message.text.strip()

    if city_ru.lower() != "темиртау":
        await message.answer("Я пока умею показывать AQI только для города Темиртау.")
        return

    city_en = "Temirtau"
    url = f"https://api.waqi.info/feed/{city_en}/?token={API_TOKEN}"
    response = requests.get(url).json()
    
    if response.get("status") == "ok":
        aqi = response["data"]["aqi"]
        last_aqi[message.message_id] = aqi  # сохраняем для callback
        await message.answer(f"📍 Город: Темиртау\n🌫 AQI: {aqi}", reply_markup=aqi_inline_kb())
    else:
        await message.answer("Не удалось получить данные AQI. Попробуйте позже.")

async def callback_inline(callback_query: types.CallbackQuery):
    data = callback_query.data
    msg_id = callback_query.message.message_id
    aqi = last_aqi.get(msg_id, None)

    if data == "advice" and aqi is not None:
        text = get_advice(aqi)
        await callback_query.message.answer(text)
    elif data == "history":
        text = "История ваших запросов AQI:\n(пока не подключена база данных)"
        await callback_query.message.answer(text)

    await callback_query.answer()

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands=["start"])
    dp.register_message_handler(ask_city, Text(equals="Узнать AQI"))
    dp.register_message_handler(get_aqi)
    dp.register_callback_query_handler(callback_inline)
