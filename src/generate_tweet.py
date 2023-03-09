import openai
import tweepy
import os
from dotenv import load_dotenv
import tweets_class

# Load the environment variables
# Set the OpenAI API key
try:
    openai.api_key = os.environ['OPENAI_API_KEY']
    TWITTER_BEARER_TOKEN = os.environ['DOUGBERT_BEARER_TOKEN']
except:
    load_dotenv()
    TWITTER_BEARER_TOKEN = os.getenv('DOUGBERT_BEARER_TOKEN')
    openai.api_key = os.getenv('OPENAI_API_KEY')

# Section for personalities, looking to make this adjustable using the discord bot
personality = 'Reword this to be more easily understood:'
discord_bot = 'Reword this as if you were an AI robot from the future, make it short and sharp:'
doug = "Using a minimum of 400 characters and full sentences reword this as if you were a country bumpkin, make it original:"
bert = "Using a minimum of 400 characters and full sentences reword this as if you were a snobby city lover, make it original:"

# List of items to cause tweet to be false
list_of_invalid_tweets = []

# Function to scrape tweets from a list of users
# Inputs:  list_of_users - a list of users
# Outputs: list_of_tweets_ - a list of tweets
# TODO: Add error handling 
def scrape_tweets(list_of_users):
        # Create a list of tweets
    list_of_new_tweets_ = []
    # Create a client
    client = tweepy.Client(TWITTER_BEARER_TOKEN)
    # Get the IDs of the users
    for user_name in list_of_users:
        user = client.get_user(username=user_name)
        if user.data == None:
            continue
        # fetching the ID
        for each in user.data:
            if each == 'id':
                user_ID = user.data[each]
                done = False
                # For each user create a client and get the tweets
                response = client.get_users_tweets(user_ID,max_results=5,exclude='retweets,replies',tweet_fields='public_metrics,created_at')
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
                        thisTweet = tweets_class.tweets(user_name, user_ID,tweet)
                        # Add the date to the tweet
                        thisTweet.created_at = date
                        # Get the engagement rate
                        thisTweet.engagement_rate = thisTweet.get_engagement_rate(tweet)
                        # Add the tweet to the list of tweets
                        list_of_new_tweets_.append(thisTweet)
    
    # For each tweet in the list of tweets
    # for tweet in list_of_new_tweets_:
    #     if tweet.sentiment == '':
    #         # Get the sentiment of the tweet
    #         sentiment = get_sentiment(tweet.text)
    #         tweet.sentiment = sentiment
    #         # Wait 1 second
    #         time.sleep(2)

    # Return the list of tweets
    return list_of_new_tweets_


# Function for getting a list of users that a user follows
# Inputs:  user_name - the user to get the list of users from
# Outputs: list_of_users - a list of users
def get_list_of_users(user_name):
    # Create a list of users
    list_of_users = []
    # Create a client
    client = tweepy.Client(TWITTER_BEARER_TOKEN)
    # Get the IDs of the users
    user = client.get_user(username=user_name)
    # fetching the ID
    for each in user.data:
        if each == 'id':
            user_ID = user.data[each]
            # For each user create a client and get the tweets
            response = client.get_users_following(user_ID,max_results=1000)
            # If there are tweets
            if response.data != None:
                # For each tweet
                for user in response.data:
                    # Get the date
                    for each in user:
                        if each == 'username':
                            list_of_users.append(user[each].replace(' ','').lower())
    # Return the list of users
    return list_of_users
# Function for converting a dictionary to tweets
# Inputs:  dict - a dict of a tweet to be converted
# Outputs: tweet - the converted tweet
def convert_to_tweets(dict_list):
    tweet_list = []
    for dict in dict_list:
        tweet = tweets_class.tweets(dict['user_name'], dict['user_id'], dict['text'])
        tweet.engagement_rate = dict['engagement_rate']
        tweet.created_at = dict['created_at']
        tweet.sentiment = dict['sentiment']
        tweet_list.append(tweet)
    return tweet_list

# Function checking if a tweet is unique
# Inputs:  tweet - the tweet to be checked
#          list_of_tweets - the list of tweets to be checked against
# Outputs: True - if the tweet is unique
#          False - if the tweet is not unique
def is_unique(tweet, list_of_tweets):
    # For each tweet in the list of tweets
    for each in list_of_tweets:
        # If the tweet is in the list of tweets
        if tweet.text == each.text and tweet.user_name == each.user_name:
            # Return False
            return False
    # Return True
    return True

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

# Function for determining the command from a message
# Inputs:  message - the message to be analysed
# Outputs: command - the command from the message
def get_command(message, commands):
    list_of_commands = ''
    for command in commands:
        list_of_commands += command+', '
    print(message)
    command_request1 = 'Ignoring db and general words find all the users that exist in this message and seperate them by a comma and a space, users can include punctuation: '
    command_request = 'Which of these commands ('+list_of_commands+') accurately describes this message:'
    # Send the prompt to the AI
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=command_request1+message,
        temperature=0,
        max_tokens=100,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )

    response2 = openai.Completion.create(
        model="text-davinci-003",
        prompt=command_request+message,
        temperature=0,
        max_tokens=100,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    # Get the command
    command = response['choices'][0]['text']
    items = response2['choices'][0]['text']
    users = ''
    for user in command.split(', '):
        print(user)
        if user.replace('\n','') != 'user':
            users += user+', '
    print(users)
    # Return the command
    return users, items


# Function for recording an idea to notion using AI
# Inputs:  message - the message to be analysed
# Outputs: response['choices'][0]['text'] - the response from the AI
def record_idea(message):
    # Set the prompt
    record_idea_prompt = 'Find the name of the project in two words and a tell me the idea in 5 words or less, seperating them using a semicolan:'
    prompt = record_idea_prompt+message
    # Send the prompt to the AI
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0,
        max_tokens=100,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    # Return the response
    result = response['choices'][0]['text'].split('; ')
    result.append('New')
    return result    



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
        new_tweet = response['choices'][0]['text'].replace('\n','')
        # Get the response
        valid_tweet = check_tweet(new_tweet)
    # Return the response
    tweet_dict = {'altered_tweet': new_tweet,'original_tweet': tweet, 'aiName': aiName, 'used': False}
    return tweet_dict 


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
            first_part = string[start:start+period_index+1].replace("\n", " ")
            first_part = first_part.replace("  ", "")
            first_part = first_part.replace(' ','',1)
            # Add the first part to the list of parts
            parts.append(first_part)
            # Set the start to the current peirod index
            start = start + period_index+1
        else:
            # Get the first part
            first_part = string[start:start+limit].replace("\n", " ")
            first_part = first_part.replace("  ", "")
            # Add the first part to the list of parts
            parts.append(first_part)
            # Set the start to the current peirod index
            start = start + limit
    # Append the rest of the string
    parts.append(string[start:].replace("\n", " "))
    # Return the list of parts
    return parts