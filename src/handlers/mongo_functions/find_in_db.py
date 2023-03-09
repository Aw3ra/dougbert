# ---------------------------------------------------------------------------------#
# Command to find document in the database
# Inputs:  myDB         - the database to find in
#          collection   - the collection to find in
#          query        - the query to find in the database
#          amount       - the amount of documents to find (One or all)
# Outputs: document(s)  - the document that matches the query
#          e            - if unsuccessful
# ---------------------------------------------------------------------------------#
def find_document(myDB, **kwargs):
    # Set the default values
    default = {'amount': 'one'}
    for key, value in default.items():
        if key not in kwargs:
            kwargs[key] = value
    # Try to find the document in the database
    try: 
        # Check if collection exists
        if kwargs['collection'] in myDB.list_collection_names():
            # If the amount is one, return one document
            if kwargs['amount'] == 'one':
                # Check if the item is in the database
                if myDB[kwargs['collection']].find_one(kwargs['query']):
                    # Find the document
                    document = myDB[kwargs['collection']].find_one(kwargs['query'])
                    # Return the document
                    return document
                # Return False if the item is not in the database
                else:
                    return 'Item does not exist'
            # If the amount is all, return all documents
            elif kwargs['amount'] == 'all':
                documents = []
                for x in myDB[kwargs['collection']].find(kwargs['query']):
                    documents.append(x)
                if len(documents) > 0:
                    return documents
                else:
                    return 'No documents found'
        # Return False if the collection does not exist
        else:
            return 'Collection does not exist'    
    # If there is an error, return the error
    except Exception as e:
        # Return the error
        return 'Oh no, somthing went wrong with: ' + str(e)