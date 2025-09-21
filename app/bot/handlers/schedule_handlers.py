from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from app.core import logger, get_user_info, parse_user_text
from app.bot import (
    CreateSchedule,
    AddingItems,
    inline_build_schedule_type,
    inline_build_edit_exists_schedule,
    inline_build_select_day_of_week
)
from app.database import (
    schedule_repos,
    ScheduleType,
    DayOfWeek
)


router = Router()


@router.message(F.text == '📅Today')
async def cmd_today(message: Message) -> None:
    user_id, username, first_name, last_name = await get_user_info(message)

    today_items = await schedule_repos.check_today_schedule(user_id)

    if not today_items:
        await message.answer("Today you have no tasks")
        return

    text_lines = []
    for item in today_items:
        line = f"{item.time_start.strftime('%H:%M')}–{item.time_end.strftime('%H:%M')} — {item.title}"
        if item.description:
            line += f" ({item.description})"
        text_lines.append(line)

    text = "📅 Today's schedule:\n\n" + "\n".join(text_lines)

    await message.answer(text)
    
    
@router.message(F.text == '📅This week')
async def cmd_this_week(message: Message) -> None:
    ...
    

@router.message(F.text == '📅Edit existing schedule')
async def cmd_edit_existing_shedule(message: Message) -> None:
    user_id, username, first_name, last_name  = await get_user_info(message)
    
    schedules, has_next = await schedule_repos.get_user_schedules_paginated(
        user_id = user_id,
        page = 0
    )
    
    await message.answer(
        f'Your schedules:',
        reply_markup=await inline_build_edit_exists_schedule(
            schedules, 0, has_next
        )
    )


@router.callback_query(F.data.startswith("schedule_select:"))
async def process_schedule_select(callback: CallbackQuery, state: FSMContext) -> None:
    user_id, username, first_name, last_name = await get_user_info(callback)

    schedule_id = int(callback.data.split(":")[1])
    await callback.answer(f"You have selected the schedule with ID: {schedule_id}")

    schedule = await schedule_repos.check_schedule_type(
        user_id,
        schedule_id,
        ["DAILY", "WEEKLY"]
    )

    if not schedule:
        await callback.message.answer("Schedule not found.")
        return

    schedule_type = schedule.type

    await state.update_data(schedule_id=schedule_id, schedule_type=schedule_type)

    if schedule_type == ScheduleType.WEEKLY:
        await callback.message.answer(
            "Before proceeding, choose a day of the week for your plan.",
            reply_markup=await inline_build_select_day_of_week()
        )
    elif schedule_type == ScheduleType.DAILY:
        await state.set_state(AddingItems.waiting_for_schedule_items_text)
        await callback.message.answer(
            "Now, please send the full text of your daily plan.\n\n"
            "Format:\n"
            "06:00–07:30 — Wake up, morning routine (wash, breakfast)\n"
            "07:30-8:00 — Go to the bus stop and school\n"
            "08:00–15:30 — School\n"
            "15:30–16:00 — Lunch + rest\n"
            "16:00–16:50 — Language (English)\n\n"
            "✅ Each line must contain time and activity.\n"
            "✅ You can optionally add a description in brackets ( )."
        )


@router.callback_query(F.data.startswith("day_inline_"))
async def process_day_select(callback: CallbackQuery, state: FSMContext) -> None:
    day_selected = callback.data.replace("day_inline_", "").upper()

    await state.update_data(day_of_week=DayOfWeek[day_selected])

    await state.set_state(AddingItems.waiting_for_schedule_items_text)

    await callback.message.answer(
        f"You selected **{day_selected}**.\n\n"
        "Now, please send the full text of your plan for this day.\n\n"
        "Format:\n"
        "06:00–07:30 — Wake up, morning routine (wash, breakfast)\n"
        "07:30 — Go to the bus stop\n"
        "08:00–15:30 — School\n"
        "15:30–16:00 — Lunch + rest\n"
        "16:00–16:50 — Language (English)\n\n"
        "✅ Each line must contain time and activity.\n"
        "✅ You can optionally add a description in brackets ( )."
    )


@router.message(AddingItems.waiting_for_schedule_items_text)
async def process_plan_text(message: Message, state: FSMContext):
    user_id = message.from_user.id
    raw_text = message.text

    data = await state.get_data()
    schedule_id = data.get("schedule_id")
    day_of_week = data.get("day_of_week", None)

    items = await parse_user_text(raw_text, day_of_week)

    await schedule_repos.add_item_in_schedule(
        user_id=user_id,
        schedule_id=schedule_id,
        items=items
    )

    await message.answer(f"✅ Added {len(items)} items to schedule!")

    await state.clear()
    

@router.callback_query(F.data.startswith("schedule_page:"))
async def process_schedule_page(callback: CallbackQuery) -> None:
    user_id, username, first_name, last_name  = await get_user_info(callback)
    
    page = int(callback.data.split(":")[1])
    
    schedules, has_next = await schedule_repos.get_user_schedules_paginated(
        user_id = user_id,
        page = page
    )
    
    await callback.message.answer(
        "Your schedules:",
        reply_markup=await inline_build_edit_exists_schedule(
            schedules, page, has_next
        )
    )
    await callback.answer()



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


@router.callback_query(CreateSchedule.waiting_for_type)
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
