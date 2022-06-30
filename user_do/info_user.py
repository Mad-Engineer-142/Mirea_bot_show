from config import dp
from aiogram import types
from config import dp, bot

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

import sql_server

@dp.message_handler(commands=['info'], state="*")
@dp.message_handler(text='📊Профиль', state="*")
async def muser(message: types.Message, state: FSMContext):
  print(sql_server.sql_server.sql_check_base(message.from_user.id))
  if sql_server.sql_server.check_user_rating(message.from_user.id) == True:
        if sql_server.sql_server.sql_check_base(message.chat.id) == True:

           print(sql_server.sql_server.get_info_user_id(message.from_user.id)[4])

           df = sql_server.sql_server.sql_info_base_user(message.chat.id)
           if df[2] == 5:
                word = 'Вы Админ'
           elif df[2] == 3:
                word = 'Вы редактор'
           elif df[2] == 0:
                word = 'Вы обычный юзер'
           info = sql_server.sql_server.get_info_user_id(message.from_user.id)

           if info[4] == None:
               st = 'Информация о тебе:'+'\n'+'-----------------'+'\n' + str(df[0])+' -твой никнейм '+'\n' +str(df[1])+' -твоя группа '+'\n' +str(df[2])+' -твой рейтинг \n'+word +'\n'+'-----------------'+'\n'+str(info[5])+' -Работ загружено'+'\n'+ '❌Страница в VK не привязана (Настройки)'
           else:
               st = 'Информация о тебе:'+'\n'+'-----------------'+'\n' + str(df[0])+' -твой никнейм '+'\n' +str(df[1])+' -твоя группа '+'\n' +str(df[2])+' -твой рейтинг \n'+word +'\n'+'-----------------'+'\n'+str(info[5])+' -Работ загружено'+'\n'+'🔗'+str(info[4]) +' - Страница в VK  привязана'
            
           await bot.send_message(message.chat.id,st)
  elif  sql_server.sql_server.check_user_rating(message.from_user.id) == None:
        await bot.send_message(message.chat.id,'Дружок-пирожок, ты ошибся коммандой, у тебя еще нет профиля\n Создать профиль - /muser')
  else:
        await bot.send_message(message.chat.id,'Вы забанены')