import json

# Open the JSON file and load its content
with open('/Users/smohar/Development/cibo/experiment-factory/carver/src/test/resources/ExampleScope3Results.json', 'r') as file:
    json_data = json.load(file)

first = True

# Loop through each farmer entry in the JSON data
for farmer in json_data:
    location_id = farmer["locationId"]
    yearly_emissions = farmer["result"]["simulationResult"]["yearlyEmissions"]
    applied_configuration = farmer["result"]["appliedConfiguration"]
    
    for oneYear in range(0, len(yearly_emissions)):
        applied_configuration[oneYear]["farmerReportedYield"] = yearly_emissions[oneYear]["simulatedYield"].copy()

        applied_configuration[oneYear]["farmerReportedYield"]["yieldKgHa"] = yearly_emissions[oneYear]["simulatedYield"]["yieldKgHa"] / 2
        applied_configuration[oneYear]["farmerReportedYield"]["displayYield"] = int(yearly_emissions[oneYear]["simulatedYield"]["displayYield"] / 2)
        applied_configuration[oneYear]["farmerReportedYield"]["displayUnit"] = yearly_emissions[oneYear]["simulatedYield"]["displayUnit"]


with open('/Users/smohar/Downloads/updated_ExampleScope3Results.json', 'w+') as f:
    json.dump(json_data, f)