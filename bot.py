import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
import time
import random
import threading
import json
import os
from keep_alive import keep_alive

# ================= কনফিগারেশন =================
MAIN_BOT_TOKEN = "8500215028:AAG8NNnRgccMe1p1NhQq96SpBF5Hd69x7ko" 
OWNER_USERNAME = "Premium_buy_admin"
OWNER_ID = 8701368956  # মেইন ওনার আইডি (একে রিমুভ করা যাবে না)

main_bot = telebot.TeleBot(MAIN_BOT_TOKEN)

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

# ================= ডাটাবেস লজিক (Ultimate DB) =================
DB_FILE = 'database.json'
def load_data():
    default_db = {
        "users": [], "banned_users": [], "admins": [OWNER_ID], "fsub_channels": [],
        "video_link": "https://youtube.com",
        "links": {"channel": "https://t.me/yourchannel", "chat": "https://t.me/yourgroup", "owner": f"https://t.me/{OWNER_USERNAME}", "youtube": "https://youtube.com"},
        "settings": {
            "maintenance": False, "emergency_stop": False, "reaction_enabled": True,
            "min_delay": 1.0, "max_delay": 5.0, "random_order": True,
            "emojis": ['❤️', '🥰', '😍', '😘', '👍'],
            "welcome_text": f"Hey {{name}} 😻\n\n😘 Welcome, I am @{{bot_username}}\n━━━━━━━━•❅•°•❈•°•❅•━━━━━━━━\n😊 Add me and all my team bots to your channel or group And Make Admin, then I will automatically react to all posts and messages in your channel or group\n\n🤖 Coder: @{OWNER_USERNAME}"
        },
        "stats": {"total_reacs": 0, "success": 0, "failed": 0},
        "logs": []
    }
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, 'r') as f:
                data = json.load(f)
                for key in default_db:
                    if key not in data: data[key] = default_db[key]
                    elif isinstance(default_db[key], dict):
                        for sub_key in default_db[key]:
                            if sub_key not in data[key]: data[key][sub_key] = default_db[key][sub_key]
                return data
        except: pass
    return default_db

def save_data(data):
    with open(DB_FILE, 'w') as f: json.dump(data, f)

db = load_data()

def is_admin(user_id):
    return user_id in db["admins"]

def log_activity(msg):
    db["logs"].append(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}")
    if len(db["logs"]) > 50: db["logs"].pop(0)
    save_data(db)

# ================= রিয়েকশন লজিক =================
react_clients = [telebot.TeleBot(bot['token']) for bot in REACTION_BOTS_DATA]
processed_messages = set()

def perform_reactions(chat_id, message_id):
    if db["settings"]["emergency_stop"] or not db["settings"]["reaction_enabled"]: return 
    
    emojis = db["settings"]["emojis"]
    min_d, max_d = db["settings"]["min_delay"], db["settings"]["max_delay"]
    
    bots_to_use = list(react_clients)
    if db["settings"]["random_order"]: random.shuffle(bots_to_use)
    
    for client in bots_to_use:
        if db["settings"]["emergency_stop"]: break
        time.sleep(random.uniform(min_d, max_d))
        try:
            client.set_message_reaction(chat_id, message_id, [telebot.types.ReactionTypeEmoji(random.choice(emojis))], is_big=False)
            db["stats"]["success"] += 1
            db["stats"]["total_reacs"] += 1
        except Exception:
            db["stats"]["failed"] += 1
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

# ================= ফোরস সাব লজিক (Fixed) =================
def check_fsub(user_id):
    if not db["fsub_channels"]: return True, []
    not_joined = []
    for ch in db["fsub_channels"]:
        try:
            stat = main_bot.get_chat_member(ch, user_id).status
            # যদি ইউজার মেম্বার, অ্যাডমিন বা ওনার না হয়
            if stat not in ['member', 'administrator', 'creator', 'restricted']:
                not_joined.append(ch)
        except Exception as e:
            # বট যদি চ্যানেলে অ্যাডমিন না থাকে তবে এই এরর আসবে। 
            print(f"Error checking {ch}: {e}") 
            not_joined.append(ch)
    return len(not_joined) == 0, not_joined

# ================= Start ও Welcome =================
@main_bot.message_handler(commands=['start'])
def start_cmd(message):
    if message.chat.type != 'private': return
    user_id = message.from_user.id
    
    if user_id in db["banned_users"]: return

    if db["settings"]["maintenance"] and not is_admin(user_id):
        main_bot.send_message(message.chat.id, "🛠️ **Bot is under maintenance. Please try again later.**", parse_mode="Markdown")
        return

    if user_id not in db["users"]:
        db["users"].append(user_id)
        save_data(db)
        if db["settings"].get("notify_new_user", True):
            for ad_id in db["admins"]:
                try: main_bot.send_message(ad_id, f"🔔 **New User:** {message.from_user.first_name} (`{user_id}`)", parse_mode="Markdown")
                except: pass
        
    is_joined, missing = check_fsub(user_id)
    if not is_joined:
        markup = InlineKeyboardMarkup()
        for ch in missing:
            markup.add(InlineKeyboardButton(text="Join Channel", url=f"https://t.me/{ch.replace('@','')}"))
        markup.add(InlineKeyboardButton(text="✅ Verify", callback_data="verify_fsub"))
        main_bot.send_message(message.chat.id, "⚠️ **To use this bot, you must join our channels!**\n\n*(If you are the admin, make sure the main bot is added as an ADMIN in all FSub channels!)*", reply_markup=markup, parse_mode="Markdown")
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
    
    if is_admin(user_id):
        markup.add(InlineKeyboardButton("👑 Admin Panel", callback_data="open_admin_panel"))
    
    try:
        photos = main_bot.get_user_profile_photos(user_id, limit=1)
        if photos.total_count > 0:
            main_bot.send_photo(chat_id, photos.photos[0][0].file_id, caption=text, reply_markup=markup)
        else:
            main_bot.send_message(chat_id, text, reply_markup=markup)
    except:
        main_bot.send_message(chat_id, text, reply_markup=markup)

# ================= Ultimate Admin Panel UI =================
def admin_dashboard_markup():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("📊 Dashboard/Stats", callback_data="adm_dash"),
        InlineKeyboardButton("👥 User Management", callback_data="adm_users"),
        InlineKeyboardButton("🔐 Force Subscribe", callback_data="adm_fsub"),
        InlineKeyboardButton("🤖 Bot Settings", callback_data="adm_bots"),
        InlineKeyboardButton("⚙️ Reaction Settings", callback_data="adm_react"),
        InlineKeyboardButton("⏱️ Delay Settings", callback_data="adm_delay"),
        InlineKeyboardButton("📢 Broadcast", callback_data="adm_brd"),
        InlineKeyboardButton("📞 Support & Links", callback_data="adm_links"),
        InlineKeyboardButton("📋 Reaction Logs", callback_data="adm_logs"),
        InlineKeyboardButton("📡 Bot Status", callback_data="adm_status"),
        InlineKeyboardButton("🔧 Maintenance", callback_data="adm_maint"),
        InlineKeyboardButton("🚨 Emergency Stop", callback_data="adm_estop"),
        InlineKeyboardButton("💾 Database Manage", callback_data="adm_db"),
        InlineKeyboardButton("👑 Admin Manage", callback_data="adm_admin"),
        InlineKeyboardButton("❌ Close Panel", callback_data="close_panel")
    )
    return markup

@main_bot.message_handler(commands=['admin'])
def admin_command(message):
    if is_admin(message.from_user.id):
        main_bot.send_message(message.chat.id, "👑 **Welcome to Ultimate Admin Panel**\nSelect an option to manage your Mega Bot:", reply_markup=admin_dashboard_markup(), parse_mode="Markdown")

# ================= কলব্যাক লজিক (User + Admin) =================
@main_bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    uid = call.from_user.id
    cid = call.message.chat.id
    mid = call.message.message_id
    
    # ------------------ সাধারণ ইউজার ------------------
    if call.data == "verify_fsub":
        is_joined, missing = check_fsub(uid)
        if is_joined:
            main_bot.delete_message(cid, mid)
            send_welcome(cid, call.from_user.first_name, uid)
        else:
            main_bot.answer_callback_query(call.id, f"You haven't joined all channels! Remaining: {len(missing)}", show_alert=True)
            
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
        if is_admin(uid):
            main_bot.send_message(cid, "👑 **Ultimate Admin Panel**", reply_markup=admin_dashboard_markup(), parse_mode="Markdown")
            
    elif call.data == "adm_dash":
        if not is_admin(uid): return
        text = f"📊 **Dashboard & Statistics**\n\n👥 Total Users: {len(db['users'])}\n🚫 Banned Users: {len(db['banned_users'])}\n\n🎯 Success Reactions: {db['stats']['success']}\n❌ Failed Reactions: {db['stats']['failed']}\n🔄 Total Triggered: {db['stats']['total_reacs']}\n\n🔧 Maintenance: {'ON 🔴' if db['settings']['maintenance'] else 'OFF 🟢'}\n🚨 Emergency Stop: {'ON 🔴' if db['settings']['emergency_stop'] else 'OFF 🟢'}"
        main_bot.edit_message_text(text, cid, mid, reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton("🔙 Back", callback_data="back_admin")), parse_mode="Markdown")

    elif call.data == "adm_users":
        if not is_admin(uid): return
        text = "👥 **User Management**\nCommands:\n`/ban [User_ID]` - Ban user\n`/unban [User_ID]` - Unban user"
        main_bot.edit_message_text(text, cid, mid, reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton("🔙 Back", callback_data="back_admin")), parse_mode="Markdown")
        
    elif call.data == "adm_fsub":
        if not is_admin(uid): return
        channels = "\n".join(db["fsub_channels"]) if db["fsub_channels"] else "No channels added."
        text = f"🔐 **Force Subscribe (Max 6)**\n\nActive:\n{channels}\n\nCommands:\n`/addfsub @channel`\n`/delfsub @channel`"
        main_bot.edit_message_text(text, cid, mid, reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton("🔙 Back", callback_data="back_admin")), parse_mode="Markdown")

    elif call.data == "adm_react":
        if not is_admin(uid): return
        text = f"⚙️ **Reaction Settings**\n\nStatus: {'Enabled ✅' if db['settings']['reaction_enabled'] else 'Disabled ❌'}\nRandom Order: {'ON' if db['settings']['random_order'] else 'OFF'}\nEmojis: {', '.join(db['settings']['emojis'])}\n\nCommands:\n`/togglereact` - Enable/Disable\n`/togglerandom` - Bot order\n`/setemojis 👍,🔥,❤️`"
        main_bot.edit_message_text(text, cid, mid, reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton("🔙 Back", callback_data="back_admin")), parse_mode="Markdown")

    elif call.data == "adm_delay":
        if not is_admin(uid): return
        min_d, max_d = db["settings"]["min_delay"], db["settings"]["max_delay"]
        text = f"⏱️ **Reaction Delay Control**\nMin: {min_d}s | Max: {max_d}s\n\nCommand to change:\n`/setdelay 1 3`"
        main_bot.edit_message_text(text, cid, mid, reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton("🔙 Back", callback_data="back_admin")), parse_mode="Markdown")

    elif call.data == "adm_brd":
        if not is_admin(uid): return
        text = "📢 **Broadcast System**\n\nTo send a message to all users, use:\n`/broadcast Your message here`"
        main_bot.edit_message_text(text, cid, mid, reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton("🔙 Back", callback_data="back_admin")), parse_mode="Markdown")
        
    elif call.data == "adm_links":
        if not is_admin(uid): return
        text = "📞 **Support & Welcome Setup**\n\nCommands:\n`/setwelcome [text]`\n`/setvideo [link]`\n`/setlink channel [link]`\n`/setlink chat [link]`"
        main_bot.edit_message_text(text, cid, mid, reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton("🔙 Back", callback_data="back_admin")), parse_mode="Markdown")

    elif call.data == "adm_logs":
        if not is_admin(uid): return
        log_text = "\n".join(db["logs"][-10:]) if db["logs"] else "No recent logs."
        text = f"📋 **Recent Logs:**\n\n`{log_text}`\n\nTo clear: `/clearlogs`"
        main_bot.edit_message_text(text, cid, mid, reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton("🔙 Back", callback_data="back_admin")), parse_mode="Markdown")

    elif call.data == "adm_status":
        if not is_admin(uid): return
        text = f"📡 **Bot Status**\n\nMain Bot: ONLINE 🟢\nReaction Bots Configured: 20\nReady to React: Yes ✅"
        main_bot.edit_message_text(text, cid, mid, reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton("🔙 Back", callback_data="back_admin")), parse_mode="Markdown")

    elif call.data == "adm_db":
        if not is_admin(uid): return
        text = "💾 **Database Management**\n\nCommand:\n`/backupdb` - Send JSON file here"
        main_bot.edit_message_text(text, cid, mid, reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton("🔙 Back", callback_data="back_admin")), parse_mode="Markdown")

    elif call.data == "adm_admin":
        if not is_admin(uid): return
        text = f"👑 **Admin List:**\n{db['admins']}\n\n`/addadmin ID`\n`/deladmin ID`"
        main_bot.edit_message_text(text, cid, mid, reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton("🔙 Back", callback_data="back_admin")), parse_mode="Markdown")

    # Toggles
    elif call.data == "adm_estop":
        if not is_admin(uid): return
        db["settings"]["emergency_stop"] = not db["settings"]["emergency_stop"]
        save_data(db)
        log_activity(f"Emergency Stop set to {db['settings']['emergency_stop']} by {uid}")
        main_bot.answer_callback_query(call.id, f"Emergency Stop is now {'ON' if db['settings']['emergency_stop'] else 'OFF'}", show_alert=True)
        main_bot.edit_message_reply_markup(cid, mid, reply_markup=admin_dashboard_markup())

    elif call.data == "adm_maint":
        if not is_admin(uid): return
        db["settings"]["maintenance"] = not db["settings"]["maintenance"]
        save_data(db)
        main_bot.answer_callback_query(call.id, f"Maintenance is now {'ON' if db['settings']['maintenance'] else 'OFF'}", show_alert=True)
        main_bot.edit_message_reply_markup(cid, mid, reply_markup=admin_dashboard_markup())

    elif call.data == "back_admin":
        if not is_admin(uid): return
        main_bot.edit_message_text("👑 **Welcome to Ultimate Admin Panel**", cid, mid, reply_markup=admin_dashboard_markup(), parse_mode="Markdown")

    elif call.data == "close_panel":
        main_bot.delete_message(cid, mid)

# ================= অ্যাডমিন কমান্ডস লজিক =================
@main_bot.message_handler(commands=['addfsub', 'delfsub', 'setvideo', 'setdelay', 'broadcast', 'ban', 'unban', 'setemojis', 'togglereact', 'togglerandom', 'clearlogs', 'backupdb', 'setlink', 'addadmin', 'deladmin'])
def admin_commands_text(message):
    uid = message.from_user.id
    if not is_admin(uid): return
    cmd = message.text.split()[0].lower()
    args = message.text.split()[1:]
    text_data = message.text.replace(f"{cmd} ", "")
    
    if cmd == '/addfsub' and args:
        ch = args[0]
        if len(db["fsub_channels"]) < 6:
            if ch not in db["fsub_channels"]:
                db["fsub_channels"].append(ch)
                save_data(db)
                main_bot.reply_to(message, f"✅ Added {ch} to FSub.\n**Make sure the bot is ADMIN in this channel!**")
        else: main_bot.reply_to(message, "❌ Maximum 6 channels allowed!")
        
    elif cmd == '/delfsub' and args:
        if args[0] in db["fsub_channels"]:
            db["fsub_channels"].remove(args[0])
            save_data(db)
            main_bot.reply_to(message, f"✅ Removed {args[0]} from FSub.")
            
    elif cmd == '/setvideo' and args:
        db["video_link"] = args[0]; save_data(db)
        main_bot.reply_to(message, "✅ Video link updated!")

    elif cmd == '/setdelay' and len(args) == 2:
        try:
            db["settings"]["min_delay"], db["settings"]["max_delay"] = float(args[0]), float(args[1])
            save_data(db); main_bot.reply_to(message, f"✅ Delay updated: {args[0]}s - {args[1]}s")
        except: main_bot.reply_to(message, "❌ Use valid numbers. Example: `/setdelay 1 3`")
        
    elif cmd == '/setemojis' and args:
        db["settings"]["emojis"] = args[0].split(',')
        save_data(db); main_bot.reply_to(message, f"✅ Emojis updated!")

    elif cmd == '/togglereact':
        db["settings"]["reaction_enabled"] = not db["settings"]["reaction_enabled"]
        save_data(db); main_bot.reply_to(message, f"✅ Reactions are now {'Enabled' if db['settings']['reaction_enabled'] else 'Disabled'}")

    elif cmd == '/togglerandom':
        db["settings"]["random_order"] = not db["settings"]["random_order"]
        save_data(db); main_bot.reply_to(message, f"✅ Random Bot Order: {db['settings']['random_order']}")

    elif cmd == '/clearlogs':
        db["logs"] = []
        save_data(db); main_bot.reply_to(message, "🧹 Logs cleared!")

    elif cmd == '/backupdb':
        with open(DB_FILE, 'rb') as f:
            main_bot.send_document(message.chat.id, f, caption="💾 Database Backup")

    elif cmd == '/ban' and args:
        try:
            ban_id = int(args[0])
            if ban_id not in db["banned_users"]:
                db["banned_users"].append(ban_id); save_data(db)
                main_bot.reply_to(message, f"🚫 Banned user {ban_id}")
        except: pass

    elif cmd == '/unban' and args:
        try:
            ban_id = int(args[0])
            if ban_id in db["banned_users"]:
                db["banned_users"].remove(ban_id); save_data(db)
                main_bot.reply_to(message, f"✅ Unbanned user {ban_id}")
        except: pass

    elif cmd == '/broadcast' and args:
        sent, failed = 0, 0
        main_bot.reply_to(message, "⏳ Broadcasting...")
        for user in db["users"]:
            try:
                main_bot.send_message(user, text_data)
                sent += 1
            except: failed += 1
        main_bot.reply_to(message, f"✅ Broadcast complete!\nSent: {sent}\nFailed: {failed}")

# ================= বট রান করানো =================
keep_alive() # Server alive for Render

print("Ultimate Mega Bot is successfully running...")
main_bot.infinity_polling(timeout=10, long_polling_timeout=5)
