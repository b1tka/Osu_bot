import requests
from pprint import pprint
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import urllib


def get_token():
    data = {
        'client_id': 14465,
        'client_secret': '3R0DNilKL8ceGgTRWQZcfZ2xILJRPreXQUvDz06I',
        'grant_type': 'client_credentials',
        'scope': 'public'
    }
    r = requests.post('https://osu.ppy.sh/oauth/token', data=data)
    return r.json()


def get_info_user(username):
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {get_token().get("access_token")}'
    }
    r = requests.get(f'https://osu.ppy.sh/api/v2/users/{username}/osu?key=username', headers=headers)
    return r.json()


def best_maps(id_username):
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {get_token().get("access_token")}'
    }
    r = requests.get(f'https://osu.ppy.sh/api/v2/users/{id_username}/scores/best?include_fails=0&mode=osu&limit=3',
                     headers=headers)
    return r.json()


def get_info_map(id_map, name=False):
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {get_token().get("access_token")}'
    }
    if name is False:
        r = requests.get(f'https://osu.ppy.sh/api/v2/beatmaps/lookup?id={id_map}', headers=headers)
    else:
        r = requests.get(f'https://osu.ppy.sh/api/v2/beatmaps/lookup?filename={name}', headers=headers)
    return r.json()


def create_message_for_user(data):
    maps = best_maps(data.get("id"))
    if len(maps) >= 3:
        mess = f'Пользователь: {data.get("username")}\n' \
               f'Текущее pp: {round(data.get("statistics").get("pp"))}\n' \
               f'Сыгранно времени: {round(data.get("statistics").get("play_time") / 3600)} hours\n' \
               f'Уровень: {data.get("statistics").get("level").get("current")}\n' \
               f'Ранк по миру: {data.get("statistics").get("global_rank")}\n' \
               f'Лучшие карты - сколько pp получено: \n' \
               f'{maps[0].get("beatmap").get("url")} - {maps[0].get("pp")}\n' \
               f'{maps[1].get("beatmap").get("url")} - {maps[1].get("pp")}\n' \
               f'{maps[2].get("beatmap").get("url")} - {maps[2].get("pp")}'
    else:
        mess = f'Пользователь: {data.get("username")}\n' \
               f'Текущее pp: {round(data.get("statistics").get("pp"))}\n' \
               f'Сыгранно времени: {round(data.get("statistics").get("play_time") / 3600)} hours\n' \
               f'Уровень: {data.get("statistics").get("level").get("current")}\n' \
               f'Ранк по миру: {data.get("statistics").get("global_rank")}\n' \
               f'Слишком мало карт'
    return mess


def check_valid(data):
    if 'error' in data:
        return False
    return True


def create_message_for_map(data):
    mess = f'Map: {data.get("beatmapset").get("title")}\n' \
           f'Creator: {data.get("beatmapset").get("creator")}\n' \
           f'bpm: {data.get("bpm")}\n' \
           f'Ranked: {"True" if data.get("beatmapset").get("ranked") == 1 else "False"}\n' \
           f'Mode: {data.get("mode")}\n'\
           f'Link: {data.get("url")}'
    return mess


def picture(avatar, banner, data):
    ban = Image.open(BytesIO(urllib.request.urlopen(banner).read()))
    av = Image.open(BytesIO(urllib.request.urlopen(avatar).read()))
    ban.paste(av, (194, 122))
    draw_text = ImageDraw.Draw(ban)
    font = ImageFont.truetype('C:/Shrift/KyivTypeSans-VarGX.ttf', size=150)
    draw_text.text((700, 125), text=data.get('username'), fill='#1C0606', font=font)
    ban.save('res.png')
    return open('res.png', 'rb')


if __name__ == '__main__':
    pprint(get_info_user('Slavick231'))