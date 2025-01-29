from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

admin_panel_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Управление текстами")],
        [KeyboardButton(text="Список пользователей")],
        [KeyboardButton(text="Аналитика"),
        ]
    ],
    resize_keyboard=True
)

