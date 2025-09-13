from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart

from app.core import logger, get_user_info
from app.bot import build_main_menu

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    username = message.from_user.username or message.from_user.first_name or "Unknown"
    user_id = getattr(message.from_user, "id", None)
    
    await message.answer(
        f'Hello, {username}!',
        reply_markup=await build_main_menu()
    )
    
    logger.info(
        f"User {username}({user_id}) started the bot."
    )
    
    
@router.message(F.text == "🔙Back to main menu")
async def cmd_back_to_main_menu(message: Message) -> None:
    user_id, username, first_name, last_name = await get_user_info(message)
    
    await message.answer(
        'Returning to main menu...',
        reply_markup=await build_main_menu()
    )
    
    logger.info(
        f'User {username}({user_id}) returned to main menu'
    )