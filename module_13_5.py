

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio


api = ' '
bot = Bot(token = api)
dp = Dispatcher(bot, storage = MemoryStorage())


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

kb = ReplyKeyboardMarkup()
button = KeyboardButton(text = 'Информация')
button2 = KeyboardButton(text = 'Рассчитать')
kb.row(button, button2)

@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer("Привет! Я бот помогающий твоему здоровью:", reply_markup=kb)

@dp.message_handler(text = 'Информация')
async def inform(message):
    await message.answer('Рекомендуемая норма потребления каллорий рассчитана по формуле Мифлина-Сан Жеора')

@dp.message_handler(text = 'Рассчитать')
async def set_age(message):
    await message.answer('Введите свой возраст:')
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    data = await state.get_data()
    await message.answer('Введите свой рост:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    data = await state.get_data()
    await message.answer('Введите свой вес:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    await message.answer("Норма каллорий для Вас (для мужчин) "
    f"{10 * float(data['weight']) + 6.25 * float(data['growth']) - 5 * float(data['age']) + 5}")

@dp.message_handler()  # Мы получили сообщение
async def all_message(message):
    await message.answer("Введите команду /start, чтобы начать общение.")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)





