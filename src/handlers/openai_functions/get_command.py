import openai

# ---------------------------------------------------------------------------------#
# Function to extract a command out of a message sent in discord
# Inputs:   api_key - the api key for openAI
#           prompt - the prompt to start the text generation
#           max_tokens - the maximum number of tokens to generate
#           engine - the engine to use for text generation
#           command_list - the list of commands to look for
# Outputs:  the generated text, should be a single command
# ---------------------------------------------------------------------------------#
def get_command(api_key, **kwargs):
    default_kwargs = {'prompt': 'Do nothing', 'max_tokens': 1000, 'engine': 'davinci'}
    default_kwargs.update(kwargs)
    kwargs = default_kwargs
    openai.api_key = api_key
    if kwargs['engine'] == 'davinci':
        kwargs['engine'] = 'text-davinci-003'
    elif kwargs['engine'] == 'curie':
        kwargs['engine'] = 'text-curie-001'
    elif kwargs['engine'] == 'babbage':
        kwargs['engine'] = 'text-babbage-001'
    elif kwargs['engine'] == 'ada':
        kwargs['engine'] = 'text-ada-001'

    question = 'Which of these commands ('+kwargs['list_of_commands']+') accurately describes this message:' + kwargs['prompt']

    # Send the prompt to the AI
    response = openai.Completion.create(
        model=kwargs['engine'],
        prompt=question,
        max_tokens=kwargs['max_tokens'],
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    # Return the response
    return response['choices'][0]['text'].replace('\n', '')