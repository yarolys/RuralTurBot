from aiogram.types import (
    InlineKeyboardButton, 
    InlineKeyboardMarkup
)

start_panel_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='🏡 Проживание', callback_data='accommodation'),
         InlineKeyboardButton(text='⛺️ Туры', callback_data='tour')],
        [InlineKeyboardButton(text='🎉 Развлечения', callback_data='entertainment'),
         InlineKeyboardButton(text='🍲 Местная кухня', callback_data='local_food')],
        [InlineKeyboardButton(text='🎁 Получить скидку', callback_data='get_discount')],
        [InlineKeyboardButton(text='💬 Контакты', callback_data='contacts'),
         InlineKeyboardButton(text='ℹ️ О нас', callback_data='about_us')]
    ]
)

accomodation_panel_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='')]
    ]
)

back_to_excursions = InlineKeyboardMarkup(
        inline_keyboard=[
                [InlineKeyboardButton(text="🔙 Вернуться", callback_data="excursions")]
            ]
)

back_to_main = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Вернуться", callback_data="back_to_main")]
    ]
)