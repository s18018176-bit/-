import asyncio

from aiogram import Bot, Dispatcher
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command


TOKEN = "8833750528:AAF7W6C6DO0QwvuHqMWKAVtgk8uWJO0TDdk"

ADMIN_ID = 8965415545


bot = Bot(token=TOKEN)
dp = Dispatcher()


menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="👤 Профиль",
                callback_data="profile"
            ),
            InlineKeyboardButton(
                text="💰 Баланс",
                callback_data="balance"
            )
        ],
        [
            InlineKeyboardButton(
                text="📋 Задания",
                callback_data="tasks"
            )
        ],
        [
            InlineKeyboardButton(
                text="🛠 Админ",
                callback_data="admin"
            )
        ]
    ]
)


@dp.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "👋 Добро пожаловать в Worker Panel\n\n"
        "Выберите раздел:",
        reply_markup=menu
    )


@dp.callback_query()
async def buttons(callback: CallbackQuery):

    if callback.data == "profile":
        await callback.message.answer(
            f"👤 Профиль\n\n"
            f"ID: {callback.from_user.id}\n"
            f"Имя: {callback.from_user.first_name}"
        )


    elif callback.data == "balance":
        await callback.message.answer(
            "💰 Баланс: 0"
        )


    elif callback.data == "tasks":
        await callback.message.answer(
            "📋 Заданий пока нет"
        )


    elif callback.data == "admin":

        if callback.from_user.id == ADMIN_ID:
            await callback.message.answer(
                "🛠 Админ-панель\n\n"
                "Пользователей: 0\n"
                "Баланс системы: 0"
            )
        else:
            await callback.message.answer(
                "❌ Доступ запрещён"
            )


    await callback.answer()


@dp.message(Command("profile"))
async def profile(message: Message):
    await message.answer(
        f"👤 ID: {message.from_user.id}\n"
        "💰 Баланс: 0"
    )


@dp.message(Command("balance"))
async def balance(message: Message):
    await message.answer(
        "💰 Ваш баланс: 0"
    )


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
