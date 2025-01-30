from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

admin_panel_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Управление текстами")],
        [KeyboardButton(text="Список пользователей")],
        [KeyboardButton(text="Работа с турами"), KeyboardButton(text="Работа с проживаниями")],
    ],
    resize_keyboard=True
)

tour_panel_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Просмотреть все туры")],
        [KeyboardButton(text="Добавить тур"),
        KeyboardButton(text="Удалить тур")],
        [KeyboardButton(text="Назад")]
    ],
    resize_keyboard=True 
)

accomodation_panel_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Просмотреть все проживания")],
        [KeyboardButton(text="Добавить проживание"),
        KeyboardButton(text="Удалить проживание")],
        [KeyboardButton(text="Назад")]
    ],
    resize_keyboard=True 
)