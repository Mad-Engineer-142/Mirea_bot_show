from aiogram import types
from config import dp, bot

import pandas as pd
from aiogram import types
import datetime

@dp.message_handler(commands=['timetable'], state="*")
async def timetable(message: types.Message):
	df = pd.read_excel('1_course.xlsx')
	df = df['ЩИКО - 02 - 20                                                                              (ИБ - 12)'].tolist()
	print(df)