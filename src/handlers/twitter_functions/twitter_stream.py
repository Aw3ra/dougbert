import tweepy
import os
from dotenv import load_dotenv
from handlers import twitter_handler, mongo_handler
from general_functions import find_json

# TODO: Clean up code, add comments, add error handling


# ---------------------------------------------------------------------------------#
# Get consumer keys
# TODO: Remove this and have auth passed in (potentially from twitter handler)
# ---------------------------------------------------------------------------------#
try:
    MY_BEARER_TOKEN = os.environ['TWITTER_BEARER_TOKEN']
except:
    load_dotenv()
    MY_BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN')


# Authenticate to Twitter using the keys for the twitter bot account
db_client = tweepy.Client(
consumer_key=os.getenv('DOUGBERT_CONSUMER_KEY'), consumer_secret=os.getenv('DOUGBERT_CONSUMER_SECRET'),
access_token=os.getenv('DOUGBERT_ACCESS_TOKEN') , access_token_secret=os.getenv('DOUGBERT_ACCESS_TOKEN_SECRET'))
fall_back_client = tweepy.Client(MY_BEARER_TOKEN)

# ---------------------------------------------------------------------------------#
# Class to handle the stream
# Inputs:   tweepy.StreamingClient - the class to inherit from
# Outputs:  None
# Methods:  on_connect - function to do something on stream connect
#           on_disconnect - function to do something on stream disconnect
#           on_error - function to do something on stream error
#           add_written_rules - function to add rules to the stream from a json file
#           delete_written_rules - function to delete rules from the stream from a json file
#           on_tweet - function to do something on a tweet
# ---------------------------------------------------------------------------------#
class DBStreaming(tweepy.StreamingClient):
    # -----------------------------------------------------------------------------#
    # Function to do something on stream connect
    # Input: None
    # Output: None
    # -----------------------------------------------------------------------------#
    def on_connect(self):
        print("Stream connected")
    # -----------------------------------------------------------------------------#

    # -----------------------------------------------------------------------------#
    # Function to do something on stream disconnect
    # Input: None
    # Output: None
    # -----------------------------------------------------------------------------#
    # TODO: Add a way to reconnect if needed
    # TODO: maybe global variable for connection status
    # TODO: Post disconnect to database and/or discord instead of printing
    def on_disconnect(self):
        print("Stream disconnected")
    # -----------------------------------------------------------------------------#

    # -----------------------------------------------------------------------------#
    # Function to do something on stream error
    # Input: status_code
    # Output: False
    # -----------------------------------------------------------------------------#
    # TODO: Instead of returning false, add a way to reconnect
    # TODO: Post error to database and/or discord instead of printing
    def on_error(self, status_code):
        print("Stream error:", status_code)
        return False
    # -----------------------------------------------------------------------------#

    # -----------------------------------------------------------------------------#
    # Function to add rules to the stream from a json file
    # Input: None
    # Output: None
    # -----------------------------------------------------------------------------#
    def add_written_rules(self):
        # Get rules from json file
        rules = find_json.find_json_file('rules.json')
        # For each in rules
        for set in rules:
            for rule in set.keys():
                # Add the rule to the stream
                rule = tweepy.StreamRule(rule)
                print(rule)
                self.add_rules(rule)
    # -----------------------------------------------------------------------------#

    # -----------------------------------------------------------------------------#
    # Function to delete all rules from the stream
    # Input: None
    # Output: None
    # -----------------------------------------------------------------------------#
    def delete_written_rules(self):
        # Get rules from the stream
        rules = self.get_rules()
        # Check if rules has data
        if rules.data:
            for rule in rules.data:
                self.delete_rules(rule)
        else:
            print("No rules to delete")
    # -----------------------------------------------------------------------------#

    # -----------------------------------------------------------------------------#
    # Function to trigger when a tweet matches the streaming rules, check rules
    # Input: tweet
    # Output: None
    # -----------------------------------------------------------------------------#
    def on_tweet(self, tweet):
        # Get rules from the stream
        rules = [r.value.lower() for r in self.get_rules().data]
        # Check if the tweet matches any of the rules
        matched_rules = [r for r in rules if r in tweet.text.lower()]
        # If no rules match, return
        if not matched_rules:
            return
        # If a rule matches, get the rule
        rule = matched_rules[0]
        # Check if the tweet is a retweet or has already been responded to
        if not (tweet.text.startswith('RT')):
            # If not, respond to the tweet
            print(twitter_handler.decide_action('reply_to_tweet', tweet_ID=str(tweet.id), rule=rule))
        else:
            print("Tweet already responded to")
    # -----------------------------------------------------------------------------#
# ---------------------------------------------------------------------------------#

# ---------------------------------------------------------------------------------#
# Function to start the twitter stream
# Input: token - Twitter bearer token
# Output: None
# ---------------------------------------------------------------------------------#
def start_streaming(token):
    # Create a new instance of the IDPrinter class
    current_stream = DBStreaming(token)
    # Delete all rules from the stream
    current_stream.delete_written_rules()
    # Add rules to the stream
    current_stream.add_written_rules()
    # Start the stream
    current_stream.filter(expansions='entities.mentions.username')
# ---------------------------------------------------------------------------------#

def stop_streaming():
    pass
