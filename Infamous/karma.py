# https://github.com/Infamous-Hydra/YaeMiko
# https://github.com/Team-ProjectCodeX
# https://t.me/O_okarma

# <============================================== IMPORTS =========================================================>
from pyrogram.types import InlineKeyboardButton as ib
from telegram import InlineKeyboardButton

from Mikobot import BOT_USERNAME, OWNER_ID, SUPPORT_CHAT

# <============================================== CONSTANTS =========================================================>
START_IMG = [
    "https://i.ibb.co/gSGYb16/e1a5590de05a.jpg",
    "https://i.ibb.co/WHTZ11T/1990095beff7.jpg", 
]

HEY_IMG = ""

ALIVE_ANIMATION = [
    "https://i.ibb.co/bFmcWpr/27083990ab27.jpg",
    "https://i.ibb.co/R3s3r4F/8a5bf7d8594d.jpg",
    "https://i.ibb.co/QK1zhw3/156005c2e6cb.jpg",
    "https://i.ibb.co/LNbs292/8c6b814576f3.jpg",
]


PM_START_TEXT = "✨ *𝐊𝐨𝐧𝐧𝐢𝐜𝐡𝐢𝐰𝐚!!, {mention}*" 

•𝐌𝐲 𝐈𝐧𝐟𝐨  ➲  Iᴛ's ᴍᴇ Osᴀᴍᴜ Dᴀᴢᴀɪ, ᴀɴ ᴀɴɪᴍᴇ ᴛʜᴇᴍᴇᴅ ᴀᴅᴠᴀɴᴄᴇ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ ʙᴏᴛ.

•𝐌𝐲 𝐉𝐨𝐛  ➲ I ᴀᴍ ᴛʜᴇ ᴜʟᴛɪᴍᴀᴛᴇ ɢʀᴏᴜᴘ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ ʙᴏᴛ . Mʏ ᴍᴏᴅᴜʟᴇs ᴀɴᴅ ғᴜɴᴄᴛɪᴏɴs ᴀʀᴇ ᴘᴇʀғᴇᴄᴛ ғᴏʀ ᴋᴇᴇᴘɪɴɢ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴏʀɢᴀɴɪᴢᴇᴅ, ᴇɴɢᴀɢᴇᴅ, ᴀɴᴅ sᴘᴀᴍ-ғʀᴇᴇ!

• Cʟɪᴄᴋ ᴏɴ ᴛʜᴇ ʙᴜᴛᴛᴏɴ ʙᴇʟᴏᴡ ғᴏʀ ᴍᴏʀᴇ ɪɴғᴏʀᴍᴀᴛɪᴏɴ*"

START_BTN = [
    [
        InlineKeyboardButton(
            text="⇦ ADD ME ⇨",
            url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
        ),
    ],
    [
        InlineKeyboardButton(text="HELP", callback_data="extra_command_handler"),
    ],
    [
        InlineKeyboardButton(text="DETAILS", callback_data="Miko_"),
        InlineKeyboardButton(text="SOURCE", callback_data="git_source"),
    ],
    [
        InlineKeyboardButton(text="CREATOR", url=f"tg://user?id={OWNER_ID}"),
    ],
]

GROUP_START_BTN = [
    [
        InlineKeyboardButton(
            text="⇦ ADD ME ⇨",
            url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
        ),
    ],
    [
        InlineKeyboardButton(text="SUPPORT", url=f"https://t.me/{SUPPORT_CHAT}"),
        InlineKeyboardButton(text="CREATOR", url=f"tg://user?id={OWNER_ID}"),
    ],
]

ALIVE_BTN = [
    [
        ib(text="UPDATES", url="https://t.me/Dazai_Updates"),
        ib(text="SUPPORT", url="https://t.me/Team7_Support_chats"),
    ],
    [
        ib(
            text="⇦ ADD ME ⇨",
            url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
        ),
    ],
]

HELP_STRINGS = """
🫧 *Yae-Miko* 🫧 [ㅤ](https://telegra.ph/file/b05535884267a19ee5c93.jpg)

☉ *Here, you will find a list of all the available commands.*

ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅs ᴄᴀɴ ʙᴇ ᴜsᴇᴅ ᴡɪᴛʜ : /
"""
