

from aiogram import types

from aiogram.dispatcher.filters import BoundFilter
#from aiogram.types import  ChatMemberRestricted
from datetime import datetime
from keyboard.main import help_perexod

register_datatime=dict()
import sqlite3
connect = sqlite3.connect("db/redshark.db")
cursor = connect.cursor()
class IsRegister2(BoundFilter):
    async def check(self, message):
        user_id = message.from_user.id
        cursor.execute(f"SELECT user_id FROM users WHERE user_id = {user_id}")
        if cursor.fetchone() is None:
            name1 = message.from_user.get_mention(as_html=True)
            await message.reply(
                f' 👋 Добро пожаловать  {name1}\n🎳 Я - игровой бот RDG!\n\n<b>Чтобы пользоваться командами бота напишите /start в Личные Сообщения бота</b>',
                reply_markup=help_perexod, parse_mode='html')
            return False
        else:
            return True