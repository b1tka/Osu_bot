from aiogram import Dispatcher, Bot, types, executor
import requests
from TOKEN import TOKEN
import defs

Token = TOKEN
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def new_user(message: types.Message):
    await message.answer('Бот kar1Osu')


@dp.message_handler()
async def get_user(message: types.Message):
    data = defs.get_info(message.text)
    maps = defs.best_maps(data.get("id"))
    mess = f'User: {data.get("username")}\n' \
           f'Current pp: {round(data.get("statistics").get("pp"))}\n' \
           f'Total play time: {round(data.get("statistics").get("play_time") / 3600)} hours\n' \
           f'Level: {data.get("statistics").get("level").get("current")}\n' \
           f'Global Ranking: {data.get("statistics").get("global_rank")}\n' \
           f'Best Scores: \n' \
           f'{maps[0].get("beatmap").get("url")}\n' \
           f'{maps[1].get("beatmap").get("url")}\n' \
           f'{maps[2].get("beatmap").get("url")}\n'
    photo = defs.picture(avatar=data.get("avatar_url"), banner=data.get("cover_url"))
    await bot.send_photo(message.chat.id, photo, caption=mess)


executor.start_polling(dp, skip_updates=True)
