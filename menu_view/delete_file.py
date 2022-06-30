from aiogram import types
from config import dp, bot

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

import datetime
import sql_server
import pickle
import mat 
import os
import skins

from time import sleep

class Delete(StatesGroup):
	delete_file = State()

@dp.message_handler(text='♻️Удалить Файлы',state="*")
async def upload_work(message: types.Message,state: FSMContext):
	keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).row('<<<')
	await bot.send_message(message.from_user.id, text='-', reply_markup=keyboard)
	menu_delete = sql_server.sql_server.show_delete_file(message.from_user.id)
	await bot.send_message(message.from_user.id, text=menu_delete[0], reply_markup=menu_delete[1])
	await Delete.delete_file.set()
	await state.update_data(n=0)

with open ("subjects.txt", "r", encoding='utf8') as myfile:
	subss=(myfile.read().split(','))

@dp.callback_query_handler(lambda c: c.data.split('_')[0] in subss,state=Delete.delete_file)
@dp.callback_query_handler(lambda c: c.data == 'next_page_delete_file',state=Delete.delete_file)
@dp.callback_query_handler(lambda c: c.data == 'back_page_delete_file',state=Delete.delete_file)
async def view_works(message: types.Message, state: FSMContext):
		await bot.delete_message(message.from_user.id, message.message.message_id)

		if message.data == 'next_page_delete_file':
			move = await state.get_data()
			n_new = move['n']

			await state.update_data(n=n_new+1)
			mesg_list=move['mesg_list']
			for i in mesg_list:
					await bot.delete_message(message.from_user.id, i.message_id)

		elif message.data == 'back_page_delete_file':
			move = await state.get_data()
			n_new = move['n']

			await state.update_data(n=n_new-1)
			mesg_list=move['mesg_list']
			for i in mesg_list:
					await bot.delete_message(message.from_user.id, i.message_id)


		else:
			await state.update_data(sub=message.data)

		move = await state.get_data()
		n = move['n']
		mesg_list = []
		num = []
		gf = move['sub'].split('_')
		show_img = sql_server.sql_server.show_file_delete(gf[0],gf[1])
		len_of_photos = len(show_img)
		show_img = show_img[0+4*n:4+4*n]
	   
		if len_of_photos%4 != 0:
			max_n = int(len_of_photos/4)+1
		else:
			max_n = int(len_of_photos/4)


		if int(n) >max_n:
			fill = skins.skin_changer.see_default().split('ᛣ')
			fill = str(fill[0]).split('/')
			markup5 = types.ReplyKeyboardMarkup().row(
	    		types.KeyboardButton(fill[0]), fill[1])
			markup5.row(types.KeyboardButton(fill[2]), types.KeyboardButton(fill[3]))
			markup5.row(types.KeyboardButton(fill[4]), types.KeyboardButton(fill[5]))
			await bot.send_message(message.message.chat.id, 'Меню',reply_markup=markup5)
			await state.finish()


		for i in range(len(show_img)):
			image_text_arr = list(show_img[i])
			keyboard = types.InlineKeyboardMarkup()
			key_yes =types.InlineKeyboardButton(text='скачать', callback_data="download_"+str(image_text_arr[3]))
			keyboard.add(key_yes);
			key_yes =types.InlineKeyboardButton(text='❌Удалить', callback_data='deletefileᛣ'+str(image_text_arr[3]))
			keyboard.add(key_yes);
			num.append(image_text_arr[3])
			img_msg = await bot.send_message(message.from_user.id, text=image_text_arr[2], reply_markup=keyboard)
			mesg_list.append(img_msg) 




		if n+1 == int(1) != max_n:
				keyboard = types.InlineKeyboardMarkup()
				row  = []
				row.append(types.InlineKeyboardButton(text='⛔', callback_data='null'))
				row.append(types.InlineKeyboardButton(text='❌', callback_data='x'))
				row.append(types.InlineKeyboardButton(text='▶', callback_data='next_page_delete_file'))
				keyboard.row(*row)
		elif n+1 == max_n != 1:
				keyboard = types.InlineKeyboardMarkup()
				row  = []
				row.append(types.InlineKeyboardButton(text='◀', callback_data='back_page_delete_file'))
				row.append(types.InlineKeyboardButton(text='❌', callback_data='x'))
				row.append(types.InlineKeyboardButton(text='⛔', callback_data='null'))
				keyboard.row(*row)
		elif n+1 == max_n == int(1):
				keyboard = types.InlineKeyboardMarkup()
				row  = []
				row.append(types.InlineKeyboardButton(text='⛔', callback_data='null'))
				row.append(types.InlineKeyboardButton(text='❌', callback_data='x'))
				row.append(types.InlineKeyboardButton(text='⛔', callback_data='null'))
				keyboard.row(*row)
		else:
				keyboard = types.InlineKeyboardMarkup()
				row  = []
				row.append(types.InlineKeyboardButton(text='◀', callback_data='back_page_delete_file'))
				row.append(types.InlineKeyboardButton(text='❌', callback_data='x'))
				row.append(types.InlineKeyboardButton(text='▶', callback_data='next_page_delete_file'))
				keyboard.row(*row)  
		await bot.send_message(message.message.chat.id ,text=str(n+1)+' / '+str(max_n), reply_markup=keyboard)
		await state.update_data(mesg_list=mesg_list)
		await state.update_data(num=num)



@dp.callback_query_handler(lambda c: c.data == 'null',state=Delete.delete_file)
async def null(message: types.Message, state: FSMContext):
	pass

@dp.callback_query_handler(lambda c: c.data == 'x',state=Delete.delete_file)
async def null(message: types.Message, state: FSMContext):
	await bot.delete_message(message.from_user.id, message.message.message_id)
	move = await state.get_data()
	mesg_list=move['mesg_list']
	for i in mesg_list:
			await bot.delete_message(message.from_user.id, i.message_id)
	fill = skins.skin_changer.see_default().split('ᛣ')
	fill = str(fill[0]).split('/')
	markup5 = types.ReplyKeyboardMarkup().row(
	    types.KeyboardButton(fill[0]), fill[1])
	markup5.row(types.KeyboardButton(fill[2]), types.KeyboardButton(fill[3]))
	markup5.row(types.KeyboardButton(fill[4]), types.KeyboardButton(fill[5]))
	await bot.send_message(message.message.chat.id, 'Меню',reply_markup=markup5)
	await state.finish()


@dp.callback_query_handler(lambda c: 'download_' in c.data,state=Delete.delete_file)
async def files_giving(message: types.Message, state: FSMContext):
	print(message.data)
	a = sql_server.sql_server.give_file(int(message.data.split('_')[1]))
	i=list(a[0])
	way = pickle.loads(i[0])
	await bot.send_document(chat_id=message.from_user.id,document=types.InputFile(way, i[1]),caption=i[2])


@dp.callback_query_handler(lambda c: 'deletefileᛣ' in c.data,state=Delete.delete_file)
async def delete_file_(message: types.Message, state: FSMContext):
	print(int(message.data.split('ᛣ')[1]))
	sql_server.sql_server.delete_user_file(int(message.data.split('ᛣ')[1]), message.from_user.id)
	await bot.edit_message_text(chat_id =message.from_user.id,message_id =message.message.message_id,text='Вы удалили свой файл')