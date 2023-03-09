import discord as bot
import os
from dotenv import load_dotenv
from handlers import discord_handler

# Set the Discord bot keys
# First try to get keys using environ for running on replit,
# if that fails, try to get keys from .env file
# ---------------------------------------------------------------------------------#
try:
    discord_token = os.environ['DISCORD_API_TOKEN_DEV']
except:
    load_dotenv()
    discord_token = os.getenv('DISCORD_API_TOKEN_DEV')

# ---------------------------------------------------------------------------------#
# Create the discord client
intents = bot.Intents.all()
client = bot.Client(intents=intents)

# ---------------------------------------------------------------------------------#
# Function to start the discord bot
# Inputs:   None
# Outputs:  None
# ---------------------------------------------------------------------------------#
def start_bot():
    # Function for when the bot starts and logs in
    @client.event
    async def on_ready():
        print('We have logged in as {0.user}'.format(client))

    # Function for when a message is sent in discord
    @client.event
    async def on_message(message):
        # If the message isnt from the bot, then process it
        if message.author != client.user:
            # If message mentions the bot, then respond
            if client.user.mentioned_in(message):
                # await message.channel.trigger_typing()
                response = discord_handler.tagged_message(message.content)
                if response.startswith('REACT|'):
                    response = response.replace('REACT| ', '')
                    message = await message.channel.send(response)
                    await message.add_reaction('✅')
                    await message.add_reaction('❌')
                    return
                # Send the response to discord
                else:
                    await message.channel.send(response)
                    return
    
    # Function for handling when a message is reacted to
    @client.event
    async def on_raw_reaction_add(payload):
        channel = client.get_channel(payload.channel_id)
        content = await channel.fetch_message(payload.message_id)
        await content.channel.trigger_typing()
        message_reacted = content.content
        # If the reaction is not from the bot, then process it
        if payload.user_id != client.user.id:
            # Send the response to discord
            await content.channel.send(discord_handler.reaction_message(message_reacted, payload.emoji))


    client.run(discord_token)
