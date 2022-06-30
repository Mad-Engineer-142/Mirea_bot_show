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

@dp.message_handler(text=['⚙️Настройки'],state='*')
async def settings(message: types.Message,state: FSMContext):
	fill = skins.skin_changer.see_default().split('ᛣ')
	fill = str(fill[11]).split('/')
	text = fill[0]
	keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
	keyboard.row(types.KeyboardButton('<<<'))
	
	keyboard.row(types.KeyboardButton(fill[2]))
	keyboard.row(types.KeyboardButton(fill[3]))
	keyboard.row(types.KeyboardButton(fill[4]))

	await bot.send_message(message.chat.id, text, reply_markup=keyboard)
