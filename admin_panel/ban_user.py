from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher import Dispatcher, filters
from aiogram.dispatcher.filters.state import State, StatesGroup


from config import dp, bot
import sql_server
import datetime

class Ban(StatesGroup):
    ban = State()


@dp.message_handler((filters.RegexpCommandsFilter(regexp_commands=['ban \d*'])), state='*')
async def ban_user(message: types.Message, state: FSMContext):
 if sql_server.sql_server.check_user_rating_admin(message.from_user.id) == True:
    user_id = message.text.split(' ')[-1]
    print(user_id)
    if user_id.isdigit():
        check = sql_server.sql_server.get_info_user_id(str(user_id))
        if check == None:
            await bot.send_message(message.from_user.id,text='Нет такого пользователя')
        elif check[1] !=2:
            print(check)
            #['842925206', 2, 'ADDD', 'ИБ-12', 1]
            if len(check) == 6:
                print('GHJASDJHb')
                send = 'Пользователь - '+check[2]+'\nГруппа - '+check[3]

                keyboard = types.InlineKeyboardMarkup()
                row  = []
                row.append(types.InlineKeyboardButton(text='🅱️AN?', callback_data='ban_'+str(check[0])))
                row.append(types.InlineKeyboardButton(text='🅱️AN + удалить его работы ('+str(check[4])+')?', callback_data='banworks_'+str(check[0])))
                keyboard.row(*row)
                keyboard.add(types.InlineKeyboardButton(text='Отмена', callback_data='cancel'))
                await Ban.ban.set()
                await bot.send_message(message.from_user.id,text=send,reply_markup=keyboard)
        else:
            await bot.send_message(message.from_user.id,text='Пользователь уже забанен')

    elif user_id.isdigit() == False:
        check = sql_server.sql_server.get_info_user_name(str(user_id))
        print(check)
        #['842925206', 2, 'ADDD', 'ИБ-12', 1]
        if check == None:
            await bot.send_message(message.from_user.id,text='Нет такого пользователя')
        elif len(check) == 6:
            if check[1] !=2:
                send = 'Пользователь'+check[2]+'\nГруппа '+check[3]

                keyboard = types.InlineKeyboardMarkup()
                row  = []
                row.append(types.InlineKeyboardButton(text='🅱️AN?', callback_data='ban_'+str(check[0])))
                row.append(types.InlineKeyboardButton(text='🅱️AN+ удалить_раб('+str(check[4])+')?', callback_data='banworks_'+str(check[0])))
                keyboard.row(*row)
                keyboard.add(types.InlineKeyboardButton(text='Отмена', callback_data='cancel'))
                await Ban.ban.set()
                await bot.send_message(message.from_user.id,text=send,reply_markup=keyboard)
            else:
                await bot.send_message(message.from_user.id,text='Пользователь уже забанен')

 else:
    pass

@dp.callback_query_handler(lambda c: 'ban_' in c.data, state=Ban.ban)
async def act(message: types.Message, state: FSMContext):
        await bot.delete_message(message.from_user.id, message.message.message_id)
        user_id = message.data.split('_')[-1]
        print(user_id)
        mes = sql_server.sql_server.ban_user(str(user_id), str(message.from_user.id))
        await bot.send_message(message.from_user.id,text=mes[1])

@dp.callback_query_handler(lambda c: 'banworks_' in c.data, state=Ban.ban)
async def actw(message: types.Message, state: FSMContext):
        await bot.delete_message(message.from_user.id, message.message.message_id)
        user_id = message.data.split('_')[-1]
        print(user_id)
        sql_server.sql_server.delete_all_users_works(user_id)
        mes = sql_server.sql_server.ban_user(str(user_id), str(message.from_user.id))
        await bot.send_message(message.from_user.id,text=mes[1])

@dp.callback_query_handler(lambda c: c.data == 'cancel', state=Ban.ban)
async def act(message: types.Message, state: FSMContext):
        await bot.delete_message(message.from_user.id, message.message.message_id)
        await state.finish()