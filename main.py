from aiogram import Dispatcher, Bot, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from utils import UserState
from TOKEN import TOKEN
from KeyButtons import kb, bc
import defs

Token = TOKEN
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())


@dp.message_handler(state='*', commands=['start'])
async def start_command(message: types.Message):
    await message.reply('Что хотите сделать?', reply_markup=kb)


@dp.message_handler(state='*', commands=['Search_user'])
async def find_user(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    await state.set_state(UserState.all()[1])
    await message.answer('Введите название игрока')


@dp.message_handler(state='*', commands=['Random_map'])
async def find_map(message:types.Message):
    state = dp.current_state(user=message.from_user.id)
    await state.set_state(UserState.all()[2])
    await message.answer('Введите название карты')


@dp.message_handler(state='*', commands=['back'])
async def back(message:types.Message):
    state = dp.current_state(user=message.from_user.id)
    await message.answer('Что хотите сделать?', reply_markup=kb)
    await state.reset_state()


@dp.message_handler(state=UserState.USER_STATE)
async def get_user(message: types.Message):
    data = defs.get_info_user(message.text)
    if defs.check_valid_user(data):
        photo = defs.picture(avatar=data.get("avatar_url"), banner=data.get("cover_url"))
        await bot.send_photo(message.chat.id, photo, caption=defs.create_message_for_user(data),
                             reply_markup=bc)
    else:
        await message.answer('Пойзователь не найден')


@dp.message_handler(state=UserState.MAP_STATE)
async def get_map(message: types.Message):
    data = defs.get_info_map(message)



@dp.message_handler(state='*')
async def err(message: types.Message):
    await message.answer('err')

executor.start_polling(dp, skip_updates=True)
