from handlers import mongo_handler

# ---------------------------------------------------------------------------------#
# Function to scrape the followers from the bot requested
# Inputs:  auth - the authentication object for the user to follow
#          following - the list of users that the bot is following
#          database - the database to check against for duplicates and to add new tweets to
# Outputs: True - if users were successfully scraped
#          False - if no users were scraped
#          e    - if any error occurs
# ---------------------------------------------------------------------------------#
def scrape_following(auth, following, database):
    # Pull the users from the database
    all_users = mongo_handler.decide_action('read', collection=database)
    try:
        # If the data in following exists
        if following.data != None:
            # Create an array of user dictionaries
            new_user_array = []
            for users in following.data:
                new_user = {'user': users.data['username'], 'user_id': int(users.data['id']), 'followers': 0,}
                # If the user is unique
                if is_unique(new_user, all_users):
                    # Add the user to the array of new users
                    new_user_array.append(new_user)
            # If there are new users
            print(len(new_user_array))
            if len(new_user_array) > 0:
                # Add the new users to the database
                for users in new_user_array:
                    print(mongo_handler.decide_action('add', collection=database, query=users))
            # Function here for updating the amount of followers each user has
            # TODO - Add function here
                return True
            else:
                return False
    except Exception as e:
        return e

# ---------------------------------------------------------------------------------#
# Function to check if the user is unique
# Inputs:  user - the user to check
#          user_array - the array of users to check against
# Outputs: True - if the user is unique
#          False - if the user is not unique
# ---------------------------------------------------------------------------------#
def is_unique(user, user_array):
    # If the all users array is a string
    if type(user_array) == str:
        return True
    # For each user in the user array
    for users in user_array:
        # If the user is unique
        if users['user_id'] == user['user_id']:
            return False
    return True