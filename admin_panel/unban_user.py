from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher import Dispatcher, filters
from aiogram.dispatcher.filters.state import State, StatesGroup


from config import dp, bot
import sql_server

@dp.message_handler((filters.RegexpCommandsFilter(regexp_commands=['unban \d*'])), state='*')
async def ban_user(message: types.Message, state: FSMContext):
 if sql_server.sql_server.check_user_rating_admin(message.from_user.id) == True:
  if int(message.from_user.id) == 1066122447:
    user_id = message.text.split(' ')[-1]
    if user_id.isdigit():
        mes = sql_server.sql_server.unban_user(str(user_id), str(message.from_user.id))
        await bot.send_message(message.from_user.id,text=mes[1])
    else:
        mes = sql_server.sql_server.unban_user_name(str(user_id), str(message.from_user.id))
        await bot.send_message(message.from_user.id,text=mes[1])
  else:
    pass
 else:
    pass
