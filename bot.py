import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
import time
import random
import threading
import queue
import json
import os
from keep_alive import keep_alive

# ================= কনফিগারেশন =================
MAIN_BOT_TOKEN = "8500215028:AAG8NNnRgccMe1p1NhQq96SpBF5Hd69x7ko"
OWNER_ID = 8701368956
OWNER_USERNAME = "Premium_buy_admin"

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

main_bot = telebot.TeleBot(MAIN_BOT_TOKEN)
react_clients = [telebot.TeleBot(bot['token']) for bot in REACTION_BOTS_DATA]

# ================= DATABASE MANAGER =================
DB_FILE = 'database.json'

def load_data():
    default_db = {
        "users": {}, "banned_users": [], "admins": [OWNER_ID], 
        "fsub_channels": [
            {"id": "@SLK_Official_Channel", "title": "SLK Official Channel", "type": "Channel", "link": "https://t.me/SLK_Official_Channel"},
            {"id": "@SLK_autoreaction_chat_group", "title": "SLK Auto Reaction Group", "type": "Group", "link": "https://t.me/SLK_autoreaction_chat_group"}
        ],
        "texts": {
            "welcome": "Hey {name} 😻\n\n😘 Welcome, I am @{bot_username}\n━━━━━━━━━━━━━━━━━━━━\n😊 Add me and all my team bots to your channel or group And Make Admin.",
            "how_to_use": "❓ HOW TO USE ❓\n1. Add the Bot to Your Channel or Group.\n2. Make it Admin.",
            "support": "📞 Support :\nFollow Our All Channel To Get All Notice And Update",
            "about": "ℹ️ About this Bot\nPremium Auto Reaction System v2.0\nDeveloper: @{owner}"
        },
        "links": {
            "channel": "https://t.me/SLK_Official_Channel", "chat": "https://t.me/SLK_autoreaction_chat_group", 
            "owner": f"https://t.me/{OWNER_USERNAME}", "youtube": "https://youtube.com", "tutorial": "https://youtube.com"
        },
        "settings": {
            "maintenance": False, "emergency_stop": False, "reaction_enabled": True,
            "min_delay": 1.0, "max_delay": 3.0, "random_order": True,
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
    with open(DB_FILE, 'w') as f: json.dump(data, f)

db = load_data()

# অটোমেটিক ডাটাবেস এরর ফিক্স (ভুল লিংক রিমুভ ও সঠিক ২টা ফিক্সড করা)
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
    db["logs"].insert(0, f"[{time.strftime('%Y-%m-%d %H:%M')}] {msg}")
    if len(db["logs"]) > 50: db["logs"] = db["logs"][:50]
    save_data(db)

def is_admin(user_id):
    return user_id in db["admins"] or user_id == OWNER_ID

# ================= QUEUE REACTION ENGINE =================
reaction_queue = queue.Queue()
processed_messages = set()

def reaction_worker():
    while True:
        task = reaction_queue.get()
        chat_id, message_id = task
        
        if db["settings"]["emergency_stop"] or not db["settings"]["reaction_enabled"]:
            reaction_queue.task_done()
            continue

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
            except telebot.apihelper.ApiTelegramException as e:
                if "Too Many Requests" in str(e): time.sleep(5)
                db["stats"]["failed"] += 1
            except Exception:
                db["stats"]["failed"] += 1
            db["stats"]["total_reacs"] += 1
        
        save_data(db)
        reaction_queue.task_done()

threading.Thread(target=reaction_worker, daemon=True).start()

@main_bot.message_handler(func=lambda m: m.chat.type in ['group', 'supergroup'])
@main_bot.channel_post_handler(func=lambda m: True)
def listen_and_trigger(message):
    if db["settings"]["emergency_stop"] or db["settings"]["maintenance"]: return
    msg_id = f"{message.chat.id}_{message.message_id}"
    if msg_id not in processed_messages:
        processed_messages.add(msg_id)
        if len(processed_messages) > 3000: processed_messages.clear()
        db["stats"]["messages_processed"] += 1
        reaction_queue.put((message.chat.id, message.message_id))

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
        except Exception as e:
            not_joined.append(ch)
    return len(not_joined) == 0, not_joined

def send_fsub_message(chat_id, missing_channels):
    markup = InlineKeyboardMarkup(row_width=1)
    for ch in missing_channels:
        icon = "📢" if ch["type"] == "Channel" else "👥"
        markup.add(InlineKeyboardButton(f"{icon} Join {ch['title']}", url=ch['link']))
        
    markup.add(InlineKeyboardButton("✅ I Have Joined", callback_data="verify_fsub"))
    text = "⚠️ **Security Check!**\nTo use this Premium Bot, you must join our official channels below:"
    main_bot.send_message(chat_id, text, reply_markup=markup, parse_mode="Markdown")

# এখানে প্রোফাইল ছবিসহ ওয়েলকাম মেসেজ সেন্ড করার কোড যুক্ত করা হলো
def send_welcome(chat_id, name, user_id):
    bot_info = main_bot.get_me()
    text = db["texts"]["welcome"].replace("{name}", name).replace("{bot_username}", bot_info.username)
    
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("🤖 Channel React Bot", callback_data="u_ch_react"),
        InlineKeyboardButton("🤖 Group React Bot", callback_data="u_gr_react")
    )
    markup.add(
        InlineKeyboardButton("❓ HOW TO USE", callback_data="u_how"),
        InlineKeyboardButton("📞 Support", callback_data="u_support")
    )
    markup.add(InlineKeyboardButton("ℹ️ About", callback_data="u_about"))
    if is_admin(user_id):
        markup.add(InlineKeyboardButton("👑 PREMIUM ADMIN PANEL", callback_data="open_admin"))
        
    try:
        # ইউজারের প্রোফাইল পিকচার আনার চেষ্টা
        photos = main_bot.get_user_profile_photos(user_id, limit=1)
        if photos.total_count > 0:
            photo_id = photos.photos[0][0].file_id
            main_bot.send_photo(chat_id, photo=photo_id, caption=text, reply_markup=markup, parse_mode="Markdown")
        else:
            main_bot.send_message(chat_id, text, reply_markup=markup, parse_mode="Markdown", disable_web_page_preview=True)
    except Exception as e:
        main_bot.send_message(chat_id, text, reply_markup=markup, parse_mode="Markdown", disable_web_page_preview=True)

# ================= USER HANDLERS =================
@main_bot.message_handler(commands=['start'])
def start_cmd(message):
    if message.chat.type != 'private': return
    uid = message.from_user.id
    cid = message.chat.id
    
    if uid in db["banned_users"]: return
    if db["settings"]["maintenance"] and not is_admin(uid):
        return main_bot.send_message(cid, "🛠️ **Bot is under maintenance.**", parse_mode="Markdown")

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
        InlineKeyboardButton("❌ Close", callback_data="close_ui")
    )
    return m

# ================= CALLBACK HANDLERS =================
@main_bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    uid = call.from_user.id
    cid = call.message.chat.id
    mid = call.message.message_id
    d = call.data

    # --- User Callbacks ---
    if d == "verify_fsub":
        is_joined, missing = check_fsub(uid)
        if is_joined:
            try: main_bot.delete_message(cid, mid)
            except: pass
            send_welcome(cid, call.from_user.first_name, uid)
        else:
            main_bot.answer_callback_query(call.id, f"❌ You haven't joined {len(missing)} channel(s) yet!", show_alert=True)
            
    elif d in ["u_ch_react", "u_gr_react"]:
        t = "Channel" if d == "u_ch_react" else "Group"
        param = "startchannel=start" if d == "u_ch_react" else "startgroup=start"
        text = f"🤖 **{t} Reaction Bots**\n━━━━━━━━━━━━━━━━━━━━\n"
        markup = InlineKeyboardMarkup(row_width=4)
        buttons = []
        for i, b in enumerate(REACTION_BOTS_DATA, 1):
            text += f"{i}. @{b['user']}\n"
            buttons.append(InlineKeyboardButton(f"Add({i})", url=f"https://t.me/{b['user']}?{param}"))
        markup.add(*buttons)
        markup.add(InlineKeyboardButton("🔙 Back", callback_data="home"))
        try:
            main_bot.delete_message(cid, mid)
            main_bot.send_message(cid, text, reply_markup=markup, parse_mode="Markdown")
        except: pass

    elif d == "u_how":
        markup = InlineKeyboardMarkup().add(InlineKeyboardButton("🎥 Watch Video Tutorial", url=db["links"]["tutorial"]), InlineKeyboardButton("🔙 Back", callback_data="home"))
        try:
            main_bot.delete_message(cid, mid)
            main_bot.send_message(cid, db["texts"]["how_to_use"], reply_markup=markup, parse_mode="Markdown")
        except: pass

    elif d == "u_support":
        markup = InlineKeyboardMarkup(row_width=2).add(
            InlineKeyboardButton("📢 Channel", url=db["links"]["channel"]), InlineKeyboardButton("💬 Chat", url=db["links"]["chat"]),
            InlineKeyboardButton("👤 Owner", url=db["links"]["owner"]), InlineKeyboardButton("▶️ YouTube", url=db["links"]["youtube"]),
            InlineKeyboardButton("🔙 Back", callback_data="home")
        )
        try:
            main_bot.delete_message(cid, mid)
            main_bot.send_message(cid, db["texts"]["support"], reply_markup=markup, parse_mode="Markdown")
        except: pass

    elif d == "u_about":
        markup = InlineKeyboardMarkup().add(InlineKeyboardButton("🔙 Back", callback_data="home"))
        try:
            main_bot.delete_message(cid, mid)
            main_bot.send_message(cid, db["texts"]["about"].replace("{owner}", OWNER_USERNAME), reply_markup=markup, parse_mode="Markdown")
        except: pass

    elif d == "home":
        try: main_bot.delete_message(cid, mid)
        except: pass
        send_welcome(cid, call.from_user.first_name, uid)

    # --- Admin Callbacks ---
    elif d == "open_admin":
        if is_admin(uid): 
            try: main_bot.delete_message(cid, mid)
            except: pass
            main_bot.send_message(cid, "👑 **Premium Admin Dashboard**", reply_markup=admin_dashboard_menu(), parse_mode="Markdown")
        
    elif d == "a_dash":
        if not is_admin(uid): return
        st = db["stats"]
        text = f"📊 **System Dashboard**\n━━━━━━━━━━━━━━━━━━━━\n👥 Total Users: {len(db['users'])}\n🚫 Banned: {len(db['banned_users'])}\n\n✅ Reactions Success: {st['success']}\n❌ Reactions Failed: {st['failed']}\n📨 Processed Messages: {st['messages_processed']}\n\n🚨 Emergency Stop: {'ON 🔴' if db['settings']['emergency_stop'] else 'OFF 🟢'}\n🔧 Maintenance: {'ON 🔴' if db['settings']['maintenance'] else 'OFF 🟢'}"
        main_bot.edit_message_text(text, cid, mid, reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton("🔙 Back", callback_data="open_admin")), parse_mode="Markdown")

    elif d == "a_users":
        if not is_admin(uid): return
        text = f"👥 **User Management**\nTotal Users: {len(db['users'])}\nBanned Users: {len(db['banned_users'])}"
        m = InlineKeyboardMarkup().add(
            InlineKeyboardButton("🚫 Ban User", callback_data="inp_ban"),
            InlineKeyboardButton("✅ Unban User", callback_data="inp_unban"),
            InlineKeyboardButton("🔙 Back", callback_data="open_admin")
        )
        main_bot.edit_message_text(text, cid, mid, reply_markup=m, parse_mode="Markdown")

    elif d == "a_bots":
        if not is_admin(uid): return
        text = f"🤖 **Reaction Bots Status**\nTotal Configured: {len(REACTION_BOTS_DATA)}\nQueue Pending: {reaction_queue.qsize()}\n\nAll bots are linked to the main queue and working smoothly."
        main_bot.edit_message_text(text, cid, mid, reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton("🔙 Back", callback_data="open_admin")), parse_mode="Markdown")

    elif d == "a_fsub":
        if not is_admin(uid): return
        ch_list = "\n".join([c["title"] for c in db["fsub_channels"]]) if db["fsub_channels"] else "None"
        text = f"🔐 **Force Subscribe Manager**\nCurrent Channels:\n**{ch_list}**\n\n*(Maximum 6 allowed)*"
        m = InlineKeyboardMarkup().add(
            InlineKeyboardButton("➕ Add Channel", callback_data="inp_addfsub"),
            InlineKeyboardButton("🗑️ Remove Channel", callback_data="inp_delfsub"),
            InlineKeyboardButton("🔙 Back", callback_data="open_admin")
        )
        main_bot.edit_message_text(text, cid, mid, reply_markup=m, parse_mode="Markdown")

    elif d.startswith("inp_"):
        if not is_admin(uid): return
        action = d.split("_")[1]
        admin_states[uid] = action
        
        if action == "addfsub":
            msg = "➕ **Add Force Sub Channel**\n\nPlease **Forward a message** from your channel/group here. (Or send the public @username).\n\n*(Make sure the bot is an ADMIN in that channel first!)*\n\nType `/cancel` to abort."
        else:
            msg = f"✏️ Please send the required value for: **{action.upper()}**\n*(Or send /cancel to abort)*"
            
        main_bot.send_message(cid, msg, parse_mode="Markdown")
        main_bot.answer_callback_query(call.id)

    elif d == "a_react":
        if not is_admin(uid): return
        set = db["settings"]
        text = f"⚙️ **Reaction Settings**\nStatus: {set['reaction_enabled']}\nOrder: {'Random' if set['random_order'] else 'Fixed'}\nDelay: {set['min_delay']}s - {set['max_delay']}s\nEmojis: {''.join(set['emojis'])}"
        m = InlineKeyboardMarkup(row_width=2).add(
            InlineKeyboardButton("🔀 Toggle Order", callback_data="tog_order"),
            InlineKeyboardButton("⏯ Toggle Status", callback_data="tog_react"),
            InlineKeyboardButton("⏱️ Set Delay", callback_data="inp_delay"),
            InlineKeyboardButton("😀 Set Emojis", callback_data="inp_emojis"),
            InlineKeyboardButton("🔙 Back", callback_data="open_admin")
        )
        main_bot.edit_message_text(text, cid, mid, reply_markup=m, parse_mode="Markdown")

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
            InlineKeyboardButton("🔙 Back", callback_data="open_admin")
        )
        main_bot.edit_message_text("🎨 **Text Manager**\nSelect text to edit:", cid, mid, reply_markup=m, parse_mode="Markdown")

    elif d == "a_links":
        if not is_admin(uid): return
        m = InlineKeyboardMarkup().add(
            InlineKeyboardButton("🔗 Official Channel", callback_data="inp_chlink"),
            InlineKeyboardButton("💬 Support Chat", callback_data="inp_chatlink"),
            InlineKeyboardButton("▶️ YouTube Link", callback_data="inp_ytlink"),
            InlineKeyboardButton("🎥 Tutorial Link", callback_data="inp_videolink"),
            InlineKeyboardButton("🔙 Back", callback_data="open_admin")
        )
        main_bot.edit_message_text("🔗 **Links Manager**\nSelect which link to edit:", cid, mid, reply_markup=m, parse_mode="Markdown")

    elif d == "a_logs":
        if not is_admin(uid): return
        logs = "\n".join(db["logs"][:15]) if db["logs"] else "No logs."
        main_bot.edit_message_text(f"📋 **System Logs**\n`{logs}`", cid, mid, reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton("🧹 Clear Logs", callback_data="clear_logs"), InlineKeyboardButton("🔙 Back", callback_data="open_admin")), parse_mode="Markdown")
        
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
        main_bot.send_message(cid, "📢 **Broadcast Mode**\nSend the message you want to broadcast (Text/Photo/Video).\nType `/cancel` to abort.", parse_mode="Markdown")

    elif d == "close_ui":
        main_bot.delete_message(cid, mid)

# ================= SMART STATE HANDLER =================
@main_bot.message_handler(func=lambda m: m.from_user.id in admin_states and admin_states[m.from_user.id] is not None, content_types=['text', 'photo', 'video', 'document', 'audio', 'voice', 'animation'])
def handle_admin_input(message):
    uid = message.from_user.id
    state = admin_states[uid]
    text = message.text if message.text else ""

    if text == "/cancel":
        admin_states[uid] = None
        return main_bot.send_message(uid, "❌ Action Cancelled.", reply_markup=admin_dashboard_menu())

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
                return main_bot.send_message(uid, f"❌ **Error:** Cannot add this channel. Make sure the bot is
