import json

def main():
    # Load configuration data from config.json
    with open("config.json", "r") as file:
        config = json.load(file)

    # Get the API key from the config
    api_key = config.get("api_key")

    # Just print the API key for demonstration
    # In a real script, you'd use this key to make an API request, etc.
    print(f"Your API key is: {api_key}")

    # Example placeholder for actual API logic:
    # e.g., requests.get("https://api.example.com/data", headers={"Authorization": f"Bearer {api_key}"})
    

if __name__ == "__main__":
    main()
