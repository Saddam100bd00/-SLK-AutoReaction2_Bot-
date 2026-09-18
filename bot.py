import os
import time
import random
import threading
import json
from datetime import datetime
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReactionTypeEmoji
from keep_alive import keep_alive

# ================= কনফিগারেশন =================
MAIN_BOT_TOKEN = "8500215028:AAEh9WqwST3PQDWtgK7KfOCOSJpTAZvkmdI" 
OWNER_ID = 8701368956
OWNER_USERNAME = "ItsSaddam9"

# ২০টি বটের ডাটা
REACTION_BOTS_DATA = [
    {"user": "slk_autoreaction_Bot", "token": "8500215028:AAGi3CUatThSfpfBW1fbyJN80T99fTmc7KE"},
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

main_bot = telebot.TeleBot(MAIN_BOT_TOKEN)

# Conflict Fix & Setup React Clients
react_clients = []
for bot in REACTION_BOTS_DATA:
    if bot['token'] == MAIN_BOT_TOKEN:
        react_clients.append({"client": main_bot, "user": bot['user']})
    else:
        react_clients.append({"client": telebot.TeleBot(bot['token']), "user": bot['user']})

ALL_CONTENT_TYPES = ['text', 'photo', 'video', 'document', 'audio', 'voice', 'animation', 'sticker', 'location', 'contact', 'poll', 'dice']

# ================= DATABASE & CACHE =================
DB_FILE = 'database.json'
db_lock = threading.Lock()

def load_data():
    default_db = {
        "users": {}, "banned_users": [], "admins": [OWNER_ID], 
        "fsub_channels": [
            {"id": "@SLK_Official_Channel", "title": "SLK Official Channel", "type": "Channel", "link": "https://t.me/SLK_Official_Channel"},
            {"id": "@SLK_autoreaction_chat_group", "title": "SLK Auto Reaction Group", "type": "Group", "link": "https://t.me/SLK_autoreaction_chat_group"}
        ],
        "texts": {
            "welcome": "✨ **𝗪𝗲𝗹𝗰𝗼𝗺𝗲 𝘁𝗼 𝗣𝗿𝗲𝗺𝗶𝘂𝗺 𝗔𝘂𝘁𝗼 𝗥𝗲𝗮𝗰𝘁𝗶𝗼𝗻** ✨\n━━━━━━━━━━━━━━━━━━━━\n👋 Hey {name} 😻!\n🤖 I am @{bot_username}.\n\n😊 Add me and all my team bots to your Channel or Group, and make us **Admin**! We will automatically react to all your posts and messages.\n\n👨‍💻 **Developer:** @{owner}",
            "how_to_use": "❓ **𝗛𝗢𝗪 𝗧𝗢 𝗨𝗦𝗘** ❓\n━━━━━━━━━━━━━━━━━━━━\n1️⃣ **Add the Bots:** Add the main bot and all reaction bots to your Telegram Channel or Group.\n2️⃣ **Make Admins:** Grant admin privileges to ensure they operate smoothly.\n3️⃣ **Enable Reactions:** Go to your Group/Channel settings and ensure Emojis (❤️, 🥰, 😍, 👍, 🔥) are enabled.\n4️⃣ **Magic Happens:** The bots will automatically apply beautiful emojis to every new message! ✨",
            "support": "📞 **𝗦𝗨𝗣𝗣𝗢𝗥𝗧 & 𝗛𝗘𝗟𝗣** 📞\n━━━━━━━━━━━━━━━━━━━━\n🔔 Follow our official channels to get all notices and the latest updates!\n\n💡 If you face any issues or want to order a custom bot, contact the Owner directly from the buttons below.",
            "about": "ℹ️ **𝗔𝗕𝗢𝗨𝗧 𝗧𝗛𝗜𝗦 𝗕𝗢𝗧** ℹ️\n━━━━━━━━━━━━━━━━━━━━\n🚀 **Premium Auto Reaction System v2.0**\n⚡ Powered by Advanced Threading & Multi-Reaction Engine.\n\n👨‍💻 **Developed By:** @{owner}"
        },
        "links": {
            "channel": "https://t.me/SLK_Official_Channel", "chat": "https://t.me/SLK_autoreaction_chat_group", 
            "owner": f"https://t.me/{OWNER_USERNAME}", "youtube": "https://youtube.com", "tutorial": "https://youtube.com"
        },
        "settings": {
            "maintenance": False, "emergency_stop": False, "reaction_enabled": True,
            "min_delay": 2.0, "max_delay": 8.0, "random_order": True,
            "emojis": ['❤️', '🥰', '😍', '😘', '👍', '🔥', '🎉']
        },
        "stats": {"total_reacs": 0, "success": 0, "failed": 0, "messages_processed": 0},
        "logs": []
    }
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, 'r') as f:
                data = json.load(f)
                for k, v in default_db.items():
                    if k not in data: data[k] = v
                    elif isinstance(v, dict):
                        for sub_k in v:
                            if sub_k not in data[k]: data[k][sub_k] = v[sub_k]
                return data
        except: pass
    return default_db

def save_data(data):
    with db_lock:
        with open(DB_FILE, 'w') as f: json.dump(data, f)

db = load_data()

def auto_fix_db():
    existing_ids = [ch["id"] for ch in db["fsub_channels"] if isinstance(ch, dict)]
    if "@SLK_Official_Channel" not in existing_ids:
        db["fsub_channels"].insert(0, {"id": "@SLK_Official_Channel", "title": "SLK Official Channel", "type": "Channel", "link": "https://t.me/SLK_Official_Channel"})
    if "@SLK_autoreaction_chat_group" not in existing_ids:
        db["fsub_channels"].append({"id": "@SLK_autoreaction_chat_group", "title": "SLK Auto Reaction Group", "type": "Group", "link": "https://t.me/SLK_autoreaction_chat_group"})

    valid_fsub = []
    for ch in db["fsub_channels"]:
        if isinstance(ch, dict) and not ch["id"].startswith('@+'):
            valid_fsub.append(ch)
            
    db["fsub_channels"] = valid_fsub
    save_data(db)

auto_fix_db()
admin_states = {}

def log_activity(msg):
    db["logs"].insert(0, f"[{time.strftime('%H:%M')}] {msg}")
    if len(db["logs"]) > 20: db["logs"] = db["logs"][:20]
    save_data(db)

def is_admin(user_id):
    return user_id in db["admins"] or user_id == OWNER_ID

# ================= ADVANCED FAST REACTION ENGINE WITH ANTI-FLOOD =================
processed_messages = set()

def process_reactions(chat_id, message_id):
    if db["settings"]["emergency_stop"] or not db["settings"]["reaction_enabled"]: return
    
    emojis = db["settings"]["emojis"]
    min_d, max_d = db["settings"]["min_delay"], db["settings"]["max_delay"]
    bots_to_use = list(react_clients)
    if db["settings"]["random_order"]: random.shuffle(bots_to_use)
    
    for bot_obj in bots_to_use:
        if db["settings"]["emergency_stop"]: break
        time.sleep(random.uniform(min_d, max_d))
        
        client = bot_obj["client"]
        bot_uname = bot_obj["user"]
        
        # Anti-Flood Logic (Retry up to 3 times if Telegram blocks)
        max_retries = 3
        for attempt in range(max_retries):
            try:
                chosen_emoji = random.choice(emojis)
                client.set_message_reaction(chat_id, message_id, [ReactionTypeEmoji(chosen_emoji)], is_big=False)
                db["stats"]["success"] += 1
                break # Success, so break out of retry loop
            except telebot.apihelper.ApiTelegramException as e:
                err_msg = e.result_json.get('description', str(e)) if hasattr(e, 'result_json') else str(e)
                
                # If it's a Rate Limit (FloodWait) Error
                if "Too Many Requests" in err_msg or "retry after" in err_msg.lower():
                    wait_time = 5 # Default wait
                    if hasattr(e, 'result_json') and 'parameters' in e.result_json:
                        wait_time = e.result_json['parameters'].get('retry_after', 5)
                    
                    log_activity(f"⚠️ {bot_uname}: Telegram said wait {wait_time}s. Retrying...")
                    time.sleep(wait_time + 1)
                    continue # Try again after waiting
                else:
                    # Other API Errors (e.g. Channel React Not Allowed)
                    log_activity(f"❌ {bot_uname}: {err_msg[:40]}")
                    db["stats"]["failed"] += 1
                    break 
            except Exception as ex:
                log_activity(f"❌ {bot_uname}: {str(ex)[:40]}")
                db["stats"]["failed"] += 1
                break
                
        db["stats"]["total_reacs"] += 1
    save_data(db)

def trigger_reactions(message):
    if db["settings"]["emergency_stop"] or db["settings"]["maintenance"]: return
    msg_id = f"{message.chat.id}_{message.message_id}"
    if msg_id not in processed_messages:
        processed_messages.add(msg_id)
        if len(processed_messages) > 5000: processed_messages.clear()
        
        db["stats"]["messages_processed"] += 1
        save_data(db)
        
        # Dedicated thread for every message
        threading.Thread(target=process_reactions, args=(message.chat.id, message.message_id), daemon=True).start()

# ⚠️ Channel Handler
@main_bot.channel_post_handler(content_types=ALL_CONTENT_TYPES)
def handle_channel_post(message):
    log_activity("📩 Channel Post Detected!")
    trigger_reactions(message)

# ⚠️ Group Handler
@main_bot.message_handler(func=lambda m: m.chat.type in ['group', 'supergroup'], content_types=ALL_CONTENT_TYPES)
def handle_group_message(message):
    log_activity("📩 Group Message Detected!")
    trigger_reactions(message)

# ================= FSUB (Force Join) LOGIC =================
def check_fsub(user_id):
    if not db["fsub_channels"]: return True, []
    not_joined = []
    for ch in db["fsub_channels"]:
        chat_id = ch["id"]
        try:
            stat = main_bot.get_chat_member(chat_id, user_id).status
            if stat in ['left', 'kicked']:
                not_joined.append(ch)
        except Exception:
            not_joined.append(ch)
    return len(not_joined) == 0, not_joined

def send_fsub_message(chat_id, missing_channels):
    markup = InlineKeyboardMarkup(row_width=1)
    for ch in missing_channels:
        btn_text = "📢 Join Channel" if ch["type"] == "Channel" else "👥 Join Group"
        markup.add(InlineKeyboardButton(btn_text, url=ch['link']))
        
    markup.add(InlineKeyboardButton("✅ Verify Join", callback_data="verify_fsub"))
    text = "🛑 **𝗦𝗘𝗖𝗨𝗥𝗜𝗧𝗬 𝗖𝗛𝗘𝗖𝗞!** 🛑\n━━━━━━━━━━━━━━━━━━━━\n⚠️ To use this Premium Bot, you **must join** our official channels below:"
    main_bot.send_message(chat_id, text, reply_markup=markup, parse_mode="Markdown")

# ================= SMOOTH UI SYSTEM =================
def get_user_menu(user_id):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("📢 Channel React Bot", callback_data="u_ch_react"),
        InlineKeyboardButton("👥 Group React Bot", callback_data="u_gr_react")
    )
    markup.add(
        InlineKeyboardButton("❓ How To Use", callback_data="u_how"),
        InlineKeyboardButton("📞 Support", callback_data="u_support")
    )
    markup.add(InlineKeyboardButton("ℹ️ About", callback_data="u_about"))
    if is_admin(user_id):
        markup.add(InlineKeyboardButton("👑 𝗣𝗥𝗘𝗠𝗜𝗨𝗠 𝗔𝗗𝗠𝗜𝗡 𝗣𝗔𝗡𝗘𝗟", callback_data="open_admin"))
    return markup

def get_welcome_text(user):
    bot_info = main_bot.get_me()
    safe_bot_name = bot_info.username.replace("_", "\\_")
    safe_owner = OWNER_USERNAME.replace("_", "\\_")
    return db["texts"]["welcome"].replace("{name}", user.first_name).replace("{bot_username}", safe_bot_name).replace("{owner}", safe_owner)

def update_ui(call, text, markup):
    try:
        if call.message.content_type == 'photo':
            main_bot.edit_message_caption(caption=text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        else:
            main_bot.edit_message_text(text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup, parse_mode="Markdown", disable_web_page_preview=True)
    except: pass

def send_welcome(chat_id, name, user_id):
    bot_info = main_bot.get_me()
    safe_bot_name = bot_info.username.replace("_", "\\_")
    safe_owner = OWNER_USERNAME.replace("_", "\\_")
    text = db["texts"]["welcome"].replace("{name}", name).replace("{bot_username}", safe_bot_name).replace("{owner}", safe_owner)
    markup = get_user_menu(user_id)
    try:
        photos = main_bot.get_user_profile_photos(user_id, limit=1)
        if photos.total_count > 0:
            photo_id = photos.photos[0][0].file_id
            main_bot.send_photo(chat_id, photo=photo_id, caption=text, reply_markup=markup, parse_mode="Markdown")
        else:
            main_bot.send_photo(chat_id, photo="https://i.imgur.com/7bQeXoF.png", caption=text, reply_markup=markup, parse_mode="Markdown")
    except Exception:
        main_bot.send_message(chat_id, text, reply_markup=markup, parse_mode="Markdown", disable_web_page_preview=True)

# ================= START COMMAND =================
@main_bot.message_handler(commands=['start'])
def start_cmd(message):
    if message.chat.type != 'private': return
    uid = message.from_user.id
    cid = message.chat.id
    
    if uid in db["banned_users"]: return
    if db["settings"]["maintenance"] and not is_admin(uid):
        return main_bot.send_message(cid, "🛠️ **Bot is under Maintenance. Please try again later!**", parse_mode="Markdown")

    if str(uid) not in db["users"]:
        db["users"][str(uid)] = {"name": message.from_user.first_name, "date": time.strftime("%Y-%m-%d")}
        save_data(db)
        log_activity(f"New User: {uid}")

    is_joined, missing = check_fsub(uid)
    if not is_joined:
        send_fsub_message(cid, missing)
        return

    send_welcome(cid, message.from_user.first_name, uid)

# ================= ADMIN MENUS =================
def admin_dashboard_menu():
    m = InlineKeyboardMarkup(row_width=2)
    m.add(
        InlineKeyboardButton("📊 Dashboard", callback_data="a_dash"),
        InlineKeyboardButton("👥 Users", callback_data="a_users"),
        InlineKeyboardButton("🔐 FSub Manager", callback_data="a_fsub"),
        InlineKeyboardButton("⚙️ React Settings", callback_data="a_react"),
        InlineKeyboardButton("🤖 Bot Manager", callback_data="a_bots"),
        InlineKeyboardButton("🎨 Texts & UI", callback_data="a_texts"),
        InlineKeyboardButton("🔗 Links", callback_data="a_links"),
        InlineKeyboardButton("📢 Broadcast", callback_data="a_brd"),
        InlineKeyboardButton("📋 Logs", callback_data="a_logs"),
        InlineKeyboardButton("🔧 Maintenance", callback_data="a_maint"),
        InlineKeyboardButton("🚨 Emergency Stop", callback_data="a_estop"),
        InlineKeyboardButton("🏠 Back Home", callback_data="home")
    )
    return m

# ================= CALLBACK HANDLERS =================
@main_bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    uid = call.from_user.id
    d = call.data

    if d == "verify_fsub":
        is_joined, missing = check_fsub(uid)
        if is_joined:
            try: main_bot.delete_message(call.message.chat.id, call.message.message_id)
            except: pass
            send_welcome(call.message.chat.id, call.from_user.first_name, uid)
            main_bot.answer_callback_query(call.id, "✅ Verified Successfully!", show_alert=False)
        else:
            main_bot.answer_callback_query(call.id, f"❌ You haven't joined {len(missing)} channel(s) yet!", show_alert=True)
            
    elif d in ["u_ch_react", "u_gr_react"]:
        t = "Channel" if d == "u_ch_react" else "Group"
        param = "startchannel=start" if d == "u_ch_react" else "startgroup=start"
        text = f"🤖 **{t} 𝗥𝗲𝗮𝗰𝘁𝗶𝗼𝗻 𝗕𝗼𝘁𝘀**\n━━━━━━━━━━━━━━━━━━━━\n✅ Add all bots to your {t} and make them Admin 🔰\n\n"
        markup = InlineKeyboardMarkup(row_width=4)
        buttons = []
        for i in range(1, 21):
            num_suffix = "" if i == 1 else str(i)
            bot_username = f"slk_autoreaction{num_suffix}_Bot"
            safe_username = bot_username.replace('_', '\\_') 
            text += f"**{i}.** [@{safe_username}](https://t.me/{bot_username})\n"
            buttons.append(InlineKeyboardButton(f"➕ Add({i})", url=f"https://t.me/{bot_username}?{param}"))
            
        markup.add(*buttons)
        markup.add(InlineKeyboardButton("🔙 Back to Menu", callback_data="home"))
        update_ui(call, text, markup)

    elif d == "u_how":
        markup = InlineKeyboardMarkup().add(InlineKeyboardButton("🎥 Watch Video Tutorial", url=db["links"]["tutorial"]), InlineKeyboardButton("🔙 Back to Menu", callback_data="home"))
        update_ui(call, db["texts"]["how_to_use"], markup)

    elif d == "u_support":
        markup = InlineKeyboardMarkup(row_width=2).add(
            InlineKeyboardButton("📢 Official Channel", url=db["links"]["channel"]), InlineKeyboardButton("💬 Support Chat", url=db["links"]["chat"]),
            InlineKeyboardButton("👤 Developer", url=db["links"]["owner"]), InlineKeyboardButton("▶️ YouTube", url=db["links"]["youtube"]),
            InlineKeyboardButton("🔙 Back to Menu", callback_data="home")
        )
        update_ui(call, db["texts"]["support"], markup)

    elif d == "u_about":
        markup = InlineKeyboardMarkup().add(InlineKeyboardButton("🔙 Back to Menu", callback_data="home"))
        safe_owner = OWNER_USERNAME.replace("_", "\\_")
        update_ui(call, db["texts"]["about"].replace("{owner}", safe_owner), markup)

    elif d == "home":
        update_ui(call, get_welcome_text(call.from_user), get_user_menu(uid))

    elif d == "open_admin":
        if is_admin(uid): 
            update_ui(call, "👑 **𝗣𝗥𝗘𝗠𝗜𝗨𝗠 𝗔𝗗𝗠𝗜𝗡 𝗗𝗔𝗦𝗛𝗕𝗢𝗔𝗥𝗗** 👑\n━━━━━━━━━━━━━━━━━━━━\nSelect an option below to manage your Mega Bot:", admin_dashboard_menu())
        
    elif d == "a_dash":
        if not is_admin(uid): return
        st = db["stats"]
        text = f"📊 **𝗦𝘆𝘀𝘁𝗲𝗺 𝗗𝗮𝘀𝗵𝗯𝗼𝗮𝗿𝗱**\n━━━━━━━━━━━━━━━━━━━━\n👥 Total Users: {len(db['users'])}\n🚫 Banned: {len(db['banned_users'])}\n\n✅ Reactions Success: {st['success']}\n❌ Reactions Failed: {st['failed']}\n📨 Messages Processed: {st['messages_processed']}\n\n🚨 Emergency Stop: {'ON 🔴' if db['settings']['emergency_stop'] else 'OFF 🟢'}\n🔧 Maintenance: {'ON 🔴' if db['settings']['maintenance'] else 'OFF 🟢'}"
        update_ui(call, text, InlineKeyboardMarkup().add(InlineKeyboardButton("🔙 Back to Panel", callback_data="open_admin")))

    elif d == "a_users":
        if not is_admin(uid): return
        text = f"👥 **𝗨𝘀𝗲𝗿 𝗠𝗮𝗻𝗮𝗴𝗲𝗺𝗲𝗻𝘁**\n━━━━━━━━━━━━━━━━━━━━\nTotal Users: {len(db['users'])}\nBanned Users: {len(db['banned_users'])}"
        m = InlineKeyboardMarkup().add(
            InlineKeyboardButton("🚫 Ban User", callback_data="inp_ban"),
            InlineKeyboardButton("✅ Unban User", callback_data="inp_unban"),
            InlineKeyboardButton("🔙 Back to Panel", callback_data="open_admin")
        )
        update_ui(call, text, m)

    elif d == "a_bots":
        if not is_admin(uid): return
        text = f"🤖 **𝗥𝗲𝗮𝗰𝘁𝗶𝗼𝗻 𝗕𝗼𝘁𝘀 𝗦𝘁𝗮𝘁𝘂𝘀**\n━━━━━━━━━━━━━━━━━━━━\nTotal Configured: {len(REACTION_BOTS_DATA)}\n\n✅ All bots are fully active and utilizing the Multi-Threading Engine!"
        update_ui(call, text, InlineKeyboardMarkup().add(InlineKeyboardButton("🔙 Back to Panel", callback_data="open_admin")))

    elif d == "a_fsub":
        if not is_admin(uid): return
        ch_list = "\n".join([c["title"].replace("_", "\\_") for c in db["fsub_channels"]]) if db["fsub_channels"] else "None"
        text = f"🔐 **𝗙𝗼𝗿𝗰𝗲 𝗦𝘂𝗯𝘀𝗰𝗿𝗶𝗯𝗲 𝗠𝗮𝗻𝗮𝗴𝗲𝗿**\n━━━━━━━━━━━━━━━━━━━━\nActive Channels:\n**{ch_list}**\n\n*(Maximum 6 allowed)*"
        m = InlineKeyboardMarkup().add(
            InlineKeyboardButton("➕ Add Channel", callback_data="inp_addfsub"),
            InlineKeyboardButton("🗑️ Remove Channel", callback_data="inp_delfsub"),
            InlineKeyboardButton("🔙 Back to Panel", callback_data="open_admin")
        )
        update_ui(call, text, m)

    elif d.startswith("inp_"):
        if not is_admin(uid): return
        action = d.split("_")[1]
        admin_states[uid] = action
        if action == "addfsub":
            msg = "➕ **Add Force Sub Channel**\n\nPlease **Forward a message** from your channel/group here. (Or send the public @username).\n\n*(Make sure the bot is an ADMIN in that channel first!)*\n\nType `/cancel` to abort."
        else:
            msg = f"✏️ Please send the required value for: **{action.upper()}**\n*(Or send /cancel to abort)*"
        main_bot.send_message(call.message.chat.id, msg, parse_mode="Markdown")
        main_bot.answer_callback_query(call.id)

    elif d == "a_react":
        if not is_admin(uid): return
        set = db["settings"]
        text = f"⚙️ **𝗥𝗲𝗮𝗰𝘁𝗶𝗼𝗻 𝗦𝗲𝘁𝘁𝗶𝗻𝗴𝘀**\n━━━━━━━━━━━━━━━━━━━━\nStatus: {'Enabled ✅' if set['reaction_enabled'] else 'Disabled ❌'}\nOrder: {'Random 🔀' if set['random_order'] else 'Fixed 🔢'}\nDelay: {set['min_delay']}s - {set['max_delay']}s\nEmojis: {''.join(set['emojis'])}"
        m = InlineKeyboardMarkup(row_width=2).add(
            InlineKeyboardButton("🔀 Toggle Order", callback_data="tog_order"),
            InlineKeyboardButton("⏯ Toggle Status", callback_data="tog_react"),
            InlineKeyboardButton("⏱️ Set Delay", callback_data="inp_delay"),
            InlineKeyboardButton("😀 Set Emojis", callback_data="inp_emojis"),
            InlineKeyboardButton("🔙 Back to Panel", callback_data="open_admin")
        )
        update_ui(call, text, m)

    elif d == "tog_order":
        db["settings"]["random_order"] = not db["settings"]["random_order"]
        save_data(db); main_bot.answer_callback_query(call.id, "Order Updated!", show_alert=True); callback_handler(telebot.types.CallbackQuery(call.id, call.from_user, "a_react", call.chat_instance, call.message))
    elif d == "tog_react":
        db["settings"]["reaction_enabled"] = not db["settings"]["reaction_enabled"]
        save_data(db); main_bot.answer_callback_query(call.id, "Status Updated!", show_alert=True); callback_handler(telebot.types.CallbackQuery(call.id, call.from_user, "a_react", call.chat_instance, call.message))

    elif d == "a_texts":
        if not is_admin(uid): return
        m = InlineKeyboardMarkup().add(
            InlineKeyboardButton("✏️ Welcome Text", callback_data="inp_welcome"),
            InlineKeyboardButton("✏️ How To Use", callback_data="inp_howtouse"),
            InlineKeyboardButton("✏️ Support Text", callback_data="inp_support"),
            InlineKeyboardButton("🔙 Back to Panel", callback_data="open_admin")
        )
        update_ui(call, "🎨 **𝗧𝗲𝘅𝘁 & 𝗨𝗜 𝗠𝗮𝗻𝗮𝗴𝗲𝗿**\n━━━━━━━━━━━━━━━━━━━━\nSelect text to edit:", m)

    elif d == "a_links":
        if not is_admin(uid): return
        m = InlineKeyboardMarkup().add(
            InlineKeyboardButton("🔗 Official Channel", callback_data="inp_chlink"),
            InlineKeyboardButton("💬 Support Chat", callback_data="inp_chatlink"),
            InlineKeyboardButton("▶️ YouTube Link", callback_data="inp_ytlink"),
            InlineKeyboardButton("🎥 Tutorial Link", callback_data="inp_videolink"),
            InlineKeyboardButton("🔙 Back to Panel", callback_data="open_admin")
        )
        update_ui(call, "🔗 **𝗟𝗶𝗻𝗸𝘀 𝗠𝗮𝗻𝗮𝗴𝗲𝗿**\n━━━━━━━━━━━━━━━━━━━━\nSelect which link to edit:", m)

    elif d == "a_logs":
        if not is_admin(uid): return
        logs = "\n".join(db["logs"][:20]) if db["logs"] else "No logs."
        update_ui(call, f"📋 **𝗦𝘆𝘀𝘁𝗲𝗺 𝗟𝗼𝗴𝘀 (Exact Errors)**\n━━━━━━━━━━━━━━━━━━━━\n`{logs}`", InlineKeyboardMarkup().add(InlineKeyboardButton("🧹 Clear Logs", callback_data="clear_logs"), InlineKeyboardButton("🔙 Back to Panel", callback_data="open_admin")))
        
    elif d == "clear_logs":
        db["logs"] = []; save_data(db); main_bot.answer_callback_query(call.id, "Logs Cleared!"); callback_handler(telebot.types.CallbackQuery(call.id, call.from_user, "open_admin", call.chat_instance, call.message))

    elif d == "a_estop":
        if not is_admin(uid): return
        db["settings"]["emergency_stop"] = not db["settings"]["emergency_stop"]
        save_data(db); main_bot.answer_callback_query(call.id, f"Emergency Stop: {db['settings']['emergency_stop']}", show_alert=True)
        callback_handler(telebot.types.CallbackQuery(call.id, call.from_user, "open_admin", call.chat_instance, call.message))

    elif d == "a_maint":
        if not is_admin(uid): return
        db["settings"]["maintenance"] = not db["settings"]["maintenance"]
        save_data(db); main_bot.answer_callback_query(call.id, f"Maintenance: {db['settings']['maintenance']}", show_alert=True)
        callback_handler(telebot.types.CallbackQuery(call.id, call.from_user, "open_admin", call.chat_instance, call.message))

    elif d == "a_brd":
        if not is_admin(uid): return
        admin_states[uid] = "broadcast"
        main_bot.send_message(call.message.chat.id, "📢 **Broadcast Mode**\nSend the message you want to broadcast (Text/Photo/Video).\nType `/cancel` to abort.", parse_mode="Markdown")

# ================= SMART STATE HANDLER =================
def is_admin_inputting(m):
    if not m.from_user: return False
    return m.from_user.id in admin_states and admin_states[m.from_user.id] is not None

@main_bot.message_handler(func=is_admin_inputting, content_types=ALL_CONTENT_TYPES)
def handle_admin_input(message):
    uid = message.from_user.id
    state = admin_states[uid]
    text = message.text if message.text else ""

    if text == "/cancel":
        admin_states[uid] = None
        return main_bot.send_message(uid, "❌ Action Cancelled.")

    try:
        if state == "addfsub":
            chat_id, chat_title, invite_link = None, "Channel", None
            if message.forward_from_chat:
                chat_id = str(message.forward_from_chat.id)
                chat_title = message.forward_from_chat.title
            else:
                if "t.me/+" in text or "joinchat" in text:
                    return main_bot.send_message(uid, "❌ **Error:** Please do not send private links! Forward a message from the channel or send the @username.", parse_mode="Markdown")
                chat_id = text if text.startswith('@') or text.startswith('-100') else f"@{text.replace('https://t.me/', '').replace('t.me/', '')}"

            try:
                c_info = main_bot.get_chat(chat_id)
                chat_title = c_info.title
                c_type = "Channel" if c_info.type == 'channel' else "Group"
                if c_info.username: invite_link = f"https://t.me/{c_info.username}"
                else: invite_link = main_bot.export_chat_invite_link(chat_id)
                main_bot.get_chat_member(chat_id, main_bot.get_me().id)
                
                new_ch = {"id": str(chat_id), "title": chat_title, "type": c_type, "link": invite_link}
                db["fsub_channels"] = [ch for ch in db["fsub_channels"] if ch["id"] != str(chat_id)]
                if len(db["fsub_channels"]) < 6:
                    db["fsub_channels"].append(new_ch)
                    main_bot.send_message(uid, f"✅ Successfully Added **{chat_title}** ({c_type})!", parse_mode="Markdown")
                else:
                    return main_bot.send_message(uid, "❌ Maximum 6 Channels allowed!")
            except Exception as e:
                return main_bot.send_message(uid, f"❌ **Error:** Cannot add this channel. Make sure the bot is an **Admin** in the channel!", parse_mode="Markdown")

        elif state == "delfsub":
            found = False
            for ch in list(db["fsub_channels"]):
                if ch["id"] == text or ch["title"].lower() == text.lower() or text in ch["link"]:
                    db["fsub_channels"].remove(ch)
                    found = True
                    main_bot.send_message(uid, f"✅ Removed {ch['title']} from FSub.")
            if not found: main_bot.send_message(uid, "❌ Channel not found in list.")
            
        elif state == "ban":
            ban_id = int(text)
            if ban_id not in db["banned_users"]: db["banned_users"].append(ban_id)
            main_bot.send_message(uid, f"✅ Banned {ban_id}.")
            
        elif state == "unban":
            ban_id = int(text)
            if ban_id in db["banned_users"]: db["banned_users"].remove(ban_id)
            main_bot.send_message(uid, f"✅ Unbanned {ban_id}.")
            
        elif state == "welcome":
            db["texts"]["welcome"] = text; main_bot.send_message(uid, "✅ Welcome text updated!")
        elif state == "howtouse":
            db["texts"]["how_to_use"] = text; main_bot.send_message(uid, "✅ How To Use updated!")
        elif state == "support":
            db["texts"]["support"] = text; main_bot.send_message(uid, "✅ Support text updated!")
        elif state == "emojis":
            db["settings"]["emojis"] = text.split(','); main_bot.send_message(uid, "✅ Emojis updated!")
        elif state == "chlink":
            db["links"]["channel"] = text; main_bot.send_message(uid, "✅ Channel Link updated!")
        elif state == "chatlink":
            db["links"]["chat"] = text; main_bot.send_message(uid, "✅ Chat Link updated!")
        elif state == "ytlink":
            db["links"]["youtube"] = text; main_bot.send_message(uid, "✅ YouTube Link updated!")
        elif state == "videolink":
            db["links"]["tutorial"] = text; main_bot.send_message(uid, "✅ Tutorial Video Link updated!")
        elif state == "delay":
            min_d, max_d = map(float, text.split())
            db["settings"]["min_delay"], db["settings"]["max_delay"] = min_d, max_d
            main_bot.send_message(uid, "✅ Delay updated!")
            
        elif state == "broadcast":
            main_bot.send_message(uid, "⏳ Broadcasting started...")
            sent, failed = 0, 0
            for user in list(db["users"].keys()):
                try:
                    main_bot.copy_message(user, message.chat.id, message.message_id)
                    sent += 1
                except: failed += 1
            main_bot.send_message(uid, f"✅ Broadcast Done!\nSuccess: {sent}\nFailed: {failed}")

        save_data(db)
        log_activity(f"Admin {uid} updated {state}")
    except Exception as e:
        main_bot.send_message(uid, f"❌ Error processing input. Please check the format and try again.")
    
    admin_states[uid] = None

# ================= RUN SERVER =================
if __name__ == "__main__":
    main_bot.remove_webhook()
    time.sleep(2)
    keep_alive()
    print("🚀 Premium Mega Bot is Running...")
    main_bot.infinity_polling(timeout=20, long_polling_timeout=10)
