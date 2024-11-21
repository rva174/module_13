# Лекция Инлайн клавиатуры

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio


api = '7896102855:AAHI1_Ozmi5PdqWVy9arpb1jibnmxwbFK9g'
bot = Bot(token = api)
dp = Dispatcher(bot, storage = MemoryStorage())

kb = InlineKeyboardMarkup()
button = InlineKeyboardButton(text = 'Информация', callback_data = 'info')
kb.add(button)

start_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text = 'Info')],
        [KeyboardButton(text='shop'),
         KeyboardButton(text='donate')
         ]
    ], resize_keyboard = True
)




@dp.message_handler(commands=['start'])
async def starter(message):
    await message.answer("Рады вас видеть!", reply_markup = start_menu)

# @dp.callback_query_handler(text = 'info')
#
# async def infor(call):
#     await call.message.answer("Информация о боте")
#     await call.answer()



if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

