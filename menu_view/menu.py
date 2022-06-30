from aiogram import types
from config import dp, bot

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

import sql_server


@dp.message_handler(commands=['menu'], state="*")
async def menu(message: types.Message):
  if sql_server.sql_server.check_user_rating(message.chat.id) == True:
     print(message.chat.id)
     if sql_server.sql_server.sql_check_base(message.chat.id) == True:
          keyboard = types.InlineKeyboardMarkup()
          key_yes = types.InlineKeyboardButton(text='Посмотреть', callback_data='view');
          keyboard.add(key_yes);
          key_no= types.InlineKeyboardButton(text='Загрузить', callback_data='upload');
          keyboard.add(key_no);
          key_no= types.InlineKeyboardButton(text='Удалить', callback_data='delete_works_and_files');
          keyboard.add(key_no);
          key_no= types.InlineKeyboardButton(text='Отмена', callback_data='cancel');
          keyboard.add(key_no);
          await bot.send_message(message.from_user.id, text = "Выбери действие:", reply_markup=keyboard)

  elif sql_server.sql_server.check_user_rating(message.chat.id) == None:
          await bot.send_message(message.from_user.id, text = "У тебя нет профиля, создать профиль:\n /muser")
  else:
          await bot.send_message(message.chat.id, 'Вы забанены')

@dp.callback_query_handler(lambda c: c.data == 'view', state='*')
async def menu(message: types.Message):
     keyboard = types.InlineKeyboardMarkup()
     key_yes = types.InlineKeyboardButton(text='Посмотреть Фотографии', callback_data='view_works');
     keyboard.add(key_yes);
     key_yes = types.InlineKeyboardButton(text='Посмотреть Файлы', callback_data='view_files');
     keyboard.add(key_yes);
     key_no= types.InlineKeyboardButton(text='<<<', callback_data='back');
     keyboard.add(key_no);
     await bot.edit_message_text(chat_id=message.message.chat.id, message_id=message.message.message_id,text = message.message.text, reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data =='back', state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
     keyboard = types.InlineKeyboardMarkup()
     key_yes = types.InlineKeyboardButton(text='Посмотреть', callback_data='view');
     keyboard.add(key_yes);
     key_no= types.InlineKeyboardButton(text='Загрузить', callback_data='upload');
     keyboard.add(key_no);
     key_no= types.InlineKeyboardButton(text='Удалить', callback_data='delete_works_and_files');
     keyboard.add(key_no);
     key_no= types.InlineKeyboardButton(text='Отмена', callback_data='cancel');
     keyboard.add(key_no);
     await bot.edit_message_text(chat_id=message.message.chat.id, message_id=message.message.message_id,text = message.message.text, reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data == 'upload', state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
     keyboard = types.InlineKeyboardMarkup()
     key_no= types.InlineKeyboardButton(text='Загрузить Фотографии ', callback_data='upload_works');
     keyboard.add(key_no);
     key_no= types.InlineKeyboardButton(text='Загрузить Файлы ', callback_data='upload_files');
     keyboard.add(key_no);
     key_no= types.InlineKeyboardButton(text='<<<', callback_data='back');
     keyboard.add(key_no);
     await bot.edit_message_text(chat_id=message.message.chat.id, message_id=message.message.message_id,text = message.message.text, reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data == 'cancel', state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
     await bot.delete_message(message.from_user.id, message.message.message_id)
