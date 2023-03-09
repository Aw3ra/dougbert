# Class
# This class is used to store tweets and their respective variables
class tweets:
    # Constructor, initalise the variables
    def __init__(self, user_name, user_ID, tweet):
        self.user_id = user_ID
        self.user_name = user_name\
        # When pulling in from a txt file the entire thing is in strings when this class is created, as when a member of this class is created from a tweet it uses the tweet object
        # If the tweet is a tweet object, then get the text from the tweet object
        try:
            self.text = str(tweet).text.replace('\n', ' ')
        # If the tweet is a string, then set the text to the string
        except:
            self.text = str(tweet).replace('\n', ' ')
        self.engagement_rate = ''
        self.created_at = ''
        self.sentiment = ''

    # Print the tweet
    def print_tweet(self):
        # Print the user, text and engagement rate of the tweet
        print( self.text, self.engagement_rate, sep='      ')

    def tweet_to_dict(self):
        # Create a dictionary of the tweet
        tweet_dict = {'user_id': self.user_id, 'user_name': self.user_name, 'text': self.text, 'engagement_rate': self.engagement_rate, 'created_at': self.created_at, 'sentiment': self.sentiment}
        return tweet_dict

    # Get the engagement rate of the tweet
    # Inputs:  tweet - the tweet to be analysed
    # Outputs: engagement_rate - the engagement rate of the tweet
    def get_engagement_rate(self, tweet):
        # Set the engagement rate to 0
        engagement_rate = 0
        # For each metric in the public metrics of the tweet, if it is a retweet, reply, like or quote, add it to the engagement rate
        for metric in tweet.public_metrics.items():
            if metric[0] == 'retweet_count' or metric[0] == 'reply_count' or metric[0] == 'like_count' or metric[0] == 'quote_count':
                engagement_rate += metric[1]
        # Return the engagement rate
        return engagement_rate