from aiogram.fsm.state import StatesGroup, State

class StepsForm(StatesGroup):
    GET_NAME = State()
    GET_COURSE = State()
    GET_SPCLUB = State()
    GET_CONFIRM = State()
    GET_PAY = State()