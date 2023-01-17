import sorting
import csv
import generate_tweet
import discord_stuff
import datetime


tweetsFile = 'src/data/tweets.csv'

# List of users to look at
list_of_users = ['litecoinyagami','dsentralized','solporttom','notbunjil','aeyakovenko','0xmert_','htmleverything','thejackforge','rick_harris','jaakonfa', 'leveraged_labs', 'theonlynom']

# Function to write tweets to a csv file
# Inputs:  list_of_tweets - a list of tweets
# Outputs: None
def tweets_to_txt(list_of_tweets):
    # Open the csv file and write the tweets to it
    with open(tweetsFile, 'w', encoding = 'utf-8', newline='') as file:
        # Write the header
        writer = csv.writer(file)
        # Write the tweets
        writer.writerow(['user', 'text', 'engagement rate', 'date_created', 'sentiment'])
        # For each tweet in the list of tweets
        for tweet in list_of_tweets[1:]:
            # Write the tweet to the csv file
            writer.writerow([tweet.user, tweet.text, tweet.engagement_rate, tweet.created_at, tweet.sentiment])


# TODO: Do this every hour
def refresh_tweets():
    # Open up csv and flood it with tweets
    list_of_tweets_= sorting.open_csv(tweetsFile)
    # Add new tweets to the list of tweets
    list_of_tweets_ = generate_tweet.scrape_tweets(list_of_users, list_of_tweets_)
    # Sort the tweets by engagement rate
    list_of_tweets_ = sorting.sort_tweets_by_engagement_rate(list_of_tweets_)
    # Write the tweets to a csv file
    tweets_to_txt(list_of_tweets_)

refresh_tweets()

# Start the discord bot
discord_stuff.start_dougbert_bot()


    


