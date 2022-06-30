from aiogram import types
from config import dp, bot

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

import datetime
import sql_server
import mat 
import os
import skins

class Upload(StatesGroup):
    waiting_for_file = State()
    waiting_for_subject_file= State()
    waiting_for_variant_file = State()
    waiting_for_checked_file = State()
    waiting_for_text_file = State()
    waiting_for_end_file = State()


@dp.message_handler(text=['🔖Загрузить Файлы'],state='*')
async def upload_work(message: types.Message,state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(types.KeyboardButton('<<<'))
    message = await bot.send_message(message.chat.id, 'Пришли своей файл работы', reply_markup=keyboard)
    await Upload.waiting_for_subject_file.set()

@dp.callback_query_handler(lambda c: c.data == 'upload_files', state='*')
async def upload_work(message: types.Message,state: FSMContext):
    await bot.delete_message(message.from_user.id, message.message.message_id)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(types.KeyboardButton('<<<'))
    message = await bot.send_message(message.message.chat.id, 'Пришли своей файл работы', reply_markup=keyboard)
    await Upload.waiting_for_subject_file.set()


'''@dp.message_handler(state=Upload.waiting_for_file, content_types=types.ContentType.DOCUMENT)
async def Photo(message: types.Message, state: FSMContext):
    await state.update_data(file=message.document)
    #ВСТАЛ ВОПРОС
    keyboard = types.InlineKeyboardMarkup()
    key_yes = types.InlineKeyboardButton(text='1', callback_data='1');
    keyboard.add(key_yes);
    key_yes = types.InlineKeyboardButton(text='2', callback_data='2');
    keyboard.add(key_yes);
    key_yes = types.InlineKeyboardButton(text='3', callback_data='3');
    keyboard.add(key_yes);
    key_yes = types.InlineKeyboardButton(text='4', callback_data='4');
    keyboard.add(key_yes);
    message = await bot.send_message(message.chat.id, 'Нажми на курс к которому принадлежит файл:', reply_markup= keyboard)
    await Upload.waiting_for_subject_file.set()'''

@dp.message_handler(state=Upload.waiting_for_subject_file, content_types=types.ContentType.DOCUMENT)
async def Confirm(message: types.Message, state: FSMContext):
    await state.update_data(file=message.document)

    subs = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    with open ("subjects.txt", "r", encoding='utf8') as myfile:
        subss=(myfile.read().split(','))

    for i in subss:
             button_hi = types.KeyboardButton(i)
             subs.add(button_hi)
    await bot.send_message(message.chat.id, "Выбери или напиши предмет по которому прислал файл", reply_markup=subs)
    await Upload.waiting_for_variant_file.set()

@dp.message_handler(state=Upload.waiting_for_variant_file, content_types=types.ContentTypes.TEXT)
async def waiting_for_variant_file(message: types.Message, state: FSMContext): 
    with open ("subjects.txt", "r", encoding='utf8') as myfile:
        subss=(myfile.read().split(','))
    if message.text.lower() not in subss:
        await bot.send_message(message.chat.id, text="Некоректный предмет, введи еще раз")
        return
    else:
        await state.update_data(subject=message.text.lower())
        await bot.send_message(message.chat.id,text='Напиши Вариант(ы) через запятую, не более четырех вариантов') 
        await Upload.waiting_for_text_file.set()

'''@dp.callback_query_handler(lambda c: c.data in ['yes_ch','no_ch'], state=Upload.waiting_for_checked_file)
async def check(message: types.Message, state: FSMContext): 
    await bot.delete_message(message.from_user.id, message.message.message_id)
    if message.data == 'yes_ch':
        await state.update_data(check=True)
    elif message.data == 'no_ch':
        await state.update_data(check=False)

    await bot.send_message(message.message.chat.id, text='Напиши Вариант(ы) через запятую, не более четырех вариантов',reply_markup=types.ReplyKeyboardRemove())  
    await Upload.waiting_for_text_file.set()'''



@dp.message_handler(state=Upload.waiting_for_text_file, content_types=types.ContentTypes.TEXT)
async def waiting_for_text_file(message: types.Message, state: FSMContext): 
    if ',' in message.text:
        if ',' in message.text.split():
            await bot.send_message(message.chat.id, text='Некорректно введен вариант')
            return
        else:
            for i in message.text.split(','):
                if i.isdigit():
                    if len(message.text.split(','))>4:
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
        if len(message.text.split('-')) == 2:
            for i in message.text.split('-'):
                if i.isdigit():
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

    await state.update_data(var= var)
    subs = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    subs.add(types.KeyboardButton('Нет'))
    await bot.send_message(message.chat.id, text='Примечания к файлу (не более 250 символов)',reply_markup=subs)
    await Upload.waiting_for_end_file.set()

@dp.message_handler(state=Upload.waiting_for_end_file, content_types=types.ContentTypes.TEXT)
async def waiting_for_end_file(message: types.Message, state: FSMContext): 
    if message.text == 'Нет':
        await state.update_data(text=None)
    else:
        if mat.mat_check.mat_checker(message.text):
            await bot.send_message(message.chat.id, text='Не матюкайся')
            return
        else:
            await state.update_data(text=message.text)
    user_data = await state.get_data()
    i = user_data['file']
    file = await bot.get_file(i.file_id)
    iobytes = await bot.download_file(file_path=file.file_path)
    file_name = i.file_name
    last_name = file_name.split('.')[-1]
    if not os.path.exists('files/'+str(message.from_user.id)):
        os.makedirs('files/'+str(message.from_user.id))
    else:
        pass
    way = 'files/'+str(message.from_user.id)+'/'+ i.file_id+'.'+last_name
    with open(way, "wb") as outfile:
        outfile.write(iobytes.getbuffer())
    
    varss = ''
    print(user_data['var'])
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
        caption = ' /'+str(unique)+'\n|Название файла:'+file_name+'\n|Предмет:'+user_data['subject']+'\n|Автор:'+str(user_name[0])+'\n|Группа: '+str(user_name[1])+'\n|Вариант(ы): '+varss+'\n|Дата: '+str(date_cortage[0])+':'+str(date_cortage[1])+':'+str(date_cortage[2]+'\n|Примечание к работе:'+user_data['text'])
    else:
        caption = ' /'+str(unique)+'\n|Название файла:'+file_name+'\n|Предмет:'+user_data['subject']+'\n|Автор:'+str(user_name[0])+'\n|Группа: '+str(user_name[1])+'\n|Вариант(ы): '+varss+'\n|Дата: '+str(date_cortage[0])+':'+str(date_cortage[1])+':'+str(date_cortage[2])

    unique_num = sql_server.sql_server.img_save(way,caption,user_data['subject'],0,0, 'f',user_data['var'], date_cortage, message.from_user.id, unique, file_name)
    fill = skins.skin_changer.see_default().split('ᛣ')
    fill = str(fill[0]).split('/')
    markup5 = types.ReplyKeyboardMarkup().row(
        types.KeyboardButton(fill[0]), fill[1])
    markup5.row(types.KeyboardButton(fill[2]), types.KeyboardButton(fill[3]))
    markup5.row(types.KeyboardButton(fill[4]), types.KeyboardButton(fill[5]))
    await bot.send_message(message.chat.id, text='Вы успешно загрузили файл\nИндификатор файла - /'+str(unique_num),reply_markup=markup5)
    await state.finish()

