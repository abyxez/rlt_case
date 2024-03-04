from datetime import datetime

from motor.motor_asyncio import AsyncIOMotorClient

from business import Data, Row


class MongoDB:
    """
    Класс описывает работу MongoDB
    """

    def __init__(self, db_name: str, mongo_uri: str, collection_name: str):
        cluster = AsyncIOMotorClient(mongo_uri)
        database = cluster[db_name]
        self.collection = database[collection_name]

    async def get_data(self, from_: datetime, to: datetime) -> Data:
        query = {"dt": {"$gte": from_, "$lte": to}}
        documents = self.collection.find(query)

        rows = []
        async for doc in documents:
            rows.append(Row(price=doc["value"], date=doc["dt"]))

        return Data(rows=rows)
