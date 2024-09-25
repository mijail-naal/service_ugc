from contextlib import closing

from pymongo import MongoClient

from mongo_mg.mongo_storage import MongoStorage
from utils.data_generator import MongoDataGenerator


def metrics(res, action, rows, batch):
    result = f"""
    Mongo {action} results:

    Total rows               |Batch                     | Average per {action:<12} | Total execution time
    -------------------------|--------------------------|--------------------------|----------------------
    {rows:<24} | {batch:<24} | {res / rows:<24} | {res:<24}
    """
    return result


if __name__ == '__main__':
    database = 'ApproachDB'
    collection_name = 'views'
    total_rows = 100000
    batch = 10000

    with closing(MongoClient('localhost:27017')) as client:
        generator = MongoDataGenerator()
        mongo_db = MongoStorage(client, generator)
        db = mongo_db.connect_to_db(database)
        collection = mongo_db.create_collection(db, collection_name)

        total_time = mongo_db.add(collection, total_rows, batch)
        print(metrics(total_time, 'insert', total_rows, batch))

        count_time = mongo_db.count_all(collection)
        print(metrics(count_time, 'read', total_rows, batch))

        db.drop_collection(collection)
    client.close()
