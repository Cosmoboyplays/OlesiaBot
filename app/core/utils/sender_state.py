from aiogram.fsm.state import StatesGroup, State

class StepsAdminForm(StatesGroup):
    GET_SENDER = State()
    GET_NAME_CAMP = State()
    GET_MESSAGE = State()
    GET_CONFIRM = State()