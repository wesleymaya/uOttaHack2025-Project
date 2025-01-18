import json

from fastapi import FastAPI, Body

app = FastAPI()

@app.post("/api/chat")
def chat_endpoint(user_message: str = Body(...)):
    """
    Endpoint to handle user messages and return assistant responses.
    :param user_message: The message from the user.
    :return: Assistant response.
    """
    # Functionality to be implemented
    pass

@app.post("/api/audio-to-text")
def audio_to_text_endpoint(audio_file: bytes = Body(...)):
    """
    Endpoint to handle audio input and convert it to text.
    :param audio_file: The audio file provided by the user.
    :return: Transcribed text.
    """
    # Functionality to be implemented
    pass

@app.post("/api/reset")
def reset_budget():
    """
    Endpoint to reset the user's budgeting data.
    :return: Confirmation of reset.
    """
    # Functionality to be implemented
    pass

@app.get("/api/budget-summary")
def get_budget_summary():
    """
    Endpoint to retrieve a summary of the current budget.
    :return: Summary of all budget items.
    """
    # Functionality to be implemented
    pass

@app.post("/api/check-purchase")
def check_purchase_within_budget(purchase: dict = Body(...)):
    """
    Endpoint to check if a specific purchase is within the budget.
    :param purchase: A dictionary containing purchase details (e.g., amount, description).
    :return: Decision on whether the purchase is within budget.
    """
    # Functionality to be implemented
    pass


def get_api_keys(filename="config.json"):
    """
    Reads and returns the API key from a JSON config file.
    
    Parameters:
        filename (str): Path to the config JSON file.
                       Defaults to "config.json".
    
    Returns:
        str: The API key (returns an empty string if not found).
    """
    try:
        with open(filename, "r") as file:
            config = json.load(file)
        return config.get("groq_api_key", ""), config.get("elevenlabs_api_key","")
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"Error: Could not read or parse {filename}.")
        return ""

def main():
    
    # Get the API key from the config
    groq_api_key,elevenlabs_api_key = get_api_keys()

    print(f"Your groq API key is: {groq_api_key}\nYour elevenlabs API key is:{elevenlabs_api_key}")

    




if __name__ == "__main__":
    main()
