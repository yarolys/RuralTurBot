from aiogram import Router, types, F
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext

from src.utils.keyboard.user import start_panel_kb, back_to_excursions, back_to_main
from src.database.models import DbEditableText, DbTour, DbAccomodation, DbLocalFood, DbEntertainment
from src.states.admin import EditTextState


router = Router()


@router.callback_query(lambda c: c.data == 'about_us')
async def about_us_handler(callback_query: CallbackQuery):
    editable_text = await DbEditableText.get_text('about_us')  
    if not editable_text:  
        return  
    if callback_query.message.text != editable_text.content:  
        await callback_query.message.edit_text(
            editable_text.content,  
            reply_markup=start_panel_kb
        )


@router.callback_query(lambda c: c.data == 'get_discount')
async def get_discount_handler(callback_query: CallbackQuery):
    editable_text = await DbEditableText.get_text('get_discount')  
    if not editable_text:  
        return  
    if callback_query.message.text != editable_text.content:  
        await callback_query.message.edit_text(
            editable_text.content,  
            reply_markup=start_panel_kb
        )


@router.callback_query(lambda c: c.data == 'contacts')
async def contacts_handler(callback_query: CallbackQuery):
    editable_text = await DbEditableText.get_text('contacts')  
    if not editable_text:  
        return  
    if callback_query.message.text != editable_text.content:  
        await callback_query.message.edit_text(
            editable_text.content,  
            reply_markup=start_panel_kb
        )


back_to_accommodation = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Вернуться", callback_data="accommodation")]
    ]
)


@router.callback_query(lambda c: c.data == 'accommodation')
async def accommodation_handler(callback_query: types.CallbackQuery):
    """Обработчик кнопки 'accommodation', выводит список точек проживания с кнопками."""
    editable_text = await DbEditableText.get_text('accommodation')
    if not editable_text:
        return

    accommodations = await DbAccomodation.get_all_accomodation()  
    if not accommodations:
        await callback_query.message.edit_text("⚠️ Нет доступных точек проживания.")
        return
    builder = InlineKeyboardBuilder()
    for accommodation in accommodations:
        builder.row(InlineKeyboardButton(
            text=accommodation.name,
            callback_data=f"view_accommodation_{accommodation.id}"
        ))
    builder.row(InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_accommodation"))

    await callback_query.message.edit_text(
        editable_text.content,
        reply_markup=builder.as_markup()
    )


@router.callback_query(F.data.startswith("view_accommodation_"))
async def view_accommodation(callback_query: types.CallbackQuery):
    """Просмотр выбранной точки проживания с кнопкой для возврата."""
    accommodation_id = int(callback_query.data.replace("view_accommodation_", ""))
    accommodation = await DbAccomodation.get_accomodation(accommodation_id)

    if accommodation:
        await callback_query.message.edit_text(
            f"🏠 Название: {accommodation.name}\n"
            f"📖 Описание: {accommodation.description}",
            reply_markup=InlineKeyboardBuilder()
                .add(InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_accommodation"))
                .as_markup()
        )
    else:
        await callback_query.answer("⚠️ Точка проживания не найдена.")


@router.callback_query(lambda c: c.data == 'entertainment')
async def entertainment_handler(callback_query: CallbackQuery):
    """Обработчик кнопки 'entertainment', выводит список развлечений с кнопками."""
    editable_text = await DbEditableText.get_text('entertainment')
    if not editable_text:
        return

    entertainments = await DbEntertainment.get_all_entertainment() 
    builder = InlineKeyboardBuilder()
    for entertainment in entertainments:
        builder.row(InlineKeyboardButton(text=entertainment.name, callback_data=f"view_entertainment_{entertainment.id}"))
    builder.row(InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_entertainment"))
    
    await callback_query.message.edit_text(
        editable_text.content,
        reply_markup=builder.as_markup()
    )


@router.callback_query(F.data.startswith("view_entertainment_"))
async def view_entertainment(callback_query: types.CallbackQuery):
    """Просмотр выбранного развлечения с кнопкой для возврата."""
    entertainment_id = int(callback_query.data.replace("view_entertainment_", ""))
    entertainment = await DbEntertainment.get_entertainment(entertainment_id)

    if entertainment:
        await callback_query.message.edit_text(
            f"🎭 Название: {entertainment.name}\n"
            f"📖 Описание: {entertainment.description}",
            reply_markup=InlineKeyboardBuilder()
                .add(InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_entertainment"))
                .as_markup()
        )
    else:
        await callback_query.answer("⚠️ Развлечение не найдено.")


@router.callback_query(lambda c: c.data == 'local_food')
async def local_cuisine_handler(callback_query: CallbackQuery):
    """Обработчик кнопки 'local_food', выводит список блюд с кнопками."""
    editable_text = await DbEditableText.get_text('local_food')
    if not editable_text:
        return

    localfoods = await DbLocalFood.get_all_local_foods()  
    builder = InlineKeyboardBuilder()
    for localfood in localfoods:
        builder.row(InlineKeyboardButton(text=localfood.name, callback_data=f"view_localfood_{localfood.id}"))
    builder.row(InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_local_food"))
    
    await callback_query.message.edit_text(
        editable_text.content,
        reply_markup=builder.as_markup()
    )


@router.callback_query(F.data.startswith("view_localfood_"))
async def view_localfood(callback_query: types.CallbackQuery):
    """Просмотр выбранного блюда с кнопкой для возврата."""
    localfood_id = int(callback_query.data.replace("view_localfood_", ""))
    localfood = await DbLocalFood.get_local_food(localfood_id)

    if localfood:
        await callback_query.message.edit_text(
            f"🍽 Название блюда: {localfood.name}\n"
            f"📖 Описание: {localfood.description}",
            reply_markup=InlineKeyboardBuilder()
                .add(InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_local_food"))
                .as_markup()
        )
    else:
        await callback_query.answer("⚠️ Блюдо не найдено.")


@router.callback_query(lambda c: c.data == 'tour')
async def excursions_handler(callback_query: CallbackQuery):
    """Обработчик кнопки 'excursions', выводит список туров с кнопками."""
    editable_text = await DbEditableText.get_text('tour')
    if not editable_text:
        return

    tours = await DbTour.get_all_tours()  
    builder = InlineKeyboardBuilder()
    for tour in tours:
        builder.row(InlineKeyboardButton(text=tour.name, callback_data=f"view_tour_{tour.id}"))
    builder.row(InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_excursions"))
    await callback_query.message.edit_text(
        editable_text.content,
        reply_markup=builder.as_markup()
    )


@router.callback_query(F.data.startswith("view_tour_"))
async def view_tour(callback_query: types.CallbackQuery):
    """Просмотр выбранного тура с кнопкой для возврата."""
    tour_id = int(callback_query.data.replace("view_tour_", ""))
    tour = await DbTour.get_tour(tour_id)

    if tour:
        await callback_query.message.edit_text(
            f"📌 Название тура: {tour.name}\n"
            f"📖 Описание: {tour.description}",
            reply_markup=InlineKeyboardBuilder()
                .add(InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_excursions"))
                .as_markup()
        )
    else:
        await callback_query.answer("⚠️ Тур не найден.")


@router.callback_query(lambda c: c.data == 'back_to_accommodation')
async def back_to_accommodation(callback_query: CallbackQuery):
    """Возвращает к списку точек проживания."""
    editable_text = await DbEditableText.get_text('accommodation')
    if not editable_text:
        return

    accommodations = await DbAccomodation.get_all_accomodation()
    builder = InlineKeyboardBuilder()
    for accommodation in accommodations:
        builder.row(InlineKeyboardButton(
            text=accommodation.name,
            callback_data=f"view_accommodation_{accommodation.id}"
        ))
    builder.row(InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_main"))

    await callback_query.message.edit_text(
        editable_text.content,
        reply_markup=builder.as_markup()
    )


@router.callback_query(lambda c: c.data == 'back_to_entertainment')
async def back_to_entertainment(callback_query: CallbackQuery):
    """Возвращает к списку развлечений."""
    editable_text = await DbEditableText.get_text('entertainment')
    if not editable_text:
        return

    entertainments = await DbEntertainment.get_all_entertainment()
    builder = InlineKeyboardBuilder()
    for entertainment in entertainments:
        builder.row(InlineKeyboardButton(
            text=entertainment.name,
            callback_data=f"view_entertainment_{entertainment.id}"
        ))
    builder.row(InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_main"))

    await callback_query.message.edit_text(
        editable_text.content,
        reply_markup=builder.as_markup()
    )


@router.callback_query(lambda c: c.data == 'back_to_local_food')
async def back_to_local_food(callback_query: CallbackQuery):
    """Возвращает к списку блюд."""
    editable_text = await DbEditableText.get_text('local_food')
    if not editable_text:
        return

    localfoods = await DbLocalFood.get_all_local_foods()
    builder = InlineKeyboardBuilder()
    for localfood in localfoods:
        builder.row(InlineKeyboardButton(
            text=localfood.name,
            callback_data=f"view_localfood_{localfood.id}"
        ))
    builder.row(InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_main"))

    await callback_query.message.edit_text(
        editable_text.content,
        reply_markup=builder.as_markup()
    )


@router.callback_query(lambda c: c.data == 'back_to_excursions')
async def back_to_excursions(callback_query: CallbackQuery):
    """Возвращает к списку туров."""
    editable_text = await DbEditableText.get_text('tour')
    if not editable_text:
        return

    tours = await DbTour.get_all_tours()
    builder = InlineKeyboardBuilder()
    for tour in tours:
        builder.row(InlineKeyboardButton(
            text=tour.name,
            callback_data=f"view_tour_{tour.id}"
        ))
    builder.row(InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_main"))

    await callback_query.message.edit_text(
        editable_text.content,
        reply_markup=builder.as_markup()
    )


@router.callback_query(lambda c: c.data == 'back_to_main')
async def back_to_main(callback_query: CallbackQuery):
    """Возвращает в главное меню."""
    await callback_query.message.edit_text("Главное меню:", reply_markup=start_panel_kb)