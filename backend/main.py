#TODO
import json, llama_chain
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Or the domain of your frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define a data model for request validation
class DataModel(BaseModel):
    message: str

def get_api(filename="config.json"):
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
        return config.get("grok_api_key", ""), config.get("elevenlabs_api_key","")
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"Error: Could not read or parse {filename}.")
        return ""
    
# **Test if works
# Main way the front-end will request data from Groq/MongoDB
@app.post("/getdata")
async def receive_data(data: DataModel):
    print(f"Received data: {data.message}")
    answer = llama_chain.parse_budget(data.message)
    return answer


# **Test if works
def main():
    try:
        print("Listening for users...")
        uvicorn.run(app, host="0.0.0.0", port=8000)
    except(HTTPException):
        print("Error: Issue when trying to listen for users.")

    
if __name__ == "__main__":
    import uvicorn
    main()

'''
 # Demonstration of how to use get_api()
    grok_key,elevenlabs_key = get_api()
    if grok_key and elevenlabs_key:
        print(f"Your API key is: {grok_key}\nYour elevenlabs key is: {elevenlabs_key}")
    else:
        print("No API key found.")
'''
