# ---------------------------------------------------------------------------------#
# Command to write to the database
# Inputs:  query         - dictionary of tweet attributes
#          collection   - the database to write to
# Outputs: True         - if successful
#          e            - if unsuccessful
# ---------------------------------------------------------------------------------#
def write_to_db(myDB, **kwargs):
    # Try to write to the database
    try: 
        # Check if collection exists
        if kwargs['collection'] in myDB.list_collection_names():
            # Check if the item is already in the database
            if myDB[kwargs['collection']].find_one(kwargs['query']):
                # Return value if the item is already in the database
                return 'Item exists'
            # Write to the database
            myDB[kwargs['collection']].insert_one(kwargs['query'])
            # Check if the user has been added to the database
            if myDB[kwargs['collection']].find_one(kwargs['query']):
                # Return True if successful
                return True
            # Return False if unsuccessful
            return False
        # Return False if the collection does not exist
        else:
            return 'Collection does not exist'    
    # If there is an error, return the error
    except Exception as e:
        # Return the error
        return 'Oh no, somthing went wrong with: ' + str(e)