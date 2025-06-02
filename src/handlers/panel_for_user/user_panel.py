from aiogram import Router, types, F
from aiogram.types import CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from src.utils.keyboard.user import start_panel_kb
from src.database.models import DbEditableText, DbTour, DbAccomodation, DbLocalFood, DbEntertainment

router = Router()


@router.callback_query(lambda c: c.data == 'about_us')
async def about_us_handler(callback_query: CallbackQuery):
    editable_text = await DbEditableText.get_text('about_us')
    if editable_text and callback_query.message.text != editable_text.content:
        await callback_query.message.edit_text(
            editable_text.content,
            reply_markup=start_panel_kb
        )
    await callback_query.answer()


@router.callback_query(lambda c: c.data == 'get_discount')
async def get_discount_handler(callback_query: CallbackQuery):
    editable_text = await DbEditableText.get_text('get_discount')
    if editable_text and callback_query.message.text != editable_text.content:
        await callback_query.message.edit_text(
            editable_text.content,
            reply_markup=start_panel_kb
        )
    await callback_query.answer()


@router.callback_query(lambda c: c.data == 'contacts')
async def contacts_handler(callback_query: CallbackQuery):
    editable_text = await DbEditableText.get_text('contacts')
    if editable_text and callback_query.message.text != editable_text.content:
        await callback_query.message.edit_text(
            editable_text.content,
            reply_markup=start_panel_kb
        )
    await callback_query.answer()


async def create_items_list(callback_query: CallbackQuery,
                            text_key: str,
                            db_func,
                            view_prefix: str,
                            empty_message: str):
    editable_text = await DbEditableText.get_text(text_key)
    if not editable_text:
        return await callback_query.answer("Контент не найден", show_alert=True)

    items = await db_func()
    builder = InlineKeyboardBuilder()

    if items:
        for item in items:
            builder.add(InlineKeyboardButton(
                text=item.name,
                callback_data=f"{view_prefix}_{item.id}"
            ))
        builder.adjust(1)
    else:
        builder.add(InlineKeyboardButton(
            text="🔙 Назад",
            callback_data="back_to_main"
        ))

    builder.row(InlineKeyboardButton(
        text="🔙 Назад",
        callback_data="back_to_main"
    ))

    new_text = editable_text.content if items else empty_message
    current_text = callback_query.message.text

    if current_text != new_text:
        await callback_query.message.edit_text(
            new_text,
            reply_markup=builder.as_markup()
        )
    else:
        await callback_query.message.edit_reply_markup(
            reply_markup=builder.as_markup()
        )

    await callback_query.answer()


# Универсальная функция для просмотра элемента
async def view_item(callback_query: CallbackQuery,
                    item_id: str,
                    db_func,
                    back_handler: str,
                    title: str):
    item = await db_func(int(item_id))
    if not item:
        return await callback_query.answer("Элемент не найден", show_alert=True)

    await callback_query.message.edit_text(
        f"{title}: {item.name}\n"
        f"📖 Описание: {item.description}",
        reply_markup=InlineKeyboardBuilder()
        .add(InlineKeyboardButton(
            text="🔙 Назад",
            callback_data=back_handler
        ))
        .as_markup()
    )
    await callback_query.answer()


# Обработчики разделов
@router.callback_query(lambda c: c.data == 'accommodation')
async def accommodation_handler(callback_query: CallbackQuery):
    await create_items_list(
        callback_query,
        'accommodation',
        DbAccomodation.get_all_accomodation,
        'view_accommodation',
        "Нет доступных точек проживания"
    )


@router.callback_query(lambda c: c.data == 'entertainment')
async def entertainment_handler(callback_query: CallbackQuery):
    await create_items_list(
        callback_query,
        'entertainment',
        DbEntertainment.get_all_entertainment,
        'view_entertainment',
        "Нет доступных развлечений"
    )


@router.callback_query(lambda c: c.data == 'local_food')
async def local_cuisine_handler(callback_query: CallbackQuery):
    await create_items_list(
        callback_query,
        'local_food',
        DbLocalFood.get_all_local_foods,
        'view_localfood',
        "Нет доступных блюд"
    )


@router.callback_query(lambda c: c.data == 'tour')
async def excursions_handler(callback_query: CallbackQuery):
    await create_items_list(
        callback_query,
        'tour',
        DbTour.get_all_tours,
        'view_tour',
        "Нет доступных туров"
    )


# Обработчики просмотра элементов
@router.callback_query(F.data.startswith("view_accommodation_"))
async def view_accommodation(callback_query: types.CallbackQuery):
    await view_item(
        callback_query,
        callback_query.data.replace("view_accommodation_", ""),
        DbAccomodation.get_accomodation,
        "back_to_accommodation",
        "🏠 Название"
    )


@router.callback_query(F.data.startswith("view_entertainment_"))
async def view_entertainment(callback_query: types.CallbackQuery):
    await view_item(
        callback_query,
        callback_query.data.replace("view_entertainment_", ""),
        DbEntertainment.get_entertainment,
        "back_to_entertainment",
        "🎭 Название"
    )


@router.callback_query(F.data.startswith("view_localfood_"))
async def view_localfood(callback_query: types.CallbackQuery):
    await view_item(
        callback_query,
        callback_query.data.replace("view_localfood_", ""),
        DbLocalFood.get_local_food,
        "back_to_local_food",
        "🍽 Название блюда"
    )


@router.callback_query(F.data.startswith("view_tour_"))
async def view_tour(callback_query: types.CallbackQuery):
    await view_item(
        callback_query,
        callback_query.data.replace("view_tour_", ""),
        DbTour.get_tour,
        "back_to_excursions",
        "📌 Название тура"
    )


@router.callback_query(lambda c: c.data == 'back_to_accommodation')
async def back_to_accommodation_handler(callback_query: CallbackQuery):
    await accommodation_handler(callback_query)


@router.callback_query(lambda c: c.data == 'back_to_entertainment')
async def back_to_entertainment_handler(callback_query: CallbackQuery):
    await entertainment_handler(callback_query)


@router.callback_query(lambda c: c.data == 'back_to_local_food')
async def back_to_local_food_handler(callback_query: CallbackQuery):
    await local_cuisine_handler(callback_query)


@router.callback_query(lambda c: c.data == 'back_to_excursions')
async def back_to_excursions_handler(callback_query: CallbackQuery):
    await excursions_handler(callback_query)


@router.callback_query(lambda c: c.data == 'back_to_main')
async def back_to_main_handler(callback_query: CallbackQuery):
    try:
        await callback_query.message.edit_text(
            "Главное меню:",
            reply_markup=start_panel_kb
        )
        await callback_query.answer()
    except:
        await callback_query.answer("Ошибка возврата в меню", show_alert=True)