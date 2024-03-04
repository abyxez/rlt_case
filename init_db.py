"""
Этот скрипт выполняет импорт папки dump/ 
в коллекцию МонгоДБ.
"""

import os

import bson
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

mongo_uri = os.getenv("MONGO_URL")
database_name = os.getenv("MONGO_DATABASE_NAME")
collection_name = os.getenv("MONGO_COLLECTION_NAME")

client = MongoClient(mongo_uri)

db = client[database_name]  # type: ignore
collection = db[collection_name]  # type: ignore

file_path = "dump/sampleDB/sample_collection.bson"

with open(file_path, "rb") as file:
    data = bson.decode_all(file.read())
    collection.insert_many(data)

print("Данные успешно внесены в MongoDB")
