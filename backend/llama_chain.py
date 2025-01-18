from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pandas import describe_option
from main import get_api
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
                }
            },
            "required": ["budget_limit", "items"]
        }
    },
    "required": ["Budget"]
})

# Create a prompt to extract budget details
prompt = ChatPromptTemplate.from_messages([
    ("system", """Extract budget details into JSON with this structure:
        {{
            "Budget": {{
                "budget_limit": 2000.0,
                "items": [
                    {{
                        "item_name": "Rent",
                        "amount": 1200.0,
                        "category": "Recurring",
                        "importance_rank": 1,
                        "recurrence_schedule": "monthly",
                        "due_date": 1
                    }},
                    {{
                        "item_name": "Groceries",
                        "amount": 300.0,
                        "category": "Regular",
                        "importance_rank": 2,
                        "recurrence_schedule": "weekly",
                        "due_date": null
                    }}
                ]
            }}
        }}"""),
    ("user", "{input}")
])

# Create the chain that ensures the output matches the JSON structure
chain = prompt | llm | parser

def parse_budget(description: str) -> dict:
    """
    Parse a budget description into the expected JSON format.
    :param description: The textual description of the budget.
    :return: Parsed JSON object.
    """
    result = chain.invoke({"input": description})
    print(json.dumps(result, indent=2))
    return result

# Example usage
# description = """
# My budget has a limit of $2500. For recurring expenses, I have rent at $1200 monthly, due on the 1st of every month.
# Groceries cost about $300 weekly. My irregular expenses include car repairs, which are about $500 but happen unpredictably.
# """
description = input("Enter your budget stuff: ")
parse_budget(description)
