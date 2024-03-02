import asyncio
import os

from aiogram import Bot

from database import MongoDB


def main():
    mongo_uri = os.getenv("MONGO_URL")
    database_name = os.getenv("MONGO_DATABASE_NAME")
    collection_name = os.getenv("MONGO_COLLECTION_NAME")
    bot_token = os.getenv("BOT_TOKEN")

    # connect, collection ...
    mongo_db = MongoDB(database_name, collection_name, mongo_uri)
    telegram_bot = Bot(bot_token, mongo_db)

    asyncio.run(telegram_bot.run())


main()
