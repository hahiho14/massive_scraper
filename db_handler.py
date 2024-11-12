from abc import ABC, abstractmethod
from pymongo import MongoClient
from bson import ObjectId
from my_env import MONGO_URI

class DBHandler(ABC):
    """
    Abstract base class defining standard database operations.
    """

    @abstractmethod
    def insert(self, data):
        pass

    @abstractmethod
    def update(self, record_id, data):
        pass

    @abstractmethod
    def delete(self, record_id):
        pass

    @abstractmethod
    def find_by_id(self, record_id):
        pass

    @abstractmethod
    def find_all(self, query=None):
        pass


class MongoDB(DBHandler):
    """
    MongoDB implementation of DBHandler.
    """

    def __init__(self, db_name, collection_name, uri=MONGO_URI):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def insert(self, data):
        """
        Inserts a new document into the collection.
        """
        return self.collection.insert_one(data).inserted_id

    def update(self, record_id, data):
        """
        Updates a document by its ID.
        """
        return self.collection.update_one({"_id": ObjectId(record_id)}, {"$set": data})

    def delete(self, record_id):
        """
        Deletes a document by its ID.
        """
        return self.collection.delete_one({"_id": ObjectId(record_id)})

    def find_by_id(self, record_id):
        """
        Finds a document by its ID.
        """
        return self.collection.find_one({"_id": ObjectId(record_id)})

    def find_all(self, query=None):
        """
        Finds all documents matching a query, or all documents if no query is provided.
        """
        if query is None:
            query = {}
        return list(self.collection.find(query))