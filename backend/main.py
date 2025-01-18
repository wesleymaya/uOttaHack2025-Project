#TODO
import json

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
    
def main():
    # Demonstration of how to use get_api()
    grok_key,elevenlabs_key = get_api()
    if grok_key and elevenlabs_key:
        print(f"Your API key is: {grok_key}\nYour elevenlabs key is: {elevenlabs_key}")
    else:
        print("No API key found.")
    
if __name__ == "__main__":
    main()
