from handlers import mongo_handler
import re

# ---------------------------------------------------------------------------------#
# Discord command to list all the users in the database
# Inputs:  collection - the collection to read from
# Outputs: response   - the users in the database, as a string
# ---------------------------------------------------------------------------------#
def list_users(**kwargs):
    # Read from the database
    db_data = mongo_handler.decide_action('read', collection=kwargs['collection'])
    # If the data was read, return the data
    if db_data != 'Collection does not exist':
        # Create the response
        response = 'Users in the database:\n'
        # Loop through each user
        for user in db_data:
            # Add the user to the response
            response = response + '• ' + str(user['user']) + '\n'
        # Return the response
        return response
    # If the data was not read, return the error
    else:
        return db_data