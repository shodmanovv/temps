from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types

apanel = types.InlineKeyboardMarkup(row_width=2)
apanel.add(types.InlineKeyboardButton(text='📊 Статистика', callback_data='stats'))
apanel.add(types.InlineKeyboardButton(text='💎 Восстановить роль "Владельца"', callback_data='owner'))
apanel.add(types.InlineKeyboardButton(text='👑 Скачать базу данных', callback_data='getdb'))
apanel.add(types.InlineKeyboardButton(text='🧙‍♂ Reset', callback_data='reset'))
apanel.add(types.InlineKeyboardButton(text='👾 Вдзу', callback_data='wdzy'))
apanel.add(types.InlineKeyboardButton(text='📢 Рассылка', callback_data='rass'))

back = types.ReplyKeyboardMarkup(resize_keyboard=True)
back.add(types.KeyboardButton('Отмена'))

cnopka = InlineKeyboardButton(text="🌫 Серебрянная кнопка", callback_data="cnopka")
serebro = InlineKeyboardMarkup()
serebro.row(cnopka)

zolotka = InlineKeyboardButton(text="🌠 Золотая кнопка", callback_data="cnopka")
zolotaya = InlineKeyboardMarkup()
zolotaya.row(zolotka)

rybin = InlineKeyboardButton(text="💎 Рубиновая кнопка", callback_data="cnopka")
rybinovaya = InlineKeyboardMarkup()
rybinovaya.row(rybin)

brillik = InlineKeyboardButton(text="♦️ Кнопка красный рубин", callback_data="cnopka")
red = InlineKeyboardMarkup()
red.row(brillik)

balanc = InlineKeyboardMarkup(row_width=1)
balanc.add(InlineKeyboardButton(text='💰 Баланс', switch_inline_query_current_chat='баланс'))

ustanovka = InlineKeyboardMarkup(row_width=3)
ustanovka1 = InlineKeyboardButton(text='🌅 Установить аватарку', callback_data='ustanovka1')
ustanovka.add(ustanovka1)