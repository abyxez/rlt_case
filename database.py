from datetime import datetime

from motor.motor_asyncio import AsyncIOMotorClient

from business import Data, Row

# from pymongo import MongoClient


class MongoDB:
    def __init__(self, db_name, mongo_uri, collection_name):
        cluster = AsyncIOMotorClient(mongo_uri)
        database = cluster[db_name]
        self.collection = database[collection_name]

    async def get_data(self, from_: datetime, to: datetime) -> Data:
        # Формируем запрос к базе данных
        # поменять
        query = {"dt": {"$gte": from_, "$lte": to}}
        documents = self.collection.find(query)

        rows = []
        values = []
        dates = []
        async for doc in documents:
            # values.append(value=doc['value'])
            # dates.append(date=doc['dt'])
            rows.append(Row(price=doc["value"], date=doc["dt"]))
        # Преобразуем документы в объекты Row
        # Если формат верный, то подойдет код, если нет, то нет.
        # print(values, dates)

        return Data(rows=rows)
