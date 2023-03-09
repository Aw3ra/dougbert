import json
import os

# ---------------------------------------------------------------------------------#
# Function to return a prompt based on a personality from a json file
# Inputs:   Message - The message sent to the bot
# Outputs:  String  - A response to send back to discord, denoting personalities
# ---------------------------------------------------------------------------------#
def return_personalities(message):
    path = os.path.join(os.path.dirname(__file__), '..', '..', 'personalities.json')
    # Load the json file
    with open(path, 'r') as f:
        data = json.load(f)
    # Array to store the characters
    personalities = []
    # Loop through the json file and add the characters to the array
    for personality in data['personalities']:
        this_one = []
        this_one.append(personality['name'])
        this_one.append(personality['description'])
        personalities.append(this_one)
    # Loop through the personalities and return the one that matches the message
    for personality in personalities:
        if personality[0].lower() in message.lower():
            return personality[0]+': '+personality[1]
    # If no personality is found, return all personalities as a list
    return_list = 'The personalities I have are:\n'
    for personality in personalities:
        return_list += personality[0]+': '+personality[1]+'\n\n'
    return return_list[:-2]
