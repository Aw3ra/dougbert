from notion.client import NotionClient
from handlers import openAI_handler
from .notion_functions import add_new_idea
from dotenv import load_dotenv
import os

# ----------------------------------------------------------------------#
# Load the environment variables for notion
# ----------------------------------------------------------------------#
try:
    notion_token = os.environ['NOTION_API_KEY']
except:
    load_dotenv()
    notion_token = os.getenv('NOTION_API_KEY')

# ----------------------------------------------------------------------#

# ----------------------------------------------------------------------#
# Function to decide which notion command to run
# Inputs:   command - the command to run
#           args - the arguments for the command
# Outputs:  None
# ----------------------------------------------------------------------#
def notion_command(command, message):
    client = NotionClient(token_v2=notion_token)
    try:
        cv = client.get_collection_view('https://www.notion.so/f976fa217e324095b3f2b52743780a0c?v=6dfa2826b6974a3882f8a34d5b9507da')
    except:
        return 'Could not find the collection view'

    # If the command is to add an idea
    if command == 'add idea':
        return add_new_idea.add_idea(cv, message)

