import os
import logging
import traceback
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
            logging.error(
                "An exception occurred in your with block: %s \nException message: %s\n",
                exc_type,
                exc_value,
            )
            traceback.print_tb(exc_tb)
            return False


# with MongoConnector() as client:
#     db = client["CreditQuaestor"]
#     collection = db["users"]
#     data = collection.find({})

#     for document in data:
#         print(document)
