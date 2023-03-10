from . import scrape_for_replies, post_tweet
from handlers import mongo_handler
from general_functions import find_json
import random
from handlers import openAI_handler, twitter_handler
import re


# ---------------------------------------------------------------------------------#
# Variables for the prompt text calls
# ---------------------------------------------------------------------------------#
# Get the json data


# ---------------------------------------------------------------------------------#



# ---------------------------------------------------------------------------------#
# Function to reply to a tweet
# Inputs:  auth - the authentication object
#          tweet - the tweet to reply to
#          reply - the reply to post
# Outputs: True - if the reply was successful
#          False - if the reply was not successful
#          e - if an error occurs
# ---------------------------------------------------------------------------------#
def reply_to(auth,auth2,**kwargs):
    json_data = find_json.find_json_file('prompts.json')[0][kwargs['rule']]
    # Get the reply prompt
    reply_prompt = json_data['prompt']
    # If the tweet_ID is passed in
    if 'tweet_ID' in kwargs:
        # Get the tweet_id as a number 
        reply_id = int(kwargs['tweet_ID'])
    # If the tweet_ID is not passed in
    else:
        # Get a random user to reply to
        user_to_reply_to = str(random.choice(mongo_handler.decide_action('read', collection='scraped_users'))['user_id'])
        # Get a tweet to reply to
        tweet_to_reply_to = scrape_for_replies.scrape_tweets(auth, user_to_reply_to, 'replied_tweets')
        try:
            # If the tweet is not unique
            if tweet_to_reply_to == 'Item exists':
                # Retry the function
                reply_to(auth,auth2, **kwargs)
            else:
                reply_id = int(tweet_to_reply_to['Tweet_id'])
        except:
            # If it fails to get a tweet, return
            return

    # Try to reply to the tweet
    try:
        # Check if the bot wrote the tweet
        bot_name = 'DougbertAI'
        tweeter = auth.get_tweet(reply_id, expansions='author_id')
        pattern = r'username=(\w+)'
        match = re.search(pattern, str(tweeter))
        if str(match.group(1)).lower() == str(bot_name).lower():
            return 'Bot wrote the tweet'
        # Get the full conversation from the tweet ID (This helps pickup a thread if the scraped tweet is a long thread)
        full_conversation = twitter_handler.decide_action('full_conversation', tweet_id = reply_id)
        # Get the list of tweets that dougbert has already replied to
        replied_tweets = mongo_handler.decide_action('read', collection='replied_tweets')
        # Check the sentiment of the tweet
        # TODO: This is probably unnecessary as we could apply any sort of personality traits instead of scraping and writing a similar response
        # Write the prompt for the sentiment
        # prompt = sentiment_prompt.replace('{TWEET_TEXT}', full_conversation)
        # # Get the sentiment
        # sentiment = openAI_handler.decide_action('text', prompt=prompt).replace('\n','')
        sentiment = 'passive aggressive'
        # Generate a reply to the conversation
        # Write the prompt for the reply
        system_message = {"role": "system", "content": reply_prompt}
        full_conversation.insert(0, system_message)
        prompt = full_conversation
        # Get the reply, replace the new line and the dougbertAI: text
        # TODO: replace any user tags in the prompt with blanks so it doesnt continually tag people in the conversation
        reply = openAI_handler.decide_action('text', prompt=prompt).replace('\n',' ').replace('DougbertAI:','')
        # Remove twitter user tags from the reply
        reply = remove_user_tags(reply)

        # Check if the tweet has been replied to before
        if is_unique(full_conversation, replied_tweets):
            # If not, reply to the tweet
            if post_tweet.post_tweet(auth2, reply, tweet_ID=reply_id, stable_auth=auth, bot_name='DougbertAI'):
                # Update the tweet in the database
                if mongo_handler.decide_action('add', collection='responded_to', query={'Tweet_id': reply_id, 'tweet_text': reply}):
                    return True
                else:
                    return 'Could not update database'
            else:
                return 'Could not post tweet'
        else:
            return 'Tweet has already been replied to'
    except Exception as e:
        return e


# Function to check if the tweet is unique
# Inputs:  tweet - the tweet to check
#          tweet_array - the array of tweets to check against
# Outputs: True - if the tweet is unique
#          False - if the tweet is not unique
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


# ---------------------------------------------------------------------------------#
# Function to remove twitter user tags from the reply
# Inputs:  reply - the reply to remove the tags from
# Outputs: reply - the reply with the tags removed
# ---------------------------------------------------------------------------------#
def remove_user_tags(reply):
    # Create a regex pattern to find the user tags
    pattern = re.compile(r'@\w+\s?')
    # Remove the user tags
    reply = re.sub(pattern,'', reply)
    # Return the reply
    return reply