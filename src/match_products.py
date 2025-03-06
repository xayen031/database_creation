import pandas as pd
import os
from fuzzywuzzy import process
from pathlib import Path

def find_best_match(product_name, txt_files):
    """
    Finds the best matching text file name for the given product name.
    """
    best_match, score = process.extractOne(product_name, txt_files)
    return best_match if score > 70 else None  # Only accept matches above a threshold

def match_product_names(csv_path, txt_folder, output_csv):
    """
    Matches product names from the CSV file with the closest text file names in the given folder.
    """
    # Load CSV file
    df = pd.read_csv(csv_path)
    
    # Ensure PRODUCT_NAME column exists
    if 'PRODUCT_NAME' not in df.columns:
        raise ValueError("CSV file must contain a PRODUCT_NAME column")
    
    # Get list of text file names (without extensions)
    txt_files = {f.stem: f for f in Path(txt_folder).glob("*.txt")}
    
    # Match each product name with the best text file name
    matched_paths = []
    for product in df['PRODUCT_NAME']:
        best_match = find_best_match(product, txt_files.keys())
        matched_paths.append(txt_files[best_match].resolve() if best_match else None)
    
    # Add new column to dataframe
    df['MATCHED_FILE_PATH'] = matched_paths
    
    # Save updated CSV
    df.to_csv(output_csv, index=False)
    print(f"Updated CSV saved to {output_csv}")

# Example usage
if __name__ == "__main__":
    csv_file = "database.csv"  # Change to your actual CSV file path
    txt_directory = "instructions"  # Change to your actual directory containing text files
    output_file = "database_updated.csv"
    
    match_product_names(csv_file, txt_directory, output_file)