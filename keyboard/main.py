from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
import config as cfg

help_perexod = InlineKeyboardMarkup(row_width=2)
addb = InlineKeyboardButton(
    text='🚶‍♂ Переход в лс', url='https://t.me/RDG_GAME_BOT')
help_perexod.add(addb)    

help_top = InlineKeyboardMarkup(row_width=2)
topb = InlineKeyboardButton(text='💸 Баланс', callback_data='topb')
tope = InlineKeyboardButton(text='💡 Опыт', callback_data='tope')
topg = InlineKeyboardButton(text='🎮 Игры', callback_data='topg')
toppet = InlineKeyboardButton(text='🤼 Бои ', callback_data='toppet')
top_clan=InlineKeyboardButton(text='⚔️Кланы', callback_data='top_clan')
top_city = InlineKeyboardButton(text='🌆 Города', callback_data='top_city')
help_top.add(topb, tope, topg,toppet,top_clan,top_city)

help_topback = InlineKeyboardMarkup(row_width=2)

main1 = InlineKeyboardButton(text='⬅️ Назад', callback_data='backtop')

help_topback.add(main1)

