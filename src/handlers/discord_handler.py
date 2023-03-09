import discord as bot
import os
from dotenv import load_dotenv
from handlers import openAI_handler
from .discord_functions import add_users, generate_tweet_command, remove_users, list_users, remove_multiple_documents, personalities_description, notion_add, update_record, twitter_streaming

# ---------------------------------------------------------------------------------#
# A list of commands that the bot can respond to
command_list = ['add user',
                'remove user',
                'list users',
                'remove multiple documents',
                'generate tweet',
                'tell you about me',
                'start stream',
                'stop stream',
                'help']
# convert the list to a string
command_list_string = ', '.join(command_list)

# ---------------------------------------------------------------------------------#
# Other variables
twitter_handle = 'DougbertNFT'

# ---------------------------------------------------------------------------------#
# Function to choose which discord command to return.
# This function is called from the discord bot, and returns a string generated from
# the appropriate function. The string is then sent to discord.
# The command is extracted from the message using openAI_handler.decide_action
# Inputs:   Message - The message sent to the bot
# Outputs:  String  - The string to send to discord
# ---------------------------------------------------------------------------------#    
def tagged_message(message):
    action = openAI_handler.decide_action('get_command', prompt=message, list_of_commands=command_list_string).lower()
    # Call the appropriate function
    # If the action is add user, call the add_users function
    if action == 'add user':
        # Get the user(s) to add from the message
        response = add_users.add_users(users=openAI_handler.decide_action('get_users', prompt=message), bot_name=twitter_handle)
    # If the action is remove user, call the remove_users function
    elif action == 'remove user':
        # Get the user(s) to remove from the message
        response = remove_users.remove_users(users=openAI_handler.decide_action('get_users', prompt=message), bot_name=twitter_handle)
    # If the action is list users, call the list_users function
    elif action == 'list users':
        response = list_users.list_users()
    # If the action is remove multiple documents, call the remove_multiple_documents function
    elif action == 'remove multiple documents':
        response = remove_multiple_documents.remove_multiple_documents(users=openAI_handler.decide_action('get_users', prompt=message), collection='scraped_tweets', amount='all')
    # If the action is help, return a message with the list of commands
    elif action == 'help':
        response = 'These are the things I can do: ' + command_list_string
    # If the action is generate tweet, call the generate_tweet function
    elif action == 'generate tweet':
        response = 'REACT| ' + generate_tweet_command.generate_tweet(message)
    # If the action is tell you about me, call the tell_you_about_me function
    elif action == 'tell you about me':
        response = personalities_description.return_personalities(message)
    else:
        response= 'I did not understand that command, please try again'
    return response

# ---------------------------------------------------------------------------------#
# Function to choose which discord command to return.
# This function is based on what reaction is given to a message in discord.
# This function is called from the discord bot, and returns a string generated from
# the appropriate function. The string is then sent to discord.
# Inputs:   Message - The message sent to the bot
# Outputs:  String  - The string to send to discord
# ---------------------------------------------------------------------------------#
def reaction_message(message, emoji):
    # Check if the message is a command
    if str(emoji) == '💡':
        return notion_add.add_idea(message=message)
    elif str(emoji) == '✅':
        # TODO: Update discord commands for updating records
        return update_record.update_record('✅',collection='generated_tweets',query = {'altered_tweet': message}, update = {'$set': {'approved': True}})
    elif str(emoji) == '❌':
        return update_record.update_record('❌', collection='generated_tweets',query = {'altered_tweet': message}, update = {'$set': {'approved': False}})
