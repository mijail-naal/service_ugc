from time import time

from pymongo import MongoClient
from pymongo.collection import Collection
from utils.data_generator import MongoDataGenerator


class MongoStorage:
    def __init__(self, client: MongoClient, generator: MongoDataGenerator):
        self.client = client
        self.generator = generator

    def connect_to_db(self, db_name):
        return self.client[db_name]

    def create_collection(self, db, collection_name):
        collection = db[collection_name]
        return collection

    def add(self, collection: Collection, total, size):
        start = time()
        for data in self.generator.add_data(total, size):
            collection.insert_many(data)
        end = time()
        return end - start

    def count_all(self, collection: Collection):
        start = time()
        collection.count_documents({})
        end = time()
        return end - start
