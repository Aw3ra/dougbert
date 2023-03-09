from handlers import openAI_handler, mongo_handler
import json
import random
import os

# ---------------------------------------------------------------------------------#
# Function to generate a tweet
# This function is called from the discord bot, and returns a string generated from
# the appropriate function. The string is then sent to discord.
# The command is extracted from the message using openAI_handler.decide_action
# Inputs:   Message - The message sent to the bot
# Outputs:  String  - The string to send to discord
# ---------------------------------------------------------------------------------#
def generate_tweet(message):
    # Retrieve the tweet from the database
    base_tweet = random.choice(mongo_handler.decide_action('read', collection = 'scraped_tweets'))
    # Personality
    personality = get_prompt(message)
    # The prompt to send along with the message to generate a tweet
    prompt = 'You are '+personality[1]+' rewrite the following tweet to make it sound more like you: '+base_tweet['text']
    # Get the tweet from the openAI handler
    tweet = openAI_handler.decide_action('text', prompt=prompt, max_tokens=512).replace('\n', '')
    # Add the tweet to the database
    added = mongo_handler.decide_action('add', collection = 'generated_tweets', query = {'altered_tweet': tweet, 'original_tweet': base_tweet['text'],'approved': False, 'used': False, 'aiName':personality[0]})
    if added:
        return tweet
    else:
        return added

# ---------------------------------------------------------------------------------#
# Function to return a prompt based on a personality from a json file
# Inputs:   Message - The message sent to the bot
# Outputs:  String  - The string to send to openAI
# ---------------------------------------------------------------------------------#
def get_prompt(message):
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
            return personality
    # If no personality is found, return a random personality
    return random.choice(personalities)