
from aiogram.fsm.state import State, StatesGroup

class LogState(StatesGroup):
    sleep = State()
    walk = State()
    workout = State()
    session_start = State()
    session_end = State()
    notes = State()
