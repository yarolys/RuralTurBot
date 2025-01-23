from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.config import logger
from src.utils.filter import AdminRoleFilter
from src.utils.keyboard.admin import admin_panel_kb

router = Router()


@router.message(Command('admin'), AdminRoleFilter())
@router.message(F.text == 'Вернуться в меню')
async def admin_panel(message: Message, state: FSMContext):
    logger.debug(f'ID пользователя: {message.from_user.id}')
    await message.answer(
        'Добро пожаловать в меню администратора!',
        reply_markup=admin_panel_kb
    )
    logger.debug(f'Пользователь {message.from_user.full_name} вошел в админ панель')
    await state.clear()
    await message.delete()
