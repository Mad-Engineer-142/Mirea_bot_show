from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


from config import dp, bot
import sql_server
import pickle


class Au(StatesGroup):
	nexts = State()

@dp.callback_query_handler(lambda c: c.data == 'unban',state=Au.nexts)
@dp.callback_query_handler(lambda c: c.data == 'next_page_unban',state=Au.nexts)
@dp.callback_query_handler(lambda c: c.data == 'back_page_unban',state=Au.nexts)
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

		move = await state.get_data()
		n = move['n']
		mesg_list = []
		panel = []
		num = []
		show_img = sql_server.sql_server.show_work_ban()
		if show_img:
			len_of_photos = len(show_img)
			show_img = show_img[0+4*n:4+4*n]
		   
			if len_of_photos%4 != 0:
				max_n = int(len_of_photos/4)+1
			else:
				max_n = int(len_of_photos/4)
	#KeYBoard Init
			for i in range(len(show_img)):
				keyboard = types.InlineKeyboardMarkup()
				image_text_arr = list(show_img[i])
				if image_text_arr[4] == 'p':
					mas = pickle.loads(image_text_arr[0]) 
					media = types.MediaGroup()
					row  = []
					row.append(types.InlineKeyboardButton(text='✅Восстановить', callback_data='Unban_work_'+str(image_text_arr[2])))
					row.append(types.InlineKeyboardButton(text='❌Удалить', callback_data='Delete_work_'+str(image_text_arr[2])))
					keyboard.row(*row)  
					for a in range(len(mas)):
						if a == 0:
							media.attach_photo(types.InputFile(mas[a]), image_text_arr[1])
							num.append(image_text_arr[2])
							print(image_text_arr[2])
						else:
							media.attach_photo(types.InputFile(mas[a]))
					img_msg = await bot.send_media_group(message.from_user.id, media=media)	

					panelka = await bot.send_message(message.from_user.id,text='Выбери действие',reply_markup=keyboard)

					mesg_list.append(img_msg)
					panel.append(panelka)

				elif image_text_arr[4] == 'f':
					image_text_arr = list(show_img[i])
					keyboard = types.InlineKeyboardMarkup()

					print(image_text_arr[1].split('|')[0])
					key_yes =types.InlineKeyboardButton(text='скачать', callback_data='|'+image_text_arr[1].split('|')[0])
					keyboard.add(key_yes);
					row  = []
					row.append(types.InlineKeyboardButton(text='✅Восстановить', callback_data='Unban_file_'+str(image_text_arr[2])))
					row.append(types.InlineKeyboardButton(text='❌Удалить', callback_data='Delete_file_'+str(image_text_arr[2])))
					keyboard.row(*row)  

					print(image_text_arr[3])
					num.append(image_text_arr[3])

					img_msg = await bot.send_message(message.from_user.id, text=image_text_arr[1], reply_markup=keyboard)
					mesg_list.append([img_msg]) 


			if n+1 == int(1) != max_n:
					keyboard = types.InlineKeyboardMarkup()
					row  = []
					row.append(types.InlineKeyboardButton(text='⛔', callback_data='null'))
					row.append(types.InlineKeyboardButton(text='❌', callback_data='x'))
					row.append(types.InlineKeyboardButton(text='➪', callback_data='next_page_ban'))
					keyboard.row(*row)
			elif n+1 == max_n != 1:
					keyboard = types.InlineKeyboardMarkup()
					row  = []
					row.append(types.InlineKeyboardButton(text='🢦', callback_data='back_page_ban'))
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
					row.append(types.InlineKeyboardButton(text='🢦', callback_data='back_page_ban'))
					row.append(types.InlineKeyboardButton(text='❌', callback_data='x'))
					row.append(types.InlineKeyboardButton(text='➪', callback_data='next_page_ban'))
					keyboard.row(*row)  
			await bot.send_message(message.message.chat.id ,text=str(n+1)+' / '+str(max_n), reply_markup=keyboard)
			await state.update_data(mesg_list=mesg_list)
			await state.update_data(panel=panel)
			await state.update_data(num=num)
		else:
			await bot.send_message(message.message.chat.id ,text='Работ с баном нет')	



@dp.callback_query_handler(lambda c: 'Delete_work_' in c.data,state=Au.nexts)
async def Delete_work_(message: types.Message, state: FSMContext):
	await bot.edit_message_text(chat_id = message.from_user.id,message_id =message.message.message_id,text='Вы удалили эту работу, она не будет появляться в глобальном поиске и будет удалена ')
	numero = int(message.data.split('_')[-1])
	print(numero)
	sql_server.sql_server.delete_ban_work(numero)

@dp.callback_query_handler(lambda c: 'Delete_file_' in c.data,state=Au.nexts)
async def Delete_file_(message: types.Message, state: FSMContext):
	await bot.edit_message_text(chat_id = message.from_user.id,message_id =message.message.message_id,text='Вы удалили эту работу, она не будет появляться в глобальном поиске и будет удалена ')
	numero = int(message.data.split('_')[-1])
	print(numero)
	sql_server.sql_server.delete_ban_file(numero)

@dp.callback_query_handler(lambda c: 'Unban_work_' in c.data,state=Au.nexts)
async def null(message: types.Message, state: FSMContext):
	await bot.edit_message_text(chat_id = message.from_user.id,message_id =message.message.message_id,text='Вы восстановили эту работу, она будет появляться в глобальном поиске')
	numero = int(message.data.split('_')[-1])
	print(numero)
	sql_server.sql_server.praise_work(numero)
	warn_work = sql_server.sql_server.praise_work(numero)
	await bot.send_message(chat_id=warn_work ,text = 'С вашей работы(/'+str(numero)+') был снят репорт')

@dp.callback_query_handler(lambda c: 'Unban_file_' in c.data,state=Au.nexts)
async def null(message: types.Message, state: FSMContext):
	await bot.edit_message_text(chat_id = message.from_user.id,message_id =message.message.message_id,text='Вы восстановили этот файл, он будет появляться в глобальном поиске')
	numero = int(message.data.split('_')[-1])
	print(numero)
	sql_server.sql_server.praise_work(numero)
	warn_work = sql_server.sql_server.praise_work(numero)
	await bot.send_message(chat_id=warn_work ,text = 'С вашего файла(/'+str(numero)+') был снят репорт')