from aiogram import types
from config import dp, bot

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

import datetime
import sql_server
import pickle
import skins

class Moving(StatesGroup):
	moving_files = State()


@dp.message_handler(text='💽Посмотреть Файлы', state='*')
async def view_files(message: types.Message, state: FSMContext):
		keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).row('<<<')
		await bot.send_message(message.from_user.id, text='-', reply_markup=keyboard)
		menu = sql_server.sql_server.see_data_file()
		await bot.send_message(message.from_user.id, text=menu[0], reply_markup=menu[1])
		await Moving.moving_files.set()
		await state.update_data(n=0)


@dp.callback_query_handler(lambda c: c.data == 'next_page_file',state=Moving.moving_files)
@dp.callback_query_handler(lambda c: c.data == 'back_page_file',state=Moving.moving_files)
@dp.callback_query_handler(lambda c: c.data in ['математика','физика','родной язык','астрономия','русский язык','иностранный язык','информатика','история','обж','технология','литература','география','химия'],state=Moving.moving_files)
async def view_files(message: types.Message, state: FSMContext):
		await bot.delete_message(message.from_user.id, message.message.message_id)
		if message.data == 'next_page_file':
			move = await state.get_data()
			n_new = move['n']

			await state.update_data(n=n_new+1)
			mesg_list_file=move['mesg_list_file']
			for i in mesg_list_file:
				await bot.delete_message(message.from_user.id, i.message_id)

		elif message.data == 'back_page_file':
			move = await state.get_data()
			n_new = move['n']

			await state.update_data(n=n_new-1)
			mesg_list_file=move['mesg_list_file']
			for i in mesg_list_file:
				await bot.delete_message(message.from_user.id, i.message_id)
		else:
			await state.update_data(sub=message.data)

		move = await state.get_data()
		n = move['n']
		mesg_list_file = []
		num = []
		show_img = sql_server.sql_server.show_data_file(move['sub'])
		len_of_photos = len(show_img)
		show_img = show_img[0+4*n:4+4*n]
	   
		if len_of_photos%4 != 0:
			max_n = int(len_of_photos/4)+1
		else:
			max_n = int(len_of_photos/4)

		for i in range(len(show_img)):
			image_text_arr = list(show_img[i])
			keyboard = types.InlineKeyboardMarkup()
			print(image_text_arr[1].split('|')[0])
			key_yes =types.InlineKeyboardButton(text='скачать', callback_data=image_text_arr[1].split('|')[0])
			print(image_text_arr[3])
			num.append(image_text_arr[3])
			keyboard.add(key_yes);
			img_msg = await bot.send_message(message.from_user.id, text=image_text_arr[1], reply_markup=keyboard)
			mesg_list_file.append(img_msg) 
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
		await state.update_data(mesg_list_file=mesg_list_file)
		await state.update_data(num=num)


@dp.callback_query_handler(lambda c: c.data == 'null',state=Moving.moving_files)
async def null(message: types.Message, state: FSMContext):
	pass

@dp.callback_query_handler(lambda c: c.data == 'x',state=Moving.moving_files)
async def null(message: types.Message, state: FSMContext):
	await bot.delete_message(message.from_user.id, message.message.message_id)
	move = await state.get_data()
	mesg_list_file=move['mesg_list_file']
	for i in mesg_list_file:
		await bot.delete_message(message.from_user.id, i.message_id)
	fill = skins.skin_changer.see_default().split('ᛣ')
	fill = str(fill[0]).split('/')
	markup5 = types.ReplyKeyboardMarkup().row(
	    types.KeyboardButton(fill[0]), fill[1])
	markup5.row(types.KeyboardButton(fill[2]), types.KeyboardButton(fill[3]))
	markup5.row(types.KeyboardButton(fill[4]), types.KeyboardButton(fill[5]))
	await bot.send_message(message.message.chat.id, 'Меню',reply_markup=markup5)
	await state.finish()


@dp.callback_query_handler(lambda c: c.data == 'report',state=Moving.moving_files)
async def null(message: types.Message, state: FSMContext):
	move = await state.get_data()
	mesg_list=move['mesg_list_file']
	num = move['num']
	print(len(mesg_list))
	keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=False)
	keyboard.add(types.KeyboardButton(text='<<<'))
	for i in range(len(mesg_list)):
					keyboard.add(types.KeyboardButton(text='/'+str(num[i])+'_report'))
	await bot.send_message(message.message.chat.id ,text='Меню репорта:', reply_markup=keyboard)


@dp.callback_query_handler(regexp=r'\d*',state=Moving.moving_files)
async def files_giving(message: types.Message, state: FSMContext):
	print(message.data[2:])
	a = sql_server.sql_server.give_file(int(message.data[2:]))
	i=list(a[0])
	way = pickle.loads(i[0])
	print(i)
	print(i[1])
	await bot.send_document(chat_id=message.from_user.id,document=types.InputFile(way, i[1]),caption=i[2])


@dp.message_handler(text='Отмена', state=Moving.moving_files)
async def otmena(message: types.Message, state: FSMContext):
	keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).row( types.KeyboardButton('<<<'))
	await bot.send_message(chat_id=message.chat.id, text = 'Отмена',reply_markup=keyboard)

@dp.message_handler(regexp=r'\d*_report',state=Moving.moving_files)
async def report(message: types.Message, state: FSMContext):
	await bot.delete_message(message.from_user.id, message.message_id)

	string_text = message.text
	string = str(string_text.split('_')[0])[1:]
	print('Report')
	print(string)
	await bot.send_message(message.chat.id ,text = 'Вы кинули репорт на файл /'+string)
	if string.isdigit():
		print(string)
		user_id = sql_server.sql_server.warn_work(str(string))
		user_id = list(user_id)[0]
		await bot.send_message(chat_id=user_id ,text = 'На ваш файл(/'+str(string)+') был кинут репорт')