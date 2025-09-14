from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton
)

from app.core import logger

from typing import List


async def build_schedule_menu(buttons: List[str] = None) -> ReplyKeyboardMarkup:
    if buttons is None:
        buttons = [
            "📅Today", "📅This week",
            "📅Edit existing schedule", "🆕Create new schedule",
            "🔙Back to main menu"
        ]
    
    builder = ReplyKeyboardBuilder()
    
    builder.add(*(KeyboardButton(text=b) for b in buttons))
    builder.adjust(2)
    
    logger.info("Schedule menu keyboard built successfully.")
    
    return builder.as_markup(
        resize_keyboard=True,
        one_time_keyboard=True
    )