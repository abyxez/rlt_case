import asyncio
import json
import os
from datetime import datetime

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Filter
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from dotenv import load_dotenv

import business
from database import MongoDB

load_dotenv()

mongo_uri = os.getenv("MONGO_URL")
database_name = os.getenv("MONGO_DATABASE_NAME")
collection_name = os.getenv("MONGO_COLLECTION_NAME")
bot_token = os.getenv("BOT_TOKEN")


class JSONFilter(Filter):
    """
    Фильтр для нахождения JSON-сообщений.
    """

    def __init__(self, start_text: str, end_text: str) -> None:
        self.start_text = start_text
        self.end_text = end_text

    async def __call__(self, message: Message) -> bool:
        if message.text is None:
            return False

        return message.text.startswith(self.start_text) and message.text.endswith(
            self.end_text
        )


dispatcher = Dispatcher()

bot = Bot(token=bot_token)
aggregator = business.Aggregator()
db = MongoDB(database_name, mongo_uri, collection_name)


async def command_start_handler(message: Message) -> None:
    """
    Приветственная функция для команды /start
    """
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")


@dispatcher.message(JSONFilter("{", "}"))
async def handle_json(message: types.Message):
    """
    Основная функция, обрабатывающая JSON запросы в чате с ботом.
    """
    json_data = json.loads(message.text)
    dt_from = datetime.fromisoformat(json_data["dt_from"])
    dt_upto = datetime.fromisoformat(json_data["dt_upto"])
    group_type = json_data["group_type"]

    try:
        result = await db.get_data(dt_from, dt_upto)
    except Exception as e:
        await message.answer(f"Не получилось взять данные из монги: {e}")

    aggregator = business.Aggregator(by=group_type)
    data = aggregator.aggregate(business.Data(result.rows))

    dataset = []
    labels = []

    for row in data.rows:
        dataset.append(row.price)
        labels.append(datetime.isoformat(row.date))

    bot_json_response = {"dataset": dataset, "labels": labels}

    await message.answer(json.dumps(bot_json_response, default=str))


async def go():
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(go())
