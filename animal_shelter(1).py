# animal_shelter.py
from pymongo import MongoClient
from pymongo.errors import PyMongoError

class AnimalShelter:
    """CRUD operations for the animals collection in the AAC MongoDB database."""

    def __init__(self, user='aacuser', password='snhu1234',
                 host='nv-desktop-services.apporto.com', port=33346,
                 db='AAC', collection='animals'):
        """Initialize MongoDB client, database, and collection."""
        try:
            uri = f"mongodb://{user}:{password}@{host}:{port}/?authSource={db}"
            self.client = MongoClient(uri, serverSelectionTimeoutMS=5000)
            self.database = self.client[db]
            self.collection = self.database[collection]
            # Touch the server to fail fast if unreachable
            _ = self.client.server_info()
        except PyMongoError as e:
            print(f"Error connecting to MongoDB: {e}")
            raise

    def create(self, data):
        """Insert a single document.

        Args:
            data (dict): Document to insert.

        Returns:
            bool: True if insert successful, False otherwise.
        """
        if not data:
            raise ValueError("Empty data provided for insert.")
        try:
            result = self.collection.insert_one(data)
            return bool(result.inserted_id)
        except PyMongoError as e:
            print(f"Insert error: {e}")
            return False

    def read(self, query, projection=None):
        """Find documents matching the query.

        Args:
            query (dict): MongoDB find query.
            projection (dict, optional): Projection dict to limit fields.

        Returns:
            list: List of documents matching the query.
        """
        if query is None:
            raise ValueError("Query parameter cannot be None.")
        try:
            cursor = self.collection.find(query, projection)
            return list(cursor)
        except PyMongoError as e:
            print(f"Read error: {e}")
            return []

    def update(self, query, update_data):
        """Update documents matching the query.

        Args:
            query (dict): MongoDB find query.
            update_data (dict): MongoDB update operators (e.g., {'$set': {...}}).

        Returns:
            int: Number of documents modified.
        """
        if not query or not update_data:
            raise ValueError("Both query and update_data must be provided.")
        try:
            result = self.collection.update_many(query, update_data)
            return result.modified_count
        except PyMongoError as e:
            print(f"Update error: {e}")
            return 0

    def delete(self, query):
        """Delete documents matching the query.

        Args:
            query (dict): MongoDB find query.

        Returns:
            int: Number of documents deleted.
        """
        if not query:
            raise ValueError("Query parameter cannot be empty.")
        try:
            result = self.collection.delete_many(query)
            return result.deleted_count
        except PyMongoError as e:
            print(f"Delete error: {e}")
            return 0
