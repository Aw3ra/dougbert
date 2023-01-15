import openai
import tweepy
import os
from dotenv import load_dotenv
import tweets_class

# Load the environment variables
load_dotenv()
# Set the OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

# Section for personalities, looking to make this adjustable using the discord bot
personality = 'Reword this to be more easily understood:\n\n'
doug = "Create an extended version of this as if you were a country bumpkin, make it original:\n\n"
bert = "Using a minimum of 1000 characters and full sentences reword this as if you were a snobby city lover, make it original:\n\n"

# List of items to cause tweet to be false
list_of_invalid_tweets = []

# Function to scrape tweets from a list of users
# Inputs:  list_of_users - a list of users
#          list_of_tweets_ - a list of tweets
# Outputs: list_of_tweets_ - a list of tweets
def scrape_tweets(list_of_users, list_of_tweets_):
    # Create a client
    client = tweepy.Client(os.getenv('TWITTER_BEARER_TOKEN'))
    # Create a list of IDs
    list_of_ids = []
    # Get the IDs of the users
    for users in list_of_users:
        user = client.get_user(username=users)

        # fetching the ID
        for each in user.data:
            if each == 'id':
                list_of_ids.append(user.data[each])
                break
    # Create a list of tweets
    list_of_tweets_ = []
    # Get tweets from users
    for user in list_of_ids:
        # For each user create a client and get the tweets
        response = client.get_users_tweets(user,max_results=5,exclude='retweets,replies',tweet_fields='public_metrics,created_at')
        # If there are tweets
        if response.data != None:
            # For each tweet
            for tweet in response.data:
                # Get the date
                date = tweet['created_at']
                # Create a tweet object
                thisTweet = tweets_class.tweets(tweet, user)
                # Get the engagement rate
                thisTweet.get_engagement_rate()
                # Add the date to the tweet
                thisTweet.created_at = date
                # Add the tweet to the list of tweets
                list_of_tweets_.append(thisTweet)
    # Return the list of tweets
    return list_of_tweets_

# Function to generate a tweet
# Inputs:  tweet - the tweet to be reworded
#          aiName - the name of the AI
# Outputs: response['choices'][0]['text'] - the reworded tweet
def get_response(tweet, aiName):
    # Set the prompt
    if aiName == "Doug":
        # Set the prompt
        prompt = doug+tweet
    # Set the prompt
    elif aiName == "Bert":
        # Set the prompt
        prompt = bert+tweet

    # Send the prompt to the AI
    valid_tweet = False
    while valid_tweet == False:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0,
            max_tokens=100,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        tweet = response['choices'][0]['text']
        # Get the response
        valid_tweet = check_tweet(tweet)
    tweet = split_tweet_for_thread(tweet)


    # Return the response
    return tweet 

# Function for checking if the tweet is valid, and if not run again
# Input: The tweet
# Output: True if the tweet is valid, False if the tweet is not valid
def check_tweet(tweet):
    if 'http' in tweet:
        return False

def split_tweet_for_thread(string):
    limit = 270
    start = 0
    parts = []
    print(len(string))
    while start < len(string):
        period_index = string[start:start+limit].rfind(".")
        if period_index != -1:
            first_part = string[start:start+period_index+1]
            parts.append(first_part)
            start = start + period_index+1
        else:
            first_part = string[start:start+limit]
            parts.append(first_part)
            start = start + limit

    parts.append(string[start:])
    return parts