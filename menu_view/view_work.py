from aiogram import types
from config import dp, bot

from aiogram.dispatcher import FSMContext, filters
from aiogram.dispatcher.filters.state import State, StatesGroup

import re
import datetime
import sql_server
import pickle
from PIL import Image
import skins

class Moving(StatesGroup):
	moving = State()



@dp.message_handler(text='📝Посмотреть Работы', state='*')
async def view_works(message: types.Message, state: FSMContext):
		keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).row('<<<')
		await bot.send_message(message.from_user.id, text='-', reply_markup=keyboard)
		menu = sql_server.sql_server.see_data()
		await bot.send_message(message.from_user.id, text=menu[0], reply_markup=menu[1])
		await Moving.moving.set()
		await state.update_data(n=0)

@dp.callback_query_handler(lambda c: c.data == 'next_page',state=Moving.moving)
@dp.callback_query_handler(lambda c: c.data == 'back_page',state=Moving.moving)
@dp.callback_query_handler(lambda c: c.data in ['математика','физика','родной язык','астрономия','русский язык','иностранный язык','информатика','история','обж','технология','литература','география','химия'],state=Moving.moving)
async def view_works(message: types.Message, state: FSMContext):
		await bot.delete_message(message.from_user.id, message.message.message_id)

		if message.data == 'next_page':
			move = await state.get_data()
			n_new = move['n']

			await state.update_data(n=n_new+1)
			mesg_list=move['mesg_list']
			for i in mesg_list:
				for a in i:
					await bot.delete_message(message.from_user.id, a.message_id)

		elif message.data == 'back_page':
			move = await state.get_data()
			n_new = move['n']

			await state.update_data(n=n_new-1)
			mesg_list=move['mesg_list']
			for i in mesg_list:
				for a in i:
					await bot.delete_message(message.from_user.id, a.message_id)
		else:
			await state.update_data(sub=message.data)

		move = await state.get_data()
		n = move['n']
		mesg_list = []
		num = []
		show_img = sql_server.sql_server.show_data(move['sub'])
		len_of_photos = len(show_img)
		show_img = show_img[0+4*n:4+4*n]
	   
		if len_of_photos%4 != 0:
			max_n = int(len_of_photos/4)+1
		else:
			max_n = int(len_of_photos/4)

		for i in range(len(show_img)):
			image_text_arr = list(show_img[i])
			mas = pickle.loads(image_text_arr[0]) 

			media = types.MediaGroup()  
			for a in range(len(mas)):
				if a == 0:
					media.attach_photo(types.InputFile(mas[a]), image_text_arr[1])
					num.append(image_text_arr[2])
				else:
					media.attach_photo(types.InputFile(mas[a]))
			img_msg = await bot.send_media_group(message.from_user.id, media=media)

			mesg_list.append(img_msg)    
		if n+1 == int(1) != max_n:
				keyboard = types.InlineKeyboardMarkup()
				row  = []
				row.append(types.InlineKeyboardButton(text='⛔', callback_data='null'))
				row.append(types.InlineKeyboardButton(text='❌', callback_data='x'))
				row.append(types.InlineKeyboardButton(text='⚠', callback_data='report'))
				row.append(types.InlineKeyboardButton(text='▶', callback_data='next_page'))
				keyboard.row(*row)
		elif n+1 == max_n != 1:
				keyboard = types.InlineKeyboardMarkup()
				row  = []
				row.append(types.InlineKeyboardButton(text='◀', callback_data='back_page'))
				row.append(types.InlineKeyboardButton(text='❌', callback_data='x'))
				row.append(types.InlineKeyboardButton(text='⚠', callback_data='report'))
				row.append(types.InlineKeyboardButton(text='⛔', callback_data='null'))
				keyboard.row(*row)
		elif n+1 == max_n == int(1):
				keyboard = types.InlineKeyboardMarkup()
				row  = []
				row.append(types.InlineKeyboardButton(text='⛔', callback_data='null'))
				row.append(types.InlineKeyboardButton(text='❌', callback_data='x'))
				row.append(types.InlineKeyboardButton(text='⚠', callback_data='report'))
				row.append(types.InlineKeyboardButton(text='⛔', callback_data='null'))
				keyboard.row(*row)
		else:
				keyboard = types.InlineKeyboardMarkup()
				row  = []
				row.append(types.InlineKeyboardButton(text='◀', callback_data='back_page'))
				row.append(types.InlineKeyboardButton(text='❌', callback_data='x'))
				row.append(types.InlineKeyboardButton(text='⚠', callback_data='report'))
				row.append(types.InlineKeyboardButton(text='▶', callback_data='next_page'))
				keyboard.row(*row)  
		await bot.send_message(message.message.chat.id ,text=str(n+1)+' / '+str(max_n), reply_markup=keyboard)
		await state.update_data(mesg_list=mesg_list)
		await state.update_data(num=num)



@dp.callback_query_handler(lambda c: c.data == 'null',state=Moving.moving)
async def null(message: types.Message, state: FSMContext):
	pass

@dp.callback_query_handler(lambda c: c.data == 'x',state=Moving.moving)
async def null(message: types.Message, state: FSMContext):
	await bot.delete_message(message.from_user.id, message.message.message_id)
	move = await state.get_data()
	mesg_list=move['mesg_list']
	for i in mesg_list:
		print(i)
		for a in i:
			await bot.delete_message(message.from_user.id, a.message_id)
	fill = skins.skin_changer.see_default().split('ᛣ')
	fill = str(fill[0]).split('/')
	markup5 = types.ReplyKeyboardMarkup().row(
	    types.KeyboardButton(fill[0]), fill[1])
	markup5.row(types.KeyboardButton(fill[2]), types.KeyboardButton(fill[3]))
	markup5.row(types.KeyboardButton(fill[4]), types.KeyboardButton(fill[5]))
	await bot.send_message(message.message.chat.id, 'Меню',reply_markup=markup5)
	await state.finish()

@dp.callback_query_handler(lambda c: c.data == 'report',state=Moving.moving)
async def null(message: types.Message, state: FSMContext):
	move = await state.get_data()
	mesg_list=move['mesg_list']
	num = move['num']
	keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=False)
	keyboard.add(types.KeyboardButton(text='<<<'))
	for i in range(len(mesg_list)):
				if len(mesg_list) == 2:
					keyboard.add(types.KeyboardButton(text='/'+str(num[i])+'_report'))
				else:
					keyboard.add(types.KeyboardButton(text='/'+str(num[i])+'_report'))
	await bot.send_message(message.message.chat.id ,text='Меню репорта:', reply_markup=keyboard)


@dp.message_handler(regexp=r'\d*_report',state=Moving.moving)
async def report(message: types.Message, state: FSMContext):
	await bot.delete_message(message.from_user.id, message.message_id)

	string_text = message.text
	string = str(string_text.split('_')[0])[1:]
	await bot.send_message(message.chat.id ,text = 'Вы кинули репорт на работу /'+string)
	if string.isdigit():
		print(string)
		user_id = sql_server.sql_server.warn_work(str(string))
		user_id = list(user_id)[0]
		keyboard = types.ReplyKeyboardMarkup()
		await bot.send_message(chat_id=user_id ,text = 'На вашу работу(/'+str(string)+') был кинут репорт',reply_markup=keyboard)