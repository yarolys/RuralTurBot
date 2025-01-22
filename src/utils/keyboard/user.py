from aiogram.types import (
    InlineKeyboardButton, 
    InlineKeyboardMarkup
)

start_panel_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='🏡 Проживание', callback_data='accommodation')],
        [InlineKeyboardButton(text='🍲 Местная кухня', callback_data='local_food'),
         InlineKeyboardButton(text='🗺 Экскурсии', callback_data='excursions')],
        [InlineKeyboardButton(text='🎉 Развлечения', callback_data='entertainment'),
         InlineKeyboardButton(text='🎁 Получить скидку', callback_data='get_discount')],
        [InlineKeyboardButton(text='💬 Контакты', callback_data='contacts'),
         InlineKeyboardButton(text='ℹ️ О нас', callback_data='about_us')]
    ]
)