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
# streamingClient = tweepy.StreamingClient(MY_BEARER_TOKEN)
# streamingClient.sample()
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
        rules = find_json.find_json_file('prompts.json')
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
    # Function to trigger when a tweet matches the streaming rules
    # Input: tweet
    # Output: None
    # -----------------------------------------------------------------------------#
    def on_tweet(self, tweet):
        # Check the user tages against prompts.json
        user_tags_rules = find_json.find_json_file('prompts.json')
        # For each rule in user_tags_rules
        for rule in user_tags_rules:
            for user in rule.keys():
                if tweet.entities['mentions'][0]['username'] == user: 
                    if str(tweet.text[0:2]) != 'RT':
                    # If the tweet has not been responded to
                        if str(tweet.id) not in mongo_handler.decide_action('find', collection='responded_to', query={'Tweet_id': int(tweet.id)}):
                            # Reply to the tweet
                            print(twitter_handler.decide_action('reply_to_tweet', tweet_ID=str(tweet.id), rule=user))

        # # If the tweet is not a retweet

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
