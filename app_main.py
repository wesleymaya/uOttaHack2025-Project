import json


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
