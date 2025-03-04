import csv
import json
import argparse
import sys
from pathlib import Path
from typing import Dict, Any, List

def load_removal_mapping(csv_path: str) -> List[str]:
    """
    Load field IDs from CSV file.
    
    Args:
        csv_path: Path to CSV file containing field data
    
    Returns:
        List of field IDs
    """
    field_ids = []
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            field_ids.append(row['desc'])
    return field_ids

def process_file(input_path: Path, output_path: Path, removal_mapping: List[str]) -> None:
    """
    Process a single JSON file, applying the field removal logic and writing to output path.
    
    Args:
        input_path: Path to input JSON file
        output_path: Path where processed JSON should be written
        removal_mapping: List of field IDs to remove
    """
    with open(input_path, 'r') as f:
        data = json.load(f)
    
    # Process the data
    modified_data = [
        field for field in data if field["description"] not in removal_mapping
    ]
    
    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Write processed data
    with open(output_path, 'w') as f:
        json.dump(modified_data, f, indent=2)

def process_directory(source_dir: str, target_dir: str, removal_csv: str = None) -> None:
    """
    Process all JSON files in source directory, maintaining directory structure in target directory.
    
    Args:
        source_dir: Root directory containing JSON files to process
        target_dir: Directory where processed files should be written
        removal_csv: Optional path to CSV file containing field IDs to remove
    """
    source_path = Path(source_dir)
    target_path = Path(target_dir)
    
    # Load removal mapping if CSV provided
    removal_mapping = []
    if removal_csv:
        removal_mapping = load_removal_mapping(removal_csv)
    
    # Walk through source directory
    for input_file in source_path.rglob('growerdata.json'):
        # Calculate relative path to maintain directory structure
        rel_path = input_file.relative_to(source_path)
        output_file = target_path / rel_path
        
        print(f"Processing {input_file} -> {output_file}")
        process_file(input_file, output_file, removal_mapping)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Simplify JSON field configurations')
    parser.add_argument('source_dir', help='Source directory containing JSON files to process')
    parser.add_argument('target_dir', help='Target directory for processed JSON files')
    parser.add_argument('--removal-csv', help='Optional CSV file containing field IDs to remove')
    
    args = parser.parse_args()
    
    process_directory(args.source_dir, args.target_dir, args.removal_csv)