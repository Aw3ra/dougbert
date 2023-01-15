import openai
import tweepy
import os
from dotenv import load_dotenv
import tweets_class

# Load the environment variables
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

personality = 'Reword this to be more easily understood:\n\n'
doug = "In 270 characters or less reword this as if you were a country bumpkin, make it original:\n\n"
bert = "In 270 characters or less Reword this as if you were a snobby city lover, make it original:\n\n"

def scrape_tweets(list_of_users, list_of_tweets_):
    client = tweepy.Client(os.getenv('TWITTER_BEARER_TOKEN'))
    list_of_ids = []
    for users in list_of_users:
        user = client.get_user(username=users)

        # fetching the ID
        for each in user.data:
            if each == 'id':
                list_of_ids.append(user.data[each])
                break

    list_of_tweets_ = []

    # Get tweets from users
    for user in list_of_ids:
        response = client.get_users_tweets(user,max_results=5,exclude='retweets,replies',tweet_fields='public_metrics')
        if response.data != None:
            for tweet in response.data:
                thisTweet = tweets_class.tweets(tweet, user)
                list_of_tweets_.append(thisTweet)
                thisTweet.get_engagement_rate()
    return list_of_tweets_

def get_response(tweet, aiName):
    if aiName == "Doug":
        prompt = doug+tweet
    elif aiName == "Bert":
        prompt = bert+tweet

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0,
        max_tokens=60,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    return response['choices'][0]['text']