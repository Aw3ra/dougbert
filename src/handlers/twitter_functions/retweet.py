import tweepy

# Function to retweet a select tweet
# Inputs:  auth - the authentication object
#          tweet_id - the id of the tweet to retweet
# Outputs: None
def retweet(auth, tweet_id):
    api = tweepy.API(auth)
    try:
        api.retweet(tweet_id)
        return True
    except Exception as e:
        return e