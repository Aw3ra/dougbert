import openai

# ---------------------------------------------------------------------------------#
# Function to generate text
# Inputs:   api_key - the OpenAI API key
#           prompt - the prompt to start the text generation
#           max_tokens - the maximum number of tokens to generate
#           engine - the engine to use for text generation
# Outputs:  the generated text
# ---------------------------------------------------------------------------------#
def generate_text(api_key, **kwargs):
    default_kwargs = {'prompt': 'Say something witty', 'max_tokens': 100, 'engine': 'chatgpt'}
    default_kwargs.update(kwargs)
    kwargs = default_kwargs
    openai.api_key = api_key
    if kwargs['engine'] == 'davinci':
        kwargs['engine'] = 'text-davinci-003'
    elif kwargs['engine'] == 'chatgpt':
        kwargs['engine'] = 'gpt-3.5-turbo'
    elif kwargs['engine'] == 'curie':
        kwargs['engine'] = 'text-curie-001'
    elif kwargs['engine'] == 'babbage':
        kwargs['engine'] = 'text-babbage-001'
    elif kwargs['engine'] == 'ada':
        kwargs['engine'] = 'text-ada-001'

    messages = kwargs['prompt']
    # Send the prompt to the AI
    response = openai.ChatCompletion.create(
        model=kwargs['engine'],
        messages=messages,
        max_tokens=kwargs['max_tokens'],
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    # Return the response
    return response['choices'][0]['message']['content']