from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.core import logger

from typing import Dict


async def inline_build_edit_exists_schedule(buttons: Dict[str, str], id: int) -> InlineKeyboardMarkup:
    inline_builder = InlineKeyboardBuilder()
    
    buttons = {
        "Edit": f"edit_exists_schedule:{id}",
        "Delete": f"delete_exists_schedule:{id}",
    }
    
    for text, callback_data in buttons.items():   
        inline_builder.button(
            text=text,
            callback_data=callback_data
        )
        
    inline_builder.adjust(2)
    
    logger.info('inline_build_edit_exists_schedule built successfull')
    
    return inline_builder.as_markup()