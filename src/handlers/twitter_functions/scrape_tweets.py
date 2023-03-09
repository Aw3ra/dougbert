from handlers import mongo_handler

# ---------------------------------------------------------------------------------#
# Function to scrape tweets from who the bot is following, or from a specific user or topic
# Inputs:  auth - the authentication object for the user to follow
#          following - the list of users that the bot is following
#          database - the database to check against for duplicates and to add new tweets to
# Outputs: True - if tweets were successfully scraped
#          False - if no tweets were scraped
#          e    - if any error occurs
# ---------------------------------------------------------------------------------#
def scrape_tweets(auth, following, database):
    # Full all tweets from mongo database
    all_tweets = mongo_handler.decide_action('read', collection=database)
    try:
        # If the following data exists
        if following.data != None:
            # Create an array of tweet dictionaries
            new_tweet_array = []
            for users in following.data:
                ID = auth.get_user(username=users).data['id']
                user_name = str(users).lower()
                tweets = auth.get_users_tweets(ID, max_results=5, exclude='retweets,replies', tweet_fields='created_at,public_metrics')
                # If the tweets exist
                if tweets.data != None:
                    # For each tweet
                    for tweet in tweets.data:
                        engagement = tweet['public_metrics']['like_count'] + tweet['public_metrics']['quote_count'] + tweet['public_metrics']['reply_count'] + tweet['public_metrics']['retweet_count']
                        # Add the tweet to an array of tweet dictionaries
                        new_tweet = {'user_id': ID, 'user_name': user_name, 'text': tweet['text'].replace('\n',' '), 'created_at': tweet['created_at'], 'engagement_rate':engagement}
                        # If the tweet is unique
                        if is_unique(new_tweet, all_tweets):
                            # Add the tweet to the array of new tweets
                            new_tweet_array.append(new_tweet)
            # If there are new tweets
            if len(new_tweet_array) > 0:
                # Add the new tweets to the database
                for tweets in new_tweet_array:
                    mongo_handler.decide_action('add', collection=database, query=tweets)
                return True
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
    # For each tweet in the tweet array
    for tweets in tweet_array:
        # If the tweet is unique
        if tweets['user_id'] == tweet['user_id'] and tweets['text'] == tweet['text']:
            return False
    return True

