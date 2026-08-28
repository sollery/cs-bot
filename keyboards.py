from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import data

def get_main_menu():
    markup = InlineKeyboardMarkup(row_width=1)
    for map_id, map_data in data.MAPS.items():
        markup.add(InlineKeyboardButton(text=map_data["name"], callback_data=f"map:{map_id}"))
    return markup

def get_side_menu(map_id):
    markup = InlineKeyboardMarkup(row_width=1)
    for side_id in data.MAPS[map_id]["sides"].keys():
        markup.add(InlineKeyboardButton(text=data.SIDE_NAMES[side_id], callback_data=f"side:{map_id}:{side_id}"))
    markup.add(InlineKeyboardButton(text="🔙 Назад к картам", callback_data="back:main"))
    return markup

def get_grenade_menu(map_id, side_id):
    markup = InlineKeyboardMarkup(row_width=1)
    available_grenades = data.MAPS[map_id]["sides"][side_id].keys()
    
    for grenade_id in available_grenades:
        markup.add(InlineKeyboardButton(
            text=data.GRENADE_NAMES[grenade_id], 
            callback_data=f"grenade:{map_id}:{side_id}:{grenade_id}"
        ))
    markup.add(InlineKeyboardButton(text="🔙 Назад к выбору стороны", callback_data=f"back:map:{map_id}"))
    return markup

def get_videos_menu(map_id, side_id, grenade_id):
    markup = InlineKeyboardMarkup(row_width=1)
    videos = data.MAPS[map_id]["sides"][side_id][grenade_id]

    for index, video_name in enumerate(videos):
        markup.add(InlineKeyboardButton(
            text=f"🎬 {video_name}", 
            callback_data=f"video:{map_id}:{side_id}:{grenade_id}:{index}"
        ))
    markup.add(InlineKeyboardButton(text="🔙 Назад к типам гранат", callback_data=f"back:side:{map_id}:{side_id}"))
    return markup

def get_help_menu():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton(text="🎮 Открыть меню раскидок", callback_data="back:main"))
    return markup