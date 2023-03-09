import tweepy

# Function to add a comment to a tweet
# Inputs:  auth - the authentication object
#          tweet_id - the id of the tweet to comment on
#          comment - the comment to add
# Outputs: None
def add_comment(auth, tweet_id, comment):
    try:
        auth.create_tweet(comment, in_reply_to_tweet_id = tweet_id)
        return True
    except Exception as e:
        return e