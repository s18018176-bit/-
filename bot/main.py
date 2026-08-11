import asyncio

from aiogram import Bot, Dispatcher
from aiogram.types import Message, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.filters import Command

from database import *
from admin import router as admin_router


TOKEN="8833750528:AAF7W6C6DO0QwvuHqMWKAVtgk8uWJO0TDdk"

ADMIN_ID=8965415545


bot=Bot(TOKEN)

dp=Dispatcher()

dp.include_router(admin_router)


state={}



def keyboard(admin=False):

    kb=ReplyKeyboardBuilder()

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
async def start(message:Message):

    uid=message.from_user.id

    add_user(uid)

    if uid==ADMIN_ID:
        make_admin(uid)

    user=get_user(uid)


    await message.answer(
        "👋 Добро пожаловать!",
        reply_markup=keyboard(
            user[4]==1
        )
    )



@dp.message(lambda m:m.text=="👤 Профиль")
async def profile(message:Message):

    user=get_user(
        message.from_user.id
    )


    await message.answer(
f"""
👤 Профиль

🆔 ID:
{user[0]}

💰 Баланс:
{user[1]}₽

💳 Реквизиты:
{user[2] or "Нет"}
{user[3] or ""}
""",
reply_markup=profile_kb()
)



def profile_kb():

    kb=ReplyKeyboardBuilder()

    kb.add(
        KeyboardButton(text="➕ Добавить реквизиты"),
        KeyboardButton(text="💸 Вывести")
    )

    return kb.as_markup(resize_keyboard=True)



@dp.message(lambda m:m.text=="➕ Добавить реквизиты")
async def wallet(message:Message):

    state[message.from_user.id]="wallet_type"

    await message.answer(
        "Выберите тип:\n\n🟦 TON\n💳 Карта"
    )



@dp.message(lambda m:m.text in ["🟦 TON","💳 Карта"])
async def wallet_type(message:Message):

    state[message.from_user.id]=message.text

    await message.answer(
        "Введите реквизит:"
    )



@dp.message(lambda m:m.from_user.id in state)
async def save_wallet(message:Message):

    uid=message.from_user.id

    typ=state[uid]

    if typ=="🟦 TON":
        set_wallet(uid,"TON",message.text)

    else:
        set_wallet(uid,"CARD",message.text)


    del state[uid]


    await message.answer(
        "✅ Реквизиты сохранены"
    )



@dp.message(lambda m:m.text=="💸 Вывести")
async def withdraw(message:Message):

    state[message.from_user.id]="withdraw"

    await message.answer(
        "Введите сумму выплаты:"
    )



@dp.message()
async def text(message:Message):

    uid=message.from_user.id


    if state.get(uid)=="withdraw":

        amount=int(message.text)

        user=get_user(uid)


        if user[1] < amount:

            await message.answer(
                "❌ Недостаточно средств"
            )

        else:

            create_withdraw(uid,amount)

            await message.answer(
                "✅ Заявка отправлена"
            )


        del state[uid]

        return



    if message.text=="⚙️ Админ":

        user=get_user(uid)

        if user[4]==1:

            await message.answer(
"""
⚙️ Админ панель

/balance ID сумма

/addadmin ID

/withdraws
"""
)



@dp.message(Command("balance"))
async def balance(message:Message):

    if get_user(message.from_user.id)[4]!=1:
        return

    args=message.text.split()

    add_balance(
        int(args[1]),
        int(args[2])
    )


    await message.answer(
        "✅ Баланс добавлен"
    )



@dp.message(Command("addadmin"))
async def addadmin(message:Message):

    if get_user(message.from_user.id)[4]!=1:
        return

    args=message.text.split()

    make_admin(
        int(args[1])
    )

    await message.answer(
        "✅ Админ добавлен"
    )



@dp.message(Command("withdraws"))
async def withdraws(message:Message):

    if get_user(message.from_user.id)[4]!=1:
        return


    data=get_withdrawals()

    text="💸 Заявки:\n"

    for w in data:
        text+=f"""
#{w[0]}
ID: {w[1]}
Сумма: {w[2]}₽
Статус: {w[3]}

"""

    await message.answer(text)



async def main():

    init_db()

    await dp.start_polling(bot)



asyncio.run(main())
