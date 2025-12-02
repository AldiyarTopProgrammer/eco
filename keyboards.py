from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

# Кнопка "Узнать AQI"
main_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Узнать AQI")]],
    resize_keyboard=True
)

# Инлайн кнопки под сообщением AQI
def aqi_inline_kb():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Советы", callback_data="advice")],
        [InlineKeyboardButton(text="История", callback_data="history")]
    ])
    return kb
