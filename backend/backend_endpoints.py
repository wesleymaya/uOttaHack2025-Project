from fastapi import FastAPI, Body
from db import (
    insert_budget_item,
    get_budget_items,
    delete_budget_items,
    insert_conversation_state,
    get_conversation_state,
    delete_conversation_state,
)

app = FastAPI()

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

@app.get("/api/budget-summary")
def get_budget_summary():
    """
    Endpoint to retrieve a summary of the current budget.
    :return: Summary of all budget items.
    """
    budget_items = get_budget_items()
    return {"message": "Budget summary retrieved.", "data": budget_items}

@app.post("/api/check-purchase")
def check_purchase_within_budget(purchase: dict = Body(...)):
    """
    Endpoint to check if a specific purchase is within the budget.
    :param purchase: A dictionary containing purchase details (e.g., amount, description).
    :return: Decision on whether the purchase is within budget.
    """
    # Placeholder for purchase checking logic
    return {"message": "Purchase check is not yet implemented.", "purchase": purchase}

@app.on_event("startup")
async def startup_event():
    print("API is starting up. Connected to MongoDB!")

@app.on_event("shutdown")
async def shutdown_event():
    print("API is shutting down. Disconnected from MongoDB.")
