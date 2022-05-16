import requests
from PIL import Image
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
    r = requests.get(f'https://osu.ppy.sh/api/v2/users/{id_username}'
                     f'/scores/best?include_fails=0&mode=osu&limit=3',
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
    mess = f'Карта: {data.get("beatmapset").get("title")}\n' \
           f'Создатель: {data.get("beatmapset").get("creator")}\n' \
           f'Бпм: {data.get("bpm")}\n' \
           f'Ранкед: {"True" if data.get("beatmapset").get("ranked") == 1 else "False"}\n' \
           f'Мод: {data.get("mode")}\n'\
           f'Ссылка на карту: {data.get("url")}'
    return mess


def picture(avatar, banner):
    ban = Image.open(BytesIO(urllib.request.urlopen(banner).read()))
    av = Image.open(BytesIO(urllib.request.urlopen(avatar).read()))
    ban.paste(av, (194, 122))
    ban.save('res.png')
    return open('res.png', 'rb')


if __name__ == '__main__':
   pass