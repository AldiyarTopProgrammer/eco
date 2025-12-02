import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.types import BotCommand
from handlers import router

TOKEN = os.getenv("8520976464:AAEXRuPMQjznxFX2vAmbI1hrFBwB8Scr0aY")

async def main():
    bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()

    dp.include_router(router)

    await bot.set_my_commands([
        BotCommand(command="start", description="Запустить бота"),
    ])

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
