import tweepy
import os
from dotenv import load_dotenv
import threading
from .twitter_functions import follow_user, post_tweet, unfollow_user, add_comment, retweet, scrape_tweets, reply_to, scrape_followers, twitter_stream, full_conversation

# ---------------------------------------------------------------------------------#
# Set the Twitter API keys
# First try to get keys using environ for running on replit, 
# if that fails, try to get keys from .env file
# ---------------------------------------------------------------------------------#
try:
    DB_BEARER_TOKEN = os.environ['DOUGBERT_BEARER_TOKEN']
    MY_BEARER_TOKEN = os.environ['TWITTER_BEARER_TOKEN']
    CONSUMER_KEY = os.environ['DOUGBERT_CONSUMER_KEY']
    CONSUMER_SECRET = os.environ['DOUGBERT_CONSUMER_SECRET']
    ACCESS_TOKEN = os.environ['DOUGBERT_ACCESS_TOKEN']
    ACCESS_TOKEN_SECRET = os.environ['DOUGBERT_ACCESS_TOKEN_SECRET']
except:
    load_dotenv()
    DB_BEARER_TOKEN = os.getenv('DOUGBERT_BEARER_TOKEN')
    MY_BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN')
    CONSUMER_KEY = os.getenv('DOUGBERT_CONSUMER_KEY')
    CONSUMER_SECRET = os.getenv('DOUGBERT_CONSUMER_SECRET')
    ACCESS_TOKEN = os.getenv('DOUGBERT_ACCESS_TOKEN')
    ACCESS_TOKEN_SECRET = os.getenv('DOUGBERT_ACCESS_TOKEN_SECRET')

# ---------------------------------------------------------------------------------#
# Function to decide which function to call
# Inputs:   action - the action to take, follow or unfollow
#           kwargs - the additional info required for the action
# Outputs:  None
# ---------------------------------------------------------------------------------#
def decide_action(action, **kwargs):
    # -----------------------------------------------------------------------------#
    # Authenticate to Twitter using the keys for the twitter bot account
    # -----------------------------------------------------------------------------#
    db_client = tweepy.Client(
        consumer_key=os.getenv('DOUGBERT_CONSUMER_KEY'), 
        consumer_secret=os.getenv('DOUGBERT_CONSUMER_SECRET'),
        access_token=os.getenv('DOUGBERT_ACCESS_TOKEN') , 
        access_token_secret=os.getenv('DOUGBERT_ACCESS_TOKEN_SECRET'))
    # -----------------------------------------------------------------------------#

    #------------------------------------------------------------------------------#
    # Authenticate to Twitter using the keys for the program account
    # This sets a normal client and a fall back client
    # The normal client is for the main account, the fall back client is for the
    # program account
    # -----------------------------------------------------------------------------#
    normal_client = tweepy.Client(DB_BEARER_TOKEN)
    fall_back_client = tweepy.Client(MY_BEARER_TOKEN)

    # -----------------------------------------------------------------------------#
    # Create the auth object
    # Set the access token and secret
    # -----------------------------------------------------------------------------#
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    # -----------------------------------------------------------------------------#

    # -----------------------------------------------------------------------------#
    # Check if botname is in kwargs
    # If it is, get the list of users that the bot is following
    # -----------------------------------------------------------------------------#
    if 'bot_name' in kwargs:
        # -----------------------------------------------------------------------------#
        # Get the user that the bot is following
        # -----------------------------------------------------------------------------#
        try:
            # Find the bot id
            bot_id = normal_client.get_user(username=kwargs['bot_name']).data['id']
            following = normal_client.get_users_following(bot_id, max_results=1000)
        except: 
            # Find the bot id
            bot_id = fall_back_client.get_user(username=kwargs['bot_name']).data['id']
            following = fall_back_client.get_users_following(bot_id, max_results=1000)
        # -----------------------------------------------------------------------------#

    # Call the appropriate function
    # If the action is follow, call the follow_user function
    if action == 'follow':
        return follow_user.follow_user(db_client,normal_client, following, **kwargs)
    # If the action is unfollow, call the unfollow_user function
    elif action == 'unfollow':
        return unfollow_user.unfollow_user(db_client, normal_client, following, **kwargs)
    # If the action is tweet, call the post_tweet function
    elif action == 'tweet':
        return post_tweet.post_tweet(db_client, kwargs['tweet'])
    # If the action is comment, call the add_comment function
    elif action == 'comment':
        add_comment.add_comment(auth, kwargs['tweet_id'], kwargs['comment'])
    # If the action is retweet, call the retweet function
    elif action == 'retweet':
        retweet.retweet(auth, kwargs['tweet_id'])
    # If the action is to scrape tweets, call the scrape_tweets function
    elif action == 'scrape_tweets':
        return scrape_tweets.scrape_tweets(fall_back_client, following, kwargs['database'])
    # If the action is to reply to a tweet, call the reply_to function
    elif action == 'reply_to_tweet':
        return reply_to.reply_to(fall_back_client,db_client,**kwargs)
        # return reply_to.reply_to(auth, kwargs['tweet_id'], kwargs['comment'])
    elif action == 'scrape_following':
        return scrape_followers.scrape_following(fall_back_client, following, kwargs['database'])
    elif action == 'full_conversation':
        return full_conversation.get_conversation(fall_back_client, kwargs['tweet_id'])
    else:
        return 'Invalid action'
# ---------------------------------------------------------------------------------#



# ---------------------------------------------------------------------------------#
# Function to start the twitter stream
# Inputs:   None
# Outputs:  None
# ---------------------------------------------------------------------------------#
def start_stream():
    # -----------------------------------------------------------------------------#
    # STart the twitter stream
    twitter_stream.start_streaming(MY_BEARER_TOKEN)

# Todo: Continue to add functions to this file
# Todo: Continue setting out how the twitter handler works and interactes with other tools.
# Todo: Abstract out the twitter functions into seperate files and test