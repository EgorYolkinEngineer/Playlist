from aiogram.fsm.state import State, StatesGroup


class CreatePlaylistStatesGroup(StatesGroup):
    set_name = State()
    set_description = State()
    set_preview = State()
    