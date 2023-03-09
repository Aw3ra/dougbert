import os
import json

# ---------------------------------------------------------------------------------#
# Function too return data from a json file
# Inputs:  Name - the name of the json file
# Outputs: data - the data from the json file
# ---------------------------------------------------------------------------------#
def find_json_file(json_name):
    json_file_name = json_name
    for root, dirs, files in os.walk(os.getcwd()):
        if json_file_name in files:
            with open(os.path.join(root, json_file_name), "r") as f:
                data = json.load(f)
            return data
    return "Error: JSON file not found."