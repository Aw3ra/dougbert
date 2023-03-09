import openai

# Function to generate an image based on a prompt
# Inputs:   api_key - the OpenAI API key
#           prompt - the prompt to start the image generation
#           n - the number of images to generate
#           size - the size of the images to generate
# Outputs:  URL - the generated image URL
# ---------------------------------------------------------------------------------#

def generate_image(api_key, **kwargs):
    default_kwargs = {'prompt': 'white scenary', 'n': 1, 'size': '1024x1024'}
    default_kwargs.update(kwargs)
    # Set the OpenAI API key
    openai.api_key = api_key
    # Send the prompt to the AI
    response = openai.Image.create(
        prompt=default_kwargs['prompt'],
        n=default_kwargs['n'],
        size=default_kwargs['size']
    )
    image_url = response['data'][0]['url']
    return image_url
