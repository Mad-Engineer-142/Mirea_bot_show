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

class Delete(StatesGroup):
	delete = State()

@dp.message_handler(text='📤Удалить Работы',state="*")
async def upload_work(message: types.Message,state: FSMContext):
	keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).row('<<<')
	await bot.send_message(message.from_user.id, text='-', reply_markup=keyboard)
	menu_delete = sql_server.sql_server.show_delete_work(message.from_user.id)
	await bot.send_message(message.from_user.id, text=menu_delete[0], reply_markup=menu_delete[1])
	await Delete.delete.set()
	await state.update_data(n=0)

with open ("subjects.txt", "r", encoding='utf8') as myfile:
	subss=(myfile.read().split(','))

@dp.callback_query_handler(lambda c: c.data.split('_')[0] in subss,state=Delete.delete)
@dp.callback_query_handler(lambda c: c.data == 'next_page_delete',state=Delete.delete)
@dp.callback_query_handler(lambda c: c.data == 'back_page_delete',state=Delete.delete)
async def view_works(message: types.Message, state: FSMContext):
		await bot.delete_message(message.from_user.id, message.message.message_id)

		if message.data == 'next_page_delete':
			move = await state.get_data()
			n_new = move['n']

			await state.update_data(n=n_new+1)
			mesg_list=move['mesg_list']
			for i in mesg_list:
				for a in i:
					await bot.delete_message(message.from_user.id, a.message_id)

		elif message.data == 'back_page_delete':
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
		gf = move['sub'].split('_')
		show_img = sql_server.sql_server.show_work_delete(gf[0],gf[1])
		len_of_photos = len(show_img)
		show_img = show_img[0+4*n:4+4*n]
	   
		if len_of_photos%4 != 0:
			max_n = int(len_of_photos/4)+1
		else:
			max_n = int(len_of_photos/4)
		print(n, max_n)
		if int(n) > max_n:
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
			mas = pickle.loads(image_text_arr[0]) 

			media = types.MediaGroup()  
			for a in range(len(mas)):
				if a == 0:
					media.attach_photo(types.InputFile(mas[a]), image_text_arr[2])
					num.append(image_text_arr[2])
				else:
					media.attach_photo(types.InputFile(mas[a]))

			img_msg = await bot.send_media_group(message.from_user.id, media=media)

			keyb = types.InlineKeyboardMarkup()
			key_yes = types.InlineKeyboardButton(text='❌Удалить ', callback_data='delete_'+str(image_text_arr[3]))
			keyb.add(key_yes);



			img_msgs = await bot.send_message(message.message.chat.id ,text='Нажми чтобы удалить', reply_markup=keyb)
			mesg_list.append([img_msgs])

			mesg_list.append(img_msg)    
		if n+1 == int(1) != max_n:
				keyboard = types.InlineKeyboardMarkup()
				row  = []
				row.append(types.InlineKeyboardButton(text='⛔', callback_data='null'))
				row.append(types.InlineKeyboardButton(text='❌', callback_data='x'))
				row.append(types.InlineKeyboardButton(text='▶', callback_data='next_page_delete'))
				keyboard.row(*row)
		elif n+1 == max_n != 1:
				keyboard = types.InlineKeyboardMarkup()
				row  = []
				row.append(types.InlineKeyboardButton(text='◀', callback_data='back_page_delete'))
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
				row.append(types.InlineKeyboardButton(text='◀', callback_data='back_page_delete'))
				row.append(types.InlineKeyboardButton(text='❌', callback_data='x'))
				row.append(types.InlineKeyboardButton(text='▶', callback_data='next_page_delete'))
				keyboard.row(*row)  
		await bot.send_message(message.message.chat.id ,text=str(n+1)+' / '+str(max_n), reply_markup=keyboard)
		await state.update_data(mesg_list=mesg_list)
		await state.update_data(num=num)



@dp.callback_query_handler(lambda c: c.data == 'null',state=Delete.delete)
async def null(message: types.Message, state: FSMContext):
	pass

@dp.callback_query_handler(lambda c: c.data == 'x',state=Delete.delete)
async def null(message: types.Message, state: FSMContext):
	await bot.delete_message(message.from_user.id, message.message.message_id)
	move = await state.get_data()
	mesg_list=move['mesg_list']
	for i in mesg_list:
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

@dp.callback_query_handler(regexp=r'delete_\d*',state=Delete.delete)
async def delete_(message: types.Message, state: FSMContext):
	sql_server.sql_server.delete_user_work(message.data.split('_')[-1], message.from_user.id)
	await bot.edit_message_text(chat_id = message.from_user.id,message_id =message.message.message_id,text='Вы удалили свою работу')
