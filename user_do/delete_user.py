from config import dp
from aiogram import types
from config import dp, bot

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

import sql_server
class Delete_user(StatesGroup):
    waiting_for_user = State()

@dp.message_handler(text=['Удалить пользователя'],state='*')
async def muser(message: types.Message, state: FSMContext):
  if sql_server.sql_server.check_user_rating(message.from_user.id) == True:
    if sql_server.sql_server.sql_check_base(message.chat.id) == True:
        keyboard = types.InlineKeyboardMarkup()
        key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes_delete');
        keyboard.add(key_yes);
        key_no= types.InlineKeyboardButton(text='Отмена', callback_data='cancel');
        keyboard.add(key_no);
        mes = await bot.send_message(chat_id = message.chat.id, text = "Ты точно хочешь удалить свой профиль?", reply_markup=keyboard)

        await state.update_data(mes=mes)
        await Delete_user.next()
  elif sql_server.sql_server.check_user_rating(message.from_user.id) == None:
    await bot.send_message(message.chat.id, 'У вас еще нет профиля. Создать - /muser')
  else:
    await bot.send_message(message.chat.id, 'Вы забанены')


@dp.callback_query_handler(lambda c: c.data == 'yes_delete', state=Delete_user.waiting_for_user)
async def cancel_handler(message: types.Message, state: FSMContext):
    
      user_data = await state.get_data()
      await bot.delete_message(user_data['mes'].chat.id, user_data['mes'].message_id)
      sql_server.sql_server.sql_delete_base_user(user_data['mes'].chat.id)
      await bot.send_message(user_data['mes'].chat.id, 'Вы удалили свой профиль\n До свидания',reply_markup=types.ReplyKeyboardRemove())
      await state.finish()

@dp.callback_query_handler(lambda c: c.data == 'cancel', state=Delete_user.waiting_for_user)
async def cancel_handler(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    await bot.delete_message(user_data['mes'].chat.id, user_data['mes'].message_id)
    await state.finish()