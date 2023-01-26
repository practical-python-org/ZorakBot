import logging
from typing import Dict, List

import pymongo
import time
from discord.ext.commands import Bot

logger = logging.getLogger("discord")


class MongoDBClient:
    """
    A class that provides a simple interface for performing common operations with MongoDB using the PyMongo library.
    This is a standard interface that can be used to implement any sort of database functionality.
    """

    def __init__(self, host: str, port: int, database: str = "Zorak"):
        """
        Initialize the MongoDB instance.

        Parameters:
        - host: the hostname or IP address of the MongoDB instance
        - port: the port number of the MongoDB instance
        - database: the name of the database to use
        """
        self.client = pymongo.MongoClient(host, port)
        self.db = self.client[database]

    def create_collection(self, collection_name: str, validators: List[Dict] = None):
        """
        Create a new collection.

        Parameters:
        - collection_name: the name of the collection to create
        - validators: a list of document validation rules to apply to the collection (optional)
        """
        self.db.create_collection(collection_name)
        if validators:
            for validator in validators:
                self.configure_validation(collection_name, validator)

    def get_all_collection_names(self):
        """Get all collection names in the database."""
        return self.db.list_collection_names()

    def drop_collection(self, collection_name: str):
        """
        Drop (delete) a collection.

        Parameters:
        - collection_name: the name of the collection to drop
        """
        self.db.drop_collection(collection_name)

    def configure_validation(self, collection: str, validator: Dict):
        """
        Configure document validation rules for a collection.

        Parameters:
        - collection: the name of the collection
        - validator: a document validation rule
        """
        self.db[collection].create_index(validator, name="validator_index", background=True)
        self.db[collection].collation = {"locale": "en", "strength": 2}
        self.db[collection].create_constraint("validator_index", validator)

    def insert_one(self, collection: str, document: Dict):
        """
        Insert a single document into a collection.

        Parameters:
        - collection: the name of the collection
        - document: the document to insert
        """
        self.db[collection].insert_one(document)

    def insert_many(self, collection: str, documents: List[Dict]):
        """Insert multiple documents into a collection.

        Parameters
        ----------
        collection : str
            The name of the collection.
        documents : List[Dict]
            The documents to insert.
        """
        self.db[collection].insert_many(documents)

    def find_one(self, collection: str, query: Dict = {}):
        """Find a single document in a collection.

        Parameters
        ----------
        collection : str
            The name of the collection.
        query : Dict, optional
            The query to use to find the document, by default {}

        Returns
        -------
        _type_
            The document found.
        """
        return self.db[collection].find_one(query)

    def find(self, collection: str, query: Dict = {}):
        """Find multiple documents in a collection.

        Parameters
        ----------
        collection : str
            The name of the collection.
        query : Dict, optional
            The query to use to find the documents, by default {}

        Returns
        -------
        _type_
            The documents found.
        """
        return self.db[collection].find(query)

    def update_one(self, collection: str, query: Dict, update: Dict, upsert: bool = False):
        """Update a single document in a collection.

        Parameters
        ----------
        collection : str
            The name of the collection.
        query : Dict
            The query to use to find the document.
        update : Dict
            The update to apply to the document.
        upsert : bool, optional
            Flag to insert the document if it is not found, by default False
        """
        self.db[collection].update_one(query, update, upsert=upsert)

    def update_many(self, collection: str, query: Dict, update: Dict, upsert: bool = False):
        """Update multiple documents in a collection.

        Parameters
        ----------
        collection : str
            The name of the collection.
        query : Dict
            The query to use to find the documents.
        update : Dict
            The update to apply to the documents.
        upsert : bool, optional
            Flag to insert the documents if they are not found, by default False
        """
        self.db[collection].update_many(query, update, upsert=upsert)

    def delete_one(self, collection, query):
        """Delete a single document from a collection.

        Parameters
        ----------
        collection : _type_
            The name of the collection.
        query : _type_
            The query to use to find the document.
        """
        self.db[collection].delete_one(query)

    def delete_many(self, collection, query):
        """Delete multiple documents from a collection.

        Parameters
        ----------
        collection : _type_
            The name of the collection.
        query : _type_
            The query to use to find the documents.
        """
        self.db[collection].delete_many(query)

    def backup_db(self, database_name: str, output_dir: str = "."):
        """Backup the MongoDB instance."""
        self.db.client.admin.command("backup", to=f"{output_dir}/{database_name}.gz")
        logger.info("Database backed up.")


class PointsDBClient(MongoDBClient):
    """A further extension ontop of the earlier MongoDB class to abstract functions to be able to more easily
    interact with a database focussed around assigning points to users. This is only intended to handle a single
    guild, but could be extended to handle multiple guilds by adding a guild_id field to the user table, or adding
    a new table for each guild."""

    # def __init__(self, host: str, port: int, database: str = "Zorak"):
    #     super(PointsDBClient, self).__init__(host=host, port=port, database=database)

    def initialise_user_table(self):
        """Initialise the user table."""
        self.db.create_collection("UserPoints", validators=[{"UserID": 1}])
        logger.info("User table initialised.")

    def create_table_from_members(self, members: List):
        """Create a table from a list of members if it does not already exist. If it does it adds all unnadded members"""
        for member in members:
            self.insert_one("UserPoints", {"UserID": member.id})

    def add_user_to_table(self, member):
        """Add a user to the user table if they are not already in it."""
        self.insert_one("UserPoints", {"UserID": member.id})

    def remove_user_from_table(self, member):
        """Remove a user from the user table."""
        self.delete_one("UserPoints", {"UserID": member.id})

    def add_points_to_user(self, user_id: int, points: int):
        """Add points to a user."""
        self.update_one(
            "UserPoints", {"UserID": user_id}, {"$inc": {"Points": points}}
        )  # The $inc operator increments a field by a specified value.

    def add_points_to_all_users(self, points: int):
        """Add points to all users."""
        self.update_many("UserPoints", {}, {"$inc": {"Points": points}})

    def remove_points_from_user(self, user_id: int, points: int):  # Not really needed, but here for completeness.
        """Remove points from a user."""
        self.update_one("UserPoints", {"UserID": user_id}, {"$inc": {"Points": -points}})

    def remove_points_from_all_users(self, points: int):
        """Remove points from all users."""
        self.update_many("UserPoints", {}, {"$inc": {"Points": -points}})

    def set_user_points(self, user_id: int, points: int):
        """Update the points of a user."""
        self.update_one(
            "UserPoints", {"UserID": user_id}, {"$set": {"Points": points}}
        )  # The $set operator replaces the value of a field with the specified value.

    def set_all_user_points(self, points: int):
        """Update the points of all users."""
        self.update_many("UserPoints", {}, {"$set": {"Points": points}})

    def get_user_points(self, user_id: int):
        """Get the points of a user."""
        user = self.find_one("UserPoints", {"UserID": user_id})
        if user:
            return user["Points"]
        return None


def initialise_bot_db(bot: Bot):
    """Initialise the database."""
    connected = False
    attempts = 0
    while connected == False and attempts < 5:
        logger.info(f"Connecting to database... Attempt {str(attempts+1)} of 10")
        db_client = PointsDBClient(host="mongo", port=27017)
        try:
            time.sleep(10)
            db_client.client.admin.command('ping')
            connected = True
        except Exception as e:
            logger.error("Connecting to database...")
            logger.error(e)
            if attempts < 9:
                logger.info("Retrying...")
            else:
                logger.info("Failed to connect to database.")
            attempts += 1
    if connected:
        logger.info("Connected to database.")
        bot.db_client = db_client
    return bot
