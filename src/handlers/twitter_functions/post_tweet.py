import re

# Function to post a tweet
# Inputs:  auth - the authentication object
#          tweet - the tweet to post
# Outputs: None
def post_tweet(auth, tweet, **kwargs):
    if 'tweet_ID' in kwargs:
        tweet_ID = kwargs['tweet_ID']
    else:
        tweet_ID = None
    if 'bot_name' in kwargs:
        bot_name = kwargs['bot_name']
    else:
        bot_name = None
    if 'stable_auth' in kwargs:
        stable_auth = kwargs['stable_auth']
        # Check if the bot wrote the tweet
        tweeter = stable_auth.get_tweet(tweet_ID, expansions='author_id')
        pattern = r'username=(\w+)'
        match = re.search(pattern, str(tweeter))
        if str(match.group(1)).lower() == str(bot_name).lower():
            return 'Written by bot'

    # Check if the tweet is longer than 280 characters
    try:
        # If the tweet is less than 280 characters, post it
        if len(tweet)<=280:
            if tweet_ID == None:
                auth.create_tweet(text=tweet)
                return True
            else:
                auth.create_tweet(text=tweet, in_reply_to_tweet_id=tweet_ID)
                return True
        else:
            # Split the tweet by punctuation
            split_text = split_text_by_punctuation(tweet)
            # Loop through the split text
            for i in split_text:
                # Set the tweet text
                tweet_text = f"{i}"
                # Check if the ID is none
                if tweet_ID == None:
                    tweet_ID = auth.create_tweet(text=tweet_text).data['id']
                else:
                    newID = auth.create_tweet(text=tweet_text, in_reply_to_tweet_id=tweet_ID)
                    tweet_ID = newID.data['id']
            return True
    # If there is an error, return the error
    except Exception as e:
        print(e)

# ---------------------------------------------------------------------------------#
# Function to split text by punctuation
# Inputs:  text - the text to split
# Outputs: split_text - the split text
# ---------------------------------------------------------------------------------#
def split_text_by_punctuation(text, max_chars=280):
    # Split the text by punctuation
    split_text = []
    # Set the remaining text to the text
    remaining_text = text
    # While the remaining text is longer than 280 characters
    while len(remaining_text) > max_chars:
        # Find the last period
        last_period_index = remaining_text[:max_chars+1].rfind('.')
        # Check if the last period is greater than 0
        if last_period_index > 0:
            # Append the text
            split_text.append(remaining_text[:last_period_index+1].strip())
            # Set the remaining text
            remaining_text = remaining_text[last_period_index+1:].strip()
        else:
            # Append the text
            split_text.append(remaining_text[:max_chars].strip())
            # Set the remaining text
            remaining_text = remaining_text[max_chars:].strip()
    # Check if the remaining text is greater than 0
    if len(remaining_text) > 0:
        # Append the remaining text
        split_text.append(remaining_text)
    # Return the split text
    return split_text


