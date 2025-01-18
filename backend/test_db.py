from pymongo import MongoClient

# MongoDB setup
MONGO_URI = "mongodb://localhost:27017/"
client = MongoClient(MONGO_URI)

# Database and collections
db = client["main_db"]
budget_items_collection = db["budget_items"]
conversation_collection = db["conversation_state"]

# Add placeholder data to budget_items
placeholder_budget_items = [
    {
        "item_name": "Rent",
        "amount": 1200.0,
        "category": "Recurring",
        "importance_rank": 1,
        "recurrence_schedule": "monthly",
        "due_date": 1
    },
    {
        "item_name": "Groceries",
        "amount": 300.0,
        "category": "Regular",
        "importance_rank": 2,
        "recurrence_schedule": "weekly",
        "due_date": None
    },
    {
        "item_name": "Poop Repair",
        "amount": 500.0,
        "category": "Irregular",
        "importance_rank": 3,
        "recurrence_schedule": None,
        "due_date": None
    }
]

# Add placeholder data to conversation_state
placeholder_conversation_state = {
    "session_id": "placeholder_session",
    "messages": [
        {"role": "user", "content": "What is my current budget?"},
        {"role": "assistant", "content": "You have $2,000 left for the month."}
    ]
}

# Insert placeholder data
budget_items_result = budget_items_collection.insert_many(placeholder_budget_items)
conversation_state_result = conversation_collection.insert_one(placeholder_conversation_state)

print(f"Inserted budget items with IDs: {budget_items_result.inserted_ids}")
print(f"Inserted conversation state with ID: {conversation_state_result.inserted_id}")


# Retrieve and print all documents from budget_items
print(list(budget_items_collection.find()))

# Retrieve and print all documents from conversation_state
print(list(conversation_collection.find()))


