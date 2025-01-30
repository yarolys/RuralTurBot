import asyncio

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.database.models import DbTour
from src.utils.keyboard.user import start_panel_kb
from src.utils.keyboard.admin import tour_panel_kb, admin_panel_kb
from src.utils.filter import AdminRoleFilter
from src.states.admin import AddTourState, DeleteTourState

router = Router()


@router.message(F.text == "Работа с турами", AdminRoleFilter())
async def show_tour_menu(message: types.Message):
    """ Отображает клавиатуру для работы с турами. """
    await message.answer("Выберите действие:", reply_markup=tour_panel_kb)
    await message.delete()


@router.message(F.text == "Добавить тур", AdminRoleFilter())
async def start_adding_tour(message: types.Message, state: FSMContext):
    """ Начало добавления нового тура. """
    await message.answer("Введите название нового тура:")
    await state.set_state(AddTourState.waiting_for_tour_name)
    await message.delete()


@router.message(AddTourState.waiting_for_tour_name)
async def receive_tour_name(message: types.Message, state: FSMContext):
    """ Получение названия тура. """
    await state.update_data(tour_name=message.text.strip())
    await message.answer("Теперь введите описание тура:")
    await state.set_state(AddTourState.waiting_for_tour_description)


@router.message(AddTourState.waiting_for_tour_description)
async def receive_tour_description(message: types.Message, state: FSMContext):
    """ Получение описания тура и сохранение его в БД. """
    state_data = await state.get_data()
    tour_name = state_data.get("tour_name")
    tour_description = message.text.strip()

    success = await DbTour.add_tour(name=tour_name, description=tour_description)
    if success:
        await message.answer(f"✅ Тур \"{tour_name}\" успешно добавлен!")
    else:
        await message.answer(f"⚠️ Тур с таким названием уже существует.")
    await state.clear()


@router.message(F.text == "Просмотреть все туры", AdminRoleFilter())
async def show_all_tours(message: types.Message):
    """ Отображает список всех туров без возможности редактирования. """
    tours = await DbTour.get_all_tours()
    if not tours:
        await message.answer("⚠️ Нет доступных туров.")
        return

    builder = InlineKeyboardBuilder()
    for tour in tours:
        builder.row(InlineKeyboardButton(text=tour.name, callback_data=f"view_tour_{tour.id}"))

    await message.answer("📋 Список всех туров:", reply_markup=builder.as_markup())
    await message.delete()


@router.callback_query(F.data.startswith("view_tour_"))
async def view_tour(callback_query: types.CallbackQuery):
    """ Просмотр выбранного тура без возможности редактирования. """
    tour_id = int(callback_query.data.replace("view_tour_", ""))
    
    tour = await DbTour.get_tour(tour_id)
    
    if tour:
        await callback_query.message.answer(
            f"📌 Название тура: {tour.name}\n"
            f"📖 Описание: {tour.description}"
        )
    else:
        await callback_query.message.answer("⚠️ Тур не найден.")


@router.message(F.text == "Удалить тур", AdminRoleFilter())
async def start_deleting_tour(message: types.Message):
    """ Отображает список туров для удаления с предупреждением. """
    tours = await DbTour.get_all_tours()
    if not tours:
        await message.answer("⚠️ Нет доступных туров.")
        return
    await message.delete()
    # Создаем Inline-клавиатуру с кнопками для удаления
    
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=tour.name, callback_data=f"delete_tour_{tour.id}")]
            for tour in tours
        ]
    )

    warning_message = await message.answer(
        "Внимание!\n"
        "Вы находитесь в режиме удаления записей \"Туры\", нажатие на кнопку - удалит запись!\n"
        "Это сообщение с записями исчезнет через 20 секунд автоматически",
        reply_markup=keyboard
    )

    # Удаляем предупреждение через 20 секунд
    await asyncio.sleep(20)
    await warning_message.delete()


@router.callback_query(F.data.startswith("delete_tour_"))
async def delete_tour(callback_query: types.CallbackQuery):
    """ Удаляет выбранный тур. """
    tour_id = int(callback_query.data.replace("delete_tour_", ""))
    success = await DbTour.delete_tour(tour_id)

    if success:
        await callback_query.message.answer("✅ Тур успешно удалён.")
    else:
        await callback_query.message.answer("⚠️ Тур не найден.")

    # Обновляем список туров
    await start_deleting_tour(callback_query.message)


@router.message(F.text == "Назад", AdminRoleFilter())
async def back_to_main_menu(message: types.Message):
    """ Возвращает пользователя к главной клавиатуре. """
    await message.answer("Главное меню:", reply_markup=admin_panel_kb)
    await message.delete()