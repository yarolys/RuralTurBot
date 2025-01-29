from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.database.models import DbEditableText
from src.utils.keyboard.user import start_panel_kb
from src.utils.filter import AdminRoleFilter
from src.states.admin import EditTextState

router = Router()



@router.message(F.text == "Управление текстами", AdminRoleFilter())
async def show_texts_menu(message: types.Message):
    button_ids = ['about_us', 'get_discount', 'contacts', 'accommodation', 'entertainment', 'local_food', 'excursions']
    for identifier in button_ids:
        editable_text = await DbEditableText.get_text(identifier)
        if not editable_text:
            # Если текста нет, создаем новый с пустым содержимым
            await DbEditableText.update_text(identifier, "")

    await message.answer(
        "Выберите текст для редактирования:",
        reply_markup=start_panel_kb
    )

@router.callback_query(F.data.in_(['about_us', 'get_discount', 'contacts', 'accommodation', 'entertainment', 'local_food', 'excursions']))
async def start_editing_button_text(callback_query: types.CallbackQuery, state: FSMContext):
    identifier = callback_query.data

    editable_text = await DbEditableText.get_text(identifier)
    if not editable_text:
        # Если текста нет, показываем сообщение
        await callback_query.message.answer("Текст для этой кнопки еще не задан.")
        return
    
    await callback_query.message.answer(
        f"⚠️ *Внимание!*\n"
        f"Вы находитесь в режиме редактирования кнопки: *{identifier}*\n\n"
        f"Старый текст:\n\n"
        f"_{editable_text.content}_\n\n"
        f"Отправьте новый текст для этой кнопки или нажмите кнопку 'Отмена'.",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_editing")]]
        ),
        parse_mode="Markdown"
    )

    await state.set_state(EditTextState.waiting_for_new_text)
    await state.update_data(identifier=identifier)


@router.message(EditTextState.waiting_for_new_text)
async def update_button_text(message: types.Message, state: FSMContext):
    state_data = await state.get_data()
    identifier = state_data.get("identifier")
    new_text = message.text.strip()

    if not new_text:
        await message.answer("⚠️ Новый текст не может быть пустым. Попробуйте снова.")
        return

    await DbEditableText.update_text(identifier, new_text)
    await message.answer(f"✅ Текст кнопки {identifier} успешно обновлён!", parse_mode="Markdown")
    await state.clear()


@router.callback_query(F.data == "cancel_editing")
async def cancel_editing(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer(
        "🚫 Редактирование отменено.",
        reply_markup=start_panel_kb  
    )
    await state.clear()