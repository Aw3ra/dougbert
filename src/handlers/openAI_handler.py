import os
from dotenv import load_dotenv
from .openai_functions import generate_text, generate_image, get_command, get_users


# Set the OpenAI API keys
# First try to get keys using environ for running on replit,
# if that fails, try to get keys from .env file
# ---------------------------------------------------------------------------------#
try:
    OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
except:
    load_dotenv()
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')


# ---------------------------------------------------------------------------------#

# Function to decide which function to call
# Inputs:   auth - the auth token
#           action - the action to take, follow or unfollow
#           kwargs - the additional info required for the action
# Outputs:  None
# ---------------------------------------------------------------------------------#
def decide_action(action, **kwargs):
    if action == 'text':
        return generate_text.generate_text(OPENAI_API_KEY, **kwargs)
    elif action == 'image':
        return generate_image.generate_image(OPENAI_API_KEY, **kwargs)
    elif action == 'get_command':
        return get_command.get_command(OPENAI_API_KEY, **kwargs)
    elif action == 'get_users':
        return get_users.get_users(OPENAI_API_KEY, **kwargs)
    elif action == 'generate idea':
        return generate_text.generate_text(OPENAI_API_KEY, **kwargs)

# ---------------------------------------------------------------------------------#