from pymongo import MongoClient
import config

_client: MongoClient = MongoClient(config.MONGO_URI)


def getDb():
    return _client[config.MONGO_DB]
