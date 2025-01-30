from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from src.database.models import DbUser
from src.utils.filter import AdminRoleFilter

router = Router()

@router.message(F.text == "Список пользователей", AdminRoleFilter())
async def show_all_users(message: types.Message):
    """Выводит список всех пользователей."""
    users = await DbUser.get_all_users()

    if not users:
        await message.answer("⚠️ Пользователей пока нет.")
        return

    # Формируем сообщение со списком пользователей
    users_list = "📋 Список пользователей:\n\n"
    
    # Формируем строки для каждого пользователя
    for user in users:
        users_list += (
            f"👤 Имя: {user.full_name}\n"
            f"🆔 ID: {user.id}\n"
            f"🔏 Link: @{user.username}\n"
            f"📅 Дата регистрации: {user.created_at.strftime('%Y-%m-%d %H:%M')}\n\n"
        )

    # Отправляем сообщение с пользователями
    await message.answer(users_list)
