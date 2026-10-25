from aiogram.fsm.state import State, StatesGroup


class TrackState(StatesGroup):
    marker = State()
    post = State()
