from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

from app.core import logger


router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    username = message.from_user.username or message.from_user.first_name or "Unknown"
    user_id = getattr(message.from_user, "id", None)
    
    await message.answer(
        f'Hello, {username}!'
    )
    
    logger.info(
        f"User {username}({user_id}) started the bot."
    )