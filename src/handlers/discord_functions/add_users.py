from handlers import twitter_handler, mongo_handler
import re

# ---------------------------------------------------------------------------------#
# Discord command to add users to a database, this also follows them on twitter
# Inputs:   bot_name - the name of the bot to follow the users
#           users   - the users to add
# Outputs:  results - the users that were added to the database, as a string
# ---------------------------------------------------------------------------------#
def add_users(**kwargs):
    users_added = []
    users_not_added = []
    # Loop through each user
    for user in kwargs['users']:
        # Follow the user
        followed = twitter_handler.decide_action('follow', user=user, bot_name=kwargs['bot_name'])
        # If the user was followed, add them to the database
        if followed==True:
            # Add the user to the database
            database_add = mongo_handler.decide_action('add', collection= 'users',query = {'user': user})
            # If the user was added to the database, return true
            if database_add:
                users_added.append('• '+ str(user) + '\n')
            # If the user was not added to the database, return the error
            else:
                database_add = 'Mongo: '+re.sub(r'\D', '', str(database_add))
                users_not_added.append('• '+ str(user) + ' ('+ str(database_add) +')\n')
                # Unfollow the user if it wasnt added to the database
                twitter_handler.decide_action('unfollow', user=user, bot_name=kwargs['bot_name'])
        # If the user was not followed, return the error
        elif followed=='Already following':
            users_not_added.append('• '+ str(user) + ' (Followed) '+ '\n')
        else:
            # Remove any non-numeric characters
            followed = 'Twitter: ' +str(followed)
            users_not_added.append('• '+ str(user) + ' ('+ str(followed) +')\n')
    # Return the users that were added to the database
    results = {'added': users_added, 'not_added': users_not_added}
    # Convert the results to a string
    added = ''.join(results['added'])
    failed = ''.join(results['not_added'])
    # Create the response
    # If there are no failed users, then just return the added users
    if len(failed) == 0:
        response = f'Added\n{added}'
    # If there are no added users, then just return the failed users
    elif len(added) == 0:
        response = f'Failed to add\n{failed}'
    # If there are failed users, then return both added and failed users
    else:
        response = f'Added\n{added}\nFailed to add\n{failed}'
    return response