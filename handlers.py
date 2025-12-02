from aiogram import Router, types
from aiogram.filters import Command
from keyboards import main_menu_kb, back_kb, history_kb, advice_kb
from aqi_service import get_aqi, get_history, get_advice

router = Router()

# /start
@router.message(Command("start"))
async def cmd_start(msg: types.Message):
    await msg.answer(
        "Выбери действие:",
        reply_markup=main_menu_kb()
    )


# Нажал кнопку Узнать AQI
@router.message(lambda m: m.text == "Узнать AQI")
async def ask_city(msg: types.Message):
    await msg.answer("Введи название города:", reply_markup=back_kb())


# Пользователь пишет город
@router.message()
async def city_handler(msg: types.Message):
    if msg.text == "Назад":
        await msg.answer("Главное меню:", reply_markup=main_menu_kb())
        return

    city = msg.text.strip()
    aqi = get_aqi(city)

    if aqi is None:
        await msg.answer("Не смог найти город или API недоступен 😕")
        return

    await msg.answer(
        f"🌎 Город: <b>{city}</b>\n"
        f"🌫 AQI: <b>{aqi}</b>",
        reply_markup=history_kb(city)
    )


# Кнопка “Советы”
@router.callback_query(lambda c: c.data.startswith("advice:"))
async def send_advice(cb: types.CallbackQuery):
    _, aqi = cb.data.split(":")
    aqi = int(aqi)

    tips = get_advice(aqi)

    await cb.message.answer(
        f"Советы при AQI {aqi}:\n\n{tips}",
        reply_markup=back_kb()
    )
    await cb.answer()


# Кнопка “История”
@router.callback_query(lambda c: c.data.startswith("history:"))
async def send_history(cb: types.CallbackQuery):
    _, city = cb.data.split(":")
    history = get_history(city)

    text = f"📊 История AQI за 3 дня в <b>{city}</b>:\n\n"
    for day, val in history.items():
        text += f"• {day}: <b>{val}</b>\n"

    await cb.message.answer(text, reply_markup=back_kb())
    await cb.answer()

