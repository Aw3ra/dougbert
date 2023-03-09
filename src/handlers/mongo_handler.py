import pymongo
import os
from dotenv import load_dotenv
from .mongo_functions import write_to_db, remove_from_db, read_from_db, find_in_db, update_record

# Set the database URL
# First try to get the database URl using environ for replit,
# if that fails, try to get the database URL from .env file
# ---------------------------------------------------------------------------------#
try:
    dbURL = os.environ['MONGO_DB']
except:
    load_dotenv()
    dbURL = os.getenv('MONGO_DB')

# ---------------------------------------------------------------------------------#
# Function to decide which function to call
# Inputs:   action - the action to take, add or check
#           kwargs - the additional info required for the action
# Outputs:  None
# ---------------------------------------------------------------------------------#
def decide_action(action, **kwargs):
    # Create the database connection
    myclient = pymongo.MongoClient(dbURL)
    myDB = myclient["dashboard"]

    # Call the appropriate function
    # If the action is add, call the add_to_db function
    if action == 'add':
        return write_to_db.write_to_db(myDB, **kwargs)
    # If the action is remove call the remove_from_db function
    elif action == 'remove':
        return remove_from_db.remove_from_db(myDB, **kwargs)
    # If the action is check, call the read_from_db function
    elif action == 'read':
        return read_from_db.read_from_db(myDB, **kwargs)
    # If the action is find, call the find_in_db function
    elif action == 'find':
        return find_in_db.find_document(myDB, **kwargs)
    # If the action is update
    elif action == 'update':
        return update_record.update_document(myDB, **kwargs)
    else:
        return 'Unknown action'
    
    






# 