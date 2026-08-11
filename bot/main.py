import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command

TOKEN = "8833750528:AAF7W6C6DO0QwvuHqMWKAVtgk8uWJO0TDdk"

ADMIN_ID = 8965415545

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "👋 Добро пожаловать в Worker Panel\n\n"
        "Команды:\n"
        "/profile — профиль\n"
        "/balance — баланс"
    )


@dp.message(Command("profile"))
async def profile(message: Message):
    await message.answer(
        f"👤 Ваш ID: {message.from_user.id}\n"
        "💰 Баланс: 0"
    )


@dp.message(Command("admin"))
async def admin(message: Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer(
            "🔐 Админ панель\n\n"
            "Команды:\n"
            "/users — пользователи\n"
            "/ban — бан\n"
            "/unban — разбан\n"
            "/addbalance — изменить баланс"
        )
    else:
        await message.answer("❌ Нет доступа")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
