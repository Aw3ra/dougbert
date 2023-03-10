import datetime
import csv
import os
import tweepy
import asyncio
from dotenv import load_dotenv
from notion.client import NotionClient
from handlers import openAI_handler, mongo_handler, twitter_handler
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

twitter_handler.start_stream()