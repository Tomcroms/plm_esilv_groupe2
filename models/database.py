from pymongo import MongoClient

class Database:
    def __init__(self, uri="mongodb+srv://thomaslaumonier:Qypj7XcUEOEuLugt@m0cluster.7daojiy.mongodb.net/PLM", db_name="PLM"):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def get_collection(self, collection_name):
        return self.db[collection_name]

    def close(self):
        self.client.close()