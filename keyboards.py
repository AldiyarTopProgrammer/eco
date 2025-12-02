from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def main_menu_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Узнать AQI")],
        ],
        resize_keyboard=True
    )

def back_kb():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Назад")]],
        resize_keyboard=True
    )

def history_kb(city: str):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Советы", callback_data=f"advice:{city}_unused")
            ],
            [
                InlineKeyboardButton(text="История AQI", callback_data=f"history:{city}")
            ]
        ]
    )

def advice_kb(aqi: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Советы", callback_data=f"advice:{aqi}")]
        ]
    )
