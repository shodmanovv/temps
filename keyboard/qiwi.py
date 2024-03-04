from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import  types

def buy_menu(isUrl=True,url="",bill=""):
    qiwiMenu=InlineKeyboardMarkup(row_width=1)
    if isUrl:
        btnUrlQIwi=InlineKeyboardButton(text="Ссылка на оплату",url=url)
        qiwiMenu.add(btnUrlQIwi)
    btnCheckQIwi = InlineKeyboardButton(text="Проверить оплату", callback_data='check_' + bill)
    qiwiMenu.add(btnCheckQIwi)
    return qiwiMenu
back = types.ReplyKeyboardMarkup(resize_keyboard=True)
back.add(types.KeyboardButton('Отмена'))

gamestavka = types.InlineKeyboardMarkup(row_width=3)
gamestavka.add(types.InlineKeyboardButton(text="✅ Принять ставку", callback_data='gamestavka2'), types.InlineKeyboardButton(text="❌ Отменить ставку", callback_data='gamestavka1'))

