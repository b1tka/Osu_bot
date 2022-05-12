from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


button_user = KeyboardButton('/Search_user')
button_map = KeyboardButton('/Random_map')
button_search_map = KeyboardButton('/Search_map_by_id')
button_return = KeyboardButton('/Back')
button_show_maps = KeyboardButton('/show_maps')

kb = ReplyKeyboardMarkup()
bc = ReplyKeyboardMarkup()
kb.add(button_user, button_search_map, button_map)
bc.add(button_return)
