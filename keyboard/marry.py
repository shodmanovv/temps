
from aiogram import types
button_marry = types.InlineKeyboardMarkup(row_width=3)
button_marry.add(types.InlineKeyboardButton(text='❤️ Согласиться', callback_data='button_marry_y'), types.InlineKeyboardButton(text='💔 Отказаться', callback_data='button_marry_n'))
button_divorce = types.InlineKeyboardMarkup(row_width=3)
button_divorce.add(types.InlineKeyboardButton(text='💔 Согласиться', callback_data='button_divorce_y'), types.InlineKeyboardButton(text='❤ Отказаться', callback_data='button_divorce_n'))