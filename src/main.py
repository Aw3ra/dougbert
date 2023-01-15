import sorting
import csv
import generate_tweet
import discord_stuff
import datetime


# List of users to look at
list_of_users = ['litecoinyagami','dsentralized','solporttom','notbunjil','aeyakovenko','0xmert_','htmleverything','thejackforge','rick_harris','jaakonfa']

# Function to write tweets to a csv file
# Inputs:  list_of_tweets - a list of tweets
# Outputs: None
def tweets_to_txt(list_of_tweets):
    # Open the csv file and write the tweets to it
    with open('data/tweets.csv', 'w', encoding = 'utf-8', newline='') as file:
        # Write the header
        writer = csv.writer(file)
        # Write the tweets
        writer.writerow(['user', 'text', 'engagement rate', 'date_created'])
        # For each tweet in the list of tweets
        for tweet in list_of_tweets[1:]:
            # Write the tweet to the csv file
            writer.writerow([tweet.user, tweet.text, tweet.engagement_rate, tweet.created_at])

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


# Open up csv and flood it with tweets
list_of_tweets_= open_csv('data/tweets.csv')

# Add new tweets to the list of tweets
list_of_tweets_ = generate_tweet.scrape_tweets(list_of_users, list_of_tweets_)
# Sort the tweets by engagement rate
list_of_tweets_ = sorting.sort_tweets_by_engagement_rate(list_of_tweets_)
# Write the tweets to a csv file
tweets_to_txt(list_of_tweets_)

# Create a final list of tweets
final_list = []

# Get the most common topics
common_words = sorting.get_most_common_topic('data/tweets.csv', 10, 10)
# For each tweet in the list of tweets
for tweet in list_of_tweets_:
    # For each word in the list of common words
    for words in common_words:
        # If the word is in the tweet, add the tweet to the final list
        if words[0] in tweet.text:
            # Add the tweet to the final list
            final_list.append(tweet)
            break

# Remove the ignored topics
final_list = sorting.remove_ignored_topics(final_list, sorting.ignored_topics)

# Start the discord bot
discord_stuff.start_dougbert_bot()




    


