import os

def create_database(llm_output: str, directory_name: str = "database") -> None:
    """
    Converts a CSV-formatted string into a file named 'database.csv' inside a given directory.
    
    Args:
        llm_output (str): The raw CSV string from an LLM (should include header).
        directory_name (str): Name of the directory to store the database. Default is 'database_dir'.
    """
    # Ensure the directory exists
    os.makedirs(directory_name, exist_ok=True)

    # Define the file path
    file_path = os.path.join(directory_name, "database.csv")

    # Write the CSV content
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(llm_output.strip())

    print(f"Database saved to: {file_path}")