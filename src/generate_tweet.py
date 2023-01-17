import openai
import tweepy
import os
from dotenv import load_dotenv
import tweets_class
import time

# Load the environment variables
load_dotenv()
# Set the OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

# Section for personalities, looking to make this adjustable using the discord bot
personality = 'Reword this to be more easily understood:\n\n'
doug = "Using a minimum of 400 characters and full sentences reword this as if you were a country bumpkin, make it original:\n\n"
bert = "Using a minimum of 400 characters and full sentences reword this as if you were a snobby city lover, make it original:\n\n"

# List of items to cause tweet to be false
list_of_invalid_tweets = []

# Function to scrape tweets from a list of users
# Inputs:  list_of_users - a list of users
#          list_of_tweets_ - a list of tweets
# Outputs: list_of_tweets_ - a list of tweets
# TODO: Add error handling 
# TODO: Add sentiment analysis, might be better in the tweet_class though
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
    list_of_new_tweets_ = []
    # Turn the list of current tweets into tweet objects
    for each in list_of_tweets_:
        # Create a tweet object
        thisTweet = tweets_class.tweets(each[1], each[0])
        # Add the engagement rate to the tweet
        thisTweet.engagement_rate = each[2]
        # Add the date to the tweet
        thisTweet.created_at = each[3]
        # Add the tweet sentiment
        thisTweet.sentiment = each[4]
        # Add the tweet to the list of tweets
        list_of_new_tweets_.append(thisTweet)
    # Get tweets from users
    for user in list_of_ids:
        done = False
        # For each user create a client and get the tweets
        response = client.get_users_tweets(user,max_results=5,exclude='retweets,replies',tweet_fields='public_metrics,created_at')
        # If there are tweets
        if response.data != None:
            # For each tweet
            for tweet in response.data:
                for each in list_of_new_tweets_:
                    if tweet.text == each.text:
                        done = True
                        break
                if done:
                    break
                # Get the date
                date = tweet['created_at']
                # Create a tweet object
                thisTweet = tweets_class.tweets(tweet, user)
                # Get the engagement rate
                thisTweet.engagement_rate = get_engagement_rate(thisTweet)
                # Add the date to the tweet
                thisTweet.created_at = date
                # Add the tweet to the list of tweets
                list_of_new_tweets_.append(thisTweet)
    # For each tweet in the list of tweets
    for tweet in list_of_new_tweets_:
        if tweet.sentiment == '':
            # Get the sentiment of the tweet
            sentiment = get_sentiment(tweet.text)
            tweet.sentiment = sentiment
            # Wait 1 second
            time.sleep(2)

    # Return the list of tweets
    return list_of_new_tweets_


    # Get the engagement rate of the tweet
def get_engagement_rate(tweet):
    # Set the engagement rate to 0
    engagement_rate = 0
    # For each metric in the public metrics of the tweet, if it is a retweet, reply, like or quote, add it to the engagement rate
    for metric in tweet.tweet.public_metrics.items():
        if metric[0] == 'retweet_count' or metric[0] == 'reply_count' or metric[0] == 'like_count' or metric[0] == 'quote_count':
            engagement_rate += metric[1]
    # Return the engagement rate
    return engagement_rate


# Function to get the sentiment of a tweet
# Inputs:  tweet - the tweet to be analysed
# Outputs: sentiment - the sentiment of the tweet
def get_sentiment(tweet):
    # Set the prompt
    prompt = 'Using one of these words tell me the sentiment of this tweet(Bullish, Bearish, crabbish):\n\n'+tweet
    # Send the prompt to the AI
    response = openai.Completion.create(
        model="text-ada-001",
        prompt=prompt,
        temperature=0,
        max_tokens=100,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    # Get the sentiment
    sentiment = response['choices'][0]['text']
    # Return the sentiment
    return sentiment


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
# TODO: Add more checks
def check_tweet(tweet):
    if 'http' in tweet:
        return False


# Function to split a tweet into multiple tweets for a thread
# Input: The tweet
# Output: A list of tweets
def split_tweet_for_thread(string):
    # Set the split limit
    limit = 270
    # Set the start
    start = 0
    # Create a list of parts
    parts = []
    # While the start is less than the length of the string
    while start < len(string):
        # Find the index of the period
        period_index = string[start:start+limit].rfind(".")
        # If the period is found
        if period_index != -1:
            # Get the first part
            first_part = string[start:start+period_index+1]
            # Add the first part to the list of parts
            parts.append(first_part)
            # Set the start to the current peirod index
            start = start + period_index+1
        else:
            # Get the first part
            first_part = string[start:start+limit]
            # Add the first part to the list of parts
            parts.append(first_part)
            # Set the start to the current peirod index
            start = start + limit
    # Append the rest of the string
    parts.append(string[start:])
    # Return the list of parts
    return parts
