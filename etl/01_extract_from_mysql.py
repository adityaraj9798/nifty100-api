import os
import re
import csv
import ast

# Define Paths
SQL_FILE_PATH = 'data/scriptticker.sql'
RAW_DATA_DIR = 'data/raw/'

def parse_sql_values(values_string):
    """
    Safely parses SQL value strings handling NULLs and quotes.
    Converts SQL NULL to Python None.
    """
    # Replace SQL NULL with Python None string representation for ast.literal_eval
    cleaned_string = re.sub(r'\bNULL\b', 'None', values_string, flags=re.IGNORECASE)
    
    try:
        # Evaluate the string as a Python literal (tuple)
        # We wrap it in a tuple format to handle multi-row inserts like: (1,2), (3,4)
        parsed_tuples = ast.literal_eval(f"({cleaned_string})")
        
        # If it's a single tuple insert, wrap it in a list so it's iterable
        if isinstance(parsed_tuples[0], (int, float, str, type(None))):
            return [parsed_tuples]
        return parsed_tuples
    except Exception as e:
        print(f"Error parsing values: {e}")
        return []

def extract_tables_from_sql():
    print("Starting extraction process...")
    
    # Regex to capture table name and the values block
    insert_pattern = re.compile(r"INSERT INTO `?([a-zA-Z0-9_]+)`?.*?(?:VALUES|\()(.+)\);", re.IGNORECASE)
    
    table_files = {}
    table_writers = {}
    row_counts = {}

    try:
        with open(SQL_FILE_PATH, 'r', encoding='utf-8', errors='replace') as file:
            for line_number, line in enumerate(file, 1):
                if line.upper().startswith('INSERT INTO'):
                    match = insert_pattern.search(line)
                    if match:
                        table_name = match.group(1).lower()
                        values_block = match.group(2)

                        # Initialize CSV writer for a new table
                        if table_name not in table_files:
                            csv_path = os.path.join(RAW_DATA_DIR, f"{table_name}.csv")
                            file_handle = open(csv_path, 'w', newline='', encoding='utf-8')
                            table_files[table_name] = file_handle
                            table_writers[table_name] = csv.writer(file_handle)
                            row_counts[table_name] = 0
                            print(f"Discovered table: {table_name} -> Creating CSV.")

                        # Parse the values and write to CSV
                        rows = parse_sql_values(values_block)
                        for row in rows:
                            # Convert None back to empty string for clean CSV output
                            cleaned_row = ["" if item is None else item for item in row]
                            table_writers[table_name].writerow(cleaned_row)
                            row_counts[table_name] += 1

    except FileNotFoundError:
        print(f"CRITICAL ERROR: Could not find the SQL file at {SQL_FILE_PATH}")
        return

    finally:
        # Ensure all files are closed cleanly
        for file_handle in table_files.values():
            file_handle.close()

    print("\n--- Extraction Complete ---")
    for table, count in row_counts.items():
        print(f"Table '{table}': {count} rows extracted.")

if __name__ == "__main__":
    extract_tables_from_sql()