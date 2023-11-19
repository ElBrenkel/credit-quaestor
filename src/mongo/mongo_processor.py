from src.mongo.mongo_connector import MongoConnector


class MongoProcessor:
    def __init__(self, connector: MongoConnector, db: str = "CreditQuaestor") -> None:
        self.connector = connector
        self.db = db

    def insert_data(self, collection: str, data):
        with self.connector as connector:
            db = connector[self.db]
            collection = db[collection]
            collection.insert_one(data.to_json())

    def update_data(self, collection: str, query, new_data):
        with self.connector as connector:
            db = connector[self.db]
            collection = db[collection]
            collection.update_one(query, new_data.to_json())

    def delete_data(self, collection: str, query):
        with self.connector as connector:
            db = connector[self.db]
            collection = db[collection]
            collection.delete_one(query)

    def get_data(self, collection: str, query, condition=None):
        if not condition:
            condition = {"_id": 0}
        with self.connector as connector:
            db = connector[self.db]
            collection = db[collection]
            return list(collection.find(query, condition))
