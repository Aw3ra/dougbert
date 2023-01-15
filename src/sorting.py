import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import gensim
from gensim import corpora
from collections import defaultdict


# List of words to ignore when looking at the most common words
word_to_ignore = ['get', 'even', 'like', 'im', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '’', '“', '”', '’', 'know', 'one', 'two', 'three', 'four', 'five',
                  'six', 'seven', 'eight', 'nine', 'ten', 'amp', 'Taiyo', 'taiyopilots', 'pilots', 'see', 'lot', 'still', 'new', 'would', 'want', 'dont', 'don’t', 'LamportDAO']

# List of topics to ignore
ignored_topics = ['taiyopilots', 'TaiyoPilots', 'LamportDAO', 'Graphite']

# Function for sorting tweets by engagment rate
# Inputs:  list_of_tweets - a list of tweets
# Outputs: list_of_tweets - a list of tweets sorted by engagement rate
def sort_tweets_by_engagement_rate(list_of_tweets):
    # Sort the tweets by engagement rate
    list_of_tweets.sort(key=lambda x: x.engagement_rate, reverse=True)
    # Return the list of tweets
    return list_of_tweets

# Function for sorting tweets by date
# Inputs:  list_of_tweets - a list of tweets
# Outputs: list_of_tweets - a list of tweets sorted by date
def sort_tweets_by_date(list_of_tweets):
    # Sort the tweets by date
    list_of_tweets.sort(key=lambda x: x.created_at, reverse=True)
    # Return the list of tweets
    return list_of_tweets

# Function removing ignored topics
# Inputs:  list_of_tweets - a list of tweets
#          ignored_topics - a list of topics to ignore
# Outputs: list_of_tweets - a list of tweets with the ignored topics removed
def remove_ignored_topics(list_of_tweets, ignored_topics):
    # For each tweet in the list of tweets
    for tweet in list_of_tweets:
        # For each topic in the list of ignored topics
        for topic in ignored_topics:
            # If the topic is in the tweet
            if topic in tweet.text:
                # Remove the tweet from the list of tweets
                list_of_tweets.remove(tweet)
                break
    return list_of_tweets

# Function for getting the most common topic
# Inputs:  file_path - the path to the csv file
#          num_topics - the number of topics to look for
#          num_words - the number of words to look for
# Outputs: words - the most words
def get_most_common_topic(file_path, num_topics, num_words):
    # Read the csv file
    tweets = pd.read_csv(file_path)

    # Tokenize the tweets
    tweets['tokenized tweets'] = tweets['text'].apply(word_tokenize)

    # Remove stop words
    stop_words = set(stopwords.words('english'))

    # Add words to ignore to the list of stop words
    for word in word_to_ignore:
        stop_words.add(word)

    # Remove the stop words from the tweets
    tweets['tokenized tweets'] = tweets['tokenized tweets'].apply(
        lambda x: [word for word in x if word.lower() not in stop_words])

    # Create a flat list of all the words
    flat_list = [word for sublist in tweets['tokenized tweets']
                 for word in sublist]
    # Create a dictionary of the words
    dictionary = corpora.Dictionary([flat_list])
    corpus = [dictionary.doc2bow(flat_list)]

    # Create the LDA model
    Lda = gensim.models.LdaModel

    # Train the model
    ladmodel = Lda(corpus, num_topics=num_topics,
                   id2word=dictionary, passes=50)

    # Get the most common topics
    topics = ladmodel.print_topics(num_words=num_words)

    # Count the number of times each topic appears
    topic_count = defaultdict(int)

    # For each topic
    for topic, words in topics:
        # For each word in the topic
        topic_count[topic] += 1
    
    # Get the most common topic
    most_common_topic = max(topic_count, key=topic_count.get)

    # Get the words in the most common topic
    words = ladmodel.show_topic(most_common_topic)
    return words
