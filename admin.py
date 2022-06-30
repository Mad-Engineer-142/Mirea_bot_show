from aiogram import types
from config import dp, bot, admins_id

from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher, filters

import datetime
import sql_server
import pickle
from PIL import Image
import admin_panel


class Au(StatesGroup):
    nexts = State()
#______________________________________________________________________________________________

@dp.message_handler(commands=['admin'], state='*')
async def starts(message: types.Message, state: FSMContext):
    if sql_server.sql_server.check_user_rating_admin(message.from_user.id) == True:
        buttons = sql_server.sql_server.admin_buttons()
        if int(message.from_user.id) == admins_id:
            await bot.send_message(message.from_user.id,text='''Велком ту админ панель \n Здесь вы будете вершить судьбы людей в Mirea_bot. \n Вы можете банить работы и разбанить работы -\nКнопка внизу\n банить людей - /ban + (id / Никнейм), \n разбанить людей - /unban + (id / Никнейм),\n /add_admin + (id / Никнейм) \n /re_admin + (id / Никнейм) \n /all_users \n /all_admins''',reply_markup=buttons)
        else:
            await bot.send_message(message.from_user.id,text='''Велком ту админ панель \n Здесь вы будете вершить судьбы людей в Mirea_bot. \n Вы можете банить работы и разбанить работы -\nКнопка внизу\n банить людей - /ban + (id / Никнейм), \n разбанить людей - /unban + (id / Никнейм),''',reply_markup=buttons)
        await Au.nexts.set()
        await state.update_data(n=0)

    else:
        pass
#______________________________________________________________________________________________

@dp.message_handler(filters.RegexpCommandsFilter(regexp_commands=['\A/(\d*) d\Z']), state='*')
async def del_work_by_id(message: types.Message, state: FSMContext):
 if sql_server.sql_server.check_user_rating_admin(message.from_user.id) == True:
        num = message.text.split(' ')[0][1:]
        print(num)
        if num.isdigit():
            if int(num) in sql_server.sql_server.unique_num_ask_arr():
                sql_server.sql_server.delete_thms(int(num))
                await bot.send_message(message.from_user.id, text='Вы удалили работу /'+str(num))
            else:
                await bot.send_message(message.from_user.id, text='Такой работы нет, проверь правильность индификатора')
        else:
            await bot.send_message(message.from_user.id, text='Некорректно введен индификатор')
 else:
        pass
#______________________________________________________________________________________________
  
@dp.message_handler((filters.RegexpCommandsFilter(regexp_commands=['add_admin \d*'])), state='*')
async def add_admin_(message: types.Message, state: FSMContext):
 if sql_server.sql_server.check_user_rating_admin(message.from_user.id) == True:
  if int(message.from_user.id) == admins_id:
    user_id = message.text.split(' ')[-1]
    if user_id.isdigit():
        mes = sql_server.sql_server.add_admin(str(user_id), str(message.from_user.id))
        print(mes)
        await bot.send_message(message.from_user.id,text=mes[1])
    else:
        print(user_id)
        mes = sql_server.sql_server.add_admin_name(str(user_id), str(message.from_user.id))
        print(mes)
        await bot.send_message(message.from_user.id,text=mes[1])
  else:
    pass
 else:
    pass
#______________________________________________________________________________________________

@dp.message_handler((filters.RegexpCommandsFilter(regexp_commands=['re_admin \d*'])), state='*')
async def re_admin(message: types.Message, state: FSMContext):
 if sql_server.sql_server.check_user_rating_admin(message.from_user.id) == True:
  if int(message.from_user.id) == admins_id:
    user_id = message.text.split(' ')[-1]
    if user_id.isdigit():
        mes = sql_server.sql_server.remove_admin(str(user_id), str(message.from_user.id))
        await bot.send_message(message.from_user.id,text=mes[1])
    else:
        mes = sql_server.sql_server.remove_admin_name(str(user_id), str(message.from_user.id))
        await bot.send_message(message.from_user.id,text=mes[1])
  else:
    pass
 else:
    pass
#______________________________________________________________________________________________

@dp.message_handler((filters.RegexpCommandsFilter(regexp_commands=['all_users'])), state='*')
async def all_users(message: types.Message, state: FSMContext):
 if sql_server.sql_server.check_user_rating_admin(message.from_user.id) == True:
        text = sql_server.sql_server.all_users()
        if text:
            send = 'Никнейм     - id\n   ________________________\n'
            for i in range(len(text[0])):
                if text[2][i] == 0:
                    status = 'Обч'
                elif text[2][i] == 2:
                    status = 'Ban'
                elif text[2][i] == 5:
                    status = 'Admin'
                elif text[2][i] == 3:
                    status = 'Redactor'
                else:
                    status = str(text[2][i])

                send = send+str(i)+'| '+text[0][i]+' - '+text[1][i]+' - '+status+"\n"
            way_to_txt = "temp_files/all_users.txt"
            with open(way_to_txt,'w',encoding='utf8') as f:
                f.write(str(send))
            await bot.send_document(chat_id=message.from_user.id,document=types.InputFile(way_to_txt))
 else:
    pass
#______________________________________________________________________________________________

@dp.message_handler((filters.RegexpCommandsFilter(regexp_commands=['all_admins'])), state='*')
async def all_admins(message: types.Message, state: FSMContext):
 if int(message.from_user.id) == admins_id:
        text = sql_server.sql_server.all_admins()
        if text:
            send = 'Никнейм     - id\n   __________________\n'
            for i in range(len(text[0])):

                send = send+str(i)+'| '+text[0][i]+' - '+text[1][i]+"\n"
            await bot.send_message(message.from_user.id,text=send)
 else:
    pass
#______________________________________________________________________________________________
