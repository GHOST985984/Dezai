# https://github.com/Infamous-Hydra/YaeMiko
# https://github.com/Team-ProjectCodeX

# <============================================== IMPORTS =========================================================>
import asyncio
import contextlib
import importlib
import json
import re
import time
import traceback
from platform import python_version
from random import choice

import psutil
import pyrogram
import telegram
import telethon
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.error import (
    BadRequest,
    ChatMigrated,
    Forbidden,
    NetworkError,
    TelegramError,
    TimedOut,
)
from telegram.ext import (
    ApplicationHandlerStop,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
from telegram.helpers import escape_markdown

from Infamous.karma import *
from Mikobot import (
    BOT_NAME,
    LOGGER,
    OWNER_ID,
    SUPPORT_CHAT,
    TOKEN,
    StartTime,
    app,
    dispatcher,
    function,
    loop,
    tbot,
)
from Mikobot.plugins import ALL_MODULES
from Mikobot.plugins.helper_funcs.chat_status import is_user_admin
from Mikobot.plugins.helper_funcs.misc import paginate_modules

# <=======================================================================================================>

PYTHON_VERSION = python_version()
PTB_VERSION = telegram.__version__
PYROGRAM_VERSION = pyrogram.__version__
TELETHON_VERSION = telethon.__version__


# <============================================== FUNCTIONS =========================================================>
def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "

    time_list.reverse()
    ping_time += ":".join(time_list)

    return ping_time


IMPORTED = {}
MIGRATEABLE = []
HELPABLE = {}
STATS = []
USER_INFO = []
DATA_IMPORT = []
DATA_EXPORT = []
CHAT_SETTINGS = {}
USER_SETTINGS = {}

for module_name in ALL_MODULES:
    imported_module = importlib.import_module("Mikobot.plugins." + module_name)
    if not hasattr(imported_module, "__mod_name__"):
        imported_module.__mod_name__ = imported_module.__name__

    if imported_module.__mod_name__.lower() not in IMPORTED:
        IMPORTED[imported_module.__mod_name__.lower()] = imported_module
    else:
        raise Exception("Can't have two modules with the same name! Please change one")

    if hasattr(imported_module, "__help__") and imported_module.__help__:
        HELPABLE[imported_module.__mod_name__.lower()] = imported_module

    # Chats to migrate on chat_migrated events
    if hasattr(imported_module, "__migrate__"):
        MIGRATEABLE.append(imported_module)

    if hasattr(imported_module, "__stats__"):
        STATS.append(imported_module)

    if hasattr(imported_module, "__user_info__"):
        USER_INFO.append(imported_module)

    if hasattr(imported_module, "__import_data__"):
        DATA_IMPORT.append(imported_module)

    if hasattr(imported_module, "__export_data__"):
        DATA_EXPORT.append(imported_module)

    if hasattr(imported_module, "__chat_settings__"):
        CHAT_SETTINGS[imported_module.__mod_name__.lower()] = imported_module

    if hasattr(imported_module, "__user_settings__"):
        USER_SETTINGS[imported_module.__mod_name__.lower()] = imported_module


# do not async
async def send_help(chat_id, text, keyboard=None):
    if not keyboard:
        keyboard = InlineKeyboardMarkup(paginate_modules(0, HELPABLE, "help"))
    await dispatcher.bot.send_message(
        chat_id=chat_id,
        text=text,
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True,
        reply_markup=keyboard,
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    message = update.effective_message
    uptime = get_readable_time((time.time() - StartTime))
    if update.effective_chat.type == "private":
        if len(args) >= 1:
            if args[0].lower() == "help":
                await send_help(update.effective_chat.id, HELP_STRINGS)
            elif args[0].lower().startswith("ghelp_"):
                mod = args[0].lower().split("_", 1)[1]
                if not HELPABLE.get(mod, False):
                    return
                await send_help(
                    update.effective_chat.id,
                    HELPABLE[mod].__help__,
                    InlineKeyboardMarkup(
                        [[InlineKeyboardButton(text="◁", callback_data="help_back")]]
                    ),
                )

            elif args[0].lower() == "markdownhelp":
                IMPORTED["exᴛʀᴀs"].markdown_help_sender(update)
            elif args[0].lower().startswith("stngs_"):
                match = re.match("stngs_(.*)", args[0].lower())
                chat = dispatcher.bot.getChat(match.group(1))

                if is_user_admin(chat, update.effective_user.id):
                    send_settings(match.group(1), update.effective_user.id, False)
                else:
                    send_settings(match.group(1), update.effective_user.id, True)

            elif args[0][1:].isdigit() and "rules" in IMPORTED:
                await IMPORTED["rules"].send_rules(update, args[0], from_pm=True)

        else:
            first_name = update.effective_user.first_name
            lol = await message.reply_photo(
                photo=str(choice(START_IMG)),
                caption=FIRST_PART_TEXT.format(escape_markdown(first_name)),
                parse_mode=ParseMode.MARKDOWN,
            )
            await asyncio.sleep(0.2)
            guu = await update.effective_message.reply_text("🐾")
            await asyncio.sleep(1.8)
            await guu.delete()  # Await this line
            await update.effective_message.reply_text(
                PM_START_TEXT,
                reply_markup=InlineKeyboardMarkup(START_BTN),
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=False,
            )
    else:
        await message.reply_photo(
            photo=str(choice(START_IMG)),
            reply_markup=InlineKeyboardMarkup(GROUP_START_BTN),
            caption="<b>I am Alive!</b>\n\n<b>Since:</b> <code>{}</code>".format(
                uptime
            ),
            parse_mode=ParseMode.HTML,
        )


async def extra_command_handlered(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [
            InlineKeyboardButton("MANAGEMENT", callback_data="help_back"),
            InlineKeyboardButton("AI", callback_data="ai_command_handler"),
        ],
        [
            InlineKeyboardButton("ANIME", callback_data="anime_command_handler"),
            InlineKeyboardButton("GENSHIN", callback_data="genshin_command_handler"),
        ],
        [
            InlineKeyboardButton("HOME", callback_data="Miko_back"),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "𝙎𝙚𝙡𝙚𝙘𝙩 𝙩𝙝𝙚 [𝙨𝙚𝙘𝙩𝙞𝙤𝙣](https://telegra.ph/file/8c092f4e9d303f9497c83.jpg) 𝙩𝙝𝙖𝙩 𝙮𝙤𝙪 𝙬𝙖𝙣𝙩 𝙩𝙤 𝙤𝙥𝙚𝙣",
        reply_markup=reply_markup,
        parse_mode="Markdown",
    )


async def extra_command_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query.data == "extra_command_handler":
        await query.answer()  # Use 'await' for asynchronous calls
        await query.message.edit_text(
            "𝙎𝙚𝙡𝙚𝙘𝙩 𝙩𝙝𝙚 [𝙨𝙚𝙘𝙩𝙞𝙤𝙣](https://telegra.ph/file/8c092f4e9d303f9497c83.jpg) 𝙩𝙝𝙖𝙩 𝙮𝙤𝙪 𝙬𝙖𝙣𝙩 𝙩𝙤 𝙤𝙥𝙚𝙣",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("MANAGEMENT", callback_data="help_back"),
                        InlineKeyboardButton("AI", callback_data="ai_command_handler"),
                    ],
                    [
                        InlineKeyboardButton(
                            "ANIME", callback_data="anime_command_handler"
                        ),
                        InlineKeyboardButton(
                            "GENSHIN", callback_data="genshin_command_handler"
                        ),
                    ],
                    [
                        InlineKeyboardButton("HOME", callback_data="Miko_back"),
                    ],
                ]
            ),
            parse_mode="Markdown",  # Added this line to explicitly specify Markdown parsing
        )


async def ai_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("AI", callback_data="ai_handler"),
            InlineKeyboardButton("IMAGEGEN", callback_data="more_aihandlered"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🧠 *Here are the options for* [𝗬𝗔𝗘 𝗠𝗜𝗞𝗢](https://telegra.ph/file/ed2d9c3693cacc9b0464e.jpg):",
        reply_markup=reply_markup,
        parse_mode="Markdown",
    )


async def ai_command_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query.data == "ai_command_handler":
        await query.answer()
        await query.message.edit_text(
            "🧠 *Here are the options for* [𝗬𝗔𝗘 𝗠𝗜𝗞𝗢](https://telegra.ph/file/ed2d9c3693cacc9b0464e.jpg):",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("AI", callback_data="ai_handler"),
                        InlineKeyboardButton(
                            "IMAGEGEN", callback_data="more_aihandlered"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            "» 𝘽𝘼𝘾𝙆 «", callback_data="extra_command_handler"
                        ),
                    ],
                ]
            ),
            parse_mode="Markdown",
        )


async def ai_handler_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query.data == "ai_handler":
        await query.answer()
        await query.message.edit_text(
            "[𝗔𝗿𝘁𝗶𝗳𝗶𝗰𝗶𝗮𝗹 𝗜𝗻𝘁𝗲𝗹𝗹𝗶𝗴𝗲𝗻𝘁 𝗙𝘂𝗻𝗰𝘁𝗶𝗼𝗻𝘀](https://telegra.ph/file/01a2e0cd1b9d03808c546.jpg):\n\n"
            "All Commands:\n"
            "➽ /askgpt <write query>: A chatbot using GPT for responding to user queries.\n\n"
            "➽ /palm <write prompt>: Performs a Palm search using a chatbot.\n\n"
            "➽ /upscale <reply to image>: Upscales your image quality.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "More Image Gen ➪", callback_data="more_ai_handler"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            "⇦ BACK", callback_data="ai_command_handler"
                        ),
                    ],
                ],
            ),
            parse_mode="Markdown",
        )


async def more_ai_handler_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query.data == "more_ai_handler":
        await query.answer()
        await query.message.edit_text(
            "*Here's more image gen related commands*:\n\n"
            "Command: /meinamix\n"
            "  • Description: Generates an image using the meinamix model.\n\n"
            "Command: /darksushi\n"
            "  • Description: Generates an image using the darksushi model.\n\n"
            "Command: /meinahentai\n"
            "  • Description: Generates an image using the meinahentai model.\n\n"
            "Command: /darksushimix\n"
            "  • Description: Generates an image using the darksushimix model.\n\n"
            "Command: /anylora\n"
            "  • Description: Generates an image using the anylora model.\n\n"
            "Command: /cetsumix\n"
            "  • Description: Generates an image using the cetsumix model.\n\n"
            "Command: /anything\n"
            "  • Description: Generates an image using the anything model.\n\n"
            "Command: /absolute\n"
            "  • Description: Generates an image using the absolute model.\n\n"
            "Command: /darkv2\n"
            "  • Description: Generates an image using the darkv2 model.\n\n"
            "Command: /creative\n"
            "  • Description: Generates an image using the creative model.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("⇦ BACK", callback_data="ai_handler"),
                    ],
                ],
            ),
        )


async def more_aihandlered_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query.data == "more_aihandlered":
        await query.answer()
        await query.message.edit_text(
            "*Here's more image gen related commands*:\n\n"
            "*Command*: /meinamix\n"
            "  • Description: Generates an image using the meinamix model.\n\n"
            "*Command*: /darksushi\n"
            "  • Description: Generates an image using the darksushi model.\n\n"
            "*Command*: /meinahentai\n"
            "  • Description: Generates an image using the meinahentai model.\n\n"
            "*Command*: /darksushimix\n"
            "  • Description: Generates an image using the darksushimix model.\n\n"
            "*Command*: /anylora\n"
            "  • Description: Generates an image using the anylora model.\n\n"
            "*Command*: /cetsumix\n"
            "  • Description: Generates an image using the cetsumix model.\n\n"
            "*Command*: /anything\n"
            "  • Description: Generates an image using the anything model.\n\n"
            "*Command*: /absolute\n"
            "  • Description: Generates an image using the absolute model.\n\n"
            "*Command*: /darkv2\n"
            "  • Description: Generates an image using the darkv2 model.\n\n"
            "*Command*: /creative\n"
            "  • Description: Generates an image using the creative model.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "⇦ BACK", callback_data="ai_command_handler"
                        ),
                    ],
                ],
            ),
        )


async def anime_command_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query.data == "anime_command_handler":
        await query.answer()
        await query.message.edit_text(
            "⛩[𝗔𝗻𝗶𝗺𝗲 𝗨𝗽𝗱𝗮𝘁𝗲𝘀](https://telegra.ph//file/59d93fede8bf12fec1a51.jpg) :\n\n"
            "**╔ /anime: **fetches info on single anime (includes buttons to look up for prequels and sequels)\n"
            "**╠ /character: **fetches info on multiple possible characters related to query\n"
            "**╠ /manga: **fetches info on multiple possible mangas related to query\n"
            "**╠ /airing: **fetches info on airing data for anime\n"
            "**╠ /studio: **fetches info on multiple possible studios related to query\n"
            "**╠ /schedule: **fetches scheduled animes\n"
            "**╠ /browse: **get popular, trending or upcoming animes\n"
            "**╠ /top: **to retrieve top animes for a genre or tag\n"
            "**╠ /watch: **fetches watch order for anime series\n"
            "**╠ /fillers: **to get a list of anime fillers\n"
            "**╠ /gettags: **get a list of available tags\n"
            "**╠ /animequotes: **get random anime quotes\n"
            "**╚ /getgenres: **Get list of available Genres\n\n"
            "**⚙️ Group Settings:**\n"
            "**╔**\n"
            "**╠ /anisettings: **to toggle NSFW lock and airing notifications and other settings in groups (anime news)\n"
            "**╚**",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("More Info", url="https://anilist.co/"),
                        InlineKeyboardButton(
                            "㊋Infamous•Hydra", url="https://t.me/Infamous_Hydra"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            "» 𝘽𝘼𝘾𝙆 «", callback_data="extra_command_handler"
                        ),
                    ],
                ]
            ),
            parse_mode="Markdown",  # Added this line to explicitly specify Markdown parsing
        )


async def genshin_command_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query.data == "genshin_command_handler":
        await query.answer()
        await query.message.edit_text(
            "⛩ [𝗚𝗲𝗻𝘀𝗵𝗶𝗻 𝗜𝗺𝗽𝗮𝗰𝘁](https://telegra.ph/file/cd03348a4a357624e70db.jpg) ⛩\n\n"
            "*UNDER DEVELOPMENT*",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "More Info", url="https://genshin.mihoyo.com/"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            "» 𝘽𝘼𝘾𝙆 «", callback_data="extra_command_handler"
                        ),
                    ],
                ]
            ),
            parse_mode="Markdown",  # Added this line to explicitly specify Markdown parsing
        )


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Log the error and send a telegram message to notify the developer."""
    # Log the error before we do anything else, so we can see it even if something breaks.
    LOGGER.error(msg="Exception while handling an update:", exc_info=context.error)

    # traceback.format_exception returns the usual python message about an exception, but as a
    # list of strings rather than a single string, so we have to join them together.
    tb_list = traceback.format_exception(
        None, context.error, context.error.__traceback__
    )
    tb = "".join(tb_list)

    # Build the message with some markup and additional information about what happened.
    message = (
        "An exception was raised while handling an update\n"
        "<pre>update = {}</pre>\n\n"
        "<pre>{}</pre>"
    ).format(
        html.escape(json.dumps(update.to_dict(), indent=2, ensure_ascii=False)),
        html.escape(tb),
    )

    if len(message) >= 4096:
        message = message[:4096]
    # Finally, send the message
    await context.bot.send_message(
        chat_id=OWNER_ID, text=message, parse_mode=ParseMode.HTML
    )


# for test purposes
async def error_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    error = context.error
    try:
        raise error
    except Forbidden:
        print("no nono1")
        print(error)
        # remove update.message.chat_id from conversation list
    except BadRequest:
        print("no nono2")
        print("BadRequest caught")
        print(error)

        # handle malformed requests - read more below!
    except TimedOut:
        print("no nono3")
        # handle slow connectio
