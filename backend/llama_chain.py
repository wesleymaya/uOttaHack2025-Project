from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from datetime import datetime
from main import get_api
from db import send_json_to_mongodb, conversation_collection
import json

# Initialize Groq API
groq_api, _ = get_api()

# Initialize Groq LLM
llm = ChatGroq(
    model_name='llama-3.3-70b-versatile',
    temperature=0.5,
    api_key=groq_api
)

# Define the expected JSON structure
parser = JsonOutputParser(pydantic_object={
    "type": "object",
    "properties": {
        "Budget": {
            "type": "object",
            "properties": {
                "budget_limit": {"type": "number"},
                "items": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "item_name": {"type": "string"},
                            "amount": {"type": "number"},
                            "category": {
                                "type": "string",
                                "enum": ["Recurring", "Regular", "Irregular"]
                            },
                            "importance_rank": {"type": "integer"},
                            "recurrence_schedule": {"type": ["string", "null"]},
                            "due_date": {"type": ["integer", "null"]}
                        },
                        "required": [
                            "item_name", "amount", "category",
                            "importance_rank", "recurrence_schedule", "due_date"
                        ]
                    }
                },
                "warnings": {
                    "type": "array",
                    "items": {"type": "string"}
                },
                "conversations" : {
                    "type": "array",
                    "items":{"type":"string"}
                    }
            },
            "required": ["budget_limit", "items", "warnings"]
        },
        "conversation": {"type": "string"}  # New field for conversational responses
    },
    "required": ["Budget", "conversation"]
})

# Enhanced prompt with conversation capabilities
def generate_prompt(previous_budget: dict):
    return ChatPromptTemplate.from_messages([
        ("system", f"""You are an intelligent budgeting assistant. Your tasks are:
        1. Start with the user's existing budget data:
            {json.dumps(previous_budget, indent=2).replace('{', '{{').replace('}', '}}')}
            1.1 Make sure to properly transfer over the conversation data. This is crucial. The conversation key must be present in every JSON return.
            1.2 Make sure to also properly transfer over the other data as well.
        2. Allow the user to append, delete, or update individual items in the budget. Reflect this in the JSON response.
        3. If the total value of the items exceeds the budget limit, add a warning in the 'warnings' field explaining how much over budget they are.
        4. When the user inquires about adding a new item, calculate whether the new item would put them over their budget. If it does, include a warning in the response.
        5. Always provide the JSON structure as output.
        6. Engage in conversation with the user by providing clear, friendly, and helpful responses alongside the JSON data. 
            6.1 Append the previous chats to the array called conversations. The most recent chat is to be put into the standalone conversation field
        7. At the end of each chat, make sure to ask the user how else you can help them (within the scope of your duties). This is also part of what is to be added to "conversations".
        8. Always factor in one-time purchases to the budget as well, as the budget is always set for the current month. 
        9. Make sure to relate any open-ended questions to the budget. 
        10. Try to give relevant examples of alternatives for potential items that may place the user outside of the budget. 
            10.1 If the expense is rather important (the expense is a necessary one to maintain the quality of a modern person's life), give suggestions on what expenses to remove based on order of least importance.
        11. Make sure to follow the parsing format for items in this way: ( "item_name": "Groceries","amount": 300.0, "category": "Regular", "importance_rank": 2, "recurrence_schedule": "weekly", "due_date": null)
        User input: {{input}}
        """),
        ("user", "{input}")
    ])

# Persistent budget for the session
current_budget = {
    "Budget": {
        "budget_limit": 0.0,
        "items": [],
        "warnings": []
    }
}

def send_json_to_mongodb(final_result):
    if not conversation_collection:
        raise ValueError("MongoDB collection 'conversation_collection' is not initialized. Ensure 'connect_to_db' has been called.")
    conversation_collection.insert_one(final_result)

def parse_budget(description: str):
    """
    Parse user input while maintaining session consistency.
    Append new items, update existing ones, and add new conversations to the budget.
    :param description: The user's input description.
    :return: Updated budget JSON and conversational response.
    """
    global current_budget

    # Ensure current_budget has the correct structure
    current_budget.setdefault("items", [])
    current_budget.setdefault("warnings", [])
    current_budget.setdefault("conversations", [])

    prompt = generate_prompt(current_budget)  # Include previous budget
    chain = prompt | llm | parser
    result = chain.invoke({"input": description})

    # Debugging: Print the raw result for inspection
    #print("Raw Result:", result)

    if "Budget" in result:
        new_budget = result["Budget"]

        # Update or append items in the budget
        for new_item in new_budget.get("items", []):
            matched = False
            for existing_item in current_budget["items"]:
                if existing_item["item_name"] == new_item["item_name"]:
                    # Update existing item
                    existing_item.update(new_item)
                    matched = True
                    break
            if not matched:
                # Append new item if no match is found
                current_budget["items"].append(new_item)

        # Replace warnings with the latest warnings
        current_budget["warnings"] = new_budget.get("warnings", [])

    else:
        print("Warning: 'Budget' key missing in the result. Retaining the previous budget state.")

    # Append conversation
    if "conversation" in result:
        current_budget["conversations"].append(result["conversation"])
    else:
        print("Warning: 'conversation' key missing in the result. No conversation appended.")

    # Return the merged result with conversations included
    final_result = {
        "Budget": {
            "budget_limit": current_budget.get("budget_limit", 2000.0),
            "items": current_budget["items"],
            "warnings": current_budget["warnings"],
            "conversations": current_budget["conversations"]
        },
        "conversation": result.get("conversation", "I couldn't process your input fully. Could you try rephrasing?")
    }

    if conversation_collection is None:
        raise ValueError("MongoDB collection 'conversation_collection' is not initialized. Ensure 'connect_to_db' has been called.")
    
    # Replaces code below
    send_json_to_mongodb(final_result)
   
    '''
    if not conversation_collection:
        raise ValueError("Mongo")
    send_json_to_mongodb(final_result, conversation_collection)
    '''

    return final_result



def save_json_to_file(data):
    """
    Save the given JSON content to a file with the filename as a timestamp.
    :param data: The JSON-serializable data to be saved.
    :return: The filename of the saved file.
    """
    # Generate a timestamp-based filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}.json"

    # Save the data to the file
    with open(filename, "w") as json_file:
        json.dump(data, json_file, indent=4)

    print(f"Data successfully saved to {filename}")
    return filename


def get_conversation_string():
    """
    Retrieve the concatenated conversation string from the 'conversations' array in the current budget.
    :return: A single string containing all conversations, separated by newlines.
    """
    global current_budget

    # Ensure 'conversations' key exists
    if "conversations" not in current_budget:
        return "No conversations available."

    # Concatenate all conversations with newline separation
    conversation_string = "\n".join(current_budget["conversations"])
    return conversation_string.split("\n")[-1]




# # Example usage
# description1 = """
# My budget is $2500. I want to add a new recurring item: Utilities at $400, due on the 15th monthly.
# """
# parse_budget(description1)
# print("------"*5,"END OF 1ST PROMPT","------"*5 )
# description2 = """
# Update the groceries amount to $350. Delete car repairs from the budget. Will adding a $600 TV put me over budget?
# """
# parse_budget(description2)
# print("------"*5,"END OF 2ND PROMPT","------"*5 )
# description3 = """
# Can you tell me how to better manage my budget while staying under the limit?
# """
# parse_budget(description3)
# print("------"*5,"END OF 3RD PROMPT","------"*5 )


# chatprompt = "Starting chat"
# #print(chatprompt)
# while True:
#     description = input(chatprompt+": ")
#     if description != "-1":
#         parse_budget(description)
#         chatprompt = get_conversation_string()


