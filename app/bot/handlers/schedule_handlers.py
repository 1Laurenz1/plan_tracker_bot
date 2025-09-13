from aiogram import Router, F
from aiogram.types import Message

from app.core import logger, get_user_info


router = Router()


@router.message(F.text == '📅Today')
async def cmd_today(message: Message) -> None:
    ...
    
    
@router.message(F.text == '📅This week')
async def cmd_this_week(message: Message) -> None:
    ...
    

@router.message(F.text == '📅Edit existing shedule')
async def cmd_edit_existing_shedule(message: Message) -> None:
    ...
    

@router.message(F.text == '🆕Create new shedule')
async def cmd_create_new_shedule(message: Message) -> None:
    ...