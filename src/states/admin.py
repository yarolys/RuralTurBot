from aiogram.fsm.state import StatesGroup, State


class EditTextState(StatesGroup):
    waiting_for_new_text = State()

class AddTourState(StatesGroup):
    waiting_for_tour_name = State()
    waiting_for_tour_description = State()

class DeleteTourState(StatesGroup):
    delete_tour = State()

class AddAccomodationState(StatesGroup):
    waiting_for_accomodation_name = State()
    waiting_for_accomodation_description = State()

class AddEntertainmentState(StatesGroup):
    waiting_for_entertainment_name = State()
    waiting_for_entertainment_description = State()

class AddLocalFoodState(StatesGroup):
    waiting_for_localfood_name = State()
    waiting_for_localfood_description = State()
    