# https://github.com/Infamous-Hydra/YaeMiko
# https://github.com/Team-ProjectCodeX


import json
import os


def get_user_list(config, key):
    with open("{}/Mikobot/{}".format(os.getcwd(), config), "r") as json_file:
        return json.load(json_file)[key]


class Config(object):
    # Configuration class for the bot

    # Enable or disable logging
    LOGGER = True

    # <================================================ REQUIRED ======================================================>
    # Telegram API configuration
    API_ID = "9552179" # Get this value from my.telegram.org/apps
    API_HASH = "fa6e0313afd8259094486d3256242102"

    # Database configuration (PostgreSQL)
    DATABASE_URL = "postgresql://postgresql://Marinjiprobot:fRcGmtNf9yWl6r_QeMZwqg@plush-jindo-4839.j77.aws-eu-west-1.cockroachlabs.cloud:26257/defaultdb?sslmode=verify-full:fRcGmtNf9yWl6r_QeMZwqg@plush-jindo-4839.j77.aws-eu-west-1.cockroachlabs.cloud:26257/defaultdb?sslmode=verify-full"

    # Event logs chat ID and message dump chat ID
    EVENT_LOGS = -1001972158659
    MESSAGE_DUMP = -1001706506258

    # MongoDB configuration
    MONGO_DB_URI = "mongodb+srv://Dazai819191:darai_roxbot001@dazai.tw3iy.mongodb.net/?retryWrites=true&w=majority&appName=Dazai"

    # Support chat and support ID
    SUPPORT_CHAT = "Team7_Support_chats"
    SUPPORT_ID = -1001706506258

    # Database name
    DB_NAME = "Marinjiprobot"
    TOKEN = "6257629560:AAHi9FSlPQ5LlQWH8bs9Q_hdsBOY0zSxMXY"  # Get bot token from @BotFather on Telegram

    # Owner's Telegram user ID (Must be an integer)
    OWNER_ID = 1327021082
    # <=======================================================================================================>

    # <================================================ OPTIONAL ======================================================>
    # Optional configuration fields

    # List of groups to blacklist
    BL_CHATS = []

    # User IDs of sudo users, dev users, support users, tiger users, and whitelist users
    DRAGONS = get_user_list("elevated_users.json", "sudos")
    DEV_USERS = get_user_list("elevated_users.json", "devs")
    DEMONS = get_user_list("elevated_users.json", "supports")
    TIGERS = get_user_list("elevated_users.json", "tigers")
    WOLVES = get_user_list("elevated_users.json", "whitelists")

    # Toggle features
    ALLOW_CHATS = True
    ALLOW_EXCL = True
    DEL_CMDS = True
    INFOPIC = True

    # Modules to load or exclude
    LOAD = []
    NO_LOAD = []

    # Global ban settings
    STRICT_GBAN = True
    BAN_STICKER = (
        "CAACAgUAAxkBAAEGWC5lloYv1tiI3-KPguoH5YX-RveWugACoQ4AAi4b2FQGdUhawbi91DQE"
    )

    # Temporary download directory
    TEMP_DOWNLOAD_DIRECTORY = "./"
    # <=======================================================================================================>


# <=======================================================================================================>


class Production(Config):
    # Production configuration (inherits from Config)

    # Enable or disable logging
    LOGGER = True


class Development(Config):
    # Development configuration (inherits from Config)

    # Enable or disable logging
    LOGGER = True
