from aiogram import types
from config import dp, bot

from aiogram.dispatcher import Dispatcher, filters
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

import sql_server
import pickle

@dp.message_handler(filters.RegexpCommandsFilter(regexp_commands=['\A/(\d*)\Z']), state='*')
async def un(message: types.Message, state: FSMContext):
  if sql_server.sql_server.check_user_rating(message.from_user.id) == True:
    if sql_server.sql_server.sql_check_base(message.chat.id) == True:
      if message.text[1:]:
        print(sql_server.sql_server.unique_num_ask_arr())
        if int(message.text[1:]) == 0:
            await bot.send_message(message.chat.id, text='Хаха, подловить меня хотел! НЕе.')    
            pass
        elif int(message.text[1:]) in sql_server.sql_server.unique_num_ask_arr():
            print(message.text[1:])
            works = sql_server.sql_server.show_work_unique(str(message.text[1:]))
            print(works)
            #works = list(works[0])
            if works[2] == 'p':
                images = pickle.loads(works[0])
                media = types.MediaGroup()
                for u in range(len(images)):
                    if u == 0:
                        media.attach_photo(types.InputFile(images[u]),works[1])
                    else:
                        media.attach_photo(types.InputFile(images[u]))
                await bot.send_media_group(message.from_user.id, media=media)
            elif works[2] == 'f':
                images = pickle.loads(works[0])
                await bot.send_document(chat_id=message.from_user.id,document=types.InputFile(images, works[3]),caption=works[1])
        else:
            await bot.send_message(message.chat.id, text="Такой работы нет, проверь правильность индификатора")

  elif  sql_server.sql_server.check_user_rating(message.from_user.id) == None:
        await bot.send_message(message.chat.id,'Вы ошибсись коммандой, у вас еще нет профиля\n Создать профиль - /muser')
  else:
        await bot.send_message(message.chat.id,'Вы забанены')
