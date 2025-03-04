import json
import os

def merge_json_files(input_dir, output_file):
    merged_data = []

    for filename in os.listdir(input_dir):
        file_path = os.path.join(input_dir, filename)
        
        if filename.endswith('.json'):
            with open(file_path, 'r') as file:
                data = json.load(file)
                merged_data.extend(data)  #
    
    with open(output_file, 'w') as output:
        json.dump(merged_data, output, indent=4)

input_directory = 'growerdata'  
output_filename = 'merged_growerdata.json'  
merge_json_files(input_directory, output_filename)
