from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


admin_panel_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Управление кнопками"),
        KeyboardButton(text="Управление текстами")],
        [KeyboardButton(text="Список пользователей")],
        [KeyboardButton(text="Аналитика"),
        KeyboardButton(text="Настройки")],
        [KeyboardButton(text="Управление скидками")],

    ],
    resize_keyboard=True
)

control_buttons_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Добавить кнопку'),
        KeyboardButton(text='Удалить кнопку')],
        [KeyboardButton(text='Назад')]
    ],
    resize_keyboard=True
)

