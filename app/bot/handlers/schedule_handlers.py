from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from app.core import logger, get_user_info
from app.bot import CreateSchedule, inline_build_schedule_type
from app.database import (
    schedule_repos,
    ScheduleType,
    DayOfWeek
)


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


@router.message(F.text == '🆕Create new schedule')
async def cmd_create_new_schedule(message: Message, state: FSMContext) -> None:
    await state.set_state(CreateSchedule.waiting_for_name)
    await message.answer("Please enter the name of the new schedule:")


@router.message(CreateSchedule.waiting_for_name)
async def process_schedule_name(message: Message, state: FSMContext) -> None:
    schedule_name = message.text.strip()

    if not schedule_name:
        await message.answer("Schedule name cannot be empty. Please enter a valid name:")
        return

    await state.update_data(schedule_name=schedule_name)
    await state.set_state(CreateSchedule.waiting_for_type)
    await message.answer(
        "Please choose the type for the new schedule:",
        reply_markup=await inline_build_schedule_type()
    )


@router.callback_query()
async def process_schedule_type(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    schedule_name = data.get("schedule_name")
    schedule_type_key = callback.data

    schedule_type_map = {
        "inline_daily": ScheduleType.DAILY,
        "inline_weekly": ScheduleType.WEEKLY,
    }

    if schedule_type_key not in schedule_type_map:
        await callback.answer("Invalid schedule type!", show_alert=True)
        return

    schedule_type = schedule_type_map[schedule_type_key]

    user = callback.from_user
    user_id = user.id
    username = user.username
    first_name = user.first_name
    last_name = user.last_name

    logger.info(f"Creating schedule for user {user_id} ({username})")

    new_schedule = await schedule_repos.create_schedule(
        user_id=user_id,
        name=schedule_name,
        schedule_type=schedule_type.value,
    )

    if new_schedule:
        await callback.message.answer(
            f"✅ Schedule '{schedule_name}' ({schedule_type.value}) created successfully!"
        )
        logger.info(f"Created schedule {schedule_name} for user {user_id}")
    else:
        await callback.message.answer("❌ Failed to create schedule, try again later.")

    await state.clear()
    await callback.answer()
