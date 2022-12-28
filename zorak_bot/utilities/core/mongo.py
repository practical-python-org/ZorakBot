import logging
from typing import Dict, List

import pymongo

logger = logging.getLogger(__name__)


class MongoDB:
    """
    A class that provides a simple interface for performing common operations with MongoDB using the PyMongo library.
    """

    def __init__(self, host: str, port: int, database: str):
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
