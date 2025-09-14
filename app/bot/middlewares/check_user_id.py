from aiogram import BaseMiddleware
from aiogram.types import Update, CallbackQuery, Message
from app.core import logger


class EnsureUserMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data: dict):
        user = None

        if isinstance(event, Update):
            if event.callback_query:
                user = event.callback_query.from_user
            elif event.message:
                user = event.message.from_user
            elif event.edited_message:
                user = event.edited_message.from_user

        elif isinstance(event, CallbackQuery):
            user = event.from_user

        elif isinstance(event, Message):
            user = event.from_user

        if user and user.is_bot:
            logger.warning(f"Middleware: Update from bot ignored (user_id={user.id}).")
            return

        return await handler(event, data)
