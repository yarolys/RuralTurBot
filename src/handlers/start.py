from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command

from src.config import BOT_ADMIN_ID
from src.utils.keyboard.user import start_panel_kb

router = Router()


@router.message(Command('start'), F.chat.type == 'private')
async def start(message: Message):
    user_name = message.from_user.full_name

    await message.answer(
        f'Добро пожаловать, {user_name}!\n'
        'Вы оказались в удивительном месте - платформе \"Деревенские приключения\", где природа встречается с комфортом!\n\n'
        '🚜 У нас вы найдете:\n'
        '🌟 Красивые места для проживания\n'
        '🍲 Кухню с местными блюдами\n'
        '🗺 Уникальные экскурсии и развлечения\n\n'
        '💡 Получите больше за меньшее!\n'
        'Просто отправьте сообщение \"Polk10\" в ЛС @polk_mn и получите скидку 10% на отдых.',
        reply_markup=start_panel_kb
    )
    if message.from_user.id == BOT_ADMIN_ID:
        await message.answer('Для запуска админки нажми /admin')
    await message.delete()
