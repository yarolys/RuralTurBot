from aiogram import F, Router
from aiogram.types import CallbackQuery

from src.utils.keyboard.user import start_panel_kb


router = Router()

from aiogram import F, Router
from aiogram.types import CallbackQuery
from src.utils.keyboard.user import start_panel_kb  

router = Router()

@router.callback_query(lambda c: c.data == 'about_us')
async def about_us_handler(callback_query: CallbackQuery):
    new_text = (
    '🌿 О нас\n\n'
    'Мы — команда, стремящаяся создать уникальную платформу для всех любителей природы и уютного отдыха.\n\n'
    'На "Деревенских приключениях" вы можете насладиться лучшими местами для проживания в окружении природы, вкусной местной кухней и увлекательными экскурсиями. Мы верим, что каждый заслуживает отдых, который наполняет силы и вдохновляет на новые подвиги.\n\n'
    '🌍 Наши ценности:\n'
    '1. Уют и комфорт для каждого гостя.\n'
    '2. Чистота и природная красота.\n'
    '3. Поддержка местных фермеров и производителей.\n'
    '4. Искренность и доверие.\n\n'
    'Мы рады каждому гостю и уверены, что ваше пребывание здесь будет незабываемым! 🌟'
    )

    if callback_query.message.text != new_text:
        await callback_query.message.edit_text(
            new_text,
            reply_markup=start_panel_kb  
        )



@router.callback_query(lambda c: c.data == 'get_discount')
async def get_discount_handler(callback_query: CallbackQuery):
    new_text = (
        '🌟 Поздравляем, вы получили скидку 10%! 🌟\n\n'
        f'🔥 Используйте промокод Polk10 на нашем сайте или в ЛС @polk_mn, чтобы получить скидку на отдых.\n\n'
        '📅 Скидка действительна до конца месяца, не упустите шанс!'
        '\n\n🌿 Приятных приключений на Деревенских приключениях!'
    )
    if callback_query.message.text != new_text:
        await callback_query.message.edit_text(
            new_text,
            reply_markup=start_panel_kb
        )