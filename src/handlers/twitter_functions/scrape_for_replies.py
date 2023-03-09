from handlers import mongo_handler

# ---------------------------------------------------------------------------------#
# Function to scrape a tweet for the twitter bot to reply to
# Inputs:  auth - the authentication object for the user to follow
#          following - the list of users that the bot is following
#          database - the database to check against for duplicates and to add new tweets to
# Outputs: True - if tweets were successfully scraped
#          False - if no tweets were scraped
#          e    - if any error occurs
# ---------------------------------------------------------------------------------#
def scrape_tweets(auth, user_ID, database):
    replied_to_tweets = mongo_handler.decide_action('read', collection=database)
    # Full all tweets from mongo database
    ID = str(user_ID)
    try:
        # If the following data exists
        if user_ID != None:
            # Create an array of tweet dictionaries
            tweets = auth.get_users_tweets(ID, max_results=5, exclude='retweets,replies', tweet_fields='created_at,public_metrics')
            # If the tweets exist
            if tweets.data != None:
                # For each tweet
                tweet = tweets.data[0]
                new_tweet = {'Tweet_id': tweet['id'], 'tweet_text': tweet['text'].replace('\n',' '), 'replied_to': False}
                # If the tweet is unique
                if is_unique(new_tweet, replied_to_tweets):
                    # Add the tweet to the database of tweets
                    print(mongo_handler.decide_action('add', collection=database, query=new_tweet))
                    return new_tweet
                else:
                    return 'Item exists'
            else:
                return 'No tweets found'
        else:
            return False
    except Exception as e:
        return e

# ---------------------------------------------------------------------------------#
# Function to check if the tweet is unique
# Inputs:  tweet - the tweet to check
#          tweet_array - the array of tweets to check against
# Outputs: True - if the tweet is unique
#          False - if the tweet is not unique
# ---------------------------------------------------------------------------------#
def is_unique(tweet, tweet_array):
    try:
        if tweet_array == 'No documents found':
            return True
        # For each tweet in the tweet array
        for tweets in tweet_array:
            # If the tweet is unique
            if tweets['Tweet_id'] == tweet['Tweet_id'] and tweets['tweet_text'] == tweet['tweet_text']:
                return False
        return True
    except Exception as e:
        return e

