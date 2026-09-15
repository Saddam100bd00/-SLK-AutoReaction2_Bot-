import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import time
import random
import threading
import json
import os
from keep_alive import keep_alive

# ================= কনফিগারেশন =================
MAIN_BOT_TOKEN = "8500215028:AAG8NNnRgccMe1p1NhQq96SpBF5Hd69x7ko" 
OWNER_USERNAME = "Premium_buy_admin"
# অ্যাডমিনদের লিস্ট (এখানে আপনার একাধিক অ্যাডমিন আইডি দিতে পারবেন কমা দিয়ে)
ADMINS = [8701368956] 

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

# ================= ডাটাবেস (Advanced JSON) =================
DB_FILE = 'database.json'
def load_data():
    default_db = {
        "users": [], "fsub_channels": [], "video_link": "https://youtube.com", 
        "links": {"channel": "https://t.me/yourchannel", "chat": "https://t.me/yourgroup", "owner": f"https://t.me/{OWNER_USERNAME}", "youtube": "https://youtube.com"},
        "settings": {
            "maintenance": False,
            "emergency_stop": False,
            "min_delay": 1.0,
            "max_delay": 5.0,
            "welcome_text": f"Hey {{name}} 😻\n\n😘 Welcome, I am @{{bot_username}}\n━━━━━━━━•❅•°•❈•°•❅•━━━━━━━━\n😊 Add me and all my team bots to your channel or group And Make Admin...\n\n🤖 Coder: @{OWNER_USERNAME}"
        },
        "stats": {"total_reactions": 0, "failed_reactions": 0}
    }
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, 'r') as f:
                data = json.load(f)
                # Update missing keys automatically
                for key in default_db:
                    if key not in data: data[key] = default_db[key]
                return data
        except: pass
    return default_db

def save_data(data):
    with open(DB_FILE, 'w') as f: json.dump(data, f)

db = load_data()

# ================= রিয়েকশন লজিক (আপডেটেড) =================
react_clients = [telebot.TeleBot(bot['token']) for bot in REACTION_BOTS_DATA]
processed_messages = set()

def perform_reactions(chat_id, message_id):
    if db["settings"]["emergency_stop"]: return # Emergency Stop ON থাকলে রিয়েক্ট করবে না
    
    emojis = ['❤️', '🥰', '😍', '😘', '👍']
    min_d, max_d = db["settings"]["min_delay"], db["settings"]["max_delay"]
    
    for client in react_clients:
        if db["settings"]["emergency_stop"]: break
        time.sleep(random.uniform(min_d, max_d))
        try:
            client.set_message_reaction(chat_id, message_id, [telebot.types.ReactionTypeEmoji(random.choice(emojis))], is_big=False)
            db["stats"]["total_reactions"] += 1
        except Exception:
            db["stats"]["failed_reactions"] += 1
    save_data(db)

@main_bot.message_handler(func=lambda m: m.chat.type in ['group', 'supergroup'])
@main_bot.channel_post_handler(func=lambda m: True)
def listen_and_trigger(message):
    if db["settings"]["emergency_stop"] or db["settings"]["maintenance"]: return
    msg_id = f"{message.chat.id}_{message.message_id}"
    if msg_id not in processed_messages:
        processed_messages.add(msg_id)
        if len(processed_messages) > 2000: processed_messages.clear()
        threading.Thread(target=perform_reactions, args=(message.chat.id, message.message_id)).start()

# ================= ফোরস সাব লজিক =================
def check_fsub(user_id):
    if not db["fsub_channels"]: return True, []
    not_joined = []
    for ch in db["fsub_channels"]:
        try:
            stat = main_bot.get_chat_member(ch, user_id).status
            if stat in ['left', 'kicked']: not_joined.append(ch)
        except: not_joined.append(ch)
    return len(not_joined) == 0, not_joined

# ================= /start কমান্ড =================
@main_bot.message_handler(commands=['start'])
def start_cmd(message):
    if message.chat.type != 'private': return
    user_id = message.from_user.id
    
    # Maintenance Check
    if db["settings"]["maintenance"] and user_id not in ADMINS:
        main_bot.send_message(message.chat.id, "🛠️ **Bot is under maintenance. Please try again later.**", parse_mode="Markdown")
        return

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
    text = db["settings"]["welcome_text"].replace("{name}", name).replace("{bot_username}", bot_info.username)
    
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("🤖 Channel React Bot", callback_data="ch_react"),
        InlineKeyboardButton("🤖 Group React Bot", callback_data="gr_react"),
        InlineKeyboardButton("❓ HOW TO USE ❓", callback_data="how_use"),
        InlineKeyboardButton("📞 Support", callback_data="support")
    )
    
    # স্পেশাল অ্যাডমিন বাটন (শুধুমাত্র অ্যাডমিনদের জন্য)
    if user_id in ADMINS:
        markup.add(InlineKeyboardButton("👑 Admin Panel", callback_data="open_admin_panel"))
    
    try:
        photos = main_bot.get_user_profile_photos(user_id, limit=1)
        if photos.total_count > 0:
            main_bot.send_photo(chat_id, photos.photos[0][0].file_id, caption=text, reply_markup=markup)
        else:
            main_bot.send_message(chat_id, text, reply_markup=markup)
    except:
        main_bot.send_message(chat_id, text, reply_markup=markup)

# ================= অ্যাডমিন প্যানেল UI =================
def admin_dashboard_markup():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("📊 Dashboard", callback_data="adm_dash"),
        InlineKeyboardButton("👥 Users & Broadcast", callback_data="adm_users"),
        InlineKeyboardButton("🔐 Force Subscribe", callback_data="adm_fsub"),
        InlineKeyboardButton("⏱️ Delay Settings", callback_data="adm_delay"),
        InlineKeyboardButton("⚙️ Bot Settings", callback_data="adm_settings"),
        InlineKeyboardButton("🚨 Emergency Stop", callback_data="adm_estop"),
        InlineKeyboardButton("🔧 Maintenance Mode", callback_data="adm_maint"),
        InlineKeyboardButton("❌ Close Panel", callback_data="close_panel")
    )
    return markup

@main_bot.message_handler(commands=['admin'])
def admin_command(message):
    if message.from_user.id in ADMINS:
        main_bot.send_message(message.chat.id, "👑 **Welcome to Ultimate Admin Panel**\nSelect an option below:", reply_markup=admin_dashboard_markup(), parse_mode="Markdown")

# ================= কলব্যাক লজিক (ইউজার + অ্যাডমিন) =================
@main_bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    uid = call.from_user.id
    cid = call.message.chat.id
    mid = call.message.message_id
    
    # ------------------ সাধারণ ইউজার কলব্যাক ------------------
    if call.data == "verify_fsub":
        is_joined, _ = check_fsub(uid)
        if is_joined:
            main_bot.delete_message(cid, mid)
            send_welcome(cid, call.from_user.first_name, uid)
        else:
            main_bot.answer_callback_query(call.id, "You haven't joined all channels yet!", show_alert=True)
            
    elif call.data in ["ch_react", "gr_react"]:
        is_channel = call.data == "ch_react"
        text = f"This Is For {'Channel' if is_channel else 'Group'} Reaction Bot Usernames\n━━━━━━━━•❅•°•❈•°•❅•━━━━━━━━\n"
        for i, b in enumerate(REACTION_BOTS_DATA, 1): text += f"{i}. @{b['user']}\n"
        text += f"━━━━━━━━•❅•°•❈•°•❅•━━━━━━━━\n✅ Add all bots to your {'channel' if is_channel else 'group'} and make admin 🔰"
        
        markup = InlineKeyboardMarkup(row_width=4)
        buttons = [InlineKeyboardButton(f"Add({i})", url=f"https://t.me/{b['user']}?{'startchannel' if is_channel else 'startgroup'}=start") for i, b in enumerate(REACTION_BOTS_DATA, 1)]
        markup.add(*buttons)
        markup.add(InlineKeyboardButton("🔙 Back", callback_data="back_home"))
        main_bot.edit_message_caption(caption=text, chat_id=cid, message_id=mid, reply_markup=markup) if call.message.content_type == 'photo' else main_bot.edit_message_text(text=text, chat_id=cid, message_id=mid, reply_markup=markup)

    elif call.data == "how_use":
        text = f"❓HOW TO USE❓\n1. Add the Bot to Your Channel or Group...\nDeveloper: @{OWNER_USERNAME}"
        markup = InlineKeyboardMarkup().add(InlineKeyboardButton("📹 Watch Video Tutorial", url=db["video_link"]), InlineKeyboardButton("🔙 Back", callback_data="back_home"))
        main_bot.edit_message_caption(caption=text, chat_id=cid, message_id=mid, reply_markup=markup) if call.message.content_type == 'photo' else main_bot.edit_message_text(text=text, chat_id=cid, message_id=mid, reply_markup=markup)

    elif call.data == "support":
        text = "📞Support :\nFollow Our All Channel To Get All Notice And Update"
        markup = InlineKeyboardMarkup(row_width=2).add(
            InlineKeyboardButton("Official Channel", url=db["links"]["channel"]),
            InlineKeyboardButton("Support Chat", url=db["links"]["chat"]),
            InlineKeyboardButton("Owner", url=db["links"]["owner"]),
            InlineKeyboardButton("YouTube Channel", url=db["links"]["youtube"]),
            InlineKeyboardButton("🔙 Back", callback_data="back_home")
        )
        main_bot.edit_message_caption(caption=text, chat_id=cid, message_id=mid, reply_markup=markup) if call.message.content_type == 'photo' else main_bot.edit_message_text(text=text, chat_id=cid, message_id=mid, reply_markup=markup)

    elif call.data == "back_home":
        main_bot.delete_message(cid, mid)
        send_welcome(cid, call.from_user.first_name, uid)

    # ------------------ অ্যাডমিন কলব্যাক ------------------
    elif call.data == "open_admin_panel":
        if uid in ADMINS:
            main_bot.send_message(cid, "👑 **Welcome to Ultimate Admin Panel**", reply_markup=admin_dashboard_markup(), parse_mode="Markdown")
            
    elif call.data == "adm_dash":
        if uid not in ADMINS: return
        t_users = len(db["users"])
        t_reac = db["stats"]["total_reactions"]
        f_reac = db["stats"]["failed_reactions"]
        text = f"📊 **Dashboard Statistics**\n\n👥 Total Users: {t_users}\n🎯 Successful Reactions: {t_reac}\n❌ Failed Reactions: {f_reac}\n🤖 Total Sub-Bots: 20\n\n🔧 Maintenance: {'ON 🔴' if db['settings']['maintenance'] else 'OFF 🟢'}\n🚨 Emergency Stop: {'ON 🔴' if db['settings']['emergency_stop'] else 'OFF 🟢'}"
        markup = InlineKeyboardMarkup().add(InlineKeyboardButton("🔙 Back to Panel", callback_data="back_admin"))
        main_bot.edit_message_text(text, cid, mid, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "adm_users":
        if uid not in ADMINS: return
        text = "👥 **User Management & Broadcast**\n\nTo broadcast, just type:\n`/broadcast Your Message`"
        markup = InlineKeyboardMarkup().add(InlineKeyboardButton("🔙 Back to Panel", callback_data="back_admin"))
        main_bot.edit_message_text(text, cid, mid, reply_markup=markup, parse_mode="Markdown")
        
    elif call.data == "adm_fsub":
        if uid not in ADMINS: return
        channels = "\n".join(db["fsub_channels"]) if db["fsub_channels"] else "No channels added."
        text = f"🔐 **Force Sub Channels:**\n{channels}\n\nCommands:\n`/addfsub @username`\n`/delfsub @username`"
        markup = InlineKeyboardMarkup().add(InlineKeyboardButton("🔙 Back to Panel", callback_data="back_admin"))
        main_bot.edit_message_text(text, cid, mid, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "adm_delay":
        if uid not in ADMINS: return
        min_d, max_d = db["settings"]["min_delay"], db["settings"]["max_delay"]
        text = f"⏱️ **Delay Settings**\n\nCurrent Minimum: {min_d}s\nCurrent Maximum: {max_d}s\n\nUse command to change:\n`/setdelay 1.5 4.0`"
        markup = InlineKeyboardMarkup().add(InlineKeyboardButton("🔙 Back to Panel", callback_data="back_admin"))
        main_bot.edit_message_text(text, cid, mid, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "adm_estop":
        if uid not in ADMINS: return
        db["settings"]["emergency_stop"] = not db["settings"]["emergency_stop"]
        save_data(db)
        stat = "ON 🔴" if db["settings"]["emergency_stop"] else "OFF 🟢"
        main_bot.answer_callback_query(call.id, f"Emergency Stop is now {stat}", show_alert=True)
        main_bot.edit_message_reply_markup(cid, mid, reply_markup=admin_dashboard_markup())

    elif call.data == "adm_maint":
        if uid not in ADMINS: return
        db["settings"]["maintenance"] = not db["settings"]["maintenance"]
        save_data(db)
        stat = "ON 🔴" if db["settings"]["maintenance"] else "OFF 🟢"
        main_bot.answer_callback_query(call.id, f"Maintenance is now {stat}", show_alert=True)
        main_bot.edit_message_reply_markup(cid, mid, reply_markup=admin_dashboard_markup())

    elif call.data == "adm_settings":
        if uid not in ADMINS: return
        text = "⚙️ **Bot Settings Commands**\n\n`/setvideo [Link]` - Update Tutorial\n`/setwelcome [Text]` - Update Welcome Message"
        markup = InlineKeyboardMarkup().add(InlineKeyboardButton("🔙 Back to Panel", callback_data="back_admin"))
        main_bot.edit_message_text(text, cid, mid, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "back_admin":
        if uid not in ADMINS: return
        main_bot.edit_message_text("👑 **Welcome to Ultimate Admin Panel**\nSelect an option below:", cid, mid, reply_markup=admin_dashboard_markup(), parse_mode="Markdown")

    elif call.data == "close_panel":
        main_bot.delete_message(cid, mid)

# ================= অ্যাডমিন কমান্ডস =================
@main_bot.message_handler(commands=['addfsub', 'delfsub', 'setvideo', 'setdelay', 'broadcast'])
def admin_commands_text(message):
    if message.from_user.id not in ADMINS: return
    cmd = message.text.split()[0]
    args = message.text.split()[1:]
    
    if cmd == '/addfsub' and args:
        ch = args[0]
        if len(db["fsub_channels"]) < 6:
            if ch not in db["fsub_channels"]:
                db["fsub_channels"].append(ch)
                save_data(db)
                main_bot.reply_to(message, f"✅ Added {ch} to FSub.")
        else: main_bot.reply_to(message, "❌ Maximum 6 channels allowed!")
        
    elif cmd == '/delfsub' and args:
        ch = args[0]
        if ch in db["fsub_channels"]:
            db["fsub_channels"].remove(ch)
            save_data(db)
            main_bot.reply_to(message, f"✅ Removed {ch} from FSub.")
            
    elif cmd == '/setvideo' and args:
        db["video_link"] = args[0]
        save_data(db)
        main_bot.reply_to(message, "✅ Video link updated!")

    elif cmd == '/setdelay' and len(args) == 2:
        try:
            db["settings"]["min_delay"] = float(args[0])
            db["settings"]["max_delay"] = float(args[1])
            save_data(db)
            main_bot.reply_to(message, f"✅ Delay updated! Min: {args[0]}s, Max: {args[1]}s")
        except:
            main_bot.reply_to(message, "❌ Use valid numbers. Example: `/setdelay 1 3`")
        
    elif cmd == '/broadcast' and args:
        msg = message.text.replace('/broadcast ', '')
        sent, failed = 0, 0
        main_bot.reply_to(message, "⏳ Broadcasting...")
        for uid in db["users"]:
            try:
                main_bot.send_message(uid, msg)
                sent += 1
            except: failed += 1
        main_bot.reply_to(message, f"✅ Broadcast complete!\nSent: {sent}\nFailed: {failed}")

# ================= বট রান করানো =================
keep_alive() # Server alive for Render

print("Ultimate Mega Bot is successfully running...")
main_bot.infinity_polling(timeout=10, long_polling_timeout=5)
