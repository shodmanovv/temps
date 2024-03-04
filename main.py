# -*-coding: utf-8 -*-
import logging
import sqlite3
import random
import time
import zipfile
import config as cfg
from colorama import Fore, Back, Style, init
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import quote_html
from aiogram.types import ContentTypes
from aiogram.types import ContentType
from datetime import datetime, timedelta
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.exceptions import Throttled
from decimal import Decimal
from bs4 import BeautifulSoup
from handlers.functions import status_users
import requests
import asyncio
import aioschedule
import utils
import openai
import numexpr
from numpy import number
from time import gmtime, strptime, strftime
from filters.admins import IsBot
from filters.register import IsRegister2
from keyboard.qiwi import  buy_menu, gamestavka
from keyboard.marry import button_marry,button_divorce
from keyboard.gey import apanel, back, serebro, zolotaya, rybinovaya, red, balanc, ustanovka
from keyboard.main import help_top, help_topback, help_perexod
from pyqiwip2p import QiwiP2P
from pycoingecko import CoinGeckoAPI
import emoji as emo
import os

logging.basicConfig(level=logging.INFO)

# CoinGeckoAPI
api = CoinGeckoAPI()

# bot init
bot = Bot(token=cfg.BOT_TOKEN)
dp = Dispatcher(bot)

openai.api_key = "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"

# datebase
p2p = QiwiP2P(auth_key=cfg.QIWI_TOKEN)

connect = sqlite3.connect("db/redshark.db")
cursor = connect.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS users(
    user_id BIGINT,
    user_name STRING,
    user_tg_name STRING,
    user_status STRING,
    balance INT,
    bank BIGINT,
    ethereum INT,
    rating INT,
    status_block STRING,
    time_register INT,
    pref STRING,
    donate_coins INT,
    game INT,
    bank2 INT,
    depozit INT,
    stats_status STRING,
    pet1 INT NOT NULL,
    pet2 INT NOT NULL,
    pet3 INT NOT NULL,
    pet4 INT NOT NULL,
    pet5 INT NOT NULL,
    pet6 INT NOT NULL,
    pet7 INT NOT NULL,
    pet8 INT NOT NULL,
    pet9 INT NOT NULL,
    pet_name text NOT NULL,
    pet_hp INT NOT NULL,
    pet_eat INT NOT NULL,
    pet_mood INT NOT NULL,
    checking INT NOT NULL,
    checking1 INT NOT NULL,
    checking2 INT NOT NULL,
    checking3 INT NOT NULL,
    pet10 INT NOT NULL,
    pet11 INT NOT NULL,
    marry INTERGER DEFAULT 0,
    marry_time INTERGER DEFAULT 0,
    marry_date INTERGER DEFAULT 0,
    stavka INT,
    last_work INT,
    stol INT,
    lampa INT,
    subs INT,
    microphone INT,
    heardphone INT,
    clava INT,
    monitor INT,
    covrik INT,
    creslo INT,
    pc INT,
    comnata INT,
    last_video INT,
    checker INT,
    mish INT,
    games INT,
    level INT,
    work INT,
    farm1 INT,
    farm2 INT,
    farm3 INT,
    farm4 INT,
    farm5 INT,
    farm_coin INT,
    generator INT,
    farmcoin1 INT,
    farmcoin2 INT,
    farmcoin3 INT,
    farmcoin4 INT,
    farmcoin5 INT,
    vcard INT,
    bitmaning INT,
    bitcoin INT,
    id INT,
    litecoin INT,
    fantom INT
)
""")

cursor.execute("""CREATE TABLE IF NOT EXISTS mine(
    user_id INT,
    user_name STRING,
    pick STRING,
    iron INT,
    metall INT,
    silver INT,
    bronza INT,
    gold INT
)
""")

cursor.execute("""CREATE TABLE IF NOT EXISTS user_case(
    user_id INT,
    case_money INT,
    case_donate INT
)
""")

cursor.execute("""CREATE TABLE IF NOT EXISTS house(
    user_id INT,
    user_name STRING,
    house INT,
    basement INT
)
""")

cursor.execute("""CREATE TABLE IF NOT EXISTS cars(
    user_id INT,
    user_name STRING,
    cars INT,
    hp INT,
    benz INT
)
""")

cursor.execute("""CREATE TABLE IF NOT EXISTS truck(
    user_id INT,
    user_name STRING,
    truck INT,
    hp INT,
    fuel INT
)
""")

cursor.execute("""CREATE TABLE IF NOT EXISTS promo(
    promo STRING,
    status STRING,
    owner STRING,
    priz BIGINT,
    active INT,
    ob_active INT
)
""")

cursor.execute("""CREATE TABLE IF NOT EXISTS promo_active(
    user_id INT,
    promo STRING,
    active INT
)
""")

cursor.execute("""CREATE TABLE IF NOT EXISTS status_message(
    status TEXT
)
""")

cursor.execute("""CREATE TABLE IF NOT EXISTS tiktok(
    tt_name STRING,
    tt_reg STRING,
    tt_subs INT,
    tt_like INT,
    tt_videos INT, 
    stavka_tt INT,
    stavka_like INT,
    stavka_ad INT,
    user_id INT
)
""") 

cursor.execute("""CREATE TABLE IF NOT EXISTS bot_time(
    user_id INT,
    stavka_games INT,
    stavka_bank INT,
    stavka_bonus INT,
    stavka_depozit INT,
    time_pick INT,
    time_rake INT,
    time_craft INT,
    time_kit INT,
    last_video INT
)
""")

cursor.execute("""CREATE TABLE IF NOT EXISTS time_bank(
    user_id INT,
    stavka INT
)
""")

cursor.execute("""CREATE TABLE IF NOT EXISTS ob_time(
    user_id INT,
    stavka INT
)
""")

cursor.execute("""CREATE TABLE IF NOT EXISTS time_prefix(
    user_id INT,
    stavka INT
)
""")

cursor.execute("""CREATE TABLE IF NOT EXISTS time_sms(
    user_id INT,
    stavka INT
)
""")

cursor.execute("""CREATE TABLE IF NOT EXISTS reffer(
    user_id INT,
    summ INT
)
""")

cursor.execute("""CREATE TABLE IF NOT EXISTS wdzy(
    summ NUMERIC,
    wdz text,
    chat_id NUMERIC,
    count NUMERIC
)
""")

cursor.execute("""CREATE TABLE IF NOT EXISTS chats(
    chat_name text NOT NULL,
    chat_id NUMERIC NOT NULL,
    chat_balance NUMERIC NOT NULL
)
""")

cursor.execute("""CREATE TABLE IF NOT EXISTS fzve(
    user_id NUMERIC ,
    money NUMERIC ,
    bill_id text NOT NULL
)
""")

cursor.execute("""CREATE TABLE IF NOT EXISTS chats(
    chat_id INT,
    chat_name STRING,
    time_register STRING
)
""")

cursor.execute("""CREATE TABLE IF NOT EXISTS clan(
    user_id NUMERIC,
    user_name text,
    status text,
    clan_id NUMERIC,
    clan_name text)
""")

cursor.execute("""CREATE TABLE IF NOT EXISTS clans(
    members NUMERIC,
    clan_id NUMERIC,
    clan_name text,
    kazna NUMERIC,
    type_clan INT,
    new_clan_id NUMERIC,
    power NUMERIC,
    win NUMERIC,
    lose NUMERIC,
    last_stavka NUMERIC NOT NULL
)
""")

cursor.execute("""CREATE TABLE IF NOT EXISTS clans_id(
    new_clan_id NUMERIC,
    type_raz INT,
    type_valut INT,
    summ NUMERIC,
    count NUMERIC,
    event_febiz INT    
)
""")

cursor.execute("""CREATE TABLE IF NOT EXISTS user_family(
     user_name STRING,
     user_id INT,
     family STRING,
     rank INT
)
""")

cursor.execute("""CREATE TABLE IF NOT EXISTS family_id(
     id INT
)
""")

cursor.execute("""CREATE TABLE IF NOT EXISTS family(
     name STRING,
     owner_id INT,
     owner_name STRING,
     id INT,
     balance INT,
     opis STRING,
     time_name INT
)
""")

cursor.execute("""CREATE TABLE IF NOT EXISTS city(
    citizens NUMERIC,
    user_id NUMERIC,
    user_name text,
    kazna NUMERIC,
    city_name text,
    happynes NUMERIC,
    electricity NUMERIC,
    water NUMERIC,
    factory NUMERIC,
    road NUMERIC NOT NULL,
    houses NUMERIC,
    work_place NUMERIC,
    taxes NUMERIC,
    material NUMERIC,
    ore_processing_plant NUMERIC,
    earning NUMERIC
)
""")

cursor.execute("""CREATE TABLE IF NOT EXISTS photo_id(
     user_id INT,
     photo TEXT
)
""")

marry_me = []
marry_rep = []
divorce_me = []
divorce_rep = []
user_me = []
user_rep = []
first_p=[]
second_p=[]
summ_stavka=[]

def add_check(user_id, money, bill_id):
    cursor.execute("INSERT INTO fzve VALUES(?, ? ,?)",
                   (user_id, money, bill_id,))
    connect.commit()


def get_check(bill_id):
    result = cursor.execute("SELECT * FROM fzve WHERE bill_id =?", (bill_id,))
    result = cursor.fetchone()
    if not bool(len(result)):
        return False
    return result[0]
    
async def get_marry(message: types.Message):
    user = message.from_user
    marry = cursor.execute("SELECT marry FROM users WHERE user_id=?", (user.id,)).fetchall()
    return marry

async def get_rang(message: types.Message):
    user = message.from_user
    cursor.execute("SELECT * FROM users WHERE user_id=?", (user.id,))
    data = cursor.fetchone()
    return data

async def reply_get_rang(message: types.Message):
    reply = message.reply_to_message
    replyuser = reply.from_user
    cursor.execute("SELECT * FROM users WHERE user_id=?", (replyuser.id,))
    data = cursor.fetchone()
    return data    

async def get_clan(id):
    cursor.execute("SELECT * FROM clan WHERE user_id=?", (id,))
    data_c = cursor.fetchone()
    return data_c

async def select_photo(user_id):
    local = cursor.execute(f'SELECT photo FROM photo_id WHERE user_id = {user_id}').fetchone()
    local = local[0]
    
    return local

async def register_photo_id(user_id, photo):
	cursor.execute('INSERT INTO photo_id VALUES(?, ?);', (user_id, photo))
	connect.commit()

###########################################СТАРТОВАЯ КОМАНДА###########################################
@dp.message_handler(commands=['Ask', 'ask'], commands_prefix=["/", "!", "."])
async def ii(message: types.Message):
    message.text[5:]
    response = openai.Completion.create( 
     engine="text-davinci-003", 
     prompt='"""\n{}\n"""'.format(message.text), 
     temperature=0, 
     max_tokens=2000,
     top_p=1, 
     frequency_penalty=0, 
     presence_penalty=0, 
     stop=['"""'])
    await message.reply(f"""RDG:
❔ Ваш вопрос: {message.text[5:]}
{response["choices"][0]["text"]}""")

@dp.message_handler(text=['/rules', '/правила', '/Правила'])
async def rules(message):
    await message.answer("https://t.me/end_soft", disable_web_page_preview=True)

@dp.message_handler(lambda message: message.text.lower() == 'игра')
async def process_command_1(message: types.Message):
    
    button1 = InlineKeyboardButton('🗿Камень', callback_data = '1')
    button2 = InlineKeyboardButton('✂️Ножницы', callback_data = '2')
    button3 = InlineKeyboardButton('📄Бумага', callback_data = '3')
    button4 = InlineKeyboardButton('🔨Лом', callback_data='4')
    buttons = InlineKeyboardMarkup().add(button1, button2, button3, button4)
    await bot.send_message(message.chat.id, "Я готов играть!\nВыбери предмет, что бы сыграть со мной🎭", reply_markup= buttons)

@dp.callback_query_handler(lambda c: c.data == '4')
async def process_callback_yes(callback: types.CallbackQuery):
    rand = random.choice(["🗿Камень", "✂️Ножницы", "📄Бумага", "🔨Лом"])

    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    await callback.message.answer("Я выбрал " + rand + "\nА ты выбрал 🔨Лом")
    if rand == '🗿Камень':
        await callback.message.answer("Ты победил🥇")
    elif rand == '✂️Ножницы':
        await callback.message.answer("Ты победил🥇")
    else:
        await callback.message.answer("Ты выиграл🥇")



@dp.callback_query_handler(lambda c: c.data == '3')
async def process_callback_yes(callback: types.CallbackQuery):
    rand = random.choice(["🗿Камень", "✂️Ножницы", "📄Бумага", "🔨Лом"])

    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    await callback.message.answer("Я выбрал " + rand + "\nА ты выбрал 📄Бумага")
    if rand == '🗿Камень':
        await callback.message.answer("Ты победил🥇")
    elif rand == '✂️Ножницы':
        await callback.message.answer("Я победил🥇")
    elif rand == '🔨Лом':
        await callback.message.answer("Я победил🥇")
    else:
        await callback.message.answer("У нас ничья🤝")


@dp.callback_query_handler(lambda c: c.data == '1')
async def process_callback_yes(callback: types.CallbackQuery):
    rand = random.choice(["🗿Камень", "✂️Ножницы", "📄Бумага", "🔨Лом"])

    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    await callback.message.answer("Я выбрал " + rand + "\nА ты выбрал 🗿Камень")
    if rand == '🗿Камень':
        await callback.message.answer("У нас ничья🤝")
    elif rand == '✂️Ножницы':
        await callback.message.answer("Ты выиграл🥇")
    elif rand == '🔨Лом':
        await callback.message.answer("Я выиграл🥇")
    else:
        await callback.message.answer("Я победил🥇")

@dp.callback_query_handler(lambda c: c.data == '2')
async def process_callback_yes(callback: types.CallbackQuery):
    rand = random.choice(["🗿Камень", "✂️Ножницы", "📄Бумага", "🔨Лом"])

    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    await callback.message.answer("Я выбрал " + rand + "\nА ты выбрал ✂️Ножницы")
    if rand == '🗿Камень':
        await callback.message.answer("Я победил🥇")
    elif rand == '✂️Ножницы':
        await callback.message.answer("У нас ничья🤝")
    elif rand == '🔨Лом':
        await callback.message.answer("Я победил🥇")
    else:
        await callback.message.answer("Ты победил🥇")
                     
@dp.message_handler(commands=['ping', 'пинг'], commands_prefix=["/", "!", "."])
async def ping(message: types.Message):
    if message.forward_date != None:
        return
    a = time.time()
    bot_msg = await message.answer(f'⚙ Проверка пинга....')
    if bot_msg:
        b = time.time()
        await bot_msg.edit_text(f'🏓 Пинг: {round((b - a) * 1000)} ms')


@dp.message_handler(commands=['sql'])
async def sql(message: types.Message):

    if message.from_user.id == cfg.owner_id:
        try:
            cursor.execute(message.text[message.text.find(' '):])
            connect.commit()
            a = time.time()
            bot_msg = await message.answer(f'🕘Please wait while me doing SQL request', parse_mode="Markdown")
            if bot_msg:
                b = time.time()
                await bot_msg.edit_text(f"🚀*SQL Запрос был выполнен за {round((b - a) * 1000)} ms*",
                                        parse_mode="Markdown")
        except Exception as e:
            connect.rollback()
            await message.answer(f"❌ Возникла ошибка при изменении\n⚠️ Ошибка: {e}")
    else:
        await message.answer("❌ *Эта команда доступна только создателю бота*",parse_mode="Markdown")


@dp.message_handler(IsBot(),content_types=["new_chat_members"])
async def bot_added_to_chat(message):
    if message.chat.type != 'supergroup':
        await message.answer("""
<b>❌ Ваша группа не является супергруппой❌</b>

Пожалуйста, превратите вашу группу в супергруппу 
(просто запретите кому-то отправлять медиафайлы и заново разрешите) 
и пригласите бота повторно."""
                             , parse_mode='html')
        await bot.leave_chat(message.chat.id)
    else:
        await message.answer("""
<b>Привет!</b>
Я игровой бот 💲
Для того чтобы я мог начать работу, выдай мне пожалуйста права администрации.

Появились предложения или же вопросы?
<a href="https://t.me/end_soft">>Обратись ко мне</a>

<a href="https://t.me/end_soft">>Так же у нас есть общая беседа </a>""", disable_web_page_preview=True, parse_mode='html')

@dp.message_handler(content_types=["new_chat_members"])
async def handler_new_member(message):

    try:
        wdz1=cursor.execute("SELECT wdz FROM wdzy WHERE chat_id=?",(message.chat.id,))
        wdz1=cursor.fetchone()
        wdz1=str(wdz1[0])
    except:
        wdz1="off"
    if wdz1 =="on":
        name1 = message.new_chat_members[0].get_mention(as_html=True)

        user_id = message.new_chat_members[0].id
        user_name = message.new_chat_members[0].full_name

        chat_id = message.chat.id

        user_sd=cursor.execute(f"SELECT user_id FROM users WHERE user_id = {user_id}")
        user_sd=cursor.fetchone()
        user_name = user_name.replace('<', '').replace('>', '')
        if user_sd is None:

            await message.reply(f' 👋Привет {name1}\nЯ бот для игры в различные игры.\nПерейди в лс для получения полного доступа в боте',
                parse_mode="html",reply_markup=help_perexod)
            try:
                user_id1 = message.from_user.id
                user_name1 = message.from_user.first_name

                balance = cursor.execute(
                    "SELECT balance from users where user_id = ?", (message.from_user.id,))
                balance = cursor.fetchone()
                balance = int(balance[0])
                summ = cursor.execute(f"SELECT summ FROM wdzy WHERE chat_id={chat_id}")
                summ = cursor.fetchone()
                summ = int(summ[0])
                count = cursor.execute(f"SELECT count FROM wdzy WHERE chat_id={chat_id}")
                count = cursor.fetchone()
                count = int(count[0])
                summ2 = '{:,}'.format(summ).replace(',', '.')
                cursor.execute(
                    f"UPDATE users SET balance={balance + summ} WHERE user_id = ?", (user_id1,))
                cursor.execute(
                    f"UPDATE wdzy SET count={count + 1} WHERE chat_id = {chat_id}")
                connect.commit()
                await bot.send_message(user_id1,
                                       f"‼️ <a href='tg://user?id={user_id1}'>{user_name1}</a>,Вам была выдана награда в размере {summ2}¢",
                                       parse_mode='html')
            except:
                pass
        if user_sd != None:
            await message.reply(
                f' 👋Привет {name1}\nЯ бот для игры в различные игры.\nПерейди в лс для получения полного доступа в боте',parse_mode="html",reply_markup=help_perexod)
            connect.commit()
            try:
                user_id1 = message.from_user.id
                user_name1 = message.from_user.first_name
                if user_id1 != message.new_chat_members[0].id:
                    await bot.send_message(user_id1,
                                       f"🚫 <a href='tg://user?id={user_id1}'>{user_name1}</a>, Игрок уже есть в базе данных бота ",
                                       parse_mode='html')
            except:
                pass

@dp.message_handler(text=['панель'])
async def adminstration(message: types.Message):
   if message.from_user.id == cfg.owner_id:
     await message.reply('Добро пожаловать в админ панель.', reply_markup=apanel)
   else:
     await message.reply('Вы не являетесь создателем бота!')


@dp.callback_query_handler(lambda c: c.data == "getdb")
async def getdb(callback_query: types.CallbackQuery):
   usid = callback_query.from_user.id
   if usid == cfg.owner_id:
      newzip = zipfile.ZipFile('redshark.zip', 'w')
      newzip.write('db/redshark.db', compress_type=zipfile.ZIP_DEFLATED)
      get_db = open(f'redshark.zip', 'rb')
      await bot.send_document(chat_id=callback_query.message.chat.id, document=get_db, caption=f'<b>🚀 Держи!</b>', parse_mode='html')

@dp.callback_query_handler(lambda c: c.data == "stats")
async def stats(callback_query: types.CallbackQuery):
   usid = callback_query.from_user.id
   chem = "SELECT * from users where user_status='Chem'"
   cursor.execute(chem)
   chem = cursor.fetchall()
   korol = "SELECT * from users where user_status='Korol'"
   cursor.execute(korol)
   korol = cursor.fetchall()
   donater = "SELECT * from users where user_status='Donater'"
   cursor.execute(donater)
   donater = cursor.fetchall()
   vip = "SELECT * from users where user_status='Vip'"
   cursor.execute(vip)
   vip = cursor.fetchall()
   admins = "SELECT * from users where user_status='Admin'"
   cursor.execute(admins)
   admins = cursor.fetchall()
   helper = "SELECT * from users where user_status='Helper_Admin'"
   cursor.execute(helper)
   helper = cursor.fetchall()
   owner = "SELECT * from users where user_status='Owner'"
   cursor.execute(owner)
   owner = cursor.fetchall()
   delux = "SELECT * from users where user_status='Deluxe'"
   cursor.execute(delux)
   delux = cursor.fetchall()
   titan = "SELECT * from users where user_status='Titanium'"
   cursor.execute(titan)
   titan = cursor.fetchall()
   users = """SELECT * from users"""
   cursor.execute(users)
   records = cursor.fetchall()
   chats = """SELECT * from chats"""
   cursor.execute(chats)
   if usid == cfg.owner_id:
      await bot.send_message(callback_query.message.chat.id, f"""
<b>👥 Пользователей в боте:</b> <code>{len(records)}</code>
<b>💬 Чатов в которых есть бот:</b> <code>{len(chats)}</code>
<b>👨‍💻 OWNER:</b> <code>{len(owner)}</code>
<b>⛔️ HELPER:</b> <code>{len(helper)}</code>
<b>⛔️ ADMIN's:</b> <code>{len(admins)}</code>
<b>❤️ VIP пользователей: </b><code>{len(vip)} </code>
<b>👾 TITANIUM пользователей:</b> <code>{len(titan)}</code>
<b>🔥 DELUXE пользователей:</b> <code>{len(delux)}</code>
<b>🏆 ЧЕМПИОН пользователей:</b> <code>{len(chem)}</code>
<b>👑 КОРОЛЬ пользователей:</b> <code>{len(korol)}</code>
<b>😈 ДОНАТЕР пользователей:</b> <code>{len(donater)}</code>""", parse_mode='html')

@dp.callback_query_handler(lambda c: c.data == "owner")
async def owner(callback_query: types.CallbackQuery):
   usid = callback_query.from_user.id
   user_status = "Rab"
   if usid == cfg.owner_id:
      await bot.send_message(callback_query.message.chat.id, f'💎 Вы успешно восстановили роль "Владельца"')
      cursor.execute(f'UPDATE users SET user_status = \"{user_status}\" WHERE user_id = "{usid}"')
      connect.commit()
      
@dp.callback_query_handler(lambda c: c.data == "wdzy")
async def check5rty(callback: types.CallbackQuery):
    usid = callback.from_user.id
    if usid == cfg.owner_id:

        chat_id=callback.message.chat.id
        chat_name = callback.message.chat.title
        try:
            summ = cursor.execute(f"SELECT summ FROM wdzy WHERE chat_id={chat_id}")
            summ = cursor.fetchone()
            summ = int(summ[0])
            count = cursor.execute(f"SELECT count FROM wdzy WHERE chat_id={chat_id}")
            count = cursor.fetchone()
            count = int(count[0])
            summ2 = '{:,}'.format(summ).replace(',', '.')
            count2 = '{:,}'.format(count).replace(',', '.')
            wdz = cursor.execute(f"SELECT wdz FROM wdzy WHERE chat_id={chat_id}")
            wdz = cursor.fetchone()
        except:
            await callback.message.answer("Чат не привязан")
            return
        wdz2=""
        if wdz[0]=="on":
            wdz2="включен"
        if wdz[0]=="off":
            wdz2="выключен"

        await bot.send_message(chat_id=callback.message.chat.id,
                                    text=f"""
 <b>ВДЗУ (Выдача денег за участников)</b>
💭 Чат <b>{chat_name}</b> (<code>{chat_id}</code>)
💰 Сумма за 1 чел : <code>{summ2}</code>
🌝 Статус - {wdz2}
🔢 Всего добавлено - <b>{count2}</b> людей.""" ,parse_mode='html')

@dp.callback_query_handler(lambda c: c.data == "reset")
async def stats(callback_query: types.CallbackQuery):
   usid = callback_query.from_user.id
   if usid == cfg.owner_id:
      await bot.send_message(callback_query.message.chat.id, f'🧙‍♂ Вы успешно проверили обнуление')
      cursor.execute(f'UPDATE users SET balance = {10000}')
      cursor.execute(f'UPDATE users SET user_name = "user_name"')
      cursor.execute(f'UPDATE users SET bank = {1000}')
      cursor.execute(f'UPDATE users SET depozit = {0}')
      cursor.execute(f'UPDATE users SET rating = {0}')
      cursor.execute(f'UPDATE users SET ethereum = {100}')
      cursor.execute(f'UPDATE users SET pet1 = {0}')
      cursor.execute(f'UPDATE users SET pet2 = {0}')
      cursor.execute(f'UPDATE users SET pet3 = {0}')
      cursor.execute(f'UPDATE users SET pet4 = {0}')
      cursor.execute(f'UPDATE users SET pet5 = {0}')
      cursor.execute(f'UPDATE users SET pet6 = {0}')
      cursor.execute(f'UPDATE users SET pet7 = {0}')
      cursor.execute(f'UPDATE users SET pet8 = {0}')
      cursor.execute(f'UPDATE users SET pet9 = {0}')
      cursor.execute(f'UPDATE users SET pet_hp = {0}')
      cursor.execute(f'UPDATE users SET pet_eat = {0}')
      cursor.execute(f'UPDATE users SET pet_mood = {0}')
      cursor.execute(f'UPDATE users SET pet10 = {0}')
      cursor.execute(f'UPDATE users SET pet11 = {0}')
      cursor.execute(f'UPDATE users SET stol = {0}')
      cursor.execute(f'UPDATE users SET lampa = {0}')
      cursor.execute(f'UPDATE users SET subs = {0}')
      cursor.execute(f'UPDATE users SET microphone = {0}')
      cursor.execute(f'UPDATE users SET heardphone = {0}')
      cursor.execute(f'UPDATE users SET clava = {0}')
      cursor.execute(f'UPDATE users SET monitor = {0}')
      cursor.execute(f'UPDATE users SET covrik = {0}')
      cursor.execute(f'UPDATE users SET creslo = {0}')
      cursor.execute(f'UPDATE users SET pc = {0}')
      cursor.execute(f'UPDATE users SET comnata = {0}')
      cursor.execute(f'UPDATE users SET last_video = {0}')
      cursor.execute(f'UPDATE users SET checker = {0}')
      cursor.execute(f'UPDATE users SET mish = {0}')
      cursor.execute(f'UPDATE users SET farm1 = {0}')
      cursor.execute(f'UPDATE users SET farm2 = {0}')
      cursor.execute(f'UPDATE users SET farm3 = {0}')
      cursor.execute(f'UPDATE users SET farm4 = {0}')
      cursor.execute(f'UPDATE users SET farm5 = {0}')
      cursor.execute(f'UPDATE users SET farm_coin = {0}')
      cursor.execute(f'UPDATE users SET generator = {0}')
      cursor.execute(f'UPDATE users SET farmcoin1 = {0}')
      cursor.execute(f'UPDATE users SET farmcoin2 = {0}')
      cursor.execute(f'UPDATE users SET farmcoin3 = {0}')
      cursor.execute(f'UPDATE users SET farmcoin4 = {0}')
      cursor.execute(f'UPDATE users SET farmcoin5 = {0}')
      cursor.execute(f'UPDATE users SET vcard = {0}')
      cursor.execute(f'UPDATE users SET bitmaning = {0}')
      cursor.execute(f'UPDATE users SET bitcoin = {100}')
      cursor.execute(f'UPDATE users SET litecoin = {100}')
      cursor.execute(f'UPDATE users SET fantom = {100}')
      cursor.execute(f'UPDATE mine SET iron = {0}')
      cursor.execute(f'UPDATE mine SET metall = {0}')
      cursor.execute(f'UPDATE mine SET silver = {0}')
      cursor.execute(f'UPDATE mine SET bronza = {0}')
      cursor.execute(f'UPDATE mine SET gold = {0}')
      cursor.execute(f'UPDATE house SET house = {0}')
      cursor.execute(f'UPDATE house SET basement = {0}')
      cursor.execute(f'UPDATE cars SET cars = {0}')
      cursor.execute(f'UPDATE cars SET hp = {0}')
      cursor.execute(f'UPDATE cars SET benz = {0}')
      cursor.execute(f'UPDATE truck SET truck = {0}')
      cursor.execute(f'UPDATE truck SET hp = {0}')
      cursor.execute(f'UPDATE truck SET fuel = {0}')       
      cursor.execute(f'UPDATE bot_time SET stavka_games = {0} ')
      cursor.execute(f'UPDATE bot_time SET stavka_bank = {0} ')
      cursor.execute(f'UPDATE bot_time SET stavka_bonus = {0} ')
      cursor.execute(f'UPDATE bot_time SET stavka_depozit = {0} ')
      cursor.execute(f'UPDATE bot_time SET time_pick = {0} ')
      cursor.execute(f'UPDATE bot_time SET time_rake = {0} ')
      cursor.execute(f'UPDATE bot_time SET time_craft = {0} ')
      cursor.execute(f'UPDATE bot_time SET time_kit = {0} ')
      cursor.execute(f'UPDATE bot_time SET last_video = {0} ')
      cursor.execute(f'UPDATE clans SET kazna = {0}')
      cursor.execute(f'UPDATE clans SET power = {0}')
      cursor.execute(f'UPDATE clans SET win = {0}')
      cursor.execute(f'UPDATE clans SET lose = {0}')
      cursor.execute(f'UPDATE wdzy SET summ = {1000000}')
      connect.commit()

###############################################РЕПОРТ############################################
@dp.message_handler(commands=['жалоба'], commands_prefix=["/", "!", "."])
async def report(message):
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    user_id = message.from_user.id

    user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()
    user_status = str(user_status[0])
    text = message.text[7:]
    
    if text == '':
       await bot.send_message(message.chat.id, f"💫 | <a href='tg://user?id={user_id}'>{user_name}</a>, жалоба не может быть пустым", parse_mode='html')
       return
    if not text == '':
        await bot.send_message(message.chat.id, f"✅ | <a href='tg://user?id={user_id}'>{user_name}</a>, ваша жалоба был успешно отправлен разработчику", parse_mode='html')
        connect.commit()
        
    if user_status == 'Rab':
       await bot.send_message(5978300530, f"<b>💫ВАМ ПРИШЁЛ ЖАЛОБА💫</b>\n👨 | Отправитель: <a href='tg://user?id={user_id}'>{user_name}</a>\n💬 |Сообщение: <i>{text}</i>", parse_mode='html')

    await bot.send_message(5978300530,f"""
<b>💫ВАМ ПРИШЁЛ ЖАЛОБА💫</b>
👨 | Отправитель: <a href='tg://user?id={user_id}'>{user_name}</a>  
💬 |Сообщение: <i>{text}</i>
    """, parse_mode='html')


@dp.message_handler(commands=['казино'])
async def kazino(message):
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    
    await bot.send_message(message.chat.id, f"""
🏁 Для начала игры в казино, вы должны найти себе соперника и предложить ему ставку командой «Казино (сумма)». (Ответом на сообщение)

🖱 После нажатия кнопки «🎲 Принять ставку от Игрока», у каждого из вас появиться рандомное число которое будет выглядить так «Игрок(1)».

🏆 У кого это число будет больше тот и победил. Победителю переводиться сумма ставки на которую вы играли, а у проигравшего она забирается""", parse_mode='html')


###############################################MMMMM############################################
@dp.message_handler(commands=['m'])
async def start_cmd(message):
   try:
      text = ' '.join(message.text.split()[2:])

      msg = message
      user_id = msg.from_user.id
      user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
      user_name = str(user_name[0])

      reply_user_id = int(message.text.split()[1])
      reply_user_name = cursor.execute(f"SELECT user_name from users where user_id = {reply_user_id}").fetchone()
      reply_user_name = str(reply_user_name[0])

      period = 5
      get = cursor.execute("SELECT stavka FROM time_sms WHERE user_id = ?", (message.from_user.id,)).fetchone()
      last_stavka = f"{int(get[0])}"
      stavkatime = time.time() - float(last_stavka)

      if len(text) > 305:
         await bot.send_message(message.chat.id, f"💫 | <a href='tg://user?id={user_id}'>{user_name}</a>, сообщение не может быть более чем 305 символов ", parse_mode='html')
         return
      if stavkatime > period:
         await bot.send_message(user_id, f"💬 | [Я ➡️ <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>] {text}", parse_mode='html')
         await bot.send_message(reply_user_id, f"💬 | [<a href='tg://user?id={user_id}'>{user_name}</a> ➡️ Я] {text}", parse_mode='html')
         cursor.execute(f'UPDATE time_sms SET stavka = {time.time()} WHERE user_id = {user_id}')
         connect.commit()
         return
      else:
         await bot.send_message(user_id, f"💫 | Игрок, сообщение писать можно раз в 5 секунд", parse_mode='html')
         return
   except:
      await bot.send_message(message.chat.id, f"💫 | <a href='tg://user?id={user_id}'>{user_name}</a>, ошибка! Либо вы не правильно ID, или данный игрок не играет в бота", parse_mode='html')


###############################################ЮТУБ############################################
@dp.message_handler(text=['Купить освещение', 'купить освещение'])
async def teth(message):
 user_id = message.from_user.id
 user_name = cursor.execute("SELECT user_name from users WHERE user_id = ?", (message.from_user.id,)).fetchone()
 user_name = str(user_name[0])

 balance = cursor.execute("SELECT balance from users WHERE user_id = ?", (message.from_user.id,)).fetchone()
 balance = int(balance[0])
 
 checker = cursor.execute("SELECT checker from users where user_id = ?", (message.from_user.id,)).fetchone()
 checker = int(checker[0])
 
 lampa = cursor.execute("SELECT lampa from users WHERE user_id = ?", (message.from_user.id,)).fetchone()
 lampa = int(lampa[0])
 
 comnata = cursor.execute("SELECT comnata from users WHERE user_id = ?", (message.from_user.id,)).fetchone()
 comnata = int(comnata[0])
 if comnata >= 1:
  cursor.execute(f'UPDATE users SET balance = {balance - 25000000}  WHERE user_id = {user_id}')
  cursor.execute(f'UPDATE users SET lampa = {1}  WHERE user_id = {user_id}')
  cursor.execute(f'UPDATE users SET checker = {checker + 1}  WHERE user_id = {user_id}')
  await message.reply(f'💡 {user_name}, вы успешно купили освещение', parse_mode='html')


@dp.message_handler(text=['Купить стол', 'купить стол'])
async def teth(message):
 user_id = message.from_user.id
 user_name = cursor.execute("SELECT user_name from users WHERE user_id = ?", (message.from_user.id,)).fetchone()
 user_name = str(user_name[0])

 balance = cursor.execute("SELECT balance from users WHERE user_id = ?", (message.from_user.id,)).fetchone()
 balance = int(balance[0])
 
 stol = cursor.execute("SELECT lampa from users WHERE user_id = ?", (message.from_user.id,)).fetchone()
 stol = int(stol[0])
 
 checker = cursor.execute("SELECT checker from users where user_id = ?", (message.from_user.id,)).fetchone()
 checker = int(checker[0])

 comnata = cursor.execute("SELECT comnata from users WHERE user_id = ?", (message.from_user.id,)).fetchone()
 comnata = int(comnata[0])
 if comnata >= 1:
  cursor.execute(f'UPDATE users SET balance = {balance - 25000000}  WHERE user_id = {user_id}')
  cursor.execute(f'UPDATE users SET stol = {1}  WHERE user_id = {user_id}')
  cursor.execute(f'UPDATE users SET checker = {checker + 1}  WHERE user_id = {user_id}')
  await message.reply(f'👨‍💻 {user_name}, вы успешно купили стол', parse_mode='html')

@dp.message_handler(text=['Купить монитор', 'купить монитор'])
async def teth(message):
 user_id = message.from_user.id
 user_name = cursor.execute("SELECT user_name from users WHERE user_id = ?", (message.from_user.id,)).fetchone()
 user_name = str(user_name[0])

 balance = cursor.execute("SELECT balance from users WHERE user_id = ?", (message.from_user.id,)).fetchone()
 balance = int(balance[0])
 
 monitor = cursor.execute("SELECT monitor from users WHERE user_id = ?", (message.from_user.id,)).fetchone()
 monitor = int(monitor[0])
 
 checker = cursor.execute("SELECT checker from users where user_id = ?", (message.from_user.id,)).fetchone()
 checker = int(checker[0])
 
 comnata = cursor.execute("SELECT comnata from users WHERE user_id = ?", (message.from_user.id,)).fetchone()
 comnata = int(comnata[0])
 if comnata >= 1:
  cursor.execute(f'UPDATE users SET balance = {balance - 25000000}  WHERE user_id = {user_id}')
  cursor.execute(f'UPDATE users SET monitor = {1}  WHERE user_id = {user_id}')
  cursor.execute(f'UPDATE users SET checker = {checker + 1}  WHERE user_id = {user_id}')
  await message.reply(f'🖥 {user_name}, вы успешно купили монитор', parse_mode='html')

@dp.message_handler(text=['Купить компьютер', 'купить компьютер'])
async def teth(message):
 user_id = message.from_user.id
 user_name = cursor.execute("SELECT user_name from users WHERE user_id = ?", (message.from_user.id,)).fetchone()
 user_name = str(user_name[0])

 balance = cursor.execute("SELECT balance from users WHERE user_id = ?", (message.from_user.id,)).fetchone()
 balance = int(balance[0])
 
 pc = cursor.execute("SELECT pc from users WHERE user_id = ?", (message.from_user.id,)).fetchone()
 pc = int(pc[0])
 
 checker = cursor.execute("SELECT checker from users where user_id = ?", (message.from_user.id,)).fetchone()
 checker = int(checker[0])

 comnata = cursor.execute("SELECT comnata from users WHERE user_id = ?", (message.from_user.id,)).fetchone()
 comnata = int(comnata[0])
 if comnata >= 1:
  cursor.execute(f'UPDATE users SET balance = {balance - 25000000}  WHERE user_id = {user_id}')
  cursor.execute(f'UPDATE users SET pc = {1}  WHERE user_id = {user_id}')
  cursor.execute(f'UPDATE users SET checker = {checker + 1}  WHERE user_id = {user_id}')
  await message.reply(f'💻 {user_name}, вы успешно купили компьютер', parse_mode='html')

@dp.message_handler(text=['Купить клавиатуру', 'купить клавиатуру'])
async def teth(message):
 user_id = message.from_user.id
 user_name = cursor.execute("SELECT user_name from users WHERE user_id = ?", (message.from_user.id,)).fetchone()
 user_name = str(user_name[0])

 balance = cursor.execute("SELECT balance from users WHERE user_id = ?", (message.from_user.id,)).fetchone()
 balance = int(balance[0])
 checker = cursor.execute("SELECT checker from users where user_id = ?", (message.from_user.id,)).fetchone()
 checker = int(checker[0])

 clava = cursor.execute("SELECT clava from users WHERE user_id = ?", (message.from_user.id,)).fetchone()
 clava = int(clava[0])
 
 comnata = cursor.execute("SELECT comnata from users WHERE user_id = ?", (message.from_user.id,)).fetchone()
 comnata = int(comnata[0])
 if comnata >= 1:
  cursor.execute(f'UPDATE users SET balance = {balance - 25000000}  WHERE user_id = {user_id}')
  cursor.execute(f'UPDATE users SET clava = {1}  WHERE user_id = {user_id}')
  cursor.execute(f'UPDATE users SET checker = {checker + 1}  WHERE user_id = {user_id}')
  await message.reply(f'⌨ {user_name}, вы успешно купили клавиатуру', parse_mode='html')

@dp.message_handler(text=['Купить игровое кресло', 'купить игровое кресло'])
async def teth(message):
 user_id = message.from_user.id
 user_name = cursor.execute("SELECT user_name from users WHERE user_id = ?", (message.from_user.id,)).fetchone()
 user_name = str(user_name[0])

 balance = cursor.execute("SELECT balance from users WHERE user_id = ?", (message.from_user.id,)).fetchone()
 balance = int(balance[0])
 
 checker = cursor.execute("SELECT checker from users where user_id = ?", (message.from_user.id,)).fetchone()
 checker = int(checker[0])
 
 creslo = cursor.execute("SELECT creslo from users WHERE user_id = ?", (message.from_user.id,)).fetchone()
 creslo = int(creslo[0])
 
 comnata = cursor.execute("SELECT comnata from users WHERE user_id = ?", (message.from_user.id,)).fetchone()
 comnata = int(comnata[0])
 if comnata >= 1:
  cursor.execute(f'UPDATE users SET balance = {balance - 25000000}  WHERE user_id = {user_id}')
  cursor.execute(f'UPDATE users SET creslo = {1}  WHERE user_id = {user_id}')
  cursor.execute(f'UPDATE users SET checker = {checker + 1}  WHERE user_id = {user_id}')
  await message.reply(f'💺 {user_name}, вы успешно купили иговое кресло', parse_mode='html')

@dp.message_handler(text=['Купить мышь', 'купить мышь'])
async def teth(message):
 user_id = message.from_user.id
 user_name = cursor.execute("SELECT user_name from users WHERE user_id = ?", (message.from_user.id,)).fetchone()
 user_name = str(user_name[0])

 balance = cursor.execute("SELECT balance from users WHERE user_id = ?", (message.from_user.id,)).fetchone()
 balance = int(balance[0])
 
 checker = cursor.execute("SELECT checker from users where user_id = ?", (message.from_user.id,)).fetchone()
 checker = int(checker[0])
 
 mish = cursor.execute("SELECT mish from users WHERE user_id = ?", (message.from_user.id,)).fetchone()
 mish = int(mish[0])
 
 comnata = cursor.execute("SELECT comnata from users WHERE user_id = ?", (message.from_user.id,)).fetchone()
 comnata = int(comnata[0])
 if comnata >= 1:
  cursor.execute(f'UPDATE users SET balance = {balance - 25000000}  WHERE user_id = {user_id}')
  cursor.execute(f'UPDATE users SET mish = {1}  WHERE user_id = {user_id}')
  cursor.execute(f'UPDATE users SET checker = {checker + 1}  WHERE user_id = {user_id}')
  await message.reply(f'🖱 {user_name}, вы успешно купили мышь', parse_mode='html')

@dp.message_handler(text=['Купить микрофон', 'купить микрофон'])
async def teth(message):
 user_id = message.from_user.id
 user_name = cursor.execute("SELECT user_name from users WHERE user_id = ?", (message.from_user.id,)).fetchone()
 user_name = str(user_name[0])

 balance = cursor.execute("SELECT balance from users WHERE user_id = ?", (message.from_user.id,)).fetchone()
 balance = int(balance[0])
 
 microphone = cursor.execute("SELECT microphone from users WHERE user_id = ?", (message.from_user.id,)).fetchone()
 microphone = int(microphone[0])
 
 checker = cursor.execute("SELECT checker from users where user_id = ?", (message.from_user.id,)).fetchone()
 checker = int(checker[0])

 comnata = cursor.execute("SELECT comnata from users WHERE user_id = ?", (message.from_user.id,)).fetchone()
 comnata = int(comnata[0])
 if comnata >= 1:
  cursor.execute(f'UPDATE users SET balance = {balance - 25000000}  WHERE user_id = {user_id}')
  cursor.execute(f'UPDATE users SET microphone = {1}  WHERE user_id = {user_id}')
  cursor.execute(f'UPDATE users SET checker = {checker + 1}  WHERE user_id = {user_id}')
  await message.reply(f'🎙 {user_name}, вы успешно купили микрофон', parse_mode='html')

@dp.message_handler(text=['Купить наушники', 'купить наушники'])
async def teth(message):
 user_id = message.from_user.id
 user_name = cursor.execute("SELECT user_name from users WHERE user_id = ?", (message.from_user.id,)).fetchone()
 user_name = str(user_name[0])

 balance = cursor.execute("SELECT balance from users WHERE user_id = ?", (message.from_user.id,)).fetchone()
 balance = int(balance[0])
 
 checker = cursor.execute("SELECT checker from users where user_id = ?", (message.from_user.id,)).fetchone()
 checker = int(checker[0])
 
 heardphone = cursor.execute("SELECT mish from users WHERE user_id = ?", (message.from_user.id,)).fetchone()
 heardphone = int(heardphone[0])
 
 comnata = cursor.execute("SELECT comnata from users WHERE user_id = ?", (message.from_user.id,)).fetchone()
 comnata = int(comnata[0])
 if comnata >= 1:
  cursor.execute(f'UPDATE users SET balance = {balance - 25000000}  WHERE user_id = {user_id}')
  cursor.execute(f'UPDATE users SET heardphone = {1}  WHERE user_id = {user_id}')
  cursor.execute(f'UPDATE users SET checker = {checker + 1}  WHERE user_id = {user_id}')
  await message.reply(f'🎧 {user_name}, вы успешно купили наушники', parse_mode='html')

@dp.message_handler(text=['Купить коврик', 'купить коврик'])
async def teth(message):
 user_id = message.from_user.id
 user_name = cursor.execute("SELECT user_name from users WHERE user_id = ?", (message.from_user.id,)).fetchone()
 user_name = str(user_name[0])

 balance = cursor.execute("SELECT balance from users WHERE user_id = ?", (message.from_user.id,)).fetchone()
 balance = int(balance[0])
 
 covrik = cursor.execute("SELECT covrik from users WHERE user_id = ?", (message.from_user.id,)).fetchone()
 covrik = int(covrik[0])
 
 checker = cursor.execute("SELECT checker from users where user_id = ?", (message.from_user.id,)).fetchone()
 checker = int(checker[0])
 
 comnata = cursor.execute("SELECT comnata from users WHERE user_id = ?", (message.from_user.id,)).fetchone()
 comnata = int(comnata[0])
 if comnata >= 1:
  cursor.execute(f'UPDATE users SET balance = {balance - 25000000}  WHERE user_id = {user_id}')
  cursor.execute(f'UPDATE users SET covrik = {1}  WHERE user_id = {user_id}')
  cursor.execute(f'UPDATE users SET checker = {checker + 1}  WHERE user_id = {user_id}')
  await message.reply(f'🎇 {user_name}, вы успешно купили коврик', parse_mode='html')

@dp.message_handler(text=["Мой канал", "мой канал", "канал", "Канал"])
async def teth(message):
 user_id = message.from_user.id
 subs = cursor.execute("SELECT subs from users WHERE user_id = ?", (message.from_user.id,)).fetchone()
 comnata = cursor.execute("SELECT comnata from users WHERE user_id = ?", (message.from_user.id,)).fetchone()
 user_name = cursor.execute("SELECT user_name from users WHERE user_id = ?", (message.from_user.id,)).fetchone()
 lampa = cursor.execute("SELECT lampa from users WHERE user_id = ?", (message.from_user.id,)).fetchone()
 stol = cursor.execute("SELECT stol from users WHERE user_id = ?", (message.from_user.id,)).fetchone()
 monitor = cursor.execute("SELECT monitor from users WHERE user_id = ?", (message.from_user.id,)).fetchone()
 pc = cursor.execute("SELECT pc from users WHERE user_id = ?", (message.from_user.id,)).fetchone()
 clava = cursor.execute("SELECT clava from users WHERE user_id = ?", (message.from_user.id,)).fetchone()
 creslo = cursor.execute("SELECT creslo from users WHERE user_id = ?", (message.from_user.id,)).fetchone()
 mish = cursor.execute("SELECT mish from users WHERE user_id = ?", (message.from_user.id,)).fetchone()
 microphone = cursor.execute("SELECT microphone from users WHERE user_id = ?", (message.from_user.id,)).fetchone()
 heardphone = cursor.execute("SELECT heardphone from users WHERE user_id = ?", (message.from_user.id,)).fetchone()
 covrik = cursor.execute("SELECT covrik from users WHERE user_id = ?", (message.from_user.id,)).fetchone()
 checker = cursor.execute("SELECT checker from users WHERE user_id = ?", (message.from_user.id,)).fetchone()
 user_name = str(user_name[0])
 subs = int(subs[0])
 comnata = int(comnata[0])
 lampa = int(lampa[0])
 stol = int(stol[0])
 monitor = int(monitor[0])
 pc = int(pc[0])
 clava = int(clava[0])
 creslo = int(creslo[0])
 mish = int(mish[0])
 microphone = int(microphone[0])
 heardphone = int(heardphone[0])
 covrik = int(covrik[0])
 checker = int(checker[0])
 subs2 = '{:,}'.format(subs).replace(',', '.') 
 if subs > 99999999:
  await message.reply(f'''{user_name}, ваша студия:

✅ Все предметы приобретены

➕ {subs2} подписчиков

ℹ <b>Снимать видео вы сможете только тогда, когда у вас будет всё куплено</b>''', parse_mode='html', reply_markup=red)
  return
  
 if subs > 49999999:
  await message.reply(f'''{user_name}, ваша студия:

✅ Все предметы приобретены

➕ {subs2} подписчиков

ℹ <b>Снимать видео вы сможете только тогда, когда у вас будет всё куплено</b>''', parse_mode='html', reply_markup=rybinovaya)
  return
  
 if subs > 999999:
  await message.reply(f'''{user_name}, ваша студия:

✅ Все предметы приобретены

➕ {subs2} подписчиков

ℹ <b>Снимать видео вы сможете только тогда, когда у вас будет всё куплено</b>''', parse_mode='html', reply_markup=zolotaya)
  return
 
 if subs > 99999:
  await message.reply(f'''{user_name}, ваша студия:

✅ Все предметы приобретены

➕ {subs2} подписчиков

ℹ <b>Снимать видео вы сможете только тогда, когда у вас будет всё куплено</b>''', parse_mode='html', reply_markup=serebro)
  return
  
 if checker > 9:
  await message.reply(f'''{user_name}, ваша студия:

✅ Все предметы приобретены

➕ {subs2} подписчиков

ℹ <b>Снимать видео вы сможете только тогда, когда у вас будет всё куплено</b>''', parse_mode='html')
  return
  
 if comnata < 1:
  await message.reply(f'''{user_name}, у вас нет студии 😖
Что бы ее построить, напишите команду <code>Построить студию</code>''', parse_mode='html')
  return
  
 if comnata < 2:
  await message.reply(f'''{user_name}, ваша студия: 
💡 Освещение: {lampa}/1
👨‍💻 Стол: {stol}/1
🖥 Монитор: {monitor}/1
💻 Компьютер: {pc}/1
⌨ Клавиатура: {clava}/1
💺 Игровое кресло: {creslo}/1
🖱 Мышь: {mish}/1
🎙 Микрофон: {microphone}/1
🎧 Наушники: {heardphone}/1
🎇 Коврик: {covrik}/1

ℹ <b>Снимать видео вы сможете только тогда, когда у вас будет всё куплено</b>''', parse_mode='html')
  return




@dp.message_handler(text=['Создать канал', 'создать канал'])
async def teth(message):
 user_id = message.from_user.id
 user_name = cursor.execute("SELECT user_name from users WHERE user_id = ?", (message.from_user.id,)).fetchone()
 user_name = str(user_name[0])
 await message.reply(f"{user_name}, Вы успешно построили канал, вам осталось купить предметы необходимые для создания контента! 🥳", parse_mode='html')
 cursor.execute(f'UPDATE users SET comnata = {1}  WHERE user_id = "{user_id}"')
 connect.commit()

@dp.message_handler(text=["Снять видео", "снять видео"])
async def teht(message):
        msg = message
        user_id = msg.from_user.id
        chat_id = message.chat.id

        win = ['🙂', '😋', '😄', '😃']
        loser = ['😔', '😕', '😣', '😞', '😢']
        rwin = random.choice(win)
        rloser = random.choice(loser)
        rx = random.randint(0, 50)
        rx2 = '{:,}'.format(rx)
        msg = message
        name1 = message.from_user.get_mention(as_html=True)
        name = msg.from_user.last_name
        user_name = cursor.execute("SELECT user_name from users where user_id = ?", (message.from_user.id,)).fetchone()
        name1 = str(user_name[0])
        balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
        balance = int(balance[0])
        subs = cursor.execute("SELECT subs from users where user_id = ?", (message.from_user.id,)).fetchone()
        subs = int(subs[0])
        pc = cursor.execute("SELECT pc from users where user_id = ?", (message.from_user.id,)).fetchone()
        pc = int(pc[0])
        checker = cursor.execute("SELECT checker from users where user_id = ?", (message.from_user.id,)).fetchone()
        checker = int(checker[0])
        period = 900
        get = cursor.execute("SELECT last_video FROM times WHERE user_id = ?", (message.from_user.id,)).fetchone()
        last_video = f"{int(get[0])}"
        stavkatime = time.time() - float(last_video)
        profit1 = '{0:,}'.format(subs * 2500).replace(',', '.')
        if stavkatime > period:
            if checker == 10:
                await bot.send_message(chat_id,
                                       f'''📼 {name1}, вы успешно сняли видеоролик
ℹ Вы получили: {profit1}¢
➕ На вас подписалось: {rx2} человек''',
                                       parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + subs * 2500} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE users SET subs = {subs + rx} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE times SET last_video=? WHERE user_id=?', (time.time(), user_id,))
                connect.commit()
                return
            else:
             await bot.send_message(message.chat.id, f'ℹ️ {name1}, у вас нет студии или же нет всех необходимых предметов для сьёмки видео {rloser}')
        if stavkatime < period:
            await bot.send_message(chat_id,
                                   f'ℹ️ {name1}, снимать видео возможно только раз в 1⃣5⃣ минут [⏳] {rloser}',
                                   parse_mode='html')

@dp.message_handler(text=['Купить все', 'купить все'])
async def teth(message):
 user_id = message.from_user.id
 user_name = cursor.execute("SELECT user_name from users WHERE user_id = ?", (message.from_user.id,)).fetchone()
 user_name = str(user_name[0])

 balance = cursor.execute("SELECT balance from users WHERE user_id = ?", (message.from_user.id,)).fetchone()
 balance = int(balance[0])

 checker = cursor.execute("SELECT checker from users where user_id = ?", (message.from_user.id,)).fetchone()
 checker = int(checker[0])
 
 lampa = cursor.execute("SELECT lampa from users WHERE user_id = ?", (message.from_user.id,)).fetchone()
 lampa = int(lampa[0])
 stol = cursor.execute("SELECT lampa from users WHERE user_id = ?", (message.from_user.id,)).fetchone()
 stol = int(stol[0])
 monitor = cursor.execute("SELECT monitor from users WHERE user_id = ?", (message.from_user.id,)).fetchone()
 monitor = int(monitor[0])
 pc = cursor.execute("SELECT pc from users WHERE user_id = ?", (message.from_user.id,)).fetchone()
 pc = int(pc[0])
 clava = cursor.execute("SELECT clava from users WHERE user_id = ?", (message.from_user.id,)).fetchone()
 clava = int(clava[0])
 creslo = cursor.execute("SELECT creslo from users WHERE user_id = ?", (message.from_user.id,)).fetchone()
 creslo = int(creslo[0])
 mish = cursor.execute("SELECT mish from users WHERE user_id = ?", (message.from_user.id,)).fetchone()
 mish = int(mish[0])
 microphone = cursor.execute("SELECT microphone from users WHERE user_id = ?", (message.from_user.id,)).fetchone()
 microphone = int(microphone[0])
 heardphone = cursor.execute("SELECT mish from users WHERE user_id = ?", (message.from_user.id,)).fetchone()
 heardphone = int(heardphone[0])
 covrik = cursor.execute("SELECT covrik from users WHERE user_id = ?", (message.from_user.id,)).fetchone()
 covrik = int(covrik[0])

 comnata = cursor.execute("SELECT comnata from users WHERE user_id = ?", (message.from_user.id,)).fetchone()
 comnata = int(comnata[0])
 if comnata >= 1:
  cursor.execute(f'UPDATE users SET balance = {balance - 25000000}  WHERE user_id = {user_id}')
  cursor.execute(f'UPDATE users SET lampa = {1}  WHERE user_id = {user_id}')
  cursor.execute(f'UPDATE users SET stol = {1}  WHERE user_id = {user_id}')
  cursor.execute(f'UPDATE users SET monitor = {1}  WHERE user_id = {user_id}')
  cursor.execute(f'UPDATE users SET pc = {1}  WHERE user_id = {user_id}')
  cursor.execute(f'UPDATE users SET clava = {1}  WHERE user_id = {user_id}')
  cursor.execute(f'UPDATE users SET creslo = {1}  WHERE user_id = {user_id}')
  cursor.execute(f'UPDATE users SET mish = {1}  WHERE user_id = {user_id}')
  cursor.execute(f'UPDATE users SET microphone = {1}  WHERE user_id = {user_id}')
  cursor.execute(f'UPDATE users SET heardphone = {1}  WHERE user_id = {user_id}')
  cursor.execute(f'UPDATE users SET covrik = {1}  WHERE user_id = {user_id}')
  cursor.execute(f'UPDATE users SET checker = {checker + 10}  WHERE user_id = {user_id}')
  await message.reply(f'🎇 {user_name}, вы успешно купили все предметы', parse_mode='html')
  connect.commit()
 

###############################################КК############################################   
@dp.message_handler(commands=['кк'], commands_prefix=["/", "!", "."])
async def disconect_database(message: types.Message):
    if not message.reply_to_message:
       await message.bot.send_message(message.chat.id , f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, эта команда должна быть ответом на сообщение", parse_mode='html')
       return
       

    status_block = cursor.execute("SELECT status_block from users where user_id = ?",(message.from_user.id,)).fetchone()
    status_block = str(status_block[0])

    if status_block == 'on':
       return

    user_id = message.from_user.id
    reply_user_id = message.reply_to_message.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    i = f'''
🗄 Вы удалили <b>{user_name}</b> с базы данных 
   '''

    i2 = f'''
❗️ Данная команда доступно для создателя
   '''

    text = [i, i2]
    if user_id == cfg.owner_id:
        await message.reply(text[0], parse_mode='html')
        cursor.execute(f'DELETE from users where user_id = {reply_user_id}')
        cursor.execute(f'DELETE from user_case where user_id = {reply_user_id}')
        cursor.execute(f'DELETE from bot_time where user_id = {reply_user_id}')
        cursor.execute(f'DELETE from time_bank where user_id = {reply_user_id}')
        cursor.execute(f'DELETE from ob_time where user_id = {reply_user_id}')
        cursor.execute(f'DELETE from time_prefix where user_id = {reply_user_id}')
        cursor.execute(f'DELETE from time_sms where user_id = {reply_user_id}')
        connect.commit()
    else:  
        await message.reply(text[1], parse_mode='html')


###############################################СТАРТ############################################
@dp.message_handler(commands=['start'])
async def start_cmd(message):
    help3 = InlineKeyboardMarkup(row_width=2)
    register_help = InlineKeyboardButton(text='Помощь', callback_data='register_help')
    help3.add(register_help)
    await bot.send_sticker(chat_id=message.chat.id, sticker="CAACAgIAAxkBAAEIdZxkLGpI6HeD8IB0mByhB_dhyUgbbgACJRQAAr7cMUtjrZOh1mLZ_S8E")    
        
    name = message.from_user.get_mention(as_html=True)
    i = f'''
👋 Привет <b>{name}</b>, я игровой бот « RDG »
💸 Тебе как новому пользователю был выдан подарок в размере 100.000¢
🔥 Для ознакомление с моими командами, введи команду <code>Помощь</code> , или вибери кнопку <b>ниже</b>
➕ Так же ты можешь добавить бота в свой чат по кнопке <b>ниже</b>
    '''
    i2 = f'''
❗️ <b>{name}</b>, вы уже зарегистрированы в боте
❕ Если у вас возникла какая то проблема с какой то командой, обратитесь к {cfg.owner} для повторной регистрации <b>[Если у вас SPAM BAN, то вы можете обратиться к нему через данного бота с помощью команд /m [ID] [message] или через команду /report ]</b>
    '''

    text_register = [i, i2]
    msg = message
    user_id = msg.from_user.id
    full_name = msg.from_user.full_name
    user_name = 'НоуНейм'
    user_status = "Player"
    status_block = 'off'
    stats_status = 'off'
    pref = 'Игрок'
    pet_name = "name"
    tt_name = 'none'
    tt_reg = 'off'
    list1 = cursor.execute(f"SELECT * FROM users ORDER BY id DESC")
    uid = 1
    for user in list1:
        uid += 1    
    chat_id = message.chat.id
    result = time.localtime()

    if int(result.tm_mon) <= 9:
      p = "0"
    else:
      p = ''
    times = f'{result.tm_mday}.{p}{result.tm_mon}.{result.tm_year} | {result.tm_hour}:{result.tm_min}:{result.tm_sec}'
    times2 = str(times)

    cursor.execute(f"SELECT user_id FROM users WHERE user_id = '{user_id}'")
    if cursor.fetchone() is None:
       
       reffer_id = message.text[7:]
       print(reffer_id)
       if reffer_id != '':
         reffer_id = int(reffer_id)
         
         reffer_name = cursor.execute(f'SELECT user_name FROM users WHERE user_id = {reffer_id}').fetchone()
         reffer_name = str(reffer_name[0])

         user_name = message.from_user.full_name

         add_users = cursor.execute(f'SELECT summ FROM reffer WHERE user_id = {reffer_id}').fetchone()
         add_users = int(add_users[0])
         
         balance = cursor.execute("SELECT balance from users where user_id = ?", (reffer_id,))
         balance = cursor.fetchone()
         balance = int(balance[0])
         donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?", (reffer_id,))
         donate_coins = cursor.fetchone()
         donate_coins = int(donate_coins[0])
         
         await message.reply(f'✅ Вы стали рефералом игрока {reffer_name}')
         cursor.execute(f'UPDATE reffer SET summ = {add_users + 1} WHERE user_id = {reffer_id}')



         try:
            await message.bot.send_message(reffer_id, f'💰 Вы стали рефералом игрока {user_name}, и получили за это 10.000.000.000.000¢ и 15 пончиков 🍩')
            cursor.execute(f'UPDATE users SET balance = {balance + 10000000000000} WHERE user_id = {reffer_id}')
            cursor.execute(f'UPDATE users SET donate_coins = {donate_coins + 15} WHERE user_id = {reffer_id}')
            connect.commit()
         except:
            pass


       cursor.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", (user_id, user_name, full_name, user_status, 100000, 0, 0, 0, status_block, times2, pref, 0, 0, 0, 0, stats_status, 0, 0, 0, 0, 0, 0, 0, 0, 0, pet_name, 100, 100, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, uid, 0, 0))
       cursor.execute("INSERT INTO mine VALUES(?, ?, ?, ?, ?, ?, ?, ?);",(user_id, full_name,status_block, 0, 0, 0, 0, 0))
       cursor.execute("INSERT INTO user_case VALUES(?, ?, ?);",(user_id, 0, 0))
       cursor.execute("INSERT INTO bot_time VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", (user_id, 0, 0, 0, 0, 0, 0, 0, 0, 0))
       cursor.execute("INSERT INTO time_bank VALUES(?, ?);",(user_id, 0))
       cursor.execute("INSERT INTO ob_time VALUES(?, ?);",(user_id, 0))
       cursor.execute("INSERT INTO cars VALUES(?, ?, ?, ?, ?);",(user_id, user_name, 0, 0, 0))
       cursor.execute("INSERT INTO reffer VALUES(?, ?);",(user_id, 0))
       cursor.execute("INSERT INTO tiktok VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?);",(tt_name, tt_reg, 0, 0, 0, 0, 0, 0, user_id))
       cursor.execute("INSERT INTO house VALUES(?, ?, ?, ?);",(user_id, user_name, 0, 0))
       cursor.execute("INSERT INTO truck VALUES(?, ?, ?, ?, ?);",(user_id, user_name, 0, 0, 0))
       connect.commit()
       print(f'Зарегестрировался в боте пользователь: {full_name}')
       await bot.send_message(message.chat.id, text_register[0], reply_markup=help3, parse_mode='html')

    else:
       await bot.send_message(message.chat.id, text_register[1], reply_markup=help3, disable_web_page_preview=True, parse_mode='html')
    

###########################################БАЛАНС###########################################
@dp.message_handler()
async def prof_user(message: types.Message):
    msg = message
    host = message.text.lower()
    user_id = msg.from_user.id
    full_name = msg.from_user.full_name
    user_name = 'НоуНейм'
    user_status = "Player"
    status_block = 'off'
    stats_status = 'off'
    pref = 'Игрок'
    pet_name = "name"
    tt_name = 'none'
    tt_reg = 'off'
    list1 = cursor.execute(f"SELECT * FROM users ORDER BY id DESC")
    uid = 1
    for user in list1:
        uid += 1
    chat_id = message.chat.id
    result = time.localtime()

    if int(result.tm_mon) <= 9:
      p = "0"
    else:
      p = ''
    times = f'{result.tm_mday}.{p}{result.tm_mon}.{result.tm_year} | {result.tm_hour}:{result.tm_min}:{result.tm_sec}'
    times2 = str(times)

    cursor.execute(f"SELECT user_id FROM users WHERE user_id = '{user_id}'")
    if cursor.fetchone() is None:
       
       cursor.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", (user_id, user_name, full_name, user_status, 100000, 0, 0, 0, status_block, times2, pref, 0, 0, 0, 0, stats_status, 0, 0, 0, 0, 0, 0, 0, 0, 0, pet_name, 100, 100, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, uid, 0, 0))
       cursor.execute("INSERT INTO mine VALUES(?, ?, ?, ?, ?, ?, ?, ?);",(user_id, full_name,status_block, 0, 0, 0, 0, 0))
       cursor.execute("INSERT INTO user_case VALUES(?, ?, ?);",(user_id, 0, 0))
       cursor.execute("INSERT INTO bot_time VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", (user_id, 0, 0, 0, 0, 0, 0, 0, 0, 0))
       cursor.execute("INSERT INTO time_bank VALUES(?, ?);",(user_id, 0))
       cursor.execute("INSERT INTO ob_time VALUES(?, ?);",(user_id, 0))
       cursor.execute("INSERT INTO cars VALUES(?, ?, ?, ?, ?);",(user_id, user_name, 0, 0, 0))
       cursor.execute("INSERT INTO reffer VALUES(?, ?);",(user_id, 0))
       cursor.execute("INSERT INTO tiktok VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?);",(tt_name, tt_reg, 0, 0, 0, 0, 0, 0, user_id))
       cursor.execute("INSERT INTO house VALUES(?, ?, ?, ?);",(user_id, user_name, 0, 0))
       cursor.execute("INSERT INTO truck VALUES(?, ?, ?, ?, ?);",(user_id, user_name, 0, 0, 0))
       connect.commit()
       print(f'Зарегестрировался в боте пользователь: {full_name}')
       help3 = InlineKeyboardMarkup(row_width=2)
       keyboard = InlineKeyboardMarkup()
       button = InlineKeyboardButton('Канал разработки!', url='https://t.me/rdg_channel')
       keyboard.add(button)
       keyboard2 = InlineKeyboardMarkup()
       button2 = InlineKeyboardButton('Чатик', url='https://t.me/end_soft')
       keyboard3 = InlineKeyboardMarkup()
       button3 = InlineKeyboardButton('Добавить меня в группу!', url='https://t.me/end_soft_BOT?startgroup=new')
       keyboard3.add(button3)
       register_help = InlineKeyboardButton(text='Помощь', callback_data='register_help')
       help3.add(button, button2, button3, register_help)
       await bot.send_sticker(chat_id=message.chat.id, sticker='CAACAgIAAxkBAAEG7yljo0ret60PPsrmFEk9gR27U6uzSQACg40AAp7OCwABxPqWMvUw1YMsBA')
       
       name = message.from_user.get_mention(as_html=True)
       await bot.send_message(message.chat.id, f'''👋 Привет, {name}!\n🔥 <b>Я - Игровой бот « RDG », я владею самой лучшей в среде игровых ботов и уникальными играми, а также ты можешь добавить меня в свой чат со своими друзьями! </b>\n💰 Мы выдали вам 100.000¢ в качестве бонуса\n🆘 Напиши <b>«Помощь»</b> чтобы узнать все комманды бота!\n\n↘️ А также советуем вам зайти по этим кнопкам!
    ''', reply_markup=help3, parse_mode='html')


    status_block = cursor.execute("SELECT status_block from users where user_id = ?",(message.from_user.id,)).fetchone()
    status_block = str(status_block[0])

    if status_block == 'on':
       if chat_id == user_id:
          return await message.reply(f'❗️ Ваш аккаунт находиться в стадии <b>блокировки</b> ', parse_mode='html')
       return

    if message.forward_date != None:
       if user_id != cfg.owner_id:
         if chat_id == user_id:
            return await message.reply(f'❗️ Я не реагирую на <b>пер. сообщение</b>', parse_mode='html')
         return


    period = 1
    get = cursor.execute("SELECT stavka FROM ob_time WHERE user_id = ?",(message.from_user.id,)).fetchone()
    last_stavka = f"{int(get[0])}"
    stavkatime = time.time() - float(last_stavka)
    if stavkatime < period:
       chat_id = message.chat.id
       user_id = message.from_user.id

       if chat_id == user_id:
          return await message.reply(f'💬 <b>[ANTI-FLOOD]</b> - Не так быстро, в боте стоит ограничение между командами <b>{period} секунд(а)</b>', parse_mode='html')


    if message.text.lower().startswith("баланс") or message.text.lower().startswith("б") or message.text.startswith("@RDG_GAMEE_BOT баланс"):
       msg = message
       user_id = msg.from_user.id
       
       chat_id = message.chat.id
       pref = cursor.execute("SELECT pref from users where user_id = ?",(message.from_user.id,)).fetchone()
       pref = str(pref[0])

       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()              
       balance = cursor.execute("SELECT balance from users where user_id = ?",(message.from_user.id,)).fetchone()
       balance = int(balance[0])
       balance2 = '{:,}'.format(balance)
       bank = cursor.execute("SELECT bank from users where user_id = ?",(message.from_user.id,)).fetchone()
       bank = int(bank[0])
       bank2 = '{:,}'.format(bank)
       user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_status = str(user_status[0])
       donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(message.from_user.id,)).fetchone()
       donate_coins = int(donate_coins[0])
       donate_coins2 = '{:,}'.format(donate_coins)
       player = status_users(message.from_user.id)
       photo = select_photo(message.from_user.id)

       life3 = types.InlineKeyboardMarkup(row_width=2)
       life3.add(types.InlineKeyboardButton(text='🎁 Бонус', callback_data='bonus5'), types.InlineKeyboardButton(text='📇 Крипто', callback_data='cripto5'))

       obb_summ = balance + bank
        
       from utils import scor_summ
        
       obb_summ2 = await scor_summ(obb_summ)

       text_balance = f"""
{player} ➪ <a href='tg://user?id={user_id}'>{user_name}</a>, данные о средствах

💸 • Кошелёк: <code>{balance2}</code>
💳 • Карта: <code>{bank2}</code>¢
🍩 • Пончиков в корзинке: <code>{donate_coins}</code>🍩

💰 • Всего денег: <code>{obb_summ2}</code>¢
    """

       await bot.send_message(message.chat.id,text_balance, reply_markup=life3, parse_mode='html')


###########################################ПЕРЕВОДЫ###########################################
    if message.text.lower().startswith("дать"):
       if not message.reply_to_message:
          await message.reply("Эта команда должна быть ответом на сообщение!")
          return
       msg = message
       user_id = msg.from_user.id
       name = msg.from_user.full_name 
       rname =  msg.reply_to_message.from_user.full_name 
       user_name = cursor.execute("SELECT user_name from users where user_id = ?", (message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?", (message.reply_to_message.from_user.id,)).fetchone()
       reply_user_name = str(reply_user_name[0])

       reply_user_id = msg.reply_to_message.from_user.id
       win = ['🙂', '😋', '😄', '🤑', '😃']
       rwin = random.choice(win)
       loser = ['😔', '😕', '😣', '😞', '😢']
       rloser = random.choice(loser)

       su = msg.text.split()[1]
       su2 = (su).replace(' ', '').replace('k', '000').replace('е','e').replace('к', '000').replace(',', '').replace('.', '')
       su3 = float(su2)
       perevod = int(su3)
       perevod2 = '{:,}'.format(perevod).replace(',', '.')

       cursor.execute(f"SELECT user_id FROM users WHERE user_id = '{user_id}'")
       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = round(int(balance[0]))
       balance2 = cursor.execute("SELECT balance from users where user_id = ?", (message.reply_to_message.from_user.id,)).fetchone()
       balance2 = round(balance2[0])
       
       
       
       
       if reply_user_id == user_id:
          await message.reply_to_message.reply(f'Вы не можете передать деньги сами себе! {rloser}', parse_mode='html')
          return

       if perevod > 0:
          if balance >= perevod:  
             await bot.send_message(cfg.log_group, f"""⚙️LOG: #перевод 
Игрок: <a href="tg://user?id={user_id}">{user_name}</a>(<code>{user_id}</code>) Передача денег игроку 
<a href="tg://user?id={reply_user_id}">{reply_user_name}</a>(<code>{reply_user_id}</code>) в размере {perevod2}¢
""", parse_mode='html')

             money_photo = open('imges/perevod.jpg', 'rb')
             await bot.send_photo(chat_id=message.chat.id, photo=money_photo, caption=f"""
💸 <a href='tg://user?id={user_id}'>{user_name}</a> передал {perevod2}¢ игроку <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a> {rwin}""", parse_mode='html')
             cursor.execute(f'UPDATE users SET balance = {balance - perevod} WHERE user_id = "{user_id}"') 
             cursor.execute(f'UPDATE users SET balance = {balance2 + perevod} WHERE user_id = "{reply_user_id}"')
             connect.commit()    
             
             money_photo = open('imges/perevod.jpg', 'rb')
             await bot.send_photo(reply_user_id, photo=money_photo, caption=f"""
💸 <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>, вы получили {perevod2}¢ от игрока <a href='tg://user?id={user_id}'>{user_name}</a> """, parse_mode='html')
   
          elif int(balance) <= int(perevod):
             await message.reply( f"<a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств! {rloser}", reply_markup=balanc, parse_mode='html')

       if perevod <= 0:
          await message.reply( f"<a href='tg://user?id={user_id}'>{user_name}</a>, нельзя перевести отрицательное число! {rloser}", parse_mode='html')
          		

    if message.text.lower().startswith("пдать"):
       if not message.reply_to_message:
          await message.reply("Эта команда должна быть ответом на сообщение!")
          return
       msg = message
       user_id = msg.from_user.id
       name = msg.from_user.full_name 
       rname =  msg.reply_to_message.from_user.full_name 
       user_name = cursor.execute("SELECT user_name from users where user_id = ?", (message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?", (message.reply_to_message.from_user.id,)).fetchone()
       reply_user_name = str(reply_user_name[0])

       reply_user_id = msg.reply_to_message.from_user.id
       win = ['🙂', '😋', '😄', '🤑', '😃']
       rwin = random.choice(win)
       loser = ['😔', '😕', '😣', '😞', '😢']
       rloser = random.choice(loser)

       su = msg.text.split()[1]
       su2 = (su).replace(' ', '').replace('k', '000').replace('е','e').replace('к', '000').replace(',', '').replace('.', '')
       su3 = float(su2)
       perevod = int(su3)
       perevod2 = '{:,}'.format(perevod).replace(',', '.')

       cursor.execute(f"SELECT user_id FROM users WHERE user_id = '{user_id}'")
       donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?", (message.from_user.id,)).fetchone()
       donate_coins = round(int(donate_coins[0]))
       donate_coins2 = cursor.execute("SELECT donate_coins from users where user_id = ?", (message.reply_to_message.from_user.id,)).fetchone()
       donate_coins2 = round(donate_coins2[0])
       

       if reply_user_id == user_id:
          await message.reply_to_message.reply(f'Вы не можете передать пончики сами себе! {rloser}', parse_mode='html')
          return

       if perevod > 0:
          if donate_coins >= perevod:  
             await bot.send_message(cfg.log_group, f"""⚙️LOG: #перевод 
Игрок: <a href="tg://user?id={user_id}">{user_name}</a>(<code>{user_id}</code>) Передача денег игроку 
<a href="tg://user?id={reply_user_id}">{reply_user_name}</a>(<code>{reply_user_id}</code>) в размере {perevod2}🍩
""", parse_mode='html')

             await bot.send_message(chat_id, f"""<a href="tg://user?id={user_id}">{user_name}</a> передал {perevod2}🍩 игроку <a href="tg://user?id={reply_user_id}">{reply_user_name}</a>""", parse_mode='html')
             cursor.execute(f'UPDATE users SET donate_coins = {donate_coins - perevod} WHERE user_id = "{user_id}"') 
             cursor.execute(f'UPDATE users SET donate_coins = {donate_coins2 + perevod} WHERE user_id = "{reply_user_id}"')
             connect.commit()

          elif int(donate_coins) <= int(perevod):
             await message.reply( f"<a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств! {rloser}", parse_mode='html')

       if perevod <= 0:
          await message.reply( f"<a href='tg://user?id={user_id}'>{user_name}</a>, нельзя перевести отрицательное число! {rloser}", parse_mode='html')

###########################################РЕФ###########################################
    if message.text.lower() == 'реф':
       user_id = message.from_user.id

       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(user_id,)).fetchone()
       user_name = str(user_name[0])

       add_users = cursor.execute("SELECT summ from reffer where user_id = ?",(user_id,)).fetchone()
       add_users = int(add_users[0])

       

       text = f'''
💰 <b>За приглашение вы получите 10.000.000.000.000¢ и 15 🍩</b>

🫂 <b>Количество приглашенных пользователей - {'{:,}'.format(add_users).replace(',', '.')} шт.</b>

🔗 <b>Реферальная ссылка -</b> <code>http://t.me/{cfg.bot_name}?start={user_id}</code>
       '''

       reff_inline = InlineKeyboardMarkup(row_width=1)

       reff_inline.add(
            InlineKeyboardButton(text='🚩 Поделиться', switch_inline_query=f'http://t.me/{cfg.bot_name}?start={user_id}')
       )

       await message.reply(text, reply_markup=reff_inline,  parse_mode='html')


################################################ПРОФИЛЬ#############################################################
    if message.text.lower() in ["профиль", "Профиль", "п", "П"]:
       msg = message
       chat_id = message.chat.id
       name = message.from_user.get_mention(as_html=True)
       
       time_register = cursor.execute("SELECT time_register FROM users WHERE user_id=?", (message.from_user.id,)).fetchall()
       time_register = time_register[0]
       
       user_id = msg.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])       
       
       user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()
       uid = cursor.execute("SELECT id from users where user_id = ?",(message.from_user.id,)).fetchone()
       balance = cursor.execute("SELECT balance from users where user_id = ?",(message.from_user.id,)).fetchone()
       bank = cursor.execute("SELECT bank from users where user_id = ?",(message.from_user.id,)).fetchone()
       ethereum = cursor.execute("SELECT ethereum from users where user_id = ?",(message.from_user.id,)).fetchone()
       bitcoin = cursor.execute("SELECT bitcoin from users where user_id = ?",(message.from_user.id,)).fetchone()
       litecoin = cursor.execute("SELECT litecoin from users where user_id = ?",(message.from_user.id,)).fetchone()
       fantom = cursor.execute("SELECT fantom from users where user_id = ?",(message.from_user.id,)).fetchone()
       rating = cursor.execute("SELECT rating from users where user_id = ?",(message.from_user.id,)).fetchone()
       pref = cursor.execute("SELECT pref from users where user_id = ?",(message.from_user.id,)).fetchone()
       pref = str(pref[0])
       level = cursor.execute("SELECT level from users where user_id = ?", (message.from_user.id,)).fetchone()
       level = int(level[0])
       work = cursor.execute("SELECT work from users where user_id = ?", (message.from_user.id,)).fetchone()
       work = int(work[0])
       donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(message.from_user.id,)).fetchone()
       donate_coins = int(donate_coins[0])
       donate_coins2 = '{:,}'.format(donate_coins)
       user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_status = str(user_status[0])
       game = cursor.execute("SELECT game from users where user_id = ?",(message.from_user.id,)).fetchone()
       game = int(game[0])
       game2 = '{:,}'.format(game)

       balance = int(balance[0])
       bank = int(bank[0])
       rating = int(rating[0])
       ethereum = int(ethereum[0])
       bitcoin = int(bitcoin[0])
       litecoin = int(litecoin[0])
       fantom = int(fantom[0])
       uid = int(uid[0])
       user_status2=status_users(user_id)
       
       truck = cursor.execute("SELECT truck from truck where user_id = ?",(message.from_user.id,)).fetchone()
       truck = int(truck[0])
       
       cars = cursor.execute("SELECT cars from cars where user_id = ?",(message.from_user.id,)).fetchone()
       cars = int(cars[0])

       house = cursor.execute("SELECT house from house where user_id = ?",(message.from_user.id,)).fetchone()
       house = int(house[0])

       ded3 = InlineKeyboardMarkup(row_width=2)
       bonus5 = InlineKeyboardButton(text='🎁 Бонус', callback_data='bonus5')
       ded3.add(bonus5)

       d5 = 0

       if house == 1:
          house2 = '\n    <b>🏠Дом:</b> <code>Дом</code>\n'
          d5 += 1
       if house == 2:
          house2 = '    <b>🏠Дом:</b> <code>Квартира</code>\n'
          d5 += 1
       if house == 3:
          house2 = '    <b>🏠Дом:</b> <code>Огромный дом</code>\n'
          d5 += 1
       if house == 4:
          house2 = '    <b>🏠Дом:</b> <code>Коттедж</code>\n'
          d5 += 1
       if house == 5:
          house2 = '    <b>🏠Дом:</b> <code>Бурдж Кхалифа</code>\n'
          d5 += 1
       if house == 6:
          house2 = '    <b>🏠Дом:</b> <code>Россия</code>\n'
          d5 += 1
       if house == 7:
          house2 = '    <b>🏠Дом:</b> <code>Половина земли</code>\n'
          d5 += 1
       if house == 8:
          house2 = '    <b>🏠Дом:</b> <code>Марс</code>\n'
          d5 += 1
       else:
          house2 = ''

       if cars == 1:
          cars2 = '    <b>🚘Машина:</b> <code>ВАЗ 2107</code>\n'
          d5 += 1
       if cars == 2:
          cars2 = '    <b>🚘Машина:</b> <code>Lada Vesta</code>\n'
          d5 += 1
       if cars == 3:
          cars2 = '    <b>🚘Машина:</b> <code>Lada XRAY Cross</code>\n'
          d5 += 1
       if cars == 4:
          cars2 = '    <b>🚘Машина:</b> <code>Audi Q7</code>\n'
          d5 += 1
       if cars == 5:
          cars2 = '    <b>🚘Машина:</b> <code>BMW X6</code>\n'
          d5 += 1
       if cars == 6:
          cars2 = '    <b>🚘Машина:</b> <code>Hyundai Solaris</code>\n'
          d5 += 1
       if cars == 7:
          cars2 = '    <b>🚘Машина:</b> <code>Toyota Supra</code>\n'
          d5 += 1
       if cars == 8:
          cars2 = '    <b>🚘Машина:</b> <code>Lamborghini Veneno</code>\n'
          d5 += 1
       if cars == 9:
          cars2 = '    <b>🚘Машина:</b> <code>Bugatti Veyron</code>\n'
          d5 += 1
       if cars == 10:
          cars2 = '    <b>🚘Машина:</b> <code>Tesla Roadster</code>\n'
          d5 += 1
       if cars == 11:
          cars2 = '    <b>🚘Машина:</b> <code>Koenigsegg Jesco</code>\n'
          d5 += 1
       else:
          cars2 = ''

       if truck == 1:
          truck2 = '    <b>🚛Грузовик:</b> <code>Daf</code>\n'
          d5 += 1
       if truck == 2:
          truck2 = '    <b>🚛Грузовик:</b> <code>Scania</code>\n'
          d5 += 1
       if truck == 3:
          truck2 = '    <b>🚛Грузовик:</b> <code>Nissan</code>\n'
          d5 += 1
       if truck == 4:
          truck2 = '    <b>🚛Грузовик:</b> <code>Renault</code>\n'
          d5 += 1
       if truck == 5:
          truck2 = '    <b>🚛Грузовик:</b> <code>Volvo</code>\n'
          d5 += 1
       if truck == 6:
          truck2 = '    <b>🚛Грузовик:</b> <code>Man</code>\n'
          d5 += 1
       if truck == 7:
          truck2 = '    <b>🚛Грузовик:</b> <code>Mercedes Benz</code>\n'
          d5 += 1
       else:
          truck2 = ''          

       if d5 == 0:
          d6 = '\n      У вас нету имущества 🙁'
       else:
          d6 = '🏗 Имущество:\n'

       from utils import scor_summ
       balance3 = await scor_summ(balance)       
       ethereum3 = await scor_summ(ethereum)
       bank3 = await scor_summ(bank)
       rating3 = await scor_summ(rating)
       bitcoin3 = await scor_summ(bitcoin)
       litecoin3 = await scor_summ(litecoin)        
       fantom3 = await scor_summ(fantom)        
                                        

       money_photo = open('imges/prof.jpg', 'rb')
       await bot.send_photo(chat_id=message.chat.id, photo=money_photo, caption=f"""
{name}, ваш профиль:
➖➖➖➖➖➖➖➖➖➖➖➖
👤 <b>Ник:</b> <code><a href='tg://user?id={user_id}'>{user_name}</a></code>
🔎 <b>ID:</b> <code>{user_id}</code>
➖➖➖➖➖➖➖➖➖➖➖➖
🔸 <b>Игровой айди:</b> <code>{uid}</code>
❗️ <b>Привилегия:</b> <code>{user_status2}</code>
➖➖➖➖➖➖➖➖➖➖➖➖
💵 <b>Деньги:</b> <code>{balance3}</code>
💳 <b>В карте:</b> <code>{bank3}</code>
➖➖➖➖➖➖➖➖➖➖➖➖
🔹 • Лайткоин: <code>{litecoin3}</code>🔹
💽 • Биткоины: <code>{bitcoin3}</code>฿
🟣 • Эфириум: <code>{ethereum3}</code>🟣
💠 • Фантом: <code>{fantom3}</code>💠
➖➖➖➖➖➖➖➖➖➖➖➖
👑 <b>Рейтинг:</b> <code>{rating3}</code>
🍩 <b>Пончиков:</b> <code>{donate_coins2}</code>
➖➖➖➖➖➖➖➖➖➖➖➖
📊 <b>Уровень:</b> <code>{level}</code>
🎯 <b>Всего сыграно игр:</b> <code>{game2}</code>
<b>{d6}</b>{house2}{cars2}{truck2}
➖➖➖➖➖➖➖➖➖➖➖➖
📆 <b>Дата регистрации:</b> <code>{time_register}</code>
   """,  reply_markup=ded3, parse_mode='html')


###########################################НИК###########################################
    if message.text.lower() in ["Ник", "ник", "Имя", "имя", "Мой ник", "мой ник", "Мое имя", "мое имя", "Моё имя", "моё имя"]:
       msg = message
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])
       
       video = open('video/mam.mp4', 'rb')
       await message.bot.send_video(chat_id=message.chat.id, video=video, caption=f"🎅 <b>Ваш ник:</b> <code>{user_name}</code>", parse_mode='html')

###########################################КАРТА###########################################
    # karta
    if message.text.lower().startswith("карта"):
       msg = message
       chat_id = message.chat.id
       
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       user_id = msg.from_user.id
       user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()
       bank = cursor.execute("SELECT bank from users where user_id = ?",(message.from_user.id,)).fetchone()
       bank_hran = cursor.execute("SELECT bank2 from users where user_id = ?",(message.from_user.id,)).fetchone()
       bank = int(bank[0])
       depozit = cursor.execute("SELECT depozit from users where user_id = ?",(message.from_user.id,)).fetchone()
       depozit = int(depozit[0])
       bank_hran = int(bank_hran[0])
       bank_hran2 = '{:,}'.format(bank_hran).replace(',', '.')
       bank = cursor.execute("SELECT bank from users where user_id = ?", (message.from_user.id,)).fetchone()
       bank = int(bank[0])
       depozit2 = '{:,}'.format(depozit).replace(',', '.')
       bank2 = '{:,}'.format(bank).replace(',', '.')
       if user_status == 'Player':
          procent = '6%'
          i = 6
          stats_depozit = 'Обычный'
       if user_status == 'Vip':
          procent = '9%'
          i = 9
          stats_depozit = 'Вип'
       if user_status == 'Premium':
          procent = '13%'
          i = 13
          stats_depozit = 'Премиум'
       if user_status == 'Platina':
          procent = '17%'
          i = 17
          stats_depozit = 'Платина'
       if user_status == 'Helper':
          procent = '21%'
          i = 21
          stats_depozit = 'Хелпер'
       if user_status == 'Sponsor':
          procent = '24%'
          i = 24
          stats_depozit = 'Спонсор'
       if user_status == 'Osnovatel':
          procent = '27%'
          i = 27
          stats_depozit = 'Основатель'
       if user_status == 'Vladelec':
          procent = '29%'
          i = 29
          stats_depozit = 'Владелец'
       if user_status == 'Bog':
          procent = '32%'
          i = 32
          stats_depozit = 'Бог'
       if user_status == 'Vlaselin':
          procent = '36%'
          i = 36
          stats_depozit = 'Властелин'

       else:
          procent = '6%'
          i = 6
          stats_depozit = 'Обычный'
          
          money_vivod = depozit / i
          money_vivod2 = int(money_vivod)
          money_vivod3 = '{:,}'.format(money_vivod2).replace(',', '.')

          bank2 = '{:,}'.format(bank).replace(',', '.')
          bank_hran2 = '{:,}'.format(bank_hran).replace(',', '.')
          depozit2 = '{:,}'.format(depozit).replace(',', '.')

          money_photo = open('imges/visa.jpg', 'rb')
          await bot.send_photo(chat_id=message.chat.id, photo=money_photo, caption=f"""
<b>Вот данные о вашем карте 💳</b>

[👤] <b>Владелец:</b> {user_name}

[⚜] <b>Данные:</b>

[💰] <b>Деньги на карте:</b> {bank2}¢
[💼] <b>Хранительный счёт:</b> {bank_hran2}¢
[🔰] <b>Деньги на депозите:</b> {depozit2}¢
[💎] <b>Статус депозита:</b> {stats_depozit}
[📈] <b>Процент под депозит:</b> {procent}
[💵] <b>Деньги на вывод:</b> {money_vivod3}¢""", parse_mode='html')
    if message.text.startswith("процент") or message.text.startswith("Процент"):
       msg = message
       user_id = msg.from_user.id
       name = msg.from_user.last_name
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       i2 = str(msg.text.split()[1])
       su = msg.text.split()[2]
       su2 = (su).replace(' ', '').replace('k', '000').replace('е','e').replace('к', '000').replace(',', '').replace('.', '')
       su3 = float(su2)
       summ = int(su3)
       summ2 = '{:,}'.format(summ).replace(',', '.')

       user_status = cursor.execute("SELECT user_status from users where user_id = ?", (message.from_user.id,)).fetchone()
       user_status = str(user_status[0])
       depozit = cursor.execute("SELECT depozit from users where user_id = ?", (message.from_user.id,)).fetchone()
       depozit = int(depozit[0])
       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])
       loser = ['😔', '😕', '😣', '😞', '😢']
       rloser = random.choice(loser)
       if user_status == 'Player':
          procent = '6%'
          i = 6
          stats_depozit = 'Обычный'
       if user_status == 'Vip':
          procent = '9%'
          i = 9
          stats_depozit = 'Вип'
       if user_status == 'Premium':
          procent = '13%'
          i = 13
          stats_depozit = 'Премиум'
       if user_status == 'Platina':
          procent = '17%'
          i = 17
          stats_depozit = 'Платина'
       if user_status == 'Helper':
          procent = '21%'
          i = 21
          stats_depozit = 'Хелпер'
       if user_status == 'Sponsor':
          procent = '24%'
          i = 24
          stats_depozit = 'Спонсор'
       if user_status == 'Osnovatel':
          procent = '27%'
          i = 27
          stats_depozit = 'Основатель'
       if user_status == 'Vladelec':
          procent = '29%'
          i = 29
          stats_depozit = 'Владелец'
       if user_status == 'Bog':
          procent = '32%'
          i = 32
          stats_depozit = 'Бог'
       if user_status == 'Vlaselin':
          procent = '36%'
          i = 36
          stats_depozit = 'Властелин'

       else:
          procent = '6%'
          i = 6
          stats_depozit = 'Обычный'
          
          money_vivod = depozit / i
          money_vivod2 = int(money_vivod)
          money_vivod3 = '{:,}'.format(money_vivod2).replace(',', '.')
       period = 259200 #259200s 3d
       get = cursor.execute("SELECT stavka_depozit FROM bot_time WHERE user_id = ?", (message.from_user.id,)).fetchone()
       last_stavka = f"{int(get[0])}"
       stavkatime = time.time() - float(last_stavka)
       if i2 == 'снять':
          if summ <= money_vivod2 :
             if summ > 0:
                if stavkatime > period:
                   await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , вы успешно сняли проценты с депозита {summ2}¢ 💵", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance + summ}  WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_depozit = {time.time()}  WHERE user_id = {user_id}')
                   connect.commit()
                   return
                else:
                   await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , извините но снимать с процентов депозита можно раз в 3 дня ⌛️", parse_mode='html')
             else:
                await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , нельзя снимать отрицательное число {rloser}", parse_mode='html')
          else:
             await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , недостаточно средств {rloser}", parse_mode='html')
   

   
    if message.text.startswith("депозит") or message.text.startswith("Депозит"):
       msg = message
       user_id = msg.from_user.id
       name = msg.from_user.last_name
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       i = str(msg.text.split()[1])
       su = msg.text.split()[2]
       su2 = (su).replace(' ', '').replace('k', '000').replace('е','e').replace('к', '000').replace(',', '').replace('.', '')
       su3 = float(su2)
       summ = int(su3)
       summ2 = '{:,}'.format(summ).replace(',', '.')

       user_status = cursor.execute("SELECT user_status from users where user_id = ?", (message.from_user.id,)).fetchone()
       user_status = str(user_status[0])
       depozit = cursor.execute("SELECT depozit from users where user_id = ?", (message.from_user.id,)).fetchone()
       depozit = int(depozit[0])
       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])
       loser = ['😔', '😕', '😣', '😞', '😢']
       rloser = random.choice(loser)
       
       period = 259200 #259200s 3d
       get = cursor.execute("SELECT stavka_depozit FROM bot_time WHERE user_id = ?", (message.from_user.id,)).fetchone()
       last_stavka = f"{int(get[0])}"
       stavkatime = time.time() - float(last_stavka)
       if i == 'положить':
          if summ <= balance :
             if summ > 0:
                if stavkatime > period:
                   await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , вы успешно положили на депозит {summ2}¢ 🔐", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ}  WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET depozit = {depozit + summ}  WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_depozit = {time.time()}  WHERE user_id = {user_id}')
                   connect.commit()
                   return
                else:
                   await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , извините но ложить, снимать с депозита можно раз в 3 дня ⌛️", parse_mode='html')
             else:
                await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , нельзя ложить отрицательное число {rloser}", parse_mode='html')
          else:
             await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , недостаточно средств {rloser}", reply_markup=balanc, parse_mode='html')
       if i == 'снять':
          if summ <= depozit :
             if summ > 0:
                if stavkatime > period:
                   await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , вы успешно сняли с депозита {summ2}¢ 🔐", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance + summ}  WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET depozit = {depozit - summ}  WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_depozit = {time.time()}  WHERE user_id = {user_id}')
                   connect.commit()
                   return
                else:
                   await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , извините но ложить, снимать с депозита можно раз в 3 дня ⌛️", parse_mode='html')
             else:
                await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , нельзя снимать отрицательное число {rloser}", parse_mode='html')
          else:
             await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , недостаточно средств {rloser}", parse_mode='html')

    if message.text.startswith("карта положить") or message.text.startswith("Карта положить"):
       msg = message
       chat_id = message.chat.id
       user_id = msg.from_user.id
       name = msg.from_user.last_name
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       su = msg.text.split()[2]
       su2 = (su).replace(' ', '').replace('k', '000').replace('е','e').replace('к', '000').replace(',', '').replace('.', '')
       su3 = float(su2)
       bank_p = int(su3)

       cursor.execute(f"SELECT user_id FROM users WHERE user_id = '{user_id}'")
       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = round(int(balance[0]))
       bank = cursor.execute("SELECT bank from users where user_id = ?", (message.from_user.id,)).fetchone()
       bank = round(int(bank[0]))
       bank2 = '{:,}'.format(bank_p).replace(',', '.')
       win = ['🙂', '😋', '😄', '🤑', '😃']
       rwin = random.choice(win)
       loser = ['😔', '😕', '😣', '😞', '😢']
       rloser = random.choice(loser)
       period = 0
       get = cursor.execute(f"SELECT stavka FROM time_bank WHERE user_id = {user_id}").fetchone()
       last_stavka = f"{int(get[0])}"
       stavkatime = time.time() - float(last_stavka)
       if stavkatime > period:
          if bank_p > 0:
             if balance >= bank_p:
                await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , вы успешно положили в карту {bank2}¢ {rwin}",
                                        parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - bank_p} WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE users SET bank = {bank + bank_p} WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE time_bank SET stavka = {time.time()} WHERE user_id = {user_id}')
                connect.commit()

             elif int(balance) < int(bank_p):
                await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , недостаточно средств! {rloser}", reply_markup=balanc, parse_mode='html')

          if bank_p <= 0:
             await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , нельзя положить в карту отрицательное число! {rloser}",
                                     parse_mode='html')
       else:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, ложить в карту можно раз в 3 минуты", parse_mode='html')                    
    
    if message.text.startswith("карта снять") or message.text.startswith("Карта снять"):
       msg = message
       chat_id = message.chat.id
       user_id = msg.from_user.id
       name = msg.from_user.last_name
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       su = msg.text.split()[2]
       su2 = (su).replace(' ', '').replace('k', '000').replace('е','e').replace('к', '000').replace(',', '').replace('.', '')
       su3 = float(su2)
       bank_s = int(su3)
       print(f"{name} снял с карты: {bank_s}")

       cursor.execute(f"SELECT user_id FROM users WHERE user_id = '{user_id}'")
       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = round(int(balance[0]))
       bank = cursor.execute("SELECT bank from users where user_id = ?", (message.from_user.id,)).fetchone()
       bank = round(int(bank[0]))
       bank2 = '{:,}'.format(bank_s).replace(',', '.')
       win = ['🙂', '😋', '😄', '🤑', '😃']
       rwin = random.choice(win)
       loser = ['😔', '😕', '😣', '😞', '😢']
       rloser = random.choice(loser)

       if bank_s > 0:
          if bank >= bank_s:
             await bot.send_message(message.chat.id,
                                    f"<a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно сняли с картовского счёта {bank2}¢ {rwin}",
                                    parse_mode='html')
             cursor.execute(f'UPDATE users SET bank = {bank - bank_s} WHERE user_id = "{user_id}"')
             cursor.execute(f'UPDATE users SET balance = {balance + bank_s} WHERE user_id = "{user_id}"')
             connect.commit()

          elif int(bank) < int(bank_s):
             await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств на картовского счету! {rloser}",
                                    parse_mode='html')    
    

###########################################РЕЙТИНГ###########################################
    if message.text.lower() in ["рейтинг", "Рейтинг"]:
       msg = message 
       user_id = msg.from_user.id
       rating = cursor.execute("SELECT rating from users where user_id = ?",(message.from_user.id,)).fetchone()
       rating = round(int(rating[0]))
       rating2 = '{:,}'.format(rating) 
       chat_id = message.chat.id
       user_name = message.from_user.get_mention(as_html=True)
       await bot.send_message(message.chat.id, f"{user_name}, ваш рейтинг {rating2}👑", parse_mode='html')

    if message.text.startswith("Рейтинг купить") or message.text.startswith("рейтинг купить"):
       msg = message
       user_id = msg.from_user.id
       user_name = message.from_user.get_mention(as_html=True)
       su = msg.text.split()[2]
       su2 = (su).replace(' ', '').replace('k', '000').replace('е','e').replace('к', '000').replace(',', '').replace('.', '')
       su3 = float(su2)
       summ = int(su3)
       chat_id = message.chat.id
       win = ['🙂', '😋', '😄', '🤑', '😃']
       rwin = random.choice(win)
       loser = ['😔', '😕', '😣', '😞', '😢']
       rloser = random.choice(loser)
       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])
       rating = cursor.execute("SELECT rating from users where user_id = ?", (message.from_user.id,)).fetchone()
       rating = int(rating[0])
       rating2 = '{:,}'.format(summ)
       balance2 = '{:,}'.format(balance) 
       c = summ * 150000000000000
       c2 = '{:,}'.format(c)
       if summ > 0:
        if int(balance) >= int(summ * 150000000000000):
          await bot.send_message(message.chat.id, f'👑 • {user_name}, вы повысили количество вашего рейтинга на {rating2}👑 за {c2}¢! {rwin}', parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance - c} WHERE user_id = "{user_id}"')
          cursor.execute(f'UPDATE users SET rating = {rating + summ} WHERE user_id = "{user_id}"')
          connect.commit()

 
        if int(balance) < int(summ * 150000000000000):
          await bot.send_message(message.chat.id, f'💰 • {user_name}, недостаточно средств! {rloser}', reply_markup=balanc, parse_mode='html')

       if summ <= 0:
         await bot.send_message(message.chat.id, f'ℹ️ • {user_name}, нельзя купить отрицательное число! {rloser}', parse_mode='html')
    
    if message.text.startswith("Рейтинг продать") or message.text.startswith("рейтинг продать"):
       msg = message
       user_id = msg.from_user.id
       chat_id = message.chat.id
       user_name = message.from_user.get_mention(as_html=True)
       su = msg.text.split()[2]
       su2 = (su).replace(' ', '').replace('k', '000').replace('е','e').replace('к', '000').replace(',', '').replace('.', '')
       su3 = float(su2)
       summ = int(su3)
       win = ['🙂', '😋', '😄', '🤑', '😃']
       rwin = random.choice(win)
       loser = ['😔', '😕', '😣', '😞', '😢']
       rloser = random.choice(loser)
       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])
       balance2 = '{:,}'.format(balance) 
       rating = cursor.execute("SELECT rating from users where user_id = ?", (message.from_user.id,)).fetchone()
       rating = int(rating[0])
       c = summ * 50000000000000
       c2 ='{:,}'.format(c)
       rating2 = '{:,}'.format(summ)
       if summ > 0:
        if int(rating) >= int(summ):
          await bot.send_message(message.chat.id, f'👑 • {user_name}, вы понизили количество вашего рейтинга на {rating2}👑 за {c2}¢! {rwin}', parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance + c} WHERE user_id = "{user_id}"')
          cursor.execute(f'UPDATE users SET rating = {rating - summ} WHERE user_id = "{user_id}"')
          connect.commit()
 
        if int(rating) < int(summ):
          await bot.send_message(message.chat.id, f'👑 • {user_name}, у вас недостаточно рейтинга для его продажи! {rloser}', parse_mode='html')

       if summ <= 0:
          await bot.send_message(message.chat.id, f'ℹ️ • {user_name}, нельзя продать отрицательное число! {rloser}', parse_mode='html')
          
          
###########################################АДМИН###########################################
    if message.text.startswith("Выдать") or message.text.startswith("выдать"):
       msg = message
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
       reply_user_name = reply_user_name[0]
       win = ['🙂', '😋', '😄', '🤑', '😃']
       rwin = random.choice(win)
       perevod5 = message.text.split()[1]
       
       
       perevod4 = (perevod5).replace(' ', '').replace('k', '000').replace('е','e').replace('к', '000').replace(',', '').replace('.', '').replace("¢", "").replace('м', '000000').replace('m', '000000')
       perevod3 = float(perevod4)
       perevod = int(perevod3)
       perevod2 = '{:,}'.format(perevod).replace(',', '.')
       reply_user_id = msg.reply_to_message.from_user.id
       user_id = msg.from_user.id
       user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()
       balance2 = cursor.execute("SELECT balance from users where user_id = ?", (message.reply_to_message.from_user.id,)).fetchone()
       balance2 = round(balance2[0])
       if user_status[0] == 'Admin':
          await bot.send_message(cfg.log_group, f"""⚙️LOG: #перевод 
Игрок: <a href="tg://user?id={user_id}">{user_name}</a>(<code>{user_id}</code>) Выдача денег игроку 
<a href="tg://user?id={reply_user_id}">{reply_user_name}</a>(<code>{reply_user_id}</code>) в размере {perevod2}¢ 
""", parse_mode='html')
          await message.reply(f"💰 • Вы <a href='tg://user?id={user_id}'>{user_name}</a> выдали {perevod2}¢ игроку <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a> {rwin}", parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance2 + perevod} WHERE user_id = "{reply_user_id}"')
          connect.commit() 
       if user_status[0] == 'Helper_Admin':
          await bot.send_message(cfg.log_group, f"""⚙️LOG: #перевод 
Игрок: <a href="tg://user?id={user_id}">{user_name}</a>(<code>{user_id}</code>) Выдача денег игроку 
<a href="tg://user?id={reply_user_id}">{reply_user_name}</a>(<code>{reply_user_id}</code>) в размере {perevod2}₽ 
""", parse_mode='html')
          await message.reply(f"💰 • Вы <a href='tg://user?id={user_id}'>{user_name}</a> выдали {perevod2}¢ игроку <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a> {rwin}", parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance2 + perevod} WHERE user_id = "{reply_user_id}"')
          connect.commit()        
       if user_status[0] == 'Owner':
          await bot.send_message(cfg.log_group, f"""⚙️LOG: #перевод 
Игрок: <a href="tg://user?id={user_id}">{user_name}</a>(<code>{user_id}</code>) Выдача денег игроку 
<a href="tg://user?id={reply_user_id}">{reply_user_name}</a>(<code>{reply_user_id}</code>) в размере {perevod2}¢ 
""", parse_mode='html')
          await message.reply(f"💰 • Вы <a href='tg://user?id={user_id}'>{user_name}</a> выдали {perevod2}¢ игроку <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a> {rwin}", parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance2 + perevod} WHERE user_id = "{reply_user_id}"')
          connect.commit() 
       if user_status[0] == 'Rab':
          await bot.send_message(cfg.log_group, f"""⚙️LOG: #перевод 
Игрок: <a href="tg://user?id={user_id}">{user_name}</a>(<code>{user_id}</code>) Выдача денег игроку 
<a href="tg://user?id={reply_user_id}">{reply_user_name}</a>(<code>{reply_user_id}</code>) в размере {perevod2}¢ 
""", parse_mode='html')
          await message.reply(f"💰 • Вы <a href='tg://user?id={user_id}'>{user_name}</a> выдали {perevod2}¢ игроку <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a> {rwin}", parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance2 + perevod} WHERE user_id = "{reply_user_id}"')
          connect.commit()           
       if user_status[0] == 'Player':
          await message.reply(f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, вы не являетесь администратором бота!", parse_mode='html') 


    if message.text.startswith("Забрать") or message.text.startswith("забрать"):
       msg = message
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
       reply_user_name = reply_user_name[0]
       win = ['🙂', '😋', '😄', '🤑', '😃']
       rwin = random.choice(win)
       perevod5 = message.text.split()[1]
       
       
       perevod4 = (perevod5).replace(' ', '').replace('k', '000').replace('е','e').replace('к', '000').replace(',', '').replace('.', '').replace("¢", "").replace('м', '000000').replace('m', '000000')
       perevod3 = float(perevod4)
       perevod = int(perevod3)
       perevod2 = '{:,}'.format(perevod).replace(',', '.')
       reply_user_id = msg.reply_to_message.from_user.id
       user_id = msg.from_user.id
       user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()
       balance2 = cursor.execute("SELECT balance from users where user_id = ?", (message.reply_to_message.from_user.id,)).fetchone()
       balance2 = round(balance2[0])
       if user_status[0] == 'Admin':
          await bot.send_message(cfg.log_group, f"""⚙️LOG: #забрать
Игрок: <a href="tg://user?id={user_id}">{user_name}</a>(<code>{user_id}</code>) забрал денег у игрока
<a href="tg://user?id={reply_user_id}">{reply_user_name}</a>(<code>{reply_user_id}</code>) в размере {perevod2}¢ 
""", parse_mode='html')
          await message.reply(f"💰 • Вы <a href='tg://user?id={user_id}'>{user_name}</a> забрали {perevod2}¢ у игрока <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a> {rwin}", parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance2 - perevod} WHERE user_id = "{reply_user_id}"')
          connect.commit() 
       if user_status[0] == 'Helper_Admin':
          await bot.send_message(cfg.log_group, f"""⚙️LOG: #перевод 
Игрок: <a href="tg://user?id={user_id}">{user_name}</a>(<code>{user_id}</code>) Забрал денег у игрока
<a href="tg://user?id={reply_user_id}">{reply_user_name}</a>(<code>{reply_user_id}</code>) в размере {perevod2}¢
""", parse_mode='html')
          await message.reply(f"💰 • Вы <a href='tg://user?id={user_id}'>{user_name}</a> забрали {perevod2}¢ у игрока <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a> {rwin}", parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance2 - perevod} WHERE user_id = "{reply_user_id}"')
          connect.commit()        
       if user_status[0] == 'Owner':
          await bot.send_message(cfg.log_group, f"""⚙️LOG: #забрать
Игрок: <a href="tg://user?id={user_id}">{user_name}</a>(<code>{user_id}</code>) Забрал денег у игрока
<a href="tg://user?id={reply_user_id}">{reply_user_name}</a>(<code>{reply_user_id}</code>) в размере {perevod2}¢
""", parse_mode='html')
          await message.reply(f"💰 • Вы <a href='tg://user?id={user_id}'>{user_name}</a> забрали {perevod2}¢ у игрока <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a> {rwin}", parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance2 - perevod} WHERE user_id = "{reply_user_id}"')
          connect.commit() 
       if user_status[0] == 'Rab':
          await bot.send_message(cfg.log_group, f"""⚙️LOG: #забрать
Игрок: <a href="tg://user?id={user_id}">{user_name}</a>(<code>{user_id}</code>) Забрал денег у игрока
<a href="tg://user?id={reply_user_id}">{reply_user_name}</a>(<code>{reply_user_id}</code>) в размере {perevod2}¢
""", parse_mode='html')
          await message.reply(f"💰 • Вы <a href='tg://user?id={user_id}'>{user_name}</a> забрали {perevod2}¢ у игрока <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a> {rwin}", parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance2 - perevod} WHERE user_id = "{reply_user_id}"')
          connect.commit()           
       if user_status[0] == 'Player':
          await message.reply(f"ℹ️ • <a href='tg://user?id={user_id}'>{user_name}</a>, вы не являетесь администратором бота!", parse_mode='html')
          
    if message.text.lower() in ["обнулить д"]:
       msg = message
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])
       reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
       reply_user_name = str(reply_user_name[0])
       win = ['🙂', '😋', '😄', '🤑', '😃']
       rwin = random.choice(win)
       reply_user_id = msg.reply_to_message.from_user.id
       user_id = msg.from_user.id
       user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()

       if not message.reply_to_message:
                await message.reply("Эта команда должна быть ответом на сообщение!")
                return
       if user_status[0] == 'Rab':
          await message.reply(f"💰 • Вы <a href='tg://user?id={user_id}'>{user_name}</a> обнулили деньги игроку <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {0} WHERE user_id = "{reply_user_id}"')
       if user_status[0] == 'Owner':
          await message.reply(f"💰 • Вы <a href='tg://user?id={user_id}'>{user_name}</a> обнулили деньги игроку <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {0} WHERE user_id = "{reply_user_id}"')
       if user_status[0] == 'Helper_Admin':
          await message.reply(f"💰 • Вы <a href='tg://user?id={user_id}'>{user_name}</a> обнулили деньги игроку <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {0} WHERE user_id = "{reply_user_id}"')          
       if user_status[0] == 'Admin':
          await message.reply(f"💰 • Вы <a href='tg://user?id={user_id}'>{user_name}</a> обнулили деньги игроку <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {0} WHERE user_id = "{reply_user_id}"')
          
                    
    if message.text.lower() in ["обнулить рейт"]:
       msg = message
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])
       reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
       reply_user_name = str(reply_user_name[0])
       win = ['🙂', '😋', '😄', '🤑', '😃']
       rwin = random.choice(win)
       reply_user_id = msg.reply_to_message.from_user.id
       user_id = msg.from_user.id
       user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()

       if not message.reply_to_message:
                await message.reply("Эта команда должна быть ответом на сообщение!")
                return
       if user_status[0] == 'Rab':
          await message.reply(f"👑 | Вы <a href='tg://user?id={user_id}'>{user_name}</a> обнулили рейтинг игроку <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')
          cursor.execute(f'UPDATE users SET rating = {0} WHERE user_id = "{reply_user_id}"')
       if user_status[0] == 'Owner':
          await message.reply(f"👑 | Вы <a href='tg://user?id={user_id}'>{user_name}</a> обнулили рейтинг игроку <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')
          cursor.execute(f'UPDATE users SET rating = {0} WHERE user_id = "{reply_user_id}"')
       if user_status[0] == 'Helper_Admin':
          await message.reply(f"👑 | Вы <a href='tg://user?id={user_id}'>{user_name}</a> обнулили рейтинг игроку <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')
          cursor.execute(f'UPDATE users SET rating = {0} WHERE user_id = "{reply_user_id}"')          
       if user_status[0] == 'Admin':
          await message.reply(f"👑 | Вы <a href='tg://user?id={user_id}'>{user_name}</a> обнулили рейтинг игроку <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')
          cursor.execute(f'UPDATE users SET rating = {0} WHERE user_id = "{reply_user_id}"')                                        


    if message.text.startswith("изменить id"):
       msg = message
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
       reply_user_name = reply_user_name[0]
       win = ['🙂', '😋', '😄', '🤑', '😃']
       rwin = random.choice(win)
       reply_user_id = msg.reply_to_message.from_user.id
       user_id = msg.from_user.id
       user_status2 = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()
       newid = int(msg.text.split()[2])
       if user_status2[0] == "Rab":
          await message.reply(f"🔎 | Вы выдали ID - {newid} - игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')
          cursor.execute(f'UPDATE users SET id = \"{newid}\" WHERE user_id = "{reply_user_id}"')
       if user_status2[0] == "Owner":
          await message.reply(f"🔎 | Вы выдали ID - {newid} - игроку: <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')
          cursor.execute(f'UPDATE users SET id = \"{newid}\" WHERE user_id = "{reply_user_id}"') 
          connect.commit()
       if user_status2[0] == 'Player':
          await message.reply(f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, вы не являетесь создателем бота!", parse_mode='html')
       if user_status2[0] == 'Admin':
          await message.reply(f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, вы не являетесь создателем бота!", parse_mode='html')
       if user_status2[0] == 'Helper_Admin':
          await message.reply(f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, вы не являетесь создателем бота!", parse_mode='html')

    if message.text.startswith('Пончик') or message.text.startswith('пончик'):
       user_id = message.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
       reply_user_name = str(reply_user_name[0])

       reply_user_id = msg.reply_to_message.from_user.id

       user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_status = user_status[0]

       donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
       donate_coins = int(donate_coins[0])

       su = msg.text.split()[1]
       su2 = (su).replace(' ', '').replace('k', '000').replace('е','e').replace('к', '000').replace(',', '').replace('.', '')
       su3 = float(su2)
       summ = int(su3)

       if user_status == 'Rab':
          text = f'''
🤵 <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a><b>, вам было начислено <code>{'{:,}'.format(summ).replace(',','.')}</code> пончиков</b> 🍩
          '''
          await bot.send_message(message.chat.id,text, parse_mode='html')
          cursor.execute(f'UPDATE users SET donate_coins = {donate_coins + summ} WHERE user_id = {reply_user_id}')
          connect.commit()
       else:
          pass                    
          

    if message.text.lower() == '+админ':
       user_id = message.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
       reply_user_name = str(reply_user_name[0])

       reply_user_id = msg.reply_to_message.from_user.id

       user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_status = user_status[0]

       if user_status == 'Rab':
          await message.reply(f"🤵 | Создатель: <a href='tg://user?id={user_id}'>{user_name}</a> выдал админ игроку <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')
          cursor.execute(f'UPDATE users SET user_status = "Admin" WHERE user_id = {reply_user_id}')
          connect.commit()
          await bot.send_message(cfg.log_group, f"""⚙️LOG: #выдача статуса
Создатель: <a href="tg://user?id={user_id}">{user_name}</a>(<code>{user_id}</code>) Выдал адм
<a href="tg://user?id={reply_user_id}">{reply_user_name}</a>(<code>{reply_user_id}</code>)
""", parse_mode='html')
       else:
          await message.reply(f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, вы не являетесь создателем бота!")
          
          
    if message.text.lower() == '+хелпер':
       user_id = message.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
       reply_user_name = str(reply_user_name[0])

       reply_user_id = msg.reply_to_message.from_user.id

       user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_status = user_status[0]

       if user_status == 'Rab':
          await message.reply(f"🤵 | Создатель: <a href='tg://user?id={user_id}'>{user_name}</a> выдал хелпера игроку <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')
          cursor.execute(f'UPDATE users SET user_status = "Helper_Admin" WHERE user_id = {reply_user_id}')
          connect.commit()
          await bot.send_message(cfg.log_group, f"""⚙️LOG: #выдача статуса
Создатель: <a href="tg://user?id={user_id}">{user_name}</a>(<code>{user_id}</code>) Выдал хелп
<a href="tg://user?id={reply_user_id}">{reply_user_name}</a>(<code>{reply_user_id}</code>)
""", parse_mode='html')
       else:
          await message.reply(f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, вы не являетесь создателем бота!")


    if message.text.lower() == '+owner':
       user_id = message.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
       reply_user_name = str(reply_user_name[0])

       reply_user_id = msg.reply_to_message.from_user.id

       user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_status = user_status[0]

       if user_status == 'Rab':
          await message.reply(f"🤵 | Создатель: <a href='tg://user?id={user_id}'>{user_name}</a> выдал owner игроку <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')
          cursor.execute(f'UPDATE users SET user_status = "Owner" WHERE user_id = {reply_user_id}')
          connect.commit()
          await bot.send_message(cfg.log_group, f"""⚙️LOG: #выдача статуса
Создатель: <a href="tg://user?id={user_id}">{user_name}</a>(<code>{user_id}</code>) Выдал owner
<a href="tg://user?id={reply_user_id}">{reply_user_name}</a>(<code>{reply_user_id}</code>)
""", parse_mode='html')
       else:
          await message.reply(f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, вы не являетесь создателем бота!")
          

########################################PROMO#########################################
    if message.text.lower() in ['очистить промо', 'reset промо']:
         user_id = message.from_user.id
         user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
         user_name = str(user_name[0])

         user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()
         user_status = str(user_status[0])

         all_promo = cursor.execute(f'SELECT promo from promo').fetchall()

         if user_status == 'Owner':
            cursor.execute(f'DELETE from promo')
            cursor.execute(f'DELETE from promo_active')
            connect.commit()
            all_dell_promo = 0

            for delete_promo in all_promo:
               all_dell_promo += 1
               await message.answer(f'🤖 промокод {delete_promo[0]} был удалён', parse_mode='html')

            await message.reply(f"👾 Всё промокоды были удалены\n🔢 Количество удаленных промокодов: {'{:,}'.format(all_dell_promo).replace(',','.')}")

            
         else:
            return await message.reply(f'🪄 Данная команда доступна от прав администратора <b>OWNER</b>', parse_mode='html')





    if message.text.startswith('промо') or message.text.startswith('Промо') or message.text.startswith('Промокод') or message.text.startswith('промокод'):
         user_id = message.from_user.id
         user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
         user_name = str(user_name[0])

         balance = cursor.execute(f'SELECT balance from users where user_id = {user_id}').fetchone()
         balance = int(balance[0])

         donate_coins = cursor.execute(f'SELECT donate_coins from users where user_id = {user_id}').fetchone()
         donate_coins = int(donate_coins[0])


         all_promo = cursor.execute(f'SELECT promo from promo').fetchall()
         all_promo2 = []

         for item in all_promo:
            all_promo2.append(item[0])



         promo = str(message.text.split()[1])

         if str(promo) in str(all_promo2):
            
            proverka = cursor.execute(f'SELECT active from promo_active where user_id = {user_id} and promo = "{promo}"').fetchone()

            if proverka != None:
               return await message.reply(f'🪄 <b>Вы использовали промокод</b> <code>{promo}</code>', parse_mode='html')
            else:
               pass

            name_promo = cursor.execute(f'SELECT promo from promo where promo = "{promo}"').fetchone()
            name_promo = name_promo[0]

            status_promo = cursor.execute(f'SELECT status from promo where promo = "{promo}"').fetchone()
            status_promo = status_promo[0]

            owner_promo = cursor.execute(f'SELECT owner from promo where promo = "{promo}"').fetchone()
            owner_promo = owner_promo[0]

            priz_promo = cursor.execute(f'SELECT priz from promo where promo = "{promo}"').fetchone()
            priz_promo = int(priz_promo[0])
   
            active_promo = cursor.execute(f'SELECT active from promo where promo = "{promo}"').fetchone()
            active_promo = int(active_promo[0])

            ob_active_promo = cursor.execute(f'SELECT ob_active from promo where promo = "{promo}"').fetchone()
            ob_active_promo = int(ob_active_promo[0])

            if ob_active_promo == active_promo:
               return await message.reply(f'🪄 Промокод больше <b>не действительный</b>', parse_mode='html')
            else:
               pass
            

            if status_promo == 'money':
               priz2 = '{:,}'.format(priz_promo).replace(',', '.')
               priz = f'{priz2}¢'
               new_balance = balance + priz_promo
               new_balance2 = '{:,}'.format(int(new_balance)).replace(',','.')
               update_profile = f'💸 <b>Теперь ваш текущий баланс:</b>  <code>{new_balance2}¢</code>'
               cursor.execute(f'UPDATE promo SET ob_active = {ob_active_promo + 1} WHERE promo = "{promo}"')
               cursor.execute(f'UPDATE users SET balance = {int(new_balance)} where user_id = {user_id}')
               cursor.execute("INSERT INTO promo_active VALUES(?, ?, ?);",(user_id, promo,1))
            elif status_promo == 'donate_coins':
               priz2 = '{:,}'.format(priz_promo).replace(',', '.')
               priz = f'{priz2} 🍩'
               update_profile = ''
               cursor.execute(f'UPDATE promo SET ob_active = {ob_active_promo + 1} WHERE promo = "{promo}"')
               cursor.execute(f'UPDATE users SET donate_coins = {donate_coins + priz_promo} where user_id = {user_id}')
               cursor.execute("INSERT INTO promo_active VALUES(?, ?, ?);",(user_id, promo,1))
            else:
               return await message.reply(f'<b>Error: No status promo in [Money, Donate-Coins, Rub, Donate-Case, Money-Case]</b>', parse_mode='html')
            
            
            text = f'''
👤 <b>Вы успешно использовали промокод <code>{promo}</code></b>
➖➖➖➖➖➖➖➖➖➖➖➖➖
🪄 <b>Получили <code>{priz}</code></b>
➖➖➖➖➖➖➖➖➖➖➖➖➖
👾 <b>Создатель промокода:</b>  <code>{owner_promo}</code>
➖➖➖➖➖➖➖➖➖➖➖➖➖
{update_profile}
            '''

            await message.reply(text, parse_mode='html')
            await bot.send_message(cfg.log_group, f"""⚙️LOG: #промо
Игрок: <a href="tg://user?id={user_id}">{user_name}</a>(<code>{user_id}</code>) использовал промо
🪄 Промокод: <code>{promo}</code>
➖➖➖➖➖➖➖➖➖➖➖➖➖
👾 <b>Создатель промокода:</b>  <code>{owner_promo}</code>
➖➖➖➖➖➖➖➖➖➖➖➖➖
🪄 <b>Получили <code>{priz}</code></b>
""", parse_mode='html')
         else:
            return await message.reply(f'🪄 Нету такого промокода')


    if message.text.startswith('+ред промо'):
      try:
         user_id = message.from_user.id
         user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
         user_name = str(user_name[0])

         if user_id == cfg.owner_id:
            return await message.reply(f'🪄 Данная команда доступна только ред шарку соси лох', parse_mode='html')
         else:
            pass

         new_promo = message.text.split()[2]

         status_promo = int(message.text.split()[3])

         summ_promo = int(message.text.split()[4])

         active_promo = int(message.text.split()[5])

         opis = message.text.split()[6:]

         all_promo = cursor.execute(f'SELECT promo from promo').fetchall()
         all_promo2 = []

         for all_promo3 in all_promo:
            all_promo2.append(all_promo3[0])

         if new_promo in all_promo2:
            return await message.reply(f'🪄 <b>Данный промокод <code>{new_promo}</code> уже существует</b>', parse_mode='html')
         else:
            pass


         if status_promo == 1:
            status = 'donate_coins'
            cursor.execute("INSERT INTO promo VALUES(?, ?, ?, ?, ?, ?);",(new_promo, status, user_name, summ_promo, active_promo, 0))
            text = f'''
🪄 <b>Промокод:</b> <code>{new_promo}</code>
🍩 <b>Содержит: 🍩</b>
👾 <b>Создатель:</b> <code>{user_name}</code>

👥 <b>Количество использований:</b> <code>{active_promo} раз(а)</code>
👤<b> На одного человека:</b> <code>{summ_promo} 🍩</code>
            '''

         else:
            text = f'''
❗️ Неправильно ведены аргументы | пример: <code>+ред промо</code> <i>[название промокода] [номер статуса] [сумма на 1 человека]</i>  [количество активаций] 

❕ Номера статусов:
      1 - пончики
         '''
            return await message.reply(text, parse_mode='html')
      
         await message.reply(text, parse_mode='html')

      except IndexError:
         text = f'''
❗️ Неправильно ведены аргументы | пример: <code>+ред промо</code> <i>[название промокода] [номер статуса] [сумма на 1 человека]</i>  [количество активаций] 

❕ Номера статусов:
      1 - пончики
         '''
         await message.reply(text, parse_mode='html')


      except ValueError:
         text = f'''
❗️ Неправильно ведены аргументы | пример: <code>+ред промо</code> <i>[название промокода] [номер статуса] [сумма на 1 человека]</i>  [количество активаций] 

❕ Номера статусов:
      1 - пончики
         '''
         await message.reply(text, parse_mode='html')




    if message.text.startswith('создать промо') or message.text.startswith('Создать промо') or message.text.startswith('+Промо') or message.text.startswith('+промо'):
      try:
         user_id = message.from_user.id
         user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
         user_name = str(user_name[0])

         balance = cursor.execute(f'SELECT balance from users where user_id = {user_id}').fetchone()
         balance = int(balance[0])
      
         user_status = cursor.execute(f'SELECT user_status from users where user_id = {user_id}').fetchone()
         user_status = user_status[0]

         all_promo = cursor.execute(f'SELECT promo from promo').fetchall()
         all_promo2 = []

         for all_promo3 in all_promo:
            all_promo2.append(all_promo3[0])
         new_promo = str(message.text.split()[1])

         su1 = message.text.split()[2]
         su2 = (su1).replace('.', '').replace(',', '').replace('е',' e').replace("к", 'k').replace('k', '000').replace('все', 'всё')
         su3 = float(su2)
         summ = int(su3)

         su1_2 = message.text.split()[3]
         su2_2 = (su1_2).replace('.', '').replace(',', '').replace('е',' e').replace("к", 'k').replace('k', '000')
         su3_2 = float(su2_2)
         active_users = int(su3_2)

         opis = message.text.split()[4:]

         if summ < 0:
            return await message.reply(f'❗️ Cумма должна быть не меньше <code>0¢</code>', parse_mode='html')
         else:
            pass

         if active_users > 1000000:
            return await message.reply(f'❗️ Вы не можете создать промокод больше чем на <b>1000000 использований</b>', parse_mode='html')
         else:
            pass
         
         if len(new_promo) < 3:
            return await message.reply(f'❗️ Промокод должен быть <b>больше 3 символов</b>', parse_mode='html')
         else:
            pass

         if new_promo in all_promo2:
            return await message.reply(f'❗️ <b>Данный промокод <code>{new_promo}</code> уже существует</b>', parse_mode='html')
         else:
            pass
         
         if summ > balance:
            return await message.reply(f'❗️ У вас <b>недостаточно средств</b>', parse_mode='html')
         else:
            pass

         if summ <= 0:
            return await message.reply(f'❗️ Сумма не должна быть отрицательным числом <b>[0 и меньше]</b>', parse_mode='html')
         else:
            pass
         
         user_summ = summ / active_users
         user_summ2 = int(user_summ)         

         text_opis = ' '.join(opis)

         if text_opis == '':
            opis2 = ''
         else:
            text_opis = ' '.join(opis)
            opis2 = f'<b>💭 Описание:</b> <code>{text_opis}</code>'

         text = f'''
🪄 Промокод: <code>{new_promo}</code>
➖➖➖➖➖➖➖➖➖➖➖➖➖
💰 Сумма: <code>{'{:,}'.format(summ).replace(',', '.')}¢</code>
➖➖➖➖➖➖➖➖➖➖➖➖➖
👾 Создатель: <code>{user_name}</code>
➖➖➖➖➖➖➖➖➖➖➖➖➖
👤 Активаций: <code>{active_users}</code>
👤 На одного человека: <code>{'{:,}'.format(user_summ2).replace(',', '.')}¢</code>
{opis2}
         '''

         if user_status in []:
            await message.reply('❗️ Администрации запрещено создавать промокоды')

            await message.bot.send_message(cfg.log_group, f'⛔️ Администратор <b>{user_name}</b> (<code>{user_id}</code>) только что попытался создать промокод.')
            return await message.bot.send_message(cfg.log_group, text, parse_mode='html')
            await message.bot.send_message(cfg.log_group, f"""⚙️LOG: #промо
Игрок: <a href="tg://user?id={user_id}">{user_name}</a>(<code>{user_id}</code>) создал промо
🪄 Промокод: <code>{new_promo}</code>
➖➖➖➖➖➖➖➖➖➖➖➖➖
💰 Сумма: <code>{'{:,}'.format(summ).replace(',', '.')}¢</code>
➖➖➖➖➖➖➖➖➖➖➖➖➖
👾 Создатель: <code>{user_name}</code>
➖➖➖➖➖➖➖➖➖➖➖➖➖
👤 Активаций: <code>{active_users}</code>
👤 На одного человека: <code>{'{:,}'.format(user_summ2).replace(',', '.')}¢</code>
{opis2}
""", parse_mode='html')
         else:
            pass
            
            
         status = 'money'
         try:
            cursor.execute("INSERT INTO promo VALUES(?, ?, ?, ?, ?, ?);",(new_promo, status, user_name, user_summ2, active_users, 0))
            cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
            connect.commit()
            await message.reply(text, parse_mode='html')
         except OverflowError:
            cursor.execute("INSERT INTO promo VALUES(?, ?, ?, ?, ?, ?);",(new_promo, status, user_name, 0, active_users, 0))
            cursor.execute(f'UPDATE promo SET priz = {user_summ2} WHERE promo = "{new_promo}"')
            cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
            connect.commit()
            await message.reply(text, parse_mode='html')
      except IndexError:
         text = f'''
❗️ Неправильно введены <b>аргументы!</b>
❕ <code>Создать промо</code> <b>[название] [сумма] [количество использований]</b>
❕ <code>+промо</code> <b>[название] [сумма] [количество использований]</b>
         '''
         await message.reply(text, parse_mode='html')

      except ValueError:
         text = f'''
❗️ Неправильно введены <b>аргументы!</b>
❕ <code>Создать промо</code> <b>[название] [сумма] [количество использований]</b>
❕ <code>+промо</code> <b>[название] [сумма] [количество использований]</b>
         '''
         await message.reply(text, parse_mode='html')
         

###########################################ПОМОЩЬ###########################################
    if message.text.lower().startswith("помощь"):
       user_id = message.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       help2 = InlineKeyboardMarkup(row_width=2)
       Osn2 = InlineKeyboardButton(text='💡 Основное', callback_data='Osn2')
       game2 = InlineKeyboardButton(text='🎮 Игры', callback_data='game2')
       Im2 = InlineKeyboardButton(text='🏘 Дом', callback_data='Im2')
       Osn = InlineKeyboardButton(text='❕Остальное', callback_data='ostal_menu')
       ded2 = InlineKeyboardButton(text='➡️ Дальше', callback_data='ded2')
       help2.add(Osn2, game2, Im2, Osn, ded2)

       await bot.send_message(message.chat.id, f'''
➖➖➖➖➖➖➖➖➖➖➖
📊 Канал - {cfg.channel}
💭 Чат - {cfg.chat}
❗️ По всем вопросам - {cfg.owner}
➖➖➖➖➖➖➖➖➖➖➖
🔎 Категории
├ 💡 Основное
├ 🎮 Игры
├ 🏘 Дом
└ ❕ Остальное
➖➖➖➖➖➖➖➖➖➖
Выберите одну кнопку ниже👇🏻
    ''', reply_markup=help2, disable_web_page_preview=True, parse_mode='html')
   

##################################################ДАЙК############################################

    if message.text.lower().startswith('дайк'):
      try:
         msg = message
         user_id = msg.from_user.id
         games = cursor.execute("SELECT game from users where user_id = ?", (message.from_user.id,)).fetchone()
         games = int(games[0])

         user_name = cursor.execute("SELECT user_name from users where user_id = ?", (message.from_user.id,)).fetchone()
         user_name = str(user_name[0])

         user_status = cursor.execute("SELECT user_status from users where user_id = ?", (message.from_user.id,)).fetchone()
         user_status = str(user_status[0])

         su = msg.text.split()[1]
         su2 = (su).replace(' ', '').replace('k', '000').replace('е','e').replace('к', '000').replace(',', '').replace('.', '').replace('$', '').replace('м', '000000').replace('все', '{balance}').replace('всё', '{balance}')
         su3 = float(su2)
         summ = int(su3)

         summ2 = '{:,}'.format(summ).replace(',', '.')
         
         ore = str(msg.text.split()[2])


         balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
         balance = round(int(balance[0]))
         player = status_users(message.from_user.id)
         

         if user_status in ['Vlaselin', 'Bog']:
            period = 2
            tp = 'секунды'
         elif user_status in ['Admin', 'Helper_Admin', 'Owner']:
            period = 1
            tp = 'секунду'
         else:
            period = 5
            tp = 'секунд'



         get = cursor.execute("SELECT stavka_games FROM bot_time WHERE user_id = ?", (message.from_user.id,)).fetchone()
         last_stavka = f"{int(get[0])}"
         stavkatime = time.time() - float(last_stavka)

         if stavkatime < period:
            return await message.reply(f'❗️ Играть можно раз в <b>{period} {tp}</b>', parse_mode='html')
         else:
            pass
         
         if balance < summ:
            return await message.reply(f'❗️ У вас <b>недостаточно средств</b>', parse_mode='html')
         else:
            pass
         
         if summ <= 0:
            return await message.reply('❗️ Ставка не может быть отрицательным числом <b>[0 и меньше]</b>', parse_mode='html')
         else:
            pass





         if ore in ["к", "К"]:
            r = random.randint(0, 101)
            
            if r in range(0, 50):
               stavka = int(summ * 0)
               stavka2 = '{:,}'.format(stavka).replace(',', '.')
               await message.reply(f"""{player} ➪ <a href="tg://user?id={user_id}">{user_name}</a>
🎱 Игра: Дайк
🗒 Проигрыш: -{stavka2}¢
🎲 Выпала система [В]""", parse_mode='html')
               cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
               cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
               cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
               connect.commit()



            if r in range(51, 101):
               
               stavka = int(summ * 2)
               stavka2 = '{:,}'.format(stavka).replace(',', '.')
               
               await message.reply(f"""{player} ➪ <a href="tg://user?id={user_id}">{user_name}</a>
🎱 Игра: Дайк
🧾 Выигрыш: +{stavka2}¢
🎲 Выпала система [К]""", parse_mode='html')
               cursor.execute(f'UPDATE users SET balance = {(balance - summ) + (summ * 2)} WHERE user_id = {user_id}')
               cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
               cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
               connect.commit()
         




         if ore in ["в", "В"]:
            r = random.randint(0, 101)
            
            if r in range(0, 50):
               stavka = int(summ * 0)
               stavka2 = '{:,}'.format(stavka).replace(',', '.')
               await message.reply(f"""{player} ➪ <a href="tg://user?id={user_id}">{user_name}</a>
🎱 Игра: Дайк
🧾 Проигрыш: -{stavka2}¢
🎲 Выпала система [К]""", parse_mode='html')
               cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
               cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
               cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
               connect.commit()



            if r in range(51, 101):
               
               stavka = int(summ * 2)
               stavka2 = '{:,}'.format(stavka).replace(',', '.')
               
               await message.reply(f"""{player} ➪ <a href="tg://user?id={user_id}">{user_name}</a>
🎱 Игра: Дайк
🗒 Выигрыш: +{stavka2}¢
🎲 Выпала система [В]""", parse_mode='html')
               cursor.execute(f'UPDATE users SET balance = {(balance - summ) + (summ * 2)} WHERE user_id = {user_id}')
               cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
               cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
               connect.commit()
      
      except IndexError:
         return await message.reply(f'❗️ <b>Вы не ввели сумму ставки, либо же то, на что хотите поставить - </b> <code>дайк 10к [к/в]</code> ', parse_mode='html')
      except ValueError:
         return await message.reply(f'❗️ <b>Не правильно введены аргументы - <code>дайк [сумма] [к/в]</code></b>', parse_mode='html')
          

##################################################КАЗИНО############################################
    if message.text.lower().startswith("отменить ставку"):
       user_id = message.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?", (user_id,))
       user_name = cursor.fetchone()
       user_name = user_name[0]
       
       user_id = message.from_user.id
       
       user_name = cursor.execute("SELECT user_name from users where user_id = ?", (user_id,))
       user_name = cursor.fetchone()
       user_name = user_name[0]
       data = await get_rang(message)
       if data[56] == 1:

           cursor.execute("UPDATE users SET stavka WHERE user_id=?",(user_id,))
           second_p.clear()
           first_p.clear()
           summ_stavka.clear()
           second_p.clear()
           return await message.reply(f"‼️ <a href='tg://user?id={user_id}'>{user_name}</a> Вы успешно отменили ставку", parse_mode='html')
       else:
           return await message.reply(f"‼️   <a href='tg://user?id={user_id}'>{user_name}</a> У вас нету активной ставки!", parse_mode='html')                       
                                                                        
                                                                           
    if message.text.lower().startswith("казино"):
       data = await get_rang(message)          
       if data is None:
           return await message.reply(f"🚫 <b>Не найден в базе данных.</b>\n\n"
                            f"/start в лс у бота!")
       user_id = message.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?", (user_id,))
       user_name = cursor.fetchone()
       user_name = user_name[0]
       reply = message.reply_to_message
       if reply:           
           replyuser = reply.from_user.id
           ruser_name = cursor.execute("SELECT user_name from users where user_id = ?", (replyuser,))
           ruser_name = cursor.fetchone()
           ruser_name = ruser_name[0]
           
           if data[36] == 0:
               if replyuser == user_id:         
                   return await message.reply(f"‼️Вы не можете играть с собой.")
               replydata = await reply_get_rang(message)
               if replydata[36] == 0:
                   try:
                       su = msg.text.split()[1]
                       su2 = (su).replace('к', '000')
                       su3 = (su2).replace('м', '000000')
                       su4 = (su3).replace('.', '')
                       su5 = float(su4)
                       summ = int(su5)
                       
                       summ2 = '{:,}'.format(summ).replace(',', '.')
                   except:
                       await message.reply('‼️Неправильный ввод команды!\nПример: Казино 1')
                       return
                                                
                   balance = cursor.execute("SELECT balance FROM users WHERE user_id=?", (user_id,))
                   balance = cursor.fetchone()
                   balance = int(balance[0])
                    
                   balance2 = cursor.execute("SELECT balance FROM users WHERE user_id=?", (replyuser,))
                   balance2 = cursor.fetchone()
                   balance2 = int(balance2[0])
                   player=status_users(user_id)
                   player2=status_users(replyuser)
                    
                   if balance >= summ and balance2 >= summ:
                       if summ > 0:
                        	cursor.execute("UPDATE users SET stavka=1 WHERE user_id=?",(user_id,))
                        	cursor.execute("UPDATE users SET stavka=1 WHERE user_id=?", (replyuser,))
                        	first_p.append(user_id)
                        	summ_stavka.append(summ)
                        	second_p.append(replyuser)
                        	
                        	await bot.send_message(message.chat.id,f"🎰 {player2} ➪ <a href='tg://user?id={replyuser}'>{ruser_name}</a>, вам пришла ставка от {player} ➪ <a href='tg://user?id={user_id}'>{user_name}</a> на {summ2}¢", reply_markup=gamestavka, parse_mode='html')

###########################################СПИН#############################################
    if message.text.lower().startswith("спин"):
        balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
        balance = int(balance[0])
        games = cursor.execute("SELECT game from users where user_id = ?", (message.from_user.id,)).fetchone()
        games = int(games[0])

        balance2 = '{:,}'.format(balance).replace(',', '.')
        msg = message
        user_id = msg.from_user.id
        chat_id = message.chat.id
        win = ['🙂', '😋', '😄', '🤑', '😃']
        loser = ['😔', '😕', '😣', '😞', '😢']
        rwin = random.choice(win)
        rloser = random.choice(loser)
        msg = message
        user_name = cursor.execute("SELECT user_name from users where user_id = ?", (message.from_user.id,)).fetchone()
        user_name = str(user_name[0])

        user_status = cursor.execute("SELECT user_status from users where user_id = ?", (message.from_user.id,)).fetchone()
        user_status = str(user_status[0])

        name = msg.from_user.full_name
        su = msg.text.split()[1]
        su2 = (su).replace(' ', '').replace('k', '000').replace('е','e').replace('к', '000').replace(',', '').replace('.', '')
        su3 = float(su2)
        summ = int(su3)

        summ2 = '{:,}'.format(summ).replace(',', '.')
        balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
        balance = round(int(balance[0]))

        period = 5
         
        get = cursor.execute("SELECT stavka_games FROM bot_time WHERE user_id = ?", (message.from_user.id,)).fetchone()
        last_stavka = f"{int(get[0])}"
        stavkatime = time.time() - float(last_stavka)
        if stavkatime > period:
            if balance >= summ:
                if summ > 0:
                    rx1 = await message.reply_dice(emoji="🎰")
                    rx = rx1.dice.value
                    if int(rx) in range(0, 38):
                        c = Decimal(summ * 0)
                        c2 = round(c)
                        c2 = '{:,}'.format(c2).replace(',', '.')

                        await bot.send_message(chat_id,
                                               f"<a href='tg://user?id={user_id}'>{user_name}</a>, ваша ствака умножилась на x0\n🎟️ Вы проиграли -{summ2}¢ {rloser}",
                                               parse_mode='html')
                        cursor.execute(
                            f'UPDATE users SET balance = {(balance - summ) + (summ * 0)} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE bot_time SET stavka_games=? WHERE user_id=?', (time.time(), user_id,))
                        connect.commit()
                        return

        if stavkatime > period:
            if balance >= summ:
                if summ > 0:
                    if int(rx) in range(38,60):
                        c = Decimal(summ * 1.25)
                        c2 = round(c)
                        c2 = '{:,}'.format(c2).replace(',', '.')
                        await bot.send_message(chat_id,
                                               f"<a href='tg://user?id={user_id}'>{user_name}</a>, ваша ствака умножилась на x1.25\n🏅 Выигрыш: {rwin} - {c2}¢",
                                               parse_mode='html')
                        cursor.execute(
                            f'UPDATE users SET balance = {(balance - summ) + (summ * 1.25)} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE bot_time SET stavka_games=? WHERE user_id=?', (time.time(), user_id,))
                        connect.commit()
                        return
        if stavkatime > period:
            if balance >= summ:
                if summ > 0:
                    if int(rx) in range(60, 64):
                        c = Decimal(summ * 2)
                        c2 = round(c)
                        c2 = '{:,}'.format(c2).replace(',', '.')
                        await bot.send_message(chat_id,
                                               f"<a href='tg://user?id={user_id}'>{user_name}</a>, ваша ствака умножилась на x2\n🏅 Выигрыш: {rwin} - {c2}¢",
                                               parse_mode='html')
                        cursor.execute(
                            f'UPDATE users SET balance = {(balance - summ) + (summ * 2)} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE bot_time SET stavka_games=? WHERE user_id=?', (time.time(), user_id,))
                        connect.commit()
                        return                        
        if stavkatime > period:
            if balance >= summ:
                if summ > 0:
                    if int(rx) ==64:
                        c = Decimal(summ * 5)
                        c2 = round(c)
                        c2 = '{:,}'.format(c2).replace(',', '.')
                        await bot.send_message(chat_id,
                                               f"<a href='tg://user?id={user_id}'>{user_name}</a>, ваша ствака умножилась на x5\n🏅 Выйгрыш составляет: +{c2}¢ {rwin}",
                                               parse_mode='html')
                        cursor.execute(
                            f'UPDATE users SET balance = {(balance - summ) + (summ * 5)} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = "{user_id}"')
                        cursor.execute(f'UPDATE bot_time SET stavka_games=? WHERE user_id=?', (time.time(), user_id,))
                        connect.commit()
                        return
                elif summ <= 1:
                    await bot.send_message(chat_id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, нельзя ставить отрицательное число! {rloser}",
                                           parse_mode='html')
            elif int(balance) <= int(summ):
                await bot.send_message(chat_id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств! {rloser}", parse_mode='html')
        else:
            await bot.send_message(chat_id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, извини. но играть можно только каждые {period} секунд. {rloser}",
                                       parse_mode='html')


########################################ДАРТС################################################    
    if message.text.lower().startswith('дартс'):
       msg = message
       user_id = msg.from_user.id
       chat_id = message.chat.id

       win = ['🙂', '😋', '😄', '🤑', '😃']
       loser = ['😔', '😕', '😣', '😞', '😢']
       rand = random.randint(1,6)
       rwin = random.choice(win)
       rloser = random.choice(loser)

       msg = message
       name1 = message.from_user.get_mention(as_html=True)
       name = msg.from_user.last_name
       su = msg.text.split()[1]
       su2 = (su).replace(' ', '').replace('k', '000').replace('е','e').replace('к', '000').replace(',', '').replace('.', '').replace("$", "").replace('м', '000000').replace('m', '000000')
       su3 = float(su2)
       summ = int(su3)
       games = cursor.execute("SELECT game from users where user_id = ?", (message.from_user.id,)).fetchone()
       games = int(games[0])
       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = round(int(balance[0]))
       period = 5
       get = cursor.execute("SELECT stavka_games FROM bot_time WHERE user_id = ?", (message.from_user.id,)).fetchone()
       last_stavka = f"{int(get[0])}"
       stavkatime = time.time() - float(last_stavka)
       if stavkatime > period:
          if balance >= summ:
             if summ > 0:
                rx1 = await message.reply_dice(emoji="🎯")
                rx = rx1.dice.value
                if int(rx) == 1:
                    c = Decimal(summ * 0)
                    c2 = round(c)
                    c2 = '{:,}'.format(c2).replace(',', '.')
                    await bot.send_message(chat_id, f'<a href="tg://user?id={user_id}">{user_name}</a>, мимо цели\n🎟️ Вы проиграли: {c2}¢',
                                                   parse_mode='html')
                    cursor.execute(f'UPDATE users SET balance = {(balance - summ) + (summ * 0)} WHERE user_id = {user_id}')
                    cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                    cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')            
                    connect.commit()
                    return
                if int(rx) == 2:
                    c = Decimal(summ * 0)
                    c2 = round(c)
                    c2 = '{:,}'.format(c2).replace(',', '.')
                    await bot.send_message(chat_id, f'<a href="tg://user?id={user_id}">{user_name}</a>, мимо!\n🎟️ Вы проиграли: {c2}¢ {rloser}',
                                                   parse_mode='html')
                    cursor.execute(f'UPDATE users SET balance = {(balance - summ) + (summ * 0)} WHERE user_id = {user_id}')
                    cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                    cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                    connect.commit()
                    return
                if int(rx) == 3:
                    c = Decimal(summ * 0.5)
                    c2 = round(c)
                    c2 = '{:,}'.format(c2).replace(',', '.')
                    await bot.send_message(chat_id, f'<a href="tg://user?id={user_id}">{user_name}</a>, еще немного!\n🎟️ Вы проиграли: {c2}¢',
                                                   parse_mode='html')
                    cursor.execute(f'UPDATE users SET balance = {(balance - summ) + (summ * 0.5)} WHERE user_id = {user_id}')
                    cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                    cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                    connect.commit()
                    return
                if int(rx) == 4:
                    c = Decimal(summ * 1)
                    c2 = round(c)
                    c2 = '{:,}'.format(c2).replace(',', '.')
                    await bot.send_message(chat_id, f'<a href="tg://user?id={user_id}">{user_name}</a>, очень близко!\n🎟 Ваши деньги остаются при вас',
                                                   parse_mode='html')
                    cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                    cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                    connect.commit()
                    return
                if int(rx) == 5:
                    c = Decimal(summ * 1.5)
                    c2 = round(c)
                    c2 = '{:,}'.format(c2).replace(',', '.')
                    await bot.send_message(chat_id, f':<a href="tg://user?id={user_id}">{user_name}</a>, Почти в цель!\n🎟 Вы выиграли: {c2}¢',
                                                   parse_mode='html')
                    cursor.execute(f'UPDATE users SET balance = {(balance - summ) + (summ * 1.5)} WHERE user_id = {user_id}')
                    cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                    cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                    connect.commit()
                    return
                if int(rx) == 6:
                    c = Decimal(summ * 3)
                    c2 = round(c)
                    c2 = '{:,}'.format(c2).replace(',', '.')
                    await bot.send_message(chat_id, f':<a href="tg://user?id={user_id}">{user_name}</a>, Точно в цель!!!\n🎟 Выигрыш составляет: {c2}¢',
                                                   parse_mode='html')
                    cursor.execute(f'UPDATE users SET balance = {(balance - summ) + (summ * 3)} WHERE user_id = {user_id}')
                    cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                    cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                    connect.commit()             
             
             else:
                await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, нельзя ставить отрицательное число", parse_mode='html')     
          else:
             await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас нехватает средств", parse_mode='html')     
       else:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, играть можно раз в 5 секунд", parse_mode='html')


########################################БАСКЕТБОЛ################################################    
    if message.text.lower().startswith('баскетбол'):
       msg = message
       user_id = msg.from_user.id
       chat_id = message.chat.id

       win = ['🙂', '😋', '😄', '🤑', '😃']
       loser = ['😔', '😕', '😣', '😞', '😢']
       rand = random.randint(1,6)
       rwin = random.choice(win)
       rloser = random.choice(loser)

       msg = message
       name1 = message.from_user.get_mention(as_html=True)
       name = msg.from_user.last_name
       su = msg.text.split()[1]
       su2 = (su).replace(' ', '').replace('k', '000').replace('е','e').replace('к', '000').replace(',', '').replace('.', '').replace("$", "").replace('м', '000000').replace('m', '000000')
       su3 = float(su2)
       summ = int(su3)
       games = cursor.execute("SELECT game from users where user_id = ?", (message.from_user.id,)).fetchone()
       games = int(games[0])
       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = round(int(balance[0]))
       period = 5
       get = cursor.execute("SELECT stavka_games FROM bot_time WHERE user_id = ?", (message.from_user.id,)).fetchone()
       last_stavka = f"{int(get[0])}"
       stavkatime = time.time() - float(last_stavka)
       if stavkatime > period:
          if balance >= summ:
             if summ > 0:
                rx1 = await message.reply_dice(emoji="🏀")
                rx = rx1.dice.value
                if int(rx) == 1:
                    c = Decimal(summ * 2)
                    c2 = round(c)
                    c2 = '{:,}'.format(c2).replace(',', '.')
                    await bot.send_message(chat_id, f'<a href="tg://user?id={user_id}">{user_name}</a>, невероятно,мяч в кольце\n🏅 Выйгрыш составляет: +{c2}¢',
                                                   parse_mode='html')
                    cursor.execute(f'UPDATE users SET balance = {(balance - summ) + (summ * 2)} WHERE user_id = {user_id}')
                    cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                    cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')            
                    connect.commit()
                    return
                if int(rx) == 2:
                    c = Decimal(summ * 0)
                    c2 = round(c)
                    c2 = '{:,}'.format(c2).replace(',', '.')
                    await bot.send_message(chat_id, f'<a href="tg://user?id={user_id}">{user_name}</a>, Судья не засчитал!\n🎫 Вы проиграли: -{c2}¢',
                                                   parse_mode='html')
                    cursor.execute(f'UPDATE users SET balance = {(balance - summ) + (summ * 0)} WHERE user_id = {user_id}')
                    cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                    cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                    connect.commit()
                    return
                if int(rx) == 3:
                    c = Decimal(summ * 0.5)
                    c2 = round(c)
                    c2 = '{:,}'.format(c2).replace(',', '.')
                    await bot.send_message(chat_id, f'<a href="tg://user?id={user_id}">{user_name}</a>, мяч не попал в кольцо!\n🎫 Вы проиграли: -{c2}¢',
                                                   parse_mode='html')
                    cursor.execute(f'UPDATE users SET balance = {(balance - summ) + (summ * 0.5)} WHERE user_id = {user_id}')
                    cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                    cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                    connect.commit()
                    return
                if int(rx) == 4:
                    c = Decimal(summ * 1)
                    c2 = round(c)
                    c2 = '{:,}'.format(c2).replace(',', '.')
                    await bot.send_message(chat_id, f'<a href="tg://user?id={user_id}">{user_name}</a>, очень близко кольцо!\n🎫 Ваши деньги остаются при вас',
                                                   parse_mode='html')
                    cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                    cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                    connect.commit()
                    return
                if int(rx) == 5:
                    c = Decimal(summ * 1.5)
                    c2 = round(c)
                    c2 = '{:,}'.format(c2).replace(',', '.')
                    await bot.send_message(chat_id, f':<a href="tg://user?id={user_id}">{user_name}</a>, Судья не увидел и засчитал!!\n🎫 Вы выиграли: {c2}¢',
                                                   parse_mode='html')
                    cursor.execute(f'UPDATE users SET balance = {(balance - summ) + (summ * 1.5)} WHERE user_id = {user_id}')
                    cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                    cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                    connect.commit()
                    return
                if int(rx) == 6:
                    c = Decimal(summ * 3)
                    c2 = round(c)
                    c2 = '{:,}'.format(c2).replace(',', '.')
                    await bot.send_message(chat_id, f':<a href="tg://user?id={user_id}">{user_name}</a>, невероятно,мяч в кольце\n🏅 Выйгрыш составляет: +{c2}¢',
                                                   parse_mode='html')
                    cursor.execute(f'UPDATE users SET balance = {(balance - summ) + (summ * 3)} WHERE user_id = {user_id}')
                    cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                    cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                    connect.commit()             
             
             else:
                await bot.send_message(message.chat.id, f"🏀 | <a href='tg://user?id={user_id}'>{user_name}</a>, нельзя ставить отрицательное число", parse_mode='html')     
          else:
             await bot.send_message(message.chat.id, f"🏀 | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас нехватает средств", parse_mode='html')     
       else:
          await bot.send_message(message.chat.id, f"🏀 | <a href='tg://user?id={user_id}'>{user_name}</a>, играть можно раз в 5 секунд", parse_mode='html')
                    

#################################################### ФУТБОЛ ########################################
    if message.text.lower().startswith('футбол'):
       msg = message
       user_id = msg.from_user.id
       chat_id = message.chat.id

       win = ['🙂', '😋', '😄', '🤑', '😃']
       loser = ['😔', '😕', '😣', '😞', '😢']
       rand = random.randint(1,6)
       rwin = random.choice(win)
       rloser = random.choice(loser)

       msg = message
       name1 = message.from_user.get_mention(as_html=True)
       name = msg.from_user.last_name
       su = msg.text.split()[1]
       su2 = (su).replace(' ', '').replace('k', '000').replace('е','e').replace('к', '000').replace(',', '').replace('.', '').replace("$", "").replace('м', '000000').replace('m', '000000')
       su3 = float(su2)
       summ = int(su3)
       games = cursor.execute("SELECT game from users where user_id = ?", (message.from_user.id,)).fetchone()
       games = int(games[0])
       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = round(int(balance[0]))
       period = 5
       get = cursor.execute("SELECT stavka_games FROM bot_time WHERE user_id = ?", (message.from_user.id,)).fetchone()
       last_stavka = f"{int(get[0])}"
       stavkatime = time.time() - float(last_stavka)
       if stavkatime > period:
          if balance >= summ:
             if summ > 0:
                rx1 = await message.reply_dice(emoji="⚽")
                rx = rx1.dice.value
                if int(rx) == 1:
                    c = Decimal(summ * 2)
                    c2 = round(c)
                    c2 = '{:,}'.format(c2).replace(',', '.')
                    await bot.send_message(chat_id, f'<a href="tg://user?id={user_id}">{user_name}</a>, невероятно,мяч в воротах\n🏅 Выйгрыш составляет: +{c2}¢',
                                                   parse_mode='html')
                    cursor.execute(f'UPDATE users SET balance = {(balance - summ) + (summ * 2)} WHERE user_id = {user_id}')
                    cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                    cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')            
                    connect.commit()
                    return
                if int(rx) == 2:
                    c = Decimal(summ * 0)
                    c2 = round(c)
                    c2 = '{:,}'.format(c2).replace(',', '.')
                    await bot.send_message(chat_id, f'<a href="tg://user?id={user_id}">{user_name}</a>, Судья не засчитал!\n🎫 Вы проиграли: -{c2}¢',
                                                   parse_mode='html')
                    cursor.execute(f'UPDATE users SET balance = {(balance - summ) + (summ * 0)} WHERE user_id = {user_id}')
                    cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                    cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                    connect.commit()
                    return
                if int(rx) == 3:
                    c = Decimal(summ * 0.5)
                    c2 = round(c)
                    c2 = '{:,}'.format(c2).replace(',', '.')
                    await bot.send_message(chat_id, f'<a href="tg://user?id={user_id}">{user_name}</a>, мяч не попал в воротах!\n🎫 Вы проиграли: -{c2}¢',
                                                   parse_mode='html')
                    cursor.execute(f'UPDATE users SET balance = {(balance - summ) + (summ * 0.5)} WHERE user_id = {user_id}')
                    cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                    cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                    connect.commit()
                    return
                if int(rx) == 4:
                    c = Decimal(summ * 1)
                    c2 = round(c)
                    c2 = '{:,}'.format(c2).replace(',', '.')
                    await bot.send_message(chat_id, f'<a href="tg://user?id={user_id}">{user_name}</a>, очень близко!\n🎫 Ваши деньги остаются при вас',
                                                   parse_mode='html')
                    cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                    cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                    connect.commit()
                    return
                if int(rx) == 5:
                    c = Decimal(summ * 1.5)
                    c2 = round(c)
                    c2 = '{:,}'.format(c2).replace(',', '.')
                    await bot.send_message(chat_id, f':<a href="tg://user?id={user_id}">{user_name}</a>, Судья не увидел и засчитал!!\n🎫 Вы выиграли: {c2}¢',
                                                   parse_mode='html')
                    cursor.execute(f'UPDATE users SET balance = {(balance - summ) + (summ * 1.5)} WHERE user_id = {user_id}')
                    cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                    cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                    connect.commit()
                    return
                if int(rx) == 6:
                    c = Decimal(summ * 3)
                    c2 = round(c)
                    c2 = '{:,}'.format(c2).replace(',', '.')
                    await bot.send_message(chat_id, f':<a href="tg://user?id={user_id}">{user_name}</a>, невероятно,мяч в девятке!\n🏅 Выйгрыш составляет: +{c2}¢',
                                                   parse_mode='html')
                    cursor.execute(f'UPDATE users SET balance = {(balance - summ) + (summ * 3)} WHERE user_id = {user_id}')
                    cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                    cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                    connect.commit()             
             
             else:
                await bot.send_message(message.chat.id, f"⚽ | <a href='tg://user?id={user_id}'>{user_name}</a>, нельзя ставить отрицательное число", parse_mode='html')     
          else:
             await bot.send_message(message.chat.id, f"⚽ | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас нехватает средств", parse_mode='html')     
       else:
          await bot.send_message(message.chat.id, f"⚽ | <a href='tg://user?id={user_id}'>{user_name}</a>, играть можно раз в 5 секунд", parse_mode='html')
              
                            
##################################################Бой############################################
    
    if message.text.lower().startswith("бой"):
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       pet1 = cursor.execute("SELECT pet1 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet1 = int(pet1[0])
       pet2 = cursor.execute("SELECT pet2 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet2 = int(pet2[0])
       pet3 = cursor.execute("SELECT pet3 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet3 = int(pet3[0])
       pet4 = cursor.execute("SELECT pet4 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet4 = int(pet4[0])
       pet5 = cursor.execute("SELECT pet5 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet5 = int(pet5[0])
       pet6 = cursor.execute("SELECT pet6 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet6 = int(pet6[0])
       pet7 = cursor.execute("SELECT pet7 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet7 = int(pet7[0])
       pet8 = cursor.execute("SELECT pet8 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet8 = int(pet8[0])
       pet9 = cursor.execute("SELECT pet9 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet9 = int(pet9[0])
       pet10 = cursor.execute("SELECT pet10 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet10 = int(pet10[0])
       pet11 = cursor.execute("SELECT pet11 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet11 = int(pet11[0])
       pet_name = cursor.execute("SELECT pet_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet_name = str(pet_name[0])
       pet_hp = cursor.execute("SELECT pet_hp from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet_hp = int(pet_hp[0])
       pet_eat = cursor.execute("SELECT pet_eat from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet_eat = int(pet_eat[0])
       pet_mood = cursor.execute("SELECT pet_mood from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet_mood = int(pet_mood[0])
       chat_id = message.chat.id
       user_id = message.from_user.id
       loser = ['😔', '😕', '😣', '😞', '😢']
       rloser = random.choice(loser)
       
       balance = cursor.execute("SELECT balance from users where user_id = ?",(message.from_user.id,)).fetchone()
       balance = round(int(balance[0]))

       checking1 = cursor.execute("SELECT checking1 from users where user_id = ?", (message.from_user.id,)).fetchone()
       checking1 = round(int(checking1[0]))
       if checking1 == 1:
          await bot.send_message(chat_id, f'ℹ | Дождитесь окончания игры! {rloser}', parse_mode='html')
          return
       checking2 = cursor.execute("SELECT checking2 from users where user_id = ?", (message.from_user.id,)).fetchone()
       checking2 = round(int(checking2[0]))
       if checking2 == 1:
          await bot.send_message(chat_id, f'ℹ | Дождитесь окончания игры! {rloser}', parse_mode='html')
          return
       checking3 = cursor.execute("SELECT checking3 from users where user_id = ?", (message.from_user.id,)).fetchone()
       checking3 = round(int(checking3[0]))
       if checking3 == 1:
          await bot.send_message(chat_id, f'ℹ | Дождитесь окончания игры! {rloser}', parse_mode='html')
          return
       c = 1
       pets = pet1 + pet2 + pet3 + pet4 + pet5 + pet6 + pet7 + pet8 + pet9 + pet10 + pet11

       summ5 = message.text.split()[1]
       
       summ4 = (summ5).replace(' ', '').replace('k', '000').replace('е','e').replace('к', '000').replace(',', '').replace('.', '').replace("$", "").replace('м', '000000').replace('m', '000000').replace('т','000000000000')
       summ3 = float(summ4)
       summ = int(summ3)
       summ2 = '{:,}'.format(summ).replace(',', '.')
       period = 5
       win = ['🙂', '😋', '😄', '🤑', '😃']
       rwin = random.choice(win)      
       games = cursor.execute("SELECT game from users where user_id = ?", (message.from_user.id,)).fetchone()
       games = int(games[0])
       get = cursor.execute("SELECT stavka_games FROM bot_time WHERE user_id = ?", (message.from_user.id,)).fetchone()
       rhp = random.randint(10, 20)
       reat = random.randint(10, 20)
       rmood = random.randint(10, 20)
       last_stavka = f"{int(get[0])}"
       stavkatime = time.time() - float(last_stavka)
       coff = random.randint(1,3)
       period1 = 5
       stavkatime1 = period1

       if time.time() >= stavkatime1:
          pass
       else:
          return

       period2 = 5
       stavkatime2 = period2

       if time.time() >= stavkatime2:
          pass
       else:
          return

       period3 = 5
       stavkatime3 = period3

       if time.time() >= stavkatime3:
          pass
       else:
          return
       if stavkatime > period:
          if balance >= summ:
             if summ > 0:
                if int(pets) >= 1:
                   if pet_hp >= 20:
                      if pet_eat >= 20:
                         if pet_mood >= 20:  
                            if coff == 1:
                               c = Decimal(summ * 2)
                               c2 = round(c)
                               c2 = '{0:,}'.format(c2).replace(',', '.')
                               await bot.send_message(chat_id, f"🎉 | <a href='tg://user?id={user_id}'>{user_name}</a>, ваш питомец победил в сражении! Ваш выигрыш: {c2}\n❤️ | ХП: -{rhp}\n🍗 | Сытость: -{reat}\n☀️ | Настроение: -{rmood}", parse_mode='html')
                               cursor.execute(f'UPDATE users SET balance = {balance - summ + (summ * 2)} WHERE user_id = "{user_id}"')
                               cursor.execute(f'UPDATE users SET pet_hp = {pet_hp - rhp} WHERE user_id = "{user_id}"')
                               cursor.execute(f'UPDATE users SET pet_eat = {pet_eat - reat} WHERE user_id = "{user_id}"')
                               cursor.execute(f'UPDATE users SET pet_mood = {pet_mood - rmood} WHERE user_id = "{user_id}"')
                               cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = "{user_id}"')
                               cursor.execute(f'UPDATE bot_time SET stavka_games=? WHERE user_id=?', (time.time(), user_id,))
                               connect.commit() 
                               return 
                            else:
                               c = Decimal(summ)
                               c2 = round(c)
                               c2 = '{0:,}'.format(c2).replace(',', '.')
                               await bot.send_message(chat_id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, ваш питомец проиграл в сражении! Ваш проигрыш: {c2}\n❤️ | ХП: -{rhp}\n🍗 | Сытость: -{reat}\n☀️ | Настроение: -{rmood}", parse_mode='html')
                               cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = "{user_id}"')
                               cursor.execute(f'UPDATE users SET pet_hp = {pet_hp - rhp} WHERE user_id = "{user_id}"')
                               cursor.execute(f'UPDATE users SET pet_eat = {pet_eat - reat} WHERE user_id = "{user_id}"')
                               cursor.execute(f'UPDATE users SET pet_mood = {pet_mood - rmood} WHERE user_id = "{user_id}"')
                               cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = "{user_id}"')
                               cursor.execute(f'UPDATE bot_time SET stavka_games=? WHERE user_id=?', (time.time(), user_id,))
                               connect.commit() 
                         if pet_mood == 0:
                            await bot.send_message(chat_id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, у вашего питомца нету настроения! {rloser}", parse_mode='html')
                      if pet_eat == 0:
                         await bot.send_message(chat_id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, ваш питомец голоден! {rloser}", parse_mode='html')
                   if pet_hp == 0:
                      await bot.send_message(chat_id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, у вашего питомца недостаточно здоровья! {rloser}", parse_mode='html')
                if int(pets) == 0:
                   await bot.send_message(chat_id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас нету питомца! {rloser}", parse_mode='html') 
             elif summ <= 0:
                  await bot.send_message(chat_id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, нельзя ставить отрицательное число! {rloser}", parse_mode='html')                                                    
          elif int(balance) <= int(summ):
               await bot.send_message(chat_id, f"💰 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств! {rloser}", parse_mode='html')
       else:
        await bot.send_message(chat_id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, играть можно раз в 5 секунд! {rloser}", parse_mode='html')


##############################################ОХОТА##################################################
    if message.text.lower().startswith("охота"):
       msg = message
       user_id = msg.from_user.id
       
       win = ['🙂', '😋', '😄', '🤑', '😃']
       loser = ['😔', '😕', '😣', '😞', '😢']
       rx = random.randint(0,110)
       rand = random.randint(1,4)
       rwin = random.choice(win)
       rloser = random.choice(loser)
       
       games = cursor.execute("SELECT game from users where user_id = ?", (message.from_user.id,)).fetchone()
       games = int(games[0])

       user_name = cursor.execute("SELECT user_name from users where user_id = ?", (message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       user_status = cursor.execute("SELECT user_status from users where user_id = ?", (message.from_user.id,)).fetchone()
       user_status = str(user_status[0])

       su = msg.text.split()[1]
       su2 = (su).replace(' ', '').replace('k', '000').replace('е','e').replace('к', '000').replace(',', '').replace('.', '')
       su3 = float(su2)
       summ = int(su3)
       summ2 = '{:,}'.format(summ).replace(',', '.')

       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])


       rx = random.randint(0,9550)
 
       if user_status in ['Admin', 'Helper_Admin', 'Owner']:             
          period = 1
       else:
          period = 5

       get = cursor.execute("SELECT stavka_games FROM bot_time WHERE user_id = ?", (message.from_user.id,)).fetchone()
       last_stavka = f"{int(get[0])}"
       stavkatime = time.time() - float(last_stavka)
       if stavkatime > period:
          if balance >= summ:
             if summ > 0:
                if int(rx) in range(0,2900):
                   i = summ * 3
                   i2 = int(i)
                   i3 = '{:,}'.format(i2).replace(',', '.')
                   await bot.send_message(message.chat.id, f"""
💽 | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a> 
🎮 | Игра: Охота
💸 | Ставка: {summ2}¢
💡 | Выводы: Вы поймали медведя!
{rwin} | Выигрыш: {i3}¢ [3X] 
""", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET balance = {balance + i2} WHERE user_id = {user_id}')
                   connect.commit()
                if int(rx) in range(2901,6000):
                   i = summ - summ * 0
                   i2 = int(i)
                   i3 = '{:,}'.format(i2).replace(',', '.')
                   await bot.send_message(message.chat.id, f"""
💽 | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a> 
🎮 | Игра: Охота
💸 | Ставка: {summ2}¢
💡 | Выводы: Вас съели!
{rloser} | Выигрыш: {i3}¢ [0X]
""", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET balance = {balance - i2} WHERE user_id = {user_id}')
                   connect.commit()
                if int(rx) in range(6001,8000):
                   i = summ * 1.5
                   i2 = int(i)
                   i3 = '{:,}'.format(i2).replace(',', '.')
                   await bot.send_message(message.chat.id, f"""
💽 | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a> 
🎮 | Игра: Охота
💸 | Ставка: {summ2}¢
💡 | Выводы: Вы поймали зайца!
{rwin} | Выигрыш: {i3}¢ [1.5X] 
""", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET balance = {balance - i2} WHERE user_id = {user_id}')
                   connect.commit()
                if int(rx) in range(8001,9200):
                   i = summ
                   i2 = int(i)
                   i3 = '{:,}'.format(i2).replace(',', '.')
                   await bot.send_message(message.chat.id, f"""
💽 | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a> 
🎮 | Игра: Охота
💸 | Ставка: {summ2}¢
💡 | Выводы: Вы никого не поймали!
{rwin} | Остаются: {i3}¢ [1X] 
""", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET balance = {balance + i2} WHERE user_id = {user_id}')
                   connect.commit()
                if int(rx) == 9500:
                   i = summ * 5
                   i2 = int(i)
                   i3 = '{:,}'.format(i2).replace(',', '.')
                   await bot.send_message(message.chat.id, f"""
💽 | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a> 
🎮 | Игра: Охота
💸 | Ставка: {summ2}¢
💡 | Выводы: Вы поймали льва!
{rwin} | Выигрыш: {i3}¢ [5X] 
""", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE users SET balance = {balance + i2} WHERE user_id = {user_id}')
                   connect.commit()
             else:
                await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, нельзя ставить отрицательное число", parse_mode='html')     
          else:
             await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! У вас нехватает средств!", parse_mode='html')     
       else:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, играть можно раз в {period} секунд ", parse_mode='html')


##################################################ФЛИП############################################

    if message.text.lower().startswith('флип'):
      try:
         msg = message
         user_id = msg.from_user.id
         games = cursor.execute("SELECT game from users where user_id = ?", (message.from_user.id,)).fetchone()
         games = int(games[0])

         user_name = cursor.execute("SELECT user_name from users where user_id = ?", (message.from_user.id,)).fetchone()
         user_name = str(user_name[0])

         user_status = cursor.execute("SELECT user_status from users where user_id = ?", (message.from_user.id,)).fetchone()
         user_status = str(user_status[0])

         su = msg.text.split()[1]
         su2 = (su).replace(' ', '').replace('k', '000').replace('е','e').replace('к', '000').replace(',', '').replace('.', '').replace('$', '').replace('м', '000000').replace('все', '{balance}').replace('всё', '{balance}')
         su3 = float(su2)
         summ = int(su3)

         summ2 = '{:,}'.format(summ).replace(',', '.')
         
         ore = str(msg.text.split()[2])


         balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
         balance = round(int(balance[0]))
         

         if user_status in ['Vlaselin', 'Bog']:
            period = 2
            tp = 'секунды'
         elif user_status in ['Admin', 'Helper_Admin', 'Owner']:
            period = 1
            tp = 'секунду'
         else:
            period = 5
            tp = 'секунд'



         get = cursor.execute("SELECT stavka_games FROM bot_time WHERE user_id = ?", (message.from_user.id,)).fetchone()
         last_stavka = f"{int(get[0])}"
         stavkatime = time.time() - float(last_stavka)

         if stavkatime < period:
            return await message.reply(f'❗️ Играть можно раз в <b>{period} {tp}</b>', parse_mode='html')
         else:
            pass
         
         if balance < summ:
            return await message.reply(f'❗️ У вас <b>недостаточно средств</b>', parse_mode='html')
         else:
            pass
         
         if summ <= 0:
            return await message.reply('❗️ Ставка не может быть отрицательным числом <b>[0 и меньше]</b>', parse_mode='html')
         else:
            pass





         if ore in ['орел', 'о', 'Орел', 'О']:
            r = random.randint(0, 101)
            
            if r in range(0, 50):
               stavka = int(summ * 0)
               stavka2 = '{:,}'.format(stavka).replace(',', '.')
               await message.reply(f"Вы поставили <code>{summ2}</code>¢ на <b>🦅 Орла</b>, а вам выпала <b>🪙 Решка</b>, вы выиграли <code>{stavka2}</code>¢", parse_mode='html')
               cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
               cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
               cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
               connect.commit()



            if r in range(51, 101):
               
               stavka = int(summ * 2)
               stavka2 = '{:,}'.format(stavka).replace(',', '.')
               
               await message.reply(f"Вы поставили <code>{summ2}</code>¢ на <b>🦅 Орла</b>, а вам выпал <b>🦅 Орел</b>, вы выиграли <code>{stavka2}</code>¢", parse_mode='html')
               cursor.execute(f'UPDATE users SET balance = {(balance - summ) + (summ * 2)} WHERE user_id = {user_id}')
               cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
               cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
               connect.commit()
         




         if ore in ['решка', 'р', 'Решка', 'Р']:
            r = random.randint(0, 101)
            
            if r in range(0, 50):
               stavka = int(summ * 0)
               stavka2 = '{:,}'.format(stavka).replace(',', '.')
               await message.reply(f"Вы поставили <code>{summ2}</code>¢ на <b>🪙 Решку</b>, а вам выпал <b>🦅 Орел</b>, вы выиграли <code>{stavka2}</code>¢", parse_mode='html')
               cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
               cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
               cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
               connect.commit()



            if r in range(51, 101):
               
               stavka = int(summ * 2)
               stavka2 = '{:,}'.format(stavka).replace(',', '.')
               
               await message.reply(f"Вы поставили <code>{summ2}</code>¢ на <b>🪙 Решку</b>, а вам выпала <b>🪙 Решка</b>, вы выиграли <code>{stavka2}</code>¢", parse_mode='html')
               cursor.execute(f'UPDATE users SET balance = {(balance - summ) + (summ * 2)} WHERE user_id = {user_id}')
               cursor.execute(f'UPDATE users SET game = {games + 1} WHERE user_id = {user_id}')
               cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
               connect.commit()
      
      except IndexError:
         return await message.reply(f'❗️ <b>Вы не ввели сумму ставки, либо же то, на что хотите поставить - </b> <code>флип 10к [о/р]</code> ', parse_mode='html')
      except ValueError:
         return await message.reply(f'❗️ <b>Не правильно введены аргументы - <code>флип [сумма] [о/р]</code></b>', parse_mode='html')


######
    if message.text.lower() == 'кости':
        msg = message
        user_id = msg.from_user.id
        mci = msg.chat.id
        user_name = cursor.execute(
            "SELECT user_name from users where user_id = ?", (message.from_user.id,)).fetchone()
        user_name = str(user_name[0])
        await bot.send_message(mci, f"""<b><a href='tg://user?id={user_id}'>{user_name}</a>, вот информация за игру кости.
        
🎰 | После ставки вам и боту падает рандом число от 1 до 12 и у кого больше выпадет тот и выйграл x2! 
💸 | Минимальная ставка 10,000¢

Команда: <code>Кости </code>[Ставка]</b>""", parse_mode='html')
    if message.text.lower() in ['Кости все', 'Кости всё', 'кости все', 'кости всё']:
        msg = message
        user_id = msg.from_user.id
        mci = message.chat.id
        user_name = cursor.execute(
            "SELECT user_name from users where user_id = ?", (message.from_user.id,)).fetchone()
        user_name = str(user_name[0])
        balance = cursor.execute(
            "SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
        balance = int(balance[0])
        games = cursor.execute(
            "SELECT games from users where user_id = ?", (message.from_user.id,)).fetchone()
        games = int(games[0])
        rb = random.randint(1, 12)
        rp = random.randint(1, 12)
        period = 9
        su2 = balance
        summ = int(su2)
        summ2 = '{:,}'.format(summ)
        get = cursor.execute(
            "SELECT stavka_games FROM bot_time WHERE user_id = ?", (message.from_user.id,)).fetchone()
        last_stavka = int(get[0])
        stavkatime = time.time() - float(last_stavka)
        if summ >= 10000:
           if summ >= 0:
                if summ <= balance:
                    if stavkatime >= period:
                        if rb == rp:
                            await bot.send_message(mci, f"""<b>
🎰Игра в кости
👤 | Ник: <a href='tg://user?id={user_id}'>{user_name}</a>
🎲 | Число бота: {rb}
🎲 | Ваше число: {rp}
💸 | Сумма ставки: {summ2}¢
❓ | Итоги: ❎Ничья❎
                      </b>""", parse_mode='html')
                            cursor.execute(
                                f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = "{user_id}"')
                            cursor.execute(
                                f'UPDATE users SET games = {games + 1} WHERE user_id = "{user_id}"')
                            connect.commit()
                            return
                        if rp > rb:
                            await bot.send_message(mci, f"""<b>
🎰Игра в кости
👤 | Ник: <a href='tg://user?id={user_id}'>{user_name}</a>
🎲 | Число бота: {rb}
🎲 | Ваше число: {rp}
💸 | Сумма ставки: {summ2}¢
❓ | Итоги: ✅Вы выйграли!✅
➕ | {summ2}¢
                      </b>""", parse_mode='html')
                            cursor.execute(
                                f'UPDATE users SET balance = {balance + summ} WHERE user_id = "{user_id}"')
                            cursor.execute(
                                f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = "{user_id}"')
                            cursor.execute(
                                f'UPDATE users SET games = {games + 1} WHERE user_id = "{user_id}"')
                            connect.commit()
                            return
                        if rb > rp:
                            await bot.send_message(mci, f"""<b>
🎰Игра в кости
👤 | Ник: <a href='tg://user?id={user_id}'>{user_name}</a>
🎲 | Число бота: {rb}
🎲 | Ваше число: {rp}
💸 | Сумма ставки: {summ2}¢
❓ | Итоги: ⭕Вы проиграли!⭕
➖ | {summ2}¢
                      </b>""", parse_mode='html')
                            cursor.execute(
                                f'UPDATE users SET balance = {balance - summ} WHERE user_id = "{user_id}"')
                            cursor.execute(
                                f'UPDATE users SET games = {games + 1} WHERE user_id = "{user_id}"')
                            cursor.execute(
                                f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = "{user_id}"')
                            connect.commit()
                            return
                    else:
                        await message.reply("<b>⏳ | Ставить ставку можно каждые 9 секунд!</b>", parse_mode='html')
                else:
                    await message.reply("<b>💸 | Нельзя ставить ставку выше чем ваш баланс!</b>", parse_mode='html')
    
    if message.text.lower().startswith("кости"):
        msg = message
        user_id = msg.from_user.id
        mci = message.chat.id
        user_name = cursor.execute(
            "SELECT user_name from users where user_id = ?", (message.from_user.id,)).fetchone()
        user_name = str(user_name[0])
        balance = cursor.execute(
            "SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
        balance = int(balance[0])
        games = cursor.execute(
            "SELECT games from users where user_id = ?", (message.from_user.id,)).fetchone()
        games = int(games[0])
        su = str(msg.text.split()[1]).replace('k', '000').replace('е', 'e').replace(
            'к', '000').replace('м', '000000').replace('m', '000000').replace('.', '').replace(',', '').replace('₽', '').replace(' ', '')
        su2 = float(su)
        summ = int(su2)
        summ2 = '{:,}'.format(summ)
        period = 9
        rb = random.randint(1, 12)
        rp = random.randint(1, 12)
        get = cursor.execute(
            "SELECT stavka_games FROM bot_time WHERE user_id = ?", (message.from_user.id,)).fetchone()
        last_stavka = int(get[0])
        stavkatime = time.time() - float(last_stavka)
        if summ >= 10000:
            if summ >= 0:
                if summ <= balance:
                    if stavkatime >= period:
                        if rb == rp:
                            await bot.send_message(mci, f"""<b>
🎰Игра в кости
👤 | Ник: <a href='tg://user?id={user_id}'>{user_name}</a>
🎲 | Число бота: {rb}
🎲 | Ваше число: {rp}
💸 | Сумма ставки: {summ2}¢
❓ | Итоги: ❎Ничья❎
                      </b>""", parse_mode='html')
                            cursor.execute(
                                f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = "{user_id}"')
                            cursor.execute(
                                f'UPDATE users SET games = {games + 1} WHERE user_id = "{user_id}"')
                            connect.commit()
                            return
                        if rp > rb:
                            await bot.send_message(mci, f"""<b>
🎰Игра в кости
👤 | Ник: <a href='tg://user?id={user_id}'>{user_name}</a>
🎲 | Число бота: {rb}
🎲 | Ваше число: {rp}
💸 | Сумма ставки: {summ2}¢
❓ | Итоги: ✅Вы выйграли!✅
➕ | {summ2}¢
                      </b>""", parse_mode='html')
                            cursor.execute(
                                f'UPDATE users SET balance = {balance + summ} WHERE user_id = "{user_id}"')
                            cursor.execute(
                                f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = "{user_id}"')
                            cursor.execute(
                                f'UPDATE users SET games = {games + 1} WHERE user_id = "{user_id}"')
                            connect.commit()
                            return
                        if rb > rp:
                            await bot.send_message(mci, f"""<b>
🎰Игра в кости
👤 | Ник: <a href='tg://user?id={user_id}'>{user_name}</a>
🎲 | Число бота: {rb}
🎲 | Ваше число: {rp}
💸 | Сумма ставки: {summ2}¢
❓ | Итоги: ⭕Вы проиграли!⭕
➖ | {summ2}¢
                      </b>""", parse_mode='html')
                            cursor.execute(
                                f'UPDATE users SET balance = {balance - summ} WHERE user_id = "{user_id}"')
                            cursor.execute(
                                f'UPDATE users SET games = {games + 1} WHERE user_id = "{user_id}"')
                            cursor.execute(
                                f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = "{user_id}"')
                            connect.commit()
                            return
                    else:
                        await message.reply("<b>⏳ | Ставить ставку можно каждые 9 секунд!</b>", parse_mode='html')
                else:
                    await message.reply("<b>💸 | Нельзя ставить ставку выше чем ваш баланс!</b>", parse_mode='html')
            else:
                await message.reply("<b>💸 | Нельзя ставить ставку выше чем 100,000,000,000¢!</b>", parse_mode='html')
        else:
            await message.reply("<b>💸 | Нельзя ставить ставку ниже чем 10,000¢!</b>", parse_mode='html')


##################################################РУЛЕТКА##########################################################

    if message.text.lower().startswith('рулетка'):
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])

       user_status = cursor.execute("SELECT user_status from users where user_id = ?", (message.from_user.id,)).fetchone()
       user_status = user_status[0]

       game = cursor.execute("SELECT game from users where user_id = ?", (message.from_user.id,)).fetchone()
       game = int(game[0])

       black_red = str(message.text.split()[1])
       su = msg.text.split()[2]
       su2 = (su).replace(' ', '').replace('k', '000').replace('е','e').replace('к', '000').replace(',', '').replace('.', '')
       su3 = float(su2)
       summ = int(su3)

       balance2 = '{:,}'.format(balance).replace(',', '.')

       period = 5
       
       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])

       get = cursor.execute("SELECT stavka_games FROM bot_time WHERE user_id = ?", (message.from_user.id,)).fetchone()
       last_stavka = int(get[0])
       stavkatime = time.time() - float(last_stavka)
       if balance >= summ:
        if summ > 0:
          if black_red in ['ч',"черное","Ч", "Черное"]:
             rx = random.randint(0,1000)

             if rx in range(0,850):
                await bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a>
🖲 Выпало - 🔴 
⚫️ Проигрыш - 0¢
               """, parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE users SET game = {game + 1} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                connect.commit()
             if rx in range(851, 999):
                summ3 = summ * 2
                summ4 = '{:,}'.format(summ3).replace(',', '.')

                await bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a>
🖲 Выпало - ⚫️
✅ Выигрыш -  {summ4}¢
               """, parse_mode='html')  
                cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE users SET balance = {balance + summ3} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE users SET game = {game + 1} WHERE user_id = {user_id}')
                cursor.exencute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                connect.commit()   
             if rx == 1000:

                await bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a>
🖲 Выпало - 🟢
⚫️ Проигрыш - 0¢
               """, parse_mode='html')   
                cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE users SET game = {game + 1} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                connect.commit() 
          if black_red in ['к',"красное","К", "Красное"]:
             rx = random.randint(0,1000)

             if rx in range(0,850):
                await bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a>
🖲 Выпало - ⚫️ 
🔴 Проигрыш - 0¢
               """, parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE users SET game = {game + 1} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                connect.commit()
             if rx in range(851, 999):

                await bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a>
🖲 Выпало - 🟢
🔴 Проигрыш - 0¢
               """, parse_mode='html')   
                cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE users SET game = {game + 1} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                connect.commit()
             if rx == 1000:
                summ3 = summ * 2
                summ4 = '{:,}'.format(summ3).replace(',', '.')

                await bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a>
🖲 Выпало - 🔴
✅ Выигрыш - {summ4}¢
               """, parse_mode='html')  
                cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE users SET balance = {balance + summ3} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE users SET game = {game + 1} WHERE user_id = {user_id}')
                cursor.exencute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                    

##################################################НИК############################################         
         
    if message.text.startswith('Сменить ник') or message.text.startswith('сменить ник'):
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       chat_id = message.chat.id
       user_id = message.from_user.id
       name = message.text.split()[2:]
       name2 = ' '.join(name)
       full_name = (name2)

       if len(full_name) < 0:
         return await message.reply('❗️ Название ника должна быть больше <b>4 символов</b>', parse_Mode='html')
       elif len(full_name) > 35:
         return await message.reply(f'❗️ Название ника должна быть меньше <b>35 символов</b>', parse_mode='html')
       else:
         pass

       all_name = cursor.execute('SELECT user_name from users').fetchall()
       all_name2 = []

       for all_name3 in all_name:
         all_name2.append(all_name3[0])
      
       if full_name in all_name2:
         return await message.reply(f'❗️ Ник с названием «<b>{full_name}</b>» уже существует', parse_mode='html')
       else:
         pass

       await bot.send_message(message.chat.id, f"✏️ | <a href='tg://user?id={user_id}'>{user_name}</a> , вы успешно поменяли свое имя на: {full_name}!", parse_mode='html')
       cursor.execute(f'UPDATE users SET user_name = \"{full_name}\" WHERE user_id = "{user_id}"')
        
       all_family = cursor.execute(f'SELECT owner_id from family').fetchall()
       all_family2 = []
       proverka_family = 0
       for all_owner_id in all_family:
         all_family2.append(all_owner_id[0])
          
       user_id_family = cursor.execute(f'SELECT user_id from user_family where user_id = {user_id}').fetchone()
        
       if user_id_family != None:
         cursor.execute(f'UPDATE user_family SET user_name = \"{name}\" WHERE user_id = "{user_id}"')
       else:
         pass
          
       if user_id in all_family2:
         cursor.execute(f'UPDATE family SET owner_name = \"{name}\" WHERE owner_id = "{user_id}"')
       else:
         pass
          
##################################################КРИПТО###########################################
    if message.text.lower() == 'лайткоин курс':
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       c = api.get_price(ids='ethereum', vs_currencies='rub')['ethereum']['rub']
       c2 = int(c)
       c3 = '{:,}'.format(c2)

       lite_photo = open('imges/lite.jpg', 'rb')
       await bot.send_photo(chat_id=message.chat.id, photo=lite_photo, caption=f"""🟦 <a href='tg://user?id={user_id}'>{user_name}</a>,Вот курс лайткоина: {c3}¢ 🔹

Чтобы купить 🔹 введите команду:  
Лайткоин купить [количество]

Чтобы продать 🔹 введите команду:  
Лайткоин продать [количество] """, parse_mode='html')


    if message.text.startswith('Лайткоин') or message.text.startswith('лайткоин'):
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id
       
       i = str(message.text.split()[1])
       d = int(message.text.split()[2])
       d2 = '{:,}'.format(d)
       c = api.get_price(ids='ethereum', vs_currencies='rub')['ethereum']['rub']
       c2 = int(c)
       c3 = '{:,}'.format(c2)

       litecoin = cursor.execute("SELECT litecoin from users where user_id = ?", (message.from_user.id,)).fetchone()
       litecoin = int(litecoin[0])

       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = round(int(balance[0]))

       summ = d * c2
       summ2 = '{:,}'.format(summ)


       if i == 'купить':
          if summ <= balance:
             if d > 0:
                await bot.send_message(message.chat.id, f" 🔹 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно купили {d2} лайткоина 🔹 за {summ2}¢", parse_mode='html')
                cursor.execute(f'UPDATE users SET litecoin = {litecoin + d}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE users SET balance = {balance - summ}  WHERE user_id = "{user_id}"')
                connect.commit()
             else:
                await bot.send_message(message.chat.id, f"🔹 | <a href='tg://user?id={user_id}'>{user_name}</a>, нельзя покупать отрицательное число ", parse_mode='html')
          else:
             await bot.send_message(message.chat.id, f"🔹 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств ", parse_mode='html')
       if i == 'продать':
          if d <= litecoin:
             if d > 0:
                await bot.send_message(message.chat.id, f" 🔹 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно продали {d2} лайткоина 🔹 за {summ2}¢", parse_mode='html')
                cursor.execute(f'UPDATE users SET litecoin = {litecoin - d}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE users SET balance = {balance + summ}  WHERE user_id = "{user_id}"')
                connect.commit()
             else:
                await bot.send_message(message.chat.id, f"🔹 | <a href='tg://user?id={user_id}'>{user_name}</a>, нельзя покупать отрицательное число ", parse_mode='html')
          else:
             await bot.send_message(message.chat.id, f"🔹 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств ", parse_mode='html')
    
        
    if message.text.lower() == 'биткоин курс':
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       c = api.get_price(ids='bitcoin', vs_currencies='rub')['bitcoin']['rub']
       c2 = int(c)
       c3 = '{:,}'.format(c2).replace(",", ".")

       lite_photo = open('imges/btc.jpg', 'rb')
       await bot.send_photo(chat_id=message.chat.id, photo=lite_photo, caption=f"""🌐 | <a href='tg://user?id={user_id}'>{user_name}</a>,Вот курс биткоина: {c3}¢ 🌐

Чтобы купить 🌐 введите команду:  
Биткоин купить [количество]

Чтобы продать 🌐 введите команду:  
Биткоин продать [количество] """, parse_mode='html')


    if message.text.startswith('Биткоин') or message.text.startswith('биткоин'):
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id
       
       i = str(message.text.split()[1])
       d = int(message.text.split()[2])
       d2 = '{:,}'.format(d)
       c = api.get_price(ids='bitcoin', vs_currencies='rub')['bitcoin']['rub']
       c2 = int(c)
       c3 = '{:,}'.format(c2)

       bitcoin = cursor.execute("SELECT bitcoin from users where user_id = ?", (message.from_user.id,)).fetchone()
       bitcoin = int(bitcoin[0])

       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = round(int(balance[0]))

       summ = d * c2
       summ2 = '{:,}'.format(summ)


       if i == 'купить':
          if summ <= balance:
             if d > 0:
                await bot.send_message(message.chat.id, f"🌐 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно купили {d2} btc за {summ2}¢", parse_mode='html')
                cursor.execute(f'UPDATE users SET bitcoin = {bitcoin + d}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE users SET balance = {balance - summ}  WHERE user_id = "{user_id}"')
                connect.commit()
             else:
                await bot.send_message(message.chat.id, f"🌐️ | <a href='tg://user?id={user_id}'>{user_name}</a>, нельзя покупать отрицательное число btc", parse_mode='html')
          else:
             await bot.send_message(message.chat.id, f"🌐️ | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств", parse_mode='html')
       if i == 'продать':
          if d <= bitcoin:
             if d > 0:
                await bot.send_message(message.chat.id, f"🌐 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно продали {d2} btc за {summ2}¢", parse_mode='html')
                cursor.execute(f'UPDATE users SET bitcoin = {bitcoin - d}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE users SET balance = {balance + summ}  WHERE user_id = "{user_id}"')
                connect.commit()
             else:
                await bot.send_message(message.chat.id, f"️🌐 | <a href='tg://user?id={user_id}'>{user_name}</a>, нельзя покупать отрицательное число btc", parse_mode='html')
          else:
             await bot.send_message(message.chat.id, f"🌐️ | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно btc", parse_mode='html')


    if message.text.lower() == 'эфириум курс':
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       c = api.get_price(ids='ethereum', vs_currencies='rub')['ethereum']['rub']
       c2 = int(c)
       c3 = '{:,}'.format(c2)

       lite_photo = open('imges/efir.jpg', 'rb')
       await bot.send_photo(chat_id=message.chat.id, photo=lite_photo, caption=f"""🟪 | <a href='tg://user?id={user_id}'>{user_name}</a>,Вот курс эфириума: {c3}¢ 🟣

Чтобы купить 🟣 введите команду:  
Эфириум купить [количество]

Чтобы продать 🟣 введите команду:  
Эфириум продать [количество] """, parse_mode='html')


    if message.text.startswith('Эфириум') or message.text.startswith('эфириум'):
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id
       
       i = str(message.text.split()[1])
       d = int(message.text.split()[2])
       d2 = '{:,}'.format(d)
       c = api.get_price(ids='ethereum', vs_currencies='rub')['ethereum']['rub']
       c2 = int(c)
       c3 = '{:,}'.format(c2)

       ethereum = cursor.execute("SELECT ethereum from users where user_id = ?", (message.from_user.id,)).fetchone()
       ethereum = int(ethereum[0])

       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = round(int(balance[0]))

       summ = d * c2
       summ2 = '{:,}'.format(summ)


       if i == 'купить':
          if summ <= balance:
             if d > 0:
                await bot.send_message(message.chat.id, f" 🟣 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно купили {d2} эфириума 🟣 за {summ2}¢", parse_mode='html')
                cursor.execute(f'UPDATE users SET ethereum = {ethereum + d}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE users SET balance = {balance - summ}  WHERE user_id = "{user_id}"')
                connect.commit()
             else:
                await bot.send_message(message.chat.id, f"🟣 | <a href='tg://user?id={user_id}'>{user_name}</a>, нельзя покупать отрицательное число ", parse_mode='html')
          else:
             await bot.send_message(message.chat.id, f"🟣 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств ", parse_mode='html')
       if i == 'продать':
          if d <= ethereum:
             if d > 0:
                await bot.send_message(message.chat.id, f" 🟣 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно продали {d2} эфириума 🟣 за {summ2}¢", parse_mode='html')
                cursor.execute(f'UPDATE users SET ethereum = {ethereum - d}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE users SET balance = {balance + summ}  WHERE user_id = "{user_id}"')
                connect.commit()
             else:
                await bot.send_message(message.chat.id, f"🟣 | <a href='tg://user?id={user_id}'>{user_name}</a>, нельзя покупать отрицательное число ", parse_mode='html')
          else:
             await bot.send_message(message.chat.id, f"🟣 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств ", parse_mode='html')  


    if message.text.lower() == 'фантом курс':
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       c = api.get_price(ids='bitcoin', vs_currencies='rub')['bitcoin']['rub']
       c2 = int(c)
       c3 = '{:,}'.format(c2)

       lite_photo = open('imges/fantom.jpg', 'rb')
       await bot.send_photo(chat_id=message.chat.id, photo=lite_photo, caption=f"""💠 | <a href='tg://user?id={user_id}'>{user_name}</a>, вот курс фантома: {c3}¢ 💠

Чтобы купить 💠 введите команду:  
Фантом купить [количество]

Чтобы продать 💠 введите команду:  
Фантом продать [количество] """, parse_mode='html')


    if message.text.startswith('Фантом') or message.text.startswith('фантом'):
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id
       
       i = str(message.text.split()[1])
       d = int(message.text.split()[2])
       d2 = '{:,}'.format(d)
       c = api.get_price(ids='bitcoin', vs_currencies='rub')['bitcoin']['rub']
       c2 = int(c)
       c3 = '{:,}'.format(c2)

       fantom = cursor.execute("SELECT fantom from users where user_id = ?", (message.from_user.id,)).fetchone()
       fantom = int(fantom[0])

       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = round(int(balance[0]))

       summ = d * c2
       summ2 = '{:,}'.format(summ)

       if i == 'купить':
          if summ <= balance:
             if d > 0:
                await bot.send_message(message.chat.id, f" 💠 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно купили {d2} фантомов 💠 за {summ2}¢", parse_mode='html')
                cursor.execute(f'UPDATE users SET fantom = {fantom + d}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE users SET balance = {balance - summ}  WHERE user_id = "{user_id}"')
                connect.commit()
             else:
                await bot.send_message(message.chat.id, f"💠 | <a href='tg://user?id={user_id}'>{user_name}</a>, нельзя покупать отрицательное число ", parse_mode='html')
          else:
             await bot.send_message(message.chat.id, f"💠 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств ", parse_mode='html')
       if i == 'продать':
          if d <= fantom:
             if d > 0:
                await bot.send_message(message.chat.id, f" 💠 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно продали {d2} фантомов 💠 за {summ2}¢", parse_mode='html')
                cursor.execute(f'UPDATE users SET fantom = {fantom - d}  WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE users SET balance = {balance + summ}  WHERE user_id = "{user_id}"')
                connect.commit()
             else:
                await bot.send_message(message.chat.id, f"💠 | <a href='tg://user?id={user_id}'>{user_name}</a>, нельзя покупать отрицательное число ", parse_mode='html')
          else:
             await bot.send_message(message.chat.id, f"💠 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств ", parse_mode='html')


############################################ПОПОЛНЕНИЯ###############################################
    
    if message.text.startswith("Пополнить") or message.text.startswith("пополнить"):
        if message.chat.type == 'private':
            user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
            user_name = user_name[0]
            user_id = message.from_user.id
            loser = ['😔', '😕', '😣', '😞', '😢']
            rloser = random.choice(loser)

            try:
                summ = int(message.text.split()[1])
            except:
                await message.reply('‼️  Не хватает аргументов!\nПример: Пополнить число ')
                return

            message_money = int(summ)
            if message_money >= 2:
                comment = str(message.from_user.id) + \
                          "_" + str(random.randint(1000, 9999))
                bill = p2p.bill(amount=message_money,
                                lifetime=15, comment=comment)
                add_check(message.from_user.id,
                          message_money, bill.bill_id)
                await bot.send_message(message.from_user.id,
                                       f"Нажмите на ссылку ниже для оплаты счета\nСсылку:{bill.pay_url}",
                                       reply_markup=buy_menu(url=bill.pay_url, bill=bill.bill_id))
            else:
                await bot.send_message(message.chat.id,
                                       f'‼️ <a href="tg://user?id={user_id}">{user_name}</a>,Минимальная сумма 2 руб{rloser}',
                                       parse_mode='html')

        else:
            loser = ['😔', '😕', '😣', '😞', '😢']
            rloser = random.choice(loser)
            await bot.send_message(message.chat.id,
                                   f'<a href="tg://user?id={user_id}">{user_name}</a>, Пополнить можно только в лс {rloser}',
                                   parse_mode='html')


######################################РП КОМАНДЫ#################################################
    if message.text.lower() in ["рп-команды", "РП-команды", "Рп", "рп"]:
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id
       await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, список РП-команд:\n🤗 | Обнять\n🧊 | Ударить об лёд\n❄️ | Кинуть снежок\n👏 | Похлопать\n👨‍💻 | Заскамить\n☕️ | Пригласить на чай\n👉👌 | Изнасиловать\n🤝 | Взять за руку\n📱 | Подарить айфон\n✋ | Дать пять\n😬 | Укусить\n🤛 | Ударить\n🤲 | Прижать\n💋 | Чмок\n💋 | Поцеловать\n😼 | Кусь\n🤲 | Прижать\n🔪 | Убить\n🤜 | Уебать\n💰 | Украсть\n🔞 | Выебать\n👅 | Отсосать\n👅 | Отлизать\n🔞 | Трахнуть\n🔥 | Сжечь\n💐 | Подарить цветы", parse_mode='html')

    if message.text.lower() in ["чмок", "Чмок"]:
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
       reply_user_name = reply_user_name[0]
       reply = message.reply_to_message
       user_id = message.from_user.id
       reply_user_id = message.reply_to_message.from_user.id
       if reply:
          replyuser = reply.from_user
          await bot.send_message(message.chat.id, f"💋 | <a href='tg://user?id={user_id}'>{user_name}</a> чмокнул(-а) <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')
    if message.text.lower() in ["кусь", "Кусь"]:
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
       reply_user_name = reply_user_name[0]
       reply = message.reply_to_message
       user_id = message.from_user.id
       reply_user_id = message.reply_to_message.from_user.id
       if reply:
          replyuser = reply.from_user
          await bot.send_message(message.chat.id, f"😼 | <a href='tg://user?id={user_id}'>{user_name}</a> кусьнул(-а) <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')
    if message.text.lower() in ["обнять", "Обнять"]:
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
       reply_user_name = reply_user_name[0]
       reply = message.reply_to_message
       user_id = message.from_user.id
       reply_user_id = message.reply_to_message.from_user.id
       if reply:
          replyuser = reply.from_user
          await bot.send_message(message.chat.id, f"🤗 | <a href='tg://user?id={user_id}'>{user_name}</a> обнял(-а) <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')
    if message.text.lower() in ["подарить цветы", "Подарить цветы"]:
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
       reply_user_name = reply_user_name[0]
       reply = message.reply_to_message
       user_id = message.from_user.id
       reply_user_id = message.reply_to_message.from_user.id
       if reply:
          replyuser = reply.from_user
          await bot.send_message(message.chat.id, f"💐 | <a href='tg://user?id={user_id}'>{user_name}</a> подарил(-а) цветы <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')

    if message.text.lower() in ["поцеловать", "Поцеловать"]:
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
       reply_user_name = reply_user_name[0]
       reply = message.reply_to_message
       user_id = message.from_user.id
       reply_user_id = message.reply_to_message.from_user.id
       if reply:
          replyuser = reply.from_user
          await bot.send_message(message.chat.id, f"💋 | <a href='tg://user?id={user_id}'>{user_name}</a> поцеловал(-а) <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')
    if message.text.lower() in ["дать пять", "Дать пять"]:
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
       reply_user_name = reply_user_name[0]
       reply = message.reply_to_message
       user_id = message.from_user.id
       reply_user_id = message.reply_to_message.from_user.id
       if reply:
          replyuser = reply.from_user
          await bot.send_message(message.chat.id, f"✋ | <a href='tg://user?id={user_id}'>{user_name}</a> дал(-а) пять <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')
    if message.text.lower() in ["подарить айфон", "Подарить айфон"]:
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
       reply_user_name = reply_user_name[0]
       reply = message.reply_to_message
       user_id = message.from_user.id
       reply_user_id = message.reply_to_message.from_user.id
       if reply:
          replyuser = reply.from_user
          await bot.send_message(message.chat.id, f"📱 | <a href='tg://user?id={user_id}'>{user_name}</a> подарил(-а) айфон <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')
    if message.text.lower() in ["ударить об лед", "Ударить об лед", "Ударить об лёд", "ударить об лёд"]:
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
       reply_user_name = reply_user_name[0]
       reply = message.reply_to_message
       user_id = message.from_user.id
       reply_user_id = message.reply_to_message.from_user.id
       if reply:
          replyuser = reply.from_user
          await bot.send_message(message.chat.id, f"🧊 | <a href='tg://user?id={user_id}'>{user_name}</a> ударил(-а) головой об лёд <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')
    if message.text.lower() in ["ударить", "Ударить"]:
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
       reply_user_name = reply_user_name[0]
       reply = message.reply_to_message
       user_id = message.from_user.id
       reply_user_id = message.reply_to_message.from_user.id
       if reply:
          replyuser = reply.from_user
          await bot.send_message(message.chat.id, f"🤛 | <a href='tg://user?id={user_id}'>{user_name}</a> ударил(-а) <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')
    if message.text.lower() in ["заскамить", "Заскамить"]:
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
       reply_user_name = reply_user_name[0]
       reply = message.reply_to_message
       user_id = message.from_user.id
       reply_user_id = message.reply_to_message.from_user.id
       if reply:
          replyuser = reply.from_user
          await bot.send_message(message.chat.id, f"👨‍💻 | <a href='tg://user?id={user_id}'>{user_name}</a> заскамил(-а) <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')
    if message.text.lower() in ["прижать", "Прижать"]:
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
       reply_user_name = reply_user_name[0]
       reply = message.reply_to_message
       user_id = message.from_user.id
       reply_user_id = message.reply_to_message.from_user.id
       if reply:
          replyuser = reply.from_user
          await bot.send_message(message.chat.id, f"🤲 | <a href='tg://user?id={user_id}'>{user_name}</a> прижал(-а) <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')
    if message.text.lower() in ["укусить", "Укусить"]:
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
       reply_user_name = reply_user_name[0]
       reply = message.reply_to_message
       user_id = message.from_user.id
       reply_user_id = message.reply_to_message.from_user.id
       if reply:
          replyuser = reply.from_user
          await bot.send_message(message.chat.id, f"😬 | <a href='tg://user?id={user_id}'>{user_name}</a> укусил(-а) <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')
    if message.text.lower() in ["взять за руку", "Взять за руку"]:
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
       reply_user_name = reply_user_name[0]
       reply = message.reply_to_message
       user_id = message.from_user.id
       reply_user_id = message.reply_to_message.from_user.id
       if reply:
          replyuser = reply.from_user
          await bot.send_message(message.chat.id, f"🤝 | <a href='tg://user?id={user_id}'>{user_name}</a> взял(-а) за руку <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')
    if message.text.lower() in ["кинуть снежок", "Кинуть снежок"]:
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
       reply_user_name = reply_user_name[0]
       reply = message.reply_to_message
       user_id = message.from_user.id
       reply_user_id = message.reply_to_message.from_user.id
       if reply:
          replyuser = reply.from_user
          await bot.send_message(message.chat.id, f"❄️ | <a href='tg://user?id={user_id}'>{user_name}</a> кинул(-а) снежок в <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')
    if message.text.lower() in ["прижать", "Прижать"]:
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
       reply_user_name = reply_user_name[0]
       reply = message.reply_to_message
       user_id = message.from_user.id
       reply_user_id = message.reply_to_message.from_user.id
       if reply:
          replyuser = reply.from_user
          await bot.send_message(message.chat.id, f"🤲 | <a href='tg://user?id={user_id}'>{user_name}</a> прижал(-а) <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')
    if message.text.lower() in ["похлопать", "Похлопать"]:
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
       reply_user_name = reply_user_name[0]
       reply = message.reply_to_message
       user_id = message.from_user.id
       reply_user_id = message.reply_to_message.from_user.id
       if reply:
          replyuser = reply.from_user
          await bot.send_message(message.chat.id, f"👏 | <a href='tg://user?id={user_id}'>{user_name}</a> похлопал(-а) <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')
    if message.text.lower() in ["изнасиловать", "Изнасиловать"]:
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
       reply_user_name = reply_user_name[0]
       reply = message.reply_to_message
       user_id = message.from_user.id
       reply_user_id = message.reply_to_message.from_user.id
       if reply:
          replyuser = reply.from_user
          await bot.send_message(message.chat.id, f"👉👌 | <a href='tg://user?id={user_id}'>{user_name}</a> изнасиловал(-а) <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')
    if message.text.lower() in ["пригласить на чай", "Пригласить на чай"]:
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
       reply_user_name = reply_user_name[0]
       reply = message.reply_to_message
       user_id = message.from_user.id
       reply_user_id = message.reply_to_message.from_user.id
       if reply:
          replyuser = reply.from_user
          await bot.send_message(message.chat.id, f"☕️ | <a href='tg://user?id={user_id}'>{user_name}</a> пригласил(-а) на чай <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')
    if message.text.lower() in ["убить", "Убить"]:
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
       reply_user_name = reply_user_name[0]
       reply = message.reply_to_message
       user_id = message.from_user.id
       reply_user_id = message.reply_to_message.from_user.id
       if reply:
          replyuser = reply.from_user
          await bot.send_message(message.chat.id, f"🔪 | <a href='tg://user?id={user_id}'>{user_name}</a> убил(-а) <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')
    if message.text.lower() in ["уебать", "Уебать"]:
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
       reply_user_name = reply_user_name[0]
       reply = message.reply_to_message
       user_id = message.from_user.id
       reply_user_id = message.reply_to_message.from_user.id
       if reply:
          replyuser = reply.from_user
          await bot.send_message(message.chat.id, f"🤜 | <a href='tg://user?id={user_id}'>{user_name}</a> уебал(-а) <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')
    if message.text.lower() in ["украсть", "Украсть"]:
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
       reply_user_name = reply_user_name[0]
       reply = message.reply_to_message
       user_id = message.from_user.id
       reply_user_id = message.reply_to_message.from_user.id
       if reply:
          replyuser = reply.from_user
          await bot.send_message(message.chat.id, f"💰 | <a href='tg://user?id={user_id}'>{user_name}</a> украл(-а) <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')

    if message.text.lower() in ["отсосать", "Отсосать"]:
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
       reply_user_name = reply_user_name[0]
       reply = message.reply_to_message
       user_id = message.from_user.id
       reply_user_id = message.reply_to_message.from_user.id
       if reply:
          replyuser = reply.from_user
          await bot.send_message(message.chat.id, f"👅 | <a href='tg://user?id={user_id}'>{user_name}</a> отсосал(-а) <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')

    if message.text.lower() in ["отлизать", "Отлизать"]:
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
       reply_user_name = reply_user_name[0]
       reply = message.reply_to_message
       user_id = message.from_user.id
       reply_user_id = message.reply_to_message.from_user.id
       if reply:
          replyuser = reply.from_user
          await bot.send_message(message.chat.id, f"👅 | <a href='tg://user?id={user_id}'>{user_name}</a> отлизал(-а) <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')

    if message.text.lower() in ["выебать", "Выебать"]:
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
       reply_user_name = reply_user_name[0]
       reply = message.reply_to_message
       user_id = message.from_user.id
       reply_user_id = message.reply_to_message.from_user.id
       if reply:
          replyuser = reply.from_user
          await bot.send_message(message.chat.id, f"🔞 | <a href='tg://user?id={user_id}'>{user_name}</a> выебал(-а) <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')

    if message.text.lower() in ["сжечь", "Сжечь"]:
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
       reply_user_name = reply_user_name[0]
       reply = message.reply_to_message
       user_id = message.from_user.id
       reply_user_id = message.reply_to_message.from_user.id
       if reply:
          replyuser = reply.from_user
          await bot.send_message(message.chat.id, f"🔥 | <a href='tg://user?id={user_id}'>{user_name}</a> сжёг <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')

    if message.text.lower() in ["трахнуть", "Трахнуть"]:
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
       reply_user_name = reply_user_name[0]
       reply = message.reply_to_message
       user_id = message.from_user.id
       reply_user_id = message.reply_to_message.from_user.id
       if reply:
          replyuser = reply.from_user
          await bot.send_message(message.chat.id, f"🔞 | <a href='tg://user?id={user_id}'>{user_name}</a> трахнул(-а) <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>", parse_mode='html')


############################### ВДЗУ - ВЫДАЧА ДЕНЕГ ЗА УЧАСТНИКОВ ################################################
    if message.text.startswith('вдзу статус') or message.text.startswith('Вдзу статус'):

         user_id = message.from_user.id
         user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
         user_name = str(user_name[0])

         status = str(message.text.split()[2])

         if user_id == cfg.owner_id:
            if status == 'выкл':
               cursor.execute(f"UPDATE wdzy SET wdz ='off' WHERE chat_id={message.chat.id}")
               connect.commit()
               text = f'♻️ <b>ВДЗУ выключена </b>'
            elif status == 'вкл':
               cursor.execute(f"UPDATE wdzy SET wdz ='on' WHERE chat_id={message.chat.id}")
               connect.commit()
               text = f'♻️ <b>ВДЗУ включена </b>'
            else:
               text = f'❗️ Не распознано «<b>{status}</b>» | Пример: <code>вдзу</code> <i>[выкл/вкл]</i>'

            await message.reply(text, parse_mode='html')
         else:
            return await message.reply(f'❗️ Данная команда доступна только <b>владельцу бота</b>', parse_mode='html')

    if message.text.startswith('вдзу сумма') or message.text.startswith('Вдзу сумма'):

         user_id = message.from_user.id
         user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
         user_name = str(user_name[0])

         su = message.text.split()[2]
         su2 = (su).replace(' ', '').replace('k', '000').replace('е','e').replace('к', '000').replace(',', '').replace('.', '')
         su3 = float(su2)
         summ = int(su3)

         if user_id == cfg.owner_id:
            cursor.execute(f'UPDATE wdzy SET summ = {summ} WHERE chat_id={message.chat.id}')
            connect.commit()

            text = f'''
♻️ <b>Обновлена</b> сумма за 1 участника - <code>{'{:,}'.format(summ).replace(',','.')}¢</code>
            '''
            await message.reply(text, parse_mode='html')
         else:
            return await message.reply(f'❗️ Данная команда доступна только <b>владельцу бота</b>', parse_mode='html')


    if message.text.startswith('!чат') or message.text.startswith('!Чат'):
         user_id = message.from_user.id

         if user_id == cfg.owner_id:
            if message.text.split()[1]=="бинд":
               wdz=cursor.execute(f"SELECT wdz FROM wdzy WHERE chat_id={message.chat.id}")
               wdz=cursor.fetchone()
               if wdz is None:
                   wdz="off"
                   cursor.execute(f'INSERT INTO wdzy VALUES (?, ?, ?, ?);', (100, wdz, message.chat.id,0,))
                   connect.commit()
                   text = f'''♻️ <b>ВДЗУ привязана к чату </b>'''
                   await message.reply(text, parse_mode='html')

            if message.text.split()[1]=="анбинд":
            	cursor.execute(f"SELECT wdz FROM wdzy WHERE chat_id={message.chat.id}")
            	if cursor.fetchone != None:
            		cursor.execute("DELETE FROM wdzy WHERE chat_id= ?", (message.chat.id,))
            		connect.commit()
            		text = f'''♻️ <b>ВДЗУ отвязана от чата </b>'''
            		await message.reply(text, parse_mode='html')


###############################################БРАК############################################ 
    if message.text.lower() in ["Брак", "брак"]:
       data = await get_rang(message)
       if data is None:
          return await message.reply(f"🚫 <b>Не найден в базе данных.</b>\n\n"
                                   f"/start в лс у бота!")
       user = message.from_user
       usid = user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(usid,)).fetchone()
       user_name = user_name[0]
       reply = message.reply_to_message
       if reply:
          replyuser = reply.from_user
          rid = replyuser.id
          ruser_name = cursor.execute("SELECT user_name from users where user_id = ?",(rid,)).fetchone()
          ruser_name = ruser_name[0] 
          if data[36] == 0:
             if replyuser.id == user.id:
                return await message.reply(f"ℹ️ | Вы не можете сделать брак с самим собой.")
             replydata = await reply_get_rang(message)
             if replydata[36] == 0:
                marry_me.append(user.id)
                marry_rep.append(replyuser.id)
                await bot.send_message(message.chat.id, f"💍 <a href='tg://user?id={rid}'>{ruser_name}</a>, минуточку внимания.\n💖 <a href='tg://user?id={usid}'>{user_name}</a> сделал вам предложение руки и сердца.\n😍 Принять решение можно нажав на одну из кнопок ниже.",  parse_mode='html' , reply_markup=button_marry)
             else:
                replyuser = reply.from_user
                rid = replyuser.id
                repuser_name = cursor.execute("SELECT user_name from users where user_id = ?",(rid,)).fetchone()
                repuser_name = repuser_name[0]
                marry = cursor.execute("SELECT marry FROM users WHERE user_id=?", (rid,)).fetchall()
                marry1 = int(marry[0][0])
                m_name = cursor.execute("SELECT user_name from users where user_id = ?",(marry1,)).fetchone()
                m_name = m_name[0]
                return await message.reply(f"ℹ️ | <a href='tg://user?id={rid}'>{repuser_name}</a> уже находится в браке с <a href='tg://user?id={marry1}'>{m_name}</a>!",  parse_mode='html')
          else:
            user = message.from_user
            usid = user.id
            marry = cursor.execute("SELECT marry FROM users WHERE user_id=?", (usid,)).fetchall()
            marry1 = int(marry[0][0])
            m_name = cursor.execute("SELECT user_name from users where user_id = ?",(marry1,)).fetchone()
            m_name = m_name[0]
            return await message.reply(f"ℹ️ | Вы уже находитесь в браке с <a href='tg://user?id={marry1}'>{m_name}</a>!",  parse_mode='html')

    if message.text.lower() in ["Развод", "развод"]:
       data = await get_rang(message)
       if data is None:
          return await message.reply(f"🚫 <b>Не найден в базе данных.</b>\n\n"
                                     f"/start в лс у бота!")
       user = message.from_user
       name = quote_html(user.full_name)
       if data[36] == 0:
          return await message.reply(f"ℹ️ Вы не состоите не с кем в браке!")
       else:
          marry = cursor.execute("SELECT marry FROM users WHERE user_id=?", (user.id,)).fetchall()
          marred = await bot.get_chat(str(marry[0][0]))
          mname = quote_html(marred.full_name)
          divorce_me.append(user.id)
          divorce_rep.append(marred.id)
          await bot.send_message(message.chat.id, f"📝 Убедить что вы согласны разводится.\n💔 Принять решение можно нажав на одну из кнопок ниже.",  parse_mode='html', reply_markup=button_divorce)

    if message.text.lower() in ["Мой брак", "мой брак"]:
       data = await get_rang(message)
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id
       if data[36] == 0:
          await bot.send_message(message.chat.id, f"💔 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы пока не состоите ни с кем в браке",  parse_mode='html')
       else:
          marry = cursor.execute("SELECT marry FROM users WHERE user_id = ?",(message.from_user.id,)).fetchone()
          marry = int(marry[0])
          mname = cursor.execute("SELECT user_name FROM users WHERE user_id=?", (marry,)).fetchone()
          mname = mname[0]

          get = cursor.execute("SELECT marry_date FROM users WHERE user_id=?", (message.from_user.id,)).fetchall()
          date_time = datetime.fromisoformat(get[0][0])
          times = date_time.strftime( "%d.%m.%Y %H:%M:%S" ) 
          await bot.send_message(message.chat.id, f"❤️ Брак между <a href='tg://user?id={user_id}'>{user_name}</a> и <a href='tg://user?id={marry}'>{mname}</a>:\n📆 Зарегистрирован: {times}",  parse_mode='html')


######################################ПИТОМЦЫ#################################################
    if message.text.lower() in ["питомцы", "Питомцы"]:
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       chat_id = message.chat.id
       user_id = message.from_user.id
       await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, доступные питомцы:\n🐥 1. Цыплёнок - 1.000.000¢\n🐈 2. Кот - 100.000.000¢\n🐕 3. Пёс - 500.000.000¢\n🦜 4. Попугай - 1.000.000.000¢\n🦄 5. Единорог - 50.000.000.000¢\n🐒 6. Обезьяна - 100.000.000.000¢\n🐬 7. Дельфин - 500.000.000.000¢\n🐅 8. Тигр - 10.000.000.000.000¢\n🐉 9. Дракон - 100.000.000.000.000¢\n\n🛒 Для покупки питомца введите: Купить питомца [номер]\nℹ Для просмотра информации о своем питомце введите: Мой питомец", parse_mode='html')

    if message.text.lower() in ["купить питомца 1", "Купить питомца 1"]:     
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       pet1 = cursor.execute("SELECT pet1 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet1 = int(pet1[0])
       pet2 = cursor.execute("SELECT pet2 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet2 = int(pet2[0])
       pet3 = cursor.execute("SELECT pet3 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet3 = int(pet3[0])
       pet4 = cursor.execute("SELECT pet4 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet4 = int(pet4[0])
       pet5 = cursor.execute("SELECT pet5 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet5 = int(pet5[0])
       pet6 = cursor.execute("SELECT pet6 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet6 = int(pet6[0])
       pet7 = cursor.execute("SELECT pet7 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet7 = int(pet7[0])
       pet8 = cursor.execute("SELECT pet8 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet8 = int(pet8[0])
       pet9 = cursor.execute("SELECT pet9 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet9 = int(pet9[0])
       pet_name = cursor.execute("SELECT pet_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet_name = str(pet_name[0])
       pet_hp = cursor.execute("SELECT pet_hp from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet_hp = int(pet_hp[0])
       pet_eat = cursor.execute("SELECT pet_eat from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet_eat = int(pet_eat[0])
       pet_mood = cursor.execute("SELECT pet_mood from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet_mood = int(pet_mood[0])
       chat_id = message.chat.id
       msg = message
       loser = ['😔', '😕', '😣', '😞', '😢']
       rloser = random.choice(loser)
       user_id = msg.from_user.id
       balance = cursor.execute("SELECT balance from users where user_id = ?",(message.from_user.id,)).fetchone()
       balance = round(int(balance[0]))
       summ = 1000000
       c = 1
       pets = pet1 + pet2 + pet3 + pet4 + pet5 + pet6 + pet7 + pet8 + pet9
       checking = cursor.execute("SELECT checking from users where user_id = ?", (message.from_user.id,)).fetchone()
       checking = round(int(checking[0]))
       if checking == 1:
          await bot.send_message(chat_id, f'ℹ | Дождитесь окончания игры! {rloser}', parse_mode='html')
          return
       checking1 = cursor.execute("SELECT checking1 from users where user_id = ?", (message.from_user.id,)).fetchone()
       checking1 = round(int(checking1[0]))
       if checking1 == 1:
          await bot.send_message(chat_id, f'ℹ | Дождитесь окончания игры! {rloser}', parse_mode='html')
          return
       checking2 = cursor.execute("SELECT checking2 from users where user_id = ?", (message.from_user.id,)).fetchone()
       checking2 = round(int(checking2[0]))
       if checking2 == 1:
          await bot.send_message(chat_id, f'ℹ | Дождитесь окончания игры! {rloser}', parse_mode='html')
          return
       checking3 = cursor.execute("SELECT checking3 from users where user_id = ?", (message.from_user.id,)).fetchone()
       checking3 = round(int(checking3[0]))
       if checking3 == 1:
          await bot.send_message(chat_id, f'ℹ | Дождитесь окончания игры! {rloser}', parse_mode='html')
          return
       if int(pets) == 0:
          if pet1 == 0:
             if int(balance) >= int(summ):
                await bot.send_message(message.chat.id, f"🐥 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно купили цыплёнка за 1.000.000¢ 🎉", parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = "{user_id}"') 
                cursor.execute(f'UPDATE users SET pet1 = {pet1 + c} WHERE user_id = "{user_id}"') 
                cursor.execute(f'UPDATE users SET pet_hp = {100} WHERE user_id = "{user_id}"') 
                cursor.execute(f'UPDATE users SET pet_eat = {100} WHERE user_id = "{user_id}"') 
                cursor.execute(f'UPDATE users SET pet_mood = {100} WHERE user_id = "{user_id}"') 
                connect.commit()    
                return
             else:
                await bot.send_message(message.chat.id, f"💰 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств! {rloser}", parse_mode='html')
                return
          if pet1 == 1:
             await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас уже есть данный питомец! {rloser}", parse_mode='html')     
             return
       if pets == 1:
          await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас уже есть питомец! {rloser}", parse_mode='html')     

    if message.text.lower() in ["купить питомца 2", "Купить питомца 2"]:    
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       pet1 = cursor.execute("SELECT pet1 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet1 = int(pet1[0])
       pet2 = cursor.execute("SELECT pet2 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet2 = int(pet2[0])
       pet3 = cursor.execute("SELECT pet3 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet3 = int(pet3[0])
       pet4 = cursor.execute("SELECT pet4 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet4 = int(pet4[0])
       pet5 = cursor.execute("SELECT pet5 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet5 = int(pet5[0])
       pet6 = cursor.execute("SELECT pet6 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet6 = int(pet6[0])
       pet7 = cursor.execute("SELECT pet7 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet7 = int(pet7[0])
       pet8 = cursor.execute("SELECT pet8 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet8 = int(pet8[0])
       pet9 = cursor.execute("SELECT pet9 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet9 = int(pet9[0])
       pet_name = cursor.execute("SELECT pet_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet_name = str(pet_name[0])
       pet_hp = cursor.execute("SELECT pet_hp from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet_hp = int(pet_hp[0])
       pet_eat = cursor.execute("SELECT pet_eat from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet_eat = int(pet_eat[0])
       pet_mood = cursor.execute("SELECT pet_mood from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet_mood = int(pet_mood[0])
       chat_id = message.chat.id
       msg = message
       loser = ['😔', '😕', '😣', '😞', '😢']
       rloser = random.choice(loser)
       user_id = msg.from_user.id
       balance = cursor.execute("SELECT balance from users where user_id = ?",(message.from_user.id,)).fetchone()
       balance = round(int(balance[0]))
       summ = 100000000
       c = 1
       pets = pet1 + pet2 + pet3 + pet4 + pet5 + pet6 + pet7 + pet8 + pet9
       checking = cursor.execute("SELECT checking from users where user_id = ?", (message.from_user.id,)).fetchone()
       checking = round(int(checking[0]))
       if checking == 1:
          await bot.send_message(chat_id, f'ℹ | Дождитесь окончания игры! {rloser}', parse_mode='html')
          return
       checking1 = cursor.execute("SELECT checking1 from users where user_id = ?", (message.from_user.id,)).fetchone()
       checking1 = round(int(checking1[0]))
       if checking1 == 1:
          await bot.send_message(chat_id, f'ℹ | Дождитесь окончания игры! {rloser}', parse_mode='html')
          return
       checking2 = cursor.execute("SELECT checking2 from users where user_id = ?", (message.from_user.id,)).fetchone()
       checking2 = round(int(checking2[0]))
       if checking2 == 1:
          await bot.send_message(chat_id, f'ℹ | Дождитесь окончания игры! {rloser}', parse_mode='html')
          return
       checking3 = cursor.execute("SELECT checking3 from users where user_id = ?", (message.from_user.id,)).fetchone()
       checking3 = round(int(checking3[0]))
       if checking3 == 1:
          await bot.send_message(chat_id, f'ℹ | Дождитесь окончания игры! {rloser}', parse_mode='html')
          return
       if int(pets) == 0:
          if pet2 == 0:
             if int(balance) >= int(summ):
                await bot.send_message(message.chat.id, f"🐈 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно купили кота за 100.000.000¢ 🎉", parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = "{user_id}"') 
                cursor.execute(f'UPDATE users SET pet2 = {pet2 + c} WHERE user_id = "{user_id}"') 
                cursor.execute(f'UPDATE users SET pet_hp = {100} WHERE user_id = "{user_id}"') 
                cursor.execute(f'UPDATE users SET pet_eat = {100} WHERE user_id = "{user_id}"') 
                cursor.execute(f'UPDATE users SET pet_mood = {100} WHERE user_id = "{user_id}"') 
                connect.commit()    
                return
             else:
                await bot.send_message(message.chat.id, f"💰 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств! {rloser}", parse_mode='html')
                return
          if pet2 == 1:
             await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас уже есть данный питомец! {rloser}", parse_mode='html')     
             return
       if pets == 1:
          await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас уже есть питомец! {rloser}", parse_mode='html')     

    if message.text.lower() in ["купить питомца 3", "Купить питомца 3"]:     
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       pet1 = cursor.execute("SELECT pet1 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet1 = int(pet1[0])
       pet2 = cursor.execute("SELECT pet2 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet2 = int(pet2[0])
       pet3 = cursor.execute("SELECT pet3 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet3 = int(pet3[0])
       pet4 = cursor.execute("SELECT pet4 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet4 = int(pet4[0])
       pet5 = cursor.execute("SELECT pet5 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet5 = int(pet5[0])
       pet6 = cursor.execute("SELECT pet6 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet6 = int(pet6[0])
       pet7 = cursor.execute("SELECT pet7 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet7 = int(pet7[0])
       pet8 = cursor.execute("SELECT pet8 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet8 = int(pet8[0])
       pet9 = cursor.execute("SELECT pet9 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet9 = int(pet9[0])
       pet_name = cursor.execute("SELECT pet_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet_name = str(pet_name[0])
       pet_hp = cursor.execute("SELECT pet_hp from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet_hp = int(pet_hp[0])
       pet_eat = cursor.execute("SELECT pet_eat from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet_eat = int(pet_eat[0])
       pet_mood = cursor.execute("SELECT pet_mood from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet_mood = int(pet_mood[0])
       chat_id = message.chat.id
       msg = message
       loser = ['😔', '😕', '😣', '😞', '😢']
       rloser = random.choice(loser)
       user_id = msg.from_user.id
       balance = cursor.execute("SELECT balance from users where user_id = ?",(message.from_user.id,)).fetchone()
       balance = round(int(balance[0]))
       summ = 500000000
       c = 1
       pets = pet1 + pet2 + pet3 + pet4 + pet5 + pet6 + pet7 + pet8 + pet9
       checking = cursor.execute("SELECT checking from users where user_id = ?", (message.from_user.id,)).fetchone()
       checking = round(int(checking[0]))
       if checking == 1:
          await bot.send_message(chat_id, f'ℹ | Дождитесь окончания игры! {rloser}', parse_mode='html')
          return
       checking1 = cursor.execute("SELECT checking1 from users where user_id = ?", (message.from_user.id,)).fetchone()
       checking1 = round(int(checking1[0]))
       if checking1 == 1:
          await bot.send_message(chat_id, f'ℹ | Дождитесь окончания игры! {rloser}', parse_mode='html')
          return
       checking2 = cursor.execute("SELECT checking2 from users where user_id = ?", (message.from_user.id,)).fetchone()
       checking2 = round(int(checking2[0]))
       if checking2 == 1:
          await bot.send_message(chat_id, f'ℹ | Дождитесь окончания игры! {rloser}', parse_mode='html')
          return
       checking3 = cursor.execute("SELECT checking3 from users where user_id = ?", (message.from_user.id,)).fetchone()
       checking3 = round(int(checking3[0]))
       if checking3 == 1:
          await bot.send_message(chat_id, f'ℹ | Дождитесь окончания игры! {rloser}', parse_mode='html')
          return
       if int(pets) == 0:
          if pet3 == 0:
             if int(balance) >= int(summ):
                await bot.send_message(message.chat.id, f"🐕 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно купили пса за 500.000.000¢ 🎉", parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = "{user_id}"') 
                cursor.execute(f'UPDATE users SET pet_hp = {100} WHERE user_id = "{user_id}"') 
                cursor.execute(f'UPDATE users SET pet_eat = {100} WHERE user_id = "{user_id}"') 
                cursor.execute(f'UPDATE users SET pet_mood = {100} WHERE user_id = "{user_id}"') 
                cursor.execute(f'UPDATE users SET pet3 = {pet3 + c} WHERE user_id = "{user_id}"') 
                connect.commit()    
                return
             else:
                await bot.send_message(message.chat.id, f"💰 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств! {rloser}", parse_mode='html')
                return
          if pet3 == 1:
             await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас уже есть данный питомец! {rloser}", parse_mode='html')     
             return
       if pets == 1:
          await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас уже есть питомец! {rloser}", parse_mode='html') 

    if message.text.lower() in ["купить питомца 4", "Купить питомца 4"]:   
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       pet1 = cursor.execute("SELECT pet1 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet1 = int(pet1[0])
       pet2 = cursor.execute("SELECT pet2 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet2 = int(pet2[0])
       pet3 = cursor.execute("SELECT pet3 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet3 = int(pet3[0])
       pet4 = cursor.execute("SELECT pet4 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet4 = int(pet4[0])
       pet5 = cursor.execute("SELECT pet5 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet5 = int(pet5[0])
       pet6 = cursor.execute("SELECT pet6 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet6 = int(pet6[0])
       pet7 = cursor.execute("SELECT pet7 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet7 = int(pet7[0])
       pet8 = cursor.execute("SELECT pet8 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet8 = int(pet8[0])
       pet9 = cursor.execute("SELECT pet9 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet9 = int(pet9[0])
       pet_name = cursor.execute("SELECT pet_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet_name = str(pet_name[0])
       pet_hp = cursor.execute("SELECT pet_hp from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet_hp = int(pet_hp[0])
       pet_eat = cursor.execute("SELECT pet_eat from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet_eat = int(pet_eat[0])
       pet_mood = cursor.execute("SELECT pet_mood from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet_mood = int(pet_mood[0])
       chat_id = message.chat.id
       msg = message
       loser = ['😔', '😕', '😣', '😞', '😢']
       rloser = random.choice(loser)
       user_id = msg.from_user.id
       balance = cursor.execute("SELECT balance from users where user_id = ?",(message.from_user.id,)).fetchone()
       balance = round(int(balance[0]))
       summ = 1000000000
       c = 1
       pets = pet1 + pet2 + pet3 + pet4 + pet5 + pet6 + pet7 + pet8 + pet9
       checking = cursor.execute("SELECT checking from users where user_id = ?", (message.from_user.id,)).fetchone()
       checking = round(int(checking[0]))
       if checking == 1:
          await bot.send_message(chat_id, f'ℹ | Дождитесь окончания игры! {rloser}', parse_mode='html')
          return
       checking1 = cursor.execute("SELECT checking1 from users where user_id = ?", (message.from_user.id,)).fetchone()
       checking1 = round(int(checking1[0]))
       if checking1 == 1:
          await bot.send_message(chat_id, f'ℹ | Дождитесь окончания игры! {rloser}', parse_mode='html')
          return
       checking2 = cursor.execute("SELECT checking2 from users where user_id = ?", (message.from_user.id,)).fetchone()
       checking2 = round(int(checking2[0]))
       if checking2 == 1:
          await bot.send_message(chat_id, f'ℹ | Дождитесь окончания игры! {rloser}', parse_mode='html')
          return
       checking3 = cursor.execute("SELECT checking3 from users where user_id = ?", (message.from_user.id,)).fetchone()
       checking3 = round(int(checking3[0]))
       if checking3 == 1:
          await bot.send_message(chat_id, f'ℹ | Дождитесь окончания игры! {rloser}', parse_mode='html')
          return
       if int(pets) == 0:
          if pet4 == 0:
             if int(balance) >= int(summ):
                await bot.send_message(message.chat.id, f"🦜 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно купили попугая за 1.000.000.000¢ 🎉", parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = "{user_id}"') 
                cursor.execute(f'UPDATE users SET pet4 = {pet4 + c} WHERE user_id = "{user_id}"') 
                cursor.execute(f'UPDATE users SET pet_hp = {100} WHERE user_id = "{user_id}"') 
                cursor.execute(f'UPDATE users SET pet_eat = {100} WHERE user_id = "{user_id}"') 
                cursor.execute(f'UPDATE users SET pet_mood = {100} WHERE user_id = "{user_id}"') 
                connect.commit()    
                return
             else:
                await bot.send_message(message.chat.id, f"💰 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств! {rloser}", parse_mode='html')
                return
          if pet4 == 1:
             await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас уже есть данный питомец! {rloser}", parse_mode='html')     
             return
       if pets == 1:
          await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас уже есть питомец! {rloser}", parse_mode='html') 

    if message.text.lower() in ["купить питомца 5", "Купить питомца 5"]:     
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       pet1 = cursor.execute("SELECT pet1 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet1 = int(pet1[0])
       pet2 = cursor.execute("SELECT pet2 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet2 = int(pet2[0])
       pet3 = cursor.execute("SELECT pet3 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet3 = int(pet3[0])
       pet4 = cursor.execute("SELECT pet4 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet4 = int(pet4[0])
       pet5 = cursor.execute("SELECT pet5 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet5 = int(pet5[0])
       pet6 = cursor.execute("SELECT pet6 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet6 = int(pet6[0])
       pet7 = cursor.execute("SELECT pet7 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet7 = int(pet7[0])
       pet8 = cursor.execute("SELECT pet8 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet8 = int(pet8[0])
       pet9 = cursor.execute("SELECT pet9 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet9 = int(pet9[0])
       pet_name = cursor.execute("SELECT pet_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet_name = str(pet_name[0])
       pet_hp = cursor.execute("SELECT pet_hp from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet_hp = int(pet_hp[0])
       pet_eat = cursor.execute("SELECT pet_eat from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet_eat = int(pet_eat[0])
       pet_mood = cursor.execute("SELECT pet_mood from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet_mood = int(pet_mood[0])
       chat_id = message.chat.id
       msg = message
       loser = ['😔', '😕', '😣', '😞', '😢']
       rloser = random.choice(loser)
       user_id = msg.from_user.id
       balance = cursor.execute("SELECT balance from users where user_id = ?",(message.from_user.id,)).fetchone()
       balance = round(int(balance[0]))
       summ = 50000000000
       c = 1
       pets = pet1 + pet2 + pet3 + pet4 + pet5 + pet6 + pet7 + pet8 + pet9
       checking = cursor.execute("SELECT checking from users where user_id = ?", (message.from_user.id,)).fetchone()
       checking = round(int(checking[0]))
       if checking == 1:
          await bot.send_message(chat_id, f'ℹ | Дождитесь окончания игры! {rloser}', parse_mode='html')
          return
       checking1 = cursor.execute("SELECT checking1 from users where user_id = ?", (message.from_user.id,)).fetchone()
       checking1 = round(int(checking1[0]))
       if checking1 == 1:
          await bot.send_message(chat_id, f'ℹ | Дождитесь окончания игры! {rloser}', parse_mode='html')
          return
       checking2 = cursor.execute("SELECT checking2 from users where user_id = ?", (message.from_user.id,)).fetchone()
       checking2 = round(int(checking2[0]))
       if checking2 == 1:
          await bot.send_message(chat_id, f'ℹ | Дождитесь окончания игры! {rloser}', parse_mode='html')
          return
       checking3 = cursor.execute("SELECT checking3 from users where user_id = ?", (message.from_user.id,)).fetchone()
       checking3 = round(int(checking3[0]))
       if checking3 == 1:
          await bot.send_message(chat_id, f'ℹ | Дождитесь окончания игры! {rloser}', parse_mode='html')
          return
       if int(pets) == 0:
          if pet5 == 0:
             if int(balance) >= int(summ):
                await bot.send_message(message.chat.id, f"🦄 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно купили единорога за 50.000.000.000¢ 🎉", parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = "{user_id}"') 
                cursor.execute(f'UPDATE users SET pet5 = {pet5 + c} WHERE user_id = "{user_id}"') 
                cursor.execute(f'UPDATE users SET pet_hp = {100} WHERE user_id = "{user_id}"') 
                cursor.execute(f'UPDATE users SET pet_eat = {100} WHERE user_id = "{user_id}"') 
                cursor.execute(f'UPDATE users SET pet_mood = {100} WHERE user_id = "{user_id}"') 
                connect.commit()    
                return
             else:
                await bot.send_message(message.chat.id, f"💰 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств! {rloser}", parse_mode='html')
                return
          if pet5 == 1:
             await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас уже есть данный питомец! {rloser}", parse_mode='html')     
             return
       if pets == 1:
          await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас уже есть питомец! {rloser}", parse_mode='html')  

    if message.text.lower() in ["купить питомца 6", "Купить питомца 6"]:      
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       pet1 = cursor.execute("SELECT pet1 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet1 = int(pet1[0])
       pet2 = cursor.execute("SELECT pet2 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet2 = int(pet2[0])
       pet3 = cursor.execute("SELECT pet3 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet3 = int(pet3[0])
       pet4 = cursor.execute("SELECT pet4 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet4 = int(pet4[0])
       pet5 = cursor.execute("SELECT pet5 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet5 = int(pet5[0])
       pet6 = cursor.execute("SELECT pet6 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet6 = int(pet6[0])
       pet7 = cursor.execute("SELECT pet7 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet7 = int(pet7[0])
       pet8 = cursor.execute("SELECT pet8 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet8 = int(pet8[0])
       pet9 = cursor.execute("SELECT pet9 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet9 = int(pet9[0])
       pet_name = cursor.execute("SELECT pet_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet_name = str(pet_name[0])
       pet_hp = cursor.execute("SELECT pet_hp from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet_hp = int(pet_hp[0])
       pet_eat = cursor.execute("SELECT pet_eat from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet_eat = int(pet_eat[0])
       pet_mood = cursor.execute("SELECT pet_mood from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet_mood = int(pet_mood[0])
       chat_id = message.chat.id
       msg = message
       loser = ['😔', '😕', '😣', '😞', '😢']
       rloser = random.choice(loser)
       user_id = msg.from_user.id
       balance = cursor.execute("SELECT balance from users where user_id = ?",(message.from_user.id,)).fetchone()
       balance = round(int(balance[0]))
       summ = 100000000000
       c = 1
       pets = pet1 + pet2 + pet3 + pet4 + pet5 + pet6 + pet7 + pet8 + pet9
       checking = cursor.execute("SELECT checking from users where user_id = ?", (message.from_user.id,)).fetchone()
       checking = round(int(checking[0]))
       if checking == 1:
          await bot.send_message(chat_id, f'ℹ | Дождитесь окончания игры! {rloser}', parse_mode='html')
          return
       checking1 = cursor.execute("SELECT checking1 from users where user_id = ?", (message.from_user.id,)).fetchone()
       checking1 = round(int(checking1[0]))
       if checking1 == 1:
          await bot.send_message(chat_id, f'ℹ | Дождитесь окончания игры! {rloser}', parse_mode='html')
          return
       checking2 = cursor.execute("SELECT checking2 from users where user_id = ?", (message.from_user.id,)).fetchone()
       checking2 = round(int(checking2[0]))
       if checking2 == 1:
          await bot.send_message(chat_id, f'ℹ | Дождитесь окончания игры! {rloser}', parse_mode='html')
          return
       checking3 = cursor.execute("SELECT checking3 from users where user_id = ?", (message.from_user.id,)).fetchone()
       checking3 = round(int(checking3[0]))
       if checking3 == 1:
          await bot.send_message(chat_id, f'ℹ | Дождитесь окончания игры! {rloser}', parse_mode='html')
          return
       if int(pets) == 0:
          if pet6 == 0:
             if int(balance) >= int(summ):
                await bot.send_message(message.chat.id, f"🐒 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно купили обезьяну за 100.000.000.000¢ 🎉", parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = "{user_id}"') 
                cursor.execute(f'UPDATE users SET pet6 = {pet6 + c} WHERE user_id = "{user_id}"') 
                cursor.execute(f'UPDATE users SET pet_hp = {100} WHERE user_id = "{user_id}"') 
                cursor.execute(f'UPDATE users SET pet_eat = {100} WHERE user_id = "{user_id}"') 
                cursor.execute(f'UPDATE users SET pet_mood = {100} WHERE user_id = "{user_id}"') 
                connect.commit()    
                return
             else:
                await bot.send_message(message.chat.id, f"💰 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств! {rloser}", parse_mode='html')
                return
          if pet6 == 1:
             await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас уже есть данный питомец! {rloser}", parse_mode='html')     
             return
       if pets == 1:
          await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас уже есть питомец! {rloser}", parse_mode='html')                        

    if message.text.lower() in ["купить питомца 7", "Купить питомца 7"]:    
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       pet1 = cursor.execute("SELECT pet1 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet1 = int(pet1[0])
       pet2 = cursor.execute("SELECT pet2 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet2 = int(pet2[0])
       pet3 = cursor.execute("SELECT pet3 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet3 = int(pet3[0])
       pet4 = cursor.execute("SELECT pet4 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet4 = int(pet4[0])
       pet5 = cursor.execute("SELECT pet5 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet5 = int(pet5[0])
       pet6 = cursor.execute("SELECT pet6 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet6 = int(pet6[0])
       pet7 = cursor.execute("SELECT pet7 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet7 = int(pet7[0])
       pet8 = cursor.execute("SELECT pet8 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet8 = int(pet8[0])
       pet9 = cursor.execute("SELECT pet9 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet9 = int(pet9[0])
       pet_name = cursor.execute("SELECT pet_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet_name = str(pet_name[0])
       pet_hp = cursor.execute("SELECT pet_hp from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet_hp = int(pet_hp[0])
       pet_eat = cursor.execute("SELECT pet_eat from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet_eat = int(pet_eat[0])
       pet_mood = cursor.execute("SELECT pet_mood from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet_mood = int(pet_mood[0])
       chat_id = message.chat.id
       msg = message
       loser = ['😔', '😕', '😣', '😞', '😢']
       rloser = random.choice(loser)
       user_id = msg.from_user.id
       balance = cursor.execute("SELECT balance from users where user_id = ?",(message.from_user.id,)).fetchone()
       balance = round(int(balance[0]))
       summ = 500000000000
       c = 1
       pets = pet1 + pet2 + pet3 + pet4 + pet5 + pet6 + pet7 + pet8 + pet9
       print(pets)
       checking = cursor.execute("SELECT checking from users where user_id = ?", (message.from_user.id,)).fetchone()
       checking = round(int(checking[0]))
       if checking == 1:
          await bot.send_message(chat_id, f'ℹ | Дождитесь окончания игры! {rloser}', parse_mode='html')
          return
       checking1 = cursor.execute("SELECT checking1 from users where user_id = ?", (message.from_user.id,)).fetchone()
       checking1 = round(int(checking1[0]))
       if checking1 == 1:
          await bot.send_message(chat_id, f'ℹ | Дождитесь окончания игры! {rloser}', parse_mode='html')
          return
       checking2 = cursor.execute("SELECT checking2 from users where user_id = ?", (message.from_user.id,)).fetchone()
       checking2 = round(int(checking2[0]))
       if checking2 == 1:
          await bot.send_message(chat_id, f'ℹ | Дождитесь окончания игры! {rloser}', parse_mode='html')
          return
       checking3 = cursor.execute("SELECT checking3 from users where user_id = ?", (message.from_user.id,)).fetchone()
       checking3 = round(int(checking3[0]))
       if checking3 == 1:
          await bot.send_message(chat_id, f'ℹ | Дождитесь окончания игры! {rloser}', parse_mode='html')
          return
       if int(pets) == 0:
          if pet7 == 0:
             if int(balance) >= int(summ):
                await bot.send_message(message.chat.id, f"🐬 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно купили дельфина за 500.000.000.000¢ 🎉", parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = "{user_id}"') 
                cursor.execute(f'UPDATE users SET pet7 = {pet7 + c} WHERE user_id = "{user_id}"') 
                cursor.execute(f'UPDATE users SET pet_hp = {100} WHERE user_id = "{user_id}"') 
                cursor.execute(f'UPDATE users SET pet_eat = {100} WHERE user_id = "{user_id}"') 
                cursor.execute(f'UPDATE users SET pet_mood = {100} WHERE user_id = "{user_id}"') 
                connect.commit()    
                return
             else:
                await bot.send_message(message.chat.id, f"💰 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств! {rloser}", parse_mode='html')
                return
          if pet7 == 1:
             await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас уже есть данный питомец! {rloser}", parse_mode='html')     
             return
       if pets == 1:
          await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас уже есть питомец! {rloser}", parse_mode='html') 

    if message.text.lower() in ["купить питомца 8", "Купить питомца 8"]:     
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       pet1 = cursor.execute("SELECT pet1 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet1 = int(pet1[0])
       pet2 = cursor.execute("SELECT pet2 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet2 = int(pet2[0])
       pet3 = cursor.execute("SELECT pet3 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet3 = int(pet3[0])
       pet4 = cursor.execute("SELECT pet4 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet4 = int(pet4[0])
       pet5 = cursor.execute("SELECT pet5 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet5 = int(pet5[0])
       pet6 = cursor.execute("SELECT pet6 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet6 = int(pet6[0])
       pet7 = cursor.execute("SELECT pet7 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet7 = int(pet7[0])
       pet8 = cursor.execute("SELECT pet8 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet8 = int(pet8[0])
       pet9 = cursor.execute("SELECT pet9 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet9 = int(pet9[0])
       pet_name = cursor.execute("SELECT pet_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet_name = str(pet_name[0])
       pet_hp = cursor.execute("SELECT pet_hp from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet_hp = int(pet_hp[0])
       pet_eat = cursor.execute("SELECT pet_eat from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet_eat = int(pet_eat[0])
       pet_mood = cursor.execute("SELECT pet_mood from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet_mood = int(pet_mood[0])
       chat_id = message.chat.id
       msg = message
       loser = ['😔', '😕', '😣', '😞', '😢']
       rloser = random.choice(loser)
       user_id = msg.from_user.id
       balance = cursor.execute("SELECT balance from users where user_id = ?",(message.from_user.id,)).fetchone()
       balance = round(int(balance[0]))
       summ = 10000000000000
       c = 1
       pets = pet1 + pet2 + pet3 + pet4 + pet5 + pet6 + pet7 + pet8 + pet9
       checking = cursor.execute("SELECT checking from users where user_id = ?", (message.from_user.id,)).fetchone()
       checking = round(int(checking[0]))
       if checking == 1:
          await bot.send_message(chat_id, f'ℹ | Дождитесь окончания игры! {rloser}', parse_mode='html')
          return
       checking1 = cursor.execute("SELECT checking1 from users where user_id = ?", (message.from_user.id,)).fetchone()
       checking1 = round(int(checking1[0]))
       if checking1 == 1:
          await bot.send_message(chat_id, f'ℹ | Дождитесь окончания игры! {rloser}', parse_mode='html')
          return
       checking2 = cursor.execute("SELECT checking2 from users where user_id = ?", (message.from_user.id,)).fetchone()
       checking2 = round(int(checking2[0]))
       if checking2 == 1:
          await bot.send_message(chat_id, f'ℹ | Дождитесь окончания игры! {rloser}', parse_mode='html')
          return
       checking3 = cursor.execute("SELECT checking3 from users where user_id = ?", (message.from_user.id,)).fetchone()
       checking3 = round(int(checking3[0]))
       if checking3 == 1:
          await bot.send_message(chat_id, f'ℹ | Дождитесь окончания игры! {rloser}', parse_mode='html')
          return
       if int(pets) == 0:
          if pet8 == 0:
             if int(balance) >= int(summ):
                await bot.send_message(message.chat.id, f"🐅 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно купили тигра за 10.000.000.000.000¢ 🎉", parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = "{user_id}"') 
                cursor.execute(f'UPDATE users SET pet8 = {pet8 + c} WHERE user_id = "{user_id}"') 
                cursor.execute(f'UPDATE users SET pet_hp = {100} WHERE user_id = "{user_id}"') 
                cursor.execute(f'UPDATE users SET pet_eat = {100} WHERE user_id = "{user_id}"') 
                cursor.execute(f'UPDATE users SET pet_mood = {100} WHERE user_id = "{user_id}"') 
                connect.commit()    
                return
             else:
                await bot.send_message(message.chat.id, f"💰 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств! {rloser}", parse_mode='html')
                return
          if pet8 == 1:
             await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас уже есть данный питомец! {rloser}", parse_mode='html')     
             return
       if pets == 1:
          await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас уже есть питомец! {rloser}", parse_mode='html') 

    if message.text.lower() in ["купить питомца 9", "Купить питомца 9"]:     
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       pet1 = cursor.execute("SELECT pet1 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet1 = int(pet1[0])
       pet2 = cursor.execute("SELECT pet2 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet2 = int(pet2[0])
       pet3 = cursor.execute("SELECT pet3 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet3 = int(pet3[0])
       pet4 = cursor.execute("SELECT pet4 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet4 = int(pet4[0])
       pet5 = cursor.execute("SELECT pet5 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet5 = int(pet5[0])
       pet6 = cursor.execute("SELECT pet6 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet6 = int(pet6[0])
       pet7 = cursor.execute("SELECT pet7 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet7 = int(pet7[0])
       pet8 = cursor.execute("SELECT pet8 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet8 = int(pet8[0])
       pet9 = cursor.execute("SELECT pet9 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet9 = int(pet9[0])
       pet_name = cursor.execute("SELECT pet_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet_name = str(pet_name[0])
       pet_hp = cursor.execute("SELECT pet_hp from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet_hp = int(pet_hp[0])
       pet_eat = cursor.execute("SELECT pet_eat from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet_eat = int(pet_eat[0])
       pet_mood = cursor.execute("SELECT pet_mood from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet_mood = int(pet_mood[0])
       chat_id = message.chat.id
       msg = message
       loser = ['😔', '😕', '😣', '😞', '😢']
       rloser = random.choice(loser)
       user_id = msg.from_user.id
       balance = cursor.execute("SELECT balance from users where user_id = ?",(message.from_user.id,)).fetchone()
       balance = round(int(balance[0]))
       summ = 100000000000000
       c = 1
       pets = pet1 + pet2 + pet3 + pet4 + pet5 + pet6 + pet7 + pet8 + pet9
       checking = cursor.execute("SELECT checking from users where user_id = ?", (message.from_user.id,)).fetchone()
       checking = round(int(checking[0]))
       if checking == 1:
          await bot.send_message(chat_id, f'ℹ | Дождитесь окончания игры! {rloser}', parse_mode='html')
          return
       checking1 = cursor.execute("SELECT checking1 from users where user_id = ?", (message.from_user.id,)).fetchone()
       checking1 = round(int(checking1[0]))
       if checking1 == 1:
          await bot.send_message(chat_id, f'ℹ | Дождитесь окончания игры! {rloser}', parse_mode='html')
          return
       checking2 = cursor.execute("SELECT checking2 from users where user_id = ?", (message.from_user.id,)).fetchone()
       checking2 = round(int(checking2[0]))
       if checking2 == 1:
          await bot.send_message(chat_id, f'ℹ | Дождитесь окончания игры! {rloser}', parse_mode='html')
          return
       checking3 = cursor.execute("SELECT checking3 from users where user_id = ?", (message.from_user.id,)).fetchone()
       checking3 = round(int(checking3[0]))
       if checking3 == 1:
          await bot.send_message(chat_id, f'ℹ | Дождитесь окончания игры! {rloser}', parse_mode='html')
          return
       if int(pets) == 0:
          if pet9 == 0:
             if int(balance) >= int(summ):
                await bot.send_message(message.chat.id, f"🐉 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно купили дракона за 100.000.000.000.000¢ 🎉", parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = "{user_id}"') 
                cursor.execute(f'UPDATE users SET pet9 = {pet9 + c} WHERE user_id = "{user_id}"') 
                cursor.execute(f'UPDATE users SET pet_hp = {100} WHERE user_id = "{user_id}"') 
                cursor.execute(f'UPDATE users SET pet_eat = {100} WHERE user_id = "{user_id}"') 
                cursor.execute(f'UPDATE users SET pet_mood = {100} WHERE user_id = "{user_id}"') 
                connect.commit()    
                return
             else:
                await bot.send_message(message.chat.id, f"💰 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств! {rloser}", parse_mode='html')
                return
          if pet9 == 1:
             await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас уже есть данный питомец! {rloser}", parse_mode='html')     
             return
       if pets == 1:
          await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас уже есть питомец! {rloser}", parse_mode='html') 

    if message.text.lower() in ["мой питомец", "Мой питомец"]:        
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       pet1 = cursor.execute("SELECT pet1 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet1 = int(pet1[0])
       pet2 = cursor.execute("SELECT pet2 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet2 = int(pet2[0])
       pet3 = cursor.execute("SELECT pet3 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet3 = int(pet3[0])
       pet4 = cursor.execute("SELECT pet4 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet4 = int(pet4[0])
       pet5 = cursor.execute("SELECT pet5 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet5 = int(pet5[0])
       pet6 = cursor.execute("SELECT pet6 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet6 = int(pet6[0])
       pet7 = cursor.execute("SELECT pet7 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet7 = int(pet7[0])
       pet8 = cursor.execute("SELECT pet8 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet8 = int(pet8[0])
       pet9 = cursor.execute("SELECT pet9 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet9 = int(pet9[0])
       pet10 = cursor.execute("SELECT pet10 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet10 = int(pet10[0])
       pet11 = cursor.execute("SELECT pet11 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet11 = int(pet11[0])
       pet_name = cursor.execute("SELECT pet_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet_name = str(pet_name[0])
       pet_hp = cursor.execute("SELECT pet_hp from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet_hp = int(pet_hp[0])
       pet_eat = cursor.execute("SELECT pet_eat from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet_eat = int(pet_eat[0])
       pet_mood = cursor.execute("SELECT pet_mood from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet_mood = int(pet_mood[0])
       chat_id = message.chat.id
       user_id = message.from_user.id
       loser = ['😔', '😕', '😣', '😞', '😢']
       rloser = random.choice(loser)
       pets = pet1 + pet2 + pet3 + pet4 + pet5 + pet6 + pet7 + pet8 + pet9 + pet10 + pet11
       if pets == 0:
          await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас нету питомца! {rloser}", parse_mode='html')    
       if pet1 == 1:
          photo = open('imges/pet1.jpg', 'rb')
          await message.bot.send_photo(chat_id=message.chat.id, photo=photo, caption=f"🐥 | <a href='tg://user?id={user_id}'>{user_name}</a>, ваш питомец: цыплёнок \n✏️ | Имя питомца: {pet_name}\n❤️ | ХП: {pet_hp} \n🍗 | Сытость: {pet_eat}\n☀️ | Настроение: {pet_mood} \n\n✏ | Питомец имя [имя] - изменить имя питомца\n❤ | Вылечить питомца - вылечить питомца\n🍗 | Покормить питомца - покормить питомца\n🌳 | Выгулять питомца - поднять настроение питомцу", parse_mode='html')            
       if pet2 == 1:     
          photo = open('imges/pet2.jpg', 'rb')
          await message.bot.send_photo(chat_id=message.chat.id, photo=photo, caption=f"🐈 | <a href='tg://user?id={user_id}'>{user_name}</a>, ваш питомец: кот \n✏️ | Имя питомца: {pet_name}\n❤️ | ХП: {pet_hp} \n🍗 | Сытость: {pet_eat}\n☀️ | Настроение: {pet_mood} \n\n✏ | Питомец имя [имя] - изменить имя питомца\n❤ | Вылечить питомца - вылечить питомца\n🍗 | Покормить питомца - покормить питомца\n🌳 | Выгулять питомца - поднять настроение питомцу", parse_mode='html')                    
       if pet3 == 1:   
          photo = open('imges/pet3.jpg', 'rb')
          await message.bot.send_photo(chat_id=message.chat.id, photo=photo, caption=f"🐕 | <a href='tg://user?id={user_id}'>{user_name}</a>, ваш питомец: пёс \n✏️ | Имя питомца: {pet_name}\n❤️ | ХП: {pet_hp} \n🍗 | Сытость: {pet_eat}\n☀️ | Настроение: {pet_mood} \n\n✏ | Питомец имя [имя] - изменить имя питомца\n❤ | Вылечить питомца - вылечить питомца\n🍗 | Покормить питомца - покормить питомца\n🌳 | Выгулять питомца - поднять настроение питомцу", parse_mode='html')                            
       if pet4 == 1:           
          photo = open('imges/pet4.jpg', 'rb')
          await message.bot.send_photo(chat_id=message.chat.id, photo=photo, caption=f"🦜 | <a href='tg://user?id={user_id}'>{user_name}</a>, ваш питомец: попугай \n✏️ | Имя питомца: {pet_name}\n❤️ | ХП: {pet_hp} \n🍗 | Сытость: {pet_eat}\n☀️ | Настроение: {pet_mood} \n\n✏ | Питомец имя [имя] - изменить имя питомца\n❤ | Вылечить питомца - вылечить питомца\n🍗 | Покормить питомца - покормить питомца\n🌳 | Выгулять питомца - поднять настроение питомцу", parse_mode='html')                            
       if pet5 == 1:
          photo = open('imges/pet5.jpg', 'rb')
          await message.bot.send_photo(chat_id=message.chat.id, photo=photo, caption=f"🦄 | <a href='tg://user?id={user_id}'>{user_name}</a>, ваш питомец: единорог \n✏️ | Имя питомца: {pet_name}\n❤️ | ХП: {pet_hp} \n🍗 | Сытость: {pet_eat}\n☀️ | Настроение: {pet_mood} \n\n✏ | Питомец имя [имя] - изменить имя питомца\n❤ | Вылечить питомца - вылечить питомца\n🍗 | Покормить питомца - покормить питомца\n🌳 | Выгулять питомца - поднять настроение питомцу", parse_mode='html')                                       
       if pet6 == 1:
          photo = open('imges/pet6.jpg', 'rb')
          await message.bot.send_photo(chat_id=message.chat.id, photo=photo, caption=f"🐒 | <a href='tg://user?id={user_id}'>{user_name}</a>, ваш питомец: обезьяна \n✏️ | Имя питомца: {pet_name}\n❤️ | ХП: {pet_hp} \n🍗 | Сытость: {pet_eat}\n☀️ | Настроение: {pet_mood} \n\n✏ | Питомец имя [имя] - изменить имя питомца\n❤ | Вылечить питомца - вылечить питомца\n🍗 | Покормить питомца - покормить питомца\n🌳 | Выгулять питомца - поднять настроение питомцу", parse_mode='html')                                       
       if pet7 == 1:
          photo = open('imges/lpet7.jpg', 'rb')
          await message.bot.send_photo(chat_id=message.chat.id, photo=photo, caption=f"🐬 | <a href='tg://user?id={user_id}'>{user_name}</a>, ваш питомец: дельфин \n✏️ | Имя питомца: {pet_name}\n❤️ | ХП: {pet_hp} \n🍗 | Сытость: {pet_eat}\n☀️ | Настроение: {pet_mood} \n\n✏ | Питомец имя [имя] - изменить имя питомца\n❤ | Вылечить питомца - вылечить питомца\n🍗 | Покормить питомца - покормить питомца\n🌳 | Выгулять питомца - поднять настроение питомцу", parse_mode='html')                                       
       if pet8 == 1:
          photo = open('imges/pet8.jpg', 'rb')
          await message.bot.send_photo(chat_id=message.chat.id, photo=photo, caption=f"🐅 | <a href='tg://user?id={user_id}'>{user_name}</a>, ваш питомец: тигр \n✏️ | Имя питомца: {pet_name}\n❤️ | ХП: {pet_hp} \n🍗 | Сытость: {pet_eat}\n☀️ | Настроение: {pet_mood} \n\n✏ | Питомец имя [имя] - изменить имя питомца\n❤ | Вылечить питомца - вылечить питомца\n🍗 | Покормить питомца - покормить питомца\n🌳 | Выгулять питомца - поднять настроение питомцу", parse_mode='html')                                       
       if pet9 == 1: 
          photo = open('imges/pet9.jpg', 'rb')
          await message.bot.send_photo(chat_id=message.chat.id, photo=photo, caption=f"🐉 | <a href='tg://user?id={user_id}'>{user_name}</a>, ваш питомец: дракон \n✏️ | Имя питомца: {pet_name}\n❤️ | ХП: {pet_hp} \n🍗 | Сытость: {pet_eat}\n☀️ | Настроение: {pet_mood} \n\n✏ | Питомец имя [имя] - изменить имя питомца\n❤ | Вылечить питомца - вылечить питомца\n🍗 | Покормить питомца - покормить питомца\n🌳 | Выгулять питомца - поднять настроение питомцу", parse_mode='html')                                      
       if pet10 == 1:
          photo = open('imges/pet10.jpg', 'rb')
          await message.bot.send_photo(chat_id=message.chat.id, photo=photo, caption=f"☃️ | <a href='tg://user?id={user_id}'>{user_name}</a>, ваш питомец: снеговик \n✏️ | Имя питомца: {pet_name}\n❤️ | ХП: {pet_hp} \n🍗 | Сытость: {pet_eat}\n☀️ | Настроение: {pet_mood} \n\n✏ | Питомец имя [имя] - изменить имя питомца\n❤ | Вылечить питомца - вылечить питомца\n🍗 | Покормить питомца - покормить питомца\n🌳 | Выгулять питомца - поднять настроение питомцу", parse_mode='html')                                       
       if pet11 == 1:
          photo = open('imges/pet11.jpg', 'rb')
          await message.bot.send_photo(chat_id=message.chat.id, photo=photo, caption=f"🐰  | <a href='tg://user?id={user_id}'>{user_name}</a>, ваш питомец: пасхальный кролик \n✏️ | Имя питомца: {pet_name}\n❤️ | ХП: {pet_hp} \n🍗 | Сытость: {pet_eat}\n☀️ | Настроение: {pet_mood} \n\n✏ | Питомец имя [имя] - изменить имя питомца\n❤ | Вылечить питомца - вылечить питомца\n🍗 | Покормить питомца - покормить питомца\n🌳 | Выгулять питомца - поднять настроение питомцу", parse_mode='html') 

    if message.text.lower() in ["вылечить питомца", "Вылечить питомца"]:   
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       pet1 = cursor.execute("SELECT pet1 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet1 = int(pet1[0])
       pet2 = cursor.execute("SELECT pet2 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet2 = int(pet2[0])
       pet3 = cursor.execute("SELECT pet3 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet3 = int(pet3[0])
       pet4 = cursor.execute("SELECT pet4 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet4 = int(pet4[0])
       pet5 = cursor.execute("SELECT pet5 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet5 = int(pet5[0])
       pet6 = cursor.execute("SELECT pet6 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet6 = int(pet6[0])
       pet7 = cursor.execute("SELECT pet7 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet7 = int(pet7[0])
       pet8 = cursor.execute("SELECT pet8 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet8 = int(pet8[0])
       pet9 = cursor.execute("SELECT pet9 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet9 = int(pet9[0])
       pet10 = cursor.execute("SELECT pet10 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet10 = int(pet10[0])
       pet11 = cursor.execute("SELECT pet11 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet11 = int(pet11[0])
       pet_name = cursor.execute("SELECT pet_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet_name = str(pet_name[0])
       pet_hp = cursor.execute("SELECT pet_hp from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet_hp = int(pet_hp[0])
       pet_eat = cursor.execute("SELECT pet_eat from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet_eat = int(pet_eat[0])
       pet_mood = cursor.execute("SELECT pet_mood from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet_mood = int(pet_mood[0])
       chat_id = message.chat.id
       user_id = message.from_user.id
       loser = ['😔', '😕', '😣', '😞', '😢']
       rloser = random.choice(loser)
       balance = cursor.execute("SELECT balance from users where user_id = ?",(message.from_user.id,)).fetchone()
       balance = round(int(balance[0]))
       pets = pet1 + pet2 + pet3 + pet4 + pet5 + pet6 + pet7 + pet8 + pet9 + pet10 + pet11
       c = Decimal((100 - pet_hp) * 10000)
       c3 = '{0:,}'.format(c).replace(',', '.')
       c2 = (100 - pet_hp) * 10000
       hp = 100 - pet_hp
       checking = cursor.execute("SELECT checking from users where user_id = ?", (message.from_user.id,)).fetchone()
       checking = round(int(checking[0]))
       if checking == 1:
          await bot.send_message(chat_id, f'ℹ | Дождитесь окончания игры! {rloser}', parse_mode='html')
          return
       checking1 = cursor.execute("SELECT checking1 from users where user_id = ?", (message.from_user.id,)).fetchone()
       checking1 = round(int(checking1[0]))
       if checking1 == 1:
          await bot.send_message(chat_id, f'ℹ | Дождитесь окончания игры! {rloser}', parse_mode='html')
          return
       checking2 = cursor.execute("SELECT checking2 from users where user_id = ?", (message.from_user.id,)).fetchone()
       checking2 = round(int(checking2[0]))
       if checking2 == 1:
          await bot.send_message(chat_id, f'ℹ | Дождитесь окончания игры! {rloser}', parse_mode='html')
          return
       checking3 = cursor.execute("SELECT checking3 from users where user_id = ?", (message.from_user.id,)).fetchone()
       checking3 = round(int(checking3[0]))
       if checking3 == 1:
          await bot.send_message(chat_id, f'ℹ | Дождитесь окончания игры! {rloser}', parse_mode='html')
          return
       if pets == 0:
          await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас нету питомца! {rloser}", parse_mode='html')  
       if pet1 == 1:
          if pet_hp < 100:
             if c <= balance:
                await bot.send_message(message.chat.id, f"❤ | <a href='tg://user?id={user_id}'>{user_name}</a>, вы вылечили своего питомца за {c3}!", parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - c2} WHERE user_id = "{user_id}"') 
                cursor.execute(f'UPDATE users SET pet_hp = {pet_hp + hp} WHERE user_id = "{user_id}"')
             if c > balance:
                await bot.send_message(message.chat.id, f"💰 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств! {rloser}", parse_mode='html')
          if pet_hp == 100:
             await bot.send_message(message.chat.id, f"❤ | <a href='tg://user?id={user_id}'>{user_name}</a>, ваш питомец не нуждается в лечении!", parse_mode='html')
       if pet2 == 1:
          if pet_hp < 100:
             if c <= balance:
                await bot.send_message(message.chat.id, f"❤ | <a href='tg://user?id={user_id}'>{user_name}</a>, вы вылечили своего питомца за {c3}!", parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - c2} WHERE user_id = "{user_id}"') 
                cursor.execute(f'UPDATE users SET pet_hp = {pet_hp + hp} WHERE user_id = "{user_id}"')
             if c > balance:
                await bot.send_message(message.chat.id, f"💰 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств! {rloser}", parse_mode='html')
          if pet_hp == 100:
             await bot.send_message(message.chat.id, f"❤ | <a href='tg://user?id={user_id}'>{user_name}</a>, ваш питомец не нуждается в лечении!", parse_mode='html')
       if pet3 == 1:
          if pet_hp < 100:
             if c <= balance:
                await bot.send_message(message.chat.id, f"❤ | <a href='tg://user?id={user_id}'>{user_name}</a>, вы вылечили своего питомца за {c3}!", parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - c2} WHERE user_id = "{user_id}"') 
                cursor.execute(f'UPDATE users SET pet_hp = {pet_hp + hp} WHERE user_id = "{user_id}"')
             if c > balance:
                await bot.send_message(message.chat.id, f"💰 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств! {rloser}", parse_mode='html')
          if pet_hp == 100:
             await bot.send_message(message.chat.id, f"❤ | <a href='tg://user?id={user_id}'>{user_name}</a>, ваш питомец не нуждается в лечении!", parse_mode='html')
       if pet4 == 1:
          if pet_hp < 100:
             if c <= balance:
                await bot.send_message(message.chat.id, f"❤ | <a href='tg://user?id={user_id}'>{user_name}</a>, вы вылечили своего питомца за {c3}!", parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - c2} WHERE user_id = "{user_id}"') 
                cursor.execute(f'UPDATE users SET pet_hp = {pet_hp + hp} WHERE user_id = "{user_id}"')
             if c > balance:
                await bot.send_message(message.chat.id, f"💰 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств! {rloser}", parse_mode='html')
          if pet_hp == 100:
             await bot.send_message(message.chat.id, f"❤ | <a href='tg://user?id={user_id}'>{user_name}</a>, ваш питомец не нуждается в лечении!", parse_mode='html')
       if pet5 == 1:
          if pet_hp < 100:
             if c <= balance:
                await bot.send_message(message.chat.id, f"❤ | <a href='tg://user?id={user_id}'>{user_name}</a>, вы вылечили своего питомца за {c3}!", parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - c2} WHERE user_id = "{user_id}"') 
                cursor.execute(f'UPDATE users SET pet_hp = {pet_hp + hp} WHERE user_id = "{user_id}"')
             if c > balance:
                await bot.send_message(message.chat.id, f"💰 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств! {rloser}", parse_mode='html')
          if pet_hp == 100:
             await bot.send_message(message.chat.id, f"❤ | <a href='tg://user?id={user_id}'>{user_name}</a>, ваш питомец не нуждается в лечении!", parse_mode='html')
       if pet6 == 1:
          if pet_hp < 100:
             if c <= balance:
                await bot.send_message(message.chat.id, f"❤ | <a href='tg://user?id={user_id}'>{user_name}</a>, вы вылечили своего питомца за {c3}!", parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - c2} WHERE user_id = "{user_id}"') 
                cursor.execute(f'UPDATE users SET pet_hp = {pet_hp + hp} WHERE user_id = "{user_id}"')
             if c > balance:
                await bot.send_message(message.chat.id, f"💰 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств! {rloser}", parse_mode='html')
          if pet_hp == 100:
             await bot.send_message(message.chat.id, f"❤ | <a href='tg://user?id={user_id}'>{user_name}</a>, ваш питомец не нуждается в лечении!", parse_mode='html')
       if pet7 == 1:
          if pet_hp < 100:
             if c <= balance:
                await bot.send_message(message.chat.id, f"❤ | <a href='tg://user?id={user_id}'>{user_name}</a>, вы вылечили своего питомца за {c3}!", parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - c2} WHERE user_id = "{user_id}"') 
                cursor.execute(f'UPDATE users SET pet_hp = {pet_hp + hp} WHERE user_id = "{user_id}"')
             if c > balance:
                await bot.send_message(message.chat.id, f"💰 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств! {rloser}", parse_mode='html')
          if pet_hp == 100:
             await bot.send_message(message.chat.id, f"❤ | <a href='tg://user?id={user_id}'>{user_name}</a>, ваш питомец не нуждается в лечении!", parse_mode='html')
       if pet8 == 1:
          if pet_hp < 100:
             if c <= balance:
                await bot.send_message(message.chat.id, f"❤ | <a href='tg://user?id={user_id}'>{user_name}</a>, вы вылечили своего питомца за {c3}!", parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - c2} WHERE user_id = "{user_id}"') 
                cursor.execute(f'UPDATE users SET pet_hp = {pet_hp + hp} WHERE user_id = "{user_id}"')
             if c > balance:
                await bot.send_message(message.chat.id, f"💰 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств! {rloser}", parse_mode='html')
          if pet_hp == 100:
             await bot.send_message(message.chat.id, f"❤ | <a href='tg://user?id={user_id}'>{user_name}</a>, ваш питомец не нуждается в лечении!", parse_mode='html')
       if pet9 == 1:
          if pet_hp < 100:
             if c <= balance:
                await bot.send_message(message.chat.id, f"❤ | <a href='tg://user?id={user_id}'>{user_name}</a>, вы вылечили своего питомца за {c3}!", parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - c2} WHERE user_id = "{user_id}"') 
                cursor.execute(f'UPDATE users SET pet_hp = {pet_hp + hp} WHERE user_id = "{user_id}"')
             if c > balance:
                await bot.send_message(message.chat.id, f"💰 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств! {rloser}", parse_mode='html')
          if pet_hp == 100:
             await bot.send_message(message.chat.id, f"❤ | <a href='tg://user?id={user_id}'>{user_name}</a>, ваш питомец не нуждается в лечении!", parse_mode='html')
       if pet10 == 1:
          if pet_hp < 100:
             if c <= balance:
                await bot.send_message(message.chat.id, f"❤ | <a href='tg://user?id={user_id}'>{user_name}</a>, вы вылечили своего питомца за {c3}!", parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - c2} WHERE user_id = "{user_id}"') 
                cursor.execute(f'UPDATE users SET pet_hp = {pet_hp + hp} WHERE user_id = "{user_id}"')
             if c > balance:
                await bot.send_message(message.chat.id, f"💰 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств! {rloser}", parse_mode='html')
          if pet_hp == 100:
             await bot.send_message(message.chat.id, f"❤ | <a href='tg://user?id={user_id}'>{user_name}</a>, ваш питомец не нуждается в лечении!", parse_mode='html')
       if pet11 == 1:
          if pet_hp < 100:
             if c <= balance:
                await bot.send_message(message.chat.id, f"❤ | <a href='tg://user?id={user_id}'>{user_name}</a>, вы вылечили своего питомца за {c3}!", parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - c2} WHERE user_id = "{user_id}"') 
                cursor.execute(f'UPDATE users SET pet_hp = {pet_hp + hp} WHERE user_id = "{user_id}"')
             if c > balance:
                await bot.send_message(message.chat.id, f"💰 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств! {rloser}", parse_mode='html')
          if pet_hp == 100:
             await bot.send_message(message.chat.id, f"❤ | <a href='tg://user?id={user_id}'>{user_name}</a>, ваш питомец не нуждается в лечении!", parse_mode='html')

    if message.text.lower() in ["покормить питомца", "Покормить питомца"]:   
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       pet1 = cursor.execute("SELECT pet1 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet1 = int(pet1[0])
       pet2 = cursor.execute("SELECT pet2 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet2 = int(pet2[0])
       pet3 = cursor.execute("SELECT pet3 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet3 = int(pet3[0])
       pet4 = cursor.execute("SELECT pet4 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet4 = int(pet4[0])
       pet5 = cursor.execute("SELECT pet5 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet5 = int(pet5[0])
       pet6 = cursor.execute("SELECT pet6 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet6 = int(pet6[0])
       pet7 = cursor.execute("SELECT pet7 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet7 = int(pet7[0])
       pet8 = cursor.execute("SELECT pet8 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet8 = int(pet8[0])
       pet9 = cursor.execute("SELECT pet9 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet9 = int(pet9[0])
       pet10 = cursor.execute("SELECT pet10 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet10 = int(pet10[0])
       pet11 = cursor.execute("SELECT pet11 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet11 = int(pet11[0])
       pet_name = cursor.execute("SELECT pet_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet_name = str(pet_name[0])
       pet_hp = cursor.execute("SELECT pet_hp from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet_hp = int(pet_hp[0])
       pet_eat = cursor.execute("SELECT pet_eat from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet_eat = int(pet_eat[0])
       pet_mood = cursor.execute("SELECT pet_mood from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet_mood = int(pet_mood[0])
       chat_id = message.chat.id
       user_id = message.from_user.id
       loser = ['😔', '😕', '😣', '😞', '😢']
       rloser = random.choice(loser)
       balance = cursor.execute("SELECT balance from users where user_id = ?",(message.from_user.id,)).fetchone()
       balance = round(int(balance[0]))
       pets = pet1 + pet2 + pet3 + pet4 + pet5 + pet6 + pet7 + pet8 + pet9 + pet10 + pet11
       c = Decimal((100 - pet_eat) * 10000)
       c3 = '{0:,}'.format(c).replace(',', '.')
       c2 = (100 - pet_eat) * 10000
       eat = 100 - pet_eat
       checking = cursor.execute("SELECT checking from users where user_id = ?", (message.from_user.id,)).fetchone()
       checking = round(int(checking[0]))
       if checking == 1:
          await bot.send_message(chat_id, f'ℹ | Дождитесь окончания игры! {rloser}', parse_mode='html')
          return
       checking1 = cursor.execute("SELECT checking1 from users where user_id = ?", (message.from_user.id,)).fetchone()
       checking1 = round(int(checking1[0]))
       if checking1 == 1:
          await bot.send_message(chat_id, f'ℹ | Дождитесь окончания игры! {rloser}', parse_mode='html')
          return
       checking2 = cursor.execute("SELECT checking2 from users where user_id = ?", (message.from_user.id,)).fetchone()
       checking2 = round(int(checking2[0]))
       if checking2 == 1:
          await bot.send_message(chat_id, f'ℹ | Дождитесь окончания игры! {rloser}', parse_mode='html')
          return
       checking3 = cursor.execute("SELECT checking3 from users where user_id = ?", (message.from_user.id,)).fetchone()
       checking3 = round(int(checking3[0]))
       if checking3 == 1:
          await bot.send_message(chat_id, f'ℹ | Дождитесь окончания игры! {rloser}', parse_mode='html')
          return
       if pets == 0:
          await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас нету питомца! {rloser}", parse_mode='html')  
       if pet1 == 1:
          if pet_eat < 100:
             if c <= balance:
                await bot.send_message(message.chat.id, f"🍗 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы покормили своего питомца за {c3}!", parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - c2} WHERE user_id = "{user_id}"') 
                cursor.execute(f'UPDATE users SET pet_eat = {pet_eat + eat} WHERE user_id = "{user_id}"')
             if c > balance:
                await bot.send_message(message.chat.id, f"💰 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств! {rloser}", parse_mode='html')
          if pet_eat == 100:
             await bot.send_message(message.chat.id, f"🍗 | <a href='tg://user?id={user_id}'>{user_name}</a>, ваш питомец не голоден! {rloser}", parse_mode='html')
       if pet2 == 1:
          if pet_eat < 100:
             if c <= balance:
                await bot.send_message(message.chat.id, f"🍗 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы покормили своего питомца за {c3}!", parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - c2} WHERE user_id = "{user_id}"') 
                cursor.execute(f'UPDATE users SET pet_eat = {pet_eat + eat} WHERE user_id = "{user_id}"')
             if c > balance:
                await bot.send_message(message.chat.id, f"💰 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств! {rloser}", parse_mode='html')
          if pet_eat == 100:
             await bot.send_message(message.chat.id, f"🍗 | <a href='tg://user?id={user_id}'>{user_name}</a>, ваш питомец не голоден! {rloser}", parse_mode='html')
       if pet3 == 1:
          if pet_eat < 100:
             if c <= balance:
                await bot.send_message(message.chat.id, f"🍗 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы покормили своего питомца за {c3}!", parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - c2} WHERE user_id = "{user_id}"') 
                cursor.execute(f'UPDATE users SET pet_eat = {pet_eat + eat} WHERE user_id = "{user_id}"')
             if c > balance:
                await bot.send_message(message.chat.id, f"💰 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств! {rloser}", parse_mode='html')
          if pet_eat == 100:
             await bot.send_message(message.chat.id, f"🍗 | <a href='tg://user?id={user_id}'>{user_name}</a>, ваш питомец не голоден! {rloser}", parse_mode='html')
       if pet4 == 1:
          if pet_eat < 100:
             if c <= balance:
                await bot.send_message(message.chat.id, f"🍗 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы покормили своего питомца за {c3}!", parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - c2} WHERE user_id = "{user_id}"') 
                cursor.execute(f'UPDATE users SET pet_eat = {pet_eat + eat} WHERE user_id = "{user_id}"')
             if c > balance:
                await bot.send_message(message.chat.id, f"💰 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств! {rloser}", parse_mode='html')
          if pet_eat == 100:
             await bot.send_message(message.chat.id, f"🍗 | <a href='tg://user?id={user_id}'>{user_name}</a>, ваш питомец не голоден! {rloser}", parse_mode='html')
       if pet5 == 1:
          if pet_eat < 100:
             if c <= balance:
                await bot.send_message(message.chat.id, f"🍗 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы покормили своего питомца за {c3}!", parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - c2} WHERE user_id = "{user_id}"') 
                cursor.execute(f'UPDATE users SET pet_eat = {pet_eat + eat} WHERE user_id = "{user_id}"')
             if c > balance:
                await bot.send_message(message.chat.id, f"💰 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств! {rloser}", parse_mode='html')
          if pet_eat == 100:
             await bot.send_message(message.chat.id, f"🍗 | <a href='tg://user?id={user_id}'>{user_name}</a>, ваш питомец не голоден! {rloser}", parse_mode='html')
       if pet6 == 1:
          if pet_eat < 100:
             if c <= balance:
                await bot.send_message(message.chat.id, f"🍗 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы покормили своего питомца за {c3}!", parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - c2} WHERE user_id = "{user_id}"') 
                cursor.execute(f'UPDATE users SET pet_eat = {pet_eat + eat} WHERE user_id = "{user_id}"')
             if c > balance:
                await bot.send_message(message.chat.id, f"💰 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств! {rloser}", parse_mode='html')
          if pet_eat == 100:
             await bot.send_message(message.chat.id, f"🍗 | <a href='tg://user?id={user_id}'>{user_name}</a>, ваш питомец не голоден! {rloser}", parse_mode='html')
       if pet7 == 1:
          if pet_eat < 100:
             if c <= balance:
                await bot.send_message(message.chat.id, f"🍗 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы покормили своего питомца за {c3}!", parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - c2} WHERE user_id = "{user_id}"') 
                cursor.execute(f'UPDATE users SET pet_eat = {pet_eat + eat} WHERE user_id = "{user_id}"')
             if c > balance:
                await bot.send_message(message.chat.id, f"💰 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств! {rloser}", parse_mode='html')
          if pet_eat == 100:
             await bot.send_message(message.chat.id, f"🍗 | <a href='tg://user?id={user_id}'>{user_name}</a>, ваш питомец не голоден! {rloser}", parse_mode='html')
       if pet8 == 1:
          if pet_eat < 100:
             if c <= balance:
                await bot.send_message(message.chat.id, f"🍗 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы покормили своего питомца за {c3}!", parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - c2} WHERE user_id = "{user_id}"') 
                cursor.execute(f'UPDATE users SET pet_eat = {pet_eat + eat} WHERE user_id = "{user_id}"')
             if c > balance:
                await bot.send_message(message.chat.id, f"💰 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств! {rloser}", parse_mode='html')
          if pet_eat == 100:
             await bot.send_message(message.chat.id, f"🍗 | <a href='tg://user?id={user_id}'>{user_name}</a>, ваш питомец не голоден! {rloser}", parse_mode='html')
       if pet9 == 1:
          if pet_eat < 100:
             if c <= balance:
                await bot.send_message(message.chat.id, f"🍗 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы покормили своего питомца за {c3}!", parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - c2} WHERE user_id = "{user_id}"') 
                cursor.execute(f'UPDATE users SET pet_eat = {pet_eat + eat} WHERE user_id = "{user_id}"')
             if c > balance:
                await bot.send_message(message.chat.id, f"💰 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств! {rloser}", parse_mode='html')
          if pet_eat == 100:
             await bot.send_message(message.chat.id, f"🍗 | <a href='tg://user?id={user_id}'>{user_name}</a>, ваш питомец не голоден! {rloser}", parse_mode='html')
       if pet10 == 1:
          if pet_eat < 100:
             if c <= balance:
                await bot.send_message(message.chat.id, f"🍗 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы покормили своего питомца за {c3}!", parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - c2} WHERE user_id = "{user_id}"') 
                cursor.execute(f'UPDATE users SET pet_eat = {pet_eat + eat} WHERE user_id = "{user_id}"')
             if c > balance:
                await bot.send_message(message.chat.id, f"💰 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств! {rloser}", parse_mode='html')
          if pet_eat == 100:
             await bot.send_message(message.chat.id, f"🍗 | <a href='tg://user?id={user_id}'>{user_name}</a>, ваш питомец не голоден! {rloser}", parse_mode='html')
       if pet11 == 1:
          if pet_eat < 100:
             if c <= balance:
                await bot.send_message(message.chat.id, f"🍗 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы покормили своего питомца за {c3}!", parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - c2} WHERE user_id = "{user_id}"') 
                cursor.execute(f'UPDATE users SET pet_eat = {pet_eat + eat} WHERE user_id = "{user_id}"')
             if c > balance:
                await bot.send_message(message.chat.id, f"💰 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств! {rloser}", parse_mode='html')
          if pet_eat == 100:
             await bot.send_message(message.chat.id, f"🍗 | <a href='tg://user?id={user_id}'>{user_name}</a>, ваш питомец не голоден! {rloser}", parse_mode='html')

    if message.text.lower() in ["выгулять питомца", "Выгулять питомца"]:  
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       pet1 = cursor.execute("SELECT pet1 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet1 = int(pet1[0])
       pet2 = cursor.execute("SELECT pet2 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet2 = int(pet2[0])
       pet3 = cursor.execute("SELECT pet3 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet3 = int(pet3[0])
       pet4 = cursor.execute("SELECT pet4 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet4 = int(pet4[0])
       pet5 = cursor.execute("SELECT pet5 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet5 = int(pet5[0])
       pet6 = cursor.execute("SELECT pet6 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet6 = int(pet6[0])
       pet7 = cursor.execute("SELECT pet7 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet7 = int(pet7[0])
       pet8 = cursor.execute("SELECT pet8 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet8 = int(pet8[0])
       pet9 = cursor.execute("SELECT pet9 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet9 = int(pet9[0])
       pet10 = cursor.execute("SELECT pet10 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet10 = int(pet10[0])
       pet11 = cursor.execute("SELECT pet11 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet11 = int(pet11[0])
       pet_name = cursor.execute("SELECT pet_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet_name = str(pet_name[0])
       pet_hp = cursor.execute("SELECT pet_hp from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet_hp = int(pet_hp[0])
       pet_eat = cursor.execute("SELECT pet_eat from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet_eat = int(pet_eat[0])
       pet_mood = cursor.execute("SELECT pet_mood from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet_mood = int(pet_mood[0])
       chat_id = message.chat.id
       user_id = message.from_user.id
       loser = ['😔', '😕', '😣', '😞', '😢']
       rloser = random.choice(loser)
       balance = cursor.execute("SELECT balance from users where user_id = ?",(message.from_user.id,)).fetchone()
       balance = round(int(balance[0]))
       pets = pet1 + pet2 + pet3 + pet4 + pet5 + pet6 + pet7 + pet8 + pet9 + pet10 + pet11
       c = Decimal((100 - pet_mood) * 10000)
       mood = 100 - pet_mood
       checking = cursor.execute("SELECT checking from users where user_id = ?", (message.from_user.id,)).fetchone()
       checking = round(int(checking[0]))
       if checking == 1:
          await bot.send_message(chat_id, f'ℹ | Дождитесь окончания игры! {rloser}', parse_mode='html')
          return
       checking1 = cursor.execute("SELECT checking1 from users where user_id = ?", (message.from_user.id,)).fetchone()
       checking1 = round(int(checking1[0]))
       if checking1 == 1:
          await bot.send_message(chat_id, f'ℹ | Дождитесь окончания игры! {rloser}', parse_mode='html')
          return
       checking2 = cursor.execute("SELECT checking2 from users where user_id = ?", (message.from_user.id,)).fetchone()
       checking2 = round(int(checking2[0]))
       if checking2 == 1:
          await bot.send_message(chat_id, f'ℹ | Дождитесь окончания игры! {rloser}', parse_mode='html')
          return
       checking3 = cursor.execute("SELECT checking3 from users where user_id = ?", (message.from_user.id,)).fetchone()
       checking3 = round(int(checking3[0]))
       if checking3 == 1:
          await bot.send_message(chat_id, f'ℹ | Дождитесь окончания игры! {rloser}', parse_mode='html')
          return
       if pets == 0:
          await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас нету питомца! {rloser}", parse_mode='html')  
       if pet1 == 1:
          if pet_mood < 100:
             await bot.send_message(message.chat.id, f"🌳 <a href='tg://user?id={user_id}'>{user_name}</a>, вы выгуляли своего питомца!", parse_mode='html')
             cursor.execute(f'UPDATE users SET pet_mood = {pet_mood + mood} WHERE user_id = "{user_id}"')
          if pet_mood == 100:
             await bot.send_message(message.chat.id, f"🌳 <a href='tg://user?id={user_id}'>{user_name}</a>, ваш питомец не хочет гулять!", parse_mode='html')
       if pet2 == 1:
          if pet_mood < 100:
             await bot.send_message(message.chat.id, f"🌳 <a href='tg://user?id={user_id}'>{user_name}</a>, вы выгуляли своего питомца!", parse_mode='html')
             cursor.execute(f'UPDATE users SET pet_mood = {pet_mood + mood} WHERE user_id = "{user_id}"')
          if pet_mood == 100:
             await bot.send_message(message.chat.id, f"🌳 <a href='tg://user?id={user_id}'>{user_name}</a>, ваш питомец не хочет гулять!", parse_mode='html')
       if pet3 == 1:
          if pet_mood < 100:
             await bot.send_message(message.chat.id, f"🌳 <a href='tg://user?id={user_id}'>{user_name}</a>, вы выгуляли своего питомца!", parse_mode='html')
             cursor.execute(f'UPDATE users SET pet_mood = {pet_mood + mood} WHERE user_id = "{user_id}"')
          if pet_mood == 100:
             await bot.send_message(message.chat.id, f"🌳 <a href='tg://user?id={user_id}'>{user_name}</a>, ваш питомец не хочет гулять!", parse_mode='html')
       if pet4 == 1:
          if pet_mood < 100:
             await bot.send_message(message.chat.id, f"🌳 <a href='tg://user?id={user_id}'>{user_name}</a>, вы выгуляли своего питомца!", parse_mode='html')
             cursor.execute(f'UPDATE users SET pet_mood = {pet_mood + mood} WHERE user_id = "{user_id}"')
          if pet_mood == 100:
             await bot.send_message(message.chat.id, f"🌳 <a href='tg://user?id={user_id}'>{user_name}</a>, ваш питомец не хочет гулять!", parse_mode='html')
       if pet5 == 1:
          if pet_mood < 100:
             await bot.send_message(message.chat.id, f"🌳 <a href='tg://user?id={user_id}'>{user_name}</a>, вы выгуляли своего питомца!", parse_mode='html')
             cursor.execute(f'UPDATE users SET pet_mood = {pet_mood + mood} WHERE user_id = "{user_id}"')
          if pet_mood == 100:
             await bot.send_message(message.chat.id, f"🌳 <a href='tg://user?id={user_id}'>{user_name}</a>, ваш питомец не хочет гулять!", parse_mode='html')
       if pet6 == 1:
          if pet_mood < 100:
             await bot.send_message(message.chat.id, f"🌳 <a href='tg://user?id={user_id}'>{user_name}</a>, вы выгуляли своего питомца!", parse_mode='html')
             cursor.execute(f'UPDATE users SET pet_mood = {pet_mood + mood} WHERE user_id = "{user_id}"')
          if pet_mood == 100:
             await bot.send_message(message.chat.id, f"🌳 <a href='tg://user?id={user_id}'>{user_name}</a>, ваш питомец не хочет гулять!", parse_mode='html')
       if pet7 == 1:
          if pet_mood < 100:
             await bot.send_message(message.chat.id, f"🌳 <a href='tg://user?id={user_id}'>{user_name}</a>, вы выгуляли своего питомца!", parse_mode='html')
             cursor.execute(f'UPDATE users SET pet_mood = {pet_mood + mood} WHERE user_id = "{user_id}"')
          if pet_mood == 100:
             await bot.send_message(message.chat.id, f"🌳 <a href='tg://user?id={user_id}'>{user_name}</a>, ваш питомец не хочет гулять!", parse_mode='html')
       if pet8 == 1:
          if pet_mood < 100:
             await bot.send_message(message.chat.id, f"🌳 <a href='tg://user?id={user_id}'>{user_name}</a>, вы выгуляли своего питомца!", parse_mode='html')
             cursor.execute(f'UPDATE users SET pet_mood = {pet_mood + mood} WHERE user_id = "{user_id}"')
          if pet_mood == 100:
             await bot.send_message(message.chat.id, f"🌳 <a href='tg://user?id={user_id}'>{user_name}</a>, ваш питомец не хочет гулять!", parse_mode='html')
       if pet9 == 1:
          if pet_mood < 100:
             await bot.send_message(message.chat.id, f"🌳 <a href='tg://user?id={user_id}'>{user_name}</a>, вы выгуляли своего питомца!", parse_mode='html')
             cursor.execute(f'UPDATE users SET pet_mood = {pet_mood + mood} WHERE user_id = "{user_id}"')
          if pet_mood == 100:
             await bot.send_message(message.chat.id, f"🌳 <a href='tg://user?id={user_id}'>{user_name}</a>, ваш питомец не хочет гулять!", parse_mode='html')
       if pet10 == 1:
          if pet_mood < 100:
             await bot.send_message(message.chat.id, f"🌳 <a href='tg://user?id={user_id}'>{user_name}</a>, вы выгуляли своего питомца!", parse_mode='html')
             cursor.execute(f'UPDATE users SET pet_mood = {pet_mood + mood} WHERE user_id = "{user_id}"')
          if pet_mood == 100:
             await bot.send_message(message.chat.id, f"🌳 <a href='tg://user?id={user_id}'>{user_name}</a>, ваш питомец не хочет гулять!", parse_mode='html')
       if pet11 == 1:
          if pet_mood < 100:
             await bot.send_message(message.chat.id, f"🌳 <a href='tg://user?id={user_id}'>{user_name}</a>, вы выгуляли своего питомца!", parse_mode='html')
             cursor.execute(f'UPDATE users SET pet_mood = {pet_mood + mood} WHERE user_id = "{user_id}"')
          if pet_mood == 100:
             await bot.send_message(message.chat.id, f"🌳 <a href='tg://user?id={user_id}'>{user_name}</a>, ваш питомец не хочет гулять!", parse_mode='html')

    if message.text.startswith("питомец имя"): 
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       pet1 = cursor.execute("SELECT pet1 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet1 = int(pet1[0])
       pet2 = cursor.execute("SELECT pet2 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet2 = int(pet2[0])
       pet3 = cursor.execute("SELECT pet3 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet3 = int(pet3[0])
       pet4 = cursor.execute("SELECT pet4 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet4 = int(pet4[0])
       pet5 = cursor.execute("SELECT pet5 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet5 = int(pet5[0])
       pet6 = cursor.execute("SELECT pet6 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet6 = int(pet6[0])
       pet7 = cursor.execute("SELECT pet7 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet7 = int(pet7[0])
       pet8 = cursor.execute("SELECT pet8 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet8 = int(pet8[0])
       pet9 = cursor.execute("SELECT pet9 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet9 = int(pet9[0])
       pet10 = cursor.execute("SELECT pet10 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet10 = int(pet10[0])
       pet11 = cursor.execute("SELECT pet11 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet11 = int(pet11[0])
       pet_name = cursor.execute("SELECT pet_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet_name = str(pet_name[0])
       pet_hp = cursor.execute("SELECT pet_hp from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet_hp = int(pet_hp[0])
       pet_eat = cursor.execute("SELECT pet_eat from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet_eat = int(pet_eat[0])
       pet_mood = cursor.execute("SELECT pet_mood from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet_mood = int(pet_mood[0])
       chat_id = message.chat.id
       user_id = message.from_user.id
       loser = ['😔', '😕', '😣', '😞', '😢']
       rloser = random.choice(loser)
       pets = pet1 + pet2 + pet3 + pet4 + pet5 + pet6 + pet7 + pet8 + pet9 + pet10 + pet11
       name = " ".join(message.text.split()[2:])
       if len(name) <= 20:
          pass
       else: 
          await bot.send_message(message.chat.id, f"ℹ️️ | <a href='tg://user?id={user_id}'>{user_name}</a> , ник питомца не может быть длинее 20 символов!", parse_mode='html')
          return
       if pets == 0:
          await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас нету питомца! {rloser}", parse_mode='html')
       if pet1 == 1:
          await bot.send_message(message.chat.id, f"✏️ | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно поменяли имя своего питомца на: {name}!", parse_mode='html')
          cursor.execute(f'UPDATE users SET pet_name = \"{name}\" WHERE user_id = "{user_id}"')
       if pet2 == 1:
          await bot.send_message(message.chat.id, f"✏️ | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно поменяли имя своего питомца на: {name}!", parse_mode='html')
          cursor.execute(f'UPDATE users SET pet_name = \"{name}\" WHERE user_id = "{user_id}"')
       if pet3 == 1:
          await bot.send_message(message.chat.id, f"✏️ | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно поменяли имя своего питомца на: {name}!", parse_mode='html')
          cursor.execute(f'UPDATE users SET pet_name = \"{name}\" WHERE user_id = "{user_id}"')
       if pet4 == 1:
          await bot.send_message(message.chat.id, f"✏️ | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно поменяли имя своего питомца на: {name}!", parse_mode='html')
          cursor.execute(f'UPDATE users SET pet_name = \"{name}\" WHERE user_id = "{user_id}"')
       if pet5 == 1:
          await bot.send_message(message.chat.id, f"✏️ | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно поменяли имя своего питомца на: {name}!", parse_mode='html')
          cursor.execute(f'UPDATE users SET pet_name = \"{name}\" WHERE user_id = "{user_id}"')
       if pet6 == 1:
          await bot.send_message(message.chat.id, f"✏️ | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно поменяли имя своего питомца на: {name}!", parse_mode='html')
          cursor.execute(f'UPDATE users SET pet_name = \"{name}\" WHERE user_id = "{user_id}"')
       if pet7 == 1:
          await bot.send_message(message.chat.id, f"✏️ | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно поменяли имя своего питомца на: {name}!", parse_mode='html')
          cursor.execute(f'UPDATE users SET pet_name = \"{name}\" WHERE user_id = "{user_id}"')
       if pet8 == 1:
          await bot.send_message(message.chat.id, f"✏️ | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно поменяли имя своего питомца на: {name}!", parse_mode='html')
          cursor.execute(f'UPDATE users SET pet_name = \"{name}\" WHERE user_id = "{user_id}"')
       if pet9 == 1:
          await bot.send_message(message.chat.id, f"✏️ | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно поменяли имя своего питомца на: {name}!", parse_mode='html')
          cursor.execute(f'UPDATE users SET pet_name = \"{name}\" WHERE user_id = "{user_id}"')
       if pet10 == 1:
          await bot.send_message(message.chat.id, f"✏️ | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно поменяли имя своего питомца на: {name}!", parse_mode='html')
          cursor.execute(f'UPDATE users SET pet_name = \"{name}\" WHERE user_id = "{user_id}"')
       if pet11 == 1:
          await bot.send_message(message.chat.id, f"✏️ | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно поменяли имя своего питомца на: {name}!", parse_mode='html')
          cursor.execute(f'UPDATE users SET pet_name = \"{name}\" WHERE user_id = "{user_id}"')

    if message.text.startswith("Питомец имя"): 
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       pet1 = cursor.execute("SELECT pet1 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet1 = int(pet1[0])
       pet2 = cursor.execute("SELECT pet2 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet2 = int(pet2[0])
       pet3 = cursor.execute("SELECT pet3 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet3 = int(pet3[0])
       pet4 = cursor.execute("SELECT pet4 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet4 = int(pet4[0])
       pet5 = cursor.execute("SELECT pet5 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet5 = int(pet5[0])
       pet6 = cursor.execute("SELECT pet6 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet6 = int(pet6[0])
       pet7 = cursor.execute("SELECT pet7 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet7 = int(pet7[0])
       pet8 = cursor.execute("SELECT pet8 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet8 = int(pet8[0])
       pet9 = cursor.execute("SELECT pet9 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet9 = int(pet9[0])
       pet10 = cursor.execute("SELECT pet10 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet10 = int(pet10[0])
       pet11 = cursor.execute("SELECT pet11 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet11 = int(pet11[0])
       pet_name = cursor.execute("SELECT pet_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet_name = str(pet_name[0])
       pet_hp = cursor.execute("SELECT pet_hp from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet_hp = int(pet_hp[0])
       pet_eat = cursor.execute("SELECT pet_eat from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet_eat = int(pet_eat[0])
       pet_mood = cursor.execute("SELECT pet_mood from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet_mood = int(pet_mood[0])
       chat_id = message.chat.id
       user_id = message.from_user.id
       loser = ['😔', '😕', '😣', '😞', '😢']
       rloser = random.choice(loser)
       pets = pet1 + pet2 + pet3 + pet4 + pet5 + pet6 + pet7 + pet8 + pet9 + pet10 + pet11
       name = " ".join(message.text.split()[2:])
       if len(name) <= 20:
          pass
       else: 
          await bot.send_message(message.chat.id, f"ℹ️️ | <a href='tg://user?id={user_id}'>{user_name}</a> , ник питомца не может быть длинее 20 символов!", parse_mode='html')
          return
       if pets == 0:
          await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас нету питомца! {rloser}", parse_mode='html')
       if pet1 == 1:
          await bot.send_message(message.chat.id, f"✏️ | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно поменяли имя своего питомца на: {name}!", parse_mode='html')
          cursor.execute(f'UPDATE users SET pet_name = \"{name}\" WHERE user_id = "{user_id}"')
       if pet2 == 1:
          await bot.send_message(message.chat.id, f"✏️ | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно поменяли имя своего питомца на: {name}!", parse_mode='html')
          cursor.execute(f'UPDATE users SET pet_name = \"{name}\" WHERE user_id = "{user_id}"')
       if pet3 == 1:
          await bot.send_message(message.chat.id, f"✏️ | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно поменяли имя своего питомца на: {name}!", parse_mode='html')
          cursor.execute(f'UPDATE users SET pet_name = \"{name}\" WHERE user_id = "{user_id}"')
       if pet4 == 1:
          await bot.send_message(message.chat.id, f"✏️ | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно поменяли имя своего питомца на: {name}!", parse_mode='html')
          cursor.execute(f'UPDATE users SET pet_name = \"{name}\" WHERE user_id = "{user_id}"')
       if pet5 == 1:
          await bot.send_message(message.chat.id, f"✏️ | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно поменяли имя своего питомца на: {name}!", parse_mode='html')
          cursor.execute(f'UPDATE users SET pet_name = \"{name}\" WHERE user_id = "{user_id}"')
       if pet6 == 1:
          await bot.send_message(message.chat.id, f"✏️ | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно поменяли имя своего питомца на: {name}!", parse_mode='html')
          cursor.execute(f'UPDATE users SET pet_name = \"{name}\" WHERE user_id = "{user_id}"')
       if pet7 == 1:
          await bot.send_message(message.chat.id, f"✏️ | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно поменяли имя своего питомца на: {name}!", parse_mode='html')
          cursor.execute(f'UPDATE users SET pet_name = \"{name}\" WHERE user_id = "{user_id}"')
       if pet8 == 1:
          await bot.send_message(message.chat.id, f"✏️ | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно поменяли имя своего питомца на: {name}!", parse_mode='html')
          cursor.execute(f'UPDATE users SET pet_name = \"{name}\" WHERE user_id = "{user_id}"')
       if pet9 == 1:
          await bot.send_message(message.chat.id, f"✏️ | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно поменяли имя своего питомца на: {name}!", parse_mode='html')
          cursor.execute(f'UPDATE users SET pet_name = \"{name}\" WHERE user_id = "{user_id}"')
       if pet10 == 1:
          await bot.send_message(message.chat.id, f"✏️ | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно поменяли имя своего питомца на: {name}!", parse_mode='html')
          cursor.execute(f'UPDATE users SET pet_name = \"{name}\" WHERE user_id = "{user_id}"')
       if pet11 == 1:
          await bot.send_message(message.chat.id, f"✏️ | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно поменяли имя своего питомца на: {name}!", parse_mode='html')
          cursor.execute(f'UPDATE users SET pet_name = \"{name}\" WHERE user_id = "{user_id}"')

    if message.text.lower() in ["продать питомца", "Продать питомца"]:  
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       pet1 = cursor.execute("SELECT pet1 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet1 = int(pet1[0])
       pet2 = cursor.execute("SELECT pet2 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet2 = int(pet2[0])
       pet3 = cursor.execute("SELECT pet3 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet3 = int(pet3[0])
       pet4 = cursor.execute("SELECT pet4 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet4 = int(pet4[0])
       pet5 = cursor.execute("SELECT pet5 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet5 = int(pet5[0])
       pet6 = cursor.execute("SELECT pet6 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet6 = int(pet6[0])
       pet7 = cursor.execute("SELECT pet7 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet7 = int(pet7[0])
       pet8 = cursor.execute("SELECT pet8 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet8 = int(pet8[0])
       pet9 = cursor.execute("SELECT pet9 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet9 = int(pet9[0])
       pet10 = cursor.execute("SELECT pet10 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet10 = int(pet10[0])
       pet11 = cursor.execute("SELECT pet11 from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet11 = int(pet11[0])
       pet_name = cursor.execute("SELECT pet_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet_name = str(pet_name[0])
       pet_hp = cursor.execute("SELECT pet_hp from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet_hp = int(pet_hp[0])
       pet_eat = cursor.execute("SELECT pet_eat from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet_eat = int(pet_eat[0])
       pet_mood = cursor.execute("SELECT pet_mood from users where user_id = ?",(message.from_user.id,)).fetchone()
       pet_mood = int(pet_mood[0])
       chat_id = message.chat.id
       user_id = message.from_user.id
       loser = ['😔', '😕', '😣', '😞', '😢']
       rloser = random.choice(loser)
       balance = cursor.execute("SELECT balance from users where user_id = ?",(message.from_user.id,)).fetchone()
       balance = round(int(balance[0]))
       checking1 = cursor.execute("SELECT checking1 from users where user_id = ?", (message.from_user.id,)).fetchone()
       checking1 = round(int(checking1[0]))
       if checking1 == 1:
          await bot.send_message(chat_id, f'ℹ | Дождитесь окончания игры! {rloser}', parse_mode='html')
          return
       checking2 = cursor.execute("SELECT checking2 from users where user_id = ?", (message.from_user.id,)).fetchone()
       checking2 = round(int(checking2[0]))
       if checking2 == 1:
          await bot.send_message(chat_id, f'ℹ | Дождитесь окончания игры! {rloser}', parse_mode='html')
          return
       checking3 = cursor.execute("SELECT checking3 from users where user_id = ?", (message.from_user.id,)).fetchone()
       checking3 = round(int(checking3[0]))
       if checking3 == 1:
          await bot.send_message(chat_id, f'ℹ | Дождитесь окончания игры! {rloser}', parse_mode='html')
          return
       c = 1
       pets = pet1 + pet2 + pet3 + pet4 + pet5 + pet6 + pet7 + pet8 + pet9 + pet10 + pet11
       if pets == 0:
          await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас нету питомца! {rloser}", parse_mode='html')
       if pet1 == 1:
          await bot.send_message(message.chat.id, f"💰 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно продали своего питомца за 750.000¢", parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance + 750000} WHERE user_id = "{user_id}"') 
          cursor.execute(f'UPDATE users SET pet1 = {pet1 - c} WHERE user_id = "{user_id}"') 
          cursor.execute(f'UPDATE users SET pet_hp = {100} WHERE user_id = "{user_id}"') 
          cursor.execute(f'UPDATE users SET pet_eat = {100} WHERE user_id = "{user_id}"') 
          cursor.execute(f'UPDATE users SET pet_mood = {100} WHERE user_id = "{user_id}"') 
       if pet2 == 1:
          await bot.send_message(message.chat.id, f"💰 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно продали своего питомца за 75.000.000¢", parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance + 75000000} WHERE user_id = "{user_id}"') 
          cursor.execute(f'UPDATE users SET pet2 = {pet2 - c} WHERE user_id = "{user_id}"') 
          cursor.execute(f'UPDATE users SET pet_hp = {100} WHERE user_id = "{user_id}"') 
          cursor.execute(f'UPDATE users SET pet_eat = {100} WHERE user_id = "{user_id}"') 
          cursor.execute(f'UPDATE users SET pet_mood = {100} WHERE user_id = "{user_id}"') 
       if pet3 == 1:
          await bot.send_message(message.chat.id, f"💰 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно продали своего питомца за 375.000.000¢", parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance + 375000000} WHERE user_id = "{user_id}"') 
          cursor.execute(f'UPDATE users SET pet3 = {pet3 - c} WHERE user_id = "{user_id}"') 
          cursor.execute(f'UPDATE users SET pet_hp = {100} WHERE user_id = "{user_id}"') 
          cursor.execute(f'UPDATE users SET pet_eat = {100} WHERE user_id = "{user_id}"') 
          cursor.execute(f'UPDATE users SET pet_mood = {100} WHERE user_id = "{user_id}"') 
       if pet4 == 1:
          await bot.send_message(message.chat.id, f"💰 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно продали своего питомца за 750.000.000¢", parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance + 750000000} WHERE user_id = "{user_id}"') 
          cursor.execute(f'UPDATE users SET pet4 = {pet4 - c} WHERE user_id = "{user_id}"') 
          cursor.execute(f'UPDATE users SET pet_hp = {100} WHERE user_id = "{user_id}"') 
          cursor.execute(f'UPDATE users SET pet_eat = {100} WHERE user_id = "{user_id}"') 
          cursor.execute(f'UPDATE users SET pet_mood = {100} WHERE user_id = "{user_id}"') 
       if pet5 == 1:
          await bot.send_message(message.chat.id, f"💰 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно продали своего питомца за 37.500.000.000¢", parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance + 37500000000} WHERE user_id = "{user_id}"') 
          cursor.execute(f'UPDATE users SET pet5 = {pet5 - c} WHERE user_id = "{user_id}"') 
          cursor.execute(f'UPDATE users SET pet_hp = {100} WHERE user_id = "{user_id}"') 
          cursor.execute(f'UPDATE users SET pet_eat = {100} WHERE user_id = "{user_id}"') 
          cursor.execute(f'UPDATE users SET pet_mood = {100} WHERE user_id = "{user_id}"') 
       if pet6 == 1:
          await bot.send_message(message.chat.id, f"💰 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно продали своего питомца за 75.000.000.000¢", parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance + 75000000000} WHERE user_id = "{user_id}"') 
          cursor.execute(f'UPDATE users SET pet6 = {pet6 - c} WHERE user_id = "{user_id}"') 
          cursor.execute(f'UPDATE users SET pet_hp = {100} WHERE user_id = "{user_id}"') 
          cursor.execute(f'UPDATE users SET pet_eat = {100} WHERE user_id = "{user_id}"') 
          cursor.execute(f'UPDATE users SET pet_mood = {100} WHERE user_id = "{user_id}"')
       if pet7 == 1:
          await bot.send_message(message.chat.id, f"💰 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно продали своего питомца за 375.000.000.000¢", parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance + 375000000000} WHERE user_id = "{user_id}"') 
          cursor.execute(f'UPDATE users SET pet7 = {pet7 - c} WHERE user_id = "{user_id}"') 
          cursor.execute(f'UPDATE users SET pet_hp = {100} WHERE user_id = "{user_id}"') 
          cursor.execute(f'UPDATE users SET pet_eat = {100} WHERE user_id = "{user_id}"') 
          cursor.execute(f'UPDATE users SET pet_mood = {100} WHERE user_id = "{user_id}"') 
       if pet8 == 1:
          await bot.send_message(message.chat.id, f"💰 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно продали своего питомца за 7.500.000.000.000¢", parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance + 7500000000000} WHERE user_id = "{user_id}"') 
          cursor.execute(f'UPDATE users SET pet8 = {pet8 - c} WHERE user_id = "{user_id}"') 
          cursor.execute(f'UPDATE users SET pet_hp = {100} WHERE user_id = "{user_id}"') 
          cursor.execute(f'UPDATE users SET pet_eat = {100} WHERE user_id = "{user_id}"') 
          cursor.execute(f'UPDATE users SET pet_mood = {100} WHERE user_id = "{user_id}"')
       if pet9 == 1:
          await bot.send_message(message.chat.id, f"💰 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно продали своего питомца за 75.000.000.000.000¢", parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance + 75000000000000} WHERE user_id = "{user_id}"') 
          cursor.execute(f'UPDATE users SET pet9 = {pet9 - c} WHERE user_id = "{user_id}"') 
          cursor.execute(f'UPDATE users SET pet_hp = {100} WHERE user_id = "{user_id}"') 
          cursor.execute(f'UPDATE users SET pet_eat = {100} WHERE user_id = "{user_id}"') 
          cursor.execute(f'UPDATE users SET pet_mood = {100} WHERE user_id = "{user_id}"') 
       if pet10 == 1:
          await bot.send_message(message.chat.id, f"💰 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно продали своего питомца за 22.000.000.000.000¢", parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance + 22000000000000} WHERE user_id = "{user_id}"') 
          cursor.execute(f'UPDATE users SET pet10 = {pet10 - c} WHERE user_id = "{user_id}"') 
          cursor.execute(f'UPDATE users SET pet_hp = {100} WHERE user_id = "{user_id}"') 
          cursor.execute(f'UPDATE users SET pet_eat = {100} WHERE user_id = "{user_id}"') 
          cursor.execute(f'UPDATE users SET pet_mood = {100} WHERE user_id = "{user_id}"') 
       if pet11 == 1:
          await bot.send_message(message.chat.id, f"💰 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно продали своего питомца за 10.000.000¢", parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance + 10000000} WHERE user_id = "{user_id}"') 
          cursor.execute(f'UPDATE users SET pet11 = {pet11 - c} WHERE user_id = "{user_id}"') 
          cursor.execute(f'UPDATE users SET pet_hp = {100} WHERE user_id = "{user_id}"') 
          cursor.execute(f'UPDATE users SET pet_eat = {100} WHERE user_id = "{user_id}"') 
          cursor.execute(f'UPDATE users SET pet_mood = {100} WHERE user_id = "{user_id}"') 


########################################ДОМА########################################
    if message.text.startswith('Продать дом') or message.text.startswith('продать дом'):
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       balance = cursor.execute("SELECT balance from users where user_Id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])

       house = cursor.execute("SELECT house from house where user_id = ?", (message.from_user.id,)).fetchone()
       house = int(house[0])

       if house == 1:
          house2 = 'Дом'
          summ = 500000
          summ2 = '{:,}'.format(summ)
          member_house = 1


       if house == 2:
          house2 = 'Квартира'
          summ = 3000000
          summ2 = '{:,}'.format(summ)
          member_house = 2
      
       if house == 3:
          house2 = 'Огромный дом'
          summ = 5000000
          summ2 = '{:,}'.format(summ)
          member_house = 3
      
       if house == 4:
          house2 = 'Коттедж'
          summ = 7000000
          summ2 = '{:,}'.format(summ)
          member_house = 4
      
       if house == 5:
          house2 = 'Бурдж Кхалифа'
          summ = 10000000
          summ2 = '{:,}'.format(summ)
          member_house = 5

       if house == 6:
          house2 = 'Россия'
          summ = 50000000
          summ2 = '{:,}'.format(summ)
          member_house = 6

       if house == 7:
          house2 = 'Половина земли'
          summ = 100000000
          summ2 = '{:,}'.format(summ)
          member_house = 7

       if house == 8:
          house2 = 'Марс'
          summ = 100000000000000
          summ2 = '{:,}'.format(summ)
          member_house = 8

       if house > 0:
          await bot.send_message(message.chat.id, f"🏡 <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно продали дом {house2} за {summ2}¢", parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance + summ} WHERE user_id = {user_id}')
          cursor.execute(f'UPDATE house SET house = {0} WHERE user_id = {user_id}')
          connect.commit()
          return
       else:
          await bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, <b>доступные дома:

🏠 1. Дом - 500.000.000¢
🏠 2. Квартира - 3.000.000.000¢
🏠 3. Огромный дом - 5.000.000.000¢
🏠 4. Коттедж - 7.000.000.000¢
🏠 5. Бурдж Кхалифа - 10.000.000.000¢
🏠 6. Россия - 50.000.000.000¢
🏠 7. Половина земли - 100.000.000.000¢
🏠 8. Свой марс - 100e12¢

🛒 Для покупки дома введите:</b> <code>Купить дом</code> <b>[номер]</b>
       """, parse_mode='html')
          return

    if message.text.startswith('купить дом') or message.text.startswith('Купить дом'):
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       balance = cursor.execute("SELECT balance from users where user_Id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])

       house = cursor.execute("SELECT house from house where user_id = ?", (message.from_user.id,)).fetchone()
       house = int(house[0])

       member = int(message.text.split()[2])

       if member == 1:
          house2 = 'Дом'
          summ = 500000000
          summ2 = '{:,}'.format(summ)
          member_house = 1


       if member == 2:
          house2 = 'Квартира'
          summ = 3000000000
          summ2 = '{:,}'.format(summ)
          member_house = 2
      
       if member == 3:
          house2 = 'Огромный дом'
          summ = 5000000000
          summ2 = '{:,}'.format(summ)
          member_house = 3
      
       if member == 4:
          house2 = 'Коттедж'
          summ = 7000000000
          summ2 = '{:,}'.format(summ)
          member_house = 4
      
       if member == 5:
          house2 = 'Бурдж Кхалифа'
          summ = 10000000000
          summ2 = '{:,}'.format(summ)
          member_house = 5

       if member == 6:
          house2 = 'Россия'
          summ = 50000000000
          summ2 = '{:,}'.format(summ)
          member_house = 6

       if member == 7:
          house2 = 'Половина земли'
          summ = 100000000000
          summ2 = '{:,}'.format(summ)
          member_house = 7

       if member == 8:
          house2 = 'Марс'
          summ = 100000000000000
          summ2 = '{:,}'.format(summ)
          member_house = 8

       if house == 0:
          if member > 0:
             if member < 9:
                if summ <= balance:
                   await bot.send_message(message.chat.id, f"🏡 <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно купили дом {house2} за {summ2}¢", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE house SET house = {member_house} WHERE user_id = {user_id}')
                   connect.commit()
                else:
                   await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, у вас нехватает средств!", parse_mode='html')               
             else:
                await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, подождите! Нету такого номера дома!", parse_mode='html')
          else:
             await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, подождите! Нету такого номера дома!", parse_mode='html')
       else:
          await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, подождите! У вас уже есть дом, что бы продать дом введите команду <code>Продать дом</code>", parse_mode='html')


    if message.text.lower().startswith("дом"):
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       house = cursor.execute("SELECT house from house where user_id = ?", (message.from_user.id,)).fetchone()
       house = int(house[0])

       if house == 1:
          house2 = 'Дом'
          summ = 100000
          summ2 = '{:,}'.format(summ)

       if house == 2:
          house2 = 'Квартира'
          summ = 300000
          summ2 = '{:,}'.format(summ)

       if house == 3:
          house2 = 'Огромный дом'
          summ = 500000
          summ2 = '{:,}'.format(summ)

       if house == 4:
          house2 = 'Коттедж'
          summ = 700000
          summ2 = '{:,}'.format(summ)

       if house == 5:
          house2 = 'Бурдж Кхалифа'
          summ = 1000000
          summ2 = '{:,}'.format(summ)
      
       if house == 6:
          house2 = 'Россия'
          summ = 5000000
          summ2 = '{:,}'.format(summ)

       if house == 7:
          house2 = 'Половина земли'
          summ = 10000000
          summ2 = '{:,}'.format(summ)

       if house == 8:
          house2 = 'Свой Марс'          
          summ = 50000000
          summ2 = '{:,}'.format(summ)

       if house == 8:
          mars_photo = open('imges/mars.jpg', 'rb')
          await bot.send_photo(chat_id=message.chat.id, photo=mars_photo, caption=f"""🏡 | <a href='tg://user?id={user_id}'>{user_name}</a>, ваш дом {house2}
💸 | Стоимость аредны: {summ2}
""", parse_mode='html')         
       if house == 7:
          world_photo = open('imges/world2.jpg', 'rb')
          await bot.send_photo(chat_id=message.chat.id, photo=world_photo, caption=f"""🏡 | <a href='tg://user?id={user_id}'>{user_name}</a>, ваш дом {house2}
💸 | Стоимость аредны: {summ2}
""", parse_mode='html')
       if house == 8:
          mars_photo = open('imges/mars.jpg', 'rb')
          await bot.send_photo(chat_id=message.chat.id, photo=mars_photo, caption=f"""🏡 | <a href='tg://user?id={user_id}'>{user_name}</a>, ваш дом {house2}
💸 | Стоимость аредны: {summ2}
""", parse_mode='html')
       if house == 6:
          russia_photo = open('imges/russia.jpg', 'rb')
          await bot.send_photo(chat_id=message.chat.id, photo=russia_photo, caption=f"""🏡 | <a href='tg://user?id={user_id}'>{user_name}</a>, ваш дом {house2}
💸 | Стоимость аредны: {summ2}
""", parse_mode='html')
       if house == 5:
          burdj_photo = open('imges/burdj.jpg', 'rb')
          await bot.send_photo(chat_id=message.chat.id, photo=burdj_photo, caption=f"""🏡 | <a href='tg://user?id={user_id}'>{user_name}</a>, ваш дом {house2}
💸 | Стоимость аредны: {summ2}
""", parse_mode='html')
       if house == 4:
          dubai_photo = open('imges/dubai.jpg', 'rb')
          await bot.send_photo(chat_id=message.chat.id, photo=dubai_photo, caption=f"""🏡 | <a href='tg://user?id={user_id}'>{user_name}</a>, ваш дом {house2}
💸 | Стоимость аредны: {summ2}
""", parse_mode='html')
       if house == 3:
          dom_photo = open('imges/dom.jpg', 'rb')
          await bot.send_photo(chat_id=message.chat.id, photo=dom_photo, caption=f"""🏡 | <a href='tg://user?id={user_id}'>{user_name}</a>, ваш дом {house2}
💸 | Стоимость аредны: {summ2}
""", parse_mode='html')
       if house == 2:
          kvartira_photo = open('imges/kvartira.jpg', 'rb')
          await bot.send_photo(chat_id=message.chat.id, photo=kvartira_photo, caption=f"""🏡 | <a href='tg://user?id={user_id}'>{user_name}</a>, ваш дом {house2}
💸 | Стоимость аредны: {summ2}
""", parse_mode='html')
       if house == 1:
          domjr_photo = open('imges/domjr.jpg', 'rb')
          await bot.send_photo(chat_id=message.chat.id, photo=domjr_photo, caption=f"""🏡 | <a href='tg://user?id={user_id}'>{user_name}</a>, ваш дом {house2}
💸 | Стоимость аредны: {summ2}
""", parse_mode='html')
    
       if house <= 0:
          await bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, <b>доступные дома:

🏠 1. Дом - 500.000.000¢
🏠 2. Квартира - 3.000.000.000¢
🏠 3. Огромный дом - 5.000.000.000¢
🏠 4. Коттедж - 7.000.000.000¢
🏠 5. Бурдж Кхалифа - 10.000.000.000¢
🏠 6. Россия - 50.000.000.000¢
🏠 7. Половина земли - 100.000.000.000¢
🏠 8. Свой марс - 100e12¢

🛒 Для покупки дома введите:</b> <code>Купить дом</code> <b>[номер]</b>
       """, parse_mode='html')


    if message.text.lower() in ['аренда дом', 'Аренда дом']:
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id
       house = cursor.execute("SELECT house from house where user_id = ?", (message.from_user.id,)).fetchone()
       house = int(house[0])
       balance = cursor.execute("SELECT balance from users where user_Id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])

       donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(message.from_user.id,)).fetchone()
       donate_coins = int(donate_coins[0])

       period = 43200 #259200s 3d
       get = cursor.execute("SELECT stavka_depozit FROM bot_time WHERE user_id = ?", (message.from_user.id,)).fetchone()
       last_stavka = f"{int(get[0])}"
       stavkatime = time.time() - float(last_stavka)

       if house == 1:
         if stavkatime > period:
            await bot.send_message(message.chat.id, f"Вы успешно арендовали свой дом и заработали 100.000")
            cursor.execute(f'UPDATE users SET balance = {balance + 100000} WHERE user_id = {user_id}')
            cursor.execute(f'UPDATE bot_time SET stavka_depozit = {time.time()}  WHERE user_id = {user_id}')
            connect.commit()
            return
         else:
            await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , извините но арендовать можно раз в 12 часа", parse_mode='html')


       if house == 2:
         if stavkatime > period:
            await bot.send_message(message.chat.id, f"Вы успешно арендовали свою квартиру и заработали 300.000")
            cursor.execute(f'UPDATE users SET balance = {balance + 300000} WHERE user_id = {user_id}')
            cursor.execute(f'UPDATE bot_time SET stavka_depozit = {time.time()}  WHERE user_id = {user_id}')
            connect.commit()
            return
         else:
            await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , извините но арендовать можно раз в 12 часа", parse_mode='html')

       if house == 3:
         if stavkatime > period:
            await bot.send_message(message.chat.id, f"Вы успешно арендовали свой огромный дом и заработали 500.000")
            cursor.execute(f'UPDATE users SET balance = {balance + 500000} WHERE user_id = {user_id}')
            cursor.execute(f'UPDATE bot_time SET stavka_depozit = {time.time()}  WHERE user_id = {user_id}')
            connect.commit()
            return
         else:
            await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , извините но арендовать можно раз в 12 часа", parse_mode='html')


       if house == 4:
         if stavkatime > period:
            await bot.send_message(message.chat.id, f"Вы успешно арендовали свой коттедж и заработали 700.000")
            cursor.execute(f'UPDATE users SET balance = {balance + 700000} WHERE user_id = {user_id}')
            cursor.execute(f'UPDATE bot_time SET stavka_depozit = {time.time()}  WHERE user_id = {user_id}')
            connect.commit()
            return
         else:
            await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , извините но арендовать можно раз в 12 часа", parse_mode='html')

       if house == 5:
         if stavkatime > period:
            await bot.send_message(message.chat.id, f"Вы успешно арендовали свою бурдж кхалифу и заработали 1.000.000")
            cursor.execute(f'UPDATE users SET balance = {balance + 1000000} WHERE user_id = {user_id}')
            cursor.execute(f'UPDATE bot_time SET stavka_depozit = {time.time()}  WHERE user_id = {user_id}')
            connect.commit()
            return
         else:
            await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , извините но арендовать можно раз в 12 часа", parse_mode='html')

       if house == 6:
         if stavkatime > period:
            await bot.send_message(message.chat.id, f"Вы успешно арендовали свою россию и заработали 5.000.000")
            cursor.execute(f'UPDATE users SET balance = {balance + 5000000} WHERE user_id = {user_id}')
            cursor.execute(f'UPDATE bot_time SET stavka_depozit = {time.time()}  WHERE user_id = {user_id}')
            connect.commit()
            return
         else:
            await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , извините но арендовать можно раз в 12 часа", parse_mode='html')

       if house == 7:
         if stavkatime > period:
            await bot.send_message(message.chat.id, f"Вы успешно арендовали свою половину земли и заработали 10.000.000")
            cursor.execute(f'UPDATE users SET balance = {balance + 10000000} WHERE user_id = {user_id}')
            cursor.execute(f'UPDATE bot_time SET stavka_depozit = {time.time()}  WHERE user_id = {user_id}')
            connect.commit()
            return
         else:
            await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , извините но арендовать можно раз в 12 часа", parse_mode='html')

       if house == 8:
         if stavkatime > period:
            await bot.send_message(message.chat.id, f"Вы успешно арендовали свой марс и заработали 50.000.000 + \n За то что ваша имущества большая вам еше выдано 10🍩")
            cursor.execute(f'UPDATE users SET balance = {balance + 50000000} WHERE user_id = {user_id}')
            cursor.execute(f'UPDATE users SET donate_coins = {donate_coins + 10} WHERE user_id = {user_id}')
            cursor.execute(f'UPDATE bot_time SET stavka_depozit = {time.time()}  WHERE user_id = {user_id}')
            connect.commit()
            return
         else:
            await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a> , извините но арендовать можно раз в 12 часа", parse_mode='html')

       if house <= 0:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! У вас нету дома, что бы купить дом введите команду \"Дома\"", parse_mode='html')

    if message.text.lower() in ['Аренда', 'аренда']:
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       arenda_photo = open('arenda/arenda.jpg', 'rb')
       await bot.send_photo(chat_id=message.chat.id, photo=arenda_photo, caption=f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вы можете дать свое имущество в аренду и получать доход
   Доход зависит от крутости вашего имущества

   Арендовать дом > аренда дом    
       """, parse_mode='html') 


###########################################АВТОМОБИЛИ###########################################
    if message.text.lower().startswith("машина"):
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       balance = cursor.execute("SELECT balance from users where user_Id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])

       cars = cursor.execute("SELECT cars from cars where user_Id = ?", (message.from_user.id,)).fetchone()
       cars = int(cars[0])

       hp = cursor.execute("SELECT hp from cars where user_Id = ?", (message.from_user.id,)).fetchone()
       hp = int(hp[0])

       benz = cursor.execute("SELECT benz from cars where user_Id = ?", (message.from_user.id,)).fetchone()
       benz = int(benz[0])

       if benz in range(90, 100):
          benz2 = '100%'
       if benz in range(80, 89):
          benz2 = '90%'
       if benz in range(70, 79):
          benz2 = '80%'
       if benz in range(60, 69):
          benz2 = '70%'
       if benz in range(50, 59):
          benz2 = '60%'
       if benz in range(40, 49):
          benz2 = '50%'
       if benz in range(30, 39):
          benz2 = '40%'
       if benz in range(20, 29):
          benz2 = '30%'
       if benz in range(10, 19):
          benz2 = '20%'
       if benz in range(1, 9):
          benz2 = '10%'
          
       if benz < 0:
             benz2 = 0
       else:
          benz2 = benz
          
       if cars == 1:
          cars_name = 'ВАЗ 2107'
          cars_summ = 10000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 2:
          cars_name = 'Lada Vesta'
          cars_summ = 50000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 3:
          cars_name = 'Lada XRAY Cross'
          cars_summ = 100000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 4:
          cars_name = 'Audi Q7'
          cars_summ = 500000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 5:
          cars_name = 'BMW X6'
          cars_summ = 750000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 6:
          cars_name = 'Hyundai Solaris'
          cars_summ = 1000000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 7:
          cars_name = 'Toyota Supra'
          cars_summ = 1500000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 8:
          cars_name = 'Lamborghini Veneno'
          cars_summ = 3000000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 9:
          cars_name = 'Bugatti Veyron'
          cars_summ = 10000000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 10:
          cars_name = 'Tesla Roadster'
          cars_summ = 50000000000
          cars_summ2 = '{:,}'.format(cars_summ)

       
       if hp in range(76,100):
          hp2 = 'Хорошое 🟩'

       if hp in range(51,75):
          hp2 = 'Среднее 🟧 '
         
       if hp in range(26,50):
          hp2 = 'Плохое 🟥'

       if hp in range(2,25):
          hp2 = 'Ужасное 🛑'

       if hp < 2:
          hp2 = 'Требуется ремонт ⛔️'

       else:
          if hp == 100:
             hp2 = 'Хорошое 🟩'
          if hp == 76:
             hp2 = 'Хорошо '
          if hp == 65:
             hp2 = 'Среднее 🟧'
          if hp == 51:
             hp2 = 'Средне '
          if hp == 43:
             hp2 = 'Плохое 🟥'
          if hp == 36:
             hp2 = 'Плохо '
          if hp == 25:
             hp2 = 'Ужасное 🛑'
          if hp == 12:
             hp2 = 'Ужасно '    
    

       if cars == 10:
          tesla_photo = open('cars/Tesla.jpg', 'rb')
          await bot.send_photo(chat_id=message.chat.id, photo=tesla_photo, caption=f"""🚗 | <a href='tg://user?id={user_id}'>{user_name}</a>, ваша машина: {cars_name}
🚨 | Состояние: {hp2}
⛽️ | Бензин: {benz2}%
""", parse_mode='html')
       if cars == 9:
          toyota_photo = open('cars/Veyron.jpg', 'rb')
          await bot.send_photo(chat_id=message.chat.id, photo=toyota_photo, caption=f"""🚗 | <a href='tg://user?id={user_id}'>{user_name}</a>, ваша машина: {cars_name}
🚨 | Состояние: {hp2}
⛽️ | Бензин: {benz2}%
""", parse_mode='html')
       if cars == 8:
          honda_photo = open('cars/Lamborghini.jpg', 'rb')
          await bot.send_photo(chat_id=message.chat.id, photo=honda_photo, caption=f"""🚗 | <a href='tg://user?id={user_id}'>{user_name}</a>, ваша машина: {cars_name}
🚨 | Состояние: {hp2}
⛽️ | Бензин: {benz2}%
""", parse_mode='html')
       if cars == 7:
          lexus_photo = open('cars/Toyota.jpg', 'rb')
          await bot.send_photo(chat_id=message.chat.id, photo=lexus_photo, caption=f"""🚗 | <a href='tg://user?id={user_id}'>{user_name}</a>, ваша машина: {cars_name}
🚨 | Состояние: {hp2}
⛽️ | Бензин: {benz2}%
""", parse_mode='html')
       if cars == 6:
          kia_photo = open('cars/Hyundai_Solaris.jpg', 'rb')
          await bot.send_photo(chat_id=message.chat.id, photo=kia_photo, caption=f"""🚗 | <a href='tg://user?id={user_id}'>{user_name}</a>, ваша машина: {cars_name}
🚨 | Состояние: {hp2}
⛽️ | Бензин: {benz2}%
""", parse_mode='html')
       if cars == 5:
          opel_photo = open('cars/bmw.jpg', 'rb')
          await bot.send_photo(chat_id=message.chat.id, photo=opel_photo, caption=f"""🚗 | <a href='tg://user?id={user_id}'>{user_name}</a>, ваша машина: {cars_name}
🚨 | Состояние: {hp2}
⛽️ | Бензин: {benz2}%
""", parse_mode='html')
       if cars == 4:
          bentley_photo = open('cars/Audi.jpg', 'rb')
          await bot.send_photo(chat_id=message.chat.id, photo=bentley_photo, caption=f"""🚗 | <a href='tg://user?id={user_id}'>{user_name}</a>, ваша машина: {cars_name}
🚨 | Состояние: {hp2}
⛽️ | Бензин: {benz2}%
""", parse_mode='html')
       if cars == 3:
          uaz_photo = open('cars/lada_xray_cross.jpg', 'rb')
          await bot.send_photo(chat_id=message.chat.id, photo=uaz_photo, caption=f"""🚗 | <a href='tg://user?id={user_id}'>{user_name}</a>, ваша машина: {cars_name}
🚨 | Состояние: {hp2}
⛽️ | Бензин: {benz2}%
""", parse_mode='html')
       if cars == 2:
          moto_photo = open('cars/Lada_Vesta.jpg', 'rb')
          await bot.send_photo(chat_id=message.chat.id, photo=moto_photo, caption=f"""🚗 | <a href='tg://user?id={user_id}'>{user_name}</a>, ваша машина: {cars_name}
🚨 | Состояние: {hp2}
⛽️ | Бензин: {benz2}%
""", parse_mode='html')
       if cars == 1:
          gyro_photo = open('cars/lada.jpg', 'rb')
          await bot.send_photo(chat_id=message.chat.id, photo=gyro_photo, caption=f"""🚗 | <a href='tg://user?id={user_id}'>{user_name}</a>, ваша машина: {cars_name}
🚨 | Состояние: {hp2}
⛽️ | Бензин: {benz2}%
""", parse_mode='html')
          return
    
       if cars <= 0:
          await bot.send_message(message.chat.id, f"""<a href='tg://user?id={user_id}'>{user_name}</a>, <b>вот доступные машины:

🚗 1. ВАЗ 2107 - 10.000.000¢
🚗 2. Lada Vesta - 50.000.000¢
🚗 3. Lada XRAY Cross - 100.000.000¢
🚗 4. Audi Q7 - 500.000.000¢
🚗 5. BMW X6 - 750.000.000¢
🚗 6. Hyundai Solaris - 1.000.000.000¢
🚗 7. Toyota Supra - 1.500.000.000¢
🚗 8. Lamborghini Veneno - 3.000.000.000¢
🚗 9. Bugatti Veyron - 10.000.000.000¢ 
🚗 10. Tesla Roadster - 50.000.000.000¢ 

🛒 Для покупки машины введите:</b> <code>Купить машину</code> <b>[номер]</b>
    """, parse_mode='html')


    if message.text.startswith('Продать машину') or message.text.startswith('продать машину'):
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       balance = cursor.execute("SELECT balance from users where user_Id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])

       donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(message.from_user.id,)).fetchone()
       donate_coins = int(donate_coins[0])

       cars = cursor.execute("SELECT cars from cars where user_Id = ?", (message.from_user.id,)).fetchone()
       cars = int(cars[0])

       if cars == 1:
          cars_name = 'ВАЗ 2107'
          cars_summ = 10000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 2:
          cars_name = 'Lada Vesta'
          cars_summ = 50000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 3:
          cars_name = 'Lada XRAY Cross'
          cars_summ = 100000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 4:
          cars_name = 'Audi Q7'
          cars_summ = 500000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 5:
          cars_name = 'BMW X6'
          cars_summ = 750000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 6:
          cars_name = 'Hyundai Solaris'
          cars_summ = 1000000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 7:
          cars_name = 'Toyota Supra'
          cars_summ = 1500000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 8:
          cars_name = 'Lamborghini Veneno'
          cars_summ = 3000000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 9:
          cars_name = 'Bugatti Veyron'
          cars_summ = 10000000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 10:
          cars_name = 'Tesla Roadster'
          cars_summ = 50000000000
          cars_summ2 = '{:,}'.format(cars_summ)


       if cars > 0:
          await bot.send_message(message.chat.id, f"🚗 <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно продали машину {cars_name} за {cars_summ2}¢", parse_mode='html')
          cursor.execute(f'UPDATE cars SET cars = {0} WHERE user_id = {user_id}')
          cursor.execute(f'UPDATE cars SET hp = {0} WHERE user_id = {user_id}')
          cursor.execute(f'UPDATE cars SET benz = {0} WHERE user_id = {user_id}')
          cursor.execute(f'UPDATE users SET balance = {balance + cars_summ} WHERE user_id = {user_id}')
          connect.commit()
          return
       else:
          await bot.send_message(message.chat.id, f"""<a href='tg://user?id={user_id}'>{user_name}</a>, <b>вот доступные машины:

🚗 1. ВАЗ 2107 - 10.000.000¢
🚗 2. Lada Vesta - 50.000.000¢
🚗 3. Lada XRAY Cross - 100.000.000¢
🚗 4. Audi Q7 - 500.000.000¢
🚗 5. BMW X6 - 750.000.000¢
🚗 6. Hyundai Solaris - 1.000.000.000¢
🚗 7. Toyota Supra - 1.500.000.000¢
🚗 8. Lamborghini Veneno - 3.000.000.000¢
🚗 9. Bugatti Veyron - 10.000.000.000¢ 
🚗 10. Tesla Roadster - 50.000.000.000¢ 

🛒 Для покупки машины введите:</b> <code>Купить машину</code> <b>[номер]</b>
    """, parse_mode='html')
          return

    if message.text.startswith('Купить машину') or message.text.startswith('купить машину'):
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       balance = cursor.execute("SELECT balance from users where user_Id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])

       cars = cursor.execute("SELECT cars from cars where user_Id = ?", (message.from_user.id,)).fetchone()
       cars = int(cars[0])

       member = int(message.text.split()[2])
       
       if member == 1:
          cars_name = 'ВАЗ 2107'
          cars_summ = 10000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if member == 2:
          cars_name = 'Lada Vesta'
          cars_summ = 50000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if member == 3:
          cars_name = 'Lada XRAY Cross'
          cars_summ = 100000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if member == 4:
          cars_name = 'Audi Q7'
          cars_summ = 500000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if member == 5:
          cars_name = 'BMW X6'
          cars_summ = 750000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if member == 6:
          cars_name = 'Hyundai Solaris'
          cars_summ = 1000000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if member == 7:
          cars_name = 'Toyota Supra'
          cars_summ = 1500000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if member == 8:
          cars_name = 'Lamborghini Veneno'
          cars_summ = 3000000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if member == 9:
          cars_name = 'Bugatti Veyron'
          cars_summ = 10000000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if member == 10:
          cars_name = 'Tesla Roadster'
          cars_summ = 50000000000
          cars_summ2 = '{:,}'.format(cars_summ)


       if member > 0:
          if member < 11:
             if cars == 0:
                if balance >= cars_summ:
                   await bot.send_message(message.chat.id, f"🚗 <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно купили машину {cars_name} за {cars_summ2}¢", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - cars_summ} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE cars SET cars = {member} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE cars SET hp = {100} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE cars SET benz = {100} WHERE user_id = {user_id}')
                   connect.commit()
                else:
                   await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств!", parse_mode='html')
             else:
                await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, Ошибка! У вас уже есть машина", parse_mode='html')
          else:
             await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, Подождите! Нету такого номера машины", parse_mode='html')
       else:
          await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, Подождите! Нету такого номера машины", parse_mode='html')
          
          
##МиниОбнова
    if message.text.startswith('Гонка') or message.text.startswith('гонка'):
       
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id
       summ5 = message.text.split()[1]
       
       
       summ4 = (summ5).replace(' ', '').replace('k', '000').replace('е','e').replace('к', '000').replace(',', '').replace('.', '').replace("$", "").replace('м', '000000').replace('m', '000000').replace('т','000000000000')
       summ3 = float(summ4)
       summ = int(summ3)
       summ2 = '{:,}'.format(summ).replace(',', '.')
       
       loser = ['😐', '😕','😟','😔','😓']
       rloser = random.choice(loser)

       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])

       cars = cursor.execute("SELECT cars from cars where user_id = ?", (message.from_user.id,)).fetchone()
       cars = cars[0]

       hp = cursor.execute("SELECT hp from cars where user_id = ?", (message.from_user.id,)).fetchone()
       hp = int(hp[0])

       benz = cursor.execute("SELECT benz from cars where user_id = ?", (message.from_user.id,)).fetchone()
       benz = int(benz[0])

       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = round(int(balance[0]))

       if cars == 1:
          cars_name = 'ВАЗ 2107'
          cars_summ = 10000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 2:
          cars_name = 'Lada Vesta'
          cars_summ = 50000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 3:
          cars_name = 'Lada XRAY Cross'
          cars_summ = 100000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 4:
          cars_name = 'Audi Q7'
          cars_summ = 500000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 5:
          cars_name = 'BMW X6'
          cars_summ = 750000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 6:
          cars_name = 'Hyundai Solaris'
          cars_summ = 1000000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 7:
          cars_name = 'Toyota Supra'
          cars_summ = 1500000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 8:
          cars_name = 'Lamborghini Veneno'
          cars_summ = 3000000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 9:
          cars_name = 'Bugatti Veyron'
          cars_summ = 10000000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 10:
          cars_name = 'Tesla Roadster'
          cars_summ = 50000000000
          cars_summ2 = '{:,}'.format(cars_summ)




       rx = random.randint(0,1000)
       rx2 = random.randint(1,25)
       summ3 = summ * 2
       summ4 = '{:,}'.format(summ3)

       period = 5
       getе = cursor.execute("SELECT stavka_games FROM bot_time WHERE user_id = ?", (message.from_user.id,)).fetchone()
       last_stavka = int(getе[0])
       stavkatime = time.time() - float(last_stavka)
       if stavkatime > period:
          if summ <= balance:
            if summ > 0:
             if cars > 0:
                if hp > 0:
                   if cars == 11:
                      await bot.send_message(message.chat.id, f"""👤 <a href='tg://user?id={user_id}'>{user_name}</a>\n
Ставка принята Через 5 секунд начинается гонка""", parse_mode='html')
                      return
                   if benz > 0:
                      await bot.send_message(message.chat.id, f"""👤 <a href='tg://user?id={user_id}'>{user_name}</a>\n
Ставка принята Через 5 секунд начинается гонка
                      
                      """, parse_mode='html')
                      time.sleep(5)
                      if int(rx) in range(0,600):
                         await bot.send_message(message.chat.id, f"""👤 <a href='tg://user?id={user_id}'>{user_name}</a>
🏎 Машина: {cars_name}
🧾 Выигрыш: 0¢""", parse_mode='html')
                         cursor.execute(f'UPDATE cars SET hp = {hp - rx2} WHERE user_id = {user_id}')
                         cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                         cursor.execute(f'UPDATE cars SET benz = {benz - rx2} WHERE user_id = {user_id}')
                         cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                         connect.commit()
                      if int(rx) in range(601, 1000):
                         await bot.send_message(message.chat.id, f"""👤 <a href='tg://user?id={user_id}'>{user_name}</a>
🏎 Машина: {cars_name}
🧾 Выигрыш: {summ4}¢""", parse_mode='html')
                         cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = {user_id}')
                         cursor.execute(f'UPDATE users SET balance = {balance + summ * 2} WHERE user_id = {user_id}')
                         cursor.execute(f'UPDATE cars SET hp = {hp - rx2} WHERE user_id = {user_id}')
                         cursor.execute(f'UPDATE cars SET benz = {benz - rx2} WHERE user_id = {user_id}')
                         cursor.execute(f'UPDATE bot_time SET stavka_games = {time.time()} WHERE user_id = {user_id}')
                         connect.commit()
                   else:
                      await bot.send_message(message.chat.id, f"🛠 <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! У вас закончился бензин в автомобиле давайте поедим в мастерскую: <code>мастерская</code>", parse_mode='html')
                else:
                   await bot.send_message(message.chat.id, f"🛠 <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! У вас поломался автомобиль , вы не можете участвовать в гонках давайте поедим в мастерскую: <code>мастерская</code>", parse_mode='html')
             else:
                await bot.send_message(message.chat.id, f"🛠 <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! Какие гонки без автомобиля? Купите автомобиль", parse_mode='html') 
          else:
             await bot.send_message(message.chat.id, f"🛠 <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! У вас нехватает средств", parse_mode='html') 
       else:
          await bot.send_message(message.chat.id, f"🛠 <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! играть можно раз в {period} секунд", parse_mode='html') 


##МиниОбнова
    if message.text.lower() == 'мой грузовик':
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       balance = cursor.execute("SELECT balance from users where user_Id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])

       truck = cursor.execute("SELECT truck from truck where user_Id = ?", (message.from_user.id,)).fetchone()
       truck = int(truck[0])

       hp = cursor.execute("SELECT hp from truck where user_Id = ?", (message.from_user.id,)).fetchone()
       hp = int(hp[0])

       fuel = cursor.execute("SELECT fuel from truck where user_Id = ?", (message.from_user.id,)).fetchone()
       fuel = int(fuel[0])

       if fuel in range(90, 100):
          fuel2 = '100%'
       if fuel in range(80, 89):
          fuel2 = '90%'
       if fuel in range(70, 79):
          fuel2 = '80%'
       if fuel in range(60, 69):
          fuel2 = '70%'
       if fuel in range(50, 59):
          fuel2 = '60%'
       if fuel in range(40, 49):
          fuel2 = '50%'
       if fuel in range(30, 39):
          fuel2 = '40%'
       if fuel in range(20, 29):
          fuel2 = '30%'
       if fuel in range(10, 19):
          fuel2 = '20%'
       if fuel in range(1, 9):
          fuel2 = '10%'
          
       if fuel < 0:
             fuel2 = 0
       else:
          fuel2 = fuel
          
       if truck == 1:
          truck_name = 'Daf'
          truck_summ = 10000000
          truck_summ2 = '{:,}'.format(truck_summ)
       if truck == 2:
          truck_name = 'Scania'
          truck_summ = 50000000
          truck_summ2 = '{:,}'.format(truck_summ)
       if truck == 3:
          truck_name = 'Nissan'
          truck_summ = 100000000
          truck_summ2 = '{:,}'.format(truck_summ)
       if truck == 4:
          truck_name = 'Renault'
          truck_summ = 500000000
          truck_summ2 = '{:,}'.format(truck_summ)
       if truck == 5:
          truck_name = 'Volvo'
          truck_summ = 750000000
          truck_summ2 = '{:,}'.format(truck_summ)
       if truck == 6:
          truck_name = 'Man'
          truck_summ = 1000000000
          truck_summ2 = '{:,}'.format(truck_summ)
       if truck == 7:
          truck_name = 'Mercedes Benz'
          truck_summ = 1500000000
          truck_summ2 = '{:,}'.format(truck_summ)

       
       if hp in range(76,100):
          hp2 = 'Хорошое 🟩'

       if hp in range(51,75):
          hp2 = 'Среднее 🟧 '
         
       if hp in range(26,50):
          hp2 = 'Плохое 🟥'

       if hp in range(2,25):
          hp2 = 'Ужасное 🛑'

       if hp < 2:
          hp2 = 'Требуется ремонт ⛔️'

       else:
          if hp == 100:
             hp2 = 'Хорошое 🟩'
          if hp == 76:
             hp2 = 'Хорошо '
          if hp == 65:
             hp2 = 'Среднее 🟧'
          if hp == 51:
             hp2 = 'Средне '
          if hp == 43:
             hp2 = 'Плохое 🟥'
          if hp == 36:
             hp2 = 'Плохо '
          if hp == 25:
             hp2 = 'Ужасное 🛑'
          if hp == 12:
             hp2 = 'Ужасно '    
    

       if truck == 7:
          lexus_photo = open('truck/Mercedes.jpg', 'rb')
          await bot.send_photo(chat_id=message.chat.id, photo=lexus_photo, caption=f"""<a href='tg://user?id={user_id}'>{user_name}</a>, вот данные за ваш грузовик🚛

👤 | Владелец: {user_name}
🚛 | Грузовик: {truck_name}
🚨 | Состояние: {hp2}
⛽️ | Бензин: {fuel2}%
💰 | Стоимость: {truck_summ2}¢

ℹ️ Чтобы продать грузовик введите команду <code>Грузовик продать</code> 

⛽️ Поехать на заправку <code>заправка</code>
🏁 Поехать на рейс: <code>рейс</code> ставка""", parse_mode='html')
       if truck == 6:
          kia_photo = open('truck/Man.jpg', 'rb')
          await bot.send_photo(chat_id=message.chat.id, photo=kia_photo, caption=f"""<a href='tg://user?id={user_id}'>{user_name}</a>, вот данные за ваш грузовик🚛

👤 | Владелец: {user_name}
🚛 | Грузовик: {truck_name}
🚨 | Состояние: {hp2}
⛽️ | Бензин: {fuel2}%
💰 | Стоимость: {truck_summ2}¢

ℹ️ Чтобы продать грузовик введите команду <code>Грузовик продать</code> 

⛽️ Поехать на заправку <code>заправка</code>
🏁 Поехать на рейс: <code>рейс</code> ставка""", parse_mode='html')
       if truck == 5:
          opel_photo = open('truck/Volvo.jpg', 'rb')
          await bot.send_photo(chat_id=message.chat.id, photo=opel_photo, caption=f"""<a href='tg://user?id={user_id}'>{user_name}</a>, вот данные за ваш грузовик🚛

👤 | Владелец: {user_name}
🚛 | Грузовик: {truck_name}
🚨 | Состояние: {hp2}
⛽️ | Бензин: {fuel2}%
💰 | Стоимость: {truck_summ2}¢

ℹ️ Чтобы продать грузовик введите команду <code>Грузовик продать</code> 

⛽️ Поехать на заправку <code>заправка</code>
🏁 Поехать на рейс: <code>рейс</code> ставка""", parse_mode='html')
       if truck == 4:
          bentley_photo = open('truck/Renault.jpg', 'rb')
          await bot.send_photo(chat_id=message.chat.id, photo=bentley_photo, caption=f"""<a href='tg://user?id={user_id}'>{user_name}</a>, вот данные за ваш грузовик🚛

👤 | Владелец: {user_name}
🚛 | Грузовик: {truck_name}
🚨 | Состояние: {hp2}
⛽️ | Бензин: {fuel2}%
💰 | Стоимость: {truck_summ2}¢

ℹ️ Чтобы продать грузовик введите команду <code>Грузовик продать</code> 

⛽️ Поехать на заправку <code>заправка</code>
🏁 Поехать на рейс: <code>рейс</code> ставка""", parse_mode='html')
       if truck == 3:
          uaz_photo = open('truck/Nissan.jpg', 'rb')
          await bot.send_photo(chat_id=message.chat.id, photo=uaz_photo, caption=f"""<a href='tg://user?id={user_id}'>{user_name}</a>, вот данные за ваш грузовик🚛

👤 | Владелец: {user_name}
🚛 | Грузовик: {truck_name}
🚨 | Состояние: {hp2}
⛽️ | Бензин: {fuel2}%
💰 | Стоимость: {truck_summ2}¢

ℹ️ Чтобы продать грузовик введите команду <code>Грузовик продать</code> 

⛽️ Поехать на заправку <code>заправка</code>
🏁 Поехать на рейс: <code>рейс</code> ставка""", parse_mode='html')
       if truck == 2:
          moto_photo = open('truck/Scania.jpg', 'rb')
          await bot.send_photo(chat_id=message.chat.id, photo=moto_photo, caption=f"""<a href='tg://user?id={user_id}'>{user_name}</a>, вот данные за ваш грузовик🚛

👤 | Владелец: {user_name}
🚛 | Грузовик: {truck_name}
🚨 | Состояние: {hp2}
⛽️ | Бензин: {fuel2}%
💰 | Стоимость: {truck_summ2}¢

ℹ️ Чтобы продать грузовик введите команду <code>Грузовик продать</code> 

⛽️ Поехать на заправку <code>заправка</code>
🏁 Поехать на рейс: <code>рейс</code> ставка""", parse_mode='html')
       if truck == 1:
          gyro_photo = open('truck/Daf.jpg', 'rb')
          await bot.send_photo(chat_id=message.chat.id, photo=gyro_photo, caption=f"""<a href='tg://user?id={user_id}'>{user_name}</a>, вот данные за ваш грузовик🚛

👤 | Владелец: {user_name}
🚛 | Грузовик: {truck_name}
🚨 | Состояние: {hp2}
⛽️ | Бензин: {fuel2}%
💰 | Стоимость: {truck_summ2}¢

ℹ️ Чтобы продать грузовик введите команду <code>Грузовик продать</code> 

⛽️ Поехать на заправку <code>заправка</code>
🏁 Поехать на рейс: <code>рейс</code> ставка""", parse_mode='html')
          return
    
       if truck <= 0:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, Подождите! У вас и так нету грузовика", parse_mode='html')    


    if message.text.lower() == 'грузовик продать':
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       balance = cursor.execute("SELECT balance from users where user_Id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])

       donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(message.from_user.id,)).fetchone()
       donate_coins = int(donate_coins[0])

       truck = cursor.execute("SELECT truck from truck where user_Id = ?", (message.from_user.id,)).fetchone()
       truck = int(truck[0])

       if truck == 1:
          truck_name = 'Daf'
          truck_summ = 10000000
          truck_summ2 = '{:,}'.format(truck_summ)
       if truck == 2:
          truck_name = 'Scania'
          truck_summ = 50000000
          truck_summ2 = '{:,}'.format(truck_summ)
       if truck == 3:
          truck_name = 'Nissan'
          truck_summ = 100000000
          truck_summ2 = '{:,}'.format(truck_summ)
       if truck == 4:
          truck_name = 'Renault'
          truck_summ = 500000000
          truck_summ2 = '{:,}'.format(truck_summ)
       if truck == 5:
          truck_name = 'Volvo'
          truck_summ = 750000000
          truck_summ2 = '{:,}'.format(truck_summ)
       if truck == 6:
          truck_name = 'Man'
          truck_summ = 1000000000
          truck_summ2 = '{:,}'.format(truck_summ)
       if truck == 7:
          truck_name = 'Mercedes Benz'
          truck_summ = 1500000000
          truck_summ2 = '{:,}'.format(truck_summ)


       if truck > 0:
          await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, Вы успешно продали грузовик 🚛 {truck_name} за {truck_summ2}¢", parse_mode='html')
          cursor.execute(f'UPDATE truck SET truck = {0} WHERE user_id = {user_id}')
          cursor.execute(f'UPDATE truck SET hp = {0} WHERE user_id = {user_id}')
          cursor.execute(f'UPDATE truck SET fuel = {0} WHERE user_id = {user_id}')
          cursor.execute(f'UPDATE users SET balance = {balance + truck_summ} WHERE user_id = {user_id}')
          connect.commit()
          return
       else:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, Подождите! У вас и так нету грузовика", parse_mode='html')
          return

    if message.text.startswith("купить грузовик") or message.text.startswith("Купить грузовик"):
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       balance = cursor.execute("SELECT balance from users where user_Id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])

       truck = cursor.execute("SELECT truck from truck where user_Id = ?", (message.from_user.id,)).fetchone()
       truck = int(truck[0])

       member = int(message.text.split()[2])
       
       if member == 1:
          truck_name = 'Daf'
          truck_summ = 10000000
          truck_summ2 = '{:,}'.format(truck_summ)
       if member == 2:
          truck_name = 'Scania'
          truck_summ = 50000000
          truck_summ2 = '{:,}'.format(truck_summ)
       if member == 3:
          truck_name = 'Nissan'
          truck_summ = 100000000
          truck_summ2 = '{:,}'.format(truck_summ)
       if member == 4:
          truck_name = 'Renault'
          truck_summ = 500000000
          truck_summ2 = '{:,}'.format(truck_summ)
       if member == 5:
          truck_name = 'Volvo'
          truck_summ = 750000000
          truck_summ2 = '{:,}'.format(truck_summ)
       if member == 6:
          truck_name = 'Man'
          truck_summ = 1000000000
          truck_summ2 = '{:,}'.format(truck_summ)
       if member == 7:
          truck_name = 'Mercedes Benz'
          truck_summ = 1500000000
          truck_summ2 = '{:,}'.format(truck_summ)


       if member > 0:
          if member < 8:
             if truck == 0:
                if balance >= truck_summ:
                   await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, Вы успешно купили грузовик 🚛 {truck_name} за {truck_summ2}¢", parse_mode='html')
                   cursor.execute(f'UPDATE users SET balance = {balance - truck_summ} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE truck SET truck = {member} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE truck SET hp = {100} WHERE user_id = {user_id}')
                   cursor.execute(f'UPDATE truck SET fuel = {100} WHERE user_id = {user_id}')
                   connect.commit()
                else:
                   await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств!", parse_mode='html')
             else:
                await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, Ошибка! У вас уже есть грузовик", parse_mode='html')
          else:
             await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, Подождите! Нету такого номера грузовика", parse_mode='html')
       else:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, Подождите! Нету такого номера грузовика", parse_mode='html')
          
          
                        
    if message.text.lower() in ["грузовики", "Грузовики"]:
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       chat_id = message.chat.id
       user_id = message.from_user.id
       await bot.send_message(message.chat.id, f"""<a href='tg://user?id={user_id}'>{user_name}</a>, доступные грузовики:
🚛 1. Daf - 10.000.000¢
🚛 2. Scania - 50.000.000¢
🚛 3. Nissan - 100.000.000¢
🚛 4. Renault - 500.000.000¢
🚛 5. Volvo - 750.000.000¢
🚛 6. Man - 1.000.000.000¢
🚛 7. Mercedes Benz - 1.500.000.000¢

🛒 Для покупки грузовика введите: Купить грузовик [номер]\nℹ Для просмотра информации о своей грузовика: Мой грузовик""", parse_mode='html')


###############################################МАСТЕРСКАЯ############################################
    if message.text.startswith('Мастерская') or message.text.startswith('мастерская'):
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       balance = cursor.execute("SELECT balance from users where user_Id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])

       hp = cursor.execute("SELECT hp from cars where user_id = ?", (message.from_user.id,)).fetchone()
       hp = int(hp[0])
       
       benz = cursor.execute("SELECT benz from cars where user_Id = ?", (message.from_user.id,)).fetchone()
       benz = int(benz[0])

       cars = cursor.execute("SELECT cars from cars where user_Id = ?", (message.from_user.id,)).fetchone()
       cars = int(cars[0])

       
       if cars == 1:
          cars_name = 'ВАЗ 2107'
          cars_summ = 10000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 2:
          cars_name = 'Lada Vesta'
          cars_summ = 50000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 3:
          cars_name = 'Lada XRAY Cross'
          cars_summ = 100000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 4:
          cars_name = 'Audi Q7'
          cars_summ = 500000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 5:
          cars_name = 'BMW X6'
          cars_summ = 750000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 6:
          cars_name = 'Hyundai Solaris'
          cars_summ = 1000000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 7:
          cars_name = 'Toyota Supra'
          cars_summ = 1500000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 8:
          cars_name = 'Lamborghini Veneno'
          cars_summ = 3000000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 9:
          cars_name = 'Bugatti Veyron'
          cars_summ = 10000000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 10:
          cars_name = 'Tesla Roadster'
          cars_summ = 50000000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 11:
          cars_name = 'Koenigsegg'
          cars_summ = 100000000000
          cars_summ2 = '{:,}'.format(cars_summ)


       if hp in range(81,100):
          hp2 = 'Хорошое 🟩'
         
       if hp in range(71,80):
          hp2 = 'Хорошое 🟩'

       if hp in range(61,70):
          hp2 = 'Среднее 🟧 '

       if hp in range(51,60):
          hp2 = 'Среднее 🟧 '
        
       if hp in range(41,50):
          hp2 = 'Плохое 🟥'

       if hp in range(31,40):
          hp2 = 'Плохое 🟥'          

       if hp in range(21,30):
          hp2 = 'Ужасное 🛑'

       if hp in range(11,20):
          hp2 = 'Ужасное 🛑'

       if hp in range(1,10):
          hp2 = 'Ужасное 🛑'          

       if hp < 2:
          hp2 = 'Требуется ремонт ⛔️'

       else:
          if hp == 100:
             hp2 = 'Хорошое 🟩'
          if hp == 80:
             hp2 = 'Хорошо '
          if hp == 70:
             hp2 = 'Среднее 🟧'
          if hp == 60:
             hp2 = 'Средне '
          if hp == 50:
             hp2 = 'Плохое 🟥'
          if hp == 40:
             hp2 = 'Плохо '
          if hp == 30:
             hp2 = 'Ужасное 🛑'
          if hp == 20:
             hp2 = 'Ужасно '


       if hp < 80:
          if hp > 70:
             summ = 20000
             summ2 = '{:,}'.format(summ)

       if hp < 70:
          if hp > 60:
             summ = 30000
             summ2 = '{:,}'.format(summ)
      
       if hp < 60:
          if hp > 50:
             summ = 40000
             summ2 = '{:,}'.format(summ)

       if hp < 50:
          if hp > 40:
             summ = 50000
             summ2 = '{:,}'.format(summ)

       if hp < 40:
          if hp > 30:
             summ = 60000
             summ2 = '{:,}'.format(summ)

       if hp < 30:
          if hp > 20:
             summ = 70000
             summ2 = '{:,}'.format(summ)

       if hp < 30:
          if hp > 20:
             summ = 80000
             summ2 = '{:,}'.format(summ)

       if hp < 20:
          if hp > 10:
             summ = 90000
             summ2 = '{:,}'.format(summ)

       if hp < 10:
          summ = 100000
          summ2 = '{:,}'.format(summ)

       if hp <= 100:
          if hp > 90:
             summ = 5000
             summ2 = '{:,}'.format(summ)

       if hp <= 90:
          if hp > 80:
             summ = 10000
             summ2 = '{:,}'.format(summ)
             
       
       if benz in range(90, 100):
          benz2 = '100%'
       
       if benz in range(80, 89):
          benz2 = '90%'
       
       if benz in range(70, 79):
          benz2 = '80%'
       
       if benz in range(60, 69):
          benz2 = '70%'
       
       if benz in range(50, 59):
          benz2 = '60%'
       
       if benz in range(40, 49):
          benz2 = '50%'
       
       if benz in range(30, 39):
          benz2 = '40%'
       
       if benz in range(20, 29):
          benz2 = '30%'
       
       if benz in range(10, 19):
          benz2 = '20%'
       
       if benz in range(1, 9):
          benz2 = '10%'
       
       if benz < 0:
             benz2 = 0
       
       else:
          benz2 = benz

       if benz2 < 80:
          if benz2 > 70:
             summ = 20000
             summ2 = '{:,}'.format(summ)

       if benz2 < 70:
          if benz2 > 60:
             summ = 30000
             summ2 = '{:,}'.format(summ)
      
       if benz2 < 60:
          if benz2 > 50:
             summ = 40000
             summ2 = '{:,}'.format(summ)

       if benz2 < 50:
          if benz2 > 40:
             summ = 50000
             summ2 = '{:,}'.format(summ)

       if benz2 < 40:
          if benz2 > 30:
             summ = 60000
             summ2 = '{:,}'.format(summ)

       if benz2 < 30:
          if benz2 > 20:
             summ = 70000
             summ2 = '{:,}'.format(summ)

       if benz2 < 30:
          if benz2 > 20:
             summ = 80000
             summ2 = '{:,}'.format(summ)

       if benz2 < 20:
          if benz2 > 10:
             summ = 90000
             summ2 = '{:,}'.format(summ)

       if benz2 < 10:
          summ = 100000
          summ2 = '{:,}'.format(summ)             


       master_photo = open('imges/usta.jpg', 'rb')
       await bot.send_photo(chat_id=message.chat.id, photo=master_photo, caption=f"""
<a href='tg://user?id={user_id}'>{user_name}</a> › добро пожаловать в заправку
Стоимость бензина не зависит от вашей машины за 10% 
вы отдаёте 10.000

Ваша машина > {cars_name}
Состояние > {hp2}
Бензин > {benz2}%

Состояние {hp2}% / 'Хорошое 🟩'
Стоимость {summ2}¢

Заправлено {benz2}% / 100%
Стоимость {summ2}¢

Напишите чтобы починить машину <code>починить</code>
Напишите чтобы заправить машину <code>заправить</code>

       """, parse_mode='html')

#######Заправка
    if message.text.startswith('Заправить') or message.text.startswith('заправить'):
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       balance = cursor.execute("SELECT balance from users where user_Id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])

       cars = cursor.execute("SELECT cars from cars where user_Id = ?", (message.from_user.id,)).fetchone()
       cars = int(cars[0])

       benz = cursor.execute("SELECT benz from cars where user_Id = ?", (message.from_user.id,)).fetchone()
       benz = int(benz[0])

       
       if cars == 1:
          cars_name = 'ВАЗ 2107'
          cars_summ = 10000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 2:
          cars_name = 'Lada Vesta'
          cars_summ = 50000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 3:
          cars_name = 'Lada XRAY Cross'
          cars_summ = 100000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 4:
          cars_name = 'Audi Q7'
          cars_summ = 500000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 5:
          cars_name = 'BMW X6'
          cars_summ = 750000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 6:
          cars_name = 'Hyundai Solaris'
          cars_summ = 1000000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 7:
          cars_name = 'Toyota Supra'
          cars_summ = 1500000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 8:
          cars_name = 'Lamborghini Veneno'
          cars_summ = 3000000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 9:
          cars_name = 'Bugatti Veyron'
          cars_summ = 10000000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 10:
          cars_name = 'Tesla Roadster'
          cars_summ = 50000000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 11:
          cars_name = 'Koenigsegg'
          cars_summ = 100000000000
          cars_summ2 = '{:,}'.format(cars_summ)


       if benz <= 80:
          if benz > 70:
             if balance > 20000:
                await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, Вы успешно заправили машину 🚘 {cars_name} за 20.000¢", parse_mode='html')
                cursor.execute(f'UPDATE cars SET benz = {100} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE users SET balance = {balance - 20000} WHERE user_id = {user_id}')
                connect.commit()
             else:
                await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств!", parse_mode='html')
       else:
          await bot.send_message(message.chat.id, f" 🆘 | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>, у вашей машины полно бензина", parse_mode='html')
          

       if benz <= 70:
          if benz > 60:
             if balance > 30000:
                await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, Вы успешно заправили машину 🚘 {cars_name} за 30.000¢", parse_mode='html')
                cursor.execute(f'UPDATE cars SET benz = {100} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE users SET balance = {balance - 30000} WHERE user_id = {user_id}')
                connect.commit()
             else:
                await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств!", parse_mode='html')
                return

       if benz <= 60:
          if benz > 50:
             if balance > 40000:
                await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, Вы успешно заправили машину 🚘 {cars_name} за 40.000¢", parse_mode='html')
                cursor.execute(f'UPDATE cars SET benz = {100} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE users SET balance = {balance - 40000} WHERE user_id = {user_id}')
                connect.commit()
             else:
                await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств!", parse_mode='html')
                return

       if benz <= 50:
          if benz > 40:
             if balance > 50000:
                await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, Вы успешно заправили машину 🚘 {cars_name} за 50.000¢", parse_mode='html')
                cursor.execute(f'UPDATE cars SET benz = {100} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE users SET balance = {balance - 50000} WHERE user_id = {user_id}')
                connect.commit()
             else:
                await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств!", parse_mode='html')
                return

       if benz <= 40:
          if benz > 30:
             if balance > 60000:
                await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, Вы успешно заправили машину 🚘 {cars_name} за 60.000¢", parse_mode='html')
                cursor.execute(f'UPDATE cars SET benz = {100} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE users SET balance = {balance - 60000} WHERE user_id = {user_id}')
                connect.commit()
             else:
                await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств!", parse_mode='html')
                return

       if benz <= 30:
          if benz > 20:
             if balance > 70000:
                await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, Вы успешно заправили машину 🚘 {cars_name} за 70.000¢", parse_mode='html')
                cursor.execute(f'UPDATE cars SET benz = {100} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE users SET balance = {balance - 70000} WHERE user_id = {user_id}')
                connect.commit()
             else:
                await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств!", parse_mode='html')
                return

       if benz <= 20:
          if benz > 10:
             if balance > 80000:
                await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, Вы успешно заправили машину 🚘 {cars_name} за 80.000¢", parse_mode='html')
                cursor.execute(f'UPDATE cars SET benz = {100} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE users SET balance = {balance - 80000} WHERE user_id = {user_id}')
                connect.commit()
             else:
                await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств!", parse_mode='html')
                return

       if benz <= 10:
             if balance > 90000:
                await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, Вы успешно заправили машину 🚘 {cars_name} за 90.000¢", parse_mode='html')
                cursor.execute(f'UPDATE cars SET benz = {100} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE users SET balance = {balance - 90000} WHERE user_id = {user_id}')
                connect.commit()
             else:
                await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств!", parse_mode='html')
                

#######Починка
    if message.text.startswith('Починить') or message.text.startswith('починить'):
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       balance = cursor.execute("SELECT balance from users where user_Id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])

       hp = cursor.execute("SELECT hp from cars where user_Id = ?", (message.from_user.id,)).fetchone()
       hp = int(hp[0])

       cars = cursor.execute("SELECT cars from cars where user_Id = ?", (message.from_user.id,)).fetchone()
       cars = int(cars[0])


       if cars == 1:
          cars_name = 'ВАЗ 2107'
          cars_summ = 10000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 2:
          cars_name = 'Lada Vesta'
          cars_summ = 50000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 3:
          cars_name = 'Lada XRAY Cross'
          cars_summ = 100000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 4:
          cars_name = 'Audi Q7'
          cars_summ = 500000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 5:
          cars_name = 'BMW X6'
          cars_summ = 750000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 6:
          cars_name = 'Hyundai Solaris'
          cars_summ = 1000000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 7:
          cars_name = 'Toyota Supra'
          cars_summ = 1500000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 8:
          cars_name = 'Lamborghini Veneno'
          cars_summ = 3000000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 9:
          cars_name = 'Bugatti Veyron'
          cars_summ = 10000000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 10:
          cars_name = 'Tesla Roadster'
          cars_summ = 50000000000
          cars_summ2 = '{:,}'.format(cars_summ)
       if cars == 11:
          cars_name = 'Koenigsegg'
          cars_summ = 100000000000
          cars_summ2 = '{:,}'.format(cars_summ)



       
       if hp in range(76,100):
          hp2 = 'Хорошое 🟩'

       if hp in range(51,75):
          hp2 = 'Среднее 🟧 '
         
       if hp in range(26,50):
          hp2 = 'Плохое 🟥'

       if hp in range(2,25):
          hp2 = 'Ужасное 🛑'

       if hp < 2:
          hp2 = 'Требуется ремонт ⛔️'

       else:
          if hp == 100:
             hp2 = 'Хорошое 🟩'
          if hp == 76:
             hp2 = 'Хорошо '
          if hp == 65:
             hp2 = 'Среднее 🟧'
          if hp == 51:
             hp2 = 'Средне '
          if hp == 43:
             hp2 = 'Плохое 🟥'
          if hp == 36:
             hp2 = 'Плохо '
          if hp == 25:
             hp2 = 'Ужасное 🛑'
          if hp == 12:
             hp2 = 'Ужасно '

       if hp <= 80:
          if hp > 70:
             if balance > 20000:
                await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, Вы успешно починили машину 🚘 {cars_name} за 20.000¢", parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - 20000} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE cars SET hp = {100} WHERE user_id = {user_id}')
                connect.commit()
             else:
                await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств!", parse_mode='html')
       else:
          await bot.send_message(message.chat.id, f" 🆘 | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>, ваша машина еше несломалась", parse_mode='html')
          

       if hp <= 70:
          if hp > 60:
             if balance > 30000:
                await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, Вы успешно починили машину 🚘 {cars_name} за 30.000¢", parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - 30000} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE cars SET hp = {100} WHERE user_id = {user_id}')
                connect.commit()
             else:
                await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств!", parse_mode='html')
             

       if hp <= 60:
          if hp > 50:
             if balance > 40000:
                await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, Вы успешно починили машину 🚘 {cars_name} за 40.000¢", parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - 40000} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE cars SET hp = {100} WHERE user_id = {user_id}')
                connect.commit()
             else:
                await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств!", parse_mode='html')


       if hp <= 50:
          if hp > 40:
             if balance > 50000:
                await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, Вы успешно починили машину 🚘 {cars_name} за 20.000¢", parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - 20000} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE cars SET hp = {100} WHERE user_id = {user_id}')
                connect.commit()
             else:
                await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств!", parse_mode='html')
             

       if hp <= 40:
          if hp > 30:
             if balance > 60000:
                await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, Вы успешно починили машину 🚘 {cars_name} за 60.000¢", parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - 60000} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE cars SET hp = {100} WHERE user_id = {user_id}')
                connect.commit()
             else:
                await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств!", parse_mode='html')
             

       if hp <= 30:
          if hp >20:
             if balance > 70000:
                await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, Вы успешно починили машину 🚘 {cars_name} за 70.000¢", parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - 70000} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE cars SET hp = {100} WHERE user_id = {user_id}')
                connect.commit()
             else:
                await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств!", parse_mode='html')
             

       if hp <= 20:
          if hp > 10:
             if balance > 80000:
                await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, Вы успешно починили машину 🚘 {cars_name} за 80.000¢", parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - 80000} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE cars SET hp = {100} WHERE user_id = {user_id}')
                connect.commit()
             else:
                await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств!", parse_mode='html')
             

       if hp <= 10:
             if balance > 90000:
                await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, Вы успешно починили машину 🚘 {cars_name} за 90.000¢", parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - 90000} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE cars SET hp = {100} WHERE user_id = {user_id}')
                connect.commit()
             else:
                await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств!", parse_mode='html')


##МиниОбнова
    if message.text.startswith('Заправка') or message.text.startswith('заправка'):
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       balance = cursor.execute("SELECT balance from users where user_Id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])

       hp = cursor.execute("SELECT hp from truck where user_id = ?", (message.from_user.id,)).fetchone()
       hp = int(hp[0])
       
       fuel = cursor.execute("SELECT fuel from truck where user_Id = ?", (message.from_user.id,)).fetchone()
       fuel = int(fuel[0])

       truck = cursor.execute("SELECT truck from truck where user_Id = ?", (message.from_user.id,)).fetchone()
       truck = int(truck[0])

       
       if truck == 1:
          truck_name = 'Daf'
          truck_summ = 10000000
          truck_summ2 = '{:,}'.format(truck_summ)
       if truck == 2:
          truck_name = 'Scania'
          truck_summ = 50000000
          truck_summ2 = '{:,}'.format(truck_summ)
       if truck == 3:
          truck_name = 'Nissan'
          truck_summ = 100000000
          truck_summ2 = '{:,}'.format(truck_summ)
       if truck == 4:
          truck_name = 'Renault'
          truck_summ = 500000000
          truck_summ2 = '{:,}'.format(truck_summ)
       if truck == 5:
          truck_name = 'Volvo'
          truck_summ = 750000000
          truck_summ2 = '{:,}'.format(truck_summ)
       if truck == 6:
          truck_name = 'Man'
          truck_summ = 1000000000
          truck_summ2 = '{:,}'.format(truck_summ)
       if truck == 7:
          truck_name = 'Mercedes Benz'
          truck_summ = 1500000000
          truck_summ2 = '{:,}'.format(truck_summ)


       if hp in range(81,100):
          hp2 = 'Хорошое 🟩'
         
       if hp in range(71,80):
          hp2 = 'Хорошое 🟩'

       if hp in range(61,70):
          hp2 = 'Среднее 🟧 '

       if hp in range(51,60):
          hp2 = 'Среднее 🟧 '
        
       if hp in range(41,50):
          hp2 = 'Плохое 🟥'

       if hp in range(31,40):
          hp2 = 'Плохое 🟥'          

       if hp in range(21,30):
          hp2 = 'Ужасное 🛑'

       if hp in range(11,20):
          hp2 = 'Ужасное 🛑'

       if hp in range(1,10):
          hp2 = 'Ужасное 🛑'          

       if hp < 2:
          hp2 = 'Требуется ремонт ⛔️'

       else:
          if hp == 100:
             hp2 = 'Хорошое 🟩'
          if hp == 80:
             hp2 = 'Хорошо '
          if hp == 70:
             hp2 = 'Среднее 🟧'
          if hp == 60:
             hp2 = 'Средне '
          if hp == 50:
             hp2 = 'Плохое 🟥'
          if hp == 40:
             hp2 = 'Плохо '
          if hp == 30:
             hp2 = 'Ужасное 🛑'
          if hp == 20:
             hp2 = 'Ужасно '


       if hp < 80:
          if hp > 70:
             summ = 20000
             summ2 = '{:,}'.format(summ)

       if hp < 70:
          if hp > 60:
             summ = 30000
             summ2 = '{:,}'.format(summ)
      
       if hp < 60:
          if hp > 50:
             summ = 40000
             summ2 = '{:,}'.format(summ)

       if hp < 50:
          if hp > 40:
             summ = 50000
             summ2 = '{:,}'.format(summ)

       if hp < 40:
          if hp > 30:
             summ = 60000
             summ2 = '{:,}'.format(summ)

       if hp < 30:
          if hp > 20:
             summ = 70000
             summ2 = '{:,}'.format(summ)

       if hp < 30:
          if hp > 20:
             summ = 80000
             summ2 = '{:,}'.format(summ)

       if hp < 20:
          if hp > 10:
             summ = 90000
             summ2 = '{:,}'.format(summ)

       if hp < 10:
          summ = 100000
          summ2 = '{:,}'.format(summ)

       if hp <= 100:
          if hp > 90:
             summ = 5000
             summ2 = '{:,}'.format(summ)

       if hp <= 90:
          if hp > 80:
             summ = 10000
             summ2 = '{:,}'.format(summ)
             
       
       if fuel in range(90, 100):
          fuel2 = '100%'
       
       if fuel in range(80, 89):
          fuel2 = '90%'
       
       if fuel in range(70, 79):
          fuel2 = '80%'
       
       if fuel in range(60, 69):
          fuel2 = '70%'
       
       if fuel in range(50, 59):
          fuel2 = '60%'
       
       if fuel in range(40, 49):
          benz2 = '50%'
       
       if fuel in range(30, 39):
          fuel2 = '40%'
       
       if fuel in range(20, 29):
          fuel2 = '30%'
       
       if fuel in range(10, 19):
          fuel2 = '20%'
       
       if fuel in range(1, 9):
          fuel2 = '10%'
       
       if fuel < 0:
             fuel2 = 0
       
       else:
          fuel2 = fuel

       if fuel2 < 80:
          if fuel2 > 70:
             summ = 20000
             summ2 = '{:,}'.format(summ)

       if fuel2 < 70:
          if fuel2 > 60:
             summ = 30000
             summ2 = '{:,}'.format(summ)
      
       if fuel2 < 60:
          if fuel2 > 50:
             summ = 40000
             summ2 = '{:,}'.format(summ)

       if fuel2 < 50:
          if fuel2 > 40:
             summ = 50000
             summ2 = '{:,}'.format(summ)

       if fuel2 < 40:
          if fuel2 > 30:
             summ = 60000
             summ2 = '{:,}'.format(summ)

       if fuel2 < 30:
          if fuel2 > 20:
             summ = 70000
             summ2 = '{:,}'.format(summ)

       if fuel2 < 30:
          if fuel2 > 20:
             summ = 80000
             summ2 = '{:,}'.format(summ)

       if fuel2 < 20:
          if fuel2 > 10:
             summ = 90000
             summ2 = '{:,}'.format(summ)

       if fuel2 < 10:
          summ = 100000
          summ2 = '{:,}'.format(summ)             


       master_photo = open('imges/metan2.jpg', 'rb')
       await bot.send_photo(chat_id=message.chat.id, photo=master_photo, caption=f"""
<a href='tg://user?id={user_id}'>{user_name}</a> › добро пожаловать в заправку
Стоимость бензина не зависит от вашей грузовика за 10% 
вы отдаёте 10.000

Ваш грузовик > {truck_name}
Состояние > {hp2}
Бензин > {fuel2}%

Состояние {hp2}% / 'Хорошое 🟩'
Стоимость {summ2}¢

Заправлено {fuel2}% / 100%
Стоимость {summ2}¢

Напишите чтобы починить грузовик <code>Грузовик починить</code>
Напишите чтобы заправить грузовик <code>Грузовик заправить</code>

       """, parse_mode='html')

#######Заправка
    if message.text.startswith('Грузовик заправить') or message.text.startswith('грузовик заправить'):
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       balance = cursor.execute("SELECT balance from users where user_Id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])

       truck = cursor.execute("SELECT truck from truck where user_Id = ?", (message.from_user.id,)).fetchone()
       truck = int(truck[0])

       fuel = cursor.execute("SELECT fuel from truck where user_Id = ?", (message.from_user.id,)).fetchone()
       fuel = int(fuel[0])

       
       if truck == 1:
          truck_name = 'Daf'
          truck_summ = 10000000
          truck_summ2 = '{:,}'.format(truck_summ)
       if truck == 2:
          truck_name = 'Scania'
          truck_summ = 50000000
          truck_summ2 = '{:,}'.format(truck_summ)
       if truck == 3:
          truck_name = 'Nissan'
          truck_summ = 100000000
          truck_summ2 = '{:,}'.format(truck_summ)
       if truck == 4:
          truck_name = 'Renault'
          truck_summ = 500000000
          truck_summ2 = '{:,}'.format(truck_summ)
       if truck == 5:
          truck_name = 'Volvo'
          truck_summ = 750000000
          truck_summ2 = '{:,}'.format(truck_summ)
       if truck == 6:
          truck_name = 'Man'
          truck_summ = 1000000000
          truck_summ2 = '{:,}'.format(truck_summ)
       if truck == 7:
          truck_name = 'Mercedes Benz'
          truck_summ = 1500000000
          truck_summ2 = '{:,}'.format(truck_summ)


       if benz <= 80:
          if benz > 70:
             if balance > 20000:
                await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, Вы успешно заправили грузовик 🚚 {truck_name} за 20.000₽", parse_mode='html')
                cursor.execute(f'UPDATE truck SET fuel = {100} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE users SET balance = {balance - 20000} WHERE user_id = {user_id}')
                connect.commit()
             else:
                await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств!", parse_mode='html')
       else:
          await bot.send_message(message.chat.id, f" 🆘 | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>, у вашей грузовика полно бензина", parse_mode='html')
          

       if benz <= 70:
          if benz > 60:
             if balance > 30000:
                await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, Вы успешно заправили грузовик 🚚 {truck_name} за 30.000₽", parse_mode='html')
                cursor.execute(f'UPDATE truck SET fuel = {100} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE users SET balance = {balance - 30000} WHERE user_id = {user_id}')
                connect.commit()
             else:
                await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств!", parse_mode='html')
                return

       if benz <= 60:
          if benz > 50:
             if balance > 40000:
                await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, Вы успешно заправили грузовик 🚚 {truck_name} за 40.000₽", parse_mode='html')
                cursor.execute(f'UPDATE truck SET fuel = {100} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE users SET balance = {balance - 40000} WHERE user_id = {user_id}')
                connect.commit()
             else:
                await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств!", parse_mode='html')
                return

       if benz <= 50:
          if benz > 40:
             if balance > 50000:
                await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, Вы успешно заправили грузовик 🚚 {truck_name} за 50.000₽", parse_mode='html')
                cursor.execute(f'UPDATE truck SET fuel = {100} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE users SET balance = {balance - 50000} WHERE user_id = {user_id}')
                connect.commit()
             else:
                await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств!", parse_mode='html')
                return

       if benz <= 40:
          if benz > 30:
             if balance > 60000:
                await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, Вы успешно заправили грузовик 🚚 {truck_name} за 60.000₽", parse_mode='html')
                cursor.execute(f'UPDATE truck SET fuel = {100} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE users SET balance = {balance - 60000} WHERE user_id = {user_id}')
                connect.commit()
             else:
                await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств!", parse_mode='html')
                return

       if benz <= 30:
          if benz > 20:
             if balance > 70000:
                await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, Вы успешно заправили грузовик 🚚 {truck_name} за 70.000₽", parse_mode='html')
                cursor.execute(f'UPDATE truck SET fuel = {100} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE users SET balance = {balance - 70000} WHERE user_id = {user_id}')
                connect.commit()
             else:
                await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств!", parse_mode='html')
                return

       if benz <= 20:
          if benz > 10:
             if balance > 80000:
                await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, Вы успешно заправили грузовик 🚚 {truck_name} за 80.000₽", parse_mode='html')
                cursor.execute(f'UPDATE truck SET fuel = {100} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE users SET balance = {balance - 80000} WHERE user_id = {user_id}')
                connect.commit()
             else:
                await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств!", parse_mode='html')
                return

       if benz <= 10:
             if balance > 90000:
                await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, Вы успешно заправили грузовик 🚚 {truck_name} за 90.000₽", parse_mode='html')
                cursor.execute(f'UPDATE truck SET fuel = {100} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE users SET balance = {balance - 90000} WHERE user_id = {user_id}')
                connect.commit()
             else:
                await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств!", parse_mode='html')
                

#######Починка
    if message.text.startswith('Грузовик починить') or message.text.startswith('Грузовик починить'):
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       balance = cursor.execute("SELECT balance from users where user_Id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])

       hp = cursor.execute("SELECT hp from truck where user_Id = ?", (message.from_user.id,)).fetchone()
       hp = int(hp[0])

       truck = cursor.execute("SELECT truck from truck where user_Id = ?", (message.from_user.id,)).fetchone()
       truck = int(truck[0])


       if truck == 1:
          truck_name = 'Daf'
          truck_summ = 10000000
          truck_summ2 = '{:,}'.format(truck_summ)
       if truck == 2:
          truck_name = 'Scania'
          truck_summ = 50000000
          truck_summ2 = '{:,}'.format(truck_summ)
       if truck == 3:
          truck_name = 'Nissan'
          truck_summ = 100000000
          truck_summ2 = '{:,}'.format(truck_summ)
       if truck == 4:
          truck_name = 'Renault'
          truck_summ = 500000000
          truck_summ2 = '{:,}'.format(truck_summ)
       if truck == 5:
          truck_name = 'Volvo'
          truck_summ = 750000000
          truck_summ2 = '{:,}'.format(truck_summ)
       if truck == 6:
          truck_name = 'Man'
          truck_summ = 1000000000
          truck_summ2 = '{:,}'.format(truck_summ)
       if truck == 7:
          truck_name = 'Mercedes Benz'
          truck_summ = 1500000000
          truck_summ2 = '{:,}'.format(truck_summ)



       
       if hp in range(76,100):
          hp2 = 'Хорошое 🟩'

       if hp in range(51,75):
          hp2 = 'Среднее 🟧 '
         
       if hp in range(26,50):
          hp2 = 'Плохое 🟥'

       if hp in range(2,25):
          hp2 = 'Ужасное 🛑'

       if hp < 2:
          hp2 = 'Требуется ремонт ⛔️'

       else:
          if hp == 100:
             hp2 = 'Хорошое 🟩'
          if hp == 76:
             hp2 = 'Хорошо '
          if hp == 65:
             hp2 = 'Среднее 🟧'
          if hp == 51:
             hp2 = 'Средне '
          if hp == 43:
             hp2 = 'Плохое 🟥'
          if hp == 36:
             hp2 = 'Плохо '
          if hp == 25:
             hp2 = 'Ужасное 🛑'
          if hp == 12:
             hp2 = 'Ужасно '

       if hp <= 80:
          if hp > 70:
             if balance > 20000:
                await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, Вы успешно починили грузовик 🚚 {truck_name} за 20.000¢", parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - 20000} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE truck SET hp = {100} WHERE user_id = {user_id}')
                connect.commit()
             else:
                await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств!", parse_mode='html')
       else:
          await bot.send_message(message.chat.id, f" 🆘 | Игрок: <a href='tg://user?id={user_id}'>{user_name}</a>, ваш грузовик еше несломалась", parse_mode='html')
          

       if hp <= 70:
          if hp > 60:
             if balance > 30000:
                await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, Вы успешно починили грузовик 🚚 {truck_name} за 30.000¢", parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - 30000} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE truck SET hp = {100} WHERE user_id = {user_id}')
                connect.commit()
             else:
                await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств!", parse_mode='html')
             

       if hp <= 60:
          if hp > 50:
             if balance > 40000:
                await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, Вы успешно починили грузовик 🚚 {truck_name} за 40.000¢", parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - 40000} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE truck SET hp = {100} WHERE user_id = {user_id}')
                connect.commit()
             else:
                await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств!", parse_mode='html')


       if hp <= 50:
          if hp > 40:
             if balance > 50000:
                await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, Вы успешно починили грузовик 🚚 {truck_name} за 20.000¢", parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - 20000} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE truck SET hp = {100} WHERE user_id = {user_id}')
                connect.commit()
             else:
                await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств!", parse_mode='html')
             

       if hp <= 40:
          if hp > 30:
             if balance > 60000:
                await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, Вы успешно починили грузовик 🚚 {truck_name} за 60.000¢", parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - 60000} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE truck SET hp = {100} WHERE user_id = {user_id}')
                connect.commit()
             else:
                await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств!", parse_mode='html')
             

       if hp <= 30:
          if hp >20:
             if balance > 70000:
                await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, Вы успешно починили грузовик 🚚 {truck_name} за 70.000¢", parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - 70000} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE truck SET hp = {100} WHERE user_id = {user_id}')
                connect.commit()
             else:
                await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств!", parse_mode='html')
             

       if hp <= 20:
          if hp > 10:
             if balance > 80000:
                await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, Вы успешно починили грузовик 🚚 {truck_name} за 80.000¢", parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - 80000} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE truck SET hp = {100} WHERE user_id = {user_id}')
                connect.commit()
             else:
                await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств!", parse_mode='html')
             

       if hp <= 10:
             if balance > 90000:
                await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, Вы успешно починили грузовик 🚚 {truck_name} за 90.000¢", parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - 90000} WHERE user_id = {user_id}')
                cursor.execute(f'UPDATE truck SET hp = {100} WHERE user_id = {user_id}')
                connect.commit()
             else:
                await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств!", parse_mode='html')


###########################################ЭЛЕКТРОСТАНЦИИ###########################################
    if message.text.lower() in ["электростанции", "Электростанции"]:
       user_id = message.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       chat_id = message.chat.id
       await bot.send_message(message.chat.id, f"""<a href='tg://user?id={user_id}'>{user_name}</a>, доступные для покупки электростанции:

🎡 1. Grand Coulee |  1🔹/час (20.000.000¢)
🎡 2. Xiluodu |  5🔹/час (600.000.000¢)
🎡 3. Three Gorges Dam | 25🔹/час (6.500.000.000¢)
🎡 4. Xiangjiaba | 450🔹/час (800.000.000.000¢)
🎡 5. Itaipu Dam | 3.000🔹/час (7.500.000.000.000¢)

🛒 <b>Для покупки электростанции введите</b> - <code>Купить электростанцию</code> [номер]
🛒 <b>Для покупки турбин для электростанции введите</b> - <code>Купить турбины</code> [кол-во]""", parse_mode='html')
    
    if message.text.lower() in ["купить электростанцию 1", "Купить электростанцию 1"]: 
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       farm1 = cursor.execute("SELECT farm1 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farm1 = int(farm1[0])
       farm2 = cursor.execute("SELECT farm2 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farm2 = int(farm2[0])
       farm3 = cursor.execute("SELECT farm3 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farm3 = int(farm3[0])
       farm4 = cursor.execute("SELECT farm4 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farm4 = int(farm4[0])
       farm5 = cursor.execute("SELECT farm5 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farm5 = int(farm5[0])
       msg = message
       chat_id = message.chat.id
       loser = ['😔', '😕', '😣', '😞', '😢']
       rloser = random.choice(loser)
       user_id = msg.from_user.id
       balance = cursor.execute("SELECT balance from users where user_id = ?",(message.from_user.id,)).fetchone()
       balance = round(int(balance[0]))
       summ = 20000000
       c = 1
       farms = farm1 + farm2 + farm3 + farm4 + farm5
       checking = cursor.execute("SELECT checking from users where user_id = ?", (message.from_user.id,)).fetchone()
       checking = round(int(checking[0]))
       if checking == 1:
          await bot.send_message(chat_id, f'ℹ | Дождитесь окончания игры! {rloser}', parse_mode='html')
          return
       checking1 = cursor.execute("SELECT checking1 from users where user_id = ?", (message.from_user.id,)).fetchone()
       checking1 = round(int(checking1[0]))
       if checking1 == 1:
          await bot.send_message(chat_id, f'ℹ | Дождитесь окончания игры! {rloser}', parse_mode='html')
          return
       checking2 = cursor.execute("SELECT checking2 from users where user_id = ?", (message.from_user.id,)).fetchone()
       checking2 = round(int(checking2[0]))
       if checking2 == 1:
          await bot.send_message(chat_id, f'ℹ | Дождитесь окончания игры! {rloser}', parse_mode='html')
          return
       checking3 = cursor.execute("SELECT checking3 from users where user_id = ?", (message.from_user.id,)).fetchone()
       checking3 = round(int(checking3[0]))
       if checking3 == 1:
          await bot.send_message(chat_id, f'ℹ | Дождитесь окончания игры! {rloser}', parse_mode='html')
          return
       if farms == 0:
          if farm1 == 0:
             if int(balance) >= int(summ):
                await bot.send_message(message.chat.id, f"🎡 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно купили Grand Coulee за 20.000.000¢ 🎉", parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = "{user_id}"') 
                cursor.execute(f'UPDATE users SET farm1 = {1} WHERE user_id = "{user_id}"') 
                connect.commit()    
                return
             else:
                await bot.send_message(message.chat.id, f"💰 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств! {rloser}", parse_mode='html')     
                return
          if farm1 == 1:
             await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас уже есть данная электростанция! {rloser}", parse_mode='html')     
             return
       if farms == 1:
          await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас уже есть электростанция! {rloser}", parse_mode='html')  

    if message.text.lower() in ["купить электростанцию 2", "Купить электростанцию 2"]: 
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       farm1 = cursor.execute("SELECT farm1 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farm1 = int(farm1[0])
       farm2 = cursor.execute("SELECT farm2 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farm2 = int(farm2[0])
       farm3 = cursor.execute("SELECT farm3 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farm3 = int(farm3[0])
       farm4 = cursor.execute("SELECT farm4 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farm4 = int(farm4[0])
       farm5 = cursor.execute("SELECT farm5 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farm5 = int(farm5[0])
       msg = message
       chat_id = message.chat.id
       loser = ['😔', '😕', '😣', '😞', '😢']
       rloser = random.choice(loser)
       user_id = msg.from_user.id
       balance = cursor.execute("SELECT balance from users where user_id = ?",(message.from_user.id,)).fetchone()
       balance = round(int(balance[0]))
       summ = 600000000
       c = 1
       farms = farm1 + farm2 + farm3 + farm4 + farm5
       checking = cursor.execute("SELECT checking from users where user_id = ?", (message.from_user.id,)).fetchone()
       checking = round(int(checking[0]))
       if checking == 1:
          await bot.send_message(chat_id, f'ℹ | Дождитесь окончания игры! {rloser}', parse_mode='html')
          return
       checking1 = cursor.execute("SELECT checking1 from users where user_id = ?", (message.from_user.id,)).fetchone()
       checking1 = round(int(checking1[0]))
       if checking1 == 1:
          await bot.send_message(chat_id, f'ℹ | Дождитесь окончания игры! {rloser}', parse_mode='html')
          return
       checking2 = cursor.execute("SELECT checking2 from users where user_id = ?", (message.from_user.id,)).fetchone()
       checking2 = round(int(checking2[0]))
       if checking2 == 1:
          await bot.send_message(chat_id, f'ℹ | Дождитесь окончания игры! {rloser}', parse_mode='html')
          return
       checking3 = cursor.execute("SELECT checking3 from users where user_id = ?", (message.from_user.id,)).fetchone()
       checking3 = round(int(checking3[0]))
       if checking3 == 1:
          await bot.send_message(chat_id, f'ℹ | Дождитесь окончания игры! {rloser}', parse_mode='html')
          return
       if farms == 0:
          if farm2 == 0:
             if int(balance) >= int(summ):
                await bot.send_message(message.chat.id, f"🎡 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно купили Xiluodu за 600.000.000¢ 🎉", parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = "{user_id}"') 
                cursor.execute(f'UPDATE users SET farm2 = {1} WHERE user_id = "{user_id}"') 
                connect.commit()    
                return
             else:
                await bot.send_message(message.chat.id, f"💰 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств! {rloser}", parse_mode='html')     
                return
          if farm2 == 1:
             await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас уже есть данная электростанция! {rloser}", parse_mode='html')     
             return
       if farms == 1:
          await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас уже есть электростанция! {rloser}", parse_mode='html') 

    if message.text.lower() in ["купить электростанцию 3", "Купить электростанцию 3"]: 
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       farm1 = cursor.execute("SELECT farm1 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farm1 = int(farm1[0])
       farm2 = cursor.execute("SELECT farm2 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farm2 = int(farm2[0])
       farm3 = cursor.execute("SELECT farm3 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farm3 = int(farm3[0])
       farm4 = cursor.execute("SELECT farm4 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farm4 = int(farm4[0])
       farm5 = cursor.execute("SELECT farm5 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farm5 = int(farm5[0])
       msg = message
       chat_id = message.chat.id
       loser = ['😔', '😕', '😣', '😞', '😢']
       rloser = random.choice(loser)
       user_id = msg.from_user.id
       balance = cursor.execute("SELECT balance from users where user_id = ?",(message.from_user.id,)).fetchone()
       balance = round(int(balance[0]))
       summ = 6500000000
       c = 1
       farms = farm1 + farm2 + farm3 + farm4 + farm5
       checking = cursor.execute("SELECT checking from users where user_id = ?", (message.from_user.id,)).fetchone()
       checking = round(int(checking[0]))
       if checking == 1:
          await bot.send_message(chat_id, f'ℹ | Дождитесь окончания игры! {rloser}', parse_mode='html')
          return
       checking1 = cursor.execute("SELECT checking1 from users where user_id = ?", (message.from_user.id,)).fetchone()
       checking1 = round(int(checking1[0]))
       if checking1 == 1:
          await bot.send_message(chat_id, f'ℹ | Дождитесь окончания игры! {rloser}', parse_mode='html')
          return
       checking2 = cursor.execute("SELECT checking2 from users where user_id = ?", (message.from_user.id,)).fetchone()
       checking2 = round(int(checking2[0]))
       if checking2 == 1:
          await bot.send_message(chat_id, f'ℹ | Дождитесь окончания игры! {rloser}', parse_mode='html')
          return
       checking3 = cursor.execute("SELECT checking3 from users where user_id = ?", (message.from_user.id,)).fetchone()
       checking3 = round(int(checking3[0]))
       if checking3 == 1:
          await bot.send_message(chat_id, f'ℹ | Дождитесь окончания игры! {rloser}', parse_mode='html')
          return
       if farms == 0:
          if farm3 == 0:
             if int(balance) >= int(summ):
                await bot.send_message(message.chat.id, f"🎡 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно купили Three Gorges Dam за 6.500.000.000¢ 🎉", parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = "{user_id}"') 
                cursor.execute(f'UPDATE users SET farm3 = {1} WHERE user_id = "{user_id}"') 
                connect.commit()    
                return
             else:
                await bot.send_message(message.chat.id, f"💰 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств! {rloser}", parse_mode='html')     
                return
          if farm3 == 1:
             await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас уже есть данная электростанция! {rloser}", parse_mode='html')     
             return
       if farms == 1:
          await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас уже есть электростанция! {rloser}", parse_mode='html')  

    if message.text.lower() in ["купить электростанцию 4", "Купить электростанцию 4"]: 
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       farm1 = cursor.execute("SELECT farm1 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farm1 = int(farm1[0])
       farm2 = cursor.execute("SELECT farm2 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farm2 = int(farm2[0])
       farm3 = cursor.execute("SELECT farm3 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farm3 = int(farm3[0])
       farm4 = cursor.execute("SELECT farm4 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farm4 = int(farm4[0])
       farm5 = cursor.execute("SELECT farm5 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farm5 = int(farm5[0])
       msg = message
       chat_id = message.chat.id
       loser = ['😔', '😕', '😣', '😞', '😢']
       rloser = random.choice(loser)
       user_id = msg.from_user.id
       balance = cursor.execute("SELECT balance from users where user_id = ?",(message.from_user.id,)).fetchone()
       balance = round(int(balance[0]))
       summ = 800000000000
       c = 1
       farms = farm1 + farm2 + farm3 + farm4 + farm5
       checking = cursor.execute("SELECT checking from users where user_id = ?", (message.from_user.id,)).fetchone()
       checking = round(int(checking[0]))
       if checking == 1:
          await bot.send_message(chat_id, f'ℹ | Дождитесь окончания игры! {rloser}', parse_mode='html')
          return
       checking1 = cursor.execute("SELECT checking1 from users where user_id = ?", (message.from_user.id,)).fetchone()
       checking1 = round(int(checking1[0]))
       if checking1 == 1:
          await bot.send_message(chat_id, f'ℹ | Дождитесь окончания игры! {rloser}', parse_mode='html')
          return
       checking2 = cursor.execute("SELECT checking2 from users where user_id = ?", (message.from_user.id,)).fetchone()
       checking2 = round(int(checking2[0]))
       if checking2 == 1:
          await bot.send_message(chat_id, f'ℹ | Дождитесь окончания игры! {rloser}', parse_mode='html')
          return
       checking3 = cursor.execute("SELECT checking3 from users where user_id = ?", (message.from_user.id,)).fetchone()
       checking3 = round(int(checking3[0]))
       if checking3 == 1:
          await bot.send_message(chat_id, f'ℹ | Дождитесь окончания игры! {rloser}', parse_mode='html')
          return
       if farms == 0:
          if farm4 == 0:
             if int(balance) >= int(summ):
                await bot.send_message(message.chat.id, f"🎡 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно купили Xiangjiaba Dam за 800.000.000.000¢ 🎉", parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = "{user_id}"') 
                cursor.execute(f'UPDATE users SET farm4 = {1} WHERE user_id = "{user_id}"') 
                connect.commit()    
                return
             else:
                await bot.send_message(message.chat.id, f"💰 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств! {rloser}", parse_mode='html')     
                return
          if farm4 == 1:
             await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас уже есть данная электростанция! {rloser}", parse_mode='html')     
             return
       if farms == 1:
          await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас уже есть электростанция! {rloser}", parse_mode='html')    

    if message.text.lower() in ["купить электростанцию 5", "Купить электростанцию 5"]: 
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       farm1 = cursor.execute("SELECT farm1 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farm1 = int(farm1[0])
       farm2 = cursor.execute("SELECT farm2 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farm2 = int(farm2[0])
       farm3 = cursor.execute("SELECT farm3 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farm3 = int(farm3[0])
       farm4 = cursor.execute("SELECT farm4 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farm4 = int(farm4[0])
       farm5 = cursor.execute("SELECT farm5 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farm5 = int(farm5[0])
       msg = message
       chat_id = message.chat.id
       loser = ['😔', '😕', '😣', '😞', '😢']
       rloser = random.choice(loser)
       user_id = msg.from_user.id
       balance = cursor.execute("SELECT balance from users where user_id = ?",(message.from_user.id,)).fetchone()
       balance = round(int(balance[0]))
       summ = 7500000000000
       c = 1
       farms = farm1 + farm2 + farm3 + farm4 + farm5
       checking = cursor.execute("SELECT checking from users where user_id = ?", (message.from_user.id,)).fetchone()
       checking = round(int(checking[0]))
       if checking == 1:
          await bot.send_message(chat_id, f'ℹ | Дождитесь окончания игры! {rloser}', parse_mode='html')
          return
       checking1 = cursor.execute("SELECT checking1 from users where user_id = ?", (message.from_user.id,)).fetchone()
       checking1 = round(int(checking1[0]))
       if checking1 == 1:
          await bot.send_message(chat_id, f'ℹ | Дождитесь окончания игры! {rloser}', parse_mode='html')
          return
       checking2 = cursor.execute("SELECT checking2 from users where user_id = ?", (message.from_user.id,)).fetchone()
       checking2 = round(int(checking2[0]))
       if checking2 == 1:
          await bot.send_message(chat_id, f'ℹ | Дождитесь окончания игры! {rloser}', parse_mode='html')
          return
       checking3 = cursor.execute("SELECT checking3 from users where user_id = ?", (message.from_user.id,)).fetchone()
       checking3 = round(int(checking3[0]))
       if checking3 == 1:
          await bot.send_message(chat_id, f'ℹ | Дождитесь окончания игры! {rloser}', parse_mode='html')
          return
       if farms == 0:
          if farm5 == 0:
             if int(balance) >= int(summ):
                await bot.send_message(message.chat.id, f"🎡 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно купили Itaipu Dam за 7.500.000.000.000¢ 🎉", parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = "{user_id}"') 
                cursor.execute(f'UPDATE users SET farm5 = {1} WHERE user_id = "{user_id}"') 
                connect.commit()    
                return
             else:
                await bot.send_message(message.chat.id, f"💰 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств! {rloser}", parse_mode='html')     
                return
          if farm5 == 1:
             await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас уже есть данная электростанция! {rloser}", parse_mode='html')     
             return
       if farms == 1:
          await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас уже есть электростанция! {rloser}", parse_mode='html')    

    if message.text.lower() in ["продать электростанцию", "Продать электростанцию"]: 
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       farm1 = cursor.execute("SELECT farm1 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farm1 = int(farm1[0])
       farm2 = cursor.execute("SELECT farm2 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farm2 = int(farm2[0])
       farm3 = cursor.execute("SELECT farm3 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farm3 = int(farm3[0])
       farm4 = cursor.execute("SELECT farm4 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farm4 = int(farm4[0])
       farm5 = cursor.execute("SELECT farm5 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farm5 = int(farm5[0])
       chat_id = message.chat.id
       msg = message
       loser = ['😔', '😕', '😣', '😞', '😢']
       rloser = random.choice(loser)
       user_id = msg.from_user.id
       balance = cursor.execute("SELECT balance from users where user_id = ?",(message.from_user.id,)).fetchone()
       balance = round(int(balance[0]))
       farms = farm1 + farm2 + farm3 + farm4 + farm5 
       if farms == 0:
          await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас нету электростанции! {rloser}", parse_mode='html')
       if farm1 == 1:
          await bot.send_message(message.chat.id, f"💰 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно продали свою электростанцию за 15.000.000¢", parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance + 15000000} WHERE user_id = "{user_id}"') 
          cursor.execute(f'UPDATE users SET farm1 = {0} WHERE user_id = "{user_id}"')  
          cursor.execute(f'UPDATE users SET generator = {0} WHERE user_id = "{user_id}"') 
          connect.commit() 
       if farm2 == 1:
          await bot.send_message(message.chat.id, f"💰 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно продали свою электростанцию за 450.000.000¢", parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance + 450000000} WHERE user_id = "{user_id}"') 
          cursor.execute(f'UPDATE users SET farm2 = {0} WHERE user_id = "{user_id}"') 
          cursor.execute(f'UPDATE users SET generator = {0} WHERE user_id = "{user_id}"') 
          connect.commit() 
       if farm3 == 1:
          await bot.send_message(message.chat.id, f"💰 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно продали свою электростанцию за 4.875.000.000¢", parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance + 4875000000} WHERE user_id = "{user_id}"') 
          cursor.execute(f'UPDATE users SET farm3 = {0} WHERE user_id = "{user_id}"') 
          cursor.execute(f'UPDATE users SET generator = {0} WHERE user_id = "{user_id}"') 
          connect.commit() 
       if farm4 == 1:
          await bot.send_message(message.chat.id, f"💰 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно продали свою электростанцию за 600.000.000.000¢", parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance + 600000000000} WHERE user_id = "{user_id}"') 
          cursor.execute(f'UPDATE users SET farm4 = {0} WHERE user_id = "{user_id}"') 
          cursor.execute(f'UPDATE users SET generator = {0} WHERE user_id = "{user_id}"') 
          connect.commit() 
       if farm5 == 1:
          await bot.send_message(message.chat.id, f"💰 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно продали свою электростанцию за 5.625.000.000.000¢", parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance + 5625000000000} WHERE user_id = "{user_id}"') 
          cursor.execute(f'UPDATE users SET farm5 = {0} WHERE user_id = "{user_id}"') 
          cursor.execute(f'UPDATE users SET generator = {0} WHERE user_id = "{user_id}"') 
          connect.commit() 

    if message.text.lower() in ["моя электростанция", "Моя электростанция"]: 
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       farm1 = cursor.execute("SELECT farm1 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farm1 = int(farm1[0])
       farm2 = cursor.execute("SELECT farm2 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farm2 = int(farm2[0])
       farm3 = cursor.execute("SELECT farm3 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farm3 = int(farm3[0])
       farm4 = cursor.execute("SELECT farm4 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farm4 = int(farm4[0])
       farm5 = cursor.execute("SELECT farm5 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farm5 = int(farm5[0])
       generator = cursor.execute("SELECT generator from users where user_id = ?",(message.from_user.id,)).fetchone()
       generator = int(generator[0])
       farm_coin = cursor.execute("SELECT farm_coin from users where user_id = ?",(message.from_user.id,)).fetchone()
       farm_coin = int(farm_coin[0])
       farm_coin_get = '{0:,}'.format(farm_coin).replace(',', '.')
       generator1 = '{0:,}'.format(generator * 1).replace(',', '.')
       generator2 = '{0:,}'.format(generator * 5).replace(',', '.')
       generator3 = '{0:,}'.format(generator * 25).replace(',', '.')
       generator4 = '{0:,}'.format(generator * 450).replace(',', '.')
       generator5 = '{0:,}'.format(generator * 3000).replace(',', '.')
       chat_id = message.chat.id
       msg = message
       loser = ['😔', '😕', '😣', '😞', '😢']
       rloser = random.choice(loser)
       user_id = msg.from_user.id
       balance = cursor.execute("SELECT balance from users where user_id = ?",(message.from_user.id,)).fetchone()
       balance = round(int(balance[0]))
       farms = farm1 + farm2 + farm3 + farm4 + farm5 
       if farms == 0:
          await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас нету электростанции! {rloser}", parse_mode='html')
       if farm1 == 1:
          await bot.send_message(message.chat.id, f"""
🎡 Электростанция: Grand Coulee
👤 Владелец: <a href='tg://user?id={user_id}'>{user_name}</a>
💼 Турбин: {generator}/15
💸 Прибыль: {generator1}🔹
💰 На балансе: {farm_coin_get}🔹

ℹ️Что бы снять с баланса электростанции введите команду ниже ⬇️
ℹ️Электростанция снять [Сумма]""", 
parse_mode='html')
       if farm2 == 1:
          await bot.send_message(message.chat.id, f"""
🎡 Электростанция: Xiluodu
👤 Владелец: <a href='tg://user?id={user_id}'>{user_name}</a>
💼 Турбин: {generator}/15
💸 Прибыль: {generator2}🔹
💰 На балансе: {farm_coin_get}🔹

ℹ️Что бы снять с баланса электростанции введите команду ниже ⬇️
ℹ️Электростанция снять [Сумма]""", 
parse_mode='html')
       if farm3 == 1:
          await bot.send_message(message.chat.id, f"""
🎡 Электростанция: Three Gorges Dam
👤 Владелец: <a href='tg://user?id={user_id}'>{user_name}</a>
💼 Турбин: {generator}/15
💸 Прибыль: {generator3}🔹
💰 На балансе: {farm_coin_get}🔹

ℹ️Что бы снять с баланса электростанции введите команду ниже ⬇️
ℹ️Электростанция снять [Сумма]""", 
parse_mode='html')
       if farm4 == 1:
          await bot.send_message(message.chat.id, f"""
🎡 Электростанция: Xiangjiaba
👤 Владелец: <a href='tg://user?id={user_id}'>{user_name}</a>
💼 Турбин: {generator}/15
💸 Прибыль: {generator4}🔹
💰 На балансе: {farm_coin_get}🔹

ℹ️Что бы снять с баланса электростанции введите команду ниже ⬇️
ℹ️Электростанция снять [Сумма]""", 
parse_mode='html')
       if farm5 == 1:
          await bot.send_message(message.chat.id, f"""
🎡 Электростанция: Itaipu Dam
👤 Владелец: <a href='tg://user?id={user_id}'>{user_name}</a>
💼 Турбин: {generator}/15
💸 Прибыль: {generator5}🔹
💰 На балансе: {farm_coin_get}🔹

ℹ️Что бы снять с баланса электростанции введите команду ниже ⬇️
ℹ️Электростанция снять [Сумма]""", 
parse_mode='html')

    if message.text.startswith("Купить турбины") or message.text.startswith("купить турбины"):
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       farm1 = cursor.execute("SELECT farm1 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farm1 = int(farm1[0])
       farm2 = cursor.execute("SELECT farm2 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farm2 = int(farm2[0])
       farm3 = cursor.execute("SELECT farm3 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farm3 = int(farm3[0])
       farm4 = cursor.execute("SELECT farm4 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farm4 = int(farm4[0])
       farm5 = cursor.execute("SELECT farm5 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farm5 = int(farm5[0])
       generator = cursor.execute("SELECT generator from users where user_id = ?",(message.from_user.id,)).fetchone()
       generator = int(generator[0])
       chat_id = message.chat.id
       msg = message
       loser = ['😔', '😕', '😣', '😞', '😢']
       rloser = random.choice(loser)
       user_id = msg.from_user.id

       balance = cursor.execute("SELECT balance from users where user_id = ?",(message.from_user.id,)).fetchone()
       balance = round(int(balance[0]))

       farms = farm1 + farm2 + farm3 + farm4 + farm5 
       summ = int(msg.text.split()[2])
       check = generator + summ

       check_balance1 = summ * 20000000
       check_balance2 = summ * 600000000
       check_balance3 = summ * 6500000000
       check_balance4 = summ * 800000000000
       check_balance5 = summ * 7500000000000
       
       check_balance1_up = '{0:,}'.format(check_balance1).replace(',', '.')
       check_balance2_up = '{0:,}'.format(check_balance2).replace(',', '.')
       check_balance3_up = '{0:,}'.format(check_balance3).replace(',', '.')
       check_balance4_up = '{0:,}'.format(check_balance4).replace(',', '.')
       check_balance5_up = '{0:,}'.format(check_balance5).replace(',', '.')

       if summ <= 0:
          await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, вы не можете купить отрицательное число турбин! {rloser}", parse_mode='html')
          return
       if farms == 0:
          await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас нету электростанции! {rloser}", parse_mode='html')
          return
       if check > 15:
          await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, вы не можете купить больше 15 турбин! {rloser}", parse_mode='html')
          return
       if check <= 15:
          if farm1 == 1:
             if check_balance1 <= balance:
                await bot.send_message(message.chat.id, f"🎡 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно купили {summ} турбин за {check_balance1_up}¢ !", parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - check_balance1} WHERE user_id = "{user_id}"') 
                cursor.execute(f'UPDATE users SET generator = {generator + summ} WHERE user_id = "{user_id}"') 
                connect.commit() 
             if check_balance1 > balance:
                await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, не достаточно средств! {rloser}", parse_mode='html')
                return
          if farm2 == 1:
             if check_balance2 <= balance:
                await bot.send_message(message.chat.id, f"🎡 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно купили {summ} турбин за {check_balance2_up}¢ !", parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - check_balance2} WHERE user_id = "{user_id}"') 
                cursor.execute(f'UPDATE users SET generator = {generator + summ} WHERE user_id = "{user_id}"') 
                connect.commit() 
             if check_balance2 > balance:
                await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, не достаточно средств! {rloser}", parse_mode='html')
                return
          if farm3 == 1:
             if check_balance3 <= balance:
                await bot.send_message(message.chat.id, f"🎡 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно купили {summ} турбин за {check_balance3_up}¢ !", parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - check_balance3} WHERE user_id = "{user_id}"') 
                cursor.execute(f'UPDATE users SET generator = {generator + summ} WHERE user_id = "{user_id}"') 
                connect.commit() 
             if check_balance3 > balance:
                await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, не достаточно средств! {rloser}", parse_mode='html')
                return
          if farm4 == 1:
             if check_balance4 <= balance:
                await bot.send_message(message.chat.id, f"🎡 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно купили {summ} турбин за {check_balance4_up}¢ !", parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - check_balance4} WHERE user_id = "{user_id}"') 
                cursor.execute(f'UPDATE users SET generator = {generator + summ} WHERE user_id = "{user_id}"') 
                connect.commit() 
             if check_balance4 > balance:
                await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, не достаточно средств! {rloser}", parse_mode='html')
                return
          if farm5 == 1:
             if check_balance5 <= balance:
                await bot.send_message(message.chat.id, f"🎡 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно купили {summ} турбин за {check_balance5_up}¢ !", parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - check_balance5} WHERE user_id = "{user_id}"') 
                cursor.execute(f'UPDATE users SET generator = {generator + summ} WHERE user_id = "{user_id}"') 
                connect.commit() 
             if check_balance5 > balance:
                await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, не достаточно средств! {rloser}", parse_mode='html')
                return

    if message.text.startswith("Электростанция снять") or message.text.startswith("электростанция снять"):
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       farm1 = cursor.execute("SELECT farm1 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farm1 = int(farm1[0])
       farm2 = cursor.execute("SELECT farm2 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farm2 = int(farm2[0])
       farm3 = cursor.execute("SELECT farm3 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farm3 = int(farm3[0])
       farm4 = cursor.execute("SELECT farm4 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farm4 = int(farm4[0])
       farm5 = cursor.execute("SELECT farm5 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farm5 = int(farm5[0])
       farm_coin = cursor.execute("SELECT farm_coin from users where user_id = ?",(message.from_user.id,)).fetchone()
       farm_coin = int(farm_coin[0])
       litecoin = cursor.execute("SELECT litecoin from users where user_id = ?",(message.from_user.id,)).fetchone()
       litecoin = int(litecoin[0])
       summ = int(msg.text.split()[2])
       summ_get = '{0:,}'.format(summ).replace(',', '.')
       chat_id = message.chat.id
       msg = message
       loser = ['😔', '😕', '😣', '😞', '😢']
       rloser = random.choice(loser)
       user_id = msg.from_user.id
       balance = cursor.execute("SELECT balance from users where user_id = ?",(message.from_user.id,)).fetchone()
       balance = round(int(balance[0]))
       farms = farm1 + farm2 + farm3 + farm4 + farm5 
       if summ <= 0:
          await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, вы не можете снять отрицательное число лайткоина! {rloser}", parse_mode='html') 
          return
       if farms == 0:
          await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас нету электростанции! {rloser}", parse_mode='html')
       if farm1 == 1:
          if summ > farm_coin:
             await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, на счету вашей электростанции недостаточно лайткоина! {rloser}", parse_mode='html') 
          if summ <= farm_coin:
             await bot.send_message(message.chat.id, f"🎡 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно сняли {summ_get}🔹 с вашей электростанции!", parse_mode='html')
             cursor.execute(f'UPDATE users SET farm_coin = {farm_coin - summ} WHERE user_id = "{user_id}"') 
             cursor.execute(f'UPDATE users SET litecoin = {litecoin + summ} WHERE user_id = "{user_id}"') 
             connect.commit() 
       if farm2 == 1:
          if summ > farm_coin:
             await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, на счету вашей электростанции недостаточно лайткоина! {rloser}", parse_mode='html') 
          if summ <= farm_coin:
             await bot.send_message(message.chat.id, f"🎡 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно сняли {summ_get}🔹 с вашей электростанции!", parse_mode='html')
             cursor.execute(f'UPDATE users SET farm_coin = {farm_coin - summ} WHERE user_id = "{user_id}"') 
             cursor.execute(f'UPDATE users SET litecoin = {litecoin + summ} WHERE user_id = "{user_id}"') 
             connect.commit() 
       if farm3 == 1:
          if summ > farm_coin:
             await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, на счету вашей электростанции недостаточно лайткоина! {rloser}", parse_mode='html') 
          if summ <= farm_coin:
             await bot.send_message(message.chat.id, f"🎡 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно сняли {summ_get}🔹 с вашей электростанции!", parse_mode='html')
             cursor.execute(f'UPDATE users SET farm_coin = {farm_coin - summ} WHERE user_id = "{user_id}"') 
             cursor.execute(f'UPDATE users SET litecoin = {litecoin + summ} WHERE user_id = "{user_id}"') 
             connect.commit() 
       if farm4 == 1:
          if summ > farm_coin:
             await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, на счету вашей электростанции недостаточно лайткоина! {rloser}", parse_mode='html') 
          if summ <= farm_coin:
             await bot.send_message(message.chat.id, f"🎡 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно сняли {summ_get}🔹 с вашей электростанции!", parse_mode='html')
             cursor.execute(f'UPDATE users SET farm_coin = {farm_coin - summ} WHERE user_id = "{user_id}"') 
             cursor.execute(f'UPDATE users SET litecoin = {litecoin + summ} WHERE user_id = "{user_id}"') 
             connect.commit() 
       if farm5 == 1:
          if summ > farm_coin:
             await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, на счету вашей электростанции недостаточно лайткоина! {rloser}", parse_mode='html') 
          if summ <= farm_coin:
             await bot.send_message(message.chat.id, f"🎡 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно сняли {summ_get}🔹 с вашей электростанции!", parse_mode='html')
             cursor.execute(f'UPDATE users SET farm_coin = {farm_coin - summ} WHERE user_id = "{user_id}"') 
             cursor.execute(f'UPDATE users SET litecoin = {litecoin + summ} WHERE user_id = "{user_id}"') 
             connect.commit() 


#############################################ФЕРМЫ#################################################
    if message.text.lower() in ["Фермы", "фермы"]:
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       await bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, доступные для покупки майнинг фермы:

🧰 1. TI-Miner 4฿/час (5.000.000¢)
🧰 2. Saturn 12฿/час (60.000.000¢)
🧰 3. Calisto 64฿/час (650.000.000¢)
🧰 4. HashMiner 650฿/час (80.000.000.000¢)
🧰 5. MegaWatt 3.500฿/час (750.000.000.000¢)

💡 <b>Вы не можете иметь фермы от разных производителей.</b>
🛒 <b>Для покупки фермы введите</b> - <code>Купить ферму</code> [номер]
🛒 <b>Для покупки видеокарты для фермы введите</b> - <code>Купить видеокарту</code> [кол-во]""", parse_mode='html')

    if message.text.lower() in ["продать ферму", "Продать ферму"]: 
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       farmcoin1 = cursor.execute("SELECT farmcoin1 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farmcoin1 = int(farmcoin1[0])
       farmcoin2 = cursor.execute("SELECT farmcoin2 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farmcoin2 = int(farmcoin2[0])
       farmcoin3 = cursor.execute("SELECT farmcoin3 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farmcoin3 = int(farmcoin3[0])
       farmcoin4 = cursor.execute("SELECT farmcoin4 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farmcoin4 = int(farmcoin4[0])
       farmcoin5 = cursor.execute("SELECT farmcoin5 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farmcoin5 = int(farmcoin5[0])
       chat_id = message.chat.id
       msg = message
       loser = ['😔', '😕', '😣', '😞', '😢']
       rloser = random.choice(loser)
       user_id = msg.from_user.id
       balance = cursor.execute("SELECT balance from users where user_id = ?",(message.from_user.id,)).fetchone()
       balance = round(int(balance[0]))
       farmscoin = farmcoin1 + farmcoin2 + farmcoin3 + farmcoin4 + farmcoin5 
       if farmscoin == 0:
          await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас нету майнинг-фермы! {rloser}", parse_mode='html')
       if farmcoin1 == 1:
          await bot.send_message(message.chat.id, f"💰 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно продали свою майнинг-ферму за 3.750.000¢", parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance + 3750000} WHERE user_id = "{user_id}"') 
          cursor.execute(f'UPDATE users SET farmcoin1 = {0} WHERE user_id = "{user_id}"')  
          cursor.execute(f'UPDATE users SET vcard = {0} WHERE user_id = "{user_id}"') 
          connect.commit() 
       if farmcoin2 == 1:
          await bot.send_message(message.chat.id, f"💰 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно продали свою майнинг-ферму за 45.000.000¢", parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance + 45000000} WHERE user_id = "{user_id}"') 
          cursor.execute(f'UPDATE users SET farmcoin2 = {0} WHERE user_id = "{user_id}"') 
          cursor.execute(f'UPDATE users SET vcard = {0} WHERE user_id = "{user_id}"') 
          connect.commit() 
       if farmcoin3 == 1:
          await bot.send_message(message.chat.id, f"💰 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно продали свою майнинг-ферму за 487.500.000¢", parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance + 487500000} WHERE user_id = "{user_id}"') 
          cursor.execute(f'UPDATE users SET farmcoin3 = {0} WHERE user_id = "{user_id}"') 
          cursor.execute(f'UPDATE users SET vcard = {0} WHERE user_id = "{user_id}"') 
          connect.commit() 
       if farmcoin4 == 1:
          await bot.send_message(message.chat.id, f"💰 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно продали свою майнинг-ферму за 60.000.000.000¢", parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance + 60000000000} WHERE user_id = "{user_id}"') 
          cursor.execute(f'UPDATE users SET farmcoin4 = {0} WHERE user_id = "{user_id}"') 
          cursor.execute(f'UPDATE users SET vcard = {0} WHERE user_id = "{user_id}"') 
          connect.commit() 
       if farmcoin5 == 1:
          await bot.send_message(message.chat.id, f"💰 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно продали свою майнинг-ферму за 562.500.000.000¢", parse_mode='html')
          cursor.execute(f'UPDATE users SET balance = {balance + 562500000000} WHERE user_id = "{user_id}"') 
          cursor.execute(f'UPDATE users SET farmcoin5 = {0} WHERE user_id = "{user_id}"') 
          cursor.execute(f'UPDATE users SET vcard = {0} WHERE user_id = "{user_id}"') 
          connect.commit() 

    if message.text.lower() in ["Моя ферма", "моя ферма", "ферма", "Ферма"]:
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       ferma = types.InlineKeyboardMarkup(row_width=2)
       pribel = InlineKeyboardButton(text='💰 Собрать прибыль', callback_data='pribel')
       ferma.add(pribel)
       farmcoin1 = cursor.execute("SELECT farmcoin1 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farmcoin1 = int(farmcoin1[0])
       farmcoin2 = cursor.execute("SELECT farmcoin2 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farmcoin2 = int(farmcoin2[0])
       farmcoin3 = cursor.execute("SELECT farmcoin3 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farmcoin3 = int(farmcoin3[0])
       farmcoin4 = cursor.execute("SELECT farmcoin4 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farmcoin4 = int(farmcoin4[0])
       farmcoin5 = cursor.execute("SELECT farmcoin5 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farmcoin5 = int(farmcoin5[0])
       vcard = cursor.execute("SELECT vcard from users where user_id = ?",(message.from_user.id,)).fetchone()
       vcard = int(vcard[0])
       bitmaning = cursor.execute("SELECT bitmaning from users where user_id = ?",(message.from_user.id,)).fetchone()
       bitmaning = int(bitmaning[0])
       profit1 = '{0:,}'.format(vcard * 4).replace(',', '.')
       profit2 = '{0:,}'.format(vcard * 12).replace(',', '.')
       profit3 = '{0:,}'.format(vcard * 64).replace(',', '.')
       profit4 = '{0:,}'.format(vcard * 650).replace(',', '.')
       profit5 = '{0:,}'.format(vcard * 3500).replace(',', '.')
       farmscoin = farmcoin1 + farmcoin2 + farmcoin3 + farmcoin4 + farmcoin5
       bitmaning2 = '{0:,}'.format(bitmaning).replace(',', '.')
       if farmscoin == 0:
          await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас нету майнинг фермы!", parse_mode='html')
       if farmcoin1 == 1:
          await bot.send_message(message.chat.id, f"""
🧰 | <a href='tg://user?id={user_id}'>{user_name}</a>, информация о вашей майнинг-ферме:

ℹ️ Название фермы: TI-Miner
💸 Прибыль: {profit1}฿/чаc
💼 Видеокарт: {vcard}/1000
💰 На счету: {bitmaning2}฿""", reply_markup=ferma, parse_mode='html')
       if farmcoin2 == 1:
          await bot.send_message(message.chat.id, f"""
🧰 | <a href='tg://user?id={user_id}'>{user_name}</a>, информация о вашей майнинг-ферме:

ℹ️ Название фермы: Saturn\n💸 Прибыль: {profit2}฿/чаc
💼 Видеокарт: {vcard}/1000
💰 На счету: {bitmaning2}฿""", reply_markup=ferma, parse_mode='html')
       if farmcoin3 == 1:
          await bot.send_message(message.chat.id, f"""
🧰 | <a href='tg://user?id={user_id}'>{user_name}</a>, информация о вашей майнинг-ферме:
	
ℹ️ Название фермы: Calisto
💸 Прибыль: {profit3}฿/чаc
💼 Видеокарт: {vcard}/1000
💰 На счету: {bitmaning2}฿""", reply_markup=ferma, parse_mode='html')
       if farmcoin4 == 1:
          await bot.send_message(message.chat.id, f"""
🧰 | <a href='tg://user?id={user_id}'>{user_name}</a>, информация о вашей майнинг-ферме:

ℹ️ Название фермы: HashMiner
💸 Прибыль: {profit4}฿/чаc
💼 Видеокарт: {vcard}/1000
💰 На счету: {bitmaning2}฿""", reply_markup=ferma, parse_mode='html')
       if farmcoin5 == 1:
          await bot.send_message(message.chat.id, f"""
🧰 | <a href='tg://user?id={user_id}'>{user_name}</a>, информация о вашей майнинг-ферме:

ℹ️ Название фермы: MegaWatt\n💸 Прибыль: {profit5}฿/чаc
💼 Видеокарт: {vcard}/1000
💰 На счету: {bitmaning2}฿""", reply_markup=ferma, parse_mode='html')

    if message.text.lower() in ["купить ферму 1", "Купить ферму 1"]: 
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       farmcoin1 = cursor.execute("SELECT farmcoin1 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farmcoin1 = int(farmcoin1[0])
       farmcoin2 = cursor.execute("SELECT farmcoin2 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farmcoin2 = int(farmcoin2[0])
       farmcoin3 = cursor.execute("SELECT farmcoin3 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farmcoin3 = int(farmcoin3[0])
       farmcoin4 = cursor.execute("SELECT farmcoin4 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farmcoin4 = int(farmcoin4[0])
       farmcoin5 = cursor.execute("SELECT farmcoin5 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farmcoin5 = int(farmcoin5[0])
       chat_id = message.chat.id
       loser = ['😔', '😕', '😣', '😞', '😢']
       rloser = random.choice(loser)
       user_id = message.from_user.id
       balance = cursor.execute("SELECT balance from users where user_id = ?",(message.from_user.id,)).fetchone()
       balance = round(int(balance[0]))
       summ = 5000000
       c = 1
       farmscoin = farmcoin1 + farmcoin2 + farmcoin3 + farmcoin4 + farmcoin5
       if farmscoin == 0:
          if farmcoin1 == 0:
             if int(balance) >= int(summ):
                await bot.send_message(message.chat.id, f"🧰 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно купили майнинг-ферму \"TI-Miner\" за 5.000.000¢ 🎉", parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = "{user_id}"') 
                cursor.execute(f'UPDATE users SET farmcoin1 = {1} WHERE user_id = "{user_id}"') 
                connect.commit()    
                return
             else:
                await bot.send_message(message.chat.id, f"💰 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств! {rloser}", parse_mode='html')     
                return
          if farmcoin1 == 1:
             await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас уже есть данная майнинг-ферма! {rloser}", parse_mode='html')     
             return
       if farmscoin == 1:
          await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас уже есть майнинг-ферма! {rloser}", parse_mode='html')  

    if message.text.lower() in ["купить ферму 2", "Купить ферму 2"]: 
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       farmcoin1 = cursor.execute("SELECT farmcoin1 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farmcoin1 = int(farmcoin1[0])
       farmcoin2 = cursor.execute("SELECT farmcoin2 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farmcoin2 = int(farmcoin2[0])
       farmcoin3 = cursor.execute("SELECT farmcoin3 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farmcoin3 = int(farmcoin3[0])
       farmcoin4 = cursor.execute("SELECT farmcoin4 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farmcoin4 = int(farmcoin4[0])
       farmcoin5 = cursor.execute("SELECT farmcoin5 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farmcoin5 = int(farmcoin5[0])
       chat_id = message.chat.id
       loser = ['😔', '😕', '😣', '😞', '😢']
       rloser = random.choice(loser)
       user_id = message.from_user.id
       balance = cursor.execute("SELECT balance from users where user_id = ?",(message.from_user.id,)).fetchone()
       balance = round(int(balance[0]))
       summ = 60000000
       c = 1
       farmscoin = farmcoin1 + farmcoin2 + farmcoin3 + farmcoin4 + farmcoin5
       if farmscoin == 0:
          if farmcoin2 == 0:
             if int(balance) >= int(summ):
                await bot.send_message(message.chat.id, f"🧰 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно купили майнинг-ферму \"Saturn\" за 60.000.000¢ 🎉", parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = "{user_id}"') 
                cursor.execute(f'UPDATE users SET farmcoin2 = {1} WHERE user_id = "{user_id}"') 
                connect.commit()    
                return
             else:
                await bot.send_message(message.chat.id, f"💰 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств! {rloser}", parse_mode='html')     
                return
          if farmcoin2 == 1:
             await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас уже есть данная майнинг-ферма! {rloser}", parse_mode='html')     
             return
       if farmscoin == 1:
          await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас уже есть майнинг-ферма! {rloser}", parse_mode='html')  
  
    if message.text.lower() in ["купить ферму 3", "Купить ферму 3"]: 
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       farmcoin1 = cursor.execute("SELECT farmcoin1 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farmcoin1 = int(farmcoin1[0])
       farmcoin2 = cursor.execute("SELECT farmcoin2 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farmcoin2 = int(farmcoin2[0])
       farmcoin3 = cursor.execute("SELECT farmcoin3 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farmcoin3 = int(farmcoin3[0])
       farmcoin4 = cursor.execute("SELECT farmcoin4 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farmcoin4 = int(farmcoin4[0])
       farmcoin5 = cursor.execute("SELECT farmcoin5 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farmcoin5 = int(farmcoin5[0])
       chat_id = message.chat.id
       loser = ['😔', '😕', '😣', '😞', '😢']
       rloser = random.choice(loser)
       user_id = message.from_user.id
       balance = cursor.execute("SELECT balance from users where user_id = ?",(message.from_user.id,)).fetchone()
       balance = round(int(balance[0]))
       summ = 650000000
       c = 1
       farmscoin = farmcoin1 + farmcoin2 + farmcoin3 + farmcoin4 + farmcoin5
       if farmscoin == 0:
          if farmcoin3 == 0:
             if int(balance) >= int(summ):
                await bot.send_message(message.chat.id, f"🧰 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно купили майнинг-ферму \"Calisto\" за 650.000.000¢ 🎉", parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = "{user_id}"') 
                cursor.execute(f'UPDATE users SET farmcoin3 = {1} WHERE user_id = "{user_id}"') 
                connect.commit()    
                return
             else:
                await bot.send_message(message.chat.id, f"💰 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств! {rloser}", parse_mode='html')     
                return
          if farmcoin3 == 1:
             await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас уже есть данная майнинг-ферма! {rloser}", parse_mode='html')     
             return
       if farmscoin == 1:
          await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас уже есть майнинг-ферма! {rloser}", parse_mode='html')  
    
    if message.text.lower() in ["купить ферму 4", "Купить ферму 4"]: 
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       farmcoin1 = cursor.execute("SELECT farmcoin1 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farmcoin1 = int(farmcoin1[0])
       farmcoin2 = cursor.execute("SELECT farmcoin2 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farmcoin2 = int(farmcoin2[0])
       farmcoin3 = cursor.execute("SELECT farmcoin3 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farmcoin3 = int(farmcoin3[0])
       farmcoin4 = cursor.execute("SELECT farmcoin4 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farmcoin4 = int(farmcoin4[0])
       farmcoin5 = cursor.execute("SELECT farmcoin5 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farmcoin5 = int(farmcoin5[0])
       chat_id = message.chat.id
       loser = ['😔', '😕', '😣', '😞', '😢']
       rloser = random.choice(loser)
       user_id = message.from_user.id
       balance = cursor.execute("SELECT balance from users where user_id = ?",(message.from_user.id,)).fetchone()
       balance = round(int(balance[0]))
       summ = 80000000000
       c = 1
       farmscoin = farmcoin1 + farmcoin2 + farmcoin3 + farmcoin4 + farmcoin5
       if farmscoin == 0:
          if farmcoin4 == 0:
             if int(balance) >= int(summ):
                await bot.send_message(message.chat.id, f"🧰 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно купили майнинг-ферму \"HashMiner\" за 80.000.000.000¢ 🎉", parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = "{user_id}"') 
                cursor.execute(f'UPDATE users SET farmcoin4 = {1} WHERE user_id = "{user_id}"') 
                connect.commit()    
                return
             else:
                await bot.send_message(message.chat.id, f"💰 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств! {rloser}", parse_mode='html')     
                return
          if farmcoin4 == 1:
             await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас уже есть данная майнинг-ферма! {rloser}", parse_mode='html')     
             return
       if farmscoin == 1:
          await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас уже есть майнинг-ферма! {rloser}", parse_mode='html')  

    if message.text.lower() in ["купить ферму 5", "Купить ферму 5"]: 
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       farmcoin1 = cursor.execute("SELECT farmcoin1 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farmcoin1 = int(farmcoin1[0])
       farmcoin2 = cursor.execute("SELECT farmcoin2 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farmcoin2 = int(farmcoin2[0])
       farmcoin3 = cursor.execute("SELECT farmcoin3 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farmcoin3 = int(farmcoin3[0])
       farmcoin4 = cursor.execute("SELECT farmcoin4 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farmcoin4 = int(farmcoin4[0])
       farmcoin5 = cursor.execute("SELECT farmcoin5 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farmcoin5 = int(farmcoin5[0])
       chat_id = message.chat.id
       loser = ['😔', '😕', '😣', '😞', '😢']
       rloser = random.choice(loser)
       user_id = message.from_user.id
       balance = cursor.execute("SELECT balance from users where user_id = ?",(message.from_user.id,)).fetchone()
       balance = round(int(balance[0]))
       summ = 750000000000
       c = 1
       farmscoin = farmcoin1 + farmcoin2 + farmcoin3 + farmcoin4 + farmcoin5
       if farmscoin == 0:
          if farmcoin5 == 0:
             if int(balance) >= int(summ):
                await bot.send_message(message.chat.id, f"🧰 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно купили майнинг-ферму \"MegaWatt\" за 750.000.000.000¢ 🎉", parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - summ} WHERE user_id = "{user_id}"') 
                cursor.execute(f'UPDATE users SET farmcoin5 = {1} WHERE user_id = "{user_id}"') 
                connect.commit()    
                return
             else:
                await bot.send_message(message.chat.id, f"💰 | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно средств! {rloser}", parse_mode='html')     
                return
          if farmcoin5 == 1:
             await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас уже есть данная майнинг-ферма! {rloser}", parse_mode='html')     
             return
       if farmscoin == 1:
          await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас уже есть майнинг-ферма! {rloser}", parse_mode='html')  

    if message.text.startswith("купить видеокарту") or message.text.startswith("Купить видеокарту"):
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       farmcoin1 = cursor.execute("SELECT farmcoin1 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farmcoin1 = int(farmcoin1[0])
       farmcoin2 = cursor.execute("SELECT farmcoin2 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farmcoin2 = int(farmcoin2[0])
       farmcoin3 = cursor.execute("SELECT farmcoin3 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farmcoin3 = int(farmcoin3[0])
       farmcoin4 = cursor.execute("SELECT farmcoin4 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farmcoin4 = int(farmcoin4[0])
       farmcoin5 = cursor.execute("SELECT farmcoin5 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farmcoin5 = int(farmcoin5[0])
       vcard = cursor.execute("SELECT vcard from users where user_id = ?",(message.from_user.id,)).fetchone()
       vcard = int(vcard[0])
       farmscoin = farmcoin1 + farmcoin2 + farmcoin3 + farmcoin4 + farmcoin5
       chat_id = message.chat.id
       msg = message
       loser = ['😔', '😕', '😣', '😞', '😢']
       rloser = random.choice(loser)
       user_id = msg.from_user.id

       balance = cursor.execute("SELECT balance from users where user_id = ?",(message.from_user.id,)).fetchone()
       balance = round(int(balance[0]))

       summ = int(msg.text.split()[2])
       check = vcard + summ

       check_balance1 = summ * 5000000
       check_balance2 = summ * 60000000
       check_balance3 = summ * 650000000
       check_balance4 = summ * 80000000000
       check_balance5 = summ * 750000000000
       
       check_balance1_up = '{0:,}'.format(check_balance1).replace(',', '.')
       check_balance2_up = '{0:,}'.format(check_balance2).replace(',', '.')
       check_balance3_up = '{0:,}'.format(check_balance3).replace(',', '.')
       check_balance4_up = '{0:,}'.format(check_balance4).replace(',', '.')
       check_balance5_up = '{0:,}'.format(check_balance5).replace(',', '.')

       if summ <= 0:
          await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, вы не можете купить отрицательное число видеокарт! {rloser}", parse_mode='html')
          return
       if farmscoin == 0:
          await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас нету майнинг-фермы! {rloser}", parse_mode='html')
          return
       if check > 1000:
          await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, вы не можете купить больше 1000 видеокарт! {rloser}", parse_mode='html')
          return
       if check <= 1000:
          if farmcoin1 == 1:
             if check_balance1 <= balance:
                await bot.send_message(message.chat.id, f"🧰 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно купили {summ} видеокарт за {check_balance1_up}¢ !", parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - check_balance1} WHERE user_id = "{user_id}"') 
                cursor.execute(f'UPDATE users SET vcard = {vcard + summ} WHERE user_id = "{user_id}"') 
                connect.commit() 
             if check_balance1 > balance:
                await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, не достаточно средств! {rloser}", parse_mode='html')
                return
          if farmcoin2 == 1:
             if check_balance2 <= balance:
                await bot.send_message(message.chat.id, f"🧰 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно купили {summ} видеокарт за {check_balance2_up}¢ !", parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - check_balance2} WHERE user_id = "{user_id}"') 
                cursor.execute(f'UPDATE users SET vcard = {vcard + summ} WHERE user_id = "{user_id}"') 
                connect.commit() 
             if check_balance2 > balance:
                await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, не достаточно средств! {rloser}", parse_mode='html')
                return
          if farmcoin3 == 1:
             if check_balance3 <= balance:
                await bot.send_message(message.chat.id, f"🧰 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно купили {summ} видеокарт за {check_balance3_up}¢ !", parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - check_balance3} WHERE user_id = "{user_id}"') 
                cursor.execute(f'UPDATE users SET vcard = {vcard + summ} WHERE user_id = "{user_id}"') 
                connect.commit() 
             if check_balance3 > balance:
                await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, не достаточно средств! {rloser}", parse_mode='html')
                return
          if farmcoin4 == 1:
             if check_balance4 <= balance:
                await bot.send_message(message.chat.id, f"🧰 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно купили {summ} видеокарт за {check_balance4_up}¢ !", parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - check_balance4} WHERE user_id = "{user_id}"') 
                cursor.execute(f'UPDATE users SET vcard = {vcard + summ} WHERE user_id = "{user_id}"') 
                connect.commit() 
             if check_balance4 > balance:
                await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, не достаточно средств! {rloser}", parse_mode='html')
                return
          if farmcoin5 == 1:
             if check_balance5 <= balance:
                await bot.send_message(message.chat.id, f"🧰 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно купили {summ} видеокарт за {check_balance5_up}¢ !", parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance - check_balance5} WHERE user_id = "{user_id}"') 
                cursor.execute(f'UPDATE users SET vcard = {vcard + summ} WHERE user_id = "{user_id}"') 
                connect.commit() 
             if check_balance5 > balance:
                await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, не достаточно средств! {rloser}", parse_mode='html')
                return
                
    if message.text.startswith("ферма снять") or message.text.startswith("Ферма снять"):
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       farmcoin1 = cursor.execute("SELECT farmcoin1 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farmcoin1 = int(farmcoin1[0])
       farmcoin2 = cursor.execute("SELECT farmcoin2 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farmcoin2 = int(farmcoin2[0])
       farmcoin3 = cursor.execute("SELECT farmcoin3 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farmcoin3 = int(farmcoin3[0])
       farmcoin4 = cursor.execute("SELECT farmcoin4 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farmcoin4 = int(farmcoin4[0])
       farmcoin5 = cursor.execute("SELECT farmcoin5 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farmcoin5 = int(farmcoin5[0])
       vcard = cursor.execute("SELECT vcard from users where user_id = ?",(message.from_user.id,)).fetchone()
       vcard = int(vcard[0])
       farmscoin = farmcoin1 + farmcoin2 + farmcoin3 + farmcoin4 + farmcoin5
       bitcoin = cursor.execute("SELECT bitcoin from users where user_id = ?",(message.from_user.id,)).fetchone()
       bitcoin = int(bitcoin[0])
       bitmaning = cursor.execute("SELECT bitmaning from users where user_id = ?",(message.from_user.id,)).fetchone()
       bitmaning = int(bitmaning[0])
       summ = int(message.text.split()[2])
       summ_get = '{0:,}'.format(summ).replace(',', '.')
       chat_id = message.chat.id
       loser = ['😔', '😕', '😣', '😞', '😢']
       rloser = random.choice(loser)
       user_id = message.from_user.id
       balance = cursor.execute("SELECT balance from users where user_id = ?",(message.from_user.id,)).fetchone()
       balance = round(int(balance[0]))
       if summ <= 0:
          await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, вы не можете снять отрицательное число биткоина! {rloser}", parse_mode='html') 
          return
       if farmscoin == 0:
          await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас нету майнинг-фермы! {rloser}", parse_mode='html')
       if farmcoin1 == 1:
          if summ > bitmaning:
             await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, на счету вашей фермы недостаточно биткоинов! {rloser}", parse_mode='html') 
          if summ <= bitmaning:
             await bot.send_message(message.chat.id, f"🧰 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно сняли {summ_get}฿ с балансов вашей майнинг-фермы!", parse_mode='html')
             cursor.execute(f'UPDATE users SET bitmaning = {bitmaning - summ} WHERE user_id = "{user_id}"') 
             cursor.execute(f'UPDATE users SET bitcoin = {bitcoin + summ} WHERE user_id = "{user_id}"') 
             connect.commit() 
       if farmcoin2 == 1:
          if summ > bitmaning:
             await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, на счету вашей фермы недостаточно биткоинов! {rloser}", parse_mode='html') 
          if summ <= bitmaning:
             await bot.send_message(message.chat.id, f"🧰 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно сняли {summ_get}฿ с балансов вашей майнинг-фермы", parse_mode='html')
             cursor.execute(f'UPDATE users SET bitmaning = {bitmaning - summ} WHERE user_id = "{user_id}"') 
             cursor.execute(f'UPDATE users SET bitcoin = {bitcoin + summ} WHERE user_id = "{user_id}"') 
             connect.commit() 
       if farmcoin3 == 1:
          if summ > bitmaning:
             await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, на счету вашей фермы недостаточно биткоинов! {rloser}", parse_mode='html') 
          if summ <= bitmaning:
             await bot.send_message(message.chat.id, f"🧰 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно сняли {summ_get}฿️ с баланса вашей майнинг-фермы!", parse_mode='html')
             cursor.execute(f'UPDATE users SET bitmaning = {bitmaning - summ} WHERE user_id = "{user_id}"') 
             cursor.execute(f'UPDATE users SET bitcoin = {bitcoin + summ} WHERE user_id = "{user_id}"') 
             connect.commit() 
       if farmcoin4 == 1:
          if summ > bitmaning:
             await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, на счету вашей фермы недостаточно биткоинов! {rloser}", parse_mode='html') 
          if summ <= bitmaning:
             await bot.send_message(message.chat.id, f"🧰 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно сняли {summ_get}฿️ с баланса вашей майнинг-фермы!", parse_mode='html')
             cursor.execute(f'UPDATE users SET bitmaning = {bitmaning - summ} WHERE user_id = "{user_id}"') 
             cursor.execute(f'UPDATE users SET bitcoin = {bitcoin + summ} WHERE user_id = "{user_id}"') 
             connect.commit() 
       if farmcoin5 == 1:
          if summ > bitmaning:
             await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, на счету вашей фермы недостаточно биткоинов! {rloser}", parse_mode='html') 
          if summ <= bitmaning:
             await bot.send_message(message.chat.id, f"🧰 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно сняли {summ_get}฿️ с баланса вашей майнинг-фермы!", parse_mode='html')
             cursor.execute(f'UPDATE users SET bitmaning = {bitmaning - summ} WHERE user_id = "{user_id}"') 
             cursor.execute(f'UPDATE users SET bitcoin = {bitcoin + summ} WHERE user_id = "{user_id}"') 
             connect.commit() 

    if message.text.startswith("продать видеокарту") or message.text.startswith("Продать видеокарту"):
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       farmcoin1 = cursor.execute("SELECT farmcoin1 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farmcoin1 = int(farmcoin1[0])
       farmcoin2 = cursor.execute("SELECT farmcoin2 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farmcoin2 = int(farmcoin2[0])
       farmcoin3 = cursor.execute("SELECT farmcoin3 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farmcoin3 = int(farmcoin3[0])
       farmcoin4 = cursor.execute("SELECT farmcoin4 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farmcoin4 = int(farmcoin4[0])
       farmcoin5 = cursor.execute("SELECT farmcoin5 from users where user_id = ?",(message.from_user.id,)).fetchone()
       farmcoin5 = int(farmcoin5[0])
       vcard = cursor.execute("SELECT vcard from users where user_id = ?",(message.from_user.id,)).fetchone()
       vcard = int(vcard[0])
       chat_id = message.chat.id
       msg = message
       loser = ['😔', '😕', '😣', '😞', '😢']
       rloser = random.choice(loser)
       user_id = msg.from_user.id

       balance = cursor.execute("SELECT balance from users where user_id = ?",(message.from_user.id,)).fetchone()
       balance = round(int(balance[0]))

       farmscoin = farmcoin1 + farmcoin2 + farmcoin3 + farmcoin4 + farmcoin5
       summ = int(msg.text.split()[2])
       check = vcard + summ

       check_balance1 = summ * 3750000
       check_balance2 = summ * 45000000
       check_balance3 = summ * 487500000
       check_balance4 = summ * 60000000000
       check_balance5 = summ * 562500000000
       
       check_balance1_up = '{0:,}'.format(check_balance1).replace(',', '.')
       check_balance2_up = '{0:,}'.format(check_balance2).replace(',', '.')
       check_balance3_up = '{0:,}'.format(check_balance3).replace(',', '.')
       check_balance4_up = '{0:,}'.format(check_balance4).replace(',', '.')
       check_balance5_up = '{0:,}'.format(check_balance5).replace(',', '.')

       if summ <= 0:
          await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, вы не можете купить отрицательное число видеокарт! {rloser}", parse_mode='html')
          return
       if farmscoin == 0:
          await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас нету майнинг-фермы! {rloser}", parse_mode='html')
          return
       if summ > 1000:
          await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, вы не можете продать больше 1000 видеокарт! {rloser}", parse_mode='html')
          return
       if summ <= 1000:
          if farmcoin1 == 1:
             if summ <= vcard:
                await bot.send_message(message.chat.id, f"🧰 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно продали {summ} видеокарт за {check_balance1_up}¢ !", parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + check_balance1} WHERE user_id = "{user_id}"') 
                cursor.execute(f'UPDATE users SET vcard = {vcard - summ} WHERE user_id = "{user_id}"') 
                connect.commit() 
             if summ > vcard:
                await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно видеокарт! {rloser}", parse_mode='html')
                return
          if farmcoin2 == 1:
             if summ <= vcard:
                await bot.send_message(message.chat.id, f"🧰 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно продали {summ} видеокарт за {check_balance2_up}¢ !", parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + check_balance2} WHERE user_id = "{user_id}"') 
                cursor.execute(f'UPDATE users SET vcard = {vcard - summ} WHERE user_id = "{user_id}"') 
                connect.commit() 
             if summ > vcard:
                await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно видеокарт! {rloser}", parse_mode='html')
                return
          if farmcoin3 == 1:
             if summ <= vcard:
                await bot.send_message(message.chat.id, f"🧰 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно продали {summ} видеокарт за {check_balance3_up}¢ !", parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + check_balance3} WHERE user_id = "{user_id}"') 
                cursor.execute(f'UPDATE users SET vcard = {vcard - summ} WHERE user_id = "{user_id}"') 
                connect.commit() 
             if summ > vcard:
                await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно видеокарт! {rloser}", parse_mode='html')
                return
          if farmcoin4 == 1:
             if summ <= vcard:
                await bot.send_message(message.chat.id, f"🧰 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно продали {summ} видеокарт за {check_balance4_up}¢ !", parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + check_balance4} WHERE user_id = "{user_id}"') 
                cursor.execute(f'UPDATE users SET vcard = {vcard - summ} WHERE user_id = "{user_id}"') 
                connect.commit() 
             if summ > vcard:
                await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно видеокарт! {rloser}", parse_mode='html')
                return
          if farmcoin5 == 1:
             if summ <= vcard:
                await bot.send_message(message.chat.id, f"🧰 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно продали {summ} видеокарт за {check_balance5_up}¢ !", parse_mode='html')
                cursor.execute(f'UPDATE users SET balance = {balance + check_balance5} WHERE user_id = "{user_id}"') 
                cursor.execute(f'UPDATE users SET vcard = {vcard - summ} WHERE user_id = "{user_id}"') 
                connect.commit() 
             if summ > vcard:
                await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, недостаточно видеокарт! {rloser}", parse_mode='html')
                return


#############################################ИНТЕРНЕТ#################################################
    if message.text.lower() in ["Тикток", "тикток"]:
       msg = message
       user_id = msg.from_user.id
       tt_reg = cursor.execute("SELECT tt_reg from tiktok where user_id = ?",(message.from_user.id,)).fetchone()
       tt_reg = str(tt_reg[0])
       tt_name = cursor.execute("SELECT tt_name from tiktok where user_id = ?",(message.from_user.id,)).fetchone()
       tt_name = str(tt_name[0])
       tt_subs = cursor.execute("SELECT tt_subs from tiktok where user_id = ?", (message.from_user.id,)).fetchone()
       tt_subs = int(tt_subs[0])
       tt_subs2 = '{:,}'.format(tt_subs)
       tt_like = cursor.execute("SELECT tt_like from tiktok where user_id = ?",(message.from_user.id,)).fetchone()
       tt_like = int(tt_like[0])
       tt_videos = cursor.execute("SELECT tt_videos from tiktok where user_id = ?", (message.from_user.id,)).fetchone()
       tt_videos = int(tt_videos[0])
       tt_videos2 = '{:,}'.format(tt_videos)
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])
       if tt_reg in ['off']:
          await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас нет тиктока. Для регистрации напишите: Тикток создать [Название вашего тиктока].", parse_mode='html')
       else:
          photo = open('imges/tt.jpg', 'rb')
          await bot.send_photo(message.chat.id, photo, f"<a href='tg://user?id={user_id}'>{user_name}</a>, тикток « {tt_name} »\n👤 Подписчики: {tt_subs2}\n❤️ Лайки: {tt_like}\n  🎥 | Количество снятых видео: {tt_videos2}\n\n📹 Снять видео: тикток видео\n💞 Поставить лайк: тикток лайк [ответ на сообщение]", parse_mode='html')
    
    if message.text.lower() ==  'тикток реклама':
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       tt_reg = cursor.execute("SELECT tt_reg from tiktok where user_id = ?",(message.from_user.id,)).fetchone()
       tt_reg = tt_reg[0]
       user_id = message.from_user.id

       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])
       tt_videos = cursor.execute("SELECT tt_videos from tiktok where user_id = ?", (message.from_user.id,)).fetchone()
       tt_videos = int(tt_videos[0])
       period = 300 #300 s = 5m
       get = cursor.execute("SELECT stavka_ad FROM tiktok WHERE user_id = ?", (message.from_user.id,)).fetchone()
       last_stavka = int(get[0])
       stavkatime = time.time() - float(last_stavka)
       
       rx = random.randint(0,12000)
       rx2 = '{:,}'.format(rx)

       if tt_reg in 'off':
          await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас нет тиктока. Для регистрации напишите: Тикток создать [Название вашего тиктока]", parse_mode='html')
       else:
          if stavkatime > period:
             await bot.send_message(message.chat.id, f"✅ | <a href='tg://user?id={user_id}'>{user_name}</a>, на эту опубликованную рекламу никак не повлияли, а вы заработали {rx2}¢", parse_mode='html')
             cursor.execute(f'UPDATE users SET balance = {balance + rx}  WHERE user_id = "{user_id}"')
             cursor.execute(f'UPDATE tiktok SET stavka_ad = {time.time()} WHERE user_id = "{user_id}"')
             connect.commit()
          else:
             await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, слишком часто выкладывать рекламу тоже вредно! Подождите 5 минут.", parse_mode='html') 
    
    
    if message.text.lower() ==  'тикток видео':
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       tt_reg = cursor.execute("SELECT tt_reg from tiktok where user_id = ?",(message.from_user.id,)).fetchone()
       tt_reg = tt_reg[0]
       user_id = message.from_user.id

       tt_subs = cursor.execute("SELECT tt_subs from tiktok where user_id = ?", (message.from_user.id,)).fetchone()
       tt_subs = int(tt_subs[0])
       tt_subs2 = '{:,}'.format(tt_subs)
       tt_videos = cursor.execute("SELECT tt_videos from tiktok where user_id = ?", (message.from_user.id,)).fetchone()
       tt_videos = int(tt_videos[0])
       tt_videos2 = '{:,}'.format(tt_videos)
       period = 300 #300 s = 5m
       get = cursor.execute("SELECT stavka_tt FROM tiktok WHERE user_id = ?", (message.from_user.id,)).fetchone()
       last_stavka = int(get[0])
       stavkatime = time.time() - float(last_stavka)
       
       rx = random.randint(0,120)
       rx2 = '{:,}'.format(rx)

       if tt_reg in 'off':
          await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас нет тиктока. Для регистрации напишите: Тикток создать [Название вашего тиктока]", parse_mode='html')
       else:
          if stavkatime > period:
             await bot.send_message(message.chat.id, f"я🎥 | <a href='tg://user?id={user_id}'>{user_name}</a>, вы сняли новое видео в ТикТок и на вас подписалось {rx2} новых подписчиков", parse_mode='html')
             cursor.execute(f'UPDATE tiktok SET tt_subs = {tt_subs + rx}  WHERE user_id = "{user_id}"')
             cursor.execute(f'UPDATE tiktok SET tt_videos = {tt_videos + 1}  WHERE user_id = "{user_id}"')
             cursor.execute(f'UPDATE tiktok SET stavka_tt = {time.time()} WHERE user_id = "{user_id}"')
             connect.commit()
          else:
             await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, слишком часто выкладывать видео тоже вредно! Подождите 5 минут.", parse_mode='html') 
             
    if message.text.startswith('повтори'): 
       text = " ".join(message.text.split()[1:])
       await bot.send_message(message.chat.id, f"{text}")
    if message.text.startswith('Повтори'): 
       text = " ".join(message.text.split()[1:])
       await bot.send_message(message.chat.id, f"{text}")
    if message.text.startswith('Тикток создать') or message.text.startswith('тикток создать'):
       user_name = cursor.execute("SELECT tt_name from tiktok where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       tt_reg = cursor.execute("SELECT tt_reg from tiktok where user_id = ?",(message.from_user.id,)).fetchone()
       tt_reg = str(tt_reg[0])
       tt_name = cursor.execute("SELECT tt_name from tiktok where user_id = ?",(message.from_user.id,)).fetchone()
       tt_name = str(tt_name[0])
       chat_id = message.chat.id
       user_id = message.from_user.id
       name = " ".join(message.text.split()[2:])
       loser = ['😔', '😕', '😣', '😞', '😢']
       rloser = random.choice(loser)
       if tt_reg in 'on':
          await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, у вас уже есть ТикТок аккаунт", parse_mode='html')
       else:
          if len(name) <= 20:
             await bot.send_message(message.chat.id, f"Вы успешно создали ТикТок аккаунт!", parse_mode='html')
             cursor.execute(f'UPDATE tiktok SET tt_name = \"{name}\" WHERE user_id = "{user_id}"')
             cursor.execute(f'UPDATE tiktok SET tt_reg = "on" WHERE user_id = "{user_id}"')
          else: 
             await bot.send_message(message.chat.id, f"ℹ️ | <a href='tg://user?id={user_id}'>{user_name}</a> , ник вашего тик ток аккаунта не может быть длинее 20 символов! [{rloser}] ", parse_mode='html')
    
    

    if message.text.lower() ==  'тикток лайк':
       msg = message
       reply_user_id = msg.reply_to_message.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       tt_name = cursor.execute("SELECT tt_name from tiktok where user_id = ?",(message.from_user.id,)).fetchone()
       tt_name = tt_name[0]
       user_id = message.from_user.id

       tt_subs = cursor.execute("SELECT tt_subs from tiktok where user_id = ?", (message.from_user.id,)).fetchone()
       tt_subs = int(tt_subs[0])
       tt_videos = cursor.execute("SELECT tt_videos from tiktok where user_id = ?", (message.from_user.id,)).fetchone()
       tt_videos = int(tt_videos[0])
       tt_like = cursor.execute("SELECT tt_like from tiktok where user_id = ?", (message.from_user.id,)).fetchone()
       tt_like = int(tt_like[0])
       reply_tt_reg = cursor.execute("SELECT tt_reg from tiktok where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
       reply_tt_reg = str(reply_tt_reg[0])
       reply_user_name = cursor.execute(f"SELECT user_name from users where user_id = {reply_user_id}").fetchone()
       reply_user_name = str(reply_user_name[0])
       period = 300 
       get = cursor.execute("SELECT stavka_like FROM tiktok WHERE user_id = ?", (message.from_user.id,)).fetchone()
       last_stavka = int(get[0])
       stavkatime = time.time() - float(last_stavka)

       if reply_tt_reg in 'off':
          await bot.send_message(message.chat.id, f"⛔ | <a href='tg://user?id={user_id}'>{user_name}</a>, у пользователя нету ТикТок аккаунта", parse_mode='html')
       else:
          
          if stavkatime > period:
             await bot.send_message(message.chat.id, f"❤️ | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно поставили <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a> лайк!", parse_mode='html')
             cursor.execute(f'UPDATE tiktok SET tt_like = {tt_like + 1}  WHERE user_id = "{reply_user_id}"')
             cursor.execute(f'UPDATE tiktok SET stavka_like = {time.time()} WHERE user_id = "{user_id}"')
             connect.commit()
          else:
             await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, ТикТок заметил вашу подозрительную активность и ограничил доступ на 5 минут к лайку.", parse_mode='html')


########################################################РАЗНОЕ###########################################################
    if message.text.lower().startswith("шанс"):
       g = random.randint(0,100)
       await message.reply(f"""Шанс этого {g}%""")
    	
    if message.text.lower().startswith("шар"):
       h = ["Мой ответ - нет","Мне кажется - да","Сейчас нельзя предсказать","Мне кажется - нет","Знаки говорят - нет","Да","Нет","Можешь быть уверен в этом"]
       g = random.choice(h)
       await message.reply(f"""{g} """)
    	
    if message.text.lower().startswith("выбери"):
    	h = ["Мне кажется,что 1 вариант лучше","Однозначно второй","Однозначно первый","Второй вариант лучше","Первый вариант лучше"]
    	g = random.choice(h)
    	await message.reply(f"""{g}""")
    	
    if message.text.lower().startswith("киви"):
    	await message.reply("""🟠QIWI владельца | оплата по никнейму
https://qiwi.com/n/REDSHARKQ""")

########################################################ГОРОД############################################################
    if message.text.startswith('город построить') or message.text.startswith('Город построить') or message.text.startswith('построить город'):
    	user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,))
    	user_name = cursor.fetchone()
    	user_name = user_name[0]
    	user_id = message.from_user.id
    	balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,))
    	balance = cursor.fetchone()
    	balance = int(balance[0])
    	cursor.execute("SELECT city_name FROM city WHERE user_id=?",(message.from_user.id,))
    	if cursor.fetchone() is None:
    		if balance>=1_000_000_000_000:
    			try:
    				name = str(message.text.split()[2])
    			except:
    				await message.reply('‼️ Не хватает аргументов!\nПример: Город построить название ')
    				return
    			cursor.execute(f"UPDATE users SET balance={balance - 1_000_000_000_000} WHERE user_id=?",(message.from_user.id,))
    			cursor.execute(f'INSERT INTO city VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);', (100,user_id, user_name, 0, name, 50, 1, 1, 1, 1000,5,100,30,100,0,0))
    			await message.reply(f'🌆 <a href="tg://user?id={user_id}">{user_name}</a> Вы успешно построили город', parse_mode='html')
    			connect.commit()
    		else:
    			await message.reply(f'💰 <a href="tg://user?id={user_id}">{user_name}</a> Вы не можете построить город (недостаточно средств)\n Стоимость: 1.000.000.000.000¢(1трлн) ', parse_mode='html')
    	else:
    		await message.reply('‼️ Вы уже построили город!')
    		
    if message.text.lower() in ["мой город", "Мой город","город","Город"]:
    	user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,))
    	user_name = cursor.fetchone()
    	user_name = user_name[0]
    	user_id = message.from_user.id
    	
    	cursor.execute("SELECT city_name FROM city WHERE user_id=?", (message.from_user.id,))
    	if cursor.fetchone() != None:
    		citizens=cursor.execute("SELECT citizens FROM city WHERE user_id=?", (message.from_user.id,))
    		citizens=cursor.fetchone()
    		citizens=int(citizens[0])
    		
    		kazna = cursor.execute("SELECT kazna FROM city WHERE user_id=?", (message.from_user.id,))
    		kazna = cursor.fetchone()
    		kazna = int(kazna[0])
    		
    		city_name = cursor.execute("SELECT city_name FROM city WHERE user_id=?", (message.from_user.id,))
    		city_name = cursor.fetchone()
    		city_name = str(city_name[0])
    		
    		happynes = cursor.execute("SELECT happynes FROM city WHERE user_id=?", (message.from_user.id,))
    		happynes = cursor.fetchone()
    		happynes = float(happynes[0])
    		
    		electricity = cursor.execute("SELECT electricity FROM city WHERE user_id=?", (message.from_user.id,))
    		electricity = cursor.fetchone()
    		electricity = int(electricity[0])
    		
    		water = cursor.execute("SELECT water FROM city WHERE user_id=?", (message.from_user.id,))
    		water = cursor.fetchone()
    		water = int(water[0])
    		
    		factory = cursor.execute("SELECT factory FROM city WHERE user_id=?", (message.from_user.id,))
    		factory = cursor.fetchone()
    		factory = int(factory[0])
    		
    		road = cursor.execute("SELECT road FROM city WHERE user_id=?", (message.from_user.id,))
    		road = cursor.fetchone()
    		road = int(road[0])
    		
    		houses = cursor.execute("SELECT houses FROM city WHERE user_id=?", (message.from_user.id,))
    		houses = cursor.fetchone()
    		houses = int(houses[0])
    		
    		work_place = cursor.execute("SELECT work_place FROM city WHERE user_id=?", (message.from_user.id,))
    		work_place = cursor.fetchone()
    		work_place = int(work_place[0])
    		
    		taxes = cursor.execute("SELECT taxes FROM city WHERE user_id=?", (message.from_user.id,))
    		taxes = cursor.fetchone()
    		taxes = int(taxes[0])
    		
    		if happynes>20:
    			happynes2 = "🙁"
    		if happynes > 40:
    			happynes2 = "😑"
    		if happynes>60:
    			happynes2 = "🙂"
    		if happynes > 80:
    			happynes2="😇"
    		if happynes < 20:
    			happynes2 = "🤬"
    		material = cursor.execute("SELECT material FROM city WHERE user_id=?", (message.from_user.id,))
    		material = cursor.fetchone()
    		material = int(material[0])
    		kazna2 = '{:,}'.format(kazna).replace(',', '.')
    		material2 = '{:,}'.format(material).replace(',', '.')
    		citizens2 = '{:,}'.format(citizens).replace(',', '.')
    		work_place2 = '{:,}'.format(work_place).replace(',', '.')
    		factory2 = '{:,}'.format(factory).replace(',', '.')
    		houses2 = '{:,}'.format(houses).replace(',', '.')
    		electricity3=round((houses*30)+(factory*45))
    		electricity4 = '{:,}'.format(electricity3).replace(',', '.')
    		water3 = round((houses * 30) + (factory * 45))
    		water4 = '{:,}'.format(water3).replace(',', '.')
    		water5=water*100
    		water2 = '{:,}'.format(water5).replace(',', '.')
    		electricity5=electricity*100
    		electricity2 = '{:,}'.format(electricity5).replace(',', '.')
    		road2 = '{:,}'.format(road).replace(',', '.')
    		if electricity5<electricity3 :
    			problem="⚠️ В городе есть проблемы:\n⚡ Расходы энергий превышают её добычу!\n➖ Постройте АЭС"
    		if water5<water3:
    			problem = "⚠️ В городе есть проблемы:\n💦 Расходы воды превышают её добычу!\n➖ Постройте водонапорную башню"
    		if electricity5<electricity3 and water5<water3:
    			problem = "⚠️ В городе есть проблемы:\n💦 Расходы воды превышают её добычу!\n⚡ Расходы энергий превышают её добычу!\n➖ Постройте водонапорную башню\n➖ Постройте АЭС"
    		if electricity5>electricity3 and water5>water3:
    			problem=""
    		await bot.send_message(message.chat.id, f"""
<a href="tg://user?id={user_id}">{user_name}</a>, информация о Вашем городе:
🏙 Название: {city_name} 
💰 Казна города: {kazna2}
👥 Жителей: {citizens2} чел
⠀{happynes2} Счастье: {round(happynes, 2)}%
⠀👨🏻‍🔧 Работают: {work_place2} чел
⠀💸 Налоги: {taxes}%
⠀💧 Вода: {water2}/{water4}м³/час-[выроботка/затрат]
⠀⚡️ Энергия: {electricity2}/{electricity4}МВт-[выроботка/затрат]
📦 Материалов: {material2} шт
⠀🚙 Дороги: {road2} метров

🏗 Здания:
🏡 Жилой дом: {houses2}x
🔧 Завод: {factory2}x
☢️ АЭС: {electricity}x
💧 Водонапорная башня: {water}x

<b>{problem}</b>
    """, parse_mode='html')
    	
    if message.text.startswith("город снять") or message.text.startswith("Город снять"):
    	user_name = cursor.execute("SELECT user_name from users where user_id = ?", (message.from_user.id,))
    	user_name = cursor.fetchone()
    	user_name = user_name[0]
    	user_id = message.from_user.id
    	
    	cursor.execute("SELECT city_name FROM city WHERE user_id=?", (message.from_user.id,))
    	if cursor.fetchone() != None:
    		kazna = cursor.execute("SELECT kazna FROM city WHERE user_id=?", (message.from_user.id,))
    		kazna = cursor.fetchone()
    		kazna = int(kazna[0])
    		balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,))
    		balance = cursor.fetchone()
    		balance = int(balance[0])
    		if kazna>0:
    			cursor.execute(f"UPDATE users SET balance={balance+kazna} WHERE user_id=?", (message.from_user.id,))
    			cursor.execute(f"UPDATE city SET kazna={0} WHERE user_id=?", (message.from_user.id,))
    			connect.commit()
    			kazna2 = '{:,}'.format(kazna).replace(',', '.')
    			balance2 = '{:,}'.format(balance).replace(',', '.')
    			await message.reply(f"""
‼️<a href="tg://user?id={user_id}">{user_name}</a>, Вы забрали из казны города {kazna2} 👍
💰 Баланс: {balance}
💳 Казна города: 0
    """, parse_mode='html')
    
    if message.text.startswith('Г налог') or message.text.startswith('г налог')or message.text.startswith('Город налог'):
    	user_name = cursor.execute("SELECT user_name from users where user_id = ?", (message.from_user.id,))
    	user_name = cursor.fetchone()
    	user_name = user_name[0]
    	user_id = message.from_user.id
    	
    	cursor.execute("SELECT city_name FROM city WHERE user_id=?", (message.from_user.id,))
    	if cursor.fetchone() != None:
    		try:
    			count = int(message.text.split()[2])
    		except:
    			await message.reply('‼️ Не хватает аргументов!\nПример: Город налог 1-99 ')
    			return
    		if count>=1:
    			if count<100:
    				cursor.execute(f"UPDATE city SET taxes={count} WHERE user_id=?", (message.from_user.id,))
    				city3 = random.uniform(0.01, 0.99)
    				city4 = random.randint(1, 8)
    				cursor.execute(f"UPDATE city SET happynes={float(city4 + city3)} WHERE taxes<99")
    				cursor.execute(f"UPDATE city SET happynes={20 + city3 + city4} WHERE taxes>80")
    				cursor.execute(f"UPDATE city SET happynes={40 + city3 + city4} WHERE taxes<60")
    				cursor.execute(f"UPDATE city SET happynes={60 + city3 + city4} WHERE taxes<40")
    				cursor.execute(f"UPDATE city SET happynes={80 + city3 + city4} WHERE taxes<20")
    				if count in range(90,100):
    					await message.reply(
    					f'‼️<a href="tg://user?id={user_id}">{user_name}</a>, Вы установили размер налога в {count}%! \n'
    					f'💰 Жители отдают всю свою зарплату. Возможно, стоит уменьшить размер налога?',parse_mode='html')
    				else:
    					await message.reply(f'‼️<a href="tg://user?id={user_id}">{user_name}</a>, Вы установили размер налога в {count}%! ',parse_mode='html')
    			else:
    				await message.reply('‼️ Установите размер налоговой ставки с помощью «Г налог [1-99]» 👍🏼')
    		else:
    			await message.reply('‼️ Установите размер налоговой ставки с помощью «Г налог [1-99]» 👍🏼')
    	else:
    		await message.reply('‼️ Для начало постройте город : Город построить [название]!')
    		
    if message.text.startswith('Город дорога') or message.text.startswith('город дорога'):    
    	user_name = cursor.execute("SELECT user_name from users where user_id = ?", (message.from_user.id,))
    	user_name = cursor.fetchone()
    	user_name = user_name[0]
    	user_id = message.from_user.id
    	
    	cursor.execute("SELECT city_name FROM city WHERE user_id=?", (message.from_user.id,))
    	
    	if cursor.fetchone() != None:
    		try:
    			count = int(message.text.split()[2])
    		except:
    			await message.reply('‼️ Не хватает аргументов!\nПример: город дорога 1 ')
    			return
    			
    		price = 10
    		material = cursor.execute("SELECT material FROM city WHERE user_id=?", (message.from_user.id,))
    		material = cursor.fetchone()
    		material = int(material[0])
    		zavodov=round(int(material / price))
    		
    		road = cursor.execute("SELECT road FROM city WHERE user_id=?", (message.from_user.id,))
    		road = cursor.fetchone()
    		road = int(road[0])
    		
    		if count>0:
    			if material>=price*count:
    				
    				cursor.execute(f"UPDATE city SET material={material-(price*count)} WHERE user_id=?", (message.from_user.id,))
    				cursor.execute(f"UPDATE city SET road={road+count} WHERE user_id=?", (message.from_user.id,))
    				connect.commit()
    				await message.reply(f'<a href="tg://user?id={user_id}">{user_name}</a>, Вы проложили {count} метров дороги  ☺️',parse_mode='html')
    			else:
    				await message.reply(f'‼️ Недостаточно материалов ! Вам хватит на {zavodov} метров!')
    		else:
    			await message.reply('‼️ Введите положительно число!')
    	else:
    		await message.reply('‼️ Для начало постройте город : Город построить [название]!')
    
    if message.text.startswith('Город завод ') or message.text.startswith('город завод '):
    	user_name = cursor.execute("SELECT user_name from users where user_id = ?", (message.from_user.id,))
    	user_name = cursor.fetchone()
    	user_name = user_name[0]
    	user_id = message.from_user.id
    	
    	cursor.execute("SELECT city_name FROM city WHERE user_id=?", (message.from_user.id,))
    	if cursor.fetchone() != None:
    		try:
    			count = int(message.text.split()[2])
    		except:
    			await message.reply('‼️ Не хватает аргументов!\nПример: город завод 1 ')
    			return
    		electricity = cursor.execute("SELECT electricity FROM city WHERE user_id=?", (message.from_user.id,))
    		electricity = cursor.fetchone()
    		electricity = int(electricity[0])
    		houses = cursor.execute("SELECT houses FROM city WHERE user_id=?", (message.from_user.id,))
    		houses = cursor.fetchone()
    		houses = int(houses[0])
    		water = cursor.execute("SELECT water FROM city WHERE user_id=?", (message.from_user.id,))
    		water = cursor.fetchone()
    		water = int(water[0])
    		factory = cursor.execute("SELECT factory FROM city WHERE user_id=?", (message.from_user.id,))
    		factory = cursor.fetchone()
    		factory = int(factory[0])
    		balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,))
    		balance = cursor.fetchone()
    		balance = int(balance[0])
    		citizens = cursor.execute("SELECT citizens FROM city WHERE user_id=?", (message.from_user.id,))
    		citizens = cursor.fetchone()
    		citizens = int(citizens[0])
    		work_place = cursor.execute("SELECT work_place FROM city WHERE user_id=?", (message.from_user.id,))
    		work_place = cursor.fetchone()
    		work_place = int(work_place[0])
    		price = 500_000_000_000
    		limit=round((factory*25)+(water*15)+(electricity*15))
    		zavodov=round(int(balance / price ))
    		
    		road = cursor.execute("SELECT road FROM city WHERE user_id=?", (message.from_user.id,))
    		road = cursor.fetchone()
    		road = int(road[0])
    		build=(electricity+houses+factory+water) * 100
    		if count>0:
    			if balance>=price*count:
    				if citizens>=limit+(count*25):
    					if road>=build+(count*100):
    						cursor.execute(f"UPDATE users SET balance={balance-(price*count)} WHERE user_id=?", (message.from_user.id,))
    						cursor.execute(f"UPDATE city SET factory={factory+count} WHERE user_id=?", (message.from_user.id,))
    						cursor.execute(f"UPDATE city SET work_place={work_place + (count*25)} WHERE user_id=?", (message.from_user.id,))
    						connect.commit()
    						work_place2 = '{:,}'.format(work_place).replace(',', '.')
    						await message.reply(
    						f'<a href="tg://user?id={user_id}">{user_name}</a>, Вы построили «Завод» {count}х ☺️\n'
    						f'🔧 Рабочих мест : {work_place2} [+{count*25}]!',parse_mode='html')
    					else:
    						await message.reply(f'‼️ Для постройки большего кол-во заводов нужно построить дороги')
    				else:
    					await message.reply(f'‼️ Для постройки большего кол-во заводов нужно больше жителей')
    			else:
    				await message.reply(f'‼️ Недостаточно средств ! Вам хватит на {zavodov} заводов!')
    		else:
    			await message.reply('‼️ Введите положительно число!')
    	else:
    		await message.reply('‼️ Для начало постройте город : Город построить [название]!')
    		
    if message.text.startswith('Город вода') or message.text.startswith('город вода'):
    	user_name = cursor.execute("SELECT user_name from users where user_id = ?", (message.from_user.id,))
    	user_name = cursor.fetchone()
    	user_name = user_name[0]
    	user_id = message.from_user.id
    	
    	cursor.execute("SELECT city_name FROM city WHERE user_id=?", (message.from_user.id,))
    	if cursor.fetchone() != None:
    		try:
    			count = int(message.text.split()[2])
    		except:
    			await message.reply('‼️ Не хватает аргументов!\nПример: Город вода 1 ')
    			return
    		electricity = cursor.execute("SELECT electricity FROM city WHERE user_id=?", (message.from_user.id,))
    		electricity = cursor.fetchone()
    		electricity = int(electricity[0])
    		houses = cursor.execute("SELECT houses FROM city WHERE user_id=?", (message.from_user.id,))
    		houses = cursor.fetchone()
    		houses = int(houses[0])
    		water = cursor.execute("SELECT water FROM city WHERE user_id=?", (message.from_user.id,))
    		water = cursor.fetchone()
    		water = int(water[0])
    		factory = cursor.execute("SELECT factory FROM city WHERE user_id=?", (message.from_user.id,))
    		factory = cursor.fetchone()
    		factory = int(factory[0])
    		
    		citizens = cursor.execute("SELECT citizens FROM city WHERE user_id=?", (message.from_user.id,))
    		citizens = cursor.fetchone()
    		citizens = int(citizens[0])
    		work_place = cursor.execute("SELECT work_place FROM city WHERE user_id=?", (message.from_user.id,))
    		work_place = cursor.fetchone()
    		work_place = int(work_place[0])
    		material = cursor.execute("SELECT material FROM city WHERE user_id=?", (message.from_user.id,))
    		material = cursor.fetchone()
    		material = int(material[0])
    		price = 500
    		limit=round((factory*25)+(water*15)+(electricity*15))
    		zavodov=round(int(material / price))
    		
    		road = cursor.execute("SELECT road FROM city WHERE user_id=?", (message.from_user.id,))
    		road = cursor.fetchone()
    		road = int(road[0])
    		build=(electricity+houses+factory+water) * 100
    		if count>0:
    			if material>=price*count:
    				if citizens>=limit+(count*25):
    					if road>=build+(count*100):
    						cursor.execute(f"UPDATE city SET material={material-(price*count)} WHERE user_id=?", (message.from_user.id,))
    						cursor.execute(f"UPDATE city SET water={water+count} WHERE user_id=?", (message.from_user.id,))
    						cursor.execute(f"UPDATE city SET work_place={work_place + (count*15)} WHERE user_id=?", (message.from_user.id,))
    						connect.commit()
    						work_place2 = '{:,}'.format(work_place).replace(',', '.')
    						await message.reply(
    						f'<a href="tg://user?id={user_id}">{user_name}</a>, Вы построили «Водонапорную башню» {count}х ☺️\n'
    						f'🔧 Рабочих мест : {work_place2} [+{count*15}]!',parse_mode='html')
    					else:
    						await message.reply(f'‼️ Для постройки большего кол-во Водонапорных башен нужно построить дороги')
    				else:
    					await message.reply(f'‼️ Для постройки большего кол-во Водонапорных башен нужно больше жителей')
    			else:
    				await message.reply(f'‼️ Недостаточно материалов ! Вам хватит на {zavodov} Водонапорных башен!')
    		else:
    			await message.reply('‼️ Введите положительно число!')
    	else:
    		await message.reply('‼️ Для начало постройте город : Город построить [название]!')
    		
    if message.text.startswith('Город энергия') or message.text.startswith('город энергия'):
    	user_name = cursor.execute("SELECT user_name from users where user_id = ?", (message.from_user.id,))
    	user_name = cursor.fetchone()
    	user_name = user_name[0]
    	user_id = message.from_user.id
    	
    	cursor.execute("SELECT city_name FROM city WHERE user_id=?", (message.from_user.id,))
    	if cursor.fetchone() != None:
    		try:
    			count = int(message.text.split()[2])
    		except:
    			await message.reply('‼️ Не хватает аргументов!\nПример: город энергия 1 ')
    			return
    		electricity = cursor.execute("SELECT electricity FROM city WHERE user_id=?", (message.from_user.id,))
    		electricity = cursor.fetchone()
    		electricity = int(electricity[0])
    		houses = cursor.execute("SELECT houses FROM city WHERE user_id=?", (message.from_user.id,))
    		houses = cursor.fetchone()
    		houses = int(houses[0])
    		water = cursor.execute("SELECT water FROM city WHERE user_id=?", (message.from_user.id,))
    		water = cursor.fetchone()
    		water = int(water[0])
    		factory = cursor.execute("SELECT factory FROM city WHERE user_id=?", (message.from_user.id,))
    		factory = cursor.fetchone()
    		factory = int(factory[0])
    		
    		citizens = cursor.execute("SELECT citizens FROM city WHERE user_id=?", (message.from_user.id,))
    		citizens = cursor.fetchone()
    		citizens = int(citizens[0])
    		work_place = cursor.execute("SELECT work_place FROM city WHERE user_id=?", (message.from_user.id,))
    		work_place = cursor.fetchone()
    		work_place = int(work_place[0])
    		material = cursor.execute("SELECT material FROM city WHERE user_id=?", (message.from_user.id,))
    		material = cursor.fetchone()
    		material = int(material[0])
    		price = 500
    		limit=round((factory*25)+(water*15)+(electricity*15))
    		zavodov=round(int(material / price))
    		
    		road = cursor.execute("SELECT road FROM city WHERE user_id=?", (message.from_user.id,))
    		road = cursor.fetchone()
    		road = int(road[0])
    		build=(electricity+houses+factory+water) * 100
    		if count>0:
    			if material>=price*count:
    				if citizens>=limit+(count*25):
    					if road>=build+(count*100):
    						cursor.execute(f"UPDATE city SET material={material - (price*count)} WHERE user_id=?", (message.from_user.id,))
    						cursor.execute(f"UPDATE city SET electricity={electricity + count} WHERE user_id=?", (message.from_user.id,))
    						cursor.execute(f"UPDATE city SET work_place={work_place + (count * 15)} WHERE user_id=?", (message.from_user.id,))
    						connect.commit()
    						work_place2 = '{:,}'.format(work_place).replace(',', '.')
    						await message.reply(
    						f'<a href="tg://user?id={user_id}">{user_name}</a>, Вы построили «АЭС» {count}х ☺️\n'
    						f'🔧 Рабочих мест : {work_place2} [+{count * 15}]!',parse_mode='html')
    					else:
    						await message.reply(f'‼️ Для постройки большего кол-во АЭС нужно построить дороги')
    				else:
    					await message.reply(f'‼️ Для постройки большего кол-во АЭС нужно больше жителей')
    			else:
    				await message.reply(f'‼️ Недостаточно материалов ! Вам хватит на {zavodov} АЭС!')
    		else:
    			await message.reply('‼️ Введите положительно число!')
    	else:
    		await message.reply('‼️ Для начало постройте город : Город построить [название]!')
    		
    if message.text.startswith('Город дом') or message.text.startswith('город дом'):
    	user_name = cursor.execute("SELECT user_name from users where user_id = ?", (message.from_user.id,))
    	user_name = cursor.fetchone()
    	user_name = user_name[0]
    	user_id = message.from_user.id
    	
    	cursor.execute("SELECT city_name FROM city WHERE user_id=?", (message.from_user.id,))
    	if cursor.fetchone() != None:
    		try:
    			count = int(message.text.split()[2])
    		except:
    			await message.reply('‼️ Не хватает аргументов!\nПример: город энергия 1 ')
    			return
    		electricity = cursor.execute("SELECT electricity FROM city WHERE user_id=?", (message.from_user.id,))
    		electricity = cursor.fetchone()
    		electricity = int(electricity[0])
    		houses = cursor.execute("SELECT houses FROM city WHERE user_id=?", (message.from_user.id,))
    		houses = cursor.fetchone()
    		houses = int(houses[0])
    		water = cursor.execute("SELECT water FROM city WHERE user_id=?", (message.from_user.id,))
    		water = cursor.fetchone()
    		water = int(water[0])
    		factory = cursor.execute("SELECT factory FROM city WHERE user_id=?", (message.from_user.id,))
    		factory = cursor.fetchone()
    		factory = int(factory[0])
    		
    		citizens = cursor.execute("SELECT citizens FROM city WHERE user_id=?", (message.from_user.id,))
    		citizens = cursor.fetchone()
    		citizens = int(citizens[0])
    		work_place = cursor.execute("SELECT work_place FROM city WHERE user_id=?", (message.from_user.id,))
    		work_place = cursor.fetchone()
    		work_place = int(work_place[0])
    		material = cursor.execute("SELECT material FROM city WHERE user_id=?", (message.from_user.id,))
    		material = cursor.fetchone()
    		material = int(material[0])
    		price = 150
    		
    		zavodov=round(int(material / price))
    		
    		road = cursor.execute("SELECT road FROM city WHERE user_id=?", (message.from_user.id,))
    		road = cursor.fetchone()
    		road = int(road[0])
    		build = (electricity + houses + factory + water) * 100
    		if count > 0:
    			if material >= price * count:
    				if road >= build + (count * 100):
    					cursor.execute(f"UPDATE city SET material={material - (price*count)} WHERE user_id=?", (message.from_user.id,))
    					cursor.execute(f"UPDATE city SET houses={houses + count} WHERE user_id=?", (message.from_user.id,))
    					cursor.execute(f"UPDATE city SET citizens={citizens + (count * 15)} WHERE user_id=?", (message.from_user.id,))
    					connect.commit()
    					work_place2 = '{:,}'.format(work_place).replace(',', '.')
    					await message.reply(
    					f'<a href="tg://user?id={user_id}">{user_name}</a>, Вы построили «Жилой дом» {count}х ☺️\n'
    					f'👤 Вместимость жителей: {houses*15} [+{count * 15}]!',parse_mode='html')
    				else:
    					await message.reply(f'‼️ Для постройки большего кол-во Жилых домов нужно построить дороги')
    			else:
    				await message.reply(f'‼️ Недостаточно материалов ! Вам хватит на {zavodov} Жилых домов!')
    		else:
    			await message.reply('‼️ Введите положительно число!')
    	else:
    		await message.reply('‼️ Для начало постройте город : Город построить [название]!')
    		
    if message.text.lower() in ['город переработка']:
    	user_name = cursor.execute("SELECT user_name from users where user_id = ?", (message.from_user.id,))
    	user_name = cursor.fetchone()
    	user_name = user_name[0]
    	user_id = message.from_user.id
    	
    	cursor.execute("SELECT city_name FROM city WHERE user_id=?", (message.from_user.id,))
    	if cursor.fetchone() != None:
    		
    		ore_processing_plant = cursor.execute("SELECT ore_processing_plant FROM city WHERE user_id=?", (message.from_user.id,))
    		ore_processing_plant = cursor.fetchone()
    		ore_processing_plant = int(ore_processing_plant[0])
    		citizens = cursor.execute("SELECT citizens FROM city WHERE user_id=?", (message.from_user.id,))
    		citizens = cursor.fetchone()
    		citizens = int(citizens[0])
    		balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,))
    		balance = cursor.fetchone()
    		balance = int(balance[0])
    		
    		if ore_processing_plant ==0:
    			if citizens >=100000:
    				if balance>=200_000_000_000_000:
    					cursor.execute(f"UPDATE city SET ore_processing_plant={1} WHERE user_id=?", (message.from_user.id,))
    					cursor.execute(f"UPDATE users SET balance={balance-200_000_000_000_000} WHERE user_id=?", (message.from_user.id,))
    					await message.reply(f'<a href="tg://user?id={user_id}">{user_name}</a>, Вы построили завод по «♻️Переработки руды» ☺️',parse_mode='html')
    				else:
    					await message.reply(f'‼️ Недостаточно средств ! 💰 Цена: 200.000.000.000.000¢')
    			else:
    				await message.reply(f'‼️ Для постройки завода по «♻️Переработки руды» нужно больше 100.000 жителей')
    		else:
    			await message.reply(f'‼️ У вас уже есть завод по переработки руды')
    	else:
    		await message.reply('‼️ Для начало постройте город : Город построить [название]!')
    		
    if message.text.lower() in ['город аренда']:
    	user_name = cursor.execute("SELECT user_name from users where user_id = ?", (message.from_user.id,))
    	user_name = cursor.fetchone()
    	user_name = user_name[0]
    	user_id = message.from_user.id
    	
    	cursor.execute("SELECT city_name FROM city WHERE user_id=?", (message.from_user.id,))
    	if cursor.fetchone() != None:
    		
    		earning = cursor.execute("SELECT earning FROM city WHERE user_id=?", (message.from_user.id,))
    		earning = cursor.fetchone()
    		earning = int(earning[0])
    		citizens = cursor.execute("SELECT citizens FROM city WHERE user_id=?", (message.from_user.id,))
    		citizens = cursor.fetchone()
    		citizens = int(citizens[0])
    		balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,))
    		balance = cursor.fetchone()
    		balance = int(balance[0])
    		
    		if earning == 0:
    			if citizens >=1000000:
    				if balance>=250_000_000_000_000:
    					cursor.execute(f"UPDATE city SET earning={1} WHERE user_id=?", (message.from_user.id,))
    					cursor.execute(f"UPDATE users SET balance={balance-250_000_000_000_000} WHERE user_id=?", (message.from_user.id,))
    					await message.reply(f'✅ <a href="tg://user?id={user_id}">{user_name}</a>, Вы развили «Аренду» в городе☺️',parse_mode='html')
    				else:
    					await message.reply(f'‼️ Недостаточно средств ! 💰 Цена: 200.000.000.000.000¢')
    			else:
    				await message.reply(f'‼️ Для развития  «Аренды» в городе нужно больше 1.000.000 жителей')
    		else:
    			await message.reply(f'‼️ Вы уже развили Аренду в городе!')
    	else:
    		await message.reply('‼️ Для начало постройте город : Город построить [название]!')


###############################################ШАХТА################################################
    if message.text.startswith('Шахта') or message.text.startswith('шахта'):
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       await bot.send_message(message.chat.id,f"""<a href='tg://user?id={user_id}'>{user_name}</a>, это шахта, Здесь вы сможете добыть ресурсы для дальнейшей продажи, На шахте можно добыть - камень, железо, бронза, золото. 

⛏ Чтобы копать вам понадобиться купить кирку.

✅ Как начать работать и добывать ресурсы?
Используйте команду <code>Копать руду</code>

♻ Как продавать ресурсы?
Используйте команду <code>Продать руду</code> [название руды]

🧰 Как увидеть свой инвентарь и знать что можно продать? Напишите «инвентарь».
       """, parse_mode='html')
    if message.text.startswith('продать') or message.text.startswith('Продать'):
      try:
         user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
         user_name = user_name[0]
         user_id = message.from_user.id

         balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
         balance = int(balance[0])

         # iron, silver, bronza, gold
         iron = cursor.execute("SELECT iron from mine where user_id = ?", (message.from_user.id,)).fetchone()
         iron = int(iron[0])
         
         metall = cursor.execute("SELECT metall from mine where user_id = ?", (message.from_user.id,)).fetchone()
         metall = int(metall[0])

         silver = cursor.execute("SELECT silver from mine where user_id = ?", (message.from_user.id,)).fetchone()
         silver = int(silver[0])

         bronza = cursor.execute("SELECT bronza from mine where user_id = ?", (message.from_user.id,)).fetchone()
         bronza = int(bronza[0])

         gold = cursor.execute("SELECT gold from mine where user_id = ?", (message.from_user.id,)).fetchone()
         gold = int(gold[0])

         rud = str(message.text.split()[1])

         c = int(message.text.split()[2])

         summ = c * 25000
         summ2 = '{:,}'.format(summ)
         if rud == 'камень':
            if c <= iron:
             if c > 0:               
               summ = c * 25000
               summ2 = '{:,}'.format(summ)
               await bot.send_message(message.chat.id, f"💸 | Вы успешно продали {c} камень 🪨 за {summ2}¢", parse_mode='html')
               cursor.execute(f'UPDATE users SET balance = {balance + summ} WHERE user_id = "{user_id}"')
               cursor.execute(f'UPDATE mine SET iron = {iron - c} WHERE user_id = "{user_id}"')
               connect.commit()
            else:
               await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас нету столько руды!", parse_mode='html')
         if rud == 'железо':
            if c <= metall:
             if c > 0:               
               summ = c * 45000
               summ2 = '{:,}'.format(summ)
               await bot.send_message(message.chat.id, f"💸 | Вы успешно продали {c} железо ⛓ за {summ2}¢", parse_mode='html')
               cursor.execute(f'UPDATE users SET balance = {balance + summ} WHERE user_id = "{user_id}"')
               cursor.execute(f'UPDATE mine SET metall = {metall - c} WHERE user_id = "{user_id}"')
               connect.commit()
            else:
               await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас нету столько руды!", parse_mode='html')

         if rud == 'серебро':
            if c <= silver:
             if c > 0:               
               summ = c * 125000
               summ2 = '{:,}'.format(summ)
               await bot.send_message(message.chat.id, f"💸 | Вы успешно продали {c} серебро 🪙 за {summ2}¢", parse_mode='html')
               cursor.execute(f'UPDATE users SET balance = {balance + summ} WHERE user_id = "{user_id}"')
               cursor.execute(f'UPDATE mine SET silver = {silver - c} WHERE user_id = "{user_id}"')
               connect.commit()
            else:
               await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас нету столько руды!", parse_mode='html')
         if rud == 'бронзу':
            if c <= bronza:
             if c > 0:               
               summ = c * 200000
               summ2 = '{:,}'.format(summ)
               await bot.send_message(message.chat.id, f"💸 | Вы успешно продали {c} бронзы 🔷 за {summ2}¢", parse_mode='html')
               cursor.execute(f'UPDATE users SET balance = {balance + summ} WHERE user_id = "{user_id}"')
               cursor.execute(f'UPDATE mine SET bronza = {bronza - c} WHERE user_id = "{user_id}"')
               connect.commit()
            else:
               await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас нету столько руды!", parse_mode='html')

         if rud == 'золото':
            if c <= gold:
             if c > 0:   
               summ = c * 500000
               summ2 = '{:,}'.format(summ)
               await bot.send_message(message.chat.id, f"💸 | Вы успешно продали {c} золото 🔶 за {summ2}¢", parse_mode='html')
               cursor.execute(f'UPDATE users SET balance = {balance + summ} WHERE user_id = "{user_id}"')
               cursor.execute(f'UPDATE mine SET bronza = {bronza - c} WHERE user_id = "{user_id}"')
               connect.commit()
            else:
               await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас нету столько руды!", parse_mode='html')
      except IndexError:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, Ошибка! Пример: [название руды] 1", parse_mode='html')       
    
    if message.text.startswith("Копать руду") or message.text.startswith("копать руду"):
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       pick = cursor.execute("SELECT pick from mine where user_id = ?", (message.from_user.id,)).fetchone()
       pick = pick[0]

       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])

       rx = random.randint(0,100)

      # iron, silver, bronza, gold
       iron = cursor.execute("SELECT iron from mine where user_id = ?", (message.from_user.id,)).fetchone()
       iron = int(iron[0])
       
       metall = cursor.execute("SELECT metall from mine where user_id = ?", (message.from_user.id,)).fetchone()
       metall = int(metall[0])

       silver = cursor.execute("SELECT silver from mine where user_id = ?", (message.from_user.id,)).fetchone()
       silver = int(silver[0])

       bronza = cursor.execute("SELECT bronza from mine where user_id = ?", (message.from_user.id,)).fetchone()
       bronza = int(bronza[0])

       gold = cursor.execute("SELECT gold from mine where user_id = ?", (message.from_user.id,)).fetchone()
       gold = int(gold[0])
       
       rx_iron = random.randint(15,20)
       rx_metall = random.randint(10,15)
       rx_silver = random.randint(5,10)
       rx_bronza = random.randint(0,5)
       
       period = 5
       get = cursor.execute("SELECT time_pick FROM bot_time WHERE user_id = ?", (message.from_user.id,)).fetchone()
       last_stavka = int(get[0])
       stavkatime = time.time() - float(last_stavka)

       if pick == 'on':
          if stavkatime > period:
             if int(rx) in range(0,40):
                await bot.send_message(message.chat.id, f"🪨 | Вы успешно выкопали {rx_iron} камня", parse_mode='html')
                cursor.execute(f'UPDATE mine SET iron = {iron + rx_iron} WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE bot_time SET time_pick = {time.time()} WHERE user_id = "{user_id}"')
                connect.commit()
                return
             if int(rx) in range(41,70):
                await bot.send_message(message.chat.id, f"⛓ | Вы успешно выкопали {rx_metall} железа", parse_mode='html')
                cursor.execute(f'UPDATE mine SET metall = {metall + rx_metall} WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE bot_time SET time_pick = {time.time()} WHERE user_id = "{user_id}"')
                connect.commit()
                return
             if int(rx) in range(71,85):
                await bot.send_message(message.chat.id, f"🪙 | Вы успешно выкопали {rx_silver} серебра", parse_mode='html')
                cursor.execute(f'UPDATE mine SET silver = {silver + rx_silver} WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE bot_time SET time_pick = {time.time()} WHERE user_id = "{user_id}"')
                connect.commit()
                return
             if int(rx) in range(86,95):
                await bot.send_message(message.chat.id, f"🔷 | Вы успешно выкопали {rx_bronza} бронзы", parse_mode='html')
                cursor.execute(f'UPDATE mine SET bronza = {bronza + rx_bronza} WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE bot_time SET time_pick = {time.time()} WHERE user_id = "{user_id}"')
                connect.commit()
                return
             if int(rx) in range(96,100):
                await bot.send_message(message.chat.id, f"🔶 | Вы успешно выкопали 1 золото", parse_mode='html')
                cursor.execute(f'UPDATE mine SET gold = {gold + 1} WHERE user_id = "{user_id}"')
                cursor.execute(f'UPDATE bot_time SET time_pick = {time.time()} WHERE user_id = "{user_id}"')
                connect.commit()
                return
          else:
             await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! собирать руду можно раз в {period} секунд!", parse_mode='html')
             return
       else:
          await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! у вас нету кирки, что бы купить кирку введите команду \"Купить кирку\"", parse_mode='html')
          return
          




    if message.text.startswith('Продать кирку') or message.text.startswith('продать кирку'):
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])
       
       pick = cursor.execute("SELECT pick from mine where user_id = ?", (message.from_user.id,)).fetchone()
       pick = pick[0]

       if pick == 'off':
          await bot.send_message(message.chat.id , f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! у вас и так нету кирки, что бы купить кирку введите команду \"Купить кирку\"", parse_mode='html')

       if pick == 'on':
          await bot.send_message(message.chat.id, f"⛏ | Вы продали кирку за 5.000¢ ", parse_mode='html')
          cursor.execute(f'UPDATE mine SET pick = "off" WHERE user_id = "{user_id}"')
          cursor.execute(f'UPDATE users SET balance = {balance + 5000} WHERE user_id = "{user_id}"')
          connect.commit()    
    if message.text.startswith('Купить кирку') or message.text.startswith('купить кирку'):
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id

       balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
       balance = int(balance[0])
       
       pick = cursor.execute("SELECT pick from mine where user_id = ?", (message.from_user.id,)).fetchone()
       pick = pick[0]

       if pick == 'on':
          await bot.send_message(message.chat.id , f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, подождите! у вас уже есть кирка, что бы продать кирку введите команду \"Продать кирку\"", parse_mode='html')

       if pick == 'off':
          if balance >= 5000:
             await bot.send_message(message.chat.id, f"⛏ | Вы купили кирку за 5.000¢ ", parse_mode='html')
             cursor.execute(f'UPDATE mine SET pick = "on" WHERE user_id = "{user_id}"')
             cursor.execute(f'UPDATE users SET balance = {balance - 5000} WHERE user_id = "{user_id}"')
             connect.commit()
          else:
             await bot.send_message(message.chat.id, f"🆘 | <a href='tg://user?id={user_id}'>{user_name}</a>, у вас не хватает средств!", parse_mode='html')          


###############################################ИНВЕНТАРЬ####################################################################

    if message.text.startswith('инвентарь') or message.text.startswith('Инвентарь') or message.text.startswith('инв') or message.text.startswith('Инв'):
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id
       
       loser = ['😐', '😕','😟','😔','😓']
       rloser = random.choice(loser)

       farm = 0
       men = 0
       ob = 0

       iron = cursor.execute("SELECT iron from mine where user_id = ?", (message.from_user.id,)).fetchone()
       iron = int(iron[0])
       iron_f = '{:,}'.format(iron)

       metall = cursor.execute("SELECT metall from mine where user_id = ?", (message.from_user.id,)).fetchone()
       metall = int(metall[0])
       metall_f = '{:,}'.format(metall)

       silver = cursor.execute("SELECT silver from mine where user_id = ?", (message.from_user.id,)).fetchone()
       silver = int(silver[0])
       silver_f = '{:,}'.format(silver)

       bronza = cursor.execute("SELECT bronza from mine where user_id = ?", (message.from_user.id,)).fetchone()
       bronza = int(bronza[0])
       bronza_f = '{:,}'.format(bronza)

       gold = cursor.execute("SELECT gold from mine where user_id = ?", (message.from_user.id,)).fetchone()
       gold = int(gold[0])
       gold_f = '{:,}'.format(gold)

       if iron > 0:
          iron2 = f'    🪨 | Камня: {iron_f} шт\n'
          men = men + 1
          ob = ob + 1
       else:
          iron2 = ''

       if metall > 0:
          metall2 = f'    ⛓ | Железа: {metall_f} шт\n'
          men = men + 1
          ob = ob + 1
       else:
          metall2 = ''
      
       if silver > 0:
          silver2 = f'    🪙 | Серебра: {silver_f} шт\n'
          men = men + 1
          ob = ob + 1
       else:
          silver2 = ''

       if bronza > 0:
          bronza2 = f'    🔷 | Бронзы: {bronza_f} шт\n'
          men = men + 1
          ob = ob + 1
       else:
          bronza2 = ''

       if gold > 0:
          gold2 = f'    🔶 | Золота: {gold_f} шт\n'
          men = men + 1
          ob = ob + 1
       else:
          gold2 = ''

       if men > 0:
          men_2 = '\n⛏ | Шахта\n'
       else:
          men_2 = ''
          
       if ob == 0:
          ob2 = f'Вещи отсутствуют {rloser}'
       else:
          ob2 = ''          
       
       await bot.send_message(message.chat.id, f"""<a href='tg://user?id={user_id}'>{user_name}</a>, вот ваш инвентарь:       	
{ob2}{men_2}{iron2}{metall2}{silver2}{bronza2}{gold2}
    """, parse_mode='html')


###############################################КЛАН####################################################################
    if message.text.lower().startswith('клан создать'):
        user_name = cursor.execute("SELECT user_name from users where user_id = ?",
                                   (message.from_user.id,))
        user_name = cursor.fetchone()
        user_name = user_name[0]
        user_id = message.from_user.id
        balance = cursor.execute(
            "SELECT balance from users where user_id = ?", (message.from_user.id,))
        balance = cursor.fetchone()
        balance = int(balance[0])
        data_с = await get_clan(message.from_user.id)
        if data_с is None:
            if balance >= 1_000_000:

                try:
                    name = str(message.text.split()[2])
                    if len(name) <= 30 and len(name) >= 4:
                        pass
                    else:
                        await message.reply('‼️Название клана должно быть не меньше 4 символов и не больше 30 символов')
                        return
                except:
                    await message.reply('‼️ Не хватает аргументов!\nПример: <code>клан создать</code> [название]')
                    return
                new_clan_id = cursor.execute(
                    "SELECT new_clan_id from clans_id ")
                new_clan_id = cursor.fetchone()
                new_clan_id = int(new_clan_id[0])
                cursor.execute(
                    f"UPDATE users SET balance={balance - 100_000_000_000_000} WHERE user_id=?", (message.from_user.id,))
                cursor.execute(
                    f'INSERT INTO clans VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);', (1, new_clan_id, name, 0, 1, new_clan_id, 0, 0, 0, 0))
                cursor.execute(
                    f'INSERT INTO clan VALUES (?, ?, ?, ?, ?);', (user_id, user_name, "SOZD", new_clan_id, name))
                connect.commit()
                await message.reply(
                    f'🛡️ <a href="tg://user?id={user_id}">{user_name}</a> Вы успешно создали клан',
                    parse_mode='html')
                cursor.execute(
                    f"UPDATE clans_id SET new_clan_id={new_clan_id+1}")
                connect.commit()
            else:
                await message.reply(f'💰 <a href="tg://user?id={user_id}">{user_name}</a> Нищий не может создать клан (недостаточно средств)\n Стоимость: 100.000.000.000.000¢',
                                    parse_mode='html')
        else:
            await message.reply(f'‼️ <a href="tg://user?id={user_id}">{user_name}</a> вы уже в клане', parse_mode='html')

    if message.text.lower().startswith('клан вступить'):
        user_name = cursor.execute("SELECT user_name from users where user_id = ?",
                                   (message.from_user.id,))
        user_name = cursor.fetchone()
        user_name = user_name[0]
        user_id = message.from_user.id
        data_с = await get_clan(message.from_user.id)
        if data_с is None:
            try:
                id = message.text.split()[2]
                if id.isdigit():
                    pass
                else:
                    await message.reply('‼️ Не хватает аргументов!\nПример:клан вступить id ')
                    return
            except:
                await message.reply('‼️ Не хватает аргументов!\nПример: клан вступить id ')
                return

            cursor.execute(
                f"SELECT clan_id FROM clans WHERE clan_id =?", (id,))
            if cursor.fetchone() != None:
                cursor.execute(
                    f"SELECT type_clan FROM clans WHERE clan_id =?", (id,))
                type_clan = cursor.fetchone()
                type_clan = int(type_clan[0])
                if type_clan == 1:
                    name = cursor.execute(
                        f"SELECT clan_name FROM clans WHERE clan_id=?", (id,))
                    name = cursor.fetchone()
                    name = name[0]

                    member = cursor.execute(
                        f"SELECT members FROM clans WHERE clan_id=?", (id,))
                    member = cursor.fetchone()
                    member = int(member[0])

                    if member > 0:
                        cursor.execute(
                            f'INSERT INTO clan VALUES (?, ?, ?, ?, ?);',
                            (user_id, user_name, "member", id, name))
                        cursor.execute(
                            f"UPDATE clans SET members={member+1} WHERE clan_id=?", (id,))
                        await message.reply(
                            f'🛡️ <a href="tg://user?id={user_id}">{user_name}</a>, вы вступили в клан',
                            parse_mode='html')
                        connect.commit()
                    if member == 0:
                        cursor.execute(
                            f'INSERT INTO clan VALUES (?, ?, ?, ?, ?);',
                            (user_id, user_name, "SOZD", id, name))
                        cursor.execute(
                            f"UPDATE clans SET members={member + 1} WHERE clan_id=?", (id,))
                        await message.reply(
                            f'🛡️ <a href="tg://user?id={user_id}">{user_name}</a>, вы вступили в клан\b‼️ Так как в клане было пусто вы теперь новый глава клана',
                            parse_mode='html')
                        connect.commit()
                else:
                    await message.reply(
                        f'🛡️ <a href="tg://user?id={user_id}">{user_name}</a> Клан закрыт',
                        parse_mode='html')
            else:
                await message.reply(f'‼️ <a href="tg://user?id={user_id}">{user_name}</a>такого  клана не существует',
                                    parse_mode='html')
        else:
            await message.reply(f'‼️ <a href="tg://user?id={user_id}">{user_name}</a>вы уже в клане',
                                parse_mode='html')
    if message.text.lower() in ["Клан покинуть", "клан покинуть"]:
        user_name = cursor.execute("SELECT user_name from users where user_id = ?",
                                   (message.from_user.id,))
        user_name = cursor.fetchone()
        user_name = user_name[0]
        user_id = message.from_user.id
        data_с = await get_clan(message.from_user.id)
        if data_с != None:
            status = cursor.execute(
                "SELECT status FROM clan WHERE user_id=?", (user_id,))
            status = cursor.fetchone()
            status = status[0]
            if status == "SOZD":

                clan_id = cursor.execute(
                    f"SELECT clan_id FROM clan WHERE user_id=?", (message.from_user.id,))
                clan_id = cursor.fetchone()
                clan_id = clan_id[0]
                member = cursor.execute(
                    f"SELECT members FROM clans WHERE clan_id=?", (clan_id,))
                member = cursor.fetchone()
                member = int(member[0])

                cursor.execute(
                    f"UPDATE clans SET members={member - 1} WHERE clan_id=?", (clan_id,))

                cursor.execute("DELETE FROM clan WHERE user_id= ?",
                               (message.from_user.id,))
                connect.commit()

                member = cursor.execute(
                    f"SELECT members FROM clans WHERE clan_id=?", (clan_id,))
                member = cursor.fetchone()
                member = int(member[0])
                if member > 0:
                    user_ids = cursor.execute(
                        "SELECT user_id FROM clan WHERE clan_id=?", (clan_id,))
                    user_ids = cursor.fetchall()
                    list = []

                    for user in user_ids:
                        list.append(f"{user[0]}")

                    random_index = random.randrange(len(list))
                    new_id = list[random_index]
                    user_name_new = cursor.execute("SELECT user_name from users where user_id = ?",
                                                   (new_id,))
                    user_name_new = cursor.fetchone()
                    user_name_new = user_name_new[0]
                    cursor.execute(
                        f"UPDATE clan SET status='SOZD' WHERE user_id={new_id} and clan_id={clan_id}")
                    await message.reply(f'‼️ <a href="tg://user?id={user_id}">{user_name}</a> вы больше не состоите в клане \n🆕 Новый глава клана:  <a href="tg://user?id={new_id}">{user_name_new}</a>({new_id}) ',
                                        parse_mode='html')
                    connect.commit()

                if member == 0:
                    await message.reply(
                        f'‼️ <a href="tg://user?id={user_id}">{user_name}</a> вы больше не состоите в клане ',
                        parse_mode='html')
            else:
                clan_id = cursor.execute(
                    f"SELECT clan_id FROM clan WHERE user_id=?", (message.from_user.id,))
                clan_id = cursor.fetchone()
                clan_id = clan_id[0]
                member = cursor.execute(
                    f"SELECT members FROM clans WHERE clan_id=?", (clan_id,))
                member = cursor.fetchone()
                member = int(member[0])

                cursor.execute(
                    f"UPDATE clans SET members={member - 1} WHERE clan_id=?", (clan_id,))

                cursor.execute("DELETE FROM clan WHERE user_id= ?",
                               (message.from_user.id,))
                connect.commit()
                await message.reply(
                    f'‼️ <a href="tg://user?id={user_id}">{user_name}</a> вы больше не состоите в клане ',
                    parse_mode='html')

        else:
            await message.reply(f'‼️ <a href="tg://user?id={user_id}">{user_name}</a> вы не состоите в клане',
                                parse_mode='html')
    if message.text.lower().startswith('клан повысить'):

        user_id = message.from_user.id
        user_name = cursor.execute("SELECT user_name from users where user_id = ?",
                                   (message.from_user.id,))
        user_name = cursor.fetchone()
        user_name = user_name[0]
        data_с = await get_clan(message.from_user.id)
        if data_с != None:
            try:
                user_kik = message.text.split()[2]
                if user_kik.isdigit():
                    pass
                else:
                    await message.reply('‼️ Не хватает аргументов!\nПример: Клан повысить id ')
                    return
            except:
                await message.reply('‼️ Не хватает аргументов!\nПример: Клан повысить id ')
                return

            cursor.execute("SELECT * FROM clan WHERE user_id=?", (user_kik,))
            if cursor.fetchone() != None:
                status = cursor.execute(
                    "SELECT status FROM clan WHERE user_id=?", (user_id,))
                status = cursor.fetchone()
                status = status[0]
                ruser_name = cursor.execute("SELECT user_name from users where user_id = ?",
                                            (user_kik,))
                ruser_name = cursor.fetchone()
                ruser_name = ruser_name[0]
                if status == "SOZD":
                    clan_id = cursor.execute(
                        f"SELECT clan_id FROM clan WHERE user_id=?", (user_kik,))
                    clan_id = cursor.fetchone()
                    clan_id = clan_id[0]
                    clan_id1 = cursor.execute(
                        f"SELECT clan_id FROM clan WHERE user_id=?", (user_id,))
                    clan_id1 = cursor.fetchone()
                    clan_id1 = clan_id1[0]
                    if clan_id1 == clan_id:
                        cursor.execute(
                            f"UPDATE clan SET status='soryk' WHERE user_id=?", (user_kik,))
                        await message.reply(
                            f'⏫️  <a href="tg://user?id={user_id}">{user_name}</a>, вы повысили статус игрока(<a href="tg://user?id={user_kik}">{ruser_name}</a>) до суроководителя !\n'
                            f'🛑 Будьте осторожны повышая ранг игрокам они могут управлять вашим кланом !',
                            parse_mode='html')
                    else:
                        await message.reply(
                            f'‼️ <a href="tg://user?id={user_id}">{user_name}</a> игрок не состоит в вашем клане',
                            parse_mode='html')
                else:
                    await message.reply(
                        f'‼️ <a href="tg://user?id={user_id}">{user_name}</a> Вы не создатель клана',
                        parse_mode='html')
            else:
                await message.reply(f'‼️ <a href="tg://user?id={user_id}">{user_name}</a> игрок не состоит в клане',
                                    parse_mode='html')
        else:
            await message.reply(f'‼️ <a href="tg://user?id={user_id}">{user_name}</a> вы не состоите в клане',
                                parse_mode='html')
    if message.text.lower().startswith('клан понизить'):

        user_id = message.from_user.id
        user_name = cursor.execute("SELECT user_name from users where user_id = ?",
                                   (message.from_user.id,))
        user_name = cursor.fetchone()
        user_name = user_name[0]
        data_с = await get_clan(message.from_user.id)
        if data_с != None:
            try:
                user_kik = message.text.split()[2]
                if user_kik.isdigit():
                    pass
                else:
                    await message.reply('‼️ Не хватает аргументов!\nПример: Клан понизить id ')
                    return
            except:
                await message.reply('‼️ Не хватает аргументов!\nПример: Клан понизить id ')
                return

            cursor.execute("SELECT * FROM clan WHERE user_id=?", (user_kik,))
            if cursor.fetchone() != None:
                status = cursor.execute(
                    "SELECT status FROM clan WHERE user_id=?", (user_id,))
                status = cursor.fetchone()
                status = status[0]
                ruser_name = cursor.execute("SELECT user_name from users where user_id = ?",
                                            (user_kik,))
                ruser_name = cursor.fetchone()
                ruser_name = ruser_name[0]
                if status == "SOZD":
                    clan_id = cursor.execute(
                        f"SELECT clan_id FROM clan WHERE user_id=?", (user_kik,))
                    clan_id = cursor.fetchone()
                    clan_id = clan_id[0]
                    clan_id1 = cursor.execute(
                        f"SELECT clan_id FROM clan WHERE user_id=?", (user_id,))
                    clan_id1 = cursor.fetchone()
                    clan_id1 = clan_id1[0]
                    if clan_id1 == clan_id:
                        cursor.execute(
                            f"UPDATE clan SET status='soryk' WHERE user_id=?", (user_kik,))
                        await message.reply(
                            f'⏬️  <a href="tg://user?id={user_id}">{user_name}</a> ,вы понизили статус игрока(<a href="tg://user?id={user_kik}">{ruser_name}</a>) до участника !', parse_mode='html')
                    else:
                        await message.reply(
                            f'‼️ <a href="tg://user?id={user_id}">{user_name}</a> игрок не состоит в вашем клане',
                            parse_mode='html')
                else:
                    await message.reply(
                        f'‼️ <a href="tg://user?id={user_id}">{user_name}</a> Вы не создатель клана',
                        parse_mode='html')
            else:
                await message.reply(f'‼️ <a href="tg://user?id={user_id}">{user_name}</a> игрок не состоит в клане',
                                    parse_mode='html')
        else:
            await message.reply(f'‼️ <a href="tg://user?id={user_id}">{user_name}</a> вы не состоите в клане',
                                parse_mode='html')

    if message.text.lower().startswith('клан кик'):

        user_id = message.from_user.id
        user_name = cursor.execute("SELECT user_name from users where user_id = ?",
                                   (message.from_user.id,))
        user_name = cursor.fetchone()
        user_name = user_name[0]
        data_с = await get_clan(message.from_user.id)
        if data_с != None:
            try:
                user_kik = message.text.split()[2]
                if user_kik.isdigit():
                    pass
                else:
                    await message.reply('‼️ Не хватает аргументов!\nПример: Клан кик id ')
                    return
            except:
                await message.reply('‼️ Не хватает аргументов!\nПример: Клан кик id ')
                return

            cursor.execute("SELECT * FROM clan WHERE user_id=?", (user_kik,))
            if cursor.fetchone() != None:
                status = cursor.execute(
                    "SELECT status FROM clan WHERE user_id=?", (user_id,))
                status = cursor.fetchone()
                status = status[0]
                if status == "SOZD" or status == "soryk":
                    clan_id = cursor.execute(
                        f"SELECT clan_id FROM clan WHERE user_id=?", (user_kik,))
                    clan_id = cursor.fetchone()
                    clan_id = clan_id[0]
                    clan_id1 = cursor.execute(
                        f"SELECT clan_id FROM clan WHERE user_id=?", (user_id,))
                    clan_id1 = cursor.fetchone()
                    clan_id1 = clan_id1[0]
                    if clan_id1 == clan_id:
                        rstatus = cursor.execute(
                            "SELECT status FROM clan WHERE user_id=?", (user_kik,))
                        rstatus = cursor.fetchone()
                        rstatus = rstatus[0]
                        if rstatus != "SOZD":
                            ruser_name = cursor.execute("SELECT user_name from users where user_id = ?",
                                                        (user_kik,))
                            ruser_name = cursor.fetchone()
                            ruser_name = ruser_name[0]

                            member = cursor.execute(
                                f"SELECT members FROM clans WHERE clan_id=?", (clan_id,))
                            member = cursor.fetchone()
                            member = int(member[0])
                            cursor.execute(
                                f"UPDATE clans SET members={member - 1} WHERE clan_id=?", (clan_id,))

                            cursor.execute(
                                "DELETE FROM clan WHERE user_id= ?", (user_kik,))
                            connect.commit()
                            await message.reply(f'⛔️ <a href="tg://user?id={user_id}">{user_name}</a> вы кикнули из клана игрока  <a href="tg://user?id={user_kik}">{ruser_name}</a>',
                                                parse_mode='html')
                        else:
                            await message.reply(
                                f'‼️ <a href="tg://user?id={user_id}">{user_name}</a> вы не можете кикнуть создателя',
                                parse_mode='html')
                    else:
                        await message.reply(
                            f'‼️ <a href="tg://user?id={user_id}">{user_name}</a> игрок не состоит в вашем клане',
                            parse_mode='html')
                else:
                    await message.reply(
                        f'‼️ <a href="tg://user?id={user_id}">{user_name}</a> выгонять из клана может только админы клана',
                        parse_mode='html')
            else:
                await message.reply(f'‼️ <a href="tg://user?id={user_id}">{user_name}</a> игрок не состоит в клане',
                                    parse_mode='html')
        else:
            await message.reply(f'‼️ <a href="tg://user?id={user_id}">{user_name}</a> вы не состоите в клане',
                                parse_mode='html')
    if message.text.lower().startswith('клан атака'):
        user_name = cursor.execute("SELECT user_name from users where user_id = ?",
                                   (message.from_user.id,))
        user_name = cursor.fetchone()
        user_name = user_name[0]
        user_id = message.from_user.id
        data_с = await get_clan(message.from_user.id)
        if data_с != None:
            clan_id1 = cursor.execute(
                f"SELECT clan_id FROM clan WHERE user_id=?", (user_id,))
            clan_id1 = cursor.fetchone()
            clan_id1 = clan_id1[0]
            status = cursor.execute(
                "SELECT status FROM clan WHERE user_id=?", (user_id,))
            status = cursor.fetchone()
            status = status[0]

            if status == "SOZD" or status == "soryk":
                try:
                    id_clan = message.text.split()[2]
                    if id_clan.isdigit():
                        pass
                    else:
                        await message.reply('‼️ Не хватает аргументов!\nПример:клан атака id ')
                        return
                except:
                    await message.reply('‼️ Не хватает аргументов!\nПример: Клан атака (id) ')
                    return
                cursor.execute(
                    f"SELECT clan_id FROM clans WHERE clan_id =?", (id_clan,))
                if cursor.fetchone() != None:
                    if clan_id1 != id_clan:
                        period = 43200
                        get = cursor.execute(
                            f"SELECT last_stavka FROM clans WHERE clan_id = ?", (clan_id1,)).fetchone()
                        get2 = int(get[0])
                        stavkatime = time.time() - float(get2)
                        if stavkatime >= period:
                            win = cursor.execute(
                                f"SELECT win FROM clans WHERE clan_id=?", (clan_id1,))
                            win = cursor.fetchone()
                            win = int(win[0])
                            lose = cursor.execute(
                                f"SELECT lose FROM clans WHERE clan_id=?", (clan_id1,))
                            lose = cursor.fetchone()
                            lose = int(lose[0])
                            win2 = cursor.execute(
                                f"SELECT win FROM clans WHERE clan_id=?", (id_clan,))
                            win2 = cursor.fetchone()
                            win2 = int(win2[0])
                            lose2 = cursor.execute(
                                f"SELECT lose FROM clans WHERE clan_id=?", (id_clan,))
                            lose2 = cursor.fetchone()
                            lose2 = int(lose2[0])
                            power = cursor.execute(
                                f"SELECT power FROM clans WHERE clan_id=?", (clan_id1,))
                            power = cursor.fetchone()
                            power = int(power[0])
                            power2 = cursor.execute(
                                f"SELECT power FROM clans WHERE clan_id=?", (id_clan,))
                            power2 = cursor.fetchone()
                            power2 = int(power2[0])
                            clan_name = cursor.execute(
                                f"SELECT clan_name FROM clans WHERE clan_id=?", (id_clan,))
                            clan_name = cursor.fetchone()
                            clan_name = clan_name[0]
                            if power2 > power:
                                cursor.execute(
                                    f"UPDATE clans SET power={power2-power} WHERE clan_id=?", (id_clan,))
                                cursor.execute(
                                    f"UPDATE clans SET win={win2 + 1} WHERE clan_id=?", (id_clan,))
                                cursor.execute(
                                    f"UPDATE clans SET lose={lose + 1} WHERE clan_id=?", (clan_id1,))
                                cursor.execute(
                                    f'UPDATE clans SET last_stavka = {time.time()} WHERE clan_id = ?', (clan_id1,))
                                connect.commit()
                                await message.reply(
                                    f"""
‼️ | <a href="tg://user?id={user_id}">{user_name}</a>, вы атакавали клан {clan_name}
📋 | Результат:
💀 | К сожелению вражеский клан оказался сильнее """, parse_mode='html')

                            elif power2 < power:
                                cursor.execute(
                                    f"UPDATE clans SET power={power - power2} WHERE clan_id=?", (clan_id1,))
                                cursor.execute(
                                    f"UPDATE clans SET win={win + 1} WHERE clan_id=?", (clan_id1,))
                                cursor.execute(
                                    f"UPDATE clans SET lose={lose2 + 1} WHERE clan_id=?", (id_clan,))
                                cursor.execute(
                                    f'UPDATE clans SET last_stavka = {time.time()} WHERE clan_id = ?', (clan_id1,))
                                connect.commit()
                                await message.reply(
                                    f"""
‼️ | <a href="tg://user?id={user_id}">{user_name}</a>, вы атакавали клан {clan_name}
📋 | Результат:
🏅 |  Поздравляю с победой над кланом {clan_name}""",
                                    parse_mode='html')
                            else:
                                cursor.execute(
                                    f"UPDATE clans SET power={0} WHERE clan_id=?", (clan_id1,))
                                cursor.execute(
                                    f"UPDATE clans SET power={0} WHERE clan_id=?", (id_clan,))
                                cursor.execute(
                                    f"UPDATE clans SET lose={lose2 + 1} WHERE clan_id=?", (clan_id1,))
                                cursor.execute(
                                    f"UPDATE clans SET lose={lose + 1} WHERE clan_id=?", (id_clan,))
                                cursor.execute(
                                    f'UPDATE clans SET last_stavka = {time.time()} WHERE clan_id = ?', (clan_id1,))
                                connect.commit()
                                await message.reply(
                                    f"""
‼️ | <a href="tg://user?id={user_id}">{user_name}</a>, вы атакавали клан {clan_name}
📋 | Результат:
💀 | Оба клана потерпели поражения """,
                                    parse_mode='html')
                        else:
                            await message.reply(
                                f'‼️ <a href="tg://user?id={user_id}">{user_name}</a> атаковать кланы можно раз в 12ч',
                                parse_mode='html')
                    else:
                        await message.reply(
                            f'‼️ <a href="tg://user?id={user_id}">{user_name}</a> вы не можете атаковать свой клан',
                            parse_mode='html')
                else:
                    await message.reply(
                        f'‼️ <a href="tg://user?id={user_id}">{user_name}</a> такого клана не существует',
                        parse_mode='html')
            else:
                await message.reply(
                    f'‼️ <a href="tg://user?id={user_id}">{user_name}</a> атакокланы может только создатель клана',
                    parse_mode='html')
        else:
            await message.reply(
                f'‼️ <a href="tg://user?id={user_id}">{user_name}</a> вы не состоите в клане',
                parse_mode='html')
    if message.text.lower().startswith('клан усилить'):
        user_name = cursor.execute("SELECT user_name from users where user_id = ?",
                                   (message.from_user.id,))
        user_name = cursor.fetchone()
        user_name = user_name[0]
        user_id = message.from_user.id
        data_с = await get_clan(message.from_user.id)
        if data_с != None:
            clan_id1 = cursor.execute(
                f"SELECT clan_id FROM clan WHERE user_id=?", (user_id,))
            clan_id1 = cursor.fetchone()
            clan_id1 = clan_id1[0]
            status = cursor.execute(
                "SELECT status FROM clan WHERE user_id=?", (user_id,))
            status = cursor.fetchone()
            status = status[0]
            balance = cursor.execute(
                "SELECT balance from users where user_id = ?", (message.from_user.id,))
            balance = cursor.fetchone()
            balance = int(balance[0])
            power = cursor.execute(
                f"SELECT power FROM clans WHERE clan_id=?", (clan_id1,))
            power = cursor.fetchone()
            power = int(power[0])
            if status == "SOZD" or status == "soryk":
                try:
                    summ = int(message.text.split()[2])
                except:
                    await message.reply('‼️ Не хватает аргументов!\nПример: Клан усилить (число) ')
                    return
                if summ > 0:
                    if balance >= summ*100_000_000_000:
                        summ3 = '{:,}'.format(summ).replace(',', '.')
                        cursor.execute(
                            f"UPDATE users SET balance={balance-summ*100_000} WHERE user_id={user_id}")
                        cursor.execute(
                            f"UPDATE clans SET power={power+summ} WHERE clan_id={clan_id1}")
                        await message.reply(
                            f'💰 <a href="tg://user?id={user_id}">{user_name}</a>, вы успешно усилили клан на: {summ3} 💪',
                            parse_mode='html')
                    else:
                        await message.reply(
                            f'💰 ️<a href="tg://user?id={user_id}">{user_name}</a>, недостаточно средств - 1 усилие = 100,000,000,000¢!',
                            parse_mode='html')
                else:
                    await message.reply(
                        f'‼️ <a href="tg://user?id={user_id}">{user_name}</a>, нельзя вводить отрицательные числа',
                        parse_mode='html')

            else:
                await message.reply(
                    f'‼️ <a href="tg://user?id={user_id}">{user_name}</a>, усилить клан может только админ клана',
                    parse_mode='html')
        else:
            await message.reply(
                f'‼️ <a href="tg://user?id={user_id}">{user_name}</a>,8 вы не состоите в клане',
                parse_mode='html')
    if message.text.lower().startswith('клан снять'):
        user_name = cursor.execute("SELECT user_name from users where user_id = ?",
                                   (message.from_user.id,))
        user_name = cursor.fetchone()
        user_name = user_name[0]
        user_id = message.from_user.id
        balance = cursor.execute(
            "SELECT balance from users where user_id = ?", (message.from_user.id,))
        balance = cursor.fetchone()
        balance = int(balance[0])
        clan_id1 = cursor.execute(
            f"SELECT clan_id FROM clan WHERE user_id=?", (user_id,))
        clan_id1 = cursor.fetchone()
        clan_id1 = clan_id1[0]
        kazna = cursor.execute(
            f"SELECT kazna FROM clans WHERE clan_id=?", (clan_id1,))
        kazna = cursor.fetchone()
        kazna = int(kazna[0])
        data_с = await get_clan(message.from_user.id)
        if data_с != None:
            try:
                su = msg.text.split()[2]
                su2 = (su).replace('к', '000')
                su3 = (su2).replace('м', '000000')
                su4 = (su3).replace('.', '')
                su5 = float(su4)
                summ = int(su5)

            except:
                await message.reply('‼️ Не хватает аргументов!\nПример: Казна снять сумма ')
                return
            if summ > 0:
                if kazna >= summ:
                    status = cursor.execute("SELECT status FROM clan WHERE user_id=? and clan_id=?",
                                            (user_id, clan_id1,))
                    status = cursor.fetchone()
                    status = status[0]
                    if status == "SOZD" or status == "soryk":
                        summ3 = '{:,}'.format(summ).replace(',', '.')
                        cursor.execute(f"UPDATE users SET balance={balance + summ} WHERE user_id=?",
                                       (message.from_user.id,))
                        cursor.execute(
                            f"UPDATE clans SET kazna={kazna - summ} WHERE clan_id=?", (clan_id1,))
                        await message.reply(
                            f'💰 ️ <a href="tg://user?id={user_id}">{user_name}</a> Вы сняли с казны сумму: {summ3}¢',
                            parse_mode='html')
                        connect.commit()
                    else:
                        await message.reply(
                            f'‼️ <a href="tg://user?id={user_id}">{user_name}</a> снимать деньги с казны может только админ клана',
                            parse_mode='html')
                else:
                    await message.reply(
                        f'💰 ️<a href="tg://user?id={user_id}">{user_name}</a> недостаточно средств',
                        parse_mode='html')
            else:
                await message.reply(
                    f'‼️ <a href="tg://user?id={user_id}">{user_name}</a> нельзя снять отрицательные числа',
                    parse_mode='html')
        else:
            await message.reply(f'‼️ <a href="tg://user?id={user_id}">{user_name}</a> вы не состоите в клане',
                                parse_mode='html')
    if message.text.lower().startswith('клан пополнить'):
        user_name = cursor.execute("SELECT user_name from users where user_id = ?",
                                   (message.from_user.id,))
        user_name = cursor.fetchone()
        user_name = user_name[0]
        user_id = message.from_user.id
        balance = cursor.execute(
            "SELECT balance from users where user_id = ?", (message.from_user.id,))
        balance = cursor.fetchone()
        balance = int(balance[0])
        clan_id1 = cursor.execute(
            f"SELECT clan_id FROM clan WHERE user_id=?", (user_id,))
        clan_id1 = cursor.fetchone()
        clan_id1 = clan_id1[0]
        kazna = cursor.execute(
            f"SELECT kazna FROM clans WHERE clan_id=?", (clan_id1,))
        kazna = cursor.fetchone()
        kazna = int(kazna[0])
        data_с = await get_clan(message.from_user.id)
        if data_с != None:
            try:
                su = msg.text.split()[2]
                su2 = (su).replace('к', '000')
                su3 = (su2).replace('м', '000000')
                su4 = (su3).replace('.', '')
                su5 = float(su4)
                summ = int(su5)

            except:
                await message.reply('‼️ Не хватает аргументов!\nПример: Казна пополнить сумма ')
                return
            if summ > 0:
                if balance >= summ:
                    summ3 = '{:,}'.format(summ).replace(',', '.')
                    cursor.execute(
                        f"UPDATE users SET balance={balance - summ} WHERE user_id=?", (message.from_user.id,))
                    cursor.execute(
                        f"UPDATE clans SET kazna={kazna + summ} WHERE clan_id=?", (clan_id1,))
                    await message.reply(
                        f'💰 <a href="tg://user?id={user_id}">{user_name}</a> Вы пополнили казну клана на сумму: {summ3}¢',
                        parse_mode='html')
                    connect.commit()

                else:
                    await message.reply(
                        f'‼️ <a href="tg://user?id={user_id}">{user_name}</a> недостаточно средств',
                        parse_mode='html')
            else:
                await message.reply(f'‼️ <a href="tg://user?id={user_id}">{user_name}</a> нельзя пополнить отрицательные числа',
                                    parse_mode='html')
        else:
            await message.reply(f'‼️ <a href="tg://user?id={user_id}">{user_name}</a> вы не состоите в клане',
                                parse_mode='html')
    if message.text.lower() in ["клан приватность"]:
        user_name = cursor.execute("SELECT user_name from users where user_id = ?",
                                   (message.from_user.id,))
        user_name = cursor.fetchone()
        user_name = user_name[0]
        user_id = message.from_user.id
        data_с = await get_clan(message.from_user.id)
        if data_с != None:
            clan_id = cursor.execute(
                f"SELECT clan_id FROM clan WHERE user_id=?", (message.from_user.id,))
            clan_id = cursor.fetchone()
            clan_id = clan_id[0]
            type_clan = cursor.execute(
                f"SELECT type_clan FROM clans WHERE clan_id=?", (clan_id,))
            type_clan = cursor.fetchone()
            type_clan = int(type_clan[0])
            status = cursor.execute(
                "SELECT status FROM clan WHERE user_id=? and clan_id=?", (user_id, clan_id,))
            status = cursor.fetchone()
            status = status[0]
            if status == "SOZD":
                if type_clan == 1:
                    cursor.execute(
                        f"UPDATE clans SET type_clan=0 WHERE clan_id=?", (clan_id,))
                    await message.reply(
                        f'🔒️ <a href="tg://user?id={user_id}">{user_name}</a>, вы закрыли клан',
                        parse_mode='html')
                    connect.commit()
                if type_clan == 0:
                    cursor.execute(
                        f"UPDATE clans SET type_clan=1 WHERE clan_id=?", (clan_id,))
                    await message.reply(
                        f'🔓️ <a href="tg://user?id={user_id}">{user_name}</a>, вы открыли клан',
                        parse_mode='html')
                    connect.commit()
            else:
                await message.reply(f'‼️ <a href="tg://user?id={user_id}">{user_name}</a> приватность менять может только создатель',
                                    parse_mode='html')
        else:
            await message.reply(f'‼️ <a href="tg://user?id={user_id}">{user_name}</a> вы не состоите в клане',
                                parse_mode='html')
    if message.text.lower() in ["мой клан", "клан"]:
        user_name = cursor.execute("SELECT user_name from users where user_id = ?",
                                   (message.from_user.id,))
        user_name = cursor.fetchone()
        user_name = user_name[0]
        user_id = message.from_user.id
        data_с = await get_clan(message.from_user.id)
        if data_с != None:
            clan_id = cursor.execute(
                f"SELECT clan_id FROM clan WHERE user_id=?", (message.from_user.id,))
            clan_id = cursor.fetchone()
            clan_id = clan_id[0]
            name = cursor.execute(
                f"SELECT clan_name FROM clans WHERE clan_id=?", (clan_id,))
            name = cursor.fetchone()
            name = name[0]
            member = cursor.execute(
                f"SELECT members FROM clans WHERE clan_id=?", (clan_id,))
            member = cursor.fetchone()
            member = int(member[0])
            kazna = cursor.execute(
                f"SELECT kazna FROM clans WHERE clan_id=?", (clan_id,))
            kazna = cursor.fetchone()
            kazna = int(kazna[0])
            type_clan = cursor.execute(
                f"SELECT type_clan FROM clans WHERE clan_id=?", (clan_id,))
            type_clan = cursor.fetchone()
            type_clan = int(type_clan[0])
            power = cursor.execute(
                f"SELECT power FROM clans WHERE clan_id=?", (clan_id,))
            power = cursor.fetchone()
            power = int(power[0])
            win = cursor.execute(
                f"SELECT win FROM clans WHERE clan_id=?", (clan_id,))
            win = cursor.fetchone()
            win = int(win[0])
            lose = cursor.execute(
                f"SELECT lose FROM clans WHERE clan_id=?", (clan_id,))
            lose = cursor.fetchone()
            lose = int(lose[0])
            status = cursor.execute("SELECT status FROM clan WHERE user_id=? and clan_id=?",
                                    (user_id, clan_id,))
            status = cursor.fetchone()
            status = status[0]
            if status == "SOZD":
                rang = '👑 Владелец клана'
            if status == "member":
                rang = '👤 Участник '
            if status == "soryk":
                rang = '👮 Соруководитель '
            if type_clan == 1:
                type = ' 🔓 Открытый'
            if type_clan == 0:
                type = '🔒 Закрытый'
            power2 = '{:,}'.format(power).replace(',', '.')
            win2 = '{:,}'.format(win).replace(',', '.')
            lose2 = '{:,}'.format(lose).replace(',', '.')
            summ3 = '{:,}'.format(kazna).replace(',', '.')
            sozd = cursor.execute(
                f"SELECT user_name FROM clan WHERE status='SOZD' and clan_id=?", (clan_id,))
            sozd = cursor.fetchone()
            sozd = sozd[0]
            await bot.send_message(message.chat.id, f"""
✅ Название клана: {name}
🤴 Создатель клана: {sozd}
🔶 Ранг в клане: {rang}
🆔 Айди клана: {clan_id}
⚔️ Тип клана: {type}
👥 Участников: {member}
💸 Казна клана: {summ3}¢

💪 Мощь: {power2}
🏆 Побед: {win2}
💀 Поражений: {lose2}

‼️ Для просмотра всех участников введите: Клан участники
""",
                                   parse_mode='html')
        else:
            await message.reply(f'‼️ <a href="tg://user?id={user_id}">{user_name}</a> вы не состоите в клане',
                                parse_mode='html')
    if message.text.lower() in ["клан участники", "клан игроки"]:
        data_с = await get_clan(message.from_user.id)
        user_name = cursor.execute("SELECT user_name from users where user_id = ?",
                                   (message.from_user.id,))
        user_name = cursor.fetchone()
        user_name = user_name[0]
        user_id = message.from_user.id
        if data_с != None:
            clan_id = cursor.execute(
                f"SELECT clan_id FROM clan WHERE user_id=?", (message.from_user.id,))
            clan_id = cursor.fetchone()
            clan_id = clan_id[0]
            user_names = cursor.execute(
                "SELECT * FROM clan WHERE clan_id=?", (clan_id,))
            user_names = cursor.fetchall()
            list = []
            list2 = []
            list3 = []
            for user in user_names:
                if user[2] == "SOZD":
                    list2.append(
                        f"[👑] <i><a href='tg://user?id={user[0]}'>{user[1]}</a></i>   | 🔍ID: <code>{user[0]}</code> ")
                elif user[2] == "soryk":
                    list3.append(
                        f"[👮] <i><a href='tg://user?id={user[0]}'>{user[1]}</a></i>   | 🔍ID: <code>{user[0]}</code> ")
                else:
                    list.append(
                        f"[👤] <i><a href='tg://user?id={user[0]}'>{user[1]}</a></i>   | 🔍ID: <code>{user[0]}</code> ")

            top = "\n".join(list)
            topa = "\n".join(list2)
            tops = "\n".join(list3)
            await message.reply(f'<a href="tg://user?id={user_id}">{user_name}</a> 👥 Участники :\n'+topa+"\n➖➖➖➖➖➖➖➖➖➖\n"+tops+"➖➖➖➖➖➖➖➖➖➖\n"+top,
                                parse_mode='html')
        else:
            await message.reply(f'‼️ <a href="tg://user?id={user_id}">{user_name}</a> вы не состоите в клане',
                                parse_mode='html')


###########################################ТОП###########################################
    if message.text.lower().startswith("топ"):
       list = cursor.execute(f"SELECT * FROM users ORDER BY rating DESC").fetchmany(10)
       top_list = []
       user_id = message.from_user.id
       chat_id = message.chat.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?", (message.from_user.id,)).fetchone()
       user_name = str(user_name[0])
       num = 0

       

       for user in list:
           if user[7] >= 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999:
              c6 = 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
           else:
              c6 = user[7]

           

           num += 1

           if num == 1:
              num2 = '1️⃣'
              num3 = ' <b>👑ТОПЕР👑</b> |'
           if num == 2:
              num2 = '2️⃣'
              num3 = ''
           if num == 3:
              num2 = '3️⃣'
              num3 = ''
           if num == 4:
              num2 = '4️⃣'
              num3 = ''
           if num == 5:
              num2 = '5️⃣'
              num3 = ''
           if num == 6:
              num2 = '6️⃣'
              num3 = ''
           if num == 7:
              num2 = '7️⃣'
              num3 = ''
           if num == 8:
              num2 = '8️⃣'
              num3 = ''
           if num == 9:
              num2 = '9️⃣'
              num3 = ''
           if num == 10:
              num2 = '🔟'
              num3 = ''
           c = Decimal(c6)
           c2 = '{:,}'.format(c).replace(',', '.')

           
           top_list.append(f"{num2} {user[1]} |{num3} {c2}👑(<code>{user[0]}</code>)")

       top = "\n".join(top_list)
       await bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_name}</a>, топ 10 игроков бота:\n➖➖➖➖➖➖➖➖➖➖➖\n" + top, parse_mode='html')


######################################################Привилегии \ Донат меню##############################################
    if message.text.lower().startswith("донат"):
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = user_name[0]
       user_id = message.from_user.id 

       donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?", (message.from_user.id,)).fetchone()
       donate_coins = int(donate_coins[0])
       donate_coins2 = '{:,}'.format(donate_coins)
       
       donate_yslov = InlineKeyboardMarkup(row_width=2)
       yslov = InlineKeyboardButton(text='✅ Соглашаюсь', callback_data='donat')
       donate_yslov.add(yslov)

       await bot.send_message(message.chat.id, f"""
<a href='tg://user?id={user_id}'>{user_name}</a> › 
❗ Пользовательское соглашение

⚠ При покупке или при нажатии кнопки с низу вы соглашаетесь со всеми правилами перечисленными ниже

1⃣ Вы должны следовать всем правилам игрового бота, иначе мы будем вынуждены обнулить ваш донат баланс.
2⃣ При покупке доната вернуть его невозможно, если вы приобрели то он навсегда.
3⃣ Если вы передали свои права другому игроку и он их вам не возвращает. То мы не можем вам вернуть ваши права, вы сами отвечаете за них.
       """, reply_markup=donate_yslov, parse_mode='html')


########################################### СЕМЬЯ СЕМЬИ ####################################
    

    if message.text.lower() == 'пригласить в семью':
      if not message.reply_to_message:
         await message.reply("❗️ Эта команда должна быть <b>ответом на сообщение</b>", parse_mode='html')
         return

      user_id = message.from_user.id
      reply_user_id = message.reply_to_message.from_user.id

      if reply_user_id == user_id:
         return await message.reply(f'❗️ Вы не можете пригласить <b>самого себя</b> в семью.', parse_mode='html')
      else:
         pass
      user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
      user_name = str(user_name[0])

      reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
      reply_user_name = str(reply_user_name[0])

      all_family = cursor.execute(f'SELECT owner_id from family').fetchall()
      all_family2 = []
      proverka_family = 0

      for all_owner_id in all_family:
         all_family2.append(all_owner_id[0])

      user_id_family = cursor.execute(f'SELECT user_id from user_family where user_id = {user_id}').fetchone()

      if user_id_family != None:
         rank_family = cursor.execute(f'SELECT rank from user_family where user_id = {user_id}').fetchone()
         rank_family = int(rank_family[0])  

         name_family = cursor.execute(f'SELECT family from user_family where user_id = {user_id}').fetchone()
         name_family = name_family[0]     
      else:
         proverka_family += 1

      if user_id in all_family2:
         rank_family = 3
         
         name_family = cursor.execute(f'SELECT name from family where owner_id = {user_id}').fetchone()
         name_family = name_family[0]     
      else:
         proverka_family += 1

      if proverka_family == 2:
         return await message.reply(f'❗️ Вы <b>не состоите</b> в семье  | Для просмотра команд перейдите в <code>Помощь</code>»Организации', parse_mode='html')
      else:
         pass
      
      if rank_family < 2:
         return await message.reply(f'❗️ Приглашать игроков в семью можно от <b>2 ранга</b>', parse_Mode='html')
      else:
         pass

      user1 = message.reply_to_message.from_user.id
      user2 = reply_user_name
      keyboard = types.InlineKeyboardMarkup()
      keyboard.add(types.InlineKeyboardButton(text="✅ Принять приглашение", callback_data=f"accept_{user1}:{user2}:{name_family}"))

      text = f'''
👶 <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>, вас приглашают в семью «<b>{name_family}</b>»
      '''

      await message.answer(text, reply_markup=keyboard, parse_mode='html')

    if message.text.startswith('cоздать семью') or message.text.startswith('Создать семью'):
       user_id = message.from_user.id
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
       user_name = str(user_name[0])

       all_family = cursor.execute(f'SELECT owner_id from family').fetchall()
       all_family2 = []
       
       for all_owner_id in all_family:
         all_family2.append(all_owner_id[0])
      
       if user_id in all_family2:
         return await message.reply(f'❗️У вас есть <b>своя семья.</b> Зачем вам ещё одна? | <code>Распустить семью</code> - удаление семьи ', parse_mode='html')
       else:
         pass

       user_id_family = cursor.execute(f'SELECT user_id from user_family where user_id = {user_id}').fetchone()

       if user_id_family != None:
         return await message.reply('❗️ Вы уже <b>состоите в семье</b> | напишите «<code>выйти с семьи</code>» - для выхода с вашей семьи',parse_mode='html')
       else:
         pass

       donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(message.from_user.id,)).fetchone()
       donate_coins = int(donate_coins[0])

       if donate_coins < cfg.cash_family:
         return await message.reply(f'❗️ <b>Недостаточно пончиков</b> | Стоимость: <b>{cfg.cash_family} пончиков</b> 🍩')
       else:
         pass
       
       name_family = message.text.split()[2:]
       name_family2 = ' '.join(name_family)
       full_name_family = (name_family2).replace(' ','').replace('🇷🇺', '').replace('Россия', 'россия').replace('россия', '')

       if len(full_name_family) < 4:
         return await message.reply('❗️ Название семьи должна быть больше <b>4 символов</b>', parse_Mode='html')
       elif len(full_name_family) > 35:
         return await message.reply(f'❗️ Название семьи должна быть меньше <b>35 символов</b>', parse_mode='html')
       else:
         pass

       all_family_name = cursor.execute('SELECT name from family').fetchall()
       all_family_name2 = []

       for all_family_name3 in all_family_name:
         all_family_name2.append(all_family_name3[0])
      
       if full_name_family in all_family_name2:
         return await message.reply(f'❗️ Семья с названием «<b>{full_name_family}</b>» уже существует', parse_mode='html')
       else:
         pass
       
       family_id = cursor.execute('SELECT id from family_id').fetchone()
       family_id = int(family_id[0])
       new_family_id = family_id + 1

       text = f'''
✅ Вы успешно создали семью «<b>{full_name_family}</b>»
       '''

       text2 = f'''
❕ Для просмотра своей семьи напишите <code>моя семья</code>
       '''
       time_family = time.time()
       opis = ''
       cursor.execute(f'UPDATE family_id SET id = {new_family_id}')
       cursor.execute("INSERT INTO family VALUES(?, ?, ?, ?, ?, ?, ?);",(full_name_family, user_id, user_name, new_family_id, 0, opis, time_family))
       connect.commit()
       await message.answer(text, parse_mode='html')
       await message.answer(text2, parse_mode='html')





    if message.text.lower() in ['моя семья', "семья"]:
      user_id = message.from_user.id
      user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
      user_name = str(user_name[0])

      all_family = cursor.execute(f'SELECT owner_id from family').fetchall()
      all_family2 = []
      proverka_family = 0
      for all_owner_id in all_family:
         all_family2.append(all_owner_id[0])

      user_id_family = cursor.execute(f'SELECT user_id from user_family where user_id = {user_id}').fetchone()

      if user_id_family != None:
         name_family = cursor.execute(f'SELECT family from user_family where user_id = {user_id}').fetchone()
         name_family = name_family[0]     
      else:
         proverka_family += 1

      if user_id in all_family2:
         name_family = cursor.execute(f'SELECT name from family where owner_id = {user_id}').fetchone()
         name_family = name_family[0]     
      else:
         proverka_family += 1

      if proverka_family == 2:
         return await message.reply(f'❗️ Вы <b>не состоите</b> в семье  | Для просмотра команд перейдите в <code>Помощь</code>»Организации', parse_mode='html')
      else:
         pass

      owner_name = cursor.execute(f'SELECT owner_name from family where name = "{name_family}"').fetchone()
      owner_name = owner_name[0]

      rank3 = cursor.execute(f'SELECT user_name from user_family where rank = {3} and family = "{name_family}"').fetchall()
      all_rank3 = []

      for user_rank3 in rank3:
         all_rank3.append(user_rank3[0])

      full_all_rank3 = ' '.join(all_rank3)

      if full_all_rank3 == '':
         full_all_rank3 = 'Отсутствуют 😕'
      else:
         pass

      rank2 = cursor.execute(f'SELECT user_name from user_family where rank = {2} and family = "{name_family}"').fetchall()
      all_rank2 = []

      for user_rank2 in rank2:
         all_rank2.append(user_rank2[0])

      full_all_rank2 = ' '.join(all_rank2)

      if full_all_rank2 == '':
         full_all_rank2 = 'Отсутствуют 😕'
      else:
         pass
      
      id_family = cursor.execute(f'SELECT id from family where name = "{name_family}"').fetchone()
      id_family = int(id_family[0])

      sqlite_select_query2 = f"SELECT * from user_family where family = '{name_family}'"
      cursor.execute(sqlite_select_query2)
      all_user_family = cursor.fetchall()

      balance_family = cursor.execute(f'SELECT balance from family where name = "{name_family}"').fetchone()
      balance_family = int(balance_family[0])

      opis_family = cursor.execute(f'SELECT opis from family where name = "{name_family}"').fetchone()
      opis_family = opis_family[0]
      
      if opis_family == '':
         opis_family = 'Пустое'
      else:
         pass

      text = f'''
Информация за семью «<b>{name_family}</b>» 👨‍👩‍👧‍👦
➖➖➖➖➖➖➖➖
🤵‍♂️ Основатель семьи: {owner_name}
👨‍💻 Заместитель (3 ранг): {full_all_rank3} 
🧑‍💼 Помощники (2 ранг): {full_all_rank2} 
➖➖➖➖➖➖➖➖
🔎 ID: <code>{id_family}</code>
👥 Игроков в семье: <b>{len(all_user_family)}</b>
💰 Мешок семьи: <code>{balance_family} с. монет</code>
💭 Описания семьи: <i>{opis_family}</i>
      '''
      await message.reply(text, parse_mode='html')






    if message.text.lower() == 'выйти с семьи':
      user_id = message.from_user.id
      user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
      user_name = str(user_name[0])

      all_family = cursor.execute(f'SELECT owner_id from family').fetchall()
      all_family2 = []
      proverka_family = 0

      for all_owner_id in all_family:
         all_family2.append(all_owner_id[0])

      user_id_family = cursor.execute(f'SELECT user_id from user_family where user_id = {user_id}').fetchone()

      if user_id_family != None:
         rank_family = cursor.execute(f'SELECT rank from user_family where user_id = {user_id}').fetchone()
         rank_family = int(rank_family[0])  

         status_owner_family = 'off'

         name_family = cursor.execute(f'SELECT family from user_family where user_id = {user_id}').fetchone()
         name_family = name_family[0]     
      else:
         proverka_family += 1

      if user_id in all_family2:
         rank_family = 3

         status_owner_family = 'on'
         
         name_family = cursor.execute(f'SELECT name from family where owner_id = {user_id}').fetchone()
         name_family = name_family[0]     
      else:
         proverka_family += 1

      if proverka_family == 2:
         return await message.reply(f'❗️ Вы <b>не состоите</b> в семье  | Для просмотра команд перейдите в <code>Помощь</code>»Организации', parse_mode='html')
      else:
         pass

      
      if status_owner_family == 'on':
         return await message.reply(f'❗️ Вы <b>владелец семьи</b>, вы не можете покинуть свою семью | Пропишите <code>Распустить семью</code> для её удаление', parse_mode='html')
      else:
         pass

      cursor.execute(f'DELETE from user_family where family = "{name_family}"')

      text = f'''
😧 Вы покинули семью «<b>{name_family}</b>» 
      '''

      await message.reply(text, parse_mode='html')

    if message.text.lower() == 'распустить семью':
      user_id = message.from_user.id
      user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
      user_name = str(user_name[0])

      all_family = cursor.execute(f'SELECT owner_id from family').fetchall()
      all_family2 = []
      proverka_family = 0

      for all_owner_id in all_family:
         all_family2.append(all_owner_id[0])

      user_id_family = cursor.execute(f'SELECT user_id from user_family where user_id = {user_id}').fetchone()

      if user_id_family != None:
         rank_family = cursor.execute(f'SELECT rank from user_family where user_id = {user_id}').fetchone()
         rank_family = int(rank_family[0])  

         status_owner_family = 'off'

         name_family = cursor.execute(f'SELECT family from user_family where user_id = {user_id}').fetchone()
         name_family = name_family[0]     
      else:
         proverka_family += 1

      if user_id in all_family2:
         rank_family = 3

         status_owner_family = 'on'
         
         name_family = cursor.execute(f'SELECT name from family where owner_id = {user_id}').fetchone()
         name_family = name_family[0]     
      else:
         proverka_family += 1

      if proverka_family == 2:
         return await message.reply(f'❗️ Вы <b>не состоите</b> в семье  | Для просмотра команд перейдите в <code>Помощь</code>»Организации', parse_mode='html')
      else:
         pass

      if status_owner_family == 'off':
         return await message.reply(f'❗️ Распустить семью может только <b>её владелец</b>', parse_mode='html')
      else:
         pass

      cursor.execute(f'DELETE from family where name = "{name_family}"')
      cursor.execute(f'DELETE from user_family where family = "{name_family}"')

      text = f'''
🥲 Вы успешно распустили семью «<b>{name_family}</b>»
      '''

      await message.reply(text, parse_mode='html')
    if message.text.startswith('+описание семьи'):
      user_id = message.from_user.id
      user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
      user_name = str(user_name[0])

      all_family = cursor.execute(f'SELECT owner_id from family').fetchall()
      all_family2 = []
      proverka_family = 0

      for all_owner_id in all_family:
         all_family2.append(all_owner_id[0])

      user_id_family = cursor.execute(f'SELECT user_id from user_family where user_id = {user_id}').fetchone()

      if user_id_family != None:
         rank_family = cursor.execute(f'SELECT rank from user_family where user_id = {user_id}').fetchone()
         rank_family = int(rank_family[0])  

         name_family5 = cursor.execute(f'SELECT family from user_family where user_id = {user_id}').fetchone()
         name_family5 = name_family5[0]     
      else:
         proverka_family += 1

      if user_id in all_family2:
         rank_family = 3
         
         name_family5 = cursor.execute(f'SELECT name from family where owner_id = {user_id}').fetchone()
         name_family5 = name_family5[0]     
      else:
         proverka_family += 1

      if proverka_family == 2:
         return await message.reply(f'❗️ Вы <b>не состоите</b> в семье  | Для просмотра команд перейдите в <code>Помощь</code>»Организации', parse_mode='html')
      else:
         pass

      if rank_family < 3:
         return await message.reply(f'❗️ Менять описание семьи можно только с <b>3 ранга</b>', parse_mode='html')
      else:
         pass

      new_opis = message.text[16:]
      
      if len(new_opis) > 150:
         return await message.reply('❗️ Описание должно быть не больше <b>150 символов</b>', parse_mode='html')
      else:
         pass
      
      cursor.execute(f'UPDATE family SET opis = "{new_opis}" where name = "{name_family5}"')

      text = f'''
✅ Вы <b>успешно</b> поменяли описание семьи
      '''

      await message.reply(text, parse_mode='html')





    if message.text.lower() == 'выгнать из семьи':
      if not message.reply_to_message:
         await message.reply("❗️ Эта команда должна быть <b>ответом на сообщение</b>", parse_mode='html')
         return

      user_id = message.from_user.id
      reply_user_id = message.reply_to_message.from_user.id

      if user_id == reply_user_id:
         return await message.reply('❗️ Вы не можете выгнать сами себя | Воспользуйтесь командой <code>Выйти с семьи</code>', parse_mode='html')
      else:
         pass

      user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
      user_name = str(user_name[0])

      reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
      reply_user_name = str(reply_user_name[0])

      all_family = cursor.execute(f'SELECT owner_id from family').fetchall()
      all_family2 = []
      proverka_family = 0

      for all_owner_id in all_family:
         all_family2.append(all_owner_id[0])

      user_id_family = cursor.execute(f'SELECT user_id from user_family where user_id = {user_id}').fetchone()

      if user_id_family != None:
         rank_family = cursor.execute(f'SELECT rank from user_family where user_id = {user_id}').fetchone()
         rank_family = int(rank_family[0])  

         status_owner_family = 'off'

         name_family = cursor.execute(f'SELECT family from user_family where user_id = {user_id}').fetchone()
         name_family = name_family[0]     
      else:
         proverka_family += 1

      if user_id in all_family2:
         rank_family = 3

         status_owner_family = 'on'

         name_family = cursor.execute(f'SELECT name from family where owner_id = {user_id}').fetchone()
         name_family = name_family[0]     
      else:
         proverka_family += 1

      if proverka_family == 2:
         return await message.reply(f'❗️ Вы <b>не состоите</b> в семье  | Для просмотра команд перейдите в <code>Помощь</code>»Организации', parse_mode='html')
      else:
         pass

      if rank_family < 3:
         return await message.reply(f'❗️ Выганять участников можно от <b>3 ранга</b>', parse_mode='html')
      else:
         pass
      
      reply_proverka_family = 0

      reply_user_id_family = cursor.execute(f'SELECT user_id from user_family where user_id = {reply_user_id}').fetchone()

      if reply_user_id_family != None:
         reply_rank_family = cursor.execute(f'SELECT rank from user_family where user_id = {reply_user_id}').fetchone()
         reply_rank_family = int(reply_rank_family[0])  

         reply_name_family = cursor.execute(f'SELECT family from user_family where user_id = {reply_user_id}').fetchone()
         reply_name_family = reply_name_family[0]     
      else:
         reply_proverka_family += 1

      if reply_user_id in all_family2:
         reply_rank_family = 3
         
         reply_name_family = cursor.execute(f'SELECT name from family where owner_id = {reply_user_id}').fetchone()
         reply_name_family = reply_name_family[0]     
      else:
         reply_proverka_family += 1

      if reply_proverka_family == 2:
         return await message.reply(f'❗️ Этот игрок не состоит в семьи')
      else:
         pass
      
      if reply_name_family != name_family:
         return await message.reply(f'❗️ Этот игрок состоит не в вашем семьи')
      else:
         pass


      if reply_rank_family == 3:
         if status_owner_family == 'on':
            pass
         else:
            return await message.reply(f'❗️ Вы не можете выгнать человека с <b>3 рангом</b> | <i>Под силу только владельцу семьи</i>', parse_mode='html')
      else:
         pass

      cursor.execute(f'DELETE from user_family where user_id = {reply_user_id}')
      connect.commit()

      text = f'''
👀 Вы выгнали <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a> с семьи «<b>{name_family}</b>»
      '''

      await message.reply(text, parse_mode='html')


    if message.text.lower() == '+ранг семьи':
      if not message.reply_to_message:
         await message.reply("❗️ Эта команда должна быть <b>ответом на сообщение</b>", parse_mode='html')
         return

      user_id = message.from_user.id
      reply_user_id = message.reply_to_message.from_user.id

      if user_id == reply_user_id:
         return await message.reply('❗️ Вы не можете повысить сам себе ранг')
      else:
         pass

      user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
      user_name = str(user_name[0])

      reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
      reply_user_name = str(reply_user_name[0])

      all_family = cursor.execute(f'SELECT owner_id from family').fetchall()
      all_family2 = []
      proverka_family = 0

      for all_owner_id in all_family:
         all_family2.append(all_owner_id[0])

      user_id_family = cursor.execute(f'SELECT user_id from user_family where user_id = {user_id}').fetchone()

      if user_id_family != None:
         rank_family = cursor.execute(f'SELECT rank from user_family where user_id = {user_id}').fetchone()
         rank_family = int(rank_family[0])  

         status_owner_family = 'off'

         name_family = cursor.execute(f'SELECT family from user_family where user_id = {user_id}').fetchone()
         name_family = name_family[0]     
      else:
         proverka_family += 1

      if user_id in all_family2:
         rank_family = 3

         status_owner_family = 'on'

         name_family = cursor.execute(f'SELECT name from family where owner_id = {user_id}').fetchone()
         name_family = name_family[0]     
      else:
         proverka_family += 1

      if proverka_family == 2:
         return await message.reply(f'❗️ Вы <b>не состоите</b> в семье  | Для просмотра команд перейдите в <code>Помощь</code>»Организации', parse_mode='html')
      else:
         pass

      if rank_family < 3:
         return await message.reply(f'❗️ Повышать ранг в семье можно от <b>3 ранга</b>', parse_mode='html')
      else:
         pass
      
      reply_proverka_family = 0

      reply_user_id_family = cursor.execute(f'SELECT user_id from user_family where user_id = {reply_user_id}').fetchone()

      if reply_user_id_family != None:
         reply_rank_family = cursor.execute(f'SELECT rank from user_family where user_id = {reply_user_id}').fetchone()
         reply_rank_family = int(reply_rank_family[0])  

         reply_name_family = cursor.execute(f'SELECT family from user_family where user_id = {reply_user_id}').fetchone()
         reply_name_family = reply_name_family[0]     
      else:
         reply_proverka_family += 1

      if reply_user_id in all_family2:
         reply_rank_family = 3
         
         reply_name_family = cursor.execute(f'SELECT name from family where owner_id = {reply_user_id}').fetchone()
         reply_name_family = reply_name_family[0]     
      else:
         reply_proverka_family += 1

      if reply_proverka_family == 2:
         return await message.reply(f'❗️ Этот игрок не состоит в семьи')
      else:
         pass
      
      if reply_name_family != name_family:
         return await message.reply(f'❗️ Этот игрок состоит не в вашем семьи')
      else:
         pass

      if reply_rank_family == 3:
         return await message.reply(f'❗️ У данного игрока максимальный ранг', parse_mode='html')
      else:
         pass
      

      cursor.execute(f'UPDATE user_family SET rank = {reply_rank_family + 1} WHERE user_id = {reply_user_id}')
      connect.commit()

      text = f'''
🔼 Вы повысили на 1 ранг игрока <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>
      '''
      await message.reply(text, parse_mode='html')







    if message.text.lower() == '-ранг семьи':
      if not message.reply_to_message:
         await message.reply("❗️ Эта команда должна быть <b>ответом на сообщение</b>", parse_mode='html')
         return

      user_id = message.from_user.id
      reply_user_id = message.reply_to_message.from_user.id

      if user_id == reply_user_id:
         return await message.reply('❗️ Вы не можете понизить сам себе ранг')
      else:
         pass

      user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
      user_name = str(user_name[0])

      reply_user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.reply_to_message.from_user.id,)).fetchone()
      reply_user_name = str(reply_user_name[0])

      all_family = cursor.execute(f'SELECT owner_id from family').fetchall()
      all_family2 = []
      proverka_family = 0

      for all_owner_id in all_family:
         all_family2.append(all_owner_id[0])

      user_id_family = cursor.execute(f'SELECT user_id from user_family where user_id = {user_id}').fetchone()

      if user_id_family != None:
         rank_family = cursor.execute(f'SELECT rank from user_family where user_id = {user_id}').fetchone()
         rank_family = int(rank_family[0])  

         status_owner_family = 'off'

         name_family = cursor.execute(f'SELECT family from user_family where user_id = {user_id}').fetchone()
         name_family = name_family[0]     
      else:
         proverka_family += 1

      if user_id in all_family2:
         rank_family = 3

         status_owner_family = 'on'

         name_family = cursor.execute(f'SELECT name from family where owner_id = {user_id}').fetchone()
         name_family = name_family[0]     
      else:
         proverka_family += 1

      if proverka_family == 2:
         return await message.reply(f'❗️ Вы <b>не состоите</b> в семье  | Для просмотра команд перейдите в <code>Помощь</code>»Организации', parse_mode='html')
      else:
         pass

      if rank_family < 3:
         return await message.reply(f'❗️ Понижать ранг в семье можно от <b>3 ранга</b>', parse_mode='html')
      else:
         pass
      
      reply_proverka_family = 0

      reply_user_id_family = cursor.execute(f'SELECT user_id from user_family where user_id = {reply_user_id}').fetchone()

      if reply_user_id_family != None:
         reply_rank_family = cursor.execute(f'SELECT rank from user_family where user_id = {reply_user_id}').fetchone()
         reply_rank_family = int(reply_rank_family[0])  

         reply_name_family = cursor.execute(f'SELECT family from user_family where user_id = {reply_user_id}').fetchone()
         reply_name_family = reply_name_family[0]     
      else:
         reply_proverka_family += 1

      if reply_user_id in all_family2:
         reply_rank_family = 3
         
         reply_name_family = cursor.execute(f'SELECT name from family where owner_id = {reply_user_id}').fetchone()
         reply_name_family = reply_name_family[0]     
      else:
         reply_proverka_family += 1

      if reply_proverka_family == 2:
         return await message.reply(f'❗️ Этот игрок не состоит в семьи')
      else:
         pass
      
      if reply_name_family != name_family:
         return await message.reply(f'❗️ Этот игрок состоит не в вашем семьи')
      else:
         pass

      if reply_rank_family == 3:
         if status_owner_family == 'on':
            pass
         else:
            return await message.reply(f'❗️ Вы не можете понизить человека с <b>3 рангом</b> | <i>Под силу только владельцу семьи</i>', parse_mode='html')
      else:
         pass
      
      if reply_rank_family == 1:
         return await message.reply(f'❗️ У данного игрока и так минимальный ранг.')
      else:
         pass

      cursor.execute(f'UPDATE user_family SET rank = {reply_rank_family - 1} WHERE user_id = {reply_user_id}')
      connect.commit()

      text = f'''
🔽 Вы понизили на 1 ранг игрока <a href='tg://user?id={reply_user_id}'>{reply_user_name}</a>
      '''
      await message.reply(text, parse_mode='html')








    if message.text.startswith('Купить монеты') or message.text.startswith('купить монеты'):
      user_id = message.from_user.id
      user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
      user_name = str(user_name[0])

      all_family = cursor.execute(f'SELECT owner_id from family').fetchall()
      all_family2 = []
      proverka_family = 0

      for all_owner_id in all_family:
         all_family2.append(all_owner_id[0])

      user_id_family = cursor.execute(f'SELECT user_id from user_family where user_id = {user_id}').fetchone()

      if user_id_family != None:
         rank_family = cursor.execute(f'SELECT rank from user_family where user_id = {user_id}').fetchone()
         rank_family = int(rank_family[0])  

         name_family = cursor.execute(f'SELECT family from user_family where user_id = {user_id}').fetchone()
         name_family = name_family[0]     
      else:
         proverka_family += 1

      if user_id in all_family2:
         rank_family = 3
         
         name_family = cursor.execute(f'SELECT name from family where owner_id = {user_id}').fetchone()
         name_family = name_family[0]     
      else:
         proverka_family += 1

      if proverka_family == 2:
         return await message.reply(f'❗️ Вы <b>не состоите</b> в семье  | Для просмотра команд перейдите в <code>Помощь</code>»Организации', parse_mode='html')
      else:
         pass

      reput = cursor.execute("SELECT reput from reput where user_id = ?",(message.from_user.id,)).fetchone()
      reput = int(reput[0])

      su = msg.text.split()[2]
      su2 = (su).replace(' ', '').replace('k', '000').replace('е','e').replace('к', '000').replace(',', '').replace('.', '')
      su3 = float(su2)
      summ = int(su3)

      summ2 = '{:,}'.format(summ).replace(',', '.')
      
      if summ < 10:
         return await message.reply(f'❗️ Можно покупать только от <code>10</code> <b>семейных монет</b>', parse_mode='html')
      else:
         pass

      if summ > reput:
         return await message.reply(f'❗️ У вас недостаточно <b>репутации</b> | <i>1 с. монета = 1 репутация</i>', parse_mode='html')
      else:
         pass

      if summ <= 0:
         return await message.reply(f'❗️ Сумма не должна быть отрицательным число <b>[0 и меньше]</b>', parse_mode='html')
      else:
         pass
      
      balance_family = cursor.execute(f'SELECT balance from family where name = "{name_family}"').fetchone()
      balance_family = balance_family[0]

      cursor.execute(f'UPDATE family SET balance = {balance_family + summ} WHERE name = "{name_family}"')
      cursor.execute(f'UPDATE reput SET reput = {reput - summ} WHERE user_id = "{user_id}"')
      connect.commit()

      text = f'''
💰 Вы положили в семейный мешок <code>{summ2}</code> семейный монет
      '''

      await message.reply(text, parse_mode='html')









    if message.text.startswith('+название семьи'):
      user_id = message.from_user.id
      user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
      user_name = str(user_name[0])

      all_family = cursor.execute(f'SELECT owner_id from family').fetchall()
      all_family2 = []
      proverka_family = 0

      for all_owner_id in all_family:
         all_family2.append(all_owner_id[0])

      user_id_family = cursor.execute(f'SELECT user_id from user_family where user_id = {user_id}').fetchone()

      if user_id_family != None:
         rank_family = cursor.execute(f'SELECT rank from user_family where user_id = {user_id}').fetchone()
         rank_family = int(rank_family[0])  

         name_family5 = cursor.execute(f'SELECT family from user_family where user_id = {user_id}').fetchone()
         name_family5 = name_family5[0]     
      else:
         proverka_family += 1

      if user_id in all_family2:
         rank_family = 3
         
         name_family5 = cursor.execute(f'SELECT name from family where owner_id = {user_id}').fetchone()
         name_family5 = name_family5[0]     
      else:
         proverka_family += 1

      if proverka_family == 2:
         return await message.reply(f'❗️ Вы <b>не состоите</b> в семье  | Для просмотра команд перейдите в <code>Помощь»Организации»семьи</code>', parse_mode='html')
      else:
         pass

      if rank_family < 3:
         return await message.reply(f'❗️ Менять название семьи можно только с <b>3 ранга</b>', parse_mode='html')
      else:
         pass

      user_status = cursor.execute("SELECT user_status from users where user_id = ?",(message.from_user.id,)).fetchone()
      user_status = user_status[0]

      if user_status in ['Helper_Admin', 'Owner']:
         period = 1
      else:
         period = 604800 #7d

      get = cursor.execute(f'SELECT time_name FROM family WHERE name = "{name_family5}"').fetchone()
      last_stavka = f"{int(get[0])}"
      stavkatime = time.time() - float(last_stavka)

      if stavkatime < period:
         times2 = time.localtime(float(get[0]))
         print(times2)

         if times2.tm_mday <= 9:
            tm_mday2 = 0
         else:
            tm_mday2 = ''
         
         if times2.tm_mon <= 9:
            tm_mon2 = 0
         else:
            tm_mon2 = ''

         if times2.tm_hour <= 9:
            tm_hour2 = 0
         else:
            tm_hour2 = ''

         if times2.tm_min <= 9:
            tm_min2 = 0
         else:
            tm_min2 = ''

         full_times2 = f'{tm_mday2}{times2.tm_mday}.{tm_mon2}{times2.tm_mon}.{times2.tm_year} в {tm_hour2}{times2.tm_hour}:{tm_min2}{times2.tm_min}'

         return await message.reply(f'❗️ Менять название семьи, можно раз в <b>7 дней</b> | Последнее изменение название было <code>{full_times2}</code>', parse_mode='html')
      else:
         pass

      name_family = message.text.split()[2:]
      name_family2 = ' '.join(name_family)
      full_name_family = (name_family2).replace(' ','').replace('🇷🇺', '').replace('Россия', 'россия').replace('россия', '')

      if len(full_name_family) < 4:
         return await message.reply('❗️ Название семьи должна быть больше <b>4 символов</b>', parse_Mode='html')
      elif len(full_name_family) > 35:
         return await message.reply(f'❗️ Название семьи должна быть меньше <b>35 символов</b>', parse_mode='html')
      else:
         pass

      all_family_name = cursor.execute('SELECT name from family').fetchall()
      all_family_name2 = []

      for all_family_name3 in all_family_name:
         all_family_name2.append(all_family_name3[0])
   
      if full_name_family in all_family_name2:
         return await message.reply(f'❗️ Семья с названием «<b>{full_name_family}</b>» уже существует', parse_mode='html')
      else:
         pass

      cursor.execute(f'UPDATE family SET name = "{full_name_family}" where name = "{name_family5}"')

      sqlite_select_query27 = f"SELECT * from user_family where family = '{name_family5}'"
      cursor.execute(sqlite_select_query27)
      full_user_id_family_update = cursor.fetchall()

      for update_name_family_user_id in full_user_id_family_update:
         print(update_name_family_user_id[1])
         cursor.execute(f'UPDATE user_family SET family = "{full_name_family}" where user_id = "{update_name_family_user_id[1]}"')
      connect.commit()

      text = f'''
✅ Вы успешно изменили название семьи с <b>{name_family5}</b> на <b>{full_name_family}</b>
      '''

      await message.reply(text, parse_mode='html')


#############################################АВАТАРКИ############################################
    if message.text.lower().startswith("ава"):
      user_id = message.from_user.id
      user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
      user_name = str(user_name[0])
      
      photo_id = cursor.execute("SELECT photo from photo_id where user_id = ?",(message.from_user.id,)).fetchone()
      photo_id = int(photo_id[0])
      
      if photo:
      	await bot.send_message(message.chat.id, f"""🌌 У вас нету аватарки""", reply_markup=ustanovka, parse_mode='html')


#############################################КНОПКИ############################################
@dp.callback_query_handler(text='ustanovka1')
async def photo_register(message, state=FSMContext):

    try:
        file_id = message.photo[-1].file_id
    except:
        return await message.answer('Отправьте фотографию. Эта фотография будет использоваться как лицо вашего баланса')
        
    await register_photo_id(message.from_user.id, file_id)
    await state.finish()

    await message.answer('<b>Вы успешно поставили аву на балансе.</b>', parse_mode='html')


@dp.callback_query_handler(lambda call: call.data.startswith('accept_'))
async def priglashenie_callback(call: types.CallbackQuery):

   user1, user2, name_family = call.data.replace('accept_', '', 1).split(':')
   print(call.from_user.id, user1)
   
   if int(call.from_user.id) == int(user1):
      pass
   else:
      return await call.answer('Приглашение не для тебя ❗️')

   user_id = call.from_user.id
   user_name = cursor.execute("SELECT user_name from users where user_id = ?",(call.from_user.id,)).fetchone()
   user_name = str(user_name[0])

   all_family = cursor.execute(f'SELECT owner_id from family').fetchall()
   all_family2 = []
   
   for all_owner_id in all_family:
      all_family2.append(all_owner_id[0])

   if user_id in all_family2:
      return await call.message.answer(f'❗️У вас есть <b>своя семья.</b> Зачем вам ещё одна? | <code>Распустить семью</code> - удаление семьи ', parse_mode='html')
   else:
      pass

   user_id_family = cursor.execute(f'SELECT user_id from user_family where user_id = {user_id}').fetchone()

   if user_id_family != None:
      return await call.message.answer('❗️ Вы уже <b>состоите в семье</b> | напишите «<code>выйти с семьи</code>» - для выхода с вашей семьи',parse_mode='html')
   else:
      pass

   text = f'''
✅ <a href='tg://user?id={user1}'>{user2}</a>, вы приняли приглашение в семью «<b>{name_family}</b>». Вы теперь состоите в семье
   '''

   text2 = f'''
❗️ В вашу семью «<b>{name_family}</b>» вступил <a href='tg://user?id={user1}'>{user2}</a>
   '''
   owner_id_family = cursor.execute(f"SELECT owner_id from family where name = \"{name_family}\"").fetchone()
   owner_id_family = owner_id_family[0]

   cursor.execute("INSERT INTO user_family VALUES(?, ?, ?, ?);",(user2, user1, name_family, 1))
   await call.message.bot.send_message(owner_id_family, text2, parse_mode='html')
   await call.message.answer(text, parse_mode='html')


@dp.callback_query_handler(text='valut1')
async def craft_resurs3(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    
    balance = cursor.execute("SELECT balance from users where user_id = ?",(callback.from_user.id,)).fetchone()
    balance = int(balance[0])
    
    user_status = cursor.execute("SELECT user_status from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_status = str(user_status[0])
    
    donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(callback.from_user.id,)).fetchone()
    donate_coins = int(donate_coins[0])
    
    help_back = InlineKeyboardMarkup(row_width=1)
    help_back2 = InlineKeyboardButton(text='🔙 Назад', callback_data='valut')
    help_back.add(help_back2)
    
    if donate_coins >= 120:
       await callback.message.edit_text(f"""✅ | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно купили 20е12 💰
Спасибо за покупку Я очень рад""", reply_markup=help_back, parse_mode='html')
       cursor.execute(f'UPDATE users SET balance = {balance + 20000000000000} WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET donate_coins = {donate_coins - 120} WHERE user_id = {user_id}')
       connect.commit()
       return 
    else:
         await bot.answer_callback_query(callback.id, show_alert=False, text=f"🆘 Ошибка! У вас нехватает пончиков 🍩")
         

@dp.callback_query_handler(text='valut2')
async def craft_resurs3(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    
    balance = cursor.execute("SELECT balance from users where user_id = ?",(callback.from_user.id,)).fetchone()
    balance = int(balance[0])
    
    user_status = cursor.execute("SELECT user_status from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_status = str(user_status[0])
    
    donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(callback.from_user.id,)).fetchone()
    donate_coins = int(donate_coins[0])
    
    help_back = InlineKeyboardMarkup(row_width=1)
    help_back2 = InlineKeyboardButton(text='🔙 Назад', callback_data='valut')
    help_back.add(help_back2)
    
    if donate_coins >= 220:
       await callback.message.edit_text(f"""✅ | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно купили 20е18 💰
Спасибо за покупку Я очень рад""", reply_markup=help_back, parse_mode='html')
       cursor.execute(f'UPDATE users SET balance = {balance + 20000000000000000000} WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET donate_coins = {donate_coins - 220} WHERE user_id = {user_id}')
       connect.commit()
       return 
    else:
         await bot.answer_callback_query(callback.id, show_alert=False, text=f"🆘 Ошибка! У вас нехватает пончиков 🍩")


@dp.callback_query_handler(text='valut3')
async def craft_resurs3(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    
    balance = cursor.execute("SELECT balance from users where user_id = ?",(callback.from_user.id,)).fetchone()
    balance = int(balance[0])
    
    user_status = cursor.execute("SELECT user_status from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_status = str(user_status[0])
    
    donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(callback.from_user.id,)).fetchone()
    donate_coins = int(donate_coins[0])
    
    help_back = InlineKeyboardMarkup(row_width=1)
    help_back2 = InlineKeyboardButton(text='🔙 Назад', callback_data='valut')
    help_back.add(help_back2)
    
    if donate_coins >= 310:
       await callback.message.edit_text(f"""✅ | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно купили 20е27 💰
Спасибо за покупку Я очень рад""", reply_markup=help_back, parse_mode='html')
       cursor.execute(f'UPDATE users SET balance = {balance + 20000000000000000000000000000} WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET donate_coins = {donate_coins - 310} WHERE user_id = {user_id}')
       connect.commit()
       return 
    else:
         await bot.answer_callback_query(callback.id, show_alert=False, text=f"🆘 Ошибка! У вас нехватает пончиков 🍩")
         

@dp.callback_query_handler(text='valut4')
async def craft_resurs3(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    
    balance = cursor.execute("SELECT balance from users where user_id = ?",(callback.from_user.id,)).fetchone()
    balance = int(balance[0])
    
    user_status = cursor.execute("SELECT user_status from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_status = str(user_status[0])
    
    donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(callback.from_user.id,)).fetchone()
    donate_coins = int(donate_coins[0])
    
    help_back = InlineKeyboardMarkup(row_width=1)
    help_back2 = InlineKeyboardButton(text='🔙 Назад', callback_data='valut')
    help_back.add(help_back2)
    
    if donate_coins >= 420:
       await callback.message.edit_text(f"""✅ | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно купили 20е36 💰
Спасибо за покупку Я очень рад""", reply_markup=help_back, parse_mode='html')
       cursor.execute(f'UPDATE users SET balance = {balance + 20000000000000000000000000000000000000} WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET donate_coins = {donate_coins - 420} WHERE user_id = {user_id}')
       connect.commit()
       return 
    else:
         await bot.answer_callback_query(callback.id, show_alert=False, text=f"🆘 Ошибка! У вас нехватает пончиков 🍩")
         
         
@dp.callback_query_handler(text='valut5')
async def craft_resurs3(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    
    balance = cursor.execute("SELECT balance from users where user_id = ?",(callback.from_user.id,)).fetchone()
    balance = int(balance[0])
    
    user_status = cursor.execute("SELECT user_status from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_status = str(user_status[0])
    
    donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(callback.from_user.id,)).fetchone()
    donate_coins = int(donate_coins[0])
    
    help_back = InlineKeyboardMarkup(row_width=1)
    help_back2 = InlineKeyboardButton(text='🔙 Назад', callback_data='valut')
    help_back.add(help_back2)
    
    if donate_coins >= 550:
       await callback.message.edit_text(f"""✅ | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно купили 20е48 💰
Спасибо за покупку Я очень рад""", reply_markup=help_back, parse_mode='html')
       cursor.execute(f'UPDATE users SET balance = {balance + 20000000000000000000000000000000000000000000000000} WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET donate_coins = {donate_coins - 550} WHERE user_id = {user_id}')
       connect.commit()
       return 
    else:
         await bot.answer_callback_query(callback.id, show_alert=False, text=f"🆘 Ошибка! У вас нехватает пончиков 🍩")
         
         
@dp.callback_query_handler(text='valut6')
async def craft_resurs3(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    
    balance = cursor.execute("SELECT balance from users where user_id = ?",(callback.from_user.id,)).fetchone()
    balance = int(balance[0])
    
    user_status = cursor.execute("SELECT user_status from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_status = str(user_status[0])
    
    donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(callback.from_user.id,)).fetchone()
    donate_coins = int(donate_coins[0])
    
    help_back = InlineKeyboardMarkup(row_width=1)
    help_back2 = InlineKeyboardButton(text='🔙 Назад', callback_data='valut')
    help_back.add(help_back2)
    
    if donate_coins >= 780:
       await callback.message.edit_text(f"""✅ | <a href='tg://user?id={user_id}'>{user_name}</a>, вы успешно купили 20е57 💰
Спасибо за покупку Я очень рад""", reply_markup=help_back, parse_mode='html')
       cursor.execute(f'UPDATE users SET balance = {balance + 20000000000000000000000000000000000000000000000000} WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET donate_coins = {donate_coins - 780} WHERE user_id = {user_id}')
       connect.commit()
       return 
    else:
         await bot.answer_callback_query(callback.id, show_alert=False, text=f"🆘 Ошибка! У вас нехватает пончиков 🍩")


@dp.callback_query_handler(text='valut')
async def craft_resurs3(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    
    donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(callback.from_user.id,)).fetchone()
    donate_coins = int(donate_coins[0])
    donate_coins2 = '{:,}'.format(donate_coins)
    
    valut = InlineKeyboardMarkup(row_width=3)
    valut1 = InlineKeyboardButton(text='💰 20е12', callback_data='valut1')
    valut2 = InlineKeyboardButton(text='💰 20е18', callback_data='valut2')
    valut3 = InlineKeyboardButton(text='💰 20е27', callback_data='valut3')
    valut4 = InlineKeyboardButton(text='💰 20е36', callback_data='valut4')
    valut5 = InlineKeyboardButton(text='💰 20е48', callback_data='valut5')
    valut6 = InlineKeyboardButton(text='💰 20е57', callback_data='valut6')
    help_back2 = InlineKeyboardButton(text='🔙 Назад', callback_data='donat')
    valut.add(valut1, valut2, valut3, valut4, valut5, valut6, help_back2)
    
    await callback.message.edit_text(f"""<a href='tg://user?id={user_id}'>{user_name}</a> › вот данные за игровую валюту 💰
➖➖➖➖➖➖➖➖➖➖➖➖
❗️ Появились проблемы с покупкой валюты? обращайтесь к {cfg.owner}    
➖➖➖➖➖➖➖➖➖➖➖➖    
🍩 Пончиков: <code>{donate_coins2}</code>    
➖➖➖➖➖➖➖➖➖➖➖➖
<b>💰 Валюта:
💰 20е12 | 120 🍩
💰 20е18 | 220 🍩
💰 20е27 | 310 🍩
💰 20е36 | 420 🍩
💰 20е48 | 550 🍩
💰 20е57 | 780 🍩</b>
➖➖➖➖➖➖➖➖➖➖➖➖
🛒 Чтобы купить валюту, выберите кнопку ниже
       """, reply_markup=valut, disable_web_page_preview=True, parse_mode='html')


@dp.callback_query_handler(text='cash_vip')
async def craft_resurs3(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    
    balance = cursor.execute("SELECT balance from users where user_id = ?",(callback.from_user.id,)).fetchone()
    balance = int(balance[0])
    
    rating = cursor.execute("SELECT rating from users where user_id = ?",(callback.from_user.id,)).fetchone()
    rating = int(rating[0])

    donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(callback.from_user.id,)).fetchone()
    donate_coins = int(donate_coins[0])
    
    vip_menu = InlineKeyboardMarkup(row_width=1)
    help_back2 = InlineKeyboardButton(text='🔙 Назад', callback_data='vip')
    vip_menu.add(help_back2)
    
    if donate_coins >= 50:
       await callback.message.edit_text( f"<a href='tg://user?id={user_id}'>{user_name}</a>, спасибо за покупку привилегию VIP", reply_markup=vip_menu, parse_mode='html' )
       cursor.execute(f'UPDATE users SET user_status = "Vip" where user_id = {user_id}')
       cursor.execute(f'UPDATE users SET rating = {rating + 100} where user_id = {user_id}')
       cursor.execute(f'UPDATE users SET balance = {balance + 10000000000} WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET donate_coins = {donate_coins - 50} WHERE user_id = {user_id}') 
       connect.commit()
    else:
       await bot.answer_callback_query(callback.id, show_alert=False, text=f"🆘 Ошибка! У вас нехватает пончиков 🍩")

@dp.callback_query_handler(text='vip')
async def craft3(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(callback.from_user.id,)).fetchone()
    donate_coins = int(donate_coins[0])

    vip_menu = InlineKeyboardMarkup(row_width=1)
    cash_vip = InlineKeyboardButton(text='🛒 Купить', callback_data='cash_vip')
    help_back2 = InlineKeyboardButton(text='🔙 Назад', callback_data='privilegii')
    vip_menu.add(cash_vip, help_back2)
    
    await callback.message.edit_text( f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вот данные за привилегию ВИП ❤️

✅ Получите отметку на балансе <b>❤️ Вип</b>
✅ Вы получите после покупки - 10е9₽ и 100 👑

🛒 Чтобы купить привилегию , виберите кнопку купить ниже
    """, reply_markup=vip_menu,  parse_mode='html')


@dp.callback_query_handler(text='cash_titan')
async def craft3(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    
    balance = cursor.execute("SELECT balance from users where user_id = ?",(callback.from_user.id,)).fetchone()
    balance = int(balance[0])
    
    rating = cursor.execute("SELECT rating from users where user_id = ?",(callback.from_user.id,)).fetchone()
    rating = int(rating[0])

    donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(callback.from_user.id,)).fetchone()
    donate_coins = int(donate_coins[0])
    
    vip_menu = InlineKeyboardMarkup(row_width=1)
    help_back2 = InlineKeyboardButton(text='🔙 Назад', callback_data='vip')
    vip_menu.add(help_back2)
    
    if donate_coins >= 150:
       await callback.message.edit_text( f"<a href='tg://user?id={user_id}'>{user_name}</a>, спасибо за покупку привилегию TITAN", reply_markup=vip_menu, parse_mode='html' )
       cursor.execute(f'UPDATE users SET user_status = "Titanium" where user_id = {user_id}')
       cursor.execute(f'UPDATE users SET rating = {rating + 170} where user_id = {user_id}')
       cursor.execute(f'UPDATE users SET balance = {balance + 10000000000000} WHERE user_id = {user_id}')
       cursor.execute(f'UPDATE users SET donate_coins = {donate_coins - 150} WHERE user_id = {user_id}') 
       connect.commit()
    else:
       await bot.answer_callback_query(callback.id, show_alert=False, text=f"🆘 Ошибка! У вас нехватает пончиков 🍩")

@dp.callback_query_handler(text='titan')
async def craft_resurs3(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?",(callback.from_user.id,)).fetchone()
    donate_coins = int(donate_coins[0])

    vip_menu = InlineKeyboardMarkup(row_width=1)
    cash_vip = InlineKeyboardButton(text='🛒 Купить', callback_data='cash_titan')
    help_back2 = InlineKeyboardButton(text='🔙 Назад', callback_data='privilegii')
    vip_menu.add(cash_vip, help_back2)
    
    await callback.message.edit_text( f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вот данные за привилегию ТИТАН 👾

✅ Получите отметку на балансе <b>👾 TITANIUM</b>
✅ Вы получите после покупки - 10е12₽ и 170 👑

🛒 Чтобы купить привилегию , виберите кнопку купить ниже
    """, reply_markup=vip_menu,  parse_mode='html')


@dp.callback_query_handler(text='privilegii')
async def craft_resurs3(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    
    privilegii_inline = InlineKeyboardMarkup(row_width=3)
    vip = InlineKeyboardButton(text='❤️ ВИП ', callback_data='vip')
    titan = InlineKeyboardButton(text='👾 ТИТАН', callback_data='titan')
    deluxe = InlineKeyboardButton(text='🔥 ДЕЛЮКС', callback_data='deluxe')
    chep = InlineKeyboardButton(text='🏆 ЧЕМПИОН', callback_data='chep')
    korol = InlineKeyboardButton(text='👑 КОРОЛЬ', callback_data='korol')
    donater = InlineKeyboardButton(text='😈 ДОНАТЕР', callback_data='donater')
    help_back2 = InlineKeyboardButton(text='🔙 Назад', callback_data='donat')
    privilegii_inline.add(vip, titan, deluxe, chep, korol, donater, help_back2)
    await callback.message.edit_text( f"""
<a href='tg://user?id={user_id}'>{user_name}</a> , вот все доступные привилегии 🔎:
➖➖➖➖➖➖➖➖➖➖➖➖
❗️ Появились проблемы с покупкой? обращайтесь к {cfg.owner}
➖➖➖➖➖➖➖➖➖➖➖➖
🔎 Редкое:
➖➖➖➖➖➖➖➖➖➖➖➖
❤️ Вип | 50 🍩
👾 Титан | 150 🍩
🔥 Делюкс | 255 🍩 [На тех. работах]
🏆 Чемпион | 300 🍩 [На тех. работах]
👑 Король | 450 🍩 [На тех. работах]
😈 Донатер | 600 🍩 [На тех. работах]
➖➖➖➖➖➖➖➖➖➖➖➖
🛒 Чтобы купить привилегию , виберите её ниже
    """, reply_markup=privilegii_inline, disable_web_page_preview=True, parse_mode='html')
    
    
@dp.callback_query_handler(text='adms')
async def donat_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    
    donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?", (callback.from_user.id,)).fetchone()
    donate_coins = int(donate_coins[0])
    donate_coins2 = '{:,}'.format(donate_coins)
    
    help_back = InlineKeyboardMarkup(row_width=1)
    help_back2 = InlineKeyboardButton(text='🔙 Назад', callback_data='donat')
    help_back.add(help_back2)
    
    await callback.message.edit_text(f"""
<a href='tg://user?id={user_id}'>{user_name}</a> › добро пожаловать в админ прав
➖➖➖➖➖➖➖➖➖➖➖➖
❗️ Появились желание купить обращайтесь к {cfg.owner}
➖➖➖➖➖➖➖➖➖➖➖➖
🏆 Администратор | 300₽
⛔️ Helper_Admin l 500₽
👑 Owner | 700₽
♦️ Developer | 1000₽
➖➖➖➖➖➖➖➖➖➖➖➖
       """, reply_markup=help_back, disable_web_page_preview=True, parse_mode='html')    
    

@dp.callback_query_handler(text='donat')
async def donat_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    
    donate_coins = cursor.execute("SELECT donate_coins from users where user_id = ?", (callback.from_user.id,)).fetchone()
    donate_coins = int(donate_coins[0])
    donate_coins2 = '{:,}'.format(donate_coins)
    
    donate_menu = InlineKeyboardMarkup(row_width=2)
    privilegii = InlineKeyboardButton(text='🔎 Привилегии', callback_data='privilegii')
    valut = InlineKeyboardButton(text='💰 Валюта', callback_data='valut')
    adms = InlineKeyboardButton(text='⛔️ Права в боте', callback_data='adms')
    donate_menu.add(privilegii, valut, adms)
    
    await callback.message.edit_text(f"""
<a href='tg://user?id={user_id}'>{user_name}</a> › добро пожаловать в донат-магазин
➖➖➖➖➖➖➖➖➖➖➖➖
❗️ Появились проблемы с авто оплатой? обращайтесь к {cfg.owner}
➖➖➖➖➖➖➖➖➖➖➖➖
🍩 <b>Баланс:</b> <code>{donate_coins2}</code>
🎗 <b>X2 Донат: Включен</b>
➖➖➖➖➖➖➖➖➖➖➖➖
👾 Команды:
💰 <code>Пополнить</code> [сумма]
➖➖➖➖➖➖➖➖➖➖➖➖
💹 Курс пончика ›
        💳 1₽ = 2 🍩
➖➖➖➖➖➖➖➖➖➖➖➖
🔎 <b>Привилегии:
        👾 Титан | 150 🍩
        🔥 Делюкс | 255 🍩
        🏆 Чемпион | 300 🍩
        👑 Король | 450 🍩
        😈 Донатер | 600 🍩</b>
➖➖➖➖➖➖➖➖➖➖➖➖
⛔️ <b>Права в боте:
        🏆 Администратор | 300₽
        ⛔️ Helper_Admin l 500₽
        👑 Owner | 700₽
        ♦️ Developer | 1000₽</b>
➖➖➖➖➖➖➖➖➖➖➖➖
💰 <b>Валюта:
         💰 20е12 | 120 🍩
         💰 20е18 | 220 🍩
         💰 20е27 | 310 🍩
         💰 20е36 | 420 🍩
         💰 20е48 | 550 🍩
         💰 20е57 | 780 🍩</b>
➖➖➖➖➖➖➖➖➖➖➖➖
⤵️ <b>Выберите одну из категорий</b>
       """, reply_markup=donate_menu, disable_web_page_preview=True, parse_mode='html')


@dp.callback_query_handler(text='cripto_kurs')
async def bonus5_callback(callback: types.CallbackQuery):
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    user_id = callback.from_user.id
    
    c = api.get_price(ids='ethereum', vs_currencies='rub')['ethereum']['rub']
    c2 = int(c)
    c3 = '{:,}'.format(c2)
    c4 = api.get_price(ids='bitcoin', vs_currencies='rub')['bitcoin']['rub']
    c5 = int(c4)
    c6 = '{:,}'.format(c5)
    c7 = api.get_price(ids='ethereum', vs_currencies='rub')['ethereum']['rub']
    c8 = int(c7)
    c9 = '{:,}'.format(c8)
    c10 = api.get_price(ids='bitcoin', vs_currencies='rub')['bitcoin']['rub']
    c11 = int(c10)
    c12 = '{:,}'.format(c11)
    
    help_back = InlineKeyboardMarkup(row_width=1)
    help_back2 = InlineKeyboardButton(text='🔙 Назад', callback_data='cripto5')
    help_back.add(help_back2)
    
    await callback.message.edit_text(f"""📊 | <a href='tg://user?id={user_id}'>{user_name}</a>, вот курс крипто валют

🔹 LITECOIN — <code>{c3}</code>₽
🌐 BITCOIN — <code>{c6}</code>₽
🟣 ETH — <code>{c9}</code>₽
💠 PHANTOM — <code>{c12}</code>₽
    """, reply_markup=help_back, parse_mode='html')


@dp.callback_query_handler(text='cripto5')
async def bonus5(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    
    ethereum = cursor.execute("SELECT ethereum from users where user_id = ?",(callback.from_user.id,)).fetchone()
    ethereum = int(ethereum[0])
    ethereum2 = '{:,}'.format(ethereum)
    bitcoin = cursor.execute("SELECT bitcoin from users where user_id = ?",(callback.from_user.id,)).fetchone()
    bitcoin = int(bitcoin[0])
    bitcoin2 = '{:,}'.format(bitcoin)
    litecoin = cursor.execute("SELECT litecoin from users where user_id = ?",(callback.from_user.id,)).fetchone()
    litecoin = int(litecoin[0])
    litecoin2 = '{:,}'.format(litecoin)
    fantom = cursor.execute("SELECT fantom from users where user_id = ?",(callback.from_user.id,)).fetchone()
    fantom = int(fantom[0])
    fantom2 = '{:,}'.format(fantom)
    
    help_back = types.InlineKeyboardMarkup(row_width=1)
    help_back.add(types.InlineKeyboardButton(text='📊 Курс крипто валют', callback_data='cripto_kurs'))
    
    await callback.message.edit_text(f"""💳 | <a href='tg://user?id={user_id}'>{user_name}</a>, вот ваш крипто кошелёк

🔹 LITECOIN: <code>{litecoin2}</code>
🌐 BITCOIN: <code>{bitcoin2}</code>
🟣 ETH: <code>{ethereum2}</code>
💠 PHANTOM: <code>{fantom2}</code>
    """, reply_markup=help_back, parse_mode='html')
    
    
@dp.callback_query_handler(text='bonus5')
async def bonus5_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    
    balance = cursor.execute("SELECT balance from users where user_id = ?", (callback.from_user.id,)).fetchone()
    balance = int(balance[0])
    period = 86400 #86400 s = 24h
    get = cursor.execute("SELECT stavka_bonus FROM bot_time WHERE user_id = ?", (callback.from_user.id,)).fetchone()
    last_stavka = int(get[0])
    stavkatime = time.time() - float(last_stavka)
    
    rx = random.randint(1000000,25000000)
    rx2 = '{:,}'.format(rx)
    
    if stavkatime > period:       
       await callback.message.answer(f"🎁 <a href='tg://user?id={user_id}'>{user_name}</a>, вы получили ежедневный бонус в сумме {rx2}¢ 💵", parse_mode='html')
       cursor.execute(f'UPDATE users SET balance = {balance + rx}  WHERE user_id = "{user_id}"')
       cursor.execute(f'UPDATE bot_time SET stavka_bonus = {time.time()} WHERE user_id = "{user_id}"')
       connect.commit()
    else:
          await bot.answer_callback_query(callback.id, show_alert=False, text=f'‼️ Получать ежедневный бонус можно раз в 24ч⏳')


@dp.callback_query_handler(text='register_help')
async def help(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    
    help2 = InlineKeyboardMarkup(row_width=2)
    Osn2 = InlineKeyboardButton(text='💡 Основное', callback_data='Osn2')
    game2 = InlineKeyboardButton(text='🕹️ Игры', callback_data='game2')
    Im2 = InlineKeyboardButton(text='🏠 Дом', callback_data='Im2')
    Osn = InlineKeyboardButton(text='❕ Остальное', callback_data='ostal_menu')
    ded2 = InlineKeyboardButton(text='➡️ Дальше', callback_data='ded2')
    help2.add(Osn2, game2, Im2, Osn, ded2)

    await callback.message.edit_text(f'''
➖➖➖➖➖➖➖➖➖➖➖
📊 Канал - {cfg.channel}
💭 Чат - {cfg.chat}
❗️ По всем вопросам - {cfg.owner}
➖➖➖➖➖➖➖➖➖➖➖
🔎 Категории
├ 💡 Основное
├ 🕹️ Игры
├ 🏠 Дом
└ ❕ Остальное
➖➖➖➖➖➖➖➖➖➖
Выберите одну кнопку ниже👇🏻
    ''', reply_markup=help2, disable_web_page_preview=True, parse_mode='html')  


@dp.callback_query_handler(text='Osn2')
async def osn2_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    help_back = InlineKeyboardMarkup(row_width=1)
    help_back2 = InlineKeyboardButton(text='🔙 Назад', callback_data='register_help')
    help_back.add(help_back2)
            
    await callback.message.edit_text(f'''
<a href='tg://user?id={user_id}'>{user_name}</a>, вот основные команды бота <b>RDG</b>

💸 <code>Б</code> <b>»</b> <code>Баланс</code> - <b>выводит ваш игровой баланс</b>
👤 <code>Профиль</code> <b>»</b> <code>П</code> - <b>выводит ваш игровой профиль</b>
👥 <code>Ник</code> <b>»</b> <code>Сменить ник</code>  - <b>Выводит ваш ник, и так же его меняет</b>
💳 <code>Карта</code> <b>»</b> <code>Карта положить 1</code> <b>»</b> <code>Карта снять 1</code>  - <b>выводит ваш игровой карту с депозитом , позволяет положить в карту сумму, позволяет снять с карты сумму</b>

❕ <b>Для использование команды, напишите её сообщением</b>
    ''', reply_markup=help_back, parse_mode='html')


@dp.callback_query_handler(text='game2')
async def game2_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    help_back = InlineKeyboardMarkup(row_width=1)
    help_back2 = InlineKeyboardButton(text='🔙 Назад', callback_data='register_help')
    help_back.add(help_back2)    
            
    await callback.message.edit_text(f'''
<a href='tg://user?id={user_id}'>{user_name}</a>, вот вам команды игр

🕹️ Игры:
┣ 🏎 Гонка
┃   ┗ Гонка [ставка]
┣ 🏀️ Баскетбол
┃   ┗ Баскетбол [ставка]
┣ 🎳 Боулинг
┃   ┗ Боулинг [ставка]
┣ 🎯 Дартс
┃   ┗ Дартс [ставка]
┣ ⚽ Футбол
┃   ┗ Футбол [ставка]
┣ 🎰 Спин
┃   ┗ Спин [ставка]
┣ 🪙 Флип
┃   ┗ Флип [ставка] [орёл, решка]
┣ 🖲 Рулетка
┃   ┗ Рулетка [черное, красное] [ставка] 
┣ 🎱 Дайк
┃   ┗ [сумма] [к/в]
┣ 🎲 Кости
┃   ┗ Кости [сумма]
┣ 🪓 Охота
┃   ┗ Охота [сумма]
┣ 🤼 Бой
┃   ┗ Бой [сумма]
┗ 🥇 Игра
    ┗ Игра [камень/ножница/бумага]

❕ <b>Для использование команды, напишите её сообщением</b>
    ''', reply_markup=help_back, parse_mode='html')


@dp.callback_query_handler(text='Im2')
async def im2_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    help_back = InlineKeyboardMarkup(row_width=2)
    help_back2 = InlineKeyboardButton(text='🔙 Назад', callback_data='register_help')
    help_back.add(help_back2)    
            
    await callback.message.edit_text(f'''
<a href='tg://user?id={user_id}'>{user_name}</a>, вот более точная информация за дом 🏠

🏡 <code>Дом</code> - <b>выводит информацию за ваш дом</b>
🏡 <code>Купить дом</code> <b>[номер] - Позволяет вам купить вам дом</b>
🏡 <code>Продать дом</code> - <b>Позволяет вам продать ваш дом</b>
🏡 <code>Аренда дом</code> - <b>вы можете дать свое имущество в аренду и получать доход зависит от крутости вашего имущества</b>

❕ <b>Для использование команды, напишите её сообщением</b>
    ''', reply_markup=help_back, parse_mode='html')
    
    
@dp.callback_query_handler(text='ostal_menu')
async def oston_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    help_back = InlineKeyboardMarkup(row_width=1)
    help_back2 = InlineKeyboardButton(text='🔙 Назад', callback_data='register_help')
    help_back.add(help_back2)    
            
    await callback.message.edit_text(f'''
<a href='tg://user?id={user_id}'>{user_name}</a>, вот остальные команды❗

🎰 Шанс
🔮 Шар [фраза]
🥅 Выбери [фраза1] или [фраза2]
🏓 /пинг - пинг моего бота.
🤖 /ask [вопрос] - отвечает на вопросы.

❕ <b>Для использование команды, напишите её сообщением</b>
    ''', reply_markup=help_back, parse_mode='html')


@dp.callback_query_handler(text='ded2')
async def help(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    
    help3 = InlineKeyboardMarkup(row_width=2)
    internet2 = InlineKeyboardButton(text='🌍 Интернет', callback_data='internet2')
    city2 = InlineKeyboardButton(text='🌇 Город', callback_data='city2')
    Im7 = InlineKeyboardButton(text='💠 Крипто валюта', callback_data='Im7')
    brak2 = InlineKeyboardButton(text='💖 Браки', callback_data='brak2')
    help_back2 = InlineKeyboardButton(text='⬅️ Назад', callback_data='register_help')
    help_back3 = InlineKeyboardButton(text='➡️ Дальше', callback_data='ded3')
    help3.add(internet2, city2, Im7, brak2, help_back2, help_back3)

    await callback.message.edit_text(f'''
➖➖➖➖➖➖➖➖➖➖➖
📊 Канал - {cfg.channel}
💭 Чат - {cfg.chat}
❗️ По всем вопросам - {cfg.owner}
➖➖➖➖➖➖➖➖➖➖➖
🔎 Категории
├ 🌍 Интернет
├ 🌇 Город
├ 💠 Крипто валюта
└ 💖 Браки
➖➖➖➖➖➖➖➖➖➖
Выберите одну кнопку ниже👇🏻
    ''', reply_markup=help3, disable_web_page_preview=True, parse_mode='html')


@dp.callback_query_handler(text='internet2')
async def internet2_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    
    help_back = InlineKeyboardMarkup(row_width=1)
    help_back2 = InlineKeyboardButton(text='🔙 Назад', callback_data='ded2')
    help_back.add(help_back2)
    
    await callback.message.edit_text(f'''
<a href='tg://user?id={user_id}'>{user_name}</a>, вот команды связанные с интернетом 🌍

💻 <code>Тикток</code> - <b>статистика вашего аккаунта ТикТок</b>
💻 <code>Тикток создать</code> [название аккаунта] - <b>создание вашего аккаунта ТикТок</b>
💻 <code>Тикток реклама</code> - <b>реклама в тиктоке</b>
💻 <code>Тикток видео</code> - <b>заснять видео в ТикТок</b>
💻 <code>Тикток лайк</code> <b>(Ответом на сообщение) - ставить пользователю лайк</b>

🎬 <code>Мой канал</code> - <b>статистика вашего канала</b>
⚒ <code>Создать канал</code> - <b>создание вашего канала</b>
🛒 <code>Купить</code> <b>[название предмета] - покупка материалов для канала</b>
📼 <code>Снять видео</code> - <b>снять видео в канал</b>
📸 <code>Видео система</code> - <b>система кнопак</b>
🛒 <code>Купить все</code> - <b>покупка весь материалов</b>

❕ <b>Для использование команды, напишите её сообщением</b>
    ''', reply_markup=help_back, parse_mode='html')


@dp.callback_query_handler(text='city2')
async def internet2_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    
    help_back = InlineKeyboardMarkup(row_width=1)
    help_back2 = InlineKeyboardButton(text='🔙 Назад', callback_data='ded2')
    help_back.add(help_back2)
    
    await callback.message.edit_text(f'''
<a href='tg://user?id={user_id}'>{user_name}</a>, вот команды связанные с городом 🌇

🌇 <code>Город построить</code> - <b>для создание города</b>
🌃 <code>Мой город</code> - <b>информация о вашем городе</b>
💱 <code>Город снять</code> - <b>снимает с казны города</b>
🔂 <code>Г налог</code> - <b>налог для жителей</b>
🛣️ <code>Город дорога</code> - <b>расширает дорогу в городе</b>
🏭 <code>Город завод</code> - <b>для постройки заводов</b>
💦 <code>Город вода</code> - <b>для постройки водонапорных башен</b>
⚡️ <code>Город энергия</code> - <b>для постройки АЭС</b>
🏘️ <code>Город дом</code> - <b>для постройки дома</b>

❕ <b>Для использование команды, напишите её сообщением</b>
    ''', reply_markup=help_back, parse_mode='html')


@dp.callback_query_handler(text='Im7')
async def internet2_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    
    help_back = InlineKeyboardMarkup(row_width=1)
    help_back2 = InlineKeyboardButton(text='🔙 Назад', callback_data='ded2')
    help_back.add(help_back2)
    
    await callback.message.edit_text(f'''
<a href='tg://user?id={user_id}'>{user_name}</a>, вот команды связанные с крипто валютой 💠

🛒 <b>Название крипто валюты продать [количество] - Покупка крипто валюты</b>
🗑 <b>Название крипто валюты продать [количество] - Продажа крипто валюты</b>
📊 <code>Б</code> <b>» Крипто » Курс крипто валют - Курс крипто валют в реальном времени</b>
🌐 <code>Б</code> <b>» Крипто - Ваш игровой крипто кошелёк</b>

❕ <b>Для использование команды, напишите её сообщением</b>
    ''', reply_markup=help_back, parse_mode='html')


@dp.callback_query_handler(text='brak2')
async def internet2_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    
    help_back = InlineKeyboardMarkup(row_width=1)
    help_back2 = InlineKeyboardButton(text='🔙 Назад', callback_data='ded2')
    help_back.add(help_back2)
    
    await callback.message.edit_text(f'''
<a href='tg://user?id={user_id}'>{user_name}</a>, вот команды связанные с браками 💖

💖 <code>Брак</code> <b>(Ответом на сообщение) - Предложение в ступить брак с игроком</b>
💖 <code>Мой брак</code> - <b>Просмотр вашего брака с игроком</b>
💔 <code>Развод</code> - <b>Разорвать ваш брак с игроком</b>

❕ <b>Для использование команды, напишите её сообщением</b>
    ''', reply_markup=help_back, parse_mode='html')


@dp.callback_query_handler(text='ded3')
async def help(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    
    help4 = InlineKeyboardMarkup(row_width=2)
    rabot2 = InlineKeyboardButton(text='🔨 Работы', callback_data='rabot2')
    info2 = InlineKeyboardButton(text='💫 Информация', callback_data='info2')
    clan2 = InlineKeyboardButton(text='🛡️ Клан', callback_data='clan2')
    kazino = InlineKeyboardButton(text='🃏 Казино', callback_data='kazino')
    help_back2 = InlineKeyboardButton(text='⬅️ Назад', callback_data='ded2')
    help_back3 = InlineKeyboardButton(text='➡️ Дальше', callback_data='ded4')
    help4.add(rabot2, info2, clan2, kazino, help_back2, help_back3)

    await callback.message.edit_text(f'''
➖➖➖➖➖➖➖➖➖➖➖
📊 Канал - {cfg.channel}
💭 Чат - {cfg.chat}
❗️ По всем вопросам - {cfg.owner}
➖➖➖➖➖➖➖➖➖➖➖
🔎 Категории
├ 🔨 Работы
├ 💫 Информация
├ 🛡️ Клан
└ 🃏 Казино
➖➖➖➖➖➖➖➖➖➖
Выберите одну кнопку ниже👇🏻
    ''', reply_markup=help4, disable_web_page_preview=True, parse_mode='html')


@dp.callback_query_handler(text='rabot2')
async def rabot2_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    help_back = InlineKeyboardMarkup(row_width=1)
    help_back2 = InlineKeyboardButton(text='🔙 Назад', callback_data='ded3')
    help_back.add(help_back2)    
            
    await callback.message.edit_text(f'''
<a href='tg://user?id={user_id}'>{user_name}</a>, все доступные работы в боте <b>RDG</b>

скоро
    ''', reply_markup=help_back, parse_mode='html')


@dp.callback_query_handler(text='info2')
async def internet2_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    
    help_back = InlineKeyboardMarkup(row_width=1)
    help_back2 = InlineKeyboardButton(text='🔙 Назад', callback_data='ded3')
    help_back.add(help_back2)
    
    await callback.message.edit_text(f'''
💫 | Информация

💫 Привет я RDG бот так же много функциональный игровой бот
💫 Мой разработчик - {cfg.owner}
💫 Дата выхода - 11.02.23 в 20:59
    ''', reply_markup=help_back, disable_web_page_preview=True, parse_mode='html')


@dp.callback_query_handler(text='clan2')
async def internet2_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    
    help_back = InlineKeyboardMarkup(row_width=1)
    help_back2 = InlineKeyboardButton(text='🔙 Назад', callback_data='ded3')
    help_back.add(help_back2)
    
    await callback.message.edit_text(f'''
<a href='tg://user?id={user_id}'>{user_name}</a>, вот команды связанные с кланами 🛡️
    
🛡️ <code>Клан создать</code> (название)
🛡️ <code>Клан покинуть</code> - <b>если вы создатель управление кланом перейдет другому игроку</b>
🛡️ <code>Клан вступить</code> (id) - <b>если клан закрыт вы не сможете вступить</b>
📁 <code>Мой клан</code> - <b>информация о клане</b>
👥 <code>Клан участники</code> - <b>вывод участников клана</b>
💰 <code>Клан пополнить</code> - <b>деньги клана</b>
💰 <code>Клан снять</code> - <b>снимать может только создатель</b>
📛 <code>Клан кик </code>(id) - <b>изгоняет игрока из клана</b>
🔐 <code>Клан приватность</code> 
⚔️ <code>Клан атака</code> (id)
💪 <code>Клан усилить</code> (число)
⏫ <code>Клан повысить</code>
⏬ <code>Клан понизить</code>

🛑 <b>Будьте осторожны повышая ранг игрокам они могут управлять вашим кланом !</b>

❕ <b>Для использование команды, напишите её сообщением</b>
    ''', reply_markup=help_back, parse_mode='html')


@dp.callback_query_handler(text='kazino')
async def kazino_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    help_back = InlineKeyboardMarkup(row_width=1)
    help_back2 = InlineKeyboardButton(text='🔙 Назад', callback_data='ded3')
    help_back.add(help_back2)
            
    await callback.message.edit_text(f"""
<a href='tg://user?id={user_id}'>{user_name}</a>, вот информация за команды Казино 🃏

🃏 <code>Казино</code> <b>[ставка] - Предложить ставку игроку</b>
⛔️ <code>Отменить ставку</code> - <b>Отменяет ставку которая стояла в ожидании</b>
ℹ️ <code>/казино</code> - <b>Выводит подробную информацию за казино</b>

❕ <b>Для использование команды, напишите её сообщением</b>
    """, reply_markup=help_back, parse_mode='html')


@dp.callback_query_handler(text='ded4')
async def help(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    
    help5 = InlineKeyboardMarkup(row_width=2)
    ferma2 = InlineKeyboardButton(text='🧰 Ферма', callback_data='ferma2')
    electro2 = InlineKeyboardButton(text='🎡 Электростанции', callback_data='electro2')
    promo2 = InlineKeyboardButton(text='🪄 Промокоды', callback_data='promo2')
    gde2 = InlineKeyboardButton(text='👮🏼‍♀️ Система жалоб', callback_data='gde2')
    help_back2 = InlineKeyboardButton(text='⬅️ Назад', callback_data='ded3')
    help_back3 = InlineKeyboardButton(text='➡️ Дальше', callback_data='ded5')
    help5.add(ferma2, electro2, promo2, gde2, help_back2, help_back3)

    await callback.message.edit_text(f'''
➖➖➖➖➖➖➖➖➖➖➖
📊 Канал - {cfg.channel}
💭 Чат - {cfg.chat}
❗️ По всем вопросам - {cfg.owner}
➖➖➖➖➖➖➖➖➖➖➖
🔎 Категории
├ 🧰 Ферма
├ 🎡 Электростанции
├ 🪄 Промокоды
└ 👮🏼‍♀️ Система жалоб
➖➖➖➖➖➖➖➖➖➖
Выберите одну кнопку ниже👇🏻
    ''', reply_markup=help5, disable_web_page_preview=True, parse_mode='html')


@dp.callback_query_handler(text='ferma2')
async def game2_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    help_back = InlineKeyboardMarkup(row_width=1)
    help_back2 = InlineKeyboardButton(text='🔙 Назад', callback_data='ded4')
    help_back.add(help_back2)
            
    await callback.message.edit_text(f'''
<a href='tg://user?id={user_id}'>{user_name}</a>, щас подробно расскажу о майнинг ферме 🧰

<b>Ферма</b> 🧰 - Один из бизнесов игровых ботов, отличный выбор для стабильного заработка без какого либо вмешательства а точнее, все зависит от времени.

🔌 Стоимость одного видеокарт: Зависит от вашего уровня фермы
🧰 Список всех ферм » <code>Фермы</code>
💸 Продажа вашего фермы: <code>Продать ферму</code>

❕ <code>Моя ферма</code> - Для просмотра прибыли и так же прокачки ферму
    ''', reply_markup=help_back, parse_mode='html')


@dp.callback_query_handler(text='electro2')
async def game2_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    help_back = InlineKeyboardMarkup(row_width=1)
    help_back2 = InlineKeyboardButton(text='🔙 Назад', callback_data='ded4')
    help_back.add(help_back2)
            
    await callback.message.edit_text(f'''
<a href='tg://user?id={user_id}'>{user_name}</a>, щас подробно расскажу о электростанциях 🎡

<b>Электростанция</b> 🎡 - Один из бизнесов игровых ботов, отличный выбор для стабильного заработка без какого либо вмешательства а точнее, все зависит от времени.

💼 <b>Стоимость одного турбины: зависит от вашего уровня электростанции.</b>
🎡 <b>Список всех электростанции:</b> <code>Электростанции</code>
💸 <b>Продажа вашего электростанции:</b> <code>Продать электростанцию</code>

👀 <code>Моя электростанция</code> - <b>Для просмотра прибыли и так же прокачки электростанции</b>
    ''', reply_markup=help_back, parse_mode='html')


@dp.callback_query_handler(text='promo2')
async def game2_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    help_back = InlineKeyboardMarkup(row_width=1)
    help_back2 = InlineKeyboardButton(text='🔙 Назад', callback_data='ded4')
    help_back.add(help_back2)

    await callback.message.edit_text(f'''
<a href='tg://user?id={user_id}'>{user_name}</a>, щас подробно расскажу о системах промокодов 🪄

🪄 <code>Промо</code> <b>[название] - активация промокодов</b>
🪄 <code>+промо</code> <b>[название] [сумма] [количество использований] - создания своего промокода</b>

❕ <b>Для использование команды, напишите её сообщением</b>
    ''', reply_markup=help_back, parse_mode='html')


@dp.callback_query_handler(text='gde2')
async def game2_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    help_back = InlineKeyboardMarkup(row_width=1)
    help_back2 = InlineKeyboardButton(text='🔙 Назад', callback_data='ded4')
    help_back.add(help_back2)

    await callback.message.edit_text(f'''
<a href='tg://user?id={user_id}'>{user_name}</a>, вот правила и команды для использования жалоб 👮🏼‍♀️

❕ Система жалоб используют только если видят пользователя который нарушает <a href="https://teletype.in/@neonion14/RDG_bot">правила игрового бота</a>

👮🏼‍♀️ <code>/жалоба</code> <b>[Нарушение] - команда для отправки жалобы, администрации бота</b>

❕ <b>Для использование команды, напишите её сообщением</b>
    ''', reply_markup=help_back, disable_web_page_preview=True, parse_mode='html')


@dp.callback_query_handler(text='ded5')
async def help(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    
    help6 = InlineKeyboardMarkup(row_width=2)
    ref2 = InlineKeyboardButton(text='✉️ Реф', callback_data='ref2')
    rp2 = InlineKeyboardButton(text='🌒 RP MOD', callback_data='rp2')
    car2 = InlineKeyboardButton(text='🚘 Машины', callback_data='car2')
    pet2 = InlineKeyboardButton(text='🐶 Питомцы', callback_data='pet2')
    help_back2 = InlineKeyboardButton(text='⬅️ Назад', callback_data='ded4')
    help_back3 = InlineKeyboardButton(text='➡️ Дальше', callback_data='ded6')
    help6.add(ref2, rp2, car2, pet2, help_back2, help_back3)

    await callback.message.edit_text(f'''
➖➖➖➖➖➖➖➖➖➖➖
📊 Канал - {cfg.channel}
💭 Чат - {cfg.chat}
❗️ По всем вопросам - {cfg.owner}
➖➖➖➖➖➖➖➖➖➖➖
🔎 Категории
├ ✉️ Реф
├ 🌒 RP MOD
├ 🚘 Машины
└ 🐶 Питомцы
➖➖➖➖➖➖➖➖➖➖
Выберите одну кнопку ниже👇🏻
    ''', reply_markup=help6, disable_web_page_preview=True, parse_mode='html')


@dp.callback_query_handler(text='ref2')
async def game2_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    help_back = InlineKeyboardMarkup(row_width=1)
    help_back2 = InlineKeyboardButton(text='🔙 Назад', callback_data='ded5')
    help_back.add(help_back2)

    await callback.message.edit_text(f'''
<a href='tg://user?id={user_id}'>{user_name}</a>, щас подробно объясню за реферальную систему ✉️

🔏 <code>Реф</code> - <b>Статистика о вашей реферальной ссылке</b>

🧍‍♂️ <b>При добавлении людей, вы получаете определенный бонус как рекламодатель бота</b>
    ''', reply_markup=help_back, disable_web_page_preview=True, parse_mode='html')


@dp.callback_query_handler(text='rp2')
async def game2_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    help_back = InlineKeyboardMarkup(row_width=1)
    help_back2 = InlineKeyboardButton(text='🔙 Назад', callback_data='ded5')
    help_back.add(help_back2)

    await callback.message.edit_text(f'''
<a href='tg://user?id={user_id}'>{user_name}</a>, сейчас расскажу за RP MOD 🌒

🌒 <code>рп</code> - Список всех рп команд
    ''', reply_markup=help_back, parse_mode='html')


@dp.callback_query_handler(text='car2')
async def game2_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    help_back = InlineKeyboardMarkup(row_width=1)
    help_back2 = InlineKeyboardButton(text='🔙 Назад', callback_data='ded5')
    help_back.add(help_back2)

    await callback.message.edit_text(f'''
<a href='tg://user?id={user_id}'>{user_name}</a>, сейчас расскажу за машины 🚘

🚘 <code>Машина</code> - <b>Выводит информацию за вашу машину</b>

🚗 <code>Купить машину</code> <b>[номер] - Позволяет вам купить вам автомобиль</b>
🚗 <code>Продать машину</code> - <b>Позволяет вам продать ваш автомобиль</b>
🚗 <code>Заправить</code> - <b>Позволяет вам заправить ваш автомобиль</b>
🚗 <code>Починить</code> - <b>Позволяет вам починить ваш автомобиль</b>
    ''', reply_markup=help_back, parse_mode='html')


@dp.callback_query_handler(text='pet2')
async def game2_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    help_back = InlineKeyboardMarkup(row_width=1)
    help_back2 = InlineKeyboardButton(text='🔙 Назад', callback_data='ded5')
    help_back.add(help_back2)

    await callback.message.edit_text(f'''
<a href='tg://user?id={user_id}'>{user_name}</a>, сейчас расскажу за питомцов 🐶

🐶 <code>Питомцы</code> - <b>Выводит доступных питомцах, и так же информацию за покупку их</b>
🐶 <code>Мой питомец</code> - <b>Выводит информацию про вашего питомца</b>
🐶 <code>Питомец имя</code> <b>[название]</b>

❤️ <code>Вылечить питомца</code> - <b>Позволяет вам вылечить питомца</b>
🍗 <code>Покормить питомца</code> - <b>Позволяет вам покормить питомца</b>
🌳 <code>Выгулять питомца</code> - <b>Позволяет вам выгулять питомца</b>
    ''', reply_markup=help_back, parse_mode='html')


@dp.callback_query_handler(text='ded6')
async def help(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    
    help6 = InlineKeyboardMarkup(row_width=2)
    refad2 = InlineKeyboardButton(text='🤝 Транзакция', callback_data='refad2')
    reting2 = InlineKeyboardButton(text='👑 Рейтинг', callback_data='reting2')
    depozit2 = InlineKeyboardButton(text='💳 Депозит', callback_data='depozit2')
    family = InlineKeyboardButton(text='🏰 Организации', callback_data='family')
    help_back2 = InlineKeyboardButton(text='⬅️ Назад', callback_data='ded5')
    help6.add(refad2, reting2, depozit2, family, help_back2)

    await callback.message.edit_text(f'''
➖➖➖➖➖➖➖➖➖➖➖
📊 Канал - {cfg.channel}
💭 Чат - {cfg.chat}
❗️ По всем вопросам - {cfg.owner}
➖➖➖➖➖➖➖➖➖➖➖
🔎 Категории
├ 🤝 Транзакция
├ 👑 Рейтинг
├ 💳 Депозит
└ 🏰 Организации
➖➖➖➖➖➖➖➖➖➖
Выберите одну кнопку ниже👇🏻
    ''', reply_markup=help6, disable_web_page_preview=True, parse_mode='html')


@dp.callback_query_handler(text='refad2')
async def game2_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    help_back = InlineKeyboardMarkup(row_width=1)
    help_back2 = InlineKeyboardButton(text='🔙 Назад', callback_data='ded6')
    help_back.add(help_back2)

    await callback.message.edit_text(f'''
<a href='tg://user?id={user_id}'>{user_name}</a>, более подробная помощь за транзакции (переводы) 🤝

💰 <code>Дать</code> <b>(сумма) - перевести средства игроку</b>
    ''', reply_markup=help_back, parse_mode='html')


@dp.callback_query_handler(text='reting2')
async def game2_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    help_back = InlineKeyboardMarkup(row_width=1)
    help_back2 = InlineKeyboardButton(text='🔙 Назад', callback_data='ded6')
    help_back.add(help_back2)

    await callback.message.edit_text(f'''
<a href='tg://user?id={user_id}'>{user_name}</a>, более подробная помощь за рейтинг

👑 <code>Рейтинг купить</code> <b>(сумма) - покупка рейтинга , стоимость одного рейтинга при покупке 150,000,000₽</b>
👑 <code>Рейтинг продать</code> <b>(сумма) - продажа рейтинга, стоимость одного рейтинга при продаже 100,000,000₽</b>
    ''', reply_markup=help_back, parse_mode='html')


@dp.callback_query_handler(text='depozit2')
async def game2_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    help_back = InlineKeyboardMarkup(row_width=1)
    help_back2 = InlineKeyboardButton(text='🔙 Назад', callback_data='ded6')
    help_back.add(help_back2)

    await callback.message.edit_text(f'''
<a href='tg://user?id={user_id}'>{user_name}</a>, более подробная помощь за депозит 💳

💳 <code>Депозит положить</code> <b>[сумма] - Позволяет положить на депозит</b>
💳 <code>Депозит снять</code> <b>[сумма] - позволяет снять с депозита</b>
💳 <code>Процент снять</code> <b>[сумма] - позволяет снять накапанный процент с депозита</b>
    ''', reply_markup=help_back, parse_mode='html')


@dp.callback_query_handler(text='family')
async def family_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])

    help_back = InlineKeyboardMarkup(row_width=1)
    help_back2 = InlineKeyboardButton(text='🔙 Назад', callback_data='ded6')
    help_back.add(help_back2)

    await callback.message.edit_text(f'''
<a href='tg://user?id={user_id}'>{user_name}</a>, вот информация за «<b>СЕМЬИ</b>» 👨‍👩‍👧‍👦

✏️ <b><code>Создать семью</code> <i>[название]</i> - команда для создание свой семьи <i>(Стоимость: {cfg.cash_family} 🍩)</i></b>
👨‍👩‍👧‍👦 <b><code>Моя семья</code> | <code>семья</code> - вывод информации за семью в которой вы состоите </b>
⚙️ <b><code>+название семьи</code> <i>[название]</i> - Меняет название семьи <i>( можно раз в 7d) (от 3 ранга)</i></b>
💎 <b><code>Купить монеты</code> <i>[количество]</i> - Покупка семейный монет в мешок семьи</b>
➖ <b><code>-ранг семьи</code> - Понизить игрока в семье на 1 ранг ниже <i>(от 3 ранга)</i></b>
➕ <b><code>+ранг семьи</code> - Повысить игрока в семье на 1 ранг выше <i>(от 3 ранга)</i></b>
👶 <b><code>Пригласить в семью</code> - Приглашение в вашу семью <i>(от 2 ранга)</i></b>
❌ <b><code>Выгнать из семьи</code> - Исключение игрока из вашей семьи <i>(от 3 ранга)</i></b>
💭 <b><code>+описание семьи</code> <i>[описание]</i> - Устоновка описание в вашей семье <i>(от 3 ранга)</i></b>
😔 <b><code>Распустить семью</code> - Удаление семьи <i>(от 3 ранга)</i></b>
🔙 <b><code>Выйти с семьи</code> - Выход с семьи </b>

❗️ Будьте окуратней при <b>выдаче ранга игроку</b>
    ''', reply_markup=help_back, parse_mode='html')


@dp.callback_query_handler(text='pribel')
async def help(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(callback.from_user.id,)).fetchone()
    user_name = str(user_name[0])
    
    chat_id = callback.message.chat.id
    win = ['🙂', '😋', '😄', '🤑', '😃']
    rwin = random.choice(win)
    loser = ['😔', '😕', '😣', '😞', '😢']
    rloser = random.choice(loser)
    user_name = cursor.execute(
        "SELECT user_name from users where user_id = ?", (callback.from_user.id,))
    user_name = cursor.fetchone()
    user_name = str(user_name[0])
    cripto = cursor.execute(
        "SELECT bitcoin from users where user_id = ?",(callback.from_user.id,))
    cripto = cursor.fetchone()
    cripto = int(cripto[0])
    balance = cursor.execute(
        "SELECT bitmaning from users where user_id = ?", (callback.from_user.id,))
    balance = cursor.fetchone()
    balance = int(balance[0])
    balance2 = '{:,}'.format(balance).replace(",", ".")
    if int(balance) > 0:
        await bot.send_message(callback.message.chat.id,
                                   f'‼️ {user_name}, вы успешно сняли с Баланса Майнинг-Фермы {balance2}฿ на свой баланс {rwin}',
                                   parse_mode='html')
        cursor.execute(
                f'UPDATE users SET bitcoin = {cripto + balance} WHERE user_id = {user_id}')
        cursor.execute(
                f'UPDATE users SET bitmaning = {balance - balance} WHERE user_id = {user_id}')
        connect.commit()
    else:
        await bot.answer_callback_query(
                callback.id, ' На балансе фермы пусто! ')

@dp.callback_query_handler(lambda c: c.data == "gamestavka2")
async def gamest(callback_query: types.CallbackQuery):
    user = await bot.get_chat(str(first_p[0]))
    replyuser = await bot.get_chat(str(second_p[0]))
    usid = user.id
    rid = replyuser.id
    ruser_name = cursor.execute("SELECT user_name from users where user_id = ?",(rid,))
    ruser_name=cursor.fetchone()
    ruser_name = ruser_name[0]
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(usid,))
    user_name=cursor.fetchone()
    user_name = user_name[0]
    if callback_query.from_user.id == replyuser.id:
        balance=cursor.execute("SELECT balance FROM users WHERE user_id=?",(usid,))
        balance=cursor.fetchone()
        balance=int(balance[0])

        balance2 = cursor.execute("SELECT balance FROM users WHERE user_id=?", (rid,))
        balance2 = cursor.fetchone()
        balance2 = int(balance2[0])
        summ_stavka1= int(summ_stavka[0])
        if balance>=summ_stavka1 and balance2>=summ_stavka1:
            if summ_stavka1>0:
                rx=random.randint(0,5)
                rx1 = random.randint(0, 5)
                if rx1>rx:
                    cursor.execute(f"UPDATE users SET balance={balance + summ_stavka1} WHERE user_id={usid}")
                    cursor.execute(f"UPDATE users SET balance={balance2 - summ_stavka1} WHERE user_id={rid}")
                    cursor.execute("UPDATE users SET stavka=0 WHERE user_id=?", (usid,))
                    cursor.execute("UPDATE users SET stavka=0 WHERE user_id=?", (rid,))
                    first_p.clear()
                    second_p.clear()
                    summ_stavka.clear()

                    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
                    await bot.send_message(callback_query.message.chat.id, f"<a href='tg://user?id={usid}'>{user_name}</a>({rx1}), и <a href='tg://user?id={rid}'>{ruser_name}</a>({rx}) - У вас победитель <a href='tg://user?id={usid}'>{user_name}</a>", parse_mode='html')
                elif rx1<rx:
                    first_p.clear()
                    second_p.clear()
                    summ_stavka.clear()
                    cursor.execute("UPDATE users SET stavka=0 WHERE user_id=?", (usid,))
                    cursor.execute("UPDATE users SET stavka=0 WHERE user_id=?", (rid,))
                    cursor.execute(f"UPDATE users SET balance={balance - summ_stavka1} WHERE user_id={usid}")
                    cursor.execute(f"UPDATE users SET balance={balance2 + summ_stavka1} WHERE user_id={rid}")

                    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
                    await bot.send_message(callback_query.message.chat.id, f"<a href='tg://user?id={rid}'>{ruser_name}</a>({rx}), и <a href='tg://user?id={usid}'>{user_name}</a>({rx1}) - У вас победитель <a href='tg://user?id={rid}'>{ruser_name}</a>", parse_mode='html')
                else:
                    first_p.clear()
                    second_p.clear()
                    summ_stavka.clear()
                    cursor.execute("UPDATE users SET stavka=0 WHERE user_id=?", (usid,))
                    cursor.execute("UPDATE users SET stavka=0 WHERE user_id=?", (rid,))
                    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
                    await bot.send_message(callback_query.message.chat.id, f"🚫 Ничья ", parse_mode='html')
    else:
        await bot.answer_callback_query(callback_query.id, show_alert=False, text="‼️ Не твоё, не трогай!")    


@dp.callback_query_handler(lambda c: c.data == "gamestavka1")
async def gamest3(callback_query: types.CallbackQuery):
    user = await bot.get_chat(str(first_p[0]))
    replyuser = await bot.get_chat(str(second_p[0]))
    usid = user.id
    rid = replyuser.id

    if callback_query.from_user.id == replyuser.id or user.id:
        first_p.clear()
        second_p.clear()
        summ_stavka.clear()
        cursor.execute("UPDATE users SET stavka=0 WHERE user_id=?", (usid,))
        cursor.execute("UPDATE users SET stavka=0 WHERE user_id=?", (rid,))
        await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    else:
        await bot.answer_callback_query(callback_query.id, show_alert=False, text="‼️ Не твоё, не трогай!")

    
@dp.callback_query_handler(lambda c: c.data == "button_marry_y")
async def callback_marry_y(callback_query: types.CallbackQuery):
    user = await bot.get_chat(str(marry_me[0]))
    replyuser = await bot.get_chat(str(marry_rep[0]))
    usid = user.id
    rid = replyuser.id
    ruser_name = cursor.execute("SELECT user_name from users where user_id = ?",(rid,)).fetchone()
    ruser_name = ruser_name[0] 
    user_name = cursor.execute("SELECT user_name from users where user_id = ?",(usid,)).fetchone()
    user_name = user_name[0] 
    if callback_query.from_user.id == replyuser.id:
        cursor.execute(f'UPDATE users SET marry=? WHERE user_id=?', (replyuser.id, user.id,))
        cursor.execute(f'UPDATE users SET marry_time=? WHERE user_id=?', (time.time(), user.id,))
        cursor.execute(f'UPDATE users SET marry_date=? WHERE user_id=?', (datetime.now(), user.id,))

        cursor.execute(f'UPDATE users SET marry=? WHERE user_id=?', (user.id, replyuser.id,))
        cursor.execute(f'UPDATE users SET marry_time=? WHERE user_id=?', (time.time(), replyuser.id,))
        cursor.execute(f'UPDATE users SET marry_date=? WHERE user_id=?', (datetime.now(), replyuser.id,))
        connect.commit()

        marry_me.clear()
        marry_rep.clear() 
        await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
        await bot.send_message(callback_query.message.chat.id, f"💍 Вы приняли предложение о браке.\n👰‍♀️👨‍⚖️ С сегодняшего дня <a href='tg://user?id={usid}'>{user_name}</a> и <a href='tg://user?id={rid}'>{ruser_name}</a> состоят в браке.\n✨ Давайте поздравим молодожён!",  parse_mode='html')
    else:
        await bot.answer_callback_query(callback_query.id, show_alert=False, text="⚠️ Не твоё, не трогай!")

@dp.callback_query_handler(lambda c: c.data == "button_marry_n")
async def callback_marry_n(callback_query: types.CallbackQuery):
    user = await bot.get_chat(str(marry_me[0]))
    replyuser = await bot.get_chat(str(marry_rep[0]))
    if callback_query.from_user.id == replyuser.id:
       usid = user.id 
       user_name = cursor.execute("SELECT user_name from users where user_id = ?",(usid,)).fetchone()
       user_name = user_name[0]
       marry_me.clear()
       marry_rep.clear()
       await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
       await bot.send_message(callback_query.message.chat.id, f"💔 | <a href='tg://user?id={usid}'>{user_name}</a>, сожалеем, но вам отказали",  parse_mode='html')
    else:
       await bot.answer_callback_query(callback_query.id, show_alert=False, text="⚠️ Не твоё, не трогай!")

@dp.callback_query_handler(lambda c: c.data == "button_divorce_y")
async def callback_divorce_y(callback_query: types.CallbackQuery):
    user = await bot.get_chat(str(divorce_me[0]))
    if callback_query.from_user.id == user.id:
        replyuser = await bot.get_chat(str(divorce_rep[0]))
        usid = user.id
        rid = replyuser.id
        ruser_name = cursor.execute("SELECT user_name from users where user_id = ?",(rid,)).fetchone()
        ruser_name = ruser_name[0] 
        user_name = cursor.execute("SELECT user_name from users where user_id = ?",(usid,)).fetchone()
        user_name = user_name[0]
        get = cursor.execute("SELECT marry_time FROM users WHERE user_id=?", (user.id,)).fetchall()
        mtime = f"{int(get[0][0])}"
        marry_time = time.time() - float(mtime)
        vremya = strftime("%j дней %H часов %M минут", gmtime(marry_time))


        cursor.execute(f'UPDATE users SET marry=? WHERE user_id=?', (0, user.id,))
        cursor.execute(f'UPDATE users SET marry_time=? WHERE user_id=?', (0, user.id,))
        cursor.execute(f'UPDATE users SET marry_date=? WHERE user_id=?', (0, user.id,))

        cursor.execute(f'UPDATE users SET marry=? WHERE user_id=?', (0, replyuser.id,))
        cursor.execute(f'UPDATE users SET marry_time=? WHERE user_id=?', (0, replyuser.id,))
        cursor.execute(f'UPDATE users SET marry_date=? WHERE user_id=?', (0, replyuser.id,))
        connect.commit()
        divorce_me.clear()
        divorce_rep.clear()
        await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
        await bot.send_message(callback_query.message.chat.id, f"💔 Брак между <a href='tg://user?id={usid}'>{user_name}</a> и <a href='tg://user?id={rid}'>{ruser_name}</a> расторгнут.\n"
                                                               f"Он просуществовал {vremya}",  parse_mode='html')
    else:
        await bot.answer_callback_query(callback_query.id, show_alert=False, text="⚠️ Не твоё, не трогай!")

@dp.callback_query_handler(lambda c: c.data == "button_divorce_n")
async def callback_divorce_n(callback_query: types.CallbackQuery):
    user = await bot.get_chat(str(divorce_me[0]))
    if callback_query.from_user.id == user.id:
        divorce_me.clear()
        divorce_rep.clear()
        await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    else:
        await bot.answer_callback_query(callback_query.id, show_alert=False, text="⚠️ Не твоё, не трогай!")     


@dp.callback_query_handler(text_contains="check_")
async def checkrty(callback: types.CallbackQuery):
    bill = str(callback.data[6:])

    info = get_check(bill)

    user_id = callback.from_user.id
    if info != False:
        if str(p2p.check(bill_id=bill).status) == "PAID":
            user_money = cursor.execute(
                "SELECT money FROM fzve WHERE user_id=?", (callback.from_user.id,))
            user_money = cursor.fetchone()
            user_money = int(user_money[0])
            donate_coins = cursor.execute(
                "SELECT donate_coins FROM users WHERE user_id=?", (callback.from_user.id,))
            donate_coins = cursor.fetchone()
            donate_coins = int(donate_coins[0])
            cursor.execute(
                f"UPDATE users SET donate_coins={donate_coins + (user_money * 2)}  WHERE user_id={user_id}")

            await bot.send_message(callback.from_user.id, "Ваш счет оплачен")
            cursor.execute("DELETE FROM fzve WHERE bill_id= ?", (bill,))
            connect.commit()
            await bot.send_message(cfg.orig_channel, f"""<a href='tg://user?id={user_id}'>{user_name}</a>, спасибо за донат""", parse_mode='html')
        else:
            await bot.send_message(callback.from_user.id, "Вы не оплатили счет",
                                   reply_markup=buy_menu(False, bill=bill))
    else:
        await bot.send_message(callback.from_user.id, "Счет не найден")


async def q():

  cursor.execute(f"UPDATE users SET farm_coin = farm_coin + 250 * generator WHERE farm3")
  connect.commit()
  print("[LOG]Farm 3 work")
  cursor.execute(f"UPDATE users SET farm_coin = farm_coin + 500 * generator WHERE farm4")
  connect.commit()
  print("[LOG]Farm 4 work")
  cursor.execute(f"UPDATE users SET farm_coin = farm_coin + 150 * generator WHERE farm2")
  connect.commit()
  print("[LOG]Farm 2 work")
  cursor.execute(f"UPDATE users SET farm_coin = farm_coin + 100 * generator WHERE farm1")
  connect.commit()
  print("[LOG]Farm 1 work")
  cursor.execute(f"UPDATE users SET farm_coin = farm_coin + 3000 * generator WHERE farm5")
  connect.commit()
  print("[LOG]Farm 5 work")
  cursor.execute(f"UPDATE users SET bitmaning = bitmaning + 64 * vcard WHERE farmcoin3")
  connect.commit()
  print("[LOG]Ferm 3 work")
  cursor.execute(f"UPDATE users SET bitmaning = bitmaning + 650 * vcard WHERE farmcoin4")
  connect.commit()
  print("[LOG]Ferm 4 work")
  cursor.execute(f"UPDATE users SET bitmaning = bitmaning + 12 * vcard WHERE farmcoin2")
  connect.commit()
  print("[LOG]Ferm 2 work")
  cursor.execute(f"UPDATE users SET bitmaning = bitmaning + 4 * vcard WHERE farmcoin1")
  connect.commit()
  print("[LOG]Ferm 1 work")
  cursor.execute(f"UPDATE users SET bitmaning = bitmaning + 3500 * vcard WHERE farmcoin5")
  connect.commit()
  print("[LOG]Ferm 5 work")
  cursor.execute(f"UPDATE city SET material=material+ factory * 700")
  connect.commit()
  print("[LOG]city work")
  cursor.execute(f"UPDATE city SET kazna=kazna+work_place*(taxes*3.5) WHERE happynes>20 ")
  connect.commit()
  print("[LOG]city work")
  cursor.execute(f"UPDATE city SET citizens=citizens WHERE houses*15>citizens")
  connect.commit()
  print("[LOG]city work")
async def scheduler():
    aioschedule.every(60).minutes.do(q)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)

async def on_startup(_):
    asyncio.create_task(scheduler())
    await register_handlers(dp)

    await bot.send_message(
                chat_id=cfg.owner_id,text=
    f"""<b>🪄 Бот запущен!</b>
<code>{datetime.now().strftime("%d.%m.%y %H:%M:?")}</code>
"""

        ,parse_mode='html')

async def on_shutdown(_):
    await bot.send_message(
        chat_id=cfg.owner_id,
        text=f"<b>🪄 Бот Выкл!</b> ",parse_mode='html')


async def register_handlers(dp: Dispatcher):

   cursor.execute("INSERT INTO family_id VALUES(?);",(str(0)))


if __name__ == "__main__":
    try:
        executor.start_polling(dp, on_startup = on_startup, on_shutdown=on_shutdown, skip_updates=True)
    except Exception as e:
        print(f"{e}")