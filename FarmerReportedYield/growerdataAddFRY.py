import json
import random

# Ensures consistency between runs
random.seed(123)

with open('/Users/smohar/Downloads/ExampleScope3Results_Joel.json', 'r') as file:
    exampleS3Results_json = json.load(file)

with open('/Users/smohar/Downloads/growerdata.json', 'r') as file:
    growerdata_json = json.load(file)

zr_map = {}

# Loop through each farmer entry in the ExampleScope3Results data to get crop + simulatedYield
for farmer in exampleS3Results_json:
    yearlyEmissions = farmer["result"]["simulationResult"]["yearlyEmissions"]
    for year in yearlyEmissions:
        crop = year["crop"]
        simulatedYield = year["simulatedYield"]

        if (crop in zr_map):
            zr_map[crop].append(simulatedYield)
        else:
            zr_map[crop] = [simulatedYield]

# Loop through each farmer entry in growerdata and insert random farmer reported yield accd. to crop
for entry in growerdata_json:
    emissionsConfig = entry["configuration"]["emissionsConfig"]
    for year in emissionsConfig:
        crop = year["seasonalConfiguration"]["crop"]
        fry = random.choice(zr_map[crop])

        factor = 1
        while (factor == 1):
            factor = random.uniform(0.8, 1.2)

        year["seasonalConfiguration"]["farmerReportedYield"] = {}
        year["seasonalConfiguration"]["farmerReportedYield"]["yieldKgHa"] = fry["yieldKgHa"] * factor
        year["seasonalConfiguration"]["farmerReportedYield"]["displayYield"] = int(fry["displayYield"] * factor)
        year["seasonalConfiguration"]["farmerReportedYield"]["displayUnit"] = fry["displayUnit"]

with open('/Users/smohar/Downloads/updated_growerdata.json', 'w+') as f:
    json.dump(growerdata_json, f)