import schedule
import time
from handlers import twitter_handler, mongo_handler
import random

post_times = ['04:00', '08:00','12:00', '16:00', '20:00','00:00']


def main():
    print('Dougbert coming online.......')
    print('Starting tweet scheduler.......')
    for time in post_times:
        schedule.every().day.at(time).do(post_tweet)
    while True:
        schedule.run_pending()
        time.sleep(1)

def post_tweet():
    try:
        database = mongo_handler.decide_action('read', collection='generated_tweets')
        aprroved_tweets = [d for d in database if 'approved' in d and d['approved'] == True]
        unused_tweets = [d for d in aprroved_tweets if 'used' in d and d['used'] == False]
        original_tweet_text = random.choice(unused_tweets)['altered_tweet']
    except:
        print('No tweets to post')
        return
    print('Posting tweet.......')
    if twitter_handler.decide_action('tweet', tweet=original_tweet_text, bot_name='DougbertNFT'):
        print('Tweet posted successfully')
        mongo_handler.decide_action('update', collection='generated_tweets', query={'altered_tweet': original_tweet_text}, update={'$set': {'used': True}})

main()