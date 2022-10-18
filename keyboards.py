from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import  types


my_notes = "Мои записи 📔"

markup = types.ReplyKeyboardMarkup(resize_keyboard= True)
button_1 = types.KeyboardButton('Запись на стрижку 🖍')
button_2 = types.KeyboardButton(my_notes)
button_3 = types.KeyboardButton('Мои работы 💇')
button_4 = types.KeyboardButton('Отзывы клиентов 📔')
button_5 = types.KeyboardButton('Как добраться 🚴')
button_6 = types.KeyboardButton('Обо мне 🙎‍♂️')
button_7 = types.KeyboardButton('Связаться со мной 📞')
markup.add(button_1, button_2, button_3, button_4, button_5, button_6, button_7)


markup1 = types.InlineKeyboardMarkup(row_width=1)
button = types.InlineKeyboardButton('Мужская стрижка', callback_data='мужская стрижка')
button1 = types.InlineKeyboardButton('Мужская стрижка + оформление усов/бороды', callback_data='усы')
button2 = types.InlineKeyboardButton('Стрижка усов/бороды', callback_data='борода')
button3 = types.InlineKeyboardButton('Стрижка детская(до 10 лет)', callback_data='дети')
markup1.add(button, button1, button2, button3)


markup3 = types.InlineKeyboardMarkup(row_width=3)
button = types.InlineKeyboardButton('1', callback_data= '1')
button1 = types.InlineKeyboardButton('2', callback_data='2')
button2 = types.InlineKeyboardButton('3', callback_data='3')
button3 = types.InlineKeyboardButton('4', callback_data='4')
button4 = types.InlineKeyboardButton('5', callback_data= '5')
button5 = types.InlineKeyboardButton('6', callback_data='6')
button6 = types.InlineKeyboardButton('7', callback_data='7')
button7 = types.InlineKeyboardButton('8', callback_data='8')
button8 = types.InlineKeyboardButton('9', callback_data= '9')
button9 = types.InlineKeyboardButton('10', callback_data='10')
button10 = types.InlineKeyboardButton('11', callback_data='11')
button11 = types.InlineKeyboardButton('12', callback_data='12')
button12 = types.InlineKeyboardButton('13', callback_data= '13')
button13 = types.InlineKeyboardButton('14', callback_data='14')
button14 = types.InlineKeyboardButton('15', callback_data='15')
button15 = types.InlineKeyboardButton('16', callback_data='16')
markup3.add(button, button1, button2, button3, button4, button5, button6, button7, button8, button9, button10, button11,
            button12, button13, button14, button15 )


murkup2 = types.InlineKeyboardMarkup(row_width= 1)
button11 = types.InlineKeyboardButton('Мои работы', url='https://www.instagram.com/slava_zhuravsky_')
murkup2.add(button11)