from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from app.core import logger, settings
from app.bot import start, CheckUserMiddleware
from app.database import engine

import asyncio


async def on_shutdown() -> None:
    await engine.dispose()
    logger.info("Database engine disposed.")


async def main() -> None:
    bot = Bot(
        token=settings.BOT_TOKEN.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    
    dp = Dispatcher()
    
    dp.message.middleware(CheckUserMiddleware())
    
    dp.include_routers(
        start.router
    )
    
    await bot.delete_webhook(drop_pending_updates=True)
    
    try:
        await dp.start_polling(bot)
        logger.info("Bot started successfully")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return None
    finally:
        await on_shutdown()
        logger.info("Bot shutdown complete.")
        
    

if __name__ == '__main__':
    asyncio.run(main())
    logger.info("Application started.")