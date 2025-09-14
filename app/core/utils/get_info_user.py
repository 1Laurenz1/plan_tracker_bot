from aiogram.types import Message

from typing import Tuple

from app.core import logger


async def get_user_info(message: Message) -> Tuple[int, str]:
    user_id = getattr(message.from_user, 'id', None)
    username = getattr(message.from_user, 'username', 'Unknown')
    first_name = getattr(message.from_user, 'first_name', '')
    last_name = getattr(message.from_user, 'last_name', '')
    
    if getattr(message.from_user, 'is_bot', False):
        logger.error("Message is from a bot, ignoring.")
        raise ValueError("Cannot process messages from bots.")
    
    if not user_id:
        logger.error("User ID is missing in the message")
        raise ValueError("User ID is missing in the message")
    
    logger.debug(f"Message.from_user content: {message.from_user}")
    logger.info(
        f'Extracted user info - ID: {user_id}, Username: {username}, First Name: {first_name}, Last Name: {last_name}'
    )
        
    return user_id, username, first_name, last_name