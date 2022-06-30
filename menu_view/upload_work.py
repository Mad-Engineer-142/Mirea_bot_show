from aiogram import types
from config import dp, bot

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

import datetime
import sql_server
import mat 
import os
import numpy as np
import PIL
from PIL import Image
import img2pdf
import io
import skins

class Upload(StatesGroup):
	waiting_for_image = State()
	waiting_for_subject= State()
	waiting_for_variant = State()
	waiting_for_checked = State()
	waiting_for_text = State()
	waiting_for_end = State()
	waiting_for_pdf = State()

@dp.message_handler(text=['✒️Загрузить Работы'],state='*')
async def upload_work(message: types.Message,state: FSMContext):
	print(message.from_user.id)
	fill = skins.skin_changer.see_default().split('ᛣ')
	fill = str(fill[10]).split('/')
	text = fill[0]
	butt = fill[1]
	keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
	keyboard.row(types.KeyboardButton(butt))
	keyboard.row(types.KeyboardButton('<<<'))
	message = await bot.send_message(message.chat.id, text, reply_markup=keyboard)
	await Upload.waiting_for_image.set()
	await state.update_data(photo=[])

@dp.callback_query_handler(lambda c: c.data == 'upload_works', state="*")
async def upload_work(message: types.Message,state: FSMContext):
	await bot.delete_message(message.from_user.id, message.message.message_id)
	print(message.from_user.id)
	fill = skins.skin_changer.see_default().split('ᛣ')
	fill = str(fill[10]).split('/')
	text = fill[0]
	butt = fill[1]
	keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
	keyboard.row(types.KeyboardButton(butt))
	keyboard.row(types.KeyboardButton('<<<'))
	message = await bot.send_message(message.message.chat.id, text, reply_markup=keyboard)
	await Upload.waiting_for_image.set()
	await state.update_data(photo=[])


@dp.message_handler(state=Upload.waiting_for_image, content_types=types.ContentType.PHOTO)
async def Photo(message: types.Message, state: FSMContext):
	for_photo = await state.get_data()
	ar = for_photo['photo']
	ar.append(message.photo[-1].file_id)
	await state.update_data(photo=ar)


@dp.message_handler(text=['✅Нажми когда все загрузишь✅'], state='*')
async def Confirm(message: types.Message, state: FSMContext):
	for_photo = await state.get_data()
	if not for_photo['photo']:
		return
	elif len(for_photo['photo'])>=36:
		message = await bot.send_message(message.chat.id, 'Ты загрузил больше 36 фото, не поместится.....')
		await state.finish()
		keyboard = types.InlineKeyboardMarkup()
		key_yes = types.InlineKeyboardButton(text='Нажми когда все загрузишь', callback_data='yes_create');
		keyboard.add(key_yes);
		message = await bot.send_message(message.chat.id, 'Пришли Фото своей работы', reply_markup= keyboard)
		await Upload.waiting_for_image.set()
		await state.update_data(photo=[])
	else:
		subs = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
		with open("subjects.txt", "r", encoding='utf8') as myfile:
			subss=(myfile.read().split(','))
		for i in subss:
			 button_hi = types.KeyboardButton(i)
			 subs.add(button_hi)
		await bot.send_message(message.chat.id, "Выбери или напиши предмет по которому прислал работу", reply_markup=subs)
		await Upload.waiting_for_variant.set()

"""@dp.callback_query_handler(lambda c: c.data in ['1','2','3','4'], state=Upload.waiting_for_subject)
async def Confirm(message: types.Message, state: FSMContext):
	await bot.delete_message(message.from_user.id, message.message.message_id)
	await state.update_data(course=message.data)

	subs = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
	with open("subjects.txt", "r", encoding='utf8') as myfile:
		subss=(myfile.read().split(','))
	for i in subss:
			 button_hi = types.KeyboardButton(i)
			 subs.add(button_hi)
	await bot.send_message(message.message.chat.id, "Выбери или напиши предмет по которому прислал работу", reply_markup=subs)
	await Upload.waiting_for_variant.set()"""

@dp.message_handler(state=Upload.waiting_for_variant, content_types=types.ContentTypes.TEXT)
async def waiting_for_variant(message: types.Message, state: FSMContext): 
	with open ("subjects.txt", "r", encoding='utf8') as myfile:
		subss=(myfile.read().split(','))
	if message.text.lower() not in subss:
		await bot.send_message(message.chat.id, text="Некоректный предмет, введи еще раз")
		return
	else:
		await state.update_data(subject=message.text.lower())
		await bot.send_message(message.chat.id, text="Напиши Вариант(ы) через запятую, не более четырех вариантов\nИли через тире (4-6)")	
		await Upload.waiting_for_text.set()
'''
@dp.callback_query_handler(lambda c: c.data in ['yes_ch','no_ch'], state=Upload.waiting_for_checked)
async def waiting_for_checked(message: types.Message, state: FSMContext): 
	await bot.delete_message(message.from_user.id, message.message.message_id)
	if message.data == 'yes_ch':
		await state.update_data(check=True)
	elif message.data == 'no_ch':
		await state.update_data(check=False)

	await bot.send_message(message.message.chat.id, text='Напиши Вариант(ы) через запятую, не более четырех вариантов\nИли через тире (4-6)',reply_markup=types.ReplyKeyboardRemove())	
	await Upload.waiting_for_text.set()
'''


@dp.message_handler(state=Upload.waiting_for_text, content_types=types.ContentTypes.TEXT)
async def waiting_for_text(message: types.Message, state: FSMContext): 
	if ',' in message.text:
		print(2)
		if ',' in message.text.split():
			print(22)
			await bot.send_message(message.chat.id, text='Некорректно введен вариант')
			return
		else:
			for i in message.text.split(','):
				if i.isdigit():
					print(222)
					if len(message.text.split(','))>4:
						print(2222)
						await bot.send_message(message.chat.id, text='Не больше 4 вариантов за раз')
						return
					else:
						var = message.text.split(',')
						for i in range(4-len(var)):
							var.append(None)
				else:
					await bot.send_message(message.chat.id, text='Некорректно введен вариант')
					return
	elif '-' in message.text:
		print(1)
		if len(message.text.split('-')) == 2:
			print(111)
			for i in message.text.split('-'):
				if i.isdigit():
					print(1111)
					varsss = message.text.split('-')
					var = ['-']
					for i in varsss:
						var.append(i)
					var.append(None)
					print(var)
				else:
					await bot.send_message(message.chat.id, text='Некорректно введен вариант')
					return
		else:
			await bot.send_message(message.chat.id, text='Некорректно введен вариант')
			return
	elif '—' in message.text:
			if len(message.text.split('—')) == 2:
				for i in message.text.split('—'):
					if i.isdigit():
						varsss = message.text.split('—')
						var = ['-']
						for i in varsss:
							var.append(i)
						var.append(None)
						print(var)
					else:
						await bot.send_message(message.chat.id, text='Некорректно введен вариант')
						return
			else:
				await bot.send_message(message.chat.id, text='Некорректно введен вариант')
				return
	elif message.text.isdigit():
		var = [message.text, None, None, None]
	else:
		await bot.send_message(message.chat.id, text='Некорректно введен вариант, нужно ввести не более четырех вариантов\nИли через тире (4-6)')
		return


	await state.update_data(var=var)
	subs = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
	subs.add(types.KeyboardButton('Нет'))
	await bot.send_message(message.chat.id, text='Примечания к работе (не более 250 символов)',reply_markup=subs)
	await Upload.waiting_for_end.set()

@dp.message_handler(state=Upload.waiting_for_end, content_types=types.ContentTypes.TEXT)
async def waiting_for_end(message: types.Message, state: FSMContext): 
	if message.text == 'Нет':
		await state.update_data(text=None)
	else:
		if mat.mat_check.mat_checker(message.text):
			await bot.send_message(message.chat.id, text='Не матюкайся')
			return
		else:
			await bot.send_message(chat_id=message.chat.id, text ='Секунду, бот обрабатывает фотографии', reply_markup=types.ReplyKeyboardRemove())
			await state.update_data(text=message.text)
	user_data = await state.get_data()
	print(user_data)
	photos = user_data['photo']
	way_arr = [] 
	if len(photos)<=10:
		for i in photos:
			file = await bot.get_file(i)
			iobytes = await bot.download_file(file_path=file.file_path)
			if not os.path.exists('photo/'+str(message.from_user.id)):
				os.makedirs('photo/'+str(message.from_user.id))
			else:
				pass
			way = 'photo/'+str(message.from_user.id)+'/'+i+".jpg"
			way_arr.append(way)
			with open(way, "wb") as outfile:
				outfile.write(iobytes.getbuffer())
	else:

		if not os.path.exists('photo/'+str(message.from_user.id)):
			os.makedirs('photo/'+str(message.from_user.id))
		else:
			pass
		poskolko_el = int(len(photos)/10+1)

		skolro_mas = int(len(photos)/int((len(photos)/10)+1)+1)
		big_arr = []

		for e in range(skolro_mas):
			mal_mas = photos[0+poskolko_el*e:poskolko_el+poskolko_el*e]
			big_arr.append(mal_mas)
		for msa in big_arr:
			coverted = []
			for a in range(len(msa)):
				if a == 0:
					print('writting name')
					way = 'photo/'+str(message.from_user.id)+'/'+msa[a]+".jpg"
					way_arr.append(way)

					file = await bot.get_file(msa[a])
					print(file)
					coverted.append(Image.open(await bot.download_file(file_path=file.file_path)).convert("RGB"))
				else:
					print('not_writting name')
					print(file)
					file = await bot.get_file(msa[a])
					coverted.append(Image.open(await bot.download_file(file_path=file.file_path)).convert("RGB"))

				min_shape = sorted([(np.sum(i.size), i.size ) for i in coverted])[0][1]
				imgs_comb = np.hstack((np.asarray(i.resize(min_shape)) for i in coverted))
				imgs_comb = PIL.Image.fromarray(imgs_comb)
				imgs_comb.save(way)

			

	varss = ''
	if user_data['var'][0] == '-':
			vv = [user_data['var'][1],user_data['var'][2]]
			varss = min(vv)+'-'+max(vv)
			print(varss)
	else:
		for i in user_data['var']:
			if i != None:
				varss = varss +' '+i

	today = datetime.datetime.today()
	date_cortage = today.strftime("%d/%m/%Y").split('/')
 
	user_name = sql_server.sql_server.user_id_to_name(message.from_user.id)
	unique = sql_server.sql_server.unique_num()
	if user_data['text'] != None:
		caption = ' /'+str(unique)+'\n|Предмет:'+user_data['subject']+'\n|Автор:'+str(user_name[0])+'\n|Группа: '+str(user_name[1])+'\n|Вариант(ы): '+varss+'\n|Дата: '+str(date_cortage[0])+':'+str(date_cortage[1])+':'+str(date_cortage[2]+'\n|Примечание к работе:'+user_data['text'])
	else:
		caption = ' /'+str(unique)+'\n|Предмет:'+user_data['subject']+'\n|Автор:'+str(user_name[0])+'\n|Группа: '+str(user_name[1])+'\n|Вариант(ы): '+varss+'\n|Дата: '+str(date_cortage[0])+':'+str(date_cortage[1])+':'+str(date_cortage[2])
	keyboard = types.InlineKeyboardMarkup()
	key_yes = types.InlineKeyboardButton(text='✅Да', callback_data='yes_download');
	keyboard.add(key_yes);
	key_yes = types.InlineKeyboardButton(text='📛Нет', callback_data='no_download');
	keyboard.add(key_yes);
	print('---___-------____---')
	print(way_arr,caption,user_data['subject'],0,0, 'p',user_data['var'], date_cortage, message.from_user.id, unique, None)
	print('---___-------____---')
	unique_num = sql_server.sql_server.img_save(way_arr,caption,user_data['subject'],0,0, 'p',user_data['var'], date_cortage, message.from_user.id, unique, None)
	
	await state.update_data(post_text='Вы успешно загрузили работу\nИндификатор - /'+str(unique_num))
	await bot.send_message(message.chat.id, text='Вы успешно загрузили работу\nИндификатор - /'+str(unique_num)+'\n Хочешь получить pdf файл со своей работой? ',reply_markup=keyboard)
	await Upload.waiting_for_pdf.set()

@dp.callback_query_handler(lambda c: c.data in ['yes_download','no_download'], state=Upload.waiting_for_pdf)
async def waiting_for_checked(message: types.Message, state: FSMContext): 
	await bot.delete_message(message.from_user.id, message.message.message_id)
	fill = skins.skin_changer.see_default().split('ᛣ')
	text = fill[3]
	fill = str(fill[0]).split('/')
	markup5 = types.ReplyKeyboardMarkup().row(
		types.KeyboardButton(fill[0]), fill[1])
	markup5.row(types.KeyboardButton(fill[2]), types.KeyboardButton(fill[3]))
	markup5.row(types.KeyboardButton(fill[4]), types.KeyboardButton(fill[5]))

	await bot.send_message(chat_id=message.message.chat.id, text=text, reply_markup=markup5)
	if message.data == 'yes_download':
		user_data = await state.get_data()
		photos = user_data['photo']
		post_text = user_data['post_text']
		await bot.send_message(chat_id=message.message.chat.id,text=post_text+'\nПодожди секунду файл создается',reply_markup=markup5)
		ppdf = []
		for i in range(len(photos)):
			if i ==0:
				name = photos[i]
			else:
				pass
			file = await bot.get_file(photos[i])
			ppdf.append(await bot.download_file(file_path=file.file_path))

		way_to_pdf = "temp_files/"+name+".pdf"
		with open(way_to_pdf,"wb") as f:
			f.write(img2pdf.convert(ppdf))
		await bot.send_document(chat_id=message.from_user.id,document=types.InputFile(way_to_pdf))
		await state.finish()
		os.remove(way_to_pdf)
	elif message.data == 'no_download':
		user_data = await state.get_data()
		post_text = user_data['post_text']
		await bot.send_message(chat_id=message.message.chat.id,text=post_text,reply_markup=markup5)
		await state.finish()