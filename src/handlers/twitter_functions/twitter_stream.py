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
class IDPrinter(tweepy.StreamingClient):
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
    # FUnction to add rules to the stream from a json file
    # Input: None
    # Output: None
    # -----------------------------------------------------------------------------#
    def add_rules(self):
        # Get rules from json file
        rules = find_json.find_json_file('rules.json')
        # Add rules to the stream
        self.add_rules(rules)
    # -----------------------------------------------------------------------------#


    # -----------------------------------------------------------------------------#
    # Function to delete all rules from the stream
    # Input: None
    # Output: None
    # -----------------------------------------------------------------------------#
    def delete_rules(self):
        # Get rules from the stream
        rules = self.get_rules()
        # Delete rules from the stream
        self.delete_rules(rules)
    # -----------------------------------------------------------------------------#

    
    # -----------------------------------------------------------------------------#
    # Function to trigger when a tweet matches the streaming rules
    # Input: tweet
    # Output: None
    # -----------------------------------------------------------------------------#
    def on_tweet(self, tweet):
        # If the tweet has been responded to, don't respond again
        print(tweet.text)
        # If the tweet is not a retweet

        if str(tweet.text[0:2]) != 'RT':
            # If the tweet has not been responded to
            if str(tweet.id) not in mongo_handler.decide_action('find', collection='responded_to', query={'Tweet_id': int(tweet.id)}):
                # Reply to the tweet
                print(twitter_handler.decide_action('reply_to_tweet', tweet_ID=str(tweet.id)))
    # -----------------------------------------------------------------------------#

# ---------------------------------------------------------------------------------#



# ---------------------------------------------------------------------------------#
# Function to start the twitter stream
# Input: token - Twitter bearer token
# Output: None
# ---------------------------------------------------------------------------------#
def start_streaming(token):
    # Create a new instance of the IDPrinter class
    printer = IDPrinter(token)
    # Add rules to the stream
    printer.filter()
# ---------------------------------------------------------------------------------#

def stop_streaming():
    pass
