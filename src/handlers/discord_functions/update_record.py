from handlers import mongo_handler

# ---------------------------------------------------------------------------------#
# Discord command to edit a record in the database
# Inputs:   message - the message to edit and check for the record to edit
#           status  - the status of the tweet(approved, rejected, etc)              
# Outputs:  results - the string to return to the discord channel
# ---------------------------------------------------------------------------------#
def update_record(emoji, **kwargs):
    # Update the record
    results = mongo_handler.decide_action('update',**kwargs)
    if results:
        if str(emoji)=='✅':
            return '**Tweet approved**'
        elif str(emoji)=='❌':
            return '**Tweet rejected**'
    else:
        return '**Error updating tweet:**' + results 