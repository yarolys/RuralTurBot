from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.utils.filter import AdminRoleFilter
from src.database.models import DbLocalFood
from src.utils.keyboard.admin import localfood_panel_kb, admin_panel_kb
from src.states.admin import AddLocalFoodState

router = Router()


@router.message(F.text == "Работа с кухней", AdminRoleFilter())
async def show_localfood_menu(message: types.Message):
    """ Отображает клавиатуру для работы с местной кухней. """
    await message.answer("Выберите действие:", reply_markup=localfood_panel_kb)
    await message.delete()


@router.message(F.text == "Добавить блюдо", AdminRoleFilter())
async def start_adding_localfood(message: types.Message, state: FSMContext):
    """ Начало добавления нового блюда. """
    await message.answer("Введите название нового блюда:")
    await state.set_state(AddLocalFoodState.waiting_for_localfood_name)
    await message.delete()


@router.message(AddLocalFoodState.waiting_for_localfood_name)
async def receive_localfood_name(message: types.Message, state: FSMContext):
    """ Получение названия блюда. """
    await state.update_data(localfood_name=message.text.strip())
    await message.answer("Теперь введите описание блюда:")
    await state.set_state(AddLocalFoodState.waiting_for_localfood_description)


@router.message(AddLocalFoodState.waiting_for_localfood_description)
async def receive_localfood_description(message: types.Message, state: FSMContext):
    """ Получение описания блюда и сохранение его в БД. """
    state_data = await state.get_data()
    localfood_name = state_data.get("localfood_name")
    localfood_description = message.text.strip()

    success = await DbLocalFood.add_local_food(name=localfood_name, description=localfood_description)
    if success:
        await message.answer(f"✅ Блюдо \"{localfood_name}\" успешно добавлено!")
    else:
        await message.answer("⚠️ Блюдо с таким названием уже существует.")
    await state.clear()


@router.message(F.text == "Просмотреть все блюда", AdminRoleFilter())
async def show_all_localfoods(message: types.Message):
    """ Отображает список всех блюд. """
    localfoods = await DbLocalFood.get_all_local_foods()
    if not localfoods:
        await message.answer("⚠️ Нет доступных блюд.")
        return

    builder = InlineKeyboardBuilder()
    for localfood in localfoods:
        builder.row(InlineKeyboardButton(text=localfood.name, callback_data=f"view_localfood_{localfood.id}"))

    await message.answer("📋 Список всех блюд:", reply_markup=builder.as_markup())
    await message.delete()


@router.callback_query(F.data.startswith("view_localfood_"))
async def view_localfood(callback_query: types.CallbackQuery):
    """ Просмотр выбранного блюда. """
    localfood_id = int(callback_query.data.replace("view_localfood_", ""))
    localfood = await DbLocalFood.get_local_food(localfood_id)
    
    if localfood:
        await callback_query.message.answer(
            f"🍲 Название: {localfood.name}\n"
            f"📖 Описание: {localfood.description}"
        )
    else:
        await callback_query.message.answer("⚠️ Блюдо не найдено.")


@router.message(F.text == "Удалить блюдо", AdminRoleFilter())
async def start_deleting_localfood(message: types.Message):
    """ Отображает список блюд для удаления. """
    localfoods = await DbLocalFood.get_all_local_foods()
    if not localfoods:
        await message.answer("⚠️ Нет доступных блюд.")
        return
    
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=localfood.name, callback_data=f"delete_localfood_{localfood.id}")]
            for localfood in localfoods
        ]
    )

    await message.answer("Выберите блюдо для удаления:", reply_markup=keyboard)
    await message.delete()


@router.callback_query(F.data.startswith("delete_localfood_"))
async def delete_localfood(callback_query: types.CallbackQuery):
    """ Удаляет выбранное блюдо. """
    localfood_id = int(callback_query.data.replace("delete_localfood_", ""))
    success = await DbLocalFood.delete_local_food(localfood_id)

    if success:
        await callback_query.message.answer("✅ Блюдо успешно удалено.")
    else:
        await callback_query.message.answer("⚠️ Блюдо не найдено.")

    await start_deleting_localfood(callback_query.message)


@router.message(F.text == "Назад", AdminRoleFilter())
async def back_to_main_menu(message: types.Message):
    """ Возвращает пользователя к главной клавиатуре. """
    await message.answer("Главное меню:", reply_markup=admin_panel_kb)
    await message.delete()