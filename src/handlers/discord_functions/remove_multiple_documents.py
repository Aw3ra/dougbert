from handlers import mongo_handler

# ---------------------------------------------------------------------------------#
# Discord command to remove all documents from a collection by a specific user
# Inputs:  collection - the collection to read from
#          query      - the query to remove from the database
#          amount     - the amount of documents to remove
# Outputs: count      - the number of documents removed
#          error      - if there was an error
# ---------------------------------------------------------------------------------#
def remove_multiple_documents(**kwargs):
    # Read from the database
    db_data = mongo_handler.decide_action('read', collection=kwargs['collection'])
    # If the data was read, return the data
    if db_data != 'Collection does not exist':
        # Find all the documents by the user
        user_docs = mongo_handler.decide_action('find', **kwargs)
        if not isinstance(user_docs, str):
            count = len(list(user_docs))
            # If there are documents, remove them
            if count > 0:
                # Remove the documents
                removed = mongo_handler.decide_action('remove', **kwargs)
                if removed:
                    # Return the number of documents removed
                    return count
                # If the documents were not removed, return the error
                else:
                    return removed
            # If there are no documents, return 0
            else:
                return 'There are no documents by that user'
        # If there was an error, return the error
        else:
            return user_docs
    # If the data was not read, return the error
    else:
        return db_data