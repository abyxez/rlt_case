import os
from dotenv import load_dotenv
from database import MongoDB
from telegram_bot import TelegramBot

load_dotenv()


def main():
    mongo_uri = os.getenv("MONGO_URL")
    if mongo_uri == None:
        raise Exception('add "mongo_url" to env')

    database_name = os.getenv("MONGO_DATABASE_NAME")
    if database_name == None:
        raise Exception('add "MONGO_DATABASE_NAME" to env')

    collection_name = os.getenv("MONGO_COLLECTION_NAME")
    if collection_name == None:
        raise Exception('add "MONGO_COLLECTION_NAME" to env')

    bot_token = os.getenv("BOT_TOKEN")
    if bot_token == None:
        raise Exception('add "BOT_TOKEN" to env')

    mongo_db = MongoDB(database_name, mongo_uri, collection_name)
    telegram_bot = TelegramBot(bot_token, mongo_db)

    telegram_bot.run()


main()
