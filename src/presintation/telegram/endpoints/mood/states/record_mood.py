from aiogram.fsm.state import State, StatesGroup


class MoodFlow(StatesGroup):
    selecting_mood = State()
    confirming_update = State()
