from aiogram.types import Message

from typing import Tuple

from app.core import logger


async def get_user_info(message: Message) -> Tuple[int, str]:
    user_id = getattr(message.from_user, 'id', None)
    username = getattr(message.from_user, 'username', 'Unknown')
    first_name = getattr(message.from_user, 'first_name', '')
    last_name = getattr(message.from_user, 'last_name', '')
    
    if not user_id:
        logger.error("User ID is missing in the message")
        raise ValueError("User ID is missing in the message")
    
    logger.info(
        f'Excracted user info - ID: {user_id}, Username: {username}'
    )
        
    return user_id, username, first_name, last_name