from aiogram.fsm.state import StatesGroup, State


class EditTextState(StatesGroup):
    waiting_for_new_text = State()