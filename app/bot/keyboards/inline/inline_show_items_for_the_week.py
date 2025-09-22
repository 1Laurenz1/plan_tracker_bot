from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from typing import Dict, List, Any


async def inline_build_show_items_for_the_week(
    day_index: int, total_days: int
) -> InlineKeyboardMarkup:
    inline_builder = InlineKeyboardBuilder()
    
    if day_index > 0:
        inline_builder.button(
            text="⬅️Prev",
            callback_data=f"week_day:{day_index-1}"
        )
        
    if day_index < total_days - 1:
        inline_builder.button(
            text="Next➡️",
            callback_data=f"week_day:{day_index+1}"
        )
        
    inline_builder.adjust(2)
    
    return inline_builder.as_markup()