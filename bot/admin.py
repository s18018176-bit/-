from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from database import (
    get_withdrawals,
    update_withdraw,
    make_admin,
    get_user
)

router = Router()


# ID главного админа
MAIN_ADMIN = 8965415545


def is_admin(user_id):
    return user_id == MAIN_ADMIN


# Админ меню
@router.message(Command("admin"))
async def admin_panel(message: Message):
    if not is_admin(message.from_user.id):
        return

    await message.answer(
        "🔐 Админ панель\n\n"
        "Команды:\n"
        "/withdraws — заявки на выплаты\n"
        "/users — пользователи\n"
        "/addadmin ID — добавить админа"
    )


# Просмотр заявок
@router.message(Command("withdrawals"))
async def withdraws(message: Message):
    if not is_admin(message.from_user.id):
        return

    data = get_withdrawals()

    if not data:
        await message.answer("📭 Заявок нет")
        return

    text = "💸 Заявки:\n\n"

    for w in data:
        text += (
            f"ID заявки: {w[0]}\n"
            f"Пользователь: {w[1]}\n"
            f"Сумма: {w[2]}\n"
            f"Статус: {w[3]}\n\n"
        )

    text += (
        "Одобрить:\n"
        "/ok ID\n\n"
        "Отклонить:\n"
        "/no ID"
    )

    await message.answer(text)


# Одобрить выплату
@router.message(Command("ok"))
async def ok_withdraw(message: Message):
    if not is_admin(message.from_user.id):
        return

    try:
        withdraw_id = int(message.text.split()[1])
    except:
        await message.answer("Используй: /ok ID")
        return

    approve_withdraw(withdraw_id)

    await message.answer("✅ Выплата одобрена")


# Отказать
@router.message(Command("no"))
async def no_withdraw(message: Message):
    if not is_admin(message.from_user.id):
        return

    try:
        withdraw_id = int(message.text.split()[1])
    except:
        await message.answer("Используй: /no ID")
        return

    reject_withdraw(withdraw_id)

    await message.answer("❌ Выплата отклонена")


# Пользователи
@router.message(Command("users"))
async def users(message: Message):
    if not is_admin(message.from_user.id):
        return

    users = get_user()

    text = "👥 Пользователи:\n\n"

    for u in users:
        text += f"ID: {u[0]} Баланс: {u[1]}\n"

    await message.answer(text)


# Добавление админа
@router.message(Command("addadmin"))
async def add_new_admin(message: Message):
    if message.from_user.id != MAIN_ADMIN:
        return

    try:
        user_id = int(message.text.split()[1])
    except:
        await message.answer("Используй: /addadmin ID")
        return

    make_admin(user_id)

    await message.answer(
        f"✅ Админ {user_id} добавлен"
    )
