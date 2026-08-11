import asyncio
from aiogram import Bot, Dispatcher

TOKEN = "8833750528:AAF7W6C6DO0QwvuHqMWKAVtgk8uWJO0TDdk"

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message()
async def start(message):
    await message.answer(
        "👋 Добро пожаловать в Worker Panel"
    )


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
