from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


class CreateSchedule(StatesGroup):
    waiting_for_name = State()
    waiting_for_type = State()