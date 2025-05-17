import time
from together import Together
from keys import TOGETHER_AI  # or replace with your API key
from data_categories_entries.data_categories import Categories
from utils import get_possibilities

client = Together(api_key=TOGETHER_AI)

MODEL = "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free"

# --- CONFIGURABLE ATTRIBUTES ---
# Only take the n-2 first elements of the header to exclude price and link
ATTRIBUTES: list[str] = Categories.LAPTOPS.header[:-2]
DATABASE_FORMAT: str = ",".join(ATTRIBUTES)
# Number of example user queries and recommendations per query
N_QUERIES: int = 3
N_RECOMMENDATIONS: int = 10
MAX_API_CALLS: int = 10  # Max API calls to avoid rate limits

PROMPT = f"""You are a laptop recommendation system. Your task is to provide laptop recommendations based on user needs and budget.
Your output should consist of only a CSV-formatted string and nothing else.
Here is the format of the database: {DATABASE_FORMAT}"""

# --- INSTRUCTION TEMPLATES ---
USER_GEN_INSTRUCTION = (
    f"Generate exactly {N_QUERIES} distinct user queries for a laptop recommendation system. "
    "Each query must be a single sentence, for some queries mention a clear budget (e.g., '500CHF', '2500CHF') but some other times don't. "
    "The queries should cover a range of user needs, such as gaming, business, travel, and education etc... "
    "Ensure each query is unique and realistic, with varied user personas."
)

RECOMMENDATION_INSTRUCTION_TEMPLATE = (
    f"You are a laptop recommendation system that provides highly realistic, diverse, and technically accurate laptop recommendations.\n"
    f"Database format: {DATABASE_FORMAT}.\n"
    f"Based on the user's needs and budget, provide exactly {N_RECOMMENDATIONS} laptop recommendations in strict CSV format. "
    f"Ensure each row has exactly the following fields in order: {DATABASE_FORMAT}.\n\n"
    "Important requirements:\n"
    f"1. For some components/specifications, you can only use the values from these lists: {get_possibilities()} except for the price and weight which you should aggregate from the database.\n"
    f"2. Each recommendation must be REALISTIC with your market estimation from current date: {time.strftime('%Y-%m-%d')} and the components you can use.\n"
    "3. Create HIGH DIVERSITY across all recommendations - vary brands, models, categories, CPUs, etc.\n"
    "4. Scale specs appropriately to user's budget and needs (higher budget = better specs).\n"
    "5. Provide varied storage options based on price point and user needs. (e.g Video/Photo = More Storage, Buisness = Less Storage)\n"
    "6. Ensure each recommendation is unique - NO duplicated models or specs except when absolutely unavoidable.\n"
    "7. Express display sizes in inches and weights in kg WITHOUT explicitly formatting units in the CSV (e.g., use only the numeric value)."
    "8. More importantly, take into account the typical user's profile to ensure the recommendations are suitable for their needs.\n"
)

# --- FUNCTIONAL STEPS ---
def generate_user_inputs():
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": USER_GEN_INSTRUCTION}
        ],
        max_tokens=min(512 * N_QUERIES, 2048),
        temperature=0.7,
    )
    
    # Extract the actual queries from the LLM response
    raw_text = response.choices[0].message.content.strip()
    lines = raw_text.splitlines()
    
    queries: list[str] = []
    
    # First pass: collect all valid queries
    all_valid_queries = []
    for line in lines:
        clean = line.strip().lstrip("-•1234567890. ").strip('"')
        if not clean or clean.lower().startswith(("here", "these", "following")):
            continue
        all_valid_queries.append(clean)
    
    # Critical bug fix: We were decrementing max_api_calls_left incorrectly
    # MAX_API_CALLS refers to the entire API usage limit, not per query
    
    # Second pass: collect queries with budget first
    for query in all_valid_queries:
        if "CHF" in query and len(queries) < N_QUERIES:
            queries.append(query)
            
    # Third pass: add queries without budget until we reach N_QUERIES
    for query in all_valid_queries:
        if "CHF" not in query and len(queries) < N_QUERIES:
            queries.append(query)
    
    # If we don't have enough queries, generate more
    if len(queries) < N_QUERIES:
        print(f"[!] Warning: Only generated {len(queries)} valid queries. Filling with defaults.")
        default_queries = [
            "I need a laptop for programming and software development under 1500CHF.",
            "Looking for a lightweight laptop for writing and web browsing.",
            "Need a powerful gaming laptop with excellent graphics and cooling."
        ]
        queries.extend(default_queries[:(N_QUERIES - len(queries))])
    
    return queries[:N_QUERIES]  # Ensure we return exactly N_QUERIES


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
            model=MODEL,
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