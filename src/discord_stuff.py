import discord as bot
import generate_tweet
import random
import csv

file_of_tweets = 'data/tweets.csv'

# Create the discord client 
intents = bot.Intents.all()
client = bot.Client(command_prefix='!', intents=intents)

# List of bot names
bot_names = ['Doug', 'Bert']

# Start Dougbert Bot
def start_dougbert_bot():
    # At client start up print a message to the console to confirm that the bot is running
    @client.event
    async def on_ready():
        print('We have logged in as {0.user}'.format(client))
    
    # When a message is sent to the discord channel
    @client.event
    async def on_message(message):
        # If the message is from the bot itself, ignore it
        if message.author == client.user:
            return
    
        # If the message starts with !tweet
        if message.content.startswith('!tweet'):
            # If the message contains 'custom' then generate a tweet based on the message
            if 'custom' in message.content:
                # If the message contains 'Doug' then generate a tweet based on the message using Doug
                if 'Doug' in message.content:
                    ai = 'Doug'
                    # Split the message at 'Doug' and get the second part of the split
                    tweet = message.content.split('Doug')[1]
                    # Generate a tweet based on the message and the ai
                    new_tweet = generate_tweet.get_response(tweet, ai)
                # If the message contains 'Bert' then generate a tweet based on the message using Bert
                elif 'Bert' in message.content:
                    ai = 'Bert'
                    # Split the message at 'Bert' and get the second part of the split
                    tweet = message.content.split('Bert')[1]
                    # Generate a tweet based on the message and the ai
                    new_tweet = generate_tweet.get_response(tweet, ai)
                else:
                    # If the message does not contain 'Doug' or 'Bert' then generate a tweet based on the message using a random ai
                    ai = random.choice(bot_names)
                    # Split the message at 'custom' and get the second part of the split
                    tweet = message.content.split('custom')[1]
                    # Generate a tweet based on the message and the ai
                    new_tweet = generate_tweet.get_response(tweet, ai)
            else:
                # If the message does not contain 'custom' then generate a tweet based on a random tweet
                tweet = random_tweet(file_of_tweets)
                # If the message contains 'Doug' then generate a tweet based on the random tweet using Doug
                if 'Doug' in message.content:
                    ai = 'Doug'
                    # Generate a tweet based on the random tweet and the ai
                    new_tweet = generate_tweet.get_response(tweet, ai)
                # If the message contains 'Bert' then generate a tweet based on the random tweet using Bert
                elif 'Bert' in message.content:
                    ai = 'Bert'
                    # Generate a tweet based on the random tweet and the ai
                    new_tweet = generate_tweet.get_response(tweet, ai)
                else:
                    # If the message does not contain 'Doug' or 'Bert' then generate a tweet based on the random tweet using a random ai
                    ai = random.choice(bot_names)
                    # Generate a tweet based on the random tweet and the ai
                    new_tweet = generate_tweet.get_response(tweet, ai)
            # Replace any new lines with a space and replace any full stops with a space, could use this to seperated by thread as well
            new_tweet.replace('\n', ' ').replace('.', '')
            # Send the tweet to the discord channel
            await message.channel.send(new_tweet)
    
    # Run the bot
    client.run('MTA2MjYwODgzMzIxOTkxOTkwMg.GRHDjp.NUqT4NaCBkMd9GA1hEvU0B0dZL6JHAV_z00ch4')


# Function for returning a random tweet from the csv file
# Output: A random tweet
def random_tweet(file_name):
    # Open the csv file and get a random tweet
    with open (file_name, 'r', encoding = 'utf-8') as file:
        # Skip the first row as it is the header
        reader = csv.reader(file)
        next(reader)
        # Add each tweet to a list
        list_of_tweets = []
        for row in reader:
            list_of_tweets.append(row[1])
        # Return a random tweet
        return random.choice(list_of_tweets)