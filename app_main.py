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
        return config.get("api_key", "")
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"Error: Could not read or parse {filename}.")
        return ""

def main():
    
    # Get the API key from the config
    api_key = get_api()

    # Just print the API key for demonstration
    # In a real script, you'd use this key to make an API request, etc.
    print(f"Your API key is: {api_key}")

    # Example placeholder for actual API logic:
    # e.g., requests.get("https://api.example.com/data", headers={"Authorization": f"Bearer {api_key}"})
    




if __name__ == "__main__":
    main()
