import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import time
import random
import threading
import json
import os
from keep_alive import keep_alive

# ================= কনফিগারেশন =================
# এখানে আপনার মেইন বটের টোকেন এবং আপনার (Admin) ইউজারনেম দিন
MAIN_BOT_TOKEN = "8500215028:AAG8NNnRgccMe1p1NhQq96SpBF5Hd69x7ko" 
OWNER_USERNAME = "t.me/Premium_buy_admin" # (যেমন: @Programmer)
ADMIN_ID = 8701368956 # আপনার টেলিগ্রাম ইউজার আইডি দিন (সংখ্যায়)

main_bot = telebot.TeleBot(MAIN_BOT_TOKEN)

# ২০টি বটের ডাটা
REACTION_BOTS_DATA = [
    {"user": "slk_autoreaction_Bot", "token": "8500215028:AAG8NNnRgccMe1p1NhQq96SpBF5Hd69x7ko"},
    {"user": "slk_autoreaction2_Bot", "token": "8959375749:AAHb8TQNGvk17xS4TMxv7LM1g_d8a2XnYek"},
    {"user": "slk_autoreaction3_Bot", "token": "8584547169:AAEL1EA6I48cQWfHHzfnWP8IoVla95bswwo"},
    {"user": "slk_autoreaction4_Bot", "token": "8818511746:AAEEC0xRjXt0OTJszhOUyoo7D7uEa8mlAew"},
    {"user": "slk_autoreaction5_Bot", "token": "8945621367:AAGguZNu4kaLrzpWO9GwGWpkzAB7RGh6XKQ"},
    {"user": "slk_autoreaction6_Bot", "token": "8939047300:AAG6Yc5urFj_bASr-HTPDWUgsyZQ7bHVLvk"},
    {"user": "slk_autoreaction7_Bot", "token": "8733782411:AAHzURizHTCwCkNcfoqQ9Mrn8H5sdIvvg8c"},
    {"user": "slk_autoreaction8_Bot", "token": "8662586985:AAHFeyOT4DcxSlq5e3Kz5TGGGeQLP214zwU"},
    {"user": "slk_autoreaction9_Bot", "token": "8884151841:AAGtr6ImOX1WejxjR7A4TRuDw3oNc9Mmejc"},
    {"user": "slk_autoreaction10_Bot", "token": "8910272074:AAHrQ0L2CPO-fPPoIZutesqew-7bVtPb3Vk"},
    {"user": "slk_autoreaction11_Bot", "token": "8900151490:AAHQB-bLBQybZZX67H4z1SVYsgzO5zVE7Gw"},
    {"user": "slk_autoreaction12_Bot", "token": "8895889976:AAGpDr5B5OS28WGoUvzooqz2_taan7ZUXGU"},
    {"user": "slk_autoreaction13_Bot", "token": "8649892066:AAEThE3SLoGwYK5HG9jyFOaN4OWs0tHHLVs"},
    {"user": "slk_autoreaction14_Bot", "token": "8631587810:AAFgveAvP86f4Dwl951spMGUp7X7Tg6XdSg"},
    {"user": "slk_autoreaction15_Bot", "token": "8828024191:AAE2_1YU2iKd3CAz27P9cVA_LpSxQsTiXFc"},
    {"user": "slk_autoreaction16_Bot", "token": "8883085350:AAGTjYOUq5HGseILy5T4CQwQSaJi4PN_7RI"},
    {"user": "slk_autoreaction17_Bot", "token": "8746045439:AAFKHIdwqlu1Qg3JHocnhueMsbXYj7qsM7s"},
    {"user": "slk_autoreaction18_Bot", "token": "8876454463:AAEWkjTVWqy3-I7iuzvzH1VhCAeQprqx87w"},
    {"user": "slk_autoreaction19_Bot", "token": "8327590148:AAGJHgLperQcbKXLmY4ID9WiHGohIU5UPnQ"},
    {"user": "slk_autoreaction20_Bot", "token": "8888836700:AAFFQL_9f0ZH8QADcWAMjw5tUjuM3hfqVog"}
]

# ডাটাবেস (JSON File)
DB_FILE = 'database.json'
def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r') as f: return json.load(f)
    return {"users": [], "fsub_channels": [], "video_link": "https://youtube.com", 
            "links": {"channel": "https://t.me/yourchannel", "chat": "https://t.me/yourgroup", "owner": f"https://t.me/{OWNER_USERNAME.replace('@','')}", "youtube": "https://youtube.com"}}

def save_data(data):
    with open(DB_FILE, 'w') as f: json.dump(data, f)

db = load_data()

# ================= রিয়েকশন লজিক (১-৫ সেকেন্ড পর পর) =================
react_clients = [telebot.TeleBot(bot['token']) for bot in REACTION_BOTS_DATA]
processed_messages = set()

def perform_reactions(chat_id, message_id):
    emojis = ['❤️', '🥰', '😍', '😘', '👍']
    for client in react_clients:
        time.sleep(random.uniform(1.0, 5.0)) # ১ থেকে ৫ সেকেন্ড গ্যাপ
        try:
            client.set_message_reaction(chat_id, message_id, [telebot.types.ReactionTypeEmoji(random.choice(emojis))], is_big=False)
        except:
            pass # গ্রুপে এড না থাকলে ইগনোর করবে

# যেকোনো একটি বটকে মেসেজ লিসেনার হিসেবে সেট করা হলো, মেসেজ এলে টাস্ক শুরু হবে
@react_clients[0].message_handler(func=lambda m: True)
@react_clients[0].channel_post_handler(func=lambda m: True)
def listen_and_trigger(message):
    msg_id = f"{message.chat.id}_{message.message_id}"
    if msg_id not in processed_messages:
        processed_messages.add(msg_id)
        if len(processed_messages) > 5000: processed_messages.clear()
        threading.Thread(target=perform_reactions, args=(message.chat.id, message.message_id)).start()

# ================= মেইন বট লজিক =================

def check_fsub(user_id):
    if not db["fsub_channels"]: return True, []
    not_joined = []
    for ch in db["fsub_channels"]:
        try:
            stat = main_bot.get_chat_member(ch, user_id).status
            if stat in ['left', 'kicked']: not_joined.append(ch)
        except: not_joined.append(ch)
    return len(not_joined) == 0, not_joined

@main_bot.message_handler(commands=['start'])
def start_cmd(message):
    user_id = message.from_user.id
    if user_id not in db["users"]:
        db["users"].append(user_id)
        save_data(db)
        
    is_joined, missing = check_fsub(user_id)
    if not is_joined:
        markup = InlineKeyboardMarkup()
        for ch in missing:
            markup.add(InlineKeyboardButton(text="Join Channel", url=f"https://t.me/{ch.replace('@','')}"))
        markup.add(InlineKeyboardButton(text="✅ Verify", callback_data="verify_fsub"))
        main_bot.send_message(message.chat.id, "⚠️ **To use this bot, you must join our channels!**", reply_markup=markup, parse_mode="Markdown")
        return

    send_welcome(message.chat.id, message.from_user.first_name, user_id)

def send_welcome(chat_id, name, user_id):
    bot_info = main_bot.get_me()
    text = f"""Hey {name} 😻\n\n😘 Welcome, I am @{bot_info.username}\n━━━━━━━━•❅•°•❈•°•❅•━━━━━━━━\n😊 Add me and all my team bots to your channel or group And Make Admin, then I will automatically react to all posts and messages in your channel or group\n\n🤖 Coder: {OWNER_USERNAME}"""
    
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("🤖 Channel React Bot", callback_data="ch_react"),
        InlineKeyboardButton("🤖 Group React Bot", callback_data="gr_react"),
        InlineKeyboardButton("❓ HOW TO USE ❓", callback_data="how_use"),
        InlineKeyboardButton("📞 Support", callback_data="support")
    )
    
    # প্রোফাইল পিকচার আনার চেষ্টা
    try:
        photos = main_bot.get_user_profile_photos(user_id, limit=1)
        if photos.total_count > 0:
            main_bot.send_photo(chat_id, photos.photos[0][0].file_id, caption=text, reply_markup=markup)
        else:
            main_bot.send_message(chat_id, text, reply_markup=markup)
    except:
        main_bot.send_message(chat_id, text, reply_markup=markup)

@main_bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "verify_fsub":
        is_joined, _ = check_fsub(call.from_user.id)
        if is_joined:
            main_bot.delete_message(call.message.chat.id, call.message.message_id)
            send_welcome(call.message.chat.id, call.from_user.first_name, call.from_user.id)
        else:
            main_bot.answer_callback_query(call.id, "You haven't joined all channels yet!", show_alert=True)
            
    elif call.data in ["ch_react", "gr_react"]:
        is_channel = call.data == "ch_react"
        text = f"This Is For {'Channel' if is_channel else 'Group'} Reaction Bot Usernames\n━━━━━━━━•❅•°•❈•°•❅•━━━━━━━━\n"
        for i, b in enumerate(REACTION_BOTS_DATA, 1): text += f"{i}. @{b['user']}\n"
        text += f"━━━━━━━━•❅•°•❈•°•❅•━━━━━━━━\n✅ Add all bots to your {'channel' if is_channel else 'group'} and make admin 🔰\nThen they will automatically react to all the posts of your {'Channel' if is_channel else 'Group'} 📣"
        
        markup = InlineKeyboardMarkup(row_width=4)
        buttons = []
        param = "startchannel=start" if is_channel else "startgroup=start"
        for i, b in enumerate(REACTION_BOTS_DATA, 1):
            url = f"https://t.me/{b['user']}?{param}"
            buttons.append(InlineKeyboardButton(f"Add({i})", url=url))
        markup.add(*buttons)
        markup.add(InlineKeyboardButton("🔙 Back", callback_data="back_home"))
        
        main_bot.edit_message_caption(caption=text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup) if call.message.photo else main_bot.edit_message_text(text=text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)

    elif call.data == "how_use":
        text = f"❓HOW TO USE❓\n1. Add the Bot to Your Channel or Group:\n- Add the reaction bot to your Telegram channel or group.\n- Grant admin privileges to ensure it operates smoothly.\n2. Enable Reactions:\n- Ensure that the following emojis are enabled: ❤️, 🥰, 😍, 😘, 👍\n3. Automated Reaction Process:\n- The bot will automatically apply one of these emojis to each message.\n4. Support and Assistance:\n- Contact the bot developer {OWNER_USERNAME}"
        markup = InlineKeyboardMarkup().add(InlineKeyboardButton("📹 Watch Video Tutorial", url=db["video_link"]), InlineKeyboardButton("🔙 Back", callback_data="back_home"))
        main_bot.edit_message_caption(caption=text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup) if call.message.photo else main_bot.edit_message_text(text=text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)

    elif call.data == "support":
        text = "📞Support :\nFollow Our All Channel To Get All Notice And Update\n\nIf You Face Any Problem, Contact The Owner Directly -"
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("Official Channel", url=db["links"]["channel"]),
            InlineKeyboardButton("Support Chat", url=db["links"]["chat"]),
            InlineKeyboardButton("Owner", url=db["links"]["owner"]),
            InlineKeyboardButton("YouTube Channel", url=db["links"]["youtube"]),
            InlineKeyboardButton("🔙 Back", callback_data="back_home")
        )
        main_bot.edit_message_caption(caption=text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup) if call.message.photo else main_bot.edit_message_text(text=text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)

    elif call.data == "back_home":
        main_bot.delete_message(call.message.chat.id, call.message.message_id)
        send_welcome(call.message.chat.id, call.from_user.first_name, call.from_user.id)

# ================= এডমিন প্যানেল =================
@main_bot.message_handler(commands=['admin'])
def admin_panel(message):
    if message.from_user.id == ADMIN_ID:
        text = "👑 **Admin Panel**\n\nCommands:\n/addfsub @channel_username (Max 6)\n/delfsub @channel_username\n/setvideo [Link]\n/broadcast [Message]\n/stats"
        main_bot.reply_to(message, text, parse_mode="Markdown")

@main_bot.message_handler(commands=['addfsub', 'delfsub', 'stats', 'setvideo', 'broadcast'])
def admin_commands(message):
    if message.from_user.id != ADMIN_ID: return
    cmd = message.text.split()[0]
    
    if cmd == '/addfsub':
        ch = message.text.split()[1]
        if len(db["fsub_channels"]) < 6:
            db["fsub_channels"].append(ch)
            save_data(db)
            main_bot.reply_to(message, f"Added {ch} to FSub.")
        else: main_bot.reply_to(message, "Maximum 6 channels allowed!")
        
    elif cmd == '/delfsub':
        ch = message.text.split()[1]
        if ch in db["fsub_channels"]:
            db["fsub_channels"].remove(ch)
            save_data(db)
            main_bot.reply_to(message, f"Removed {ch} from FSub.")
            
    elif cmd == '/stats':
        main_bot.reply_to(message, f"📊 Total Users: {len(db['users'])}")
        
    elif cmd == '/setvideo':
        db["video_link"] = message.text.split()[1]
        save_data(db)
        main_bot.reply_to(message, "Video link updated!")
        
    elif cmd == '/broadcast':
        msg = message.text.replace('/broadcast ', '')
        sent = 0
        for uid in db["users"]:
            try:
                main_bot.send_message(uid, msg)
                sent += 1
            except: pass
        main_bot.reply_to(message, f"Broadcast complete. Sent to {sent} users.")

# ================= বট রান করানো =================
keep_alive() # Server alive for Render

def run_reaction_bot(client):
    client.polling(none_stop=True, skip_pending=True)

print("Starting bots...")
# রিয়েকশন লিসেনার (১ম বট) থ্রেডে রান করানো
threading.Thread(target=run_reaction_bot, args=(react_clients[0],)).start()

# মেইন বট রান করানো
main_bot.polling(none_stop=True)
