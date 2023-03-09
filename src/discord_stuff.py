import discord as bot
import generate_tweet
import random
import os
import read_write
# import twitter_functions
from dotenv import load_dotenv
from datetime import datetime, timedelta
from handlers import twitter_handler as tweet_controls

# Load the environment variables
try:
    discord_token = os.environ['DISCORD_API_TOKEN_DEV']
except:
    load_dotenv()
    discord_token = os.getenv('DISCORD_API_TOKEN_DEV')

command_list = ['add user',
                'remove user',
                'list users',
                'remove documents by user',
                'list documents by user',
                'return document count',
                'generate a tweet',
                'follow user',
                'unfollow user',
                'none']

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
        # If the message is from the bot itself, create a global variable for the last message and return
        if message.author != client.user:
            if 'DB' in message.content.upper():
                ai_response = generate_tweet.get_command(message.content, command_list)
                users = ai_response[0].replace('\n', '').split(',')
                command = ai_response[1].replace('\n', '').lower()
                users = [i for i in users if i != ' ']
                print(users, command, sep=' | ')
                if command == 'add user' or command == 'add users':
                    response = add_user_command(users)
                    await message.channel.send(response)
                    return
                
                elif command == 'remove user' or command == 'remove users':
                    response = remove_users_command(users)
                    await message.channel.send(response)
                    return

                elif command == 'list users':
                    response = list_users_command()
                    await message.channel.send(response)
                    return

                elif command == 'list documents by user':
                    if read_write.find_document('scraped_tweets', {'user_name': users[0].lower()}) != None:
                        tweets = read_write.find_all_documents('scraped_tweets', {'user_name': users[0].lower()})
                        response = ''
                        if len(tweets[1]) == 0:
                            response = 'No tweets by '+users[0].lower()+' in the database.'
                            return
                        for each in tweets[1]:
                            response += '• '+ each + '\n'
                        await message.channel.send(response)
                        return
                    else:
                        await message.channel.send('No tweets by '+users[0].lower()+' in the database.')
                        return

                elif command == 'return document count':
                    count = read_write.find_all_documents('scraped_tweets', {'user_name': users[0].lower()})[0]
                    await message.channel.send('There are '+str(count)+' tweets by '+users[0].lower()+' in the database.')
                    return

                elif command == 'remove documents by user':
                    user = users[0].lower()
                    if read_write.find_document('scraped_tweets', {'user_name': user}) != None:
                        count = read_write.delete_all_documents('scraped_tweets', {'user_name': user})
                        await message.channel.send('Removed '+str(count)+' documents by: '+user+'.')
                        return
                    else:
                        await message.channel.send(user+  'not in database.')
                        return

                elif command == 'generate a tweet':
                    new_tweet = messaging_logic(message)
                    if new_tweet == None:
                        return
                    # Send the tweet to the discord channel
                    message = await message.channel.send(new_tweet)
                    await message.add_reaction('✅')
                    await message.add_reaction('❌')
                                          
                else:
                    await message.channel.send(generate_tweet.get_response_from_text('Please rephrase that for me.').replace('\n', ' '))

    @client.event
    async def on_raw_reaction_add(payload):
        if payload.user_id != client.user.id:
            channel = client.get_channel(payload.channel_id)
            content = await channel.fetch_message(payload.message_id)
            message_reacted = content.content
            if read_write.find_document('generated_tweets', {'altered_tweet': message_reacted}) != None:
                if str(payload.emoji) == '✅':
                    await channel.send('**Tweet approved**')
                    read_write.update_document('generated_tweets', {'altered_tweet': message_reacted}, {'$set': {'approved': True}})
                elif str(payload.emoji) == '❌':
                    await channel.send('**Tweet rejected**')
                    read_write.update_document('generated_tweets', {'altered_tweet': message_reacted}, {'$set': {'approved': False}})
            else:
                if str(payload.emoji) == '💡':
                    idea = generate_tweet.record_idea(message_reacted)
                    read_write.add_to_notion(idea[0], idea[1], idea[2], message_reacted)
                    await channel.send('**Idea recorded**')
                

    # Run the bot
    client.run(discord_token)


# Function for returning a random tweet from the data base file
# Output: A random tweet
def random_tweet():
    now = datetime.now()
    three_days_ago = now - timedelta(days=3)
    list_of_tweets = read_write.read_from_db('scraped_tweets')
    if len(list_of_tweets) == 0:
        return False
    list_of_tweets = sorted(list_of_tweets, key=lambda k: k['engagement_rate'], reverse=True)
    list_of_tweets = [i for i in list_of_tweets if i['created_at'] >= three_days_ago]
    list_of_tweets = list_of_tweets[:10]
    return random.choice(list_of_tweets)['text']
    
    # TODO: Add more function calls for adding personality or more custom tweets
    # TODO: Add capability to create bullish and bearish tweets, as well as tweets based on topics



# Function for deciding which tweet to generate based on the message
# Input: The message
# Output: The tweet to generate
# TODO: Add more function calls for adding personality or more custom tweets
def messaging_logic(message):
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
        tweet = random_tweet()
        if tweet == False:
            return 'No tweets in the database.'
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
    new_tweet['altered_tweet'].replace('\n','')
    read_write.write_to_db('generated_tweets', new_tweet)

    # Return the new tweet
    return new_tweet['altered_tweet']


def add_user_command(users):
    added_users = []
    users_in_db = []
    users_not_found = []
    # For each user in the list of users requested to be added
    for user in users:
        # Remove any spaces and make the user lowercase
        user = user.replace(' ','').lower()
        # If the user is not in the database then follow them and add them to the database
        if read_write.find_document('users', {'user': user}) == None:
            # If the user is followed then add them to the database
            if tweet_controls.decide_action(action='follow', user=user):
                # Add the user to the database
                read_write.write_to_db('users',{'user': user})
                added_users.append(user.replace(' ', ''))
            else:
                # If the user is not followed then add them to the list of users not found
                users_not_found.append(user.replace(' ', ''))
        else:
            # If the user is already in the database then add them to the list of users already in the database
            users_in_db.append(user.replace(' ', ''))
    # Create a response string
    response = ''
    # If there are users added then add them to the response string
    if len(added_users) > 0:
        # Add the users added to the response string
        response += 'Users added and followed: \n'
        # For each user in the list of users added
        for user in added_users:
            # Add the user to the response string
            response +='• '+ user + '\n'
    if len(users_in_db) > 0:
        response += 'Users already in database: \n'
        for user in users_in_db:
            response +='• '+ user + '\n'
    if len(users_not_found) > 0:
        response += 'Users not found: \n'
        for user in users_not_found:
            response +='• '+ user + '\n'
    if response == '':
        response = 'No users added.'
    return response

def remove_users_command(users):
    removed_users = []
    users_not_in_db = []
    for user in users:
        user = user.replace(' ','').lower()
        if read_write.find_document('users', {'user': user}) != None:
            if tweet_controls.decide_action(action='unfollow',user=user):
                read_write.remove_from_db('users',{'user': user})
                removed_users.append(user.replace(' ', ''))
        else:
            users_not_in_db.append(user.replace(' ', ''))
    response = ''
    if len(removed_users) > 0:
        response += 'Users removed and unfollowed: \n'
        for user in removed_users:
            response +='• '+ user + '\n'
    if len(users_not_in_db) > 0:
        response += 'Users not in database: \n'
        for user in users_not_in_db:
            response +='• '+ user + '\n'
    if response == '':
        response = 'No users removed.'
    return response

def list_users_command():
    users = read_write.read_from_db('users')
    response = ''
    if len(users) > 0:
        response += 'Users in database: \n'
        for user in users:
            response +='• '+ user['user'] + '\n'
    else:
        response = 'No users in database.'
    return response