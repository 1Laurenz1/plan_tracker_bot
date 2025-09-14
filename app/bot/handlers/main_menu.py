from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from app.bot import build_schedule_menu
from app.core import logger, get_user_info


router = Router()


@router.message(F.text == '📅Schedule')
async def cmd_schedule(message: Message):
    await message.answer(
        'Schedule...',
        reply_markup=await build_schedule_menu()
    )