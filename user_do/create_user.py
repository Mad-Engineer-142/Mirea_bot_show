from aiogram import types
from config import dp, bot

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

import sql_server
import skins

class Making_user(StatesGroup):
    waiting_for_user_name = State()
    waiting_for_user_group = State()
    waiting_for_user_id = State()

@dp.message_handler(commands=['muser'], state="*")
async def muser(message: types.Message):
    if sql_server.sql_server.check_user_rating(message.from_user.id) == True:
        await bot.send_message(message.chat.id,'''Ты не можешь создать нового пользователя пока у тебя есть старый\nУдалить - /deluser\nПереименновать - /reuser\nПолучить информацию о существующем - /info''')
    elif sql_server.sql_server.check_user_rating(message.from_user.id) == None:
        await bot.send_message(message.chat.id, 'Создаем нового пользователя, назови его!')
        await Making_user.waiting_for_user_name.set()
    else:
        await bot.send_message(message.chat.id, 'Вы забанены')



@dp.message_handler(state=Making_user.waiting_for_user_name, content_types=types.ContentTypes.TEXT)
async def user_name(message: types.Message, state: FSMContext): 
    if sql_server.sql_server.sql_check_base_name(message.text):
        await message.reply("Такой Никнейм уже существует, попробуте другой.")
        return
    await state.update_data(user_name=message.text)

    await Making_user.next()  # для простых шагов можно не указывать название состояния, обходясь next()
    await message.answer("Теперь Напишие название своей группы. Пример: ИБ-12:")

@dp.message_handler(state=Making_user.waiting_for_user_group, content_types=types.ContentTypes.TEXT)
async def user_group(message: types.Message, state: FSMContext):
     if '-' not in message.text:
            await message.reply('Неправильная группа, напиши еще раз. Пример: ИБ-12')
            return
    
     group_lst = message.text.split('-')
     if not group_lst[1].isdigit() :
            await message.reply('Некорректно введена группа, напиши еще раз. Пример: ПКС-11')
            return
     elif not group_lst[0].isalpha(): 
            await message.reply('Некорректно введена группа, напиши еще раз. Пример: ИКС-13')
            return
     await state.update_data(user_group=message.text)
     user_data = await state.get_data()

     keyboard = types.InlineKeyboardMarkup()
     key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes_create');
     keyboard.add(key_yes);
     key_no= types.InlineKeyboardButton(text='Отмена', callback_data='cancel');
     keyboard.add(key_no);
     mes = await message.answer(f"{user_data['user_name']}  - Ваш Никнейм  \n {message.text} - ваша группа \n создать профиль?", reply_markup=keyboard)
     await state.update_data(mes=mes)
     await Making_user.next()

@dp.callback_query_handler(lambda c: c.data == 'yes_create', state=Making_user.waiting_for_user_id)
async def cancel_handler(message: types.Message, state: FSMContext):
      user_data = await state.get_data()
      await bot.delete_message(user_data['mes'].chat.id, user_data['mes'].message_id)
      sql_server.sql_server.sql_write_base_user(message.from_user.id, user_data['user_name'], user_data['user_group']) #chat_id,user_name, group
      
      fill = skins.skin_changer.see_default().split('ᛣ')
      print(fill)
      fill = str(fill[0]).split('/')
      print(fill)
      markup5 = types.ReplyKeyboardMarkup().row(types.KeyboardButton(fill[0]), fill[1])
      markup5.row(types.KeyboardButton(fill[2]), types.KeyboardButton(fill[3]))
      markup5.row(types.KeyboardButton(fill[4]), types.KeyboardButton(fill[5]))

      await bot.send_message(user_data['mes'].chat.id, 'Поздравляю, вы создали нового пользователя',reply_markup=markup5)
      await state.finish()
@dp.callback_query_handler(lambda c: c.data == 'cancel', state = Making_user.waiting_for_user_id)
async def cancel_handler(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    await bot.delete_message(user_data['mes'].chat.id, user_data['mes'].message_id)
    await state.finish()