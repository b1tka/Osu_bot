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


def get_info(username):
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


def picture(avatar, banner):
    ban = Image.open(BytesIO(urllib.request.urlopen(banner).read()))
    av = Image.open(BytesIO(urllib.request.urlopen(avatar).read()))
    ban.paste(av, (194, 122))
    ban.save('res.png')
    return open('res.png', 'rb')


if __name__ == '__main__':
    pprint(get_info_map('1483372'))