# -*- coding: utf8 -*-

#______________________________________________________________________________________________


#           _____ ____   _____ _____            __  __             _____ ____  _   _ ______ _____ _____ 
#     /\   |_   _/ __ \ / ____|  __ \     /\   |  \/  |   ___     / ____/ __ \| \ | |  ____|_   _/ ____|
#    /  \    | || |  | | |  __| |__) |   /  \  | \  / |  ( _ )   | |   | |  | |  \| | |__    | || |  __ 
#   / /\ \   | || |  | | | |_ |  _  /   / /\ \ | |\/| |  / _ \/\ | |   | |  | | . ` |  __|   | || | |_ |
#  / ____ \ _| || |__| | |__| | | \ \  / ____ \| |  | | | (_>  < | |___| |__| | |\  | |     _| || |__| |
# /_/    \_\_____\____/ \_____|_|  \_\/_/    \_\_|  |_|  \___/\/  \_____\____/|_| \_|_|    |_____\_____|
                                                                                                       
                                                                                                       

from aiogram import Bot, types
from aiogram.utils.markdown import text, bold, italic, code, pre
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.dispatcher import Dispatcher, filters

from aiogram.utils import executor
from aiogram.dispatcher import FSMContext

from config import dp, bot

#______________________________________________________________________________________________


 # _      ____   _____          _        _____ __  __ _____   ____  _____ _______ _____ 
 #| |    / __ \ / ____|   /\   | |      |_   _|  \/  |  __ \ / __ \|  __ \__   __/ ____|
 #| |   | |  | | |       /  \  | |        | | | \  / | |__) | |  | | |__) | | | | (___  
 #| |   | |  | | |      / /\ \ | |        | | | |\/| |  ___/| |  | |  _  /  | |  \___ \ 
 #| |___| |__| | |____ / ____ \| |____   _| |_| |  | | |    | |__| | | \ \  | |  ____) |
 #|______\____/ \_____/_/    \_\______| |_____|_|  |_|_|     \____/|_|  \_\ |_| |_____/ 
                                                                                       
                                                                                       
import user_do
import menu_view
import timetable
import mat
import sql_server
import admin
import admin_panel
import send_alert
import backup_gd
import skins
import pdf_conv
#______________________________________________________________________________________________

 #__      ___  __  _____ __  __ _____   ____  _____ _______ _____ 
 #\ \    / / |/ / |_   _|  \/  |  __ \ / __ \|  __ \__   __/ ____|
 # \ \  / /| ' /    | | | \  / | |__) | |  | | |__) | | | | (___  
 #  \ \/ / |  <     | | | |\/| |  ___/| |  | |  _  /  | |  \___ \ 
 #   \  /  | . \   _| |_| |  | | |    | |__| | | \ \  | |  ____) |
 #    \/   |_|\_\ |_____|_|  |_|_|     \____/|_|  \_\ |_| |_____/ 
                                                                 
                                                                 

from datetime import datetime, timedelta
from cryptography.fernet import Fernet
from time import sleep

import vk_api
from vk_api import VkApi, AuthError

#______________________________________________________________________________________________

@dp.message_handler(commands=['start'], state='*')
async def start(message: types.Message):
	if sql_server.sql_server.check_user_rating(message.from_user.id) == None:
		await user_do.create_user.muser(message)
	elif sql_server.sql_server.check_user_rating(message.from_user.id) == True:
		print(message.from_user.id)
		'''await bot.send_message(message.from_user.id,
			─────────────────
 			/help - меню помощи
 			/muser - чтобы создать новую учетку
 			/reuser чтобы переименовать уже существующую
 			/deluser чтобы удалить свою учетную запись
 			/info -чтобы получить информацию о своем профиле
 			/menu - чтобы войти в главное меню
			─────────────────
			)'''

		fill = skins.skin_changer.see_default().split('ᛣ')
		print(fill)
		fill = str(fill[0]).split('/')
		print(fill)
		markup5 = types.ReplyKeyboardMarkup().row(
		    types.KeyboardButton(fill[0]), fill[1])
		markup5.row(types.KeyboardButton(fill[2]), types.KeyboardButton(fill[3]))
		markup5.row(types.KeyboardButton(fill[4]), types.KeyboardButton(fill[5]))
		current_datetime = datetime.now()
		info = sql_server.sql_server.get_info_user_id(message.from_user.id)
		if info[4] == None:
			ask = ' '
		else:
			ask = ' '
		if current_datetime.hour <= 11:
			text = 'Доброе Утро '+sql_server.sql_server.user_id_to_name(message.from_user.id)[0]+'\n'+str(current_datetime.hour)+':'+str(current_datetime.minute)+"\n"+str(current_datetime.day)+':'+str(current_datetime.month)+':'+str(current_datetime.year) +'\n'+ask
		elif current_datetime.hour > 11 and current_datetime.hour < 18:
			text = 'Добрый день '+sql_server.sql_server.user_id_to_name(message.from_user.id)[0]+'\n'+str(current_datetime.hour)+':'+str(current_datetime.minute)+"\n"+str(current_datetime.day)+':'+str(current_datetime.month)+':'+str(current_datetime.year)+'\n'+ask
		else:
			text = 'Добрый вечер '+sql_server.sql_server.user_id_to_name(message.from_user.id)[0]+'\n'+str(current_datetime.hour)+':'+str(current_datetime.minute)+"\n"+str(current_datetime.day)+':'+str(current_datetime.month)+':'+str(current_datetime.year)+'\n'+ask
		
		await message.reply(text, reply_markup=markup5)
	else:
		await bot.send_message(message.chat.id, 'Вы забанены')
#______________________________________________________________________________________________

@dp.message_handler(commands=['help'], state="*")
@dp.message_handler(text='Помощь', state="*")
async def start(message: types.Message):
	if sql_server.sql_server.check_user_rating(message.from_user.id) == None:
		print('asd')
		#media = types.MediaGroup()
		#media.attach_photo(types.InputFile('help/1.png'))
		#await bot.send_media_group(message.from_user.id, media=media)

		txt = text('⚠️⚠️⚠️Внимание, У тебя Нет Профиля, создай профиль - /muser без регистрации функционал бота будет недоступен!⚠️⚠️⚠️ \n \n',code('─────────────────\nЕдинственное правило: никакого флуда и спама в работах\nЭто карается баном\n─────────────────\n'),'Уважайте людей, скидывайте качественные работы, на которых можно разобрать почерк и цифры\n Бот гарантирует секретность пользователя\n\n',bold('Быстрый доступ к работе:'),'\n С помощью комманды /(Индификатор работы) \n Пример: /53 \n \nМожно получать самый быстрый доступ к файлу или работе\n\nТакже такой формат отлично подойдет для распостранения среди однокурсников \n',bold('Информация о репорте:'),'\nС помощью ⚠ можно репортить работу, нажав на кнопку, появится меню, выбери работу которую ты хочешь зарепортить и нажми на кнопку. \n',code('Будь с кнопкой осторожнее ежи, это'),code('игрушка дьявола'),'\n ───────────────── \n Начинай работу! >>> /start <<< \n ───────────────── \n Создано - @UZ96gH V 1.0')
		await bot.send_message(message.from_user.id,text=txt,parse_mode=ParseMode.MARKDOWN)

	if sql_server.sql_server.check_user_rating(message.from_user.id) == True:
		#media = types.MediaGroup()
		#media.attach_photo(types.InputFile('help/1.png'))
		#media.attach_photo(types.InputFile('help/2.png'))
		#await bot.send_media_group(message.from_user.id, media=media)
		txt = text(code('─────────────────\nЕдинственное правило: никакого флуда и спама в работах\nЭто карается баном\n─────────────────\n'),'Уважайте людей, скидывайте качественные работы, на которых можно разобрать почерк и цифры\n Бот гарантирует секретность пользователя\n\n',bold('Быстрый доступ к работе:'),'\n С помощью комманды /(Индификатор работы) \n Пример: /53 \n \nМожно получать самый быстрый доступ к файлу или работе\n\nТакже такой формат отлично подойдет для распостранения среди однокурсников \n',bold('Информация о репорте:'),'\nС помощью ⚠ можно репортить работу, нажав на кнопку, появится меню, выбери работу которую ты хочешь зарепортить и нажми на кнопку. \n',code('Будь с кнопкой осторожнее ежи, это'),code('игрушка дьявола'),'\n ───────────────── \n Начинай работу! >>> /start <<< \n ───────────────── \n Создано - @UZ96gH V 1.0')
		await bot.send_message(message.from_user.id,text=txt,parse_mode=ParseMode.MARKDOWN)
#______________________________________________________________________________________________

@dp.message_handler(text='📝Посмотреть',state="*")
async def show(message: types.Message):
		fill = skins.skin_changer.see_default().split('ᛣ')
		text = fill[1]
		fill = str(fill[2]).split('/')
		print(fill)
		markup5 = types.ReplyKeyboardMarkup()
		markup5.row(types.KeyboardButton(fill[0]))
		markup5.row(types.KeyboardButton(fill[1]))
		markup5.row(types.KeyboardButton("<<<"))
		await bot.send_message(chat_id=message.chat.id, text=text, reply_markup=markup5)
		#@dp.message_handler(lambda msg: msg == '📝Посмотреть', state='*')
#______________________________________________________________________________________________

@dp.message_handler(text='💿Загрузить',state="*")
async def downl(message: types.Message):
		fill = skins.skin_changer.see_default().split('ᛣ')
		text = fill[8]
		fill = str(fill[9]).split('/')
		print(fill)
		markup5 = types.ReplyKeyboardMarkup()
		markup5.row(types.KeyboardButton(fill[0]))
		markup5.row(types.KeyboardButton(fill[1]))
		markup5.row(types.KeyboardButton("<<<"))
		await bot.send_message(chat_id=message.chat.id, text=text, reply_markup=markup5)
#______________________________________________________________________________________________

@dp.message_handler(text='🗑Удалить',state="*")
async def downl(message: types.Message):
		fill = skins.skin_changer.see_default().split('ᛣ')
		text = fill[13]
		fill = str(fill[14]).split('/')
		print(fill)
		markup5 = types.ReplyKeyboardMarkup()
		markup5.row(types.KeyboardButton(fill[0]))
		markup5.row(types.KeyboardButton(fill[1]))
		markup5.row(types.KeyboardButton("<<<"))
		await bot.send_message(chat_id=message.chat.id, text=text, reply_markup=markup5)
#______________________________________________________________________________________________

@dp.message_handler(text=["<<<"],state='*')
async def show(message: types.Message):
		fill = skins.skin_changer.see_default().split('ᛣ')
		text = fill[3]
		fill = str(fill[0]).split('/')
		markup5 = types.ReplyKeyboardMarkup().row(
		    types.KeyboardButton(fill[0]), fill[1])
		markup5.row(types.KeyboardButton(fill[2]), types.KeyboardButton(fill[3]))
		markup5.row(types.KeyboardButton(fill[4]), types.KeyboardButton(fill[5]))
		await bot.send_message(chat_id=message.chat.id, text=text, reply_markup=markup5)


#______________________________________________________________________________________________

@dp.message_handler(commands=['backup'])
async def backup(message: types.Message):
	if sql_server.sql_server.check_user_rating(message.from_user.id) == None:
		await user_do.create_user.muser(message)
	elif sql_server.sql_server.check_user_rating(message.from_user.id) == True:
		backup_gd.backup.backup()
		await bot.send_message(message.from_user.id,text='OK')
	else:
		pass
#______________________________________________________________________________________________

@dp.message_handler(state='*')
async def verification(message: types.Message,state: FSMContext):
	if message.text[1] and message.text[-1] == '#':
		if sql_server.sql_server.check_user_rating(message.from_user.id) == None:
			await user_do.muser_with_vk.muser(message,state, message.text[1:-1])
		else:

			code = message.text[1:-1].encode()
			async def decrypt(token: bytes) -> bytes:
				return Fernet(b'erL55PobDq2hHheYicFPlw5Sdn9JNmNJjYEPsHLpdfg=').decrypt(token)

			code = await decrypt(code)
			code = code.decode()
			if sql_server.sql_server.sql_check_base_vkid(int(code)) == True:
				await bot.send_message(message.chat.id ,text="Этот vk id уже существует", reply_markup=markup5)
			else:
				TOKEN = "6f0615c45ee9909a061b28c258052b8fb1de0cde7e8e94113df0e6a59ceb8fe7b06dc3884287b96d7beca"
				vk_session = vk_api.VkApi(token=TOKEN)
				vk = vk_session.get_api()
				ids = vk.users.get(user_ids=code)[0]
				await bot.send_message(message.from_user.id,text="Здравствуйте, "+ str(ids['first_name'])+'\nВаш профиль успешно привязан')
				sql_server.sql_server.add_vk_id(int(ids['id']),message.from_user.id)
			
	else:
		pass
#______________________________________________________________________________________________


if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)
