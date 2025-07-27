# app/db/db.py (revised)

from pymongo import MongoClient

class DatabaseClient:
    def __init__(self, mongo_uri, db_name, db_username, db_password, is_prod):
        # Just call MongoClient directly

        if is_prod == "TRUE":
            self.client = MongoClient(mongo_uri,
                                username=db_username,
                                password=db_password,
                                authSource=db_name)
        else:
            self.client = MongoClient(mongo_uri)

        self.db_name = db_name

    def get_db(self, db_name=None):
        return self.client[db_name or self.db_name]

db_client = None

def init_db(flask_config):
    """
    Initializes the database client using the keys from the Flask config object.
    We expect flask_config['MONGO_URI'] and flask_config['DB_NAME'] to exist.
    """
    global db_client

    mongo_uri = flask_config["MONGO_URI"]
    db_name = flask_config["DB_NAME"]
    db_username = flask_config["MONGO_DB_USERNAME"]
    db_password = flask_config["MONGO_DB_PASSWORD"]
    is_prod = flask_config["IS_PROD"]

    db_client = DatabaseClient(mongo_uri, db_name, db_username, db_password, is_prod)

def get_db():
    if db_client is None:
        raise Exception("Database client is not initialized. Call init_db(...) first.")
    return db_client.get_db()

def get_collection(collection_name):
    db = get_db()
    return db[collection_name]
