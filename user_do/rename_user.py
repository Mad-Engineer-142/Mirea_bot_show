from aiogram import types
from config import dp, bot

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

import sql_server
import skins

class Rename_user(StatesGroup):
    waiting_for_user_new_name = State()
    waiting_for_user_new_confirm = State()


@dp.message_handler(text=['Переименовать пользователя'],state='*')
async def muser(message: types.Message):
  if sql_server.sql_server.check_user_rating(message.from_user.id) == True:
    if sql_server.sql_server.sql_check_base(message.chat.id) == True:
        await bot.send_message(message.chat.id, 'Дай своему профилю новое имя!',reply_markup=types.ReplyKeyboardRemove())
        await Rename_user.waiting_for_user_new_name.set()

  elif sql_server.sql_server.check_user_rating(message.from_user.id) == None:
        message = await bot.send_message(message.chat.id,'Дружок-пирожок, ты ошибся коммандой, у тебя еще нет профиля\n Создать профиль - /muser',reply_markup=types.ReplyKeyboardRemove())
        await state.finish()
        await user_do.create_user.muser(message)
  else:
    await bot.send_message(message.chat.id,'Вы забанены')



@dp.message_handler(state=Rename_user.waiting_for_user_new_name, content_types=types.ContentTypes.TEXT)
async def user_group(message: types.Message, state: FSMContext):
    if sql_server.sql_server.sql_check_base_name(message.text):
        await message.reply("Такой Никнейм уже существует, попробуте другой.")
        return
    else:
        await state.update_data(user_name=message.text)

    keyboard = types.InlineKeyboardMarkup()
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes_rename');
    keyboard.add(key_yes);
    key_no= types.InlineKeyboardButton(text='Отмена', callback_data='cancel');
    keyboard.add(key_no);
    mes = await message.answer(f"Вы точно хотите переименовать свой профиль?", reply_markup=keyboard)
    await state.update_data(mes=mes)
    await Rename_user.next()

@dp.callback_query_handler(lambda c: c.data == 'yes_rename', state=Rename_user.waiting_for_user_new_confirm)
async def cancel_handler(message: types.Message, state: FSMContext):
      user_data = await state.get_data()
      await bot.delete_message(user_data['mes'].chat.id, user_data['mes'].message_id)
      sql_server.sql_server.sql_rename_base_user(user_data['user_name'], message.from_user.id) 
      await bot.send_message(user_data['mes'].chat.id, 'Вы переименовали свой профиль')
      df = sql_server.sql_server.sql_info_base_user(user_data['mes'].chat.id)
      print(df)
      st = 'Информация о тебе:'+'\n' + str(df[0])+' -твой никнейм '+'\n' +str(df[1])+' -твоя группа '+'\n' +str(df[2])+' -твой рейтинг'
      fill = skins.skin_changer.see_default().split('ᛣ')
      fill = str(fill[0]).split('/')
      markup5 = types.ReplyKeyboardMarkup().row(
        types.KeyboardButton(fill[0]), fill[1])
      markup5.row(types.KeyboardButton(fill[2]), types.KeyboardButton(fill[3]))
      markup5.row(types.KeyboardButton(fill[4]), types.KeyboardButton(fill[5]))
      await bot.send_message(user_data['mes'].chat.id, text=st, reply_markup=markup5)
      await state.finish()

@dp.callback_query_handler(lambda c: c.data == 'cancel', state = Rename_user.waiting_for_user_new_confirm)
async def cancel_handler(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    await bot.delete_message(user_data['mes'].chat.id, user_data['mes'].message_id)

    fill = skins.skin_changer.see_default().split('ᛣ')
    fill = str(fill[0]).split('/')
    markup5 = types.ReplyKeyboardMarkup().row(
      types.KeyboardButton(fill[0]), fill[1])
    markup5.row(types.KeyboardButton(fill[2]), types.KeyboardButton(fill[3]))
    markup5.row(types.KeyboardButton(fill[4]), types.KeyboardButton(fill[5]))
    await bot.send_message(message.message.chat.id, text='Отмена', reply_markup=markup5)
    await state.finish()