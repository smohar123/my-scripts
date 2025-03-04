import csv
import json
import argparse
import sys
from pathlib import Path
from typing import Dict, Any

properties_to_remove = [
    "useRasterAgronomoModels",
    "maturity",
    "variety",
    "gduSilking",
    "gduMaturity",
    "kernelPotential",
    "kernelFillRate",
    "plantingDensity",
    "plantingDay",
    "harvestDay",
    "residueRemovalPct",
    "fertilizer",
    "fertilizerReduction",
    "irrigation",
    "irrigationEvents",
    "tillageEvents",
    "coverCropType",
    "coverCropParams",
    "grazingInformation",
    "transportationMiles",
    "biomassBurningFraction",
    "irrigationFuelInfo"
]

def load_tillage_mapping(csv_path: str) -> Dict[str, Dict[int, str]]:
    """
    Load field ID to yearly tillage mapping from CSV file.
    
    Args:
        csv_path: Path to CSV file containing field data
    
    Returns:
        Dictionary mapping field IDs to their yearly tillage values
        
        Valid Values:
        MoldboardPlow, Conventional, Conservation, NoTill
    """
    def fix_tillage(tillage: str) -> str:
        fixed = tillage.replace('Tillage', '') \
               .replace('No Till', 'NoTill') \
               .strip()
        if fixed not in ['MoldboardPlow', 'Conventional', 'Conservation', 'NoTill']:
            raise ValueError(f"Invalid tillage value: {tillage}")
        return fixed
    
    tillage_mapping = {}
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            field_id = row['Field ID']
            tillage_mapping[field_id] = {}
            for year in range(2017, 2025):
                tillage_year = row[f'{year} Tillage'] or 'Conventional'
                if tillage_year:  # Only add if tillage value exists
                    tillage_mapping[field_id][year] = fix_tillage(tillage_year)
    return tillage_mapping

def remove_properties(obj: Any, field_id: str, tillage_mapping: Dict[str, str], best_case: bool = False, worst_case: bool = False, omit_geometry: bool = False) -> Any:
    """
    Recursively remove specified properties from seasonalConfiguration in a JSON object.
    
    Args:
        obj: Dictionary representing the JSON object
        properties_to_remove: List of property names to remove from seasonalConfiguration
    
    Returns:
        Modified dictionary with specified properties removed
    """
    if isinstance(obj, dict):
        if omit_geometry and 'geometry' in obj:
            del obj["geometry"]
        if "seasonalConfiguration" in obj:
            # Handle tillageSelection lookup if it's empty
            if "tillageSelection" in obj["seasonalConfiguration"] and not obj["seasonalConfiguration"]["tillageSelection"]:
                if field_id in tillage_mapping:
                    year = obj["seasonalConfiguration"]["year"]
                    obj["seasonalConfiguration"]["tillageSelection"] = tillage_mapping[field_id][year]
                        
            for prop in properties_to_remove:
                obj["seasonalConfiguration"].pop(prop, None)
                
            if best_case and worst_case:
                raise ValueError("Cannot specify both best_case and worst_case")
            elif best_case:
                obj["seasonalConfiguration"]["tillageSelection"] = "NoTill"
                obj["seasonalConfiguration"]["hasCoverCrop"] = True
            elif worst_case:
                obj["seasonalConfiguration"]["tillageSelection"] = "Conventional"
                obj["seasonalConfiguration"]["hasCoverCrop"] = False

        # Recursively process nested dictionaries
        return {k: remove_properties(v, field_id, tillage_mapping, best_case, worst_case, omit_geometry) for k, v in obj.items()}
    elif isinstance(obj, list):
        # Recursively process list items
        return [remove_properties(item, field_id, tillage_mapping, best_case, worst_case, omit_geometry) for item in obj]
    else:
        return obj

def process_file(input_path: Path, output_path: Path, tillage_mapping: Dict[str, str], best_case: bool = False, worst_case: bool = False) -> None:
    """
    Process a single JSON file, applying the property removal logic and writing to output path.
    
    Args:
        input_path: Path to input JSON file
        output_path: Path where processed JSON should be written
        tillage_mapping: Dictionary of field ID to tillage mappings
        best_case: Generate best case JSON
        worst_case: Generate worst case JSON
    """
    with open(input_path, 'r') as f:
        data = json.load(f)
    
    # Process the data
    modified_data = [
        remove_properties(field, field_id=field["description"], tillage_mapping=tillage_mapping, best_case=best_case, worst_case=worst_case, omit_geometry=False)
        for field in data
    ]
    
    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Write processed data
    with open(output_path, 'w') as f:
        json.dump(modified_data, f, indent=2)

def process_directory(source_dir: str, target_dir: str, tillage_csv: str = None, best_case: bool = False, worst_case: bool = False) -> None:
    """
    Process all JSON files in source directory, maintaining directory structure in target directory.
    
    Args:
        source_dir: Root directory containing JSON files to process
        target_dir: Directory where processed files should be written
        tillage_csv: Optional path to CSV file containing tillage mappings
        best_case: Generate best case JSON
        worst_case: Generate worst case JSON
    """
    source_path = Path(source_dir)
    target_path = Path(target_dir)
    
    # Load tillage mapping if CSV provided
    tillage_mapping = {}
    if tillage_csv:
        tillage_mapping = load_tillage_mapping(tillage_csv)
    
    # Walk through source directory
    for input_file in source_path.rglob('growerdata.json'):
        # Calculate relative path to maintain directory structure
        rel_path = input_file.relative_to(source_path)
        output_file = target_path / rel_path
        
        print(f"Processing {input_file} -> {output_file}")
        process_file(input_file, output_file, tillage_mapping, best_case, worst_case)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Simplify JSON field configurations')
    parser.add_argument('source_dir', help='Source directory containing JSON files to process')
    parser.add_argument('target_dir', help='Target directory for processed JSON files')
    parser.add_argument('--tillage-csv', help='Optional CSV file containing tillage mappings')
    parser.add_argument('--best-case', action='store_true', help='Generate best case JSON')
    parser.add_argument('--worst-case', action='store_true', help='Generate worst case JSON')
    
    args = parser.parse_args()
    
    process_directory(args.source_dir, args.target_dir, args.tillage_csv, args.best_case, args.worst_case)