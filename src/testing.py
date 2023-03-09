import discord_stuff
import generate_tweet
import datetime
import csv
import tweets_class
import read_write
import os
import tweepy
import asyncio
from dotenv import load_dotenv
from notion.client import NotionClient
from handlers import openAI_handler, mongo_handler, twitter_handler, discord_handler
from handlers.twitter_functions import twitter_stream, post_tweet
from handlers.mongo_functions import add_via_prisma
from general_functions import find_json
import random
import time

prompt_json = path = os.path.join(os.path.dirname(__file__), '..', '..', 'prompt.json')

test_command = 'This is me testing the abilities of my program. I am testing the twitter handler. Lets hope that I can post a tweet that is longer than 280 chracters as that is my twitter limit. I will just continue to ramble on and on and on about nothing until twitter decides to post this as a thread. Not sure if it is going to work as I wish it to bujt it is worth a try especially if this means that I can continue to post threads over and over again with no regard to the charatcer limit and especially if it means I can more easily enage with my immense following.'
command_list = ['add single user',
                'remove single user',
                'list users',
                'remove single document',
                'remove multiple documents',
                'none']

prompt = twitter_handler.decide_action('full_conversation', tweet_id = 1629359835215982592, bot_name = 'dougbertAI')
# reply = openA

# Uses AI to write a tweet
tones = ['bullish', 'bearish', 'neutral', 'hyperetoic', 'hypoetoic', 'random', 'sad']
for tone in tones:
    prompt = [{'role': 'user', 'content': f'Write me a {tone} tweet about solana'}]
    prompt = openAI_handler.decide_action('text', prompt=prompt).replace('\n','')
    data = {
                "user": 'dougbertAI',
                'topic': 'solana',
                'tone': tone,
                "personality": tone,
                "original_text": f'Write me a {tone} tweet about solana',
                "generated_text": prompt
            }
    print(asyncio.run(add_via_prisma.add_via_prisma('generated_tweets', data)))
    time.sleep(5)
