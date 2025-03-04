import json
import random

# Ensures consistency between runs
random.seed(123)

with open('/Users/smohar/Development/cibo/experiment-factory/carver/src/test/resources/ExampleScope3Results.json', 'r') as file:
    exampleS3Results_json = json.load(file)

with open('/Users/smohar/Development/cibo/experiment-factory/carver/src/test/resources/scope3-test-data/batchmode/unprepared_inputs/growerdata.json', 'r') as file:
    growerdata_json = json.load(file)

zr_map = {}

# Loop through each farmer entry in the ExampleScope3Results data to get crop + simulatedYield
for farmer in exampleS3Results_json:
    desc = farmer['desc']

    if desc == "BALLARD FARMS::SE 14-28-17 E.CIRCLE 100% MATT::SE 14-28-17 E.CIRCLE 100% MATT Trial":
        print("Found")

    yearlyEmissions = farmer["result"]["simulationResult"]["yearlyEmissions"]
    for year in yearlyEmissions:
        sy = year["simulatedYield"]

        if desc not in zr_map:
            zr_map[desc] = {}
        
        zr_map[desc][year['year']] = [sy['yieldKgHa'], sy['displayYield'], sy['displayUnit']]

# Loop through each farmer entry in growerdata and insert FRY
for entry in growerdata_json:
    emissionsConfig = entry["configuration"]["emissionsConfig"]
    desc = entry["description"]

    for year in emissionsConfig:
        current_year = year['seasonalConfiguration']['year']

        yieldKgHa, displayYield, displayUnit = zr_map[desc][current_year]

        factor = random.uniform(0.8, 1.2)

        year["seasonalConfiguration"]["farmerReportedYield"] = {}
        year["seasonalConfiguration"]["farmerReportedYield"]["yieldKgHa"] = yieldKgHa * factor
        year["seasonalConfiguration"]["farmerReportedYield"]["displayYield"] = int(displayYield * factor)
        year["seasonalConfiguration"]["farmerReportedYield"]["displayUnit"] = displayUnit

with open('/Users/smohar/Development/cibo/experiment-factory/carver/src/test/resources/scope3-test-data/batchmode/unprepared_inputs/updated_growerdata.json', 'w+') as f:
    json.dump(growerdata_json, f)
