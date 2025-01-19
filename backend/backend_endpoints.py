from fastapi import FastAPI, Body
from db import (
    insert_budget_item,
    get_budget_items,
    delete_budget_items,
    insert_conversation_state,
    get_conversation_state,
    delete_conversation_state,
    get_budget_limit
)

app = FastAPI()

# Define a global budget limit (you can also store this in the database)

@app.get("/api/budget-summary")
def get_budget_summary():
    """
    Endpoint to retrieve a summary of the current budget.
    :return: Summary of all budget items and an overage warning if applicable.
    """
    budget_limit = get_budget_limit()
    budget_items = get_budget_items()
    total_expenses = calculate_total_expenses()
    over_budget = total_expenses > budget_limit

    return {
        "message": "Budget summary retrieved.",
        "data": budget_items,
        "total_expenses": total_expenses,
        "budget_limit": budget_limit,
        "over_budget": over_budget,
        "warning": "You have exceeded your budget limit!" if over_budget else None
    }

@app.post("/api/check-purchase")
def check_purchase_within_budget(purchase: dict = Body(...)):
    """
    Endpoint to check if a specific purchase is within the budget.
    :param purchase: A dictionary containing purchase details (e.g., amount, description).
    :return: Decision on whether the purchase is within budget.
    """
    budget_limit = get_budget_limit()
    purchase_amount = purchase.get("amount", 0)
    total_expenses = calculate_total_expenses()
    remaining_budget = budget_limit - total_expenses
    within_budget = purchase_amount <= remaining_budget

    return {
        "message": "Purchase check completed.",
        "purchase": purchase,
        "remaining_budget": remaining_budget,
        "within_budget": within_budget,
        "warning": "This purchase exceeds your remaining budget!" if not within_budget else None
    }

def calculate_total_expenses():
    """
    Calculate the total expenses from the budget items.
    :return: Total expense amount.
    """
    budget_items = get_budget_items()
    total_expenses = sum(item.get("amount", 0) for item in budget_items)
    return total_expenses

@app.post("/api/chat")
def chat_endpoint(user_message: str = Body(...)):
    """
    Endpoint to handle user messages and return assistant responses.
    :param user_message: The message from the user.
    :return: Assistant response.
    """
    # For now, return a mock response
    return {"message": "Chat endpoint received the message.", "user_message": user_message}

@app.post("/api/audio-to-text")
def audio_to_text_endpoint(audio_file: bytes = Body(...)):
    """
    Endpoint to handle audio input and convert it to text.
    :param audio_file: The audio file provided by the user.
    :return: Transcribed text.
    """
    # Placeholder for audio-to-text logic
    return {"message": "Audio-to-text processing is not yet implemented."}

@app.post("/api/reset")
def reset_budget():
    """
    Endpoint to reset the user's budgeting data.
    :return: Confirmation of reset.
    """
    delete_budget_items()
    delete_conversation_state()
    return {"message": "Budget data and conversation state have been reset."}



'''
@app.on_event("startup")
async def startup_event():
    print("API is starting up. Connected to MongoDB!")

@app.on_event("shutdown")
async def shutdown_event():
    print("API is shutting down. Disconnected from MongoDB!")
'''
