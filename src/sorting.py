import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import gensim
from gensim import corpora
from collections import defaultdict
import string

nltk.download('punkt')
nltk.download('stopwords')
word_to_ignore = ['get', 'even', 'like', 'im', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '’', '“', '”', '’', 'know', 'one', 'two', 'three', 'four', 'five',
                  'six', 'seven', 'eight', 'nine', 'ten', 'amp', 'Taiyo', 'taiyopilots', 'pilots', 'see', 'lot', 'still', 'new', 'would', 'want', 'dont', 'don’t', 'LamportDAO']

ignored_topics = ['taiyopilots', 'TaiyoPilots', 'LamportDAO']


def sort_tweets_by_engagement_rate(list_of_tweets):
    list_of_tweets.sort(key=lambda x: x.engagement_rate, reverse=True)
    return list_of_tweets

def remove_ignored_topics(list_of_tweets, ignored_topics):
    for tweet in list_of_tweets:
        for topic in ignored_topics:
            if topic in tweet.text:
                list_of_tweets.remove(tweet)
                break
    return list_of_tweets

def get_most_common_topic(file_path, num_topics, num_words):
    tweets = pd.read_csv(file_path)
    tweets['tokenized tweets'] = tweets['text'].apply(word_tokenize)
    stop_words = set(stopwords.words('english'))
    for word in word_to_ignore:
        stop_words.add(word)

    tweets['tokenized tweets'] = tweets['tokenized tweets'].apply(
        lambda x: [word for word in x if word.lower() not in stop_words])

    flat_list = [word for sublist in tweets['tokenized tweets']
                 for word in sublist]

    dictionary = corpora.Dictionary([flat_list])
    corpus = [dictionary.doc2bow(flat_list)]

    Lda = gensim.models.LdaModel

    ladmodel = Lda(corpus, num_topics=num_topics,
                   id2word=dictionary, passes=50)

    topics = ladmodel.print_topics(num_words=num_words)

    topic_count = defaultdict(int)
    for topic, words in topics:
        topic_count[topic] += 1
    most_common_topic = max(topic_count, key=topic_count.get)

    words = ladmodel.show_topic(most_common_topic)
    return words
