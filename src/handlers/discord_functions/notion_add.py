from handlers import notion_handler

# ---------------------------------------------------------------------------------#
# Discord command to add an idea to a notion database
# Inputs:   idea - the idea to add
# Outputs:  response - the response to send to discord
# ---------------------------------------------------------------------------------#
def add_idea(**kwargs):
    # Add the idea to the database
    added = notion_handler.notion_command('add idea', message=kwargs['message'])
    # If the idea was added to the database, return true
    if added:
        response = '**Idea recorded**'
    # If the idea was not added to the database, return the error
    else:
        response = '**Failed to add idea**'
    return response