import asyncio
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.database.models import DbEntertainment  # Подключаем модель БД
from src.utils.keyboard.admin import entertainment_panel_kb, admin_panel_kb
from src.states.admin import AddEntertainmentState

router = Router()


@router.message(F.text == "Работа с развлечениями")
async def show_entertainment_menu(message: types.Message):
    """ Отображает меню управления развлечениями. """
    await message.answer("Выберите действие:", reply_markup=entertainment_panel_kb)
    await message.delete()


@router.message(F.text == "Просмотреть все развлечения")
async def show_all_entertainments(message: types.Message):
    """ Отображает список всех доступных развлечений. """
    entertainments = await DbEntertainment.get_all_entertainment()
    if not entertainments:
        await message.answer("⚠️ Нет доступных развлечений.")
        return

    builder = InlineKeyboardBuilder()
    for entertainment in entertainments:
        builder.row(InlineKeyboardButton(text=entertainment.name, callback_data=f"view_entertainment_{entertainment.id}"))

    await message.answer("🎡 Список всех развлечений:", reply_markup=builder.as_markup())
    await message.delete()


@router.callback_query(F.data.startswith("view_entertainment_"))
async def view_entertainment(callback_query: types.CallbackQuery):
    """ Отображает информацию о выбранном развлечении. """
    entertainment_id = int(callback_query.data.replace("view_entertainment_", ""))
    entertainment = await DbEntertainment.get_entertainment(entertainment_id)

    if entertainment:
        await callback_query.message.answer(
            f"🎡 Название: {entertainment.name}\n"
            f"📖 Описание: {entertainment.description}"
        )
    else:
        await callback_query.message.answer("⚠️ Развлечение не найдено.")


@router.message(F.text == "Добавить развлечение")
async def start_adding_entertainment(message: types.Message, state: FSMContext):
    """ Начинает процесс добавления развлечения. """
    await message.answer("Введите название нового развлечения:")
    await state.set_state(AddEntertainmentState.waiting_for_entertainment_name)
    await message.delete()


@router.message(AddEntertainmentState.waiting_for_entertainment_name)
async def receive_entertainment_name(message: types.Message, state: FSMContext):
    """ Получает название развлечения. """
    await state.update_data(entertainment_name=message.text.strip())
    await message.answer("Теперь введите описание развлечения:")
    await state.set_state(AddEntertainmentState.waiting_for_entertainment_description)


@router.message(AddEntertainmentState.waiting_for_entertainment_description)
async def receive_entertainment_description(message: types.Message, state: FSMContext):
    """ Получает описание развлечения и сохраняет его в БД. """
    state_data = await state.get_data()
    entertainment_name = state_data.get("entertainment_name")
    entertainment_description = message.text.strip()

    success = await DbEntertainment.add_entertainment(name=entertainment_name, description=entertainment_description)
    if success:
        await message.answer(f"✅ Развлечение \"{entertainment_name}\" успешно добавлено!")
    else:
        await message.answer(f"⚠️ Развлечение с таким названием уже существует.")
    await state.clear()


@router.message(F.text == "Удалить развлечение")
async def start_deleting_entertainment(message: types.Message):
    """ Показывает список развлечений для удаления. """
    entertainments = await DbEntertainment.get_all_entertainment()
    if not entertainments:
        await message.answer("⚠️ Нет доступных развлечений.")
        return
    await message.delete()

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=ent.name, callback_data=f"delete_entertainment_{ent.id}")]
            for ent in entertainments
        ]
    )

    warning_message = await message.answer(
        "Внимание!\n"
        "Вы находитесь в режиме удаления записей \"Развлечения\", нажатие на кнопку - удалит запись!\n"
        "Это сообщение исчезнет через 20 секунд автоматически",
        reply_markup=keyboard
    )

    await asyncio.sleep(20)
    await warning_message.delete()


@router.callback_query(F.data.startswith("delete_entertainment_"))
async def delete_entertainment(callback_query: types.CallbackQuery):
    """ Удаляет выбранное развлечение. """
    entertainment_id = int(callback_query.data.replace("delete_entertainment_", ""))
    success = await DbEntertainment.delete_entertainment(entertainment_id)

    if success:
        await callback_query.message.answer("✅ Развлечение успешно удалено.")
    else:
        await callback_query.message.answer("⚠️ Развлечение не найдено.")

    # Обновляем список
    await start_deleting_entertainment(callback_query.message)


@router.message(F.text == "Назад")
async def back_to_main_menu(message: types.Message):
    """ Возвращает пользователя к главному меню. """
    await message.answer("Главное меню:", reply_markup=admin_panel_kb)
    await message.delete()
