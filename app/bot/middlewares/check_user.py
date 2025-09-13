from aiogram import BaseMiddleware
from aiogram.types import Message
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.core import logger, get_user_info
from app.database import AsyncSessionLocal, User

from typing import Callable, Awaitable, Any, Dict


class CheckUserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ):
        user_id, username, first_name, last_name = await get_user_info(event)
        logger.info(f"Checking user with ID: {user_id}")

        async with AsyncSessionLocal() as session:
            try:
                result = await session.execute(
                    select(User).where(User.user_id == user_id)
                )
                user = result.scalar_one_or_none()
                
                if not user:
                    new_user = User(
                        user_id=user_id,
                        username=username,
                        first_name=first_name,
                        last_name=last_name,
                    )
                    
                    session.add(new_user)
                    await session.commit()

                    await session.refresh(user)
                    session.expunge(user)

                    data["user"] = user
                    logger.debug(f"User ensured in DB: {user.user_id} ({user.username})")
                else:
                    logger.info(
                        f'User {username}({user_id}) allready exists.'
                    )
            except SQLAlchemyError as e:
                await session.rollback()
                logger.error(f"DB error while ensuring user {user_id}: {e}")
                data["user"] = None

        return await handler(event, data)