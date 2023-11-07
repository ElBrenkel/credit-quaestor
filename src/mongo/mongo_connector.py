import os
import pymongo
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.environ.get("MONGO_URI")


class MongoConnector:
    def __init__(self):
        self.mongodb_uri = MONGO_URI
        self.client = None

    def __enter__(self):
        try:
            self.client = pymongo.MongoClient(self.mongodb_uri)
            return self.client
        except pymongo.errors.ConnectionFailure as e:
            raise ConnectionError(f"Failed to connect to MongoDB: {e}") from e

    def __exit__(self, exc_type, exc_value, exc_tb):
        if self.client is not None:
            self.client.close()
        if isinstance(exc_value, Exception):
            print(f"An exception occurred in your with block: {exc_type}")
            print(f"Exception message: {exc_value}")
            return True


with MongoConnector() as client:
    db = client["CreditQuaestor"]
    collection = db["users"]
    data = collection.find({})

    for document in data:
        print(document)
