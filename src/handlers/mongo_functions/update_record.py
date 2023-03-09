# ---------------------------------------------------------------------------------#
# Command to update a document in the database
# Inputs:  myDB         - the database to update in
#          collection   - the collection to update in
#          query        - the query to update in the database
#          update       - the update to make to the document
# Outputs: document(s)  - the document that matches the query
#          e            - if unsuccessful
# ---------------------------------------------------------------------------------#
def update_document(myDB, **kwargs):
    # Try to update the document in the database
    try:
        # Check if collection exists
        if kwargs['collection'] in myDB.list_collection_names():
            # Check if the item is in the database
            if myDB[kwargs['collection']].find_one(kwargs['query']):
                # Update the document
                myDB[kwargs['collection']].update_one(kwargs['query'], kwargs['update'])
                # Return True
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