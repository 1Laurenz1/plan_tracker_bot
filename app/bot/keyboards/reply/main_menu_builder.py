from aiogram.utils.keyboard import (
    ReplyKeyboardBuilder,
)
from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
)

from typing import List

from app.core import logger


async def build_main_menu(buttons: List[str] = None) -> ReplyKeyboardMarkup:
    
    if buttons is None:
        buttons = [
            "🏠Main", "📅Schedule", "⚙️Settings",
            "❓Help"
        ]

    builder = ReplyKeyboardBuilder()
    
    builder.add(*(KeyboardButton(text=b) for b in buttons))
    builder.adjust(2)
    
    logger.info("Main menu keyboard built successfull.")
    
    return builder.as_markup(
        resize_keyboard=True,
        one_time_keyboard=True
    )