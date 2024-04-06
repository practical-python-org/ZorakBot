"""Our Mongo DB instance."""
import logging
import time
from typing import Dict, List

import pymongo
from discord.ext.commands import Bot

logger = logging.getLogger(__name__)


class MongoDBClient:
    """
    A class that provides a simple interface for performing common
    operations with MongoDB using the PyMongo library.
    This is a standard interface that can be used to implement any sort of database functionality.
    """

    def __init__(self, host: str, port: int, database: str = "Zorak"):
        """
        Initialize the MongoDB instance.

        Parameters:
        - host: the hostname or IP address of the MongoDB instance
        - port: the port number of the MongoDB instance
        - port: the port number of the MongoDB instance
        - database: the name of the database to use
        """
        self.client = pymongo.MongoClient(host, port)
        self.db = self.client[database]

    def create_collection(self, collection_name: str, validator_schema: Dict = None):
        """
        Create a new collection.

        Parameters:
        - collection_name: the name of the collection to create
        - validators: a list of document validation rules to apply to the collection (optional)
        """
        try:
            self.db.create_collection(collection_name)
        except pymongo.errors.CollectionInvalid:
            logger.debug("Collection {%s} already exists.", collection_name)
        if validator_schema:
            self.configure_validation(collection_name, validator_schema)

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

        """
        try:
            self.db.command("collMod", collection, validator={"$jsonSchema": validator})
        except pymongo.errors.OperationFailure:
            logger.warning("Validation rule already exists for collection {%s}.", collection)

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

    # def backup_db(self):
    #     """Backup the MongoDB instance."""

    #     subprocess.run(
    #       ["docker", "exec", "mongo", "sh", "-c", "'mongodump", "--archive'", ">", "db.dump"])
    #     logger.info("Database backed up.")


class CustomMongoDBClient(MongoDBClient):
    """A further extension ontop of the earlier MongoDB class to abstract functions to be able
    to more easily interact with a custom database design. This is only intended to handle a single
    guild, but could be extended to handle multiple guilds by adding a guild_id field
    to the user table, or adding a new table for each guild."""

    ###############
    #    Settings
    ###############
    def initialise_settings_table(self):
        """ Initializes a GuildSettings Table """
        validator = {
            "validator": {
                "$jsonSchema": {
                    "bsonType": "object",
                    "title": "GuildSettings Validation",
                    "required": ["id", "name"],
                    "properties": {
                        "id": {
                            "bsonType": "int",
                            "description": "'id' must be an int and is required"
                        },
                        "name": {
                            "bsonType": "string",
                            "description": "'name' must be a string and is required"
                        },
                        "website": {
                            "bsonType": "string",
                            "description": "'website' must be a string and is required"
                        },
                        "email": {
                            "bsonType": "string",
                            "description": "'email' must be a string and is required"
                        },
                        "logo": {
                            "bsonType": "string",
                            "description": "'logo' must be a string if the field exists"
                        },
                        "verification_channel": {
                            "bsonType": "int",
                            "description": "'verification_channel' must be an integer"
                        },
                        "quarantine_channel": {
                            "bsonType": "int",
                            "description": "'quarantine_channel' must be an integer if the field exists"
                        },
                        "support_channel": {
                            "bsonType": "int",
                            "description": "'support_channel' must be an integer if the field exists"
                        },
                        "role_channel": {
                            "bsonType": "int",
                            "description": "'role_channel' must be an integer if the field exists"
                        },
                        "rules_channel": {
                            "bsonType": "int",
                            "description": "'rules_channel' must be an integer if the field exists"
                        },
                        "general_channel": {
                            "bsonType": "int",
                            "description": "'general_channel' must be an integer if the field exists"
                        },
                        "resources_channel": {
                            "bsonType": "int",
                            "description": "'resources_channel' must be an integer if the field exists"
                        },
                        "challenges_channel": {
                            "bsonType": "int",
                            "description": "'challenges_channel' must be an integer if the field exists"
                        },
                        "chat_log": {
                            "bsonType": "int",
                            "description": "'chat_log' must be an integer if the field exists"
                        },
                        "join_log": {
                            "bsonType": "int",
                            "description": "'join_log' must be an integer if the field exists"
                        },
                        "mod_log": {
                            "bsonType": "int",
                            "description": "'mod_log' must be an integer if the field exists"
                        },
                        "server_change_log": {
                            "bsonType": "int",
                            "description": "'server_change_log' must be an integer if the field exists"
                        },
                        "user_log": {
                            "bsonType": "int",
                            "description": "'user_log' must be an integer if the field exists"
                        },
                        "verification_log": {
                            "bsonType": "int",
                            "description": "'verification_log' must be an integer if the field exists"
                        },
                        "zorak_log": {
                            "bsonType": "int",
                            "description": "'zorak_log' must be an integer if the field exists"
                        },
                        "owner_role": {
                            "bsonType": "int",
                            "description": "'owner_role' must be an integer if the field exists"
                        },
                        "admin_role": {
                            "bsonType": "int",
                            "description": "'admin_role' must be an integer if the field exists"
                        },
                        "staff_role": {
                            "bsonType": "int",
                            "description": "'staff_role' must be an integer if the field exists"
                        },
                        "networking_role": {
                            "bsonType": "int",
                            "description": "'networking_role' must be an integer if the field exists"
                        },
                        "bot_role": {
                            "bsonType": "int",
                            "description": "'bot_role' must be an integer if the field exists"
                        },
                        "beginner_role": {
                            "bsonType": "int",
                            "description": "'beginner_role' must be an integer if the field exists"
                        },
                        "intermediate_role": {
                            "bsonType": "int",
                            "description": "'intermediate_role' must be an integer if the field exists"
                        },
                        "professional_role": {
                            "bsonType": "int",
                            "description": "'professional_role' must be an integer if the field exists"
                        },
                        "north_america_role": {
                            "bsonType": "int",
                            "description": "'north_america_role' must be an integer if the field exists"
                        },
                        "europe_role": {
                            "bsonType": "int",
                            "description": "'europe_role' must be an integer if the field exists"
                        },
                        "asia_role": {
                            "bsonType": "int",
                            "description": "'asia_role' must be an integer if the field exists"
                        },
                        "africa_role": {
                            "bsonType": "int",
                            "description": "'africa_role' must be an integer if the field exists"
                        },
                        "south_america_role": {
                            "bsonType": "int",
                            "description": "'south_america_role' must be an integer if the field exists"
                        },
                        "oceana_role": {
                            "bsonType": "int",
                            "description": "'oceana_role' must be an integer if the field exists"
                        },
                        "naughty_role": {
                            "bsonType": "int",
                            "description": "'naughty_role' must be an integer if the field exists"
                        },
                        "verified_role": {
                            "bsonType": "int",
                            "description": "'verified_role' must be an integer if the field exists"
                        }
                    }
                }
            }
        }

        self.create_collection("GuildSettings", validator_schema=validator)
        logger.info("GuildSettings initialised.")

    def get_guild_settings(self, guild):
        settings = self.find_one("GuildSettings", {"id": guild.id})
        if settings:
            return settings
        return None

    def add_guild_to_table(self, guild):
        if not self.find_one("GuildSettings", {"id": guild.id}):
            logger.info(f" ---- Adding {guild.name} to DB")
            self.insert_one("GuildSettings", {
                # Guild Info
                "id": guild.id
                , "name": guild.name
                , "logo": guild.icon.url
                , "website": None
                , "email": None
                , "review": None
                , "invite": None
                , "member_count": guild.member_count
                , "premium_guild": False
                , "FeatureFlag1": False
                , "FeatureFlag2": False
                , "FeatureFlag3": False

                # Channel Info
                , "verification_channel": None
                , "quarantine_channel": None
                , "support_channel": None
                , "role_channel": None
                , "rules_channel": guild.rules_channel  # Default: None
                , "general_channel": None
                , "resources_channel": None
                , "challenges_channel": None

                # Logging Channels
                , "chat_log": None
                , "join_log": None
                , "mod_log": None
                , "server_change_log": None
                , "user_log": None
                , "verification_log": None
                , "zorak_log": None

                # Roles
                , "owner_role": None
                , "admin_role": None
                , "staff_role": None
                , "networking_role": None
                , "bot_role": guild.self_role.id  # Default: None
                , "beginner_role": None
                , "intermediate_role": None
                , "professional_role": None
                , "north_america_role": None
                , "europe_role": None
                , "asia_role": None
                , "africa_role": None
                , "south_america_role": None
                , "oceana_role": None
                , "naughty_role": None
                , "verified_role": None
            })

    def update_guild_settings(self, guild, item, value):
        """Update the settings of a guild."""
        try:
            self.update_one(
                "GuildSettings", {"id": guild.id}, {"$set": {item: value}}
            )  # The $set operator replaces the value of a field with the specified value.

        except Exception as ohfuck:
            logger.critical(f"There was an issue updating {item} with {value}. Error: {ohfuck}")

    def remove_guild_from_table(self, guild):
        """Remove a guild from the GuildSettings table."""
        self.delete_one("GuildSettings", {"id": guild.id})

    ###############
    #    Users
    ###############
    def initialise_user_table(self):
        """Initialise the user table. Ensures that the UserID field is unique."""
        validator = {
            "bsonType": "object",
            "title": "Points Collection Validation",
            "required": ["UserID", "Points"],
            "properties": {
                "UserID": {
                    "bsonType": "long",
                    "description": "The ID of the user.",
                },
                "Points": {
                    "bsonType": "int",
                    "minimum": 0,
                    "description": "The number of points the user has.",
                },
            },
        }
        self.create_collection("UserPoints", validator_schema=validator)
        logger.info("User table initialised.")

    def add_user_to_table(self, member):
        """Add a user to the user table if they are not already in it."""
        if not self.find_one("UserPoints", {"UserID": member.id}):
            self.insert_one("UserPoints", {"UserID": member.id, "Points": 0})

    def create_table_from_members(self, members: List):
        """Create a table from a list of members if it does not already exist.
        If it does it adds all unnadded members"""
        for member in members:
            self.add_user_to_table(member)

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

    def get_top_10(self):
        """Get the top 10 point earners."""
        top10 = []
        # Grab 20, because we filter out staff/bot users later in the command.
        for x in self.find("UserPoints").sort("Points", -1).limit(20):
            top10.append(x)
        return top10

    # ###############
    # #    RSS
    # ###############
    #
    # def initialise_news_table(self):
    #     """Initialise the news table."""
    #     validator = {
    #         "bsonType": "object",
    #         "title": "News Collection Validation",
    #         "required": ["entryID"],
    #         "properties": {
    #             "entryID": {
    #                 "bsonType": "string",
    #                 "description": "The ID of the story.",
    #             }
    #         },
    #     }
    #     self.create_collection("News", validator_schema=validator)
    #     logger.info("News table initialised.")
    #
    # def add_story_to_table(self, entry_id: str):
    #     """Add a story to the news table if they are not already in it."""
    #     if not self.find_one("News", {"entryID": entry_id}):
    #         self.insert_one("News", {"entryID": entry_id})
    #
    # def get_all_stories(self):
    #     """Get all stories from the news table."""
    #     return self.find("News", {})

    ###############
    #    DevTimes
    ###############
    def initialise_dev_times_table(self):
        """Initialise the devtimes table. """
        validator = {
            "bsonType": "object",
            "title": "Dev Times Collection Validation",
            "required": ["Username", "Country", "Timezone"],
            "properties": {
                "Username": {
                    "bsonType": "string",
                    "description": "The Username (Display name not UID) of the user to be displayed.",
                },
                "Country": {
                    "bsonType": "string",
                    "description": "The country of the user.",
                },
                "Timezone": {
                    "bsonType": "string",
                    "description": " The time according to pytz.timezone, example: Asia/Kolkata.",
                },
            },
        }
        self.create_collection("DevTimes", validator_schema=validator)
        logger.info("Dev Times table initialised.")

    def add_dev_time_to_table(self, username: str, country: str, timezone: str):
        """Add a user to the user table if they are not already in it."""
        if not self.find_one("DevTimes", {"Username": username}):
            self.insert_one("DevTimes", {"Username": username, "Country": country, "Timezone": timezone})

    def remove_dev_time_from_table(self, username: str):
        """Remove a user from the user table."""
        self.delete_one("DevTimes", {"Username": username})

    def get_all_dev_times(self):
        """Get all dev times from the table."""
        return self.find("DevTimes", {})


def initialise_bot_db(
    bot: Bot,
):  # This is called in the main bot file and is the bit of code that connects to the database.
    """Initialise the database."""
    connected = False
    attempts = 0
    while connected is False and attempts < 5:
        logger.info("Connecting to database... Attempt %s of 10", str(attempts + 1))
        db_client = CustomMongoDBClient(host="mongo",
                                        port=27017)  # It creates a new instance of the CustomMongoDBClient class,
        # which abstracts our database interactions.
        try:
            time.sleep(10)
            db_client.client.admin.command("ping")  # This is a test to see if the database is up and running.
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

        db_client.initialise_user_table()  # type: ignore
        db_client.initialise_settings_table()  # type: ignore

        bot.db_client = db_client  # type: ignore
        # This adds the db_client to the bot
        # object so that it can be accessed elsewhere.
