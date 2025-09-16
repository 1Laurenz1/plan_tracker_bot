from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from typing import Dict

from app.core import logger


async def inline_build_edit_exists_schedule(schedules: list, page: int, has_next: bool) -> InlineKeyboardMarkup:
    inline_builder = InlineKeyboardBuilder()
    
    for s in schedules:
        inline_builder.add(
            InlineKeyboardButton(
                text=f"{s.name} ({s.type})",
                callback_data=f"schedule_select:{s.id}"
            )
        )
 
    nav_buttons = []
    if page > 0:
        nav_buttons.append(
            InlineKeyboardButton(
                text="⬅️Prev",
                callback_data=f"schedule_page:{page - 1}"
            )
        )
    if has_next:
        nav_buttons.append(
            InlineKeyboardButton(
                text="➡️Next",
                callback_data=f"schedule_page:{page + 1}"
            )
        )

    if nav_buttons:
        inline_builder.row(*nav_buttons)
        
    inline_builder.adjust(2)
        
    logger.info('inline_build_edit_exists_schedule built successfull')
        

    return inline_builder.as_markup()
