'''from aiogram import types
from config import dp, bot

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

import vk_api
import vk

from PIL import Image
import requests

import sql_server
import skins

import string
import random

from vk_api import VkApi, AuthError
from vk_api.utils import get_random_id



TOKEN = "6f0615c45ee9909a061b28c258052b8fb1de0cde7e8e94113df0e6a59ceb8fe7b06dc3884287b96d7beca"


def id_generator(size=4, chars=string.digits):
    return ''.join(random.choice(chars) for x in range(size))

class Making_vkid(StatesGroup):
    waiting_for_vk = State()
    waiting_for_auth = State()


@dp.message_handler(text=['🔗Привязать свой профиль в VK'],state='*')
async def settings(message: types.Message,state: FSMContext):
	keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
	keyboard.add(types.KeyboardButton(text='<<<'))
	keyboard.add(types.KeyboardButton(text='Отвязать профиль вк'))
	await bot.send_message(message.chat.id, 'Введи свой vk id (адрес страницы) \n https://vk.com/settings',reply_markup=keyboard)
	await Making_vkid.waiting_for_vk.set()


@dp.message_handler(state=Making_vkid.waiting_for_vk, content_types=types.ContentTypes.TEXT)
async def check(message: types.Message, state: FSMContext): 
	fill = skins.skin_changer.see_default().split('ᛣ')

	fill = str(fill[0]).split('/')
	markup5 = types.ReplyKeyboardMarkup().row(
	    types.KeyboardButton(fill[0]), fill[1])
	markup5.row(types.KeyboardButton(fill[2]), types.KeyboardButton(fill[3]))
	markup5.row(types.KeyboardButton(fill[4]), types.KeyboardButton(fill[5]))

	if message.text == '<<<':
		fill = skins.skin_changer.see_default().split('ᛣ')
		text = fill[3]
		fill = str(fill[0]).split('/')
		markup5 = types.ReplyKeyboardMarkup().row(
		    types.KeyboardButton(fill[0]), fill[1])
		markup5.row(types.KeyboardButton(fill[2]), types.KeyboardButton(fill[3]))
		markup5.row(types.KeyboardButton(fill[4]), types.KeyboardButton(fill[5]))
		await bot.send_message(chat_id=message.chat.id, text=text, reply_markup=markup5)
		await state.finish()
	else:
		vk_session = vk_api.VkApi(token=TOKEN)
		vk = vk_session.get_api()
		if message.text == 'Отвязать профиль вк':
			await bot.send_message(message.chat.id ,text="Вы успешно отвязали свой профиль!", reply_markup=markup5)
			sql_server.sql_server.add_vk_id(None,message.from_user.id)
			await state.finish()
			return
		elif message.text == '1':
			await bot.send_message(message.chat.id ,text="Шизоид ты, а не Павел Дуров")
			return
		ids = vk.users.get(user_ids=message.text)[0]
		print(ids)
		print(sql_server.sql_server.sql_check_base_vkid(int(ids['id'])))
		if sql_server.sql_server.sql_check_base_vkid(int(ids['id'])) == True:
				await bot.send_message(message.chat.id ,text="Этот vk id уже существует", reply_markup=markup5)
		else:
				await state.update_data(name=message.text)
				await state.update_data(ids=ids)
				kod = id_generator()
				print('aboba')
				#vk.messages.send(user_id=int(ids['id']), message="Ваш код подтверждения "+kod+' Никому не сообщайте код', random_id=get_random_id())
				print('aboba')
				keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
				keyboard.add(types.KeyboardButton(text='<<<'))
				print('aboba')
				await bot.send_message(message.chat.id ,text=kod+"  - ваш код для привязки страницы в вк\nОтправьте его в лс боту в вк - https://vk.com/im?media=&sel=-202073817", reply_markup=keyboard)
				await Making_vkid.waiting_for_auth.set()
				await state.update_data(kod=kod)
				#except vk_api.exceptions.ApiError:
				#await bot.send_message(message.chat.id ,text="Некоректный вк_ид, введите еще раз")
				#return

@dp.message_handler(state=Making_vkid.waiting_for_auth, content_types=types.ContentTypes.TEXT)
async def auth(message: types.Message, state: FSMContext): 
	fill = skins.skin_changer.see_default().split('ᛣ')
	text = fill[3]
	fill = str(fill[0]).split('/')
	markup5 = types.ReplyKeyboardMarkup().row(
	    types.KeyboardButton(fill[0]), fill[1])
	markup5.row(types.KeyboardButton(fill[2]), types.KeyboardButton(fill[3]))
	markup5.row(types.KeyboardButton(fill[4]), types.KeyboardButton(fill[5]))

	kodd = await state.get_data()
	kod = kodd['kod']
	ids = kodd['ids']
	name = kodd['name']
	if int(message.text) == int(kod):
		await bot.send_message(message.chat.id ,text="Вы: "+ids['last_name']+' '+ids['first_name']+'\n'+'vk.com/'+str(name)+'\n 🟩Вы успешно привязали свой профиль', reply_markup=markup5)
		sql_server.sql_server.add_vk_id(int(ids['id']),message.from_user.id)
		await state.finish()
	else:
		await bot.send_message(message.chat.id ,text="Неправильный код, повторите попытку снова", reply_markup=markup5)
		await state.finish()


#await bot.send_photo(chat_id=message.from_user.id,photo= types.InputFile.from_url(ids['photo_200_orig']),caption="Твоя ава")
sql_server.sql_server.add_vk_id(int(ids['id']),message.from_user.id)
await bot.send_message(message.chat.id ,text="Вы: "+ids['last_name']+' '+ids['first_name']+'\n'+'vk.com/'+str(message.text)+'\n 🟩Вы успешно привязали свой профиль', reply_markup=markup5)
await state.finish()


'''