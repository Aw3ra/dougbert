# ---------------------------------------------------------------------------------#
# Command to remove from the database
# Inputs:  myDB - the database to remove from
#          collection - the collection to remove from
#          query - the query to remove from the database
#          amount - the amount of documents to remove (One or all)
# Outputs: True     - if successful
#          e        - if unsuccessful
# ---------------------------------------------------------------------------------#
def remove_from_db(myDB, **kwargs):
    # Set the default values
    default = {'amount': 'one'}
    for key, value in default.items():
        if key not in kwargs:
            kwargs[key] = value
    # Try to remove from the database
    try: 
        # Check if collection exists
        if kwargs['collection'] in myDB.list_collection_names():
            # Check if the item is in the database
            if myDB[kwargs['collection']].find_one(kwargs['query']):
                # Check if the amount is one
                if kwargs['amount'] == 'one':
                    # Remove from the database
                    deleted = myDB[kwargs['collection']].delete_one(kwargs['query'])
                    # Check if the user has been removed from the database
                    if myDB[kwargs['collection']].find_one(kwargs['query']):
                        # Return False if unsuccessful
                        return False
                    else:
                        print('deleted')
                elif kwargs['amount'] == 'all':
                    # Remove from the database
                    myDB[kwargs['collection']].delete_many(kwargs['query'])
                    # Check if the user has been removed from the database
                    if myDB[kwargs['collection']].find(kwargs['query']):
                        # Return False if unsuccessful
                        return False
                # Return True if successful
                return True
            # Return False if the item is not in the database
            else:
                return 'Item does not exist'
        # Return False if the collection does not exist
        else:
            return 'Collection does not exist'    
    # If there is an error, return the error
    except Exception as e:
        # Return the error
        return 'Oh no, somthing went wrong with: ' + str(e)