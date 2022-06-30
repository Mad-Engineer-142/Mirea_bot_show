import sqlite3
import sql_server
from aiogram import types
from config import dp, bot

from aiogram.dispatcher import FSMContext, filters
from aiogram.dispatcher.filters.state import State, StatesGroup

class Alert(StatesGroup):
	alert = State()


@dp.message_handler(commands=['alert'], state='*')
async def alert(message: types.Message, state: FSMContext):
	if sql_server.sql_server.check_user_rating_admin(message.from_user.id) == True:
		keyboard = types.InlineKeyboardMarkup()
		row=[]
		row.append(types.InlineKeyboardButton(text='⛔Отмена⛔', callback_data='no'))
		keyboard.row(*row)
		await bot.send_message(message.from_user.id, text='Напиши сообщение, которое будет видно всем', reply_markup= keyboard)
		await Alert.alert.set()
		await state.update_data(b=message)

@dp.message_handler(state=Alert.alert)
async def textalert(message: types.Message, state: FSMContext):
	print(message.text)
	move = await state.get_data()
	b = move['b']
	users_id = sql_server.sql_server.get_users_ids_alert()
	await bot.delete_message(b.from_user.id, b.message_id)
	for i in users_id:
		print(i)
		try:
			await bot.send_message(i, text=message.text)
		except:
			pass
	await state.finish()

@dp.callback_query_handler(lambda c: c.data == 'no',state=Alert.alert)
async def null(message: types.Message, state: FSMContext):
	await bot.delete_message(message.from_user.id, message.message.message_id)
	await state.finish()