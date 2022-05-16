from aiogram import Dispatcher, Bot, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from utils import UserState
from TOKEN import TOKEN
from KeyButtons import kb, bc
from random import randrange
import defs

Token = TOKEN
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())


@dp.message_handler(state='*', commands=['start'])
async def start_command(message: types.Message):
    await bot.send_photo(message.chat.id, 'https://i.imgur.com/q9nQfR1.jpeg', reply_markup=kb,
                         caption=f'Привет {message.from_user.username} \n'
                                 f'Вот что я умею:\n'
                                 f'/Search_user - поиск пользователья по имени\n'
                                 f'/Search_map_by_id - поиск карты по её id\n'
                                 f'/Random_map - рандомная карта\n'
                                 f'/back - вернуться обратно')


@dp.message_handler(state='*', commands=['help'])
async def help_def(message: types.Message):
    await message.answer('/Search_user - поиск пользователья по имени\n'
                         '/Search_map_by_id - поиск карты по её id\n'
                         '/Random_map - рандомная карта'
                         '/back - вернуться обратно')


@dp.message_handler(state='*', commands=['Search_user'])
async def find_user(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    await state.set_state(UserState.all()[1])
    await message.answer('Введите название игрока', reply_markup=bc)


@dp.message_handler(state='*', commands=['Search_map_by_id'])
async def find_map_by_id(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    await state.set_state(UserState.all()[0])
    await message.answer('Введите id карты', reply_markup=bc)


@dp.message_handler(state='*', commands=['Random_map'])
async def random_map(message: types.Message):
    id = randrange(1232451, 2451235)
    data = defs.get_info_map(id)
    while defs.check_valid(data) is False:
        id = randrange(1232451, 2451235)
        data = defs.get_info_map(id)
    await bot.send_photo(message.chat.id, data.get('beatmapset').get('covers').get('cover'),
                         caption=defs.create_message_for_map(data))


@dp.message_handler(state='*', commands=['back'])
async def back(message:types.Message):
    state = dp.current_state(user=message.from_user.id)
    await message.answer('Выберите команду', reply_markup=kb)
    await state.reset_state()


@dp.message_handler(state=UserState.USER_STATE)
async def get_user(message: types.Message):
    data = defs.get_info_user(message.text)
    if defs.check_valid(data):
        photo = defs.picture(avatar=data.get("avatar_url"), banner=data.get("cover_url"))
        await bot.send_photo(message.chat.id, photo, caption=defs.create_message_for_user(data),
                             reply_markup=bc)
    else:
        await message.answer('Пойзователь не найден', reply_markup=bc)


@dp.message_handler(state=UserState.MAP_STATE)
async def get_map(message: types.Message):
    data = defs.get_info_map(message.text)
    if defs.check_valid(data):
        await bot.send_photo(message.chat.id, data.get('beatmapset').get('covers').get('cover'),
                         caption=defs.create_message_for_map(data), reply_markup=bc)
    else:
        await message.answer('Карта не найдена', reply_markup=bc)


@dp.message_handler(state='*')
async def err(message: types.Message):
    await message.answer('/help - Основные команды\n'
                         '/start - старт бота')

executor.start_polling(dp, skip_updates=True)
