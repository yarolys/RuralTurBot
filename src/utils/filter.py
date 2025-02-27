from typing import Union

from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery

from src.config import BOT_ADMIN_ID


class AdminRoleFilter(BaseFilter):
    async def __call__(self, message: Union[Message, CallbackQuery]) -> bool:
        if message.from_user.id != BOT_ADMIN_ID:
            await message.answer(text='Только админ может делать это')
            return False
        return True
    