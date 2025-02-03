import asyncio

from aiogram import Dispatcher
from src.config import bot, logger
from src.handlers import (
    start_router,
    user_panel_router,
    admin_panel_router,
    control_buttons_router,
    tour_panel_router,
    user_list_router,
    accomodation_buttons_router,
    entertainment_buttons_router,
    localfood_buttons_router,
)


async def main():
    dp = Dispatcher()
    dp.include_routers(
        start_router,
        user_panel_router,
        admin_panel_router,
        control_buttons_router,
        tour_panel_router,
        user_list_router,
        accomodation_buttons_router,
        entertainment_buttons_router,
        localfood_buttons_router,
    )
    r = await bot.get_me()
    logger.info(f"Бот запущен: https://t.me/{r.username}")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
