from aiogram.fsm.state import State, StatesGroup

class UserStates(StatesGroup):
    waiting_photo_for_haircut_board = State()
    waiting_photo_for_color_board = State()
    waiting_photo_for_style_identity_board = State()

    generating = State()
    result_ready = State()
    error = State()