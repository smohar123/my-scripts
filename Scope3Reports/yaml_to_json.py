# A utility script that reads a YAML file and writes a JSON file.
#
# Usage: python yaml_to_json.py input.yaml output.json

import sys
import yaml
import json

if len(sys.argv) != 3:
    print("Usage: python yaml_to_json.py input.yaml output.json")
    sys.exit(1)

input_file = sys.argv[1]
output_file = sys.argv[2]

with open(input_file, 'r') as f:
    data = yaml.safe_load(f)

with open(output_file, 'w') as f:
    json.dump(data, f, indent=4)

print(f"Converted {input_file} to {output_file}")