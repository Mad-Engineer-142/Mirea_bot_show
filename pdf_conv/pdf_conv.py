from aiogram import types
from config import dp, bot

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

import skins
import random
import img2pdf
import os
class Uploadс(StatesGroup):
	waiting_for_image_conv = State()

@dp.message_handler(text=["🧰PDF-конвертер"],state='*')
async def upload_work(message: types.Message,state: FSMContext):
	fill = skins.skin_changer.see_default().split('ᛣ')
	fill = str(fill[12]).split('/')
	text = fill[0]
	butt = fill[1]
	keyboard = types.ReplyKeyboardMarkup()
	keyboard.row(types.KeyboardButton(butt))
	keyboard.row(types.KeyboardButton("<<<"))
	message = await bot.send_message(message.chat.id, text, reply_markup=keyboard)
	await Uploadс.waiting_for_image_conv.set()
	await state.update_data(photo=[])



@dp.message_handler(state=Uploadс.waiting_for_image_conv, content_types=types.ContentType.PHOTO)
async def photos(message: types.Message, state: FSMContext):
	for_photo = await state.get_data()
	ar = for_photo['photo']
	ar.append(message.photo[-1].file_id)
	await state.update_data(photo=ar)


@dp.message_handler(text=['🧰Нажми когда все загрузишь🧰'], state='*')
async def Confirms(message: types.Message, state: FSMContext):
	for_photo = await state.get_data()
	fill = skins.skin_changer.see_default().split('ᛣ')
	fill = str(fill[0]).split('/')

	markup5 = types.ReplyKeyboardMarkup().row(
	    types.KeyboardButton(fill[0]), fill[1])
	markup5.row(types.KeyboardButton(fill[2]), types.KeyboardButton(fill[3]))
	markup5.row(types.KeyboardButton(fill[4]), types.KeyboardButton(fill[5]))

	if not for_photo['photo']:
		print('return')
		return
	elif len(for_photo['photo'])>=50:
		message = await bot.send_message(message.chat.id, text =random.choices(['Ты загрузил больше 50 фото, не поместится.....', 'Ну ладно 30 фоток я могу поверить, но 50+ это пребор братишка'], weights=[80, 20])[0], reply_markup=markup5)
		await state.finish()
	else:
		user_data = await state.get_data()
		photos = user_data['photo']

		await bot.send_message(chat_id=message.chat.id,text='Подожди секунду файл создается',reply_markup=markup5)
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