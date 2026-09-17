import os
import time
import asyncio
import logging
import re
import httpx
import urllib.parse
import random
from datetime import datetime
from dotenv import load_dotenv
from contextlib import asynccontextmanager

# Aiogram Imports (১০০% Async Engine)
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile, ReactionTypeEmoji
from aiogram.client.default import DefaultBotProperties

# Database Imports
from sqlalchemy import Column, Integer, String, Boolean, DateTime, BigInteger, select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

# FastAPI & Uvicorn for Render Web Server
from fastapi import FastAPI
import uvicorn

# ================= 1. CONFIGURATION =================
load_dotenv()

MAIN_BOT_TOKEN = os.environ.get("BOT_TOKEN", "8500215028:AAGi3CUatThSfpfBW1fbyJN80T99fTmc7KE")
OWNER_ID = 8701368956
OWNER_USERNAME = "Premium_buy_admin"

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite+aiosqlite:///terabox.db")

try:
    MAX_FILE_SIZE_BYTES = int(os.environ.get("MAX_FILE_SIZE_GB", 2)) * 1024 * 1024 * 1024
except:
    MAX_FILE_SIZE_BYTES = 2 * 1024 * 1024 * 1024

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)
logging.basicConfig(level=logging.INFO)

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

# Initialize all bots asynchronously
main_bot = Bot(token=MAIN_BOT_TOKEN, default=DefaultBotProperties(parse_mode="Markdown"))
react_clients = []
for bot_data in REACTION_BOTS_DATA:
    if bot_data['token'] == MAIN_BOT_TOKEN:
        react_clients.append({"client": main_bot, "user": bot_data['user']})
    else:
        react_clients.append({"client": Bot(token=bot_data['token']), "user": bot_data['user']})

# ================= 2. DATABASE MODELS =================
Base = declarative_base()
engine = create_async_engine(DATABASE_URL, echo=False)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, unique=True)
    username = Column(String, nullable=True)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# ================= 3. SYSTEM CACHE & LOGIC =================
DB_FILE = 'database.json'

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
            "about": "ℹ️ **𝗔𝗕𝗢𝗨𝗧 𝗧𝗛𝗜𝗦 𝗕𝗢𝗧** ℹ️\n━━━━━━━━━━━━━━━━━━━━\n🚀 **Premium Auto Reaction System v2.0**\n⚡ Powered by Advanced Async Engine.\n\n👨‍💻 **Developed By:** @{owner}"
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

def log_activity(msg):
    db["logs"].insert(0, f"[{time.strftime('%H:%M')}] {msg}")
    if len(db["logs"]) > 20: db["logs"] = db["logs"][:20]
    save_data(db)

def is_admin(user_id):
    return user_id in db["admins"] or user_id == OWNER_ID

# ================= 4. THE ULTIMATE ASYNC REACTION ENGINE =================
processed_messages = set()

async def process_reactions(chat_id: int, message_id: int):
    """এটি ১০০% অ্যাসিনক্রোনাস (Async) ইঞ্জিন, কোনো জ্যাম হবে না!"""
    if db["settings"]["emergency_stop"] or not db["settings"]["reaction_enabled"]: return
    
    emojis = db["settings"]["emojis"]
    min_d, max_d = db["settings"]["min_delay"], db["settings"]["max_delay"]
    bots_to_use = list(react_clients)
    if db["settings"]["random_order"]: random.shuffle(bots_to_use)
    
    for bot_obj in bots_to_use:
        if db["settings"]["emergency_stop"]: break
        
        # Async delay (Server block হবে না)
        await asyncio.sleep(random.uniform(min_d, max_d))
        
        client: Bot = bot_obj["client"]
        bot_uname = bot_obj["user"]
        
        try:
            chosen_emoji = random.choice(emojis)
            # Modern Aiogram Reaction implementation
            await client.set_message_reaction(
                chat_id=chat_id, 
                message_id=message_id, 
                reaction=[ReactionTypeEmoji(type="emoji", emoji=chosen_emoji)],
                is_big=False
            )
            db["stats"]["success"] += 1
        except Exception as e:
            err = str(e)
            if "Too Many Requests" in err: 
                await asyncio.sleep(5)
            log_activity(f"❌ {bot_uname}: {err[:35]}")
            db["stats"]["failed"] += 1
            
        db["stats"]["total_reacs"] += 1
    save_data(db)

dp = Dispatcher()

# Channels Handler
@dp.channel_post()
async def handle_channel_post(message: types.Message):
    msg_id = f"{message.chat.id}_{message.message_id}"
    if msg_id not in processed_messages:
        processed_messages.add(msg_id)
        if len(processed_messages) > 5000: processed_messages.clear()
        db["stats"]["messages_processed"] += 1
        save_data(db)
        log_activity("📩 Channel Post Detected!")
        # Background task
        asyncio.create_task(process_reactions(message.chat.id, message.message_id))

# Group Handler
@dp.message(F.chat.type.in_(['group', 'supergroup']))
async def handle_group_message(message: types.Message):
    msg_id = f"{message.chat.id}_{message.message_id}"
    if msg_id not in processed_messages:
        processed_messages.add(msg_id)
        if len(processed_messages) > 5000: processed_messages.clear()
        db["stats"]["messages_processed"] += 1
        save_data(db)
        log_activity("📩 Group Message Detected!")
        asyncio.create_task(process_reactions(message.chat.id, message.message_id))

# ================= 5. USER & ADMIN UI =================
def get_user_menu(user_id):
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📥 Download TeraBox", callback_data="menu_download"),
         InlineKeyboardButton(text="👤 My Account", callback_data="menu_account")],
        [InlineKeyboardButton(text="📢 Channel React Bot", callback_data="u_ch_react"),
         InlineKeyboardButton(text="👥 Group React Bot", callback_data="u_gr_react")],
        [InlineKeyboardButton(text="❓ How To Use", callback_data="u_how"),
         InlineKeyboardButton(text="📞 Support", callback_data="u_support")]
    ])
    if is_admin(user_id):
        markup.inline_keyboard.append([InlineKeyboardButton(text="👑 𝗣𝗥𝗘𝗠𝗜𝗨𝗠 𝗔𝗗𝗠𝗜𝗡 𝗣𝗔𝗡𝗘𝗟", callback_data="open_admin")])
    return markup

def admin_dashboard_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📊 Dashboard", callback_data="a_dash"),
         InlineKeyboardButton(text="👥 Users", callback_data="a_users")],
        [InlineKeyboardButton(text="🔐 FSub Manager", callback_data="a_fsub"),
         InlineKeyboardButton(text="⚙️ React Settings", callback_data="a_react")],
        [InlineKeyboardButton(text="🤖 Bot Manager", callback_data="a_bots"),
         InlineKeyboardButton(text="🎨 Texts & UI", callback_data="a_texts")],
        [InlineKeyboardButton(text="📢 Broadcast", callback_data="a_brd"),
         InlineKeyboardButton(text="📋 Logs", callback_data="a_logs")],
        [InlineKeyboardButton(text="🔧 Maintenance", callback_data="a_maint"),
         InlineKeyboardButton(text="🚨 Stop Engine", callback_data="a_estop")],
        [InlineKeyboardButton(text="🏠 Back Home", callback_data="home")]
    ])

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    if message.chat.type != 'private': return
    try:
        async with async_session() as session:
            result = await session.execute(select(User).where(User.telegram_id == message.from_user.id))
            if not result.scalar_one_or_none():
                session.add(User(telegram_id=message.from_user.id, username=message.from_user.username))
                await session.commit()
    except: pass
    
    bot_info = await main_bot.get_me()
    safe_name = bot_info.username.replace('_', '\\_')
    text = db["texts"]["welcome"].replace("{name}", message.from_user.first_name).replace("{bot_username}", safe_name).replace("{owner}", OWNER_USERNAME.replace('_', '\\_'))
    await message.answer(text, reply_markup=get_user_menu(message.from_user.id))

@dp.callback_query(F.data.in_(["u_ch_react", "u_gr_react"]))
async def bot_list_grid(callback: types.CallbackQuery):
    t = "Channel" if callback.data == "u_ch_react" else "Group"
    param = "startchannel=start" if callback.data == "u_ch_react" else "startgroup=start"
    
    text = f"🤖 **{t} 𝗥𝗲𝗮𝗰𝘁𝗶𝗼𝗻 𝗕𝗼𝘁𝘀**\n━━━━━━━━━━━━━━━━━━━━\n✅ Add all bots to your {t} and make them Admin 🔰\n\n"
    
    # User wanted exactly this design grid (4 items per row)
    markup = InlineKeyboardMarkup(inline_keyboard=[])
    row = []
    
    for i in range(1, 21):
        num = "" if i == 1 else str(i)
        bot_uname = f"slk_autoreaction{num}_Bot"
        safe_uname = bot_uname.replace('_', '\\_')
        text += f"**{i}.** [@{safe_uname}](https://t.me/{bot_uname})\n"
        
        row.append(InlineKeyboardButton(text=f"Add ({i})", url=f"https://t.me/{bot_uname}?{param}"))
        if len(row) == 4:
            markup.inline_keyboard.append(row)
            row = []
            
    if row: markup.inline_keyboard.append(row)
    
    # Adding Father Bot button at the bottom
    main_info = await main_bot.get_me()
    markup.inline_keyboard.append([InlineKeyboardButton(text="✅ Add Main Bot (Father)", url=f"https://t.me/{main_info.username}?{param}")])
    markup.inline_keyboard.append([InlineKeyboardButton(text="🔙 Back to Menu", callback_data="home")])
    
    await callback.message.edit_text(text, reply_markup=markup)

@dp.callback_query(F.data == "home")
async def go_home(callback: types.CallbackQuery):
    bot_info = await main_bot.get_me()
    text = db["texts"]["welcome"].replace("{name}", callback.from_user.first_name).replace("{bot_username}", bot_info.username.replace('_','\\_')).replace("{owner}", OWNER_USERNAME.replace('_','\\_'))
    await callback.message.edit_text(text, reply_markup=get_user_menu(callback.from_user.id))

@dp.callback_query(F.data == "open_admin")
async def open_admin_panel(callback: types.CallbackQuery):
    if is_admin(callback.from_user.id):
        await callback.message.edit_text("👑 **𝗣𝗥𝗘𝗠𝗜𝗨𝗠 𝗔𝗗𝗠𝗜𝗡 𝗗𝗔𝗦𝗛𝗕𝗢𝗔𝗥𝗗** 👑\n━━━━━━━━━━━━━━━━━━━━\nSelect an option below to manage your Mega Bot:", reply_markup=admin_dashboard_menu())

@dp.callback_query(F.data == "a_dash")
async def admin_dash(callback: types.CallbackQuery):
    if not is_admin(callback.from_user.id): return
    st = db["stats"]
    text = f"📊 **𝗦𝘆𝘀𝘁𝗲𝗺 𝗗𝗮𝘀𝗵𝗯𝗼𝗮𝗿𝗱**\n━━━━━━━━━━━━━━━━━━━━\n👥 Total Users: {len(db['users'])}\n\n✅ Reactions Success: {st['success']}\n❌ Reactions Failed: {st['failed']}\n📨 Messages Processed: {st['messages_processed']}\n\n🚨 Emergency Stop: {'ON 🔴' if db['settings']['emergency_stop'] else 'OFF 🟢'}"
    await callback.message.edit_text(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🔙 Back to Panel", callback_data="open_admin")]]))

@dp.callback_query(F.data == "a_react")
async def admin_react(callback: types.CallbackQuery):
    if not is_admin(callback.from_user.id): return
    set = db["settings"]
    text = f"⚙️ **𝗥𝗲𝗮𝗰𝘁𝗶𝗼𝗻 𝗦𝗲𝘁𝘁𝗶𝗻𝗴𝘀**\n━━━━━━━━━━━━━━━━━━━━\nStatus: {'Enabled ✅' if set['reaction_enabled'] else 'Disabled ❌'}\nOrder: {'Random 🔀' if set['random_order'] else 'Fixed 🔢'}\nDelay: {set['min_delay']}s - {set['max_delay']}s\nEmojis: {''.join(set['emojis'])}"
    m = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔀 Toggle Order", callback_data="tog_order"),
         InlineKeyboardButton(text="⏯ Toggle Status", callback_data="tog_react")],
        [InlineKeyboardButton(text="🔙 Back to Panel", callback_data="open_admin")]
    ])
    await callback.message.edit_text(text, reply_markup=m)

@dp.callback_query(F.data == "tog_order")
async def tog_order(callback: types.CallbackQuery):
    db["settings"]["random_order"] = not db["settings"]["random_order"]
    save_data(db); await admin_react(callback)

@dp.callback_query(F.data == "tog_react")
async def tog_react(callback: types.CallbackQuery):
    db["settings"]["reaction_enabled"] = not db["settings"]["reaction_enabled"]
    save_data(db); await admin_react(callback)

@dp.callback_query(F.data == "a_logs")
async def a_logs(callback: types.CallbackQuery):
    if not is_admin(callback.from_user.id): return
    logs = "\n".join(db["logs"][:20]) if db["logs"] else "No logs."
    await callback.message.edit_text(f"📋 **𝗦𝘆𝘀𝘁𝗲𝗺 𝗟𝗼𝗴𝘀 (Exact Errors)**\n━━━━━━━━━━━━━━━━━━━━\n`{logs}`", reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🔙 Back to Panel", callback_data="open_admin")]]))

# ================= 6. TERABOX DOWNLOADER =================
@dp.callback_query(F.data == "menu_download")
async def handle_menu_download(callback: types.CallbackQuery):
    await callback.message.reply("🔗 **Please send me a valid TeraBox share link to download.**")
    await callback.answer()

@dp.message(F.text.startswith("http"))
async def handle_link(message: types.Message):
    url = message.text
    msg = await message.answer("🔍 **Validating and Analyzing Media... ⏳**")
    
    # RapidAPI Fetch Logic
    api_url = "https://terabox-downloader-direct-download-link-generator.p.rapidapi.com/fetch"
    payload = {"url": url}
    headers = {
        "x-rapidapi-key": "81612a03f7msh9343986d4544d64p1f3741jsn3e7c72cdbfc8",
        "x-rapidapi-host": "terabox-downloader-direct-download-link-generator.p.rapidapi.com",
        "Content-Type": "application/json"
    }

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(api_url, json=payload, headers=headers)
            if response.status_code == 200:
                data = response.json()
                
                # Smart find link
                dl = None
                for k, v in data.items():
                    if isinstance(v, str) and v.startswith("http") and "link" in k.lower():
                        dl = v; break
                        
                if dl:
                    text = f"✅ **Media Found!**\n\nChoose an option below:"
                    await msg.edit_text(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                        [InlineKeyboardButton(text="📥 Start Download", url=dl)],
                        [InlineKeyboardButton(text="❌ Cancel", callback_data="home")]
                    ]))
                    return
    except: pass
    await msg.edit_text("❌ **Failed to fetch video!**\nThe API server might be busy or the link is private.")

# ================= 7. FASTAPI SERVER FOR RENDER =================
@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Initializing Database...")
    await init_db()
    logging.info("Starting Telegram Bot...")
    await main_bot.delete_webhook(drop_pending_updates=True) 
    asyncio.create_task(dp.start_polling(main_bot))
    yield
    logging.info("Shutting down bot...")
    await main_bot.session.close()

for client_obj in react_clients:
    # Ensure background bots are closed properly too
    pass

app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {"status": "TeraBox & React Premium Bot is Running perfectly! 🚀"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
