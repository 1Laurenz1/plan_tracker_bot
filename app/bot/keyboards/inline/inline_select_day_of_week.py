from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from typing import Dict

from app.core import logger


async def inline_build_select_day_of_week(buttons: Dict[str, str] = None) -> InlineKeyboardMarkup:
    inline_builder = InlineKeyboardBuilder()
    
    if not buttons:
        buttons = {
            "Monday": "day_inline_monday",
            "Tuesday": "day_inline_tuesday",
            "Wednesday": "day_inline_wednesday",
            "Thursday": "day_inline_thursday",
            "Friday": "day_inline_friday",
            "Saturday": "day_inline_saturday",
            "Sunday": "day_inline_sunday",
        }
        
    inline_builder.add(
        *(
            InlineKeyboardButton(text=text, callback_data=cb)
            for text, cb in buttons.items()
        )
    )
    
    inline_builder.adjust(1)
    
    logger.info(
        'inline_build_select_day_of_week built successfull'
    )
    
    return inline_builder.as_markup()