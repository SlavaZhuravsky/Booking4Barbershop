import datetime
import logging

import aiogram
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup
from aiogram_calendar import simple_cal_callback, SimpleCalendar

import config
import messages
from StateMachine import StateMachine
from keyboards import markup, markup1, murkup2, my_notes
from sqlighter import SQLighter

logging.basicConfig(level=logging.INFO)

# Initialize telegram bot with MemoryStorage
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

# initialize calendar
start_kb = ReplyKeyboardMarkup(resize_keyboard=True, )
start_kb.row('Calendar')

# initialize DB
booking_db = SQLighter('booking.db')


def validateDate(date_text):
    if not type(date_text) is str:
        return False
    if datetime.datetime.strptime(date_text, '%d/%m/%Y'):
        return True
    else:
        return False


@dp.message_handler(commands=['start'])
async def start(message):
    await bot.send_message(message.chat.id, messages.start_message, reply_markup=markup)


@dp.message_handler(commands=['calendar'])
async def startCalendar(message):
    await bot.send_message(message.chat.id, messages.calendar_message, reply_markup=start_kb)


@dp.message_handler(Text(equals=['Calendar'], ignore_case=True))
async def nav_cal_handler(message: Message):
    await message.answer('выберете время для записи! ', reply_markup=await SimpleCalendar().start_calendar())


@dp.callback_query_handler(simple_cal_callback.filter())
async def process_calendar(callback_query: CallbackQuery, callback_data: dict):
    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
    if selected:
        await callback_query.message.answer(
            f'You selected {date.strftime("%d/%m/%Y")}',
            reply_markup=start_kb
        )
        StateMachine.date_state = str(date.strftime("%d/%m/%Y"))
        times = booking_db.get_booked_time(StateMachine.date_state)

        if not len(times) == 0:
            await callback_query.message.answer("Забронироыанное время: ")
            for t in times:
                await callback_query.message.answer(str(t))
        else:
            await callback_query.message.answer('Сегодня все доступно с 10:00 по 21:00!!!')

        await callback_query.message.answer("Хотите записаться? Нажмите /booking ! Выше указано занятое время!")


@dp.message_handler(commands=['booking'])
async def booking(message: aiogram.types.Message):
    await message.answer('введите Ваше Имя: ')
    await StateMachine.name_state.set()


# 2. Answer name
# if data is empty need to check and ask to write in format
@dp.message_handler(state=StateMachine.name_state)
async def stateName(message: aiogram.types.Message, state: FSMContext):
    await state.update_data(name_state=message.text)
    await message.answer('введите время согласно формату "17:30": ')
    await StateMachine.time_state.set()


# 3. Answer time
@dp.message_handler(state=StateMachine.time_state)
async def stateTime(message: aiogram.types.Message, state: FSMContext):
    # TODO if date not setup
    if not validateDate(StateMachine.date_state):
        await message.answer('Дата не указана! Введите дату согласно формату "18/10/2022": ')
        await StateMachine.date_state.set()
        # print('Date: ', str(get_date.strftime("%d/%m/%Y")))
        # StateMachine.date_state = str(StateMachine.date_state('date_state'))

    await state.update_data(time_state=message.text)
    user_name = await state.get_data('name_state')
    user_name = str(user_name['name_state'])
    _time = await state.get_data('time_state')
    _time = str(_time['time_state'])

    date = StateMachine.date_state
    # date = str(date['date_state'])
    service_type = StateMachine.service_type_state

    await message.answer(user_name + ' вы записаны на ' + date + ' ' + _time + '\nТип услуги: ' +
                         service_type.format(user_name, date, _time, service_type))
    await message.answer('Если вы решите отменить запись нажмите /cancel')
    booking_db.add_client(message.from_user.id, user_name, date, _time, StateMachine.service_type_state, status=True)
    await state.finish()


# 4. Choose date
@dp.message_handler(state=StateMachine.date_state)
async def choose_date(message: aiogram.types.Message):
    await message.answer('введите дату согласно формату "18/10/2022": ')
    await StateMachine.date_state.set()


# 5. Choose time
@dp.message_handler(state=StateMachine.time_state)
async def choose_time(message: aiogram.types.Message):
    await message.answer('введите время согласно формату "17:30": ')
    await StateMachine.time_state.set()


@dp.message_handler(commands=['booking'])
async def booking(message: aiogram.types.Message):
    await message.answer('введите Ваше Имя: ')
    await StateMachine.name_state.set()


@dp.message_handler(commands=['cancel'])
async def cancel_booking(message: aiogram.types.Message):
    await message.answer('Вы отменили ваше бронивание!')
    booking_db.remove_client(message.from_user.id)


@dp.message_handler(content_types=['text'])
async def bot_message(message: aiogram.types.Message):
    if message.text == messages.contact_with_me:
        await bot.send_message(message.chat.id, messages.my_contacts)
    elif message.text == 'Как добраться 🚴':
        await bot.send_message(message.chat.id, messages.my_address)
        await bot.send_location(message.chat.id, latitude='53.88955103620152', longitude='27.539036100533224')

    elif message.text == 'Запись на стрижку 🖍':
        await bot.send_message(message.chat.id, '🎁Выберете нужную услугу:', reply_markup=markup1)

    elif message.text == my_notes:
        await bot.send_sticker(message.chat.id,
                               sticker=r"CAACAgQAAxkBAAEF8TBjM2fT9Qpj1mzkHeHCDkZ3L-qPqwACkBgAAqbxcR6TtLMvhVvOoSkE",
                               reply_markup=murkup2)

    elif message.text == 'Обо мне 🙎‍♂️':
        file = open('image/photo_2022-09-28 01.24.09.jpeg', 'rb')
        await bot.send_photo(message.chat.id, file, messages.my_portfolio)

    elif message.text == 'Как добраться 🚴':
        await bot.send_message(message.chat.id, messages.my_address)
        await bot.send_location(message.chat.id, latitude='53.88955103620152', longitude='27.539036100533224')


@dp.callback_query_handler()
async def callback(_callback: aiogram.types.CallbackQuery):
    if _callback.message and \
            (_callback.data == 'усы' or _callback.data == 'мужская стрижка' or _callback.data == 'борода' or
             _callback.data == 'дети'):
        StateMachine.service_type_state = _callback.data
        await startCalendar(_callback.message)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
