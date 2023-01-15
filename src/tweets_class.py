import tweepy
import os
from dotenv import load_dotenv

# Load the environment variables
load_dotenv()

# Create a tweepy client with the bearer token to pull tweets
bearer_token = os.getenv('BEARER_TOKEN')
client = tweepy.Client(bearer_token)

# Class
# This class is used to store tweets and their respective variables
# It also contains functions to get the engagement rate of a tweet
# and to print the tweet
class tweets:
    # Constructor, initalise the variables
    def __init__(self, tweet, user):
        # When pulling in from a txt file the entire thing is in strings when this class is created, as when a member of this class is created from a tweet it uses the tweet object
        # If the tweet is a tweet object, then get the text from the tweet object
        try:
            self.text = tweet.text.replace('\n', ' ')
        # If the tweet is a string, then set the text to the string
        except:
            self.text = tweet.replace('\n', ' ')
        self.user = user 
        self.engagement_rate = 0
        self.tweet = tweet
        self.created_at = 0
    
    # Get the engagement rate of the tweet
    def get_engagement_rate(self):
        # For each metric in the public metrics of the tweet, if it is a retweet, reply, like or quote, add it to the engagement rate
        for metric in self.tweet.public_metrics.items():
            if metric[0] == 'retweet_count' or metric[0] == 'reply_count' or metric[0] == 'like_count' or metric[0] == 'quote_count':
                self.engagement_rate += metric[1]
    
    # Print the tweet
    def print_tweet(self):
        # Print the user, text and engagement rate of the tweet
        print(self.user, self.text, self.engagement_rate, sep='      ')