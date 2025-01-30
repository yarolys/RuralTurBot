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
    buttons = await DbEditableText.get_all_texts()
    
    if not buttons:
        await message.answer("⚠️ Нет доступных кнопок для редактирования.")
        return

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=button.name_button, callback_data=f"edit_{button.identifier}")]
            for button in buttons
        ]
    )

    await message.answer("Выберите кнопку для редактирования:", reply_markup=keyboard)
    await message.delete()


@router.callback_query(F.data.startswith("edit_"))
async def start_editing_button_text(callback_query: types.CallbackQuery, state: FSMContext):
    identifier = callback_query.data.replace("edit_", "")
    editable_text = await DbEditableText.get_text(identifier)
    if not editable_text:
        await callback_query.answer("⚠️ Ошибка! Текст для этой кнопки не найден.", show_alert=True)
        return

    await callback_query.message.edit_text(
        f"⚠️ Внимание!*\n"
        f"Вы находитесь в режиме редактирования кнопки: {editable_text.name_button}\n\n"
        f"Старый текст:\n\n"
        f"_{editable_text.content}_\n\n"
        f"Отправьте новый текст для этой кнопки или нажмите кнопку 'Отмена'.",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_editing")]]
        ),
        parse_mode="HTML"
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
    await message.answer(f"✅ Текст кнопки *{identifier}* успешно обновлён!", parse_mode="HTML",
                         reply_markup=start_panel_kb)
    await state.clear()


@router.callback_query(F.data == "cancel_editing")
async def cancel_editing(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.edit_text("🚫 Редактирование отменено.", reply_markup=start_panel_kb)
    await state.clear()
    await callback_query.answer()
