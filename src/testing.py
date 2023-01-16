import discord_stuff
import generate_tweet
import datetime
import csv

test_tweet = 'I hate how the team at solana does their marketing, if only someone were to come in and manage social media.'

# Function to open the csv file
# Inputs:  csv_name - the name of the csv file
# Outputs: list_of_tweets_ - a list of tweets
def open_csv(csv_name):
    # Open the csv file
    with open(csv_name, 'r', encoding = 'utf-8') as file:
        # Create a first 'dummy' tweet
        firstTweet = [00000,'This is a fake tweet',30, datetime.datetime(2020, 1, 1, 0, 0)]
        # Create a list of tweets
        list_of_tweets_ = []
        # Add the first tweet to the list of tweets
        list_of_tweets_.append(firstTweet)
        # Create a csv reader
        reader = csv.reader(file)
        # Skip the header
        next(reader)
        # For each row in the csv file
        for row in reader:
            # Add the row to the list of tweets
            list_of_tweets_.append(row)
    # Return the list of tweets
    return list_of_tweets_

list_of_tweets = open_csv('src/data/tweets.csv')


for tweet in list_of_tweets:
    response = generate_tweet.get_sentiment(tweet[1])
    print(response)