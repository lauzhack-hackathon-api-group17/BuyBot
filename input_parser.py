import os
import time
from together import Together
from constants import PROMPT, USER_INPUTS, LLM_OUTPUTS
from keys import TOGETHER_AI
from utils import get_possibilities

# Instantiate the Together client (it will also read TOGETHER_API_KEY from env if not passed)
client = Together(api_key=TOGETHER_AI)
N_RECOMMENDATIONS = 20

def get_laptop_recommendations(user_input: str) -> str:
    """
    Get laptop recommendations based on user input using Together AI.
    Returns a CSV string following the expected format.
    """
    # 1. Start with the system prompt
    full_prompt = PROMPT + f"""
        You are working with a database. Use only the following values for certain fields:
        Possible field values: {get_possibilities()}

        Note: The current date is {time.strftime('%Y-%m-%d')}.
        - Some components may have changed in price since your last training data.
        - Some components may be newly released and not present in your knowledge.
        - You should aggregate the price and weight from the database.

        Please proceed accordingly.
    """
    messages = [
        {"role": "system", "content": full_prompt}
    ]

    # 2. Add our example pairs
    for user_example, assistant_example in zip(USER_INPUTS, LLM_OUTPUTS):
        messages.append({"role": "user", "content": user_example})
        messages.append({"role": "assistant", "content": assistant_example})

    # 3. Finally, add the actual user query
    messages.append({"role": "user", "content": user_input})

    # 4. Call the Together AI chat completion endpoint
    response = client.chat.completions.create(
        model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
        messages=messages,
        max_tokens=min(512 * N_RECOMMENDATIONS, 4096),
        temperature=0.2,
    )

    # 5. Extract and return the content
    return response.choices[0].message.content


def create_database(llm_output: str, directory_name: str = "database", filename = "specs_database.csv") -> None:
    """
    Converts a CSV-formatted string into a csv file and saves it to a specified directory. 
    
    Args:
        llm_output (str): The raw CSV string from an LLM (should include header).
        directory_name (str): Name of the directory to store the database. Default is 'database_dir'.
    """
    # Ensure the directory exists
    os.makedirs(directory_name, exist_ok=True)

    # Define the file path
    file_path = os.path.join(directory_name, filename)

    # Write the CSV content
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(llm_output.strip())

    print(f"Database saved to: {file_path}")

def create_specs_database(user_input: str) -> None:
    recommendations = get_laptop_recommendations(user_input)
    
    print(recommendations)

    create_database(recommendations)
    
    return recommendations