import telebot
import config
import data
import keyboards

# Инициализация бота
bot = telebot.TeleBot(config.load_token())

# ===== ОБРАБОТЧИКИ КОМАНД =====
@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        "👋 Привет, боец!\n\n"
        "Этот бот поможет тебе прокачать скилл в Counter-Strike.\n"
        "Выбирай карту, сторону и тип гранаты 👇",
        reply_markup=keyboards.get_main_menu(),
    )

@bot.message_handler(commands=["help"])
def help_command(message):
    bot.send_message(
        message.chat.id,
        "📖 <b>Список команд:</b>\n\n"
        "🔹 /start — главное меню\n"
        "🔹 /help — это сообщение\n\n"
        "💡 Или нажми кнопку ниже 👇",
        parse_mode="HTML",
        reply_markup=keyboards.get_help_menu(),
    )

# ===== ОБРАБОТЧИК НАЖАТИЙ НА КНОПКИ =====
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    data_callback = call.data

    if data_callback.startswith("map:"):
        map_id = data_callback.split(":")[1]
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=f"📍 Карта: <b>{data.MAPS[map_id]['name']}</b>\n\nВыбери сторону 👇",
            parse_mode="HTML",
            reply_markup=keyboards.get_side_menu(map_id),
        )

    elif data_callback.startswith("side:"):
        _, map_id, side_id = data_callback.split(":")
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=f"📍 <b>{data.MAPS[map_id]['name']}</b> | {data.SIDE_NAMES[side_id]}\n\nВыбери тип гранаты 👇",
            parse_mode="HTML",
            reply_markup=keyboards.get_grenade_menu(map_id, side_id),
        )

    elif data_callback.startswith("grenade:"):
        _, map_id, side_id, grenade_id = data_callback.split(":")
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=f"📍 <b>{data.MAPS[map_id]['name']}</b> | {data.SIDE_NAMES[side_id]} | {data.GRENADE_NAMES[grenade_id]}\n\nВыбери раскидку 👇",
            parse_mode="HTML",
            reply_markup=keyboards.get_videos_menu(map_id, side_id, grenade_id),
        )

    elif data_callback.startswith("video:"):
        _, map_id, side_id, grenade_id, index_str = data_callback.split(":")
        index = int(index_str)
        
        videos = data.MAPS[map_id]["sides"][side_id][grenade_id]
        video_name = list(videos.keys())[index]
        video_link = list(videos.values())[index]

        bot.send_message(
            call.message.chat.id,
            f"🎮 <b>{video_name}</b>\n\n🔗 Смотри тут: {video_link}",
            parse_mode="HTML",
        )
        bot.answer_callback_query(call.id, text="Ссылка отправлена! ✅")

    elif data_callback.startswith("back:"):
        parts = data_callback.split(":")
        back_type = parts[1]

        if back_type == "main":
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="👇 Выбери карту:",
                reply_markup=keyboards.get_main_menu(),
            )
        elif back_type == "map":
            map_id = parts[2]
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=f"📍 Карта: <b>{data.MAPS[map_id]['name']}</b>\n\nВыбери сторону 👇",
                parse_mode="HTML",
                reply_markup=keyboards.get_side_menu(map_id),
            )
        elif back_type == "side":
            map_id, side_id = parts[2], parts[3]
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=f"📍 <b>{data.MAPS[map_id]['name']}</b> | {data.SIDE_NAMES[side_id]}\n\nВыбери тип гранаты 👇",
                parse_mode="HTML",
                reply_markup=keyboards.get_grenade_menu(map_id, side_id),
            )

# ===== ОБРАБОТЧИК ЛЮБЫХ СООБЩЕНИЙ =====
@bot.message_handler(func=lambda message: True)
def handle_any_message(message):
    bot.send_message(
        message.chat.id,
        "🤔 Я не понимаю это сообщение.\n\n"
        "Используй /start или /help, либо выбери карту ниже 👇",
        parse_mode="HTML",
        reply_markup=keyboards.get_main_menu(),
    )

# ===== ЗАПУСК =====
if __name__ == "__main__":
    print("🤖 CS Bot запущен! Жду игроков...")
    bot.infinity_polling()