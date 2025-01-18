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

def insert_budget_item(item):
    """
    Inserts a new budget item into the database.
    :param item: Dictionary containing budget item details.
    :return: Inserted ID.
    """
    return budget_items_collection.insert_one(item).inserted_id


def edit_budget_item(item_name, updates):
    """
    Edits a budget item in the database by item_name.
    :param item_name: The name of the item to update.
    :param updates: A dictionary containing the fields to update and their new values.
    :return: The result of the update operation.
    """
    if not updates:
        raise ValueError("Updates cannot be empty.")

    result = budget_items_collection.update_one(
        {"item_name": item_name},  # Filter
        {"$set": updates}  # Update
    )

    if result.matched_count == 0:
        print(f"No budget item found with name '{item_name}'.")
        return None

    print(f"Updated budget item '{item_name}' with {updates}.")
    return result

def get_budget_items():
    """
    Retrieves all budget items from the database.
    :return: List of budget items.
    """
    return list(budget_items_collection.find())

def delete_budget_items():
    """
    Deletes all budget items from the database.
    :return: Result of the delete operation.
    """
    return budget_items_collection.delete_many({})

def insert_conversation_state(state):
    """
    Inserts a conversation state into the database.
    :param state: Dictionary containing conversation state details.
    :return: Inserted ID.
    """
    return conversation_collection.insert_one(state).inserted_id

def get_conversation_state():
    """
    Retrieves the current conversation state from the database.
    :return: List of conversation states.
    """
    return list(conversation_collection.find())

def delete_conversation_state():
    """
    Deletes all conversation state data from the database.
    :return: Result of the delete operation.
    """
    return conversation_collection.delete_many({})

# Connection handlers for app lifecycle

def connect_to_db():
    """Establish connection to MongoDB."""
    global client
    client = MongoClient(MONGO_URI)
    print("Connected to MongoDB")

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
    finally:
        close_db_connection()
