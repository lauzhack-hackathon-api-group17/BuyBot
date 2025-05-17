import os
from together import Together
from keys import TOGETHER_AI  # or replace with your API key
from data_categories_entries.data_categories import Categories

client = Together(api_key=TOGETHER_AI)

# --- CONFIGURABLE ATTRIBUTES ---
# Only take the n-2 first elements of the header to exclude price and link
ATTRIBUTES: list[str] = Categories.LAPTOPS.header[:-2]
DATABASE_FORMAT: str = ",".join(ATTRIBUTES)
# Number of example user queries and recommendations per query
N_QUERIES: int = 3
N_RECOMMENDATIONS: int = 10

PROMPT = f"""You are a laptop recommendation system. Your task is to provide laptop recommendations based on user needs and budget.
Your output should consist of only a CSV-formatted string and nothing else.
Here is the format of the database: {DATABASE_FORMAT}"""

# --- INSTRUCTION TEMPLATES ---
USER_GEN_INSTRUCTION = (
    f"Generate exactly {N_QUERIES} distinct user queries for a laptop recommendation system. "
    "Each query must be a single sentence, mention a clear budget (e.g., '$500'), and describe a primary use case. "
    "Ensure each query is unique and realistic, with varied user personas."
)

RECOMMENDATION_INSTRUCTION_TEMPLATE = (
    f"You are a laptop recommendation system.\n"
    f"Database format: {DATABASE_FORMAT}.\n"
    f"Based on the user's needs and budget, provide exactly {N_RECOMMENDATIONS} laptop recommendations in strict CSV format. "
    f"Ensure each row has exactly the following fields in order: {DATABASE_FORMAT}. "
    "Avoid repeating values across any column unless all reasonable alternatives are exhausted, allowing repetition only when necessary. "
    "Express display sizes in inches and weights in kg WITHOUT explicitly formatting units in the CSV (e.g., use only the numeric value)."
)

# --- FUNCTIONAL STEPS ---
def generate_user_inputs():
    response = client.chat.completions.create(
        model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
        messages=[{"role": "system", "content": USER_GEN_INSTRUCTION}],
        max_tokens=256,
        temperature=0.7,
    )
    lines = response.choices[0].message.content.strip().splitlines()
    queries: list[str] = []
    for line in lines:
        clean = line.strip().lstrip("-•1234567890. ").strip('"')
        # Skip any line that doesn't include a dollar budget
        if '$' not in clean:
            continue
        if clean:
            queries.append(clean)
        if len(queries) == N_QUERIES:
            break
    return queries


def generate_llm_outputs(user_inputs: list[str]) -> list[str]:
    outputs: list[str] = []
    system_msg = RECOMMENDATION_INSTRUCTION_TEMPLATE
    for user_query in user_inputs:
        messages = [
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_query}
        ]
        response = client.chat.completions.create(
            model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
            messages=messages,
            max_tokens=512,
            temperature=0.3,
        )
        outputs.append(response.choices[0].message.content.strip())
    return outputs


def save_constants_py(user_inputs: list[str], llm_outputs: list[str], file_path: str = "constants.py"):
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("# Define the database schema and user inputs\n")
        f.write(f'DATABASE_FORMAT = "{DATABASE_FORMAT}"\n\n')

        f.write("# Prompt template for recommendations\n")
        f.write(f'PROMPT = f"""{PROMPT}"""\n\n')

        f.write("USER_INPUTS = [\n")
        for user in user_inputs:
            f.write(f'    {user!r},\n')
        f.write("]\n\n")

        f.write("# LLM outputs as plain CSV strings per user\n")
        f.write("LLM_OUTPUTS = [\n")
        for output in llm_outputs:
            escaped = output.replace('"""', '\"\"\"')
            f.write(f'    """{escaped}""",\n\n')
        f.write("]\n")

    print(f"[✓] constants.py written with cleaned, diversified recommendations.")

# --- EXECUTION ---
if __name__ == "__main__":
    user_inputs = generate_user_inputs()
    llm_outputs = generate_llm_outputs(user_inputs)
    save_constants_py(user_inputs, llm_outputs)
