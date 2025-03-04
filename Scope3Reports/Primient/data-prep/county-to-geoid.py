import pandas as pd
import yaml

csv_file = 'PrimientSupplySheds11.20.24.csv'
df = pd.read_csv(csv_file)

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
    
    data_by_name[name]['expansionGeometry']['geoidPrefixes'].append(f"'{fips}' # {county}")

yaml_data = list(data_by_name.values())

yaml_file = 'output.yaml'  
with open(yaml_file, 'w') as file:
    yaml.dump(yaml_data, file, default_flow_style=False)

print(f"YAML file has been created: {yaml_file}")
