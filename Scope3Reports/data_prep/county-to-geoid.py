import pandas as pd
import yaml

csv_file = 'Ingredion_Supply_Shed.csv'
data_folder = "/Users/smohar/Development/cibo/my-scripts/Scope3Reports/Ingredion/data_prep/"
df = pd.read_csv(data_folder + csv_file)

data_by_name = {}

for _, row in df.iterrows():
    name = row['Supply Shed']
    county = row['County']
    state = row['State']
    fips = row['FIPS']
    
    if name not in data_by_name:
        data_by_name[name] = {
            'name': name, 
            'id': name.lower(), 
            'expansionGeometry': {'geoidPrefixes': []}
        }
    
    data_by_name[name]['expansionGeometry']['geoidPrefixes'].append(f"//{fips}// # {county}")

yaml_data = list(data_by_name.values())

yaml_file = csv_file[:-4] + '.yaml'  
with open(data_folder + yaml_file, 'w') as file:
    yaml.dump(yaml_data, file, default_flow_style=False)

with open(data_folder + yaml_file, 'r') as file:
    # Read the content of the file
    file_content = file.read()

# Replace the text
file_content = file_content.replace("'", "").replace("//", "'")

# Write the modified content back to the file
with open(data_folder + yaml_file, 'w') as file:
    file.write(file_content)

print(f"YAML file has been created: {yaml_file}")
