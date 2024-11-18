from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio


api = '7896102855:AAHI1_Ozmi5PdqWVy9arpb1jibnmxwbFK9g'
bot = Bot(token = api)
dp = Dispatcher(bot, storage = MemoryStorage())


# Инициализация клавиатуры
# Содаем переменную и иницианализируем ее как экземпляр класса "ReplyKeyboardMarkup"
kb = ReplyKeyboardMarkup()

# Кнопка базируется на KeyboardButton и внутри содержит некий текст
#Метод add добавления кнопок в клавиатуру
button = KeyboardButton( text = 'Информация')
button2 = KeyboardButton( text = 'Начало')
kb.add(button)
kb.add(button2)
@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer("Привет!", reply_markup = kb) # reply_makup позволяет отображать клавиатуру

@dp.message_handler(text = 'Информация')
async def inform(message):
    await message.answer('Информация о боте!')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)