from calendar import month
from datetime import datetime, timedelta

from motor.motor_asyncio import AsyncIOMotorClient

from business import Data, Row


class MongoDB:
    """
    Класс описывает выдачу коллекции из MongoDB
    """

    def __init__(self, db_name: str, mongo_uri: str, collection_name: str):
        cluster = AsyncIOMotorClient(mongo_uri)
        database = cluster[db_name]
        self.collection = database[collection_name]

    async def get_data(self, from_: datetime, to: datetime, by: str) -> Data:
        query = {"dt": {"$gte": from_, "$lte": to}}
        documents = self.collection.find(query)
        delta = self.get_timedelta(by)
        lowest_stamp = from_
        highest_stamp = to
        print(delta)
        rows = []
        dates = []
        async for doc in documents:
            rows.append(Row(price=doc["value"], date=doc["dt"]))
            dates.append(doc["dt"])

        iterations = round((highest_stamp - lowest_stamp) / delta)
        for _ in range(iterations + 1):
            if not lowest_stamp in dates:
                rows.append(Row(price=0, date=lowest_stamp))
            lowest_stamp += delta

        if rows[-1].date > highest_stamp:
            rows.pop()

        return Data(rows=sorted(rows, key=lambda x: x.date))

    def get_timedelta(self, group_type: str) -> timedelta:
        if group_type == "hour":
            return timedelta(minutes=60)
        elif group_type == "day":
            return timedelta(hours=24)
        elif group_type == "month":
            return timedelta(days=30)
        else:
            return timedelta(days=365)
