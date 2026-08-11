from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from database import (
    get_withdrawals,
    update_withdraw,
    add_admin,
    add_news,
    get_news,
    add_bot,
    get_bots,
    set_top,
    get_top
)

router = Router()

MAIN_ADMIN = 8965415545


def is_admin(user_id: int):
    return user_id == MAIN_ADMIN


# =========================
# АДМИН ПАНЕЛЬ
# =========================

@router.message(Command("admin"))
async def admin_panel(message: Message):
    if not is_admin(message.from_user.id):
        return

    await message.answer(
        "⚙️ Админ панель\n\n"
        "/withdraws — заявки на выплаты\n"
        "/addadmin ID — добавить админа\n\n"
        "📰 Новости:\n"
        "/addnews текст\n"
        "/news\n\n"
        "🤖 Боты:\n"
        "/addbot текст\n"
        "/bots\n\n"
        "🏆 Топ:\n"
        "/settop текст\n"
        "/top"
    )


# =========================
# АДМИНЫ
# =========================

@router.message(Command("addadmin"))
async def add_admin_cmd(message: Message):
    if not is_admin(message.from_user.id):
        return

    args = message.text.split()

    if len(args) < 2:
        await message.answer("Пример:\n/addadmin 123456789")
        return

    try:
        user_id = int(args[1])
    except ValueError:
        await message.answer("❌ ID должен быть числом")
        return

    add_admin(user_id)

    await message.answer("✅ Админ добавлен")


# =========================
# ВЫПЛАТЫ
# =========================

@router.message(Command("withdraws"))
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
            f"ID: {w[0]}\n"
            f"Пользователь: {w[1]}\n"
            f"Сумма: {w[2]}\n"
            f"Статус: {w[3]}\n\n"
        )

    text += (
        "/ok ID — одобрить\n"
        "/no ID — отклонить"
    )

    await message.answer(text)


@router.message(Command("ok"))
async def approve(message: Message):
    if not is_admin(message.from_user.id):
        return

    args = message.text.split()

    if len(args) < 2:
        await message.answer("Пример:\n/ok 1")
        return

    try:
        withdraw_id = int(args[1])
    except ValueError:
        await message.answer("❌ ID должен быть числом")
        return

    update_withdraw(withdraw_id, "approved")

    await message.answer("✅ Выплата одобрена")


@router.message(Command("no"))
async def reject(message: Message):
    if not is_admin(message.from_user.id):
        return

    args = message.text.split()

    if len(args) < 2:
        await message.answer("Пример:\n/no 1")
        return

    try:
        withdraw_id = int(args[1])
    except ValueError:
        await message.answer("❌ ID должен быть числом")
        return

    update_withdraw(withdraw_id, "rejected")

    await message.answer("❌ Выплата отклонена")


# =========================
# НОВОСТИ
# =========================

@router.message(Command("addnews"))
async def add_news_cmd(message: Message):
    if not is_admin(message.from_user.id):
        return

    text = message.text.removeprefix("/addnews").strip()

    if not text:
        await message.answer(
            "Пример:\n"
            "/addnews Обновление бота сегодня"
        )
        return

    add_news(text)

    await message.answer("📰 Новость добавлена")


@router.message(Command("news"))
async def news(message: Message):
    data = get_news()

    if not data:
        await message.answer("📰 Новостей пока нет")
        return

    text = "📰 Новости:\n\n"

    for n in data:
        text += f"• {n}\n"

    await message.answer(text)


# =========================
# БОТЫ
# =========================

@router.message(Command("addbot"))
async def add_bot_cmd(message: Message):
    if not is_admin(message.from_user.id):
        return

    text = message.text.removeprefix("/addbot").strip()

    if not text:
        await message.answer(
            "Пример:\n"
            "/addbot @BotName — описание бота"
        )
        return

    add_bot(text)

    await message.answer("🤖 Бот добавлен")


@router.message(Command("bots"))
async def bots(message: Message):
    data = get_bots()

    if not data:
        await message.answer("🤖 Актуальных ботов пока нет")
        return

    text = "🤖 Актуальные боты:\n\n"

    for b in data:
        text += f"• {b}\n"

    await message.answer(text)


# КНОПКА "🤖 Актуальные боты"
@router.message(lambda message: message.text == "🤖 Актуальные боты")
async def bots_button(message: Message):
    data = get_bots()

    if not data:
        await message.answer("🤖 Актуальных ботов пока нет")
        return

    text = "🤖 Актуальные боты:\n\n"

    for b in data:
        text += f"• {b}\n"

    await message.answer(text)


# =========================
# ТОП
# =========================

@router.message(Command("settop"))
async def set_top_cmd(message: Message):
    if not is_admin(message.from_user.id):
        return

    text = message.text.removeprefix("/settop").strip()

    if not text:
        await message.answer(
            "Пример:\n"
            "/settop 🥇 BotName — 1000 пользователей"
        )
        return

    set_top(text)

    await message.answer("🏆 Топ обновлён")


@router.message(Command("top"))
async def top(message: Message):
    data = get_top()

    await message.answer(
        "🏆 Топ:\n\n" + str(data)
    )


# КНОПКА "🏆 Топ"
@router.message(lambda message: message.text == "🏆 Топ")
async def top_button(message: Message):
    data = get_top()

    await message.answer(
        "🏆 Топ:\n\n" + str(data)
    )


# КНОПКА "⚙️ Админ"
@router.message(lambda message: message.text == "⚙️ Админ")
async def admin_button(message: Message):
    if not is_admin(message.from_user.id):
        return

    await admin_panel(message)

@router.message(lambda message: message.text == "🤖 Актуальные боты")
async def bots_button(message: Message):

    data = get_bots()

    if not data:
        await message.answer("🤖 Актуальных ботов пока нет")
        return

    text = "🤖 Актуальные боты:\n\n"

    for b in data:
        text += f"• {b}\n"

    await message.answer(text)
