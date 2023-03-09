from handlers import twitter_handler, mongo_handler
import re

# ---------------------------------------------------------------------------------#
# Discord command to remove users from a database, this also unfollows them on twitter
# Inputs:   bot_name - the name of the bot to unfollow the users
#           users   - the users to remove
# Outputs:  results - the users that were removed from the database, as a string
# ---------------------------------------------------------------------------------#
def remove_users(**kwargs):
    users_removed = []
    users_not_removed = []
    # Loop through each user
    for user in kwargs['users']:
        # Unfollow the user
        unfollowed = twitter_handler.decide_action('unfollow', user=user, bot_name=kwargs['bot_name'])
        # If the user was unfollowed, remove them from the database
        if unfollowed==True:
            # Remove the user from the database
            database_remove = mongo_handler.decide_action('remove', collection= 'users',query = {'user': user})
            # If the user was removed from the database, return true
            if database_remove:
                users_removed.append('• '+ str(user) + '\n')
            # If the user was not removed from the database, return the error
            else:
                database_remove = 'Mongo: '+re.sub(r'\D', '', str(database_remove))
                users_not_removed.append('• '+ str(user) + ' ('+ str(database_remove) +')\n')
        # If the user was not unfollowed, return the error
        elif unfollowed=='Not following':
            users_not_removed.append('• '+ str(user) + ' (Not followed) '+ '\n')
            # Remove the user from the database if it isnt followed
            mongo_handler.decide_action('remove', collection= 'users',query = {'user': user})
        else:
            # Remove any non-numeric characters
            unfollowed = 'Twitter: ' +str(unfollowed)
            users_not_removed.append('• '+ str(user) + ' ('+ str(unfollowed) +')\n')
    # Return the users that were removed from the database
    results = {'removed': users_removed, 'not_removed': users_not_removed}
    # Convert the results to a string
    removed = ''.join(results['removed'])
    failed = ''.join(results['not_removed'])
    # Create the response
    # If there are no failed users, then just return the removed users
    if len(failed) == 0:
        response = f'Removed\n{removed}'
    # If there are no removed users, then just return the failed users
    elif len(removed) == 0:
        response = f'Failed to remove\n{failed}'
    # If there are failed users, then return both removed and failed users
    else:
        response = f'Removed\n{removed}\nFailed to remove\n{failed}'
    return response
    