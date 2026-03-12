from aiogram.fsm.state import State, StatesGroup


class StatsFlow(StatesGroup):
    viewing_stats = State()
