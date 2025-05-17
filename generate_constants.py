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
    f"You are a laptop recommendation system that provides highly realistic, diverse, and technically accurate laptop recommendations.\n"
    f"Database format: {DATABASE_FORMAT}.\n"
    f"Based on the user's needs and budget, provide exactly {N_RECOMMENDATIONS} laptop recommendations in strict CSV format. "
    f"Ensure each row has exactly the following fields in order: {DATABASE_FORMAT}.\n\n"
    "Important requirements:\n"
    "1. Each recommendation must be REALISTIC with current market specifications and models as of 2024.\n"
    "2. Create HIGH DIVERSITY across all recommendations - vary brands, models, categories, CPUs, etc.\n"
    "3. Match specifications accurately to real-world laptop segments and price points.\n"
    "4. Scale specs appropriately to user's budget and needs (higher budget = better specs).\n"
    "5. Include diverse brands: Dell, HP, Lenovo, Apple, Asus, MSI, Acer, Microsoft, LG, Samsung, Razer, Gigabyte, etc.\n"
    "6. Use accurate CPU naming conventions like 'Intel Core i7-13700H', 'AMD Ryzen 7 7840U', 'Apple M3 Pro', etc.\n"
    "7. Include realistic GPU options from 'Intel Iris Xe', 'AMD Radeon 780M' to 'NVIDIA RTX 4070' depending on budget.\n"
    "8. Provide varied storage options from 256GB to 2TB based on price point.\n"
    "9. Ensure each recommendation is unique - NO duplicated models or specs except when absolutely unavoidable.\n"
    "10. Express display sizes in inches and weights in kg WITHOUT explicitly formatting units in the CSV (e.g., use only the numeric value)."
)

# --- FUNCTIONAL STEPS ---
def generate_user_inputs():
    response = client.chat.completions.create(
        model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": USER_GEN_INSTRUCTION}
        ],
        max_tokens=min(256 * N_QUERIES, 2048),
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
    
    for idx, user_query in enumerate(user_inputs):
        # Customize instructions for each query type to further diversify results
        custom_instruction = RECOMMENDATION_INSTRUCTION_TEMPLATE
        
        # Add query-specific guidance to prevent repetition across different queries
        if idx == 0:
            custom_instruction += "\nFocus on mid-range workstation and creator laptops suitable for the specified budget."
        elif idx == 1:
            custom_instruction += "\nFocus on budget-friendly, lightweight options with good battery life that match the lower price point."
        else:
            custom_instruction += "\nFocus on high-performance professional workstations or gaming laptops converted for professional use."
        
        messages = [
            {"role": "system", "content": custom_instruction},
            {"role": "user", "content": f"Query: {user_query}\n\nProvide {N_RECOMMENDATIONS} diverse recommendations that would suit this need and budget."}
        ]
        
        response = client.chat.completions.create(
            model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
            messages=messages,
            max_tokens=min(256 * N_RECOMMENDATIONS, 4096),  # Increased token limit
            temperature=0.5,  # Balanced temperature for creativity and accuracy
        )
        
        # Clean the output to ensure it's proper CSV format
        raw_output = response.choices[0].message.content.strip()
        cleaned_output = clean_csv_output(raw_output)
        outputs.append(cleaned_output)
        
    return outputs


def clean_csv_output(raw_output: str) -> str:
    """Clean and normalize CSV output from LLM to ensure proper formatting"""
    lines = raw_output.strip().split('\n')
    cleaned_lines = []
    
    # Skip header line if present (starts with Brand or contains all attribute names)
    for line in lines:
        if line.startswith("Brand,") or all(attr.lower() in line.lower() for attr in ATTRIBUTES):
            continue
        # Remove any line numbers, bullets, or other prefixes
        clean_line = line.strip().lstrip("-•1234567890. ")
        # Skip empty lines or lines with incomplete data
        if clean_line and "," in clean_line:
            # Ensure we have the expected number of fields
            fields = clean_line.split(',')
            if len(fields) >= len(ATTRIBUTES):
                # Keep only the fields we need in case there are extra fields
                cleaned_lines.append(",".join(fields[:len(ATTRIBUTES)]))
    
    return "\n".join(cleaned_lines)


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