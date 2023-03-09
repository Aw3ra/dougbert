import re

# ---------------------------------------------------------------------------------#
# Function to get the full conversation of a tweet
# Inputs:  tweet - the tweet to get the conversation of
# Outputs: conversation - the full conversation of the tweet
#          Need to return full conversation as an array of dictionaries in this format
#       message[
#         {'role': 'user', 'content': 'text'}
#         {'role': 'assistant', 'content': 'text'}
#           ]
# ---------------------------------------------------------------------------------#
def get_conversation(auth, tweet_id):
    # Create the array to store the conversation
    reversed_conversation = []
    # WHile there is a tweet id
    while tweet_id != None:
        # Create the string to add to the array
        dict_to_add = {}
        string_to_add = ''
        # Get the conversation using tweepy
        reference_tweet = auth.get_tweet(tweet_id, expansions='referenced_tweets.id,author_id')
        # If the author is DougbertAI, set the role to assistant
        user = re.search(r'username=(\w+)', str(reference_tweet.includes['users'])).group(1)
        if user == 'DougbertAI':
            dict_to_add['role'] = 'assistant'
        # If the author is not DougbertAI, set the role to user
        else:
            dict_to_add['role'] = 'user'
        string_to_add += user+': '
        # Find the content of the tweet
        content = remove_user_tags(reference_tweet.data['text'].replace('\n', ' '))
        # Add the content to the string
        string_to_add += content
        #Add the string to the dictionary
        dict_to_add['content'] = string_to_add
        # Add the responded to tweet id to the first tweet array
        try:
            # If it can get a tweet id, add it to the array
            tweet_id = re.search(r'<Tweet id=(\w+)', str(reference_tweet.includes['tweets'])).group(1)
        except:
            # If it can't get a tweet id, set the tweet id to none
            tweet_id = None
        # Add the string to the array
        reversed_conversation.append(dict_to_add)
    # Reverse the order of the array so the conversation comes in time order
    conversation = reversed_conversation[::-1]
    # Return the conversation as a string
    return conversation


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