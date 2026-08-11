import asyncio

from aiogram import Bot, Dispatcher
from aiogram.types import Message, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.filters import Command


from database import *


TOKEN = "8833750528:AAF7W6C6DO0QwvuHqMWKAVtgk8uWJO0TDdk"

ADMIN_ID = 8965415545


bot = Bot(TOKEN)
dp = Dispatcher()


wallet_wait = {}
admin_wait = {}


def menu(admin=False):

    kb = ReplyKeyboardBuilder()

    kb.add(
        KeyboardButton(text="🤖 Актуальные боты"),
        KeyboardButton(text="📰 Новости"),
        KeyboardButton(text="🏆 Топ"),
        KeyboardButton(text="👤 Профиль")
    )

    if admin:
        kb.add(
            KeyboardButton(text="⚙️ Админ")
        )

    kb.adjust(2)

    return kb.as_markup(
        resize_keyboard=True
    )


@dp.message(Command("start"))
async def start(message: Message):

    add_user(message.from_user.id)

    if message.from_user.id == ADMIN_ID:
        make_admin(message.from_user.id)

    user = get_user(message.from_user.id)

    await message.answer(
        "👋 Добро пожаловать в Worker Panel",
        reply_markup=menu(
            user[4] == 1
        )
    )



@dp.message(lambda m: m.text=="👤 Профиль")
async def profile(message:Message):

    user=get_user(message.from_user.id)

    wallet = user[2] or "Нет"

    await message.answer(
        f"""
👤 Профиль

🆔 ID: {user[0]}
💰 Баланс: {user[3]}

💳 Реквизиты:
{wallet}

Нажмите:
➕ Добавить кошелек
        """,
        reply_markup=wallet_menu()
    )


def wallet_menu():

    kb=ReplyKeyboardBuilder()

    kb.add(
        KeyboardButton(text="➕ Добавить кошелек"),
        KeyboardButton(text="⬅️ Назад")
    )

    return kb.as_markup(resize_keyboard=True)



@dp.message(lambda m:m.text=="➕ Добавить кошелек")
async def wallet(message:Message):

    wallet_wait[message.from_user.id]="type"

    kb=ReplyKeyboardBuilder()

    kb.add(
        KeyboardButton(text="🟦 TON"),
        KeyboardButton(text="💳 Карта")
    )

    await message.answer(
        "Выберите тип:",
        reply_markup=kb.as_markup(resize_keyboard=True)
    )



@dp.message(lambda m:m.text in ["🟦 TON","💳 Карта"])
async def wallet_type(message:Message):

    wallet_wait[message.from_user.id]=message.text

    await message.answer(
        "Введите реквизит:"
    )



@dp.message()
async def text(message:Message):

    uid=message.from_user.id


    if uid in wallet_wait:

        typ=wallet_wait[uid]

        if typ=="🟦 TON":
            set_wallet(uid,"TON",message.text)

        else:
            set_wallet(uid,"CARD",message.text)


        del wallet_wait[uid]

        await message.answer(
            "✅ Реквизит сохранен",
            reply_markup=menu()
        )

        return



    if message.text=="🤖 Актуальные боты":

        await message.answer(
            "🤖 Пока список пуст"
        )


    elif message.text=="📰 Новости":

        await message.answer(
            "📰 Новостей пока нет"
        )


    elif message.text=="🏆 Топ":

        await message.answer(
            "🏆 Топ пользователей пуст"
        )



    elif message.text=="⚙️ Админ":

        user=get_user(uid)

        if user[4]==1:

            await message.answer(
                """
⚙️ Админ панель

/addadmin ID

Пользователи
Реквизиты
"""
            )



@dp.message(Command("addadmin"))
async def addadmin(message:Message):

    user=get_user(message.from_user.id)

    if user[4]!=1:
        return


    args=message.text.split()

    if len(args)>1:

        make_admin(int(args[1]))

        await message.answer(
            "✅ Админ добавлен"
        )



async def main():

    init_db()

    await dp.start_polling(bot)



asyncio.run(main())
