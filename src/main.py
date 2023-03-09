import schedule
import time
import random
from handlers import twitter_handler, mongo_handler
from handlers.twitter_functions import twitter_stream
import threading

# Twitter handle for our bot
bot_twitter_handle = 'DougbertAI'

# ---------------------------------------------------------------------------------#
# Variables for scraping and posting times
# Scrape frequency in hours
scrape_frequency = 1
# Reply frequency in minutes
reply_frequency = 1
# Post times
post_times = ['04:00', '08:00','12:00', '16:00', '20:00','00:00']

# ---------------------------------------------------------------------------------#
# Function to refresh scrape tweets
# Inputs:  None
# Outputs: None
# ---------------------------------------------------------------------------------#
def scrape_tweets():
    twitter_handler.decide_action('scrape_tweets', database='scraped_tweets', bot_name=bot_twitter_handle)

# ---------------------------------------------------------------------------------#
# Function to reply to tweets at time intervals
# Inputs:  None
# Outputs: None
def reply_randomly():
    twitter_handler.decide_action('reply_to_tweet', bot_name=bot_twitter_handle, database='scraped_users')

# ---------------------------------------------------------------------------------#
# Function to post a tweet
# Inputs:  None
# Outputs: None
# ---------------------------------------------------------------------------------#
def post_tweet():
    try:
        # Get a tweet from the database, that has not been used, and is approved
        original_tweet_text = random.choice([d['altered_tweet'] for d in mongo_handler.decide_action('read', collection='generated_tweets') if 'approved' in d and d['approved'] == True and 'used' in d and d['used'] == False])
    except:
        # If there are no tweets to post, return
        print('No tweets to post')
        return
    # Post the tweet
    print('Posting tweet.......')
    # If the tweet is posted successfully, update the database
    if twitter_handler.decide_action('tweet', tweet=original_tweet_text, bot_name=bot_twitter_handle):
        print('Tweet posted successfully')
        # Update the database
        mongo_handler.decide_action('update', collection='generated_tweets', query={'altered_tweet': original_tweet_text}, update={'$set': {'used': True}})

# ---------------------------------------------------------------------------------#
# Main function
# Inputs:  None
# Outputs: None
# ---------------------------------------------------------------------------------#
def main():
    # Print the start up message
    print('Dougbert coming online.......')
    # Start the streaming thread
    threading.Thread(target=twitter_handler.start_stream).start()
    print('Stream started')
    print('Dougbert online')
    # Schedule the tweet posting
    for scheduled_times in post_times:
        schedule.every().day.at(scheduled_times).do(post_tweet)
    # Scrape the tweets
    schedule.every(scrape_frequency).hour.do(scrape_tweets)
    # Reply to tweets
    schedule.every(reply_frequency).minutes.do(reply_randomly)
    # Run the scheduler
    while True:
        # Run the scheduler
        schedule.run_pending()
        time.sleep(1)
# ---------------------------------------------------------------------------------#
# Run main function
# ---------------------------------------------------------------------------------#
main()


    


