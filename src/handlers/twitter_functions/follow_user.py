# ---------------------------------------------------------------------------------#
# Function to follow a select user
# Inputs:  auth - the authentication object
#          auth2 - the authentication object for the user to follow
#          following - the list of users that the bot is following
#          user - the user to follow
# Outputs: True - if the user was followed
#          'Already following' - if the user is already being followed
#          'User not found' - if the user could not be found
#          'No following data' - if there is no following data
#          e    - if any error occurs
# ---------------------------------------------------------------------------------#
def follow_user(auth,auth2, following, **kwargs):
    # Try to follow the user
    try:
        # Find the user id
        user_id = auth2.get_user(username=kwargs['user']).data
        # If the user is not found, return the error
        if user_id == None:
            return 'User not found'
        # Get the user id
        user_id = user_id['id']
        # Make sure the returned user exists
        if following.data != None:
            # Check against the list of users that the bot is following
            for user in following.data:
                # If the user is already being followed, return ALready following
                if user['id'] == user_id:
                    # Return Already following if the user is already being followed
                    return 'Already following'
        else:
            # Return that the user could not be found
            return 'No following data'
        # Follow the user
        if auth.follow_user(user_id):
            # Return True if successful
            return True
        # Return False if unsuccessful
        return False
    # If there is an error, return the error
    except Exception as e:
        # Return the error
        return e