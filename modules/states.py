from aiogram.fsm.state import StatesGroup, State


class Form(StatesGroup):
    record = State()
    categories = State()
    text = State()


class Categories(StatesGroup):
    name = State()
