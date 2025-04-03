import json
import csv
from collections import defaultdict

# Step 1: Read the CSV file and create a dictionary of (County, State) -> Group
def read_csv(csv_filename):
    group_mapping = {}
    with open(csv_filename, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            county_state = (row['County'], row['State'])
            group_mapping[county_state] = row['Supply Shed']
    return group_mapping

# Step 2: Read the original JSON file that contains geometry and other fields
def read_original_json(json_filename):
    with open(json_filename, mode='r') as file:
        return json.load(file)

# Step 3: Read the GeoJSON file and create a dictionary of (geometry) -> (County, State)
def read_geojson(geojson_filename):
    with open(geojson_filename, mode='r') as file:
        geojson_data = json.load(file)
    
    geojson_mapping = {}
    for feature in geojson_data['features']:
        geometry = json.dumps(feature['geometry']['coordinates'])  # Serialize coordinates for easy comparison
        county = feature['properties']['County']
        state = feature['properties']['State']
        geojson_mapping[geometry] = (county, state)  # Map geometry to (County, State)
    return geojson_mapping

# Step 4: Create the new JSON files for each group
def create_group_json_files(original_json, group_mapping, geojson_mapping):
    # Group entries by their group name
    groups = defaultdict(list)
    
    for entry in original_json:
        # Get the geometry as a JSON string to compare it easily
        geometry_str = json.dumps(entry['geometry']['coordinates'])
        
        # Match geometry with the GeoJSON
        county_state = geojson_mapping.get(geometry_str)
        
        if county_state:
            county, state = county_state
            # Get the group for the county-state pair
            group = group_mapping.get((county, state))
            if group:
                # Add the entry to the appropriate group without modifying properties
                groups[group].append(entry)
    
    # Write out separate JSON files for each group
    for group, entries in groups.items():
        output_filename = f'{group}_data.json'
        with open(output_filename, 'w') as outfile:
            json.dump(entries, outfile, indent=4)
        print(f'Created {output_filename} with {len(entries)} entries')

# Main execution
csv_filename = 'Ingredion_Supply_Shed.csv'
original_json_filename = 'growerdata.jsons/growerdata_ingredion_int.json'
geojson_filename = 'growerdata.jsons/expanded_growerdata_int.geojson'

group_mapping = read_csv(csv_filename)
original_json = read_original_json(original_json_filename)
geojson_mapping = read_geojson(geojson_filename)

create_group_json_files(original_json, group_mapping, geojson_mapping)
