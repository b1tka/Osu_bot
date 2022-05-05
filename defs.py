import requests
from pprint import pprint
from PIL import Image, ImageDraw
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


def get_info_map(id_map):
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {get_token().get("access_token")}'
    }
    r = requests.get(f'https://osu.ppy.sh/api/v2/beatmaps/lookup?id={id_map}', headers=headers)
    return r.json()


def create_message_for_user(data):
    maps = best_maps(data.get("id"))
    if len(maps) >= 3:
        mess = f'User: {data.get("username")}\n' \
               f'Current pp: {round(data.get("statistics").get("pp"))}\n' \
               f'Total play time: {round(data.get("statistics").get("play_time") / 3600)} hours\n' \
               f'Level: {data.get("statistics").get("level").get("current")}\n' \
               f'Global Ranking: {data.get("statistics").get("global_rank")}\n' \
               f'Best Scores: \n' \
               f'{maps[0].get("beatmap").get("url")}\n' \
               f'{maps[1].get("beatmap").get("url")}\n' \
               f'{maps[2].get("beatmap").get("url")}\n'
    else:
        mess = f'User: {data.get("username")}\n' \
               f'Current pp: {round(data.get("statistics").get("pp"))}\n' \
               f'Total play time: {round(data.get("statistics").get("play_time") / 3600)} hours\n' \
               f'Level: {data.get("statistics").get("level").get("current")}\n' \
               f'Global Ranking: {data.get("statistics").get("global_rank")}\n' \
               f'Best Scores: \n' \
               f'Too many maps'
    return mess


def check_valid_user(data):
    if 'error' in data:
        return False
    return True



def create_message_for_map(id):
    data = get_info_map(id)
    mess = f'{data.get("beatmapset").get("title")}' \
           f'{data.get("")}'



def picture(avatar, banner):
    ban = Image.open(BytesIO(urllib.request.urlopen(banner).read()))
    av = Image.open(BytesIO(urllib.request.urlopen(avatar).read()))
    ban.paste(av, (194, 122))
    ban.save('res.png')
    return open('res.png', 'rb')


if __name__ == '__main__':
    pprint(get_info_map('1486189'))