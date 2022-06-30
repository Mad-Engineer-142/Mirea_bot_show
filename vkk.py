# Обратите внимание, версия лонгпула должна быть больше или равна 5.103
#______________________________________________________________________________________________

 #__      ___  __  _____        _____ _______ 
 #\ \    / / |/ / |  __ \ /\   |  __ \__   __|
 # \ \  / /| ' /  | |__) /  \  | |__) | | |   
 #  \ \/ / |  <   |  ___/ /\ \ |  _  /  | |   
 #   \  /  | . \  | |  / ____ \| | \ \  | |   
 #    \/   |_|\_\ |_| /_/    \_\_|  \_\ |_|   
                                             
#______________________________________________________________________________________________
                                          
from vkwave.bots import SimpleLongPollBot, SimpleBotEvent
from vkwave.bots.core.dispatching import filters

from vkwave.bots.core.dispatching.filters.builtin import PayloadContainsFilter, AttachmentTypeFilter
from vkwave.bots.utils.uploaders import PhotoUploader, DocUploader
from vkwave.api import API
from vkwave.client import AIOHTTPClient

from config import GROUP_ID, TOKEN, GROUP_CALLING, ADMIN_VK_CALLING

import sql_server
import pickle
import  os
import PIL
from PIL import Image
from io import BytesIO

import requests
import datetime
import string
import random
import requests
import numpy as np

from cryptography.fernet import Fernet
from vkwave.bots.core.dispatching.filters import filter_caster

#______________________________________________________________________________________________

import asyncio
from vkwave.bots.storage.storages import Storage
from vkwave.bots.storage.types import Key
#______________________________________________________________________________________________

storage = Storage()
bot = SimpleLongPollBot(tokens=TOKEN, group_id=GROUP_ID)
api = API(clients=AIOHTTPClient(), tokens=TOKEN)
uploader = PhotoUploader(api.get_context())


#______________________________________________________________________________________________

@bot.message_handler(bot.text_filter(GROUP_CALLING))
async def handle(event) -> str:
	user_data = (await event.api_ctx.users.get(user_ids=event.object.object.message.from_id)).response[0] 
	if sql_server.sql_server.check_user_rating_vk(event.object.object.message.from_id) or sql_server.sql_server.check_user_rating_vk(event.object.object.message.from_id)==None:

			user_data = (await event.api_ctx.users.get(user_ids=event.object.object.message.from_id)).response[0] 
			await event.answer('К вашим услугам '+ user_data.first_name+"\nПомощь - /help")
	else:
			await event.answer(message='Вы забанены')

@bot.message_handler(bot.text_filter("начать"))
@bot.message_handler(bot.command_filter(commands=('start',"help",'помощь'), prefixes=("/") ))
async def handle(event) -> str:
	user_data = (await event.api_ctx.users.get(user_ids=event.object.object.message.from_id)).response[0] 
	if sql_server.sql_server.check_user_rating_vk(event.object.object.message.from_id) or sql_server.sql_server.check_user_rating_vk(event.object.object.message.from_id)==None:

			user_data = (await event.api_ctx.users.get(user_ids=event.object.object.message.from_id)).response[0]
			trxt = '''
				──────────────
				Единственное правило: никакого флуда и спама в работах
				Это карается баном
				──────────────
				\nКоманда /list\n для просмотра последних 4 загруженных работ
				\n/ls 2 для просмотра второй страницы последних загруженных работ
				\nЧтобы посмотреть работы и файлы пиши:
				/(индификатор работы, без скобок)\n
				Пример: /53
				\nПример загрузки фото и файлов через бота на картинке ниже\n
				 Примечания:
				- лимит фото при пересылке сообщения - 40 фото
				- лимит фото при прямой загрузке - 10 фото
				- лимит для файлов\n Всегда - 1 файл
				\nСуществует привязка аккаунта вк к основному боту в телеграме\n
				!Без привязки все ваши работы будут Анонимными\n
				Она нужна для синхронизации и лучшего управления работами и файлами
				 --> Пиши в лс боту /connect и следуй инстукции
				 --> /disconnect - отвязать акк
				\n/info - для получения информации о своем профиле
				*Только для привзанных пользователей
				\nV - 1.0
				\nПо всем вопросам и багам\n'''+ADMIN_VK_CALLING

			await event.answer('Привет '+ user_data.first_name+','+trxt)
			way = os.path.abspath('help/Vk_help.png')
			big_attachment = await uploader.get_attachments_from_paths(peer_id=event.object.object.message.peer_id,file_paths=[way])
			await event.answer(message='',attachment=big_attachment)
	else:
			await event.answer(message='Вы забанены')
#______________________________________________________________________________________________

@bot.message_handler(bot.command_filter(commands=("connect"), prefixes=("/")),bot.conversation_type_filter(from_what="from_chat"))
async def handle(event) -> str:
		await event.answer(message="Пиши /connect в лс боту") # отправляем сообщение

@bot.message_handler(bot.command_filter(commands=("info"), prefixes=("/")))
async def infos(event) -> str:
	user_data = (await event.api_ctx.users.get(user_ids=event.object.object.message.from_id)).response[0] 
	print(sql_server.sql_server.sql_check_base_vkid(int(user_data.id)))
	if sql_server.sql_server.check_user_rating_vk(int(user_data.id)) == True:
		if sql_server.sql_server.sql_check_base_vkid(int(user_data.id)) == True:

			df = sql_server.sql_server.get_info_user_id_vk(int(user_data.id))
			print(df)
			if df[1] == 5:
				word = 'Вы Админ'
			elif df[1] == 3:
				word = 'Вы редактор'
			elif df[1] == 0:
				word = 'Вы обычный юзер'

			st = 'Информация о тебе:'+'\n'+'-----------------'+'\n' + str(df[2])+' -твой никнейм '+'\n' +str(df[3])+' -твоя группа '+'\n' +str(df[1])+' -твой рейтинг \n'+word +'\n'+'-----------------'+'\n'+str(df[5])+' -Работ загружено'
			
			await event.answer(st)
	elif  sql_server.sql_server.check_user_rating_vk(int(user_data.id)) == None:
		await event.answer(message='Ваш профиль не привязан\nПиши /connect в лс боту')
	else:
		await event.answer(message='Вы забанены')

#______________________________________________________________________________________________

@bot.message_handler(bot.command_filter(commands=("connect"), prefixes=("/")),bot.conversation_type_filter(from_what="from_pm"))
async def handle(event) -> str:
	user_data = (await event.api_ctx.users.get(user_ids=event.object.object.message.from_id)).response[0] # обращаемся к апи
	print(user_data.id)
	print(sql_server.sql_server.sql_check_base_vkid(int(user_data.id)))
	if sql_server.sql_server.check_user_rating_vk(event.object.object.message.from_id):
		await event.answer(message="Такой id уже существует в базе, попробуй /disconnect") # отправляем сообщение
	else:
		h = str(user_data.id)
		async def encrypt(message: bytes, key: bytes) -> bytes:
			return Fernet(key).encrypt(message)

		a = await encrypt(h.encode(), b'erL55PobDq2hHheYicFPlw5Sdn9JNmNJjYEPsHLpdfg=')

		await event.answer(message='#'+a.decode()+'#') # отправляем сообщение
		await event.answer(message="Отправь следующее сообщение боту в телеграмм - http://t.me/Cheatbase_bot") # отправляем сообщение
#______________________________________________________________________________________________

@bot.message_handler(bot.command_filter(commands=("disconnect"), prefixes=("/")))
async def handle(event) -> str:
	user_data = (await event.api_ctx.users.get(user_ids=event.object.object.message.from_id)).response[0] # обращаемся к апи
	print(user_data.id)
	print(sql_server.sql_server.sql_check_base_vkid(int(user_data.id)))
	if sql_server.sql_server.check_user_rating_vk(event.object.object.message.from_id):
		sql_server.sql_server.add_vk_id_vk(int(user_data.id))
		await event.answer(message="Вы успешно отвязали свой профиль")
	else:
		await event.answer(message="Ваш профиль еще не привязан  -> /connect") # отправляем сообщение
#______________________________________________________________________________________________

@bot.message_handler(filters.RegexFilter(r"\A/list (\d*)\Z"))
@bot.message_handler(filters.RegexFilter(r"\A/ls (\d*)\Z"))
async def handle(event) -> str:
	user_data = (await event.api_ctx.users.get(user_ids=event.object.object.message.from_id)).response[0] 
	if sql_server.sql_server.check_user_rating_vk(event.object.object.message.from_id) or sql_server.sql_server.check_user_rating_vk(event.object.object.message.from_id)==None:
		num  = int(event.text.split(' ')[1])
		tex =sql_server.sql_server.last_works(num)
		if tex == False:
			await event.answer(message='Такая страница недоступна')
		else:
			dd = ''
			for i in tex:
				gg = list(i)[1].split('|')
				if len(gg) == 7:
					dd = dd + str(gg[0])+str(gg[1])+str(gg[2])+str(gg[6])+'\n\n'
				else:
					dd = dd + str(gg[0])+str(gg[1])+str(gg[2])+'\n'
			await event.answer(message=dd)
	else:
		await event.answer(message='Вы забанены')
#______________________________________________________________________________________________

@bot.message_handler(bot.command_filter(commands=("list"), prefixes=("/")))
@bot.message_handler(bot.command_filter(commands=("ls"), prefixes=("/")))
async def handle(event) -> str:
	user_data = (await event.api_ctx.users.get(user_ids=event.object.object.message.from_id)).response[0] 
	if sql_server.sql_server.check_user_rating_vk(event.object.object.message.from_id) or sql_server.sql_server.check_user_rating_vk(event.object.object.message.from_id)==None:
		tex =sql_server.sql_server.last_works(0)
		if tex == False:
			await event.answer(message='Такая страница недоступна')
		else:
			dd = ''
			for i in tex:
				gg = list(i)[1].split('|')
				if len(gg) == 7:
					dd = dd + str(gg[0])+str(gg[1])+str(gg[2])+str(gg[6])+'\n\n'
				else:
					dd = dd + str(gg[0])+str(gg[1])+str(gg[2])+'\n'
			await event.answer(message=dd)
	else:
		await event.answer(message='Вы забанены')
#______________________________________________________________________________________________

@bot.message_handler(filters.RegexFilter(r"\A/(\d*)\Z"))
async def only_matched_by_regex(event: SimpleBotEvent):
	user_data = (await event.api_ctx.users.get(user_ids=event.object.object.message.from_id)).response[0] 
	if sql_server.sql_server.check_user_rating_vk(event.object.object.message.from_id) or sql_server.sql_server.check_user_rating_vk(event.object.object.message.from_id)==None:
			if event.text[1:]:
				if int(event.text[1:]) == 0:
					await event.answer(message='Работы /0 не существует, не ищите ее.\nТакой работы нет, и не было никогда')    
					pass
				elif int(event.text[1:]) in sql_server.sql_server.unique_num_ask_arr():
					works = sql_server.sql_server.show_work_unique(event.text[1:])
					print(works)
					if works[2] == 'p':
						print(works)
						images = pickle.loads(works[0])
						big_attachment = await uploader.get_attachments_from_paths(peer_id=event.object.object.message.peer_id,file_paths=images)
						await event.answer(message=works[1],attachment=big_attachment)
						#await bot.send_media_group(message.from_user.id, media=media)


					elif works[2] == 'f':
						print('_______________________')
						print(works)
						
						documents = pickle.loads(works[0])
						doc = await DocUploader(api.get_context()).get_attachment_from_path(peer_id=event.object.object.message.peer_id, file_path=documents, title=works[3])
						await event.answer(message=works[1], attachment=doc)


				else:
					await event.answer(message="Такой работы нет, проверь правильность индификатора")
	elif sql_server.sql_server.check_user_rating_vk(event.object.object.message.from_id) == 'ban':
		await event.answer('Вы забанены')
#______________________________________________________________________________________________



async def recursion(cc, final_mass):
	if cc.fwd_messages == None:
		return False
	for n in cc.fwd_messages:
		if n.attachments == []:
			await recursion(cc.fwd_messages[-1], final_mass)
		else:
			for a in n.attachments:
				final_mass.append(a)
	return final_mass

async def type_check(msg, attach_type):
    return any([att.type.value==attach_type for att in msg.attachments])

#______________________________________________________________________________________________

@bot.message_handler(filters.FwdMessagesFilter())
@bot.message_handler(filters.MessageFromConversationTypeFilter("from_pm"),filters.MessageFromConversationTypeFilter("from_dm"),filters.MessageFromConversationTypeFilter("from_chat"),filters.MessageFromConversationTypeFilter("from_direct"))
async def only_matched_by_regex(event: SimpleBotEvent):
	if sql_server.sql_server.check_user_rating_vk(event.object.object.message.from_id) or sql_server.sql_server.check_user_rating_vk(event.object.object.message.from_id)==None:
		print('yes')
		photos = []
		bb = await event.api_ctx.messages.get_by_conversation_message_id(peer_id=event.object.object.message.peer_id ,group_id=event.object.group_id , conversation_message_ids=event.object.object.message.conversation_message_id)
		cc = bb.response.items
		photos = await recursion(cc[0], [])

		#gg = await type_check(event,'doc')
		#print(gg)
		if event.text:
			if event.text[0] == '#':
				await second_stage(event, photos)
	else:
		await event.answer('Вы забанены')
#______________________________________________________________________________________________

@bot.message_handler(AttachmentTypeFilter(attachment_type='photo'))
@bot.message_handler(lambda event: event.object.object.message.is_cropped)
async def only_photo(event: SimpleBotEvent):
	user_data = (await event.api_ctx.users.get(user_ids=event.object.object.message.from_id)).response[0] 
	if sql_server.sql_server.check_user_rating_vk(event.object.object.message.from_id) or sql_server.sql_server.check_user_rating_vk(event.object.object.message.from_id)==None:

		print('asdasd rabotayet')
		bb = await event.api_ctx.messages.get_by_conversation_message_id(peer_id=event.object.object.message.peer_id ,group_id=event.object.group_id , conversation_message_ids=event.object.object.message.conversation_message_id)
		photos = bb.response.items[-1].attachments
		#photos = event.object.object.message.attachments
		print(photos)
		if event.text:
			if event.text[0] == '#':
				await second_stage(event, photos)
	else:
		await event.answer('Вы забанены')
#______________________________________________________________________________________________


async def second_stage(event, photos):
		if photos == []:
			pass
		elif len(photos)>40:
			await event.answer(message="Слишком много фотографий")
		else:

			a  = event.text
			b = a.split('\n')
			if len(b) == 1:
				await event.answer(message="Ты неправильно указал аннотацию к работе, посмотри пример загрузки работы - /help")
				#way = os.path.abspath('help/Vk_help.png')
				#big_attachment = await uploader.get_attachments_from_paths(peer_id=event.object.object.message.peer_id,file_paths=[way])
				#await event.answer(message='',attachment=big_attachment)
			else:
				with open ("subjects.txt", "r", encoding='utf8') as myfile:
					subss=(myfile.read().split(','))
				predmet = b[0][1:].lower()
				while True:
					if predmet[-1] == ' ':
						 predmet = predmet[0:-1]
					else:
						break
				b[0] = predmet
				if predmet not in subss:
					await event.answer(message="Такого предмета нет")
				else:
					v = await check_var(event,b[1].replace(' ', ''))
					if v == None:
						pass
					else:
						print('aboba')
						print(photos[-1])
						#print(photos[-1].object.type)
						if photos[-1].doc:
							print('+document')
							await upload_file(event, photos, v, b)
						elif photos[-1].photo:
							print('++photos')
							await upload(event, photos, v, b)
						#print(b.split(" "))
						#doc = await uploader.get_attachments_from_links(peer_id=event.object.object.message.peer_id, links=[event.object.object.message.attachments[0].photo.sizes[-1].url])
						#await event.answer(message=event.text, attachment=doc)
						print('adads')
#______________________________________________________________________________________________

@bot.message_handler(AttachmentTypeFilter(attachment_type='doc'))
async def only_matched_by_regex(event: SimpleBotEvent):
	user_data = (await event.api_ctx.users.get(user_ids=event.object.object.message.from_id)).response[0] 
	if sql_server.sql_server.check_user_rating_vk(event.object.object.message.from_id) or sql_server.sql_server.check_user_rating_vk(event.object.object.message.from_id)==None:
		print('files rabotayet')
		photos = event.object.object.message.attachments
		if event.text:
			if event.text[0] == '#':
				print('second Fiels')
				await second_stage(event, photos)
	else:
		await event.answer('Вы забанены')
#______________________________________________________________________________________________


async def upload(event,photos, pvars, b):
		user_data = (await event.api_ctx.users.get(user_ids=event.object.object.message.from_id)).response[0] # обращаемся к апи
		way_arr = []
		if sql_server.sql_server.sql_check_base_vkid(int(user_data.id)):
			if len(photos)<=10:
				for i in photos:
					print(i)
					iobytes = requests.get(i.photo.sizes[-1].url).content
					if not os.path.exists('photo/'+str(sql_server.sql_server.add_vk_id_to_tg_id(int(user_data.id)))):
						os.makedirs('photo/'+str(sql_server.sql_server.add_vk_id_to_tg_id(int(user_data.id))))
					else:
						pass
					way = 'photo/'+str(sql_server.sql_server.add_vk_id_to_tg_id(int(user_data.id)))+'/'+''.join(random.choice(string.ascii_lowercase+string.digits+string.ascii_letters) for i in range(12))+'.jpg'
					way_arr.append(way)
					with open(way, "wb") as outfile:
						outfile.write(iobytes)
			else:
				if not os.path.exists('photo/'+str(sql_server.sql_server.add_vk_id_to_tg_id(int(user_data.id)))):
					os.makedirs('photo/'+str(sql_server.sql_server.add_vk_id_to_tg_id(int(user_data.id))))
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
							way = 'photo/'+str(sql_server.sql_server.add_vk_id_to_tg_id(int(user_data.id)))+'/'+''.join(random.choice(string.ascii_lowercase+string.digits+string.ascii_letters) for i in range(12))+'.jpg'
							way_arr.append(way)

							iobytes = requests.get(msa[a]).content
							iobytes = BytesIO(iobytes)
							coverted.append(Image.open(iobytes).convert("RGB"))
						else:


							iobytes = requests.get(msa[a]).content
							iobytes = BytesIO(iobytes)
							coverted.append(Image.open(iobytes).convert("RGB"))

						min_shape = sorted([(np.sum(i.size), i.size ) for i in coverted])[0][1]
						imgs_comb = np.hstack((np.asarray(i.resize(min_shape)) for i in coverted))
						imgs_comb = PIL.Image.fromarray(imgs_comb)
						imgs_comb.save(way)

			varss = ''
			if pvars[0] == '-':
					vv = [pvars[1],pvars[2]]
					varss = min(vv)+'-'+max(vv)
					print(varss)
			else:
				for i in pvars:
					if i != None:
						varss = varss +' '+i

			today = datetime.datetime.today()
			date_cortage = today.strftime("%d/%m/%Y").split('/')

			user_name = list(sql_server.sql_server.user_id_to_vkid(int(user_data.id)))
			unique = sql_server.sql_server.unique_num()
			print(user_name)
			print(unique)
			print(b)
			#('Admin', 'ИБ-12')
			#10
			#['#Химия', '4-32', 'фыв']

			if len(b) == 3:
				caption = ' /'+str(unique)+'\n|Предмет:'+b[0].lower()+'\n|Автор:'+str(user_name[0])+'\n|Группа: '+str(user_name[1])+'\n|Вариант(ы): '+varss+'\n|Дата: '+str(date_cortage[0])+':'+str(date_cortage[1])+':'+str(date_cortage[2]+'\n|Примечание к работе: '+b[2])
			else:
				caption = ' /'+str(unique)+'\n|Предмет:'+b[0].lower()+'\n|Автор:'+str(user_name[0])+'\n|Группа: '+str(user_name[1])+'\n|Вариант(ы): '+varss+'\n|Дата: '+str(date_cortage[0])+':'+str(date_cortage[1])+':'+str(date_cortage[2])

			unique_num = sql_server.sql_server.img_save(way_arr,caption,b[0].lower(),0,0, 'p',pvars, date_cortage,user_name[2], unique, None) #11
			await event.answer(message=user_data.first_name+' успешно загрузил работу: \n/'+str(unique))


		else:
			if len(photos)<=10:
				print('anonumys')
				for i in photos:
					iobytes = requests.get(i.photo.sizes[-1].url).content
					if not os.path.exists('photo/anon/'):
						os.makedirs('photo/anon/')
					else:
						pass
					way = 'photo/anon/'+''.join(random.choice(string.ascii_lowercase+string.digits+string.ascii_letters) for i in range(12))+'.jpg'
					way_arr.append(way)
					with open(way, "wb") as outfile:
						outfile.write(iobytes)
			else:
				print('more than 10 photos')
				if not os.path.exists('photo/anon/'):
					os.makedirs('photo/anon/')
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
							way = 'photo/anon/'+''.join(random.choice(string.ascii_lowercase+string.digits+string.ascii_letters) for i in range(12))+'.'+photos[-1].doc.ext
							way_arr.append(way)

							iobytes = requests.get(msa[a]).content
							iobytes = BytesIO(iobytes)
							coverted.append(Image.open(iobytes).convert("RGB"))
						else:
							print('not_writting name')

							iobytes = requests.get(msa[a]).content
							iobytes = BytesIO(iobytes)
							coverted.append(Image.open(iobytes).convert("RGB"))

						min_shape = sorted([(np.sum(i.size), i.size ) for i in coverted])[0][1]
						imgs_comb = np.hstack((np.asarray(i.resize(min_shape)) for i in coverted))
						imgs_comb = PIL.Image.fromarray(imgs_comb)
						print('downloading')
						imgs_comb.save(way)

			print('varianty')
			varss = ''
			if pvars[0] == '-':
					vv = [pvars[1],pvars[2]]
					varss = min(vv)+'-'+max(vv)
					print(varss)
			else:
				for i in pvars:
					if i != None:
						varss = varss +' '+i
			today = datetime.datetime.today()
			date_cortage = today.strftime("%d/%m/%Y").split('/')
			unique = sql_server.sql_server.unique_num()


			if len(b) == 3:
				caption = ' /'+str(unique)+'\n|Предмет:'+b[0].lower()+'\n|Автор:'+'Аноним'+'\n|Группа: '+'Неизвестна'+'\n|Вариант(ы): '+varss+'\n|Дата: '+str(date_cortage[0])+':'+str(date_cortage[1])+':'+str(date_cortage[2]+'\n|Примечание к работе:'+b[2])
			else:
				caption = ' /'+str(unique)+'\n|Предмет:'+b[0].lower()+'\n|Автор:'+'Аноним'+'\n|Группа: '+'Неизвестна'+'\n|Вариант(ы): '+varss+'\n|Дата: '+str(date_cortage[0])+':'+str(date_cortage[1])+':'+str(date_cortage[2])
			unique_num = sql_server.sql_server.img_save(way_arr,caption,b[0].lower(),0,0, 'p',pvars, date_cortage,0, unique, None) #11
			await event.answer(message=user_data.first_name+' анонимно загрузил работу: \n/'+str(unique))

#______________________________________________________________________________________________

async def upload_file(event,photos, pvars, b):
		user_data = (await event.api_ctx.users.get(user_ids=event.object.object.message.from_id)).response[0] # обращаемся к апи
		if sql_server.sql_server.sql_check_base_vkid(int(user_data.id)):
				iobytes = requests.get(photos[-1].doc.url).content
				if not os.path.exists('files/'+str(sql_server.sql_server.add_vk_id_to_tg_id(int(user_data.id)))):
					os.makedirs('files/'+str(sql_server.sql_server.add_vk_id_to_tg_id(int(user_data.id))))
				else:
					pass
				way = 'files/'+str(sql_server.sql_server.add_vk_id_to_tg_id(int(user_data.id)))+'/'+''.join(random.choice(string.ascii_lowercase+string.digits+string.ascii_letters) for i in range(12))+'.'+photos[-1].doc.ext
				with open(way, "wb") as outfile:
					outfile.write(iobytes)

				varss = ''
				if pvars[0] == '-':
						vv = [pvars[1],pvars[2]]
						varss = min(vv)+'-'+max(vv)
						
						
						
				else:
					for i in pvars:
						if i != None:
							varss = varss +' '+i

				today = datetime.datetime.today()
				date_cortage = today.strftime("%d/%m/%Y").split('/')
				user_name = list(sql_server.sql_server.user_id_to_vkid(int(user_data.id)))
				unique = sql_server.sql_server.unique_num()
				print(way)
				#('Admin', 'ИБ-12')
				#10
				#['#Химия', '4-32', 'фыв']
				if len(b) == 3:
					caption = ' /'+str(unique)+'\n|Предмет:'+b[0].lower()+'\n|Название файла:'+photos[-1].doc.title+'\n|Автор:'+str(user_name[0])+'\n|Группа: '+str(user_name[1])+'\n|Вариант(ы): '+varss+'\n|Дата: '+str(date_cortage[0])+':'+str(date_cortage[1])+':'+str(date_cortage[2]+'\n|Примечание к работе: '+b[2])
				else:
					caption = ' /'+str(unique)+'\n|Предмет:'+b[0].lower()+'\n|Название файла:'+photos[-1].doc.title+'\n|Автор:'+str(user_name[0])+'\n|Группа: '+str(user_name[1])+'\n|Вариант(ы): '+varss+'\n|Дата: '+str(date_cortage[0])+':'+str(date_cortage[1])+':'+str(date_cortage[2])
				
				unique_num = sql_server.sql_server.img_save(way,caption,b[0].lower(),0,0, 'f',pvars, date_cortage, user_name[2], unique, photos[-1].doc.title) #11
				await event.answer(message=user_data.first_name+' успешно загрузил файл: \n/'+str(unique))


		else:
			print('anonumys')
			iobytes = requests.get(photos[-1].doc.url).content
			if not os.path.exists('files/anon/'):
				os.makedirs('files/anon/')
			else:
				pass
			way = 'files/anon/'+''.join(random.choice(string.ascii_lowercase+string.digits+string.ascii_letters) for i in range(12))+'.'+photos[-1].doc.ext
			with open(way, "wb") as outfile:
				outfile.write(iobytes)
		

			print('varianty')
			varss = ''
			if pvars[0] == '-':
					vv = [pvars[1],pvars[2]]
					varss = min(vv)+'-'+max(vv)
					print(varss)
			else:
				for i in pvars:
					if i != None:
						varss = varss +' '+i
			today = datetime.datetime.today()
			date_cortage = today.strftime("%d/%m/%Y").split('/')
			unique = sql_server.sql_server.unique_num()


			if len(b) == 3:
				caption = ' /'+str(unique)+'\n|Предмет:'+b[0].lower()+'\n|Название файла:'+photos[-1].doc.title+'\n|Автор: Аноним'+'\n|Группа: Неизвестна'+'\n|Вариант(ы): '+varss+'\n|Дата: '+str(date_cortage[0])+':'+str(date_cortage[1])+':'+str(date_cortage[2]+'\n|Примечание к работе: '+b[2])
			else:
				caption = ' /'+str(unique)+'\n|Предмет:'+b[0].lower()+'\n|Название файла:'+photos[-1].doc.title+'\n|Автор: Аноним'+'\n|Группа: Неизвестна'+'\n|Вариант(ы): '+varss+'\n|Дата: '+str(date_cortage[0])+':'+str(date_cortage[1])+':'+str(date_cortage[2])
			unique_num = sql_server.sql_server.img_save(way,caption,b[0].lower(),0,0, 'f',pvars, date_cortage, 0, unique, photos[-1].doc.title)
			await event.answer(message=user_data.first_name+' анонимно загрузил файл: \n/'+str(unique))

#______________________________________________________________________________________________

async def check_var(event, varss):
	if ',' in varss:
		if ',' in varss.split():
			await event.answer(message='Некорректно введен вариант')
		else:
			for i in varss.split(','):
				if i.isdigit():
					if len(varss.split(','))>4:
						await event.answer(message='Не больше 4 вариантов за раз')
					else:
						var = varss.split(',')
						for i in range(4-len(var)):
							var.append(None)
				else:
					await event.answer(message='Некорректно введен вариант')
					return None
			return var
	elif '-' in varss:
		if len(varss.split('-')) == 2:
			for i in varss.split('-'):
				if i.isdigit():
					varsss = varss.split('-')
					var = ['-']
					for i in varsss:
						var.append(i)
					var.append(None)
				else:
					await event.answer(message='Некорректно введен вариант')
			return var
		else:
			await event.answer(message='Некорректно введен вариант')
	elif '—' in varss:
			if len(varss.split('—')) == 2:
				for i in varss.split('—'):
					if i.isdigit():
						varsss = varss.split('—')
						var = ['-']
						for i in varsss:
							var.append(i)
						var.append(None)
					else:
						await event.answer(message='Некорректно введен вариант')
				return var
			else:
				await event.answer(message='Некорректно введен вариант')
	elif varss.isdigit():
		var = [varss, None, None, None]
		return var
	else:
		await event.answer(message='Некорректно введен вариант, нужно ввести не более четырех вариантов\nИли через тире (4-6)')

@bot.message_handler()
async def group_join(event):
	try:	
		if event.object.message.action.member_id == -GROUP_ID:
			way = os.path.abspath('help/group_join.png')
			big_attachment = await uploader.get_attachments_from_paths(peer_id=event.object.object.message.peer_id,file_paths=[way])
			await event.answer(message='',attachment=big_attachment)
		else:
			pass
	except AttributeError:
		pass
#______________________________________________________________________________________________

bot.run_forever()
