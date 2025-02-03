from aiogram import Router, types, F
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext

from src.utils.keyboard.user import start_panel_kb, back_to_excursions, back_to_main
from src.database.models import DbEditableText, DbTour, DbAccomodation
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
    builder.row(InlineKeyboardButton(text="🔙 Вернуться", callback_data="back_to_main"))

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
            reply_markup=back_to_accommodation
        )
    else:
        await callback_query.answer("⚠️ Точка проживания не найдена.")


@router.callback_query(lambda c: c.data == 'entertainment')
async def entertainment_handler(callback_query: CallbackQuery):
    editable_text = await DbEditableText.get_text('entertainment')  
    if not editable_text:  
        return  
    if callback_query.message.text != editable_text.content:  
        await callback_query.message.edit_text(
            editable_text.content,  
            reply_markup=start_panel_kb
        )


@router.callback_query(lambda c: c.data == 'local_food')
async def local_cuisine_handler(callback_query: CallbackQuery):
    editable_text = await DbEditableText.get_text('local_food')  
    if not editable_text:  
        return  
    if callback_query.message.text != editable_text.content:  
        await callback_query.message.edit_text(
            editable_text.content,  
            reply_markup=start_panel_kb
        )


@router.callback_query(lambda c: c.data == 'excursions')
async def local_cuisine_handler(callback_query: CallbackQuery):
    editable_text = await DbEditableText.get_text('tour')  
    if not editable_text:  
        return  
    if callback_query.message.text != editable_text.content:  
        await callback_query.message.edit_text(
            editable_text.content,  
            reply_markup=start_panel_kb
        )


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
    builder.row(InlineKeyboardButton(text="🔙 Вернуться", callback_data="back_to_main"))
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
            reply_markup=back_to_excursions
        )
    else:
        await callback_query.answer("⚠️ Тур не найден.")


@router.callback_query(lambda c: c.data == 'back_to_main')
async def back_to_main(callback_query: CallbackQuery):
    """Возвращает в главное меню."""
    await callback_query.message.edit_text("Главное меню:", reply_markup=start_panel_kb)