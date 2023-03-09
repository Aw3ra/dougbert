# ---------------------------------------------------------------------------------#
# Command to read from the database
# Inputs:  myDB - the database to read from
#          collection - the collection to read from
# Outputs: db_data - array of data in dict form
#          e       - if unsuccessful
# ---------------------------------------------------------------------------------#
def read_from_db(myDB, **kwargs):
    # Try to read from the database
    try:
        # Check if collection exists
        if kwargs['collection'] in myDB.list_collection_names():
            # Read from the database
            db_data = []
            for x in myDB[kwargs['collection']].find():
                db_data.append(x)
            if len(db_data) > 0:
                # Return the data
                return db_data
            else:
                return 'No documents found'
        # Return False if the collection does not exist
        else:
            return 'Collection does not exist'
    # If there is an error, return the error
    except Exception as e:
        # Return the error
        return 'Oh no, somthing went wrong with: ' + str(e)
