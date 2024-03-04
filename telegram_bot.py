import json
import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Protocol

from telegram import Update
from telegram.ext import Application, ContextTypes, MessageHandler
from telegram.ext.filters import BaseFilter

import business


class JsonFilter(BaseFilter):
    """
    Фильтр для нахождения JSON-сообщений
    """

    def __init__(self, expected_keys: list[str]):
        self.expected_keys = expected_keys

    def filter(self, message):
        try:
            data = json.loads(message.text)
        except ValueError:
            return False

        if isinstance(data, dict):
            for key in self.expected_keys:
                if key not in data:
                    return False
            return True


@dataclass
class ParsedMessage:
    group_type: str
    dt_from: datetime
    dt_upto: datetime


class DataGetter(Protocol):
    async def get_data(self, from_: datetime, to: datetime) -> business.Data: ...


class TelegramBot:
    """
    Класс телеграм бота, выполняющего агрегацию
    """

    def __init__(self, token: str, data_getter: DataGetter):
        self.data_getter = data_getter
        self.application = Application.builder().token(token).build()

        get_aggregated_data_filter = JsonFilter(
            expected_keys=["group_type", "dt_from", "dt_upto"]
        )
        self.application.add_handler(
            MessageHandler(get_aggregated_data_filter, self.get_aggregated_data)
        )

    def run(self):
        logging.basicConfig(
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            level=logging.ERROR,
        )
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)

    async def get_aggregated_data(
        self, update: Update, _: ContextTypes.DEFAULT_TYPE
    ) -> None:
        if update.message == None or update.message.text == None:
            return

        inp = self.parse_input(update.message.text)
        try:
            result = await self.data_getter.get_data(inp.dt_from, inp.dt_upto)
        except Exception as e:
            await update.message.reply_text(
                f"Не получилось взять данные из MongoDB: {e}"
            )
            return

        aggregator = business.Aggregator(by=inp.group_type)
        data = aggregator.aggregate(business.Data(result.rows))

        await update.message.reply_text(self.create_response(data))

    def parse_input(self, message_text) -> ParsedMessage:
        json_data = json.loads(message_text)
        dt_from = datetime.fromisoformat(json_data["dt_from"])
        dt_upto = datetime.fromisoformat(json_data["dt_upto"])
        group_type = json_data["group_type"]
        return ParsedMessage(group_type, dt_from, dt_upto)

    def create_response(self, data: business.Data) -> str:
        dataset = []
        labels = []

        for row in data.rows:
            dataset.append(row.price)
            labels.append(datetime.isoformat(row.date))

        bot_json_response = {"dataset": dataset, "labels": labels}
        return json.dumps(bot_json_response, default=str)
