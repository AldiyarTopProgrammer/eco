from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

# Кнопка "Узнать AQI"
main_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton("Узнать AQI")]],
    resize_keyboard=True
)

# Инлайн кнопки под сообщением AQI
def aqi_inline_kb():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("Советы", callback_data="advice"))
    kb.add(InlineKeyboardButton("История", callback_data="history"))
    return kb
