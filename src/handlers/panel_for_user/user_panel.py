from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from src.utils.keyboard.user import start_panel_kb
from src.database.models import DbEditableText
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


@router.callback_query(lambda c: c.data == 'accommodation')
async def accommodation_handler(callback_query: CallbackQuery):
    editable_text = await DbEditableText.get_text('accommodation')  
    if not editable_text:  
        return  
    if callback_query.message.text != editable_text.content:  
        await callback_query.message.edit_text(
            editable_text.content,  
            reply_markup=start_panel_kb
        )


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
async def excursions_handler(callback_query: CallbackQuery):
    editable_text = await DbEditableText.get_text('excursions')  
    if not editable_text:  
        return  
    if callback_query.message.text != editable_text.content:  
        await callback_query.message.edit_text(
            editable_text.content,  
            reply_markup=start_panel_kb
        )
