from pymongo import MongoClient, errors

# MongoDB setup
MONGO_URI = "mongodb://localhost:27017/"
client = None

# Database and collections
db = None
budget_items_collection = None
conversation_collection = None

def connect_to_db():
    """Establish connection to MongoDB."""
    global client, db, budget_items_collection, conversation_collection
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)  # Timeout after 5 seconds
        # Test the connection
        client.admin.command("ping")
        db = client["main_db"]
        budget_items_collection = db["budget_items"]
        conversation_collection = db["conversation_state"]
        print("Connected to MongoDB!")
    except errors.ConnectionFailure as e:
        print(f"Failed to connect to MongoDB: {e}")
        raise
    except errors.ConfigurationError as e:
        print(f"Configuration Error: {e}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise

def send_json_to_mongodb(data, collection):
    """
    Sends the given JSON content to the specified MongoDB collection.
    This function overwrites any existing data in the collection.
    
    :param data: The JSON-serializable data to be sent.
    :param collection: The MongoDB collection to overwrite.
    :return: Result of the insertion operation.
    """
    try:
        # Overwrite the existing data in the collection
        collection.delete_many({})  # Delete all existing documents
        result = collection.insert_one(data)  # Insert the new data
        
        print("JSON content successfully sent to MongoDB!")
        return result
    except Exception as e:
        print(f"An error occurred while sending JSON to MongoDB: {e}")
        raise


def delete_conversation_state():
    """
    Deletes all conversation state data from the database.
    :return: Result of the delete operation.
    """
    return conversation_collection.delete_many({})

# Connection handlers for app lifecycle

def close_db_connection():
    """Close connection to MongoDB."""
    client.close()
    print("Disconnected from MongoDB")

if __name__ == "__main__":
    try:
        connect_to_db()
        
        print("Connection to MongoDB was successful.")
    except Exception as e:
        print("Error while connecting to MongoDB:", e)
    
        
