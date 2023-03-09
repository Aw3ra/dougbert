from handlers import openAI_handler

# ----------------------------------------------------------------------#
# Function to add a new idea to the database
# Inputs:   cv - the collection view to add the idea to
#           name - the name of the project it relates too
#           idea - the idea
# Outputs:  None
# ----------------------------------------------------------------------#
def add_idea(cv, message):
    try:
        row = cv.collection.add_row()
        row.name = message.author.name
        row.idea = openAI_handler.decide_action('generate idea', message=message, prompt='Explain this in 5 words or less: '+message.content)
        row.status = 'New'
        row.message = message.content
        return True
    except Exception as e:
        return e
