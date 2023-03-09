# ---------------------------------------------------------------------------------#
# Function to unfollow a select user
# Inputs:  auth - the authentication object
#          user - the user to unfollow
# Outputs: True - if the user was unfollowed
#          'Not following' - if the user is not being followed
#          'User not found' - if the user could not be found
#          'No following data' - if there is no following data
#          e    - if any error occurs
# ---------------------------------------------------------------------------------#
def unfollow_user(auth,auth2, following, **kwargs):
    # Try to unfollow the user
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
                    # Unfollow the user
                    if auth.unfollow_user(user_id):
                        # Return True if successful
                        return True
                    # Return False if unsuccessful
                    return False
            # Return that the user is not being followed
            return 'Not following'
        else:
            # Return that the user could not be found
            return 'No following data'
    # If there is an error, return the error
    except Exception as e:
        # Return the error
        return e