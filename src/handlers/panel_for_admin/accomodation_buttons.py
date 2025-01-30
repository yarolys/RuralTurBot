import asyncio

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.database.models import DbAccomodation
from src.utils.keyboard.admin import accomodation_panel_kb, admin_panel_kb
from src.utils.filter import AdminRoleFilter
from src.states.admin import AddAccomodationState

router = Router()


@router.message(F.text == "Работа с проживаниями", AdminRoleFilter())
async def show_accomodation_menu(message: types.Message):
    """Отображает клавиатуру для работы с проживаниями."""
    await message.answer("Выберите действие:", reply_markup=accomodation_panel_kb)
    await message.delete()


@router.message(F.text == "Добавить проживание", AdminRoleFilter())
async def start_adding_accomodation(message: types.Message, state: FSMContext):
    """Начало добавления нового проживания."""
    await message.answer("Введите название нового проживания:")
    await state.set_state(AddAccomodationState.waiting_for_accomodation_name)
    await message.delete()


@router.message(AddAccomodationState.waiting_for_accomodation_name)
async def receive_accomodation_name(message: types.Message, state: FSMContext):
    """Получение названия проживания."""
    await state.update_data(accomodation_name=message.text.strip())
    await message.answer("Теперь введите описание проживания:")
    await state.set_state(AddAccomodationState.waiting_for_accomodation_description)


@router.message(AddAccomodationState.waiting_for_accomodation_description)
async def receive_accomodation_description(message: types.Message, state: FSMContext):
    """Получение описания проживания и сохранение его в БД."""
    state_data = await state.get_data()
    accomodation_name = state_data.get("accomodation_name")
    accomodation_description = message.text.strip()

    success = await DbAccomodation.add_accomodation(name=accomodation_name, description=accomodation_description)
    if success:
        await message.answer(f"✅ Проживание \"{accomodation_name}\" успешно добавлено!")
    else:
        await message.answer("⚠️ Проживание с таким названием уже существует.")
    await state.clear()


@router.message(F.text == "Просмотреть все проживания", AdminRoleFilter())
async def show_all_accomodation(message: types.Message):
    """Отображает список всех проживаний без возможности редактирования."""
    accomodations = await DbAccomodation.get_all_accomodation()
    if not accomodations:
        await message.answer("⚠️ Нет доступных проживаний.")
        return

    builder = InlineKeyboardBuilder()
    for accomodation in accomodations:
        builder.row(InlineKeyboardButton(text=accomodation.name, callback_data=f"view_accomodation_{accomodation.id}"))

    await message.answer("📋 Список всех проживаний:", reply_markup=builder.as_markup())
    await message.delete()


@router.callback_query(F.data.startswith("view_accomodation_"))
async def view_accomodation(callback_query: types.CallbackQuery):
    """Просмотр выбранного проживания."""
    accomodation_id = int(callback_query.data.replace("view_accomodation_", ""))
    accomodation = await DbAccomodation.get_accomodation(accomodation_id)

    if accomodation:
        await callback_query.message.answer(
            f"📌 Название: {accomodation.name}\n"
            f"📖 Описание: {accomodation.description}"
        )
    else:
        await callback_query.message.answer("⚠️ Проживание не найдено.")


@router.message(F.text == "Удалить проживание", AdminRoleFilter())
async def start_deleting_accomodation(message: types.Message):
    """Отображает список проживаний для удаления с предупреждением."""
    accomodations = await DbAccomodation.get_all_accomodation()
    if not accomodations:
        await message.answer("⚠️ Нет доступных проживаний.")
        return

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=acc.name, callback_data=f"delete_accomodation_{acc.id}")]
            for acc in accomodations
        ]
    )

    warning_message = await message.answer(
        "⚠️ Внимание!\n"
        "Вы находитесь в режиме удаления записей \"Проживания\".\n"
        "Нажатие на кнопку — удалит запись!\n"
        "Сообщение исчезнет через 20 секунд.",
        reply_markup=keyboard
    )

    await asyncio.sleep(20)
    await warning_message.delete()


@router.callback_query(F.data.startswith("delete_accomodation_"))
async def delete_accomodation(callback_query: types.CallbackQuery):
    """Удаляет выбранное проживание."""
    accomodation_id = int(callback_query.data.replace("delete_accomodation_", ""))
    success = await DbAccomodation.delete_accomodation(accomodation_id)

    if success:
        await callback_query.message.answer("✅ Проживание успешно удалено.")
    else:
        await callback_query.message.answer("⚠️ Проживание не найдено.")

    await start_deleting_accomodation(callback_query.message)


@router.message(F.text == "Назад", AdminRoleFilter())
async def back_to_main_menu(message: types.Message):
    """Возвращает пользователя к главной клавиатуре."""
    await message.answer("Главное меню:", reply_markup=admin_panel_kb)
    await message.delete()
