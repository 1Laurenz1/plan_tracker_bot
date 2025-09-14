from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.core import logger

from typing import Dict


async def inline_build_schedule_type(buttons: Dict[str, str] = None) -> InlineKeyboardMarkup:
    inline_builder = InlineKeyboardBuilder()
    
    if not buttons:
        buttons = {
            'Daily': "inline_daily",
            'Weekly': "inline_weekly",
        }
        
    inline_builder.add(
        *(
            InlineKeyboardButton(text=text, callback_data=cb)
            for text, cb in buttons.items()
        )
    )
    inline_builder.adjust(2)
    
    logger.info('inline_build_schedule_type built successfull')
    
    return inline_builder.as_markup()