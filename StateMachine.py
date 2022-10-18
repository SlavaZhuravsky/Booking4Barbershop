from aiogram.dispatcher.filters.state import State, StatesGroup


class StateMachine(StatesGroup):
    service_type_state = State()
    name_state = State()
    date_state = State()
    time_state = State()
