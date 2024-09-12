# Setup
from PIL import Image
from clip_interrogator import Config, Interrogator

# Configuration
caption_model_name = 'blip-large'
clip_model_name = 'ViT-L-14/openai'

config = Config()
config.clip_model_name = clip_model_name
config.caption_model_name = caption_model_name
ci = Interrogator(config)

def image_to_prompt(image, mode='best'):
    ci.config.chunk_size = 2048 if ci.config.clip_model_name == "ViT-L-14/openai" else 1024
    ci.config.flavor_intermediate_count = 2048 if ci.config.clip_model_name == "ViT-L-14/openai" else 1024
    image = image.convert('RGB')
    if mode == 'best':
        return ci.interrogate(image)
    elif mode == 'classic':
        return ci.interrogate_classic(image)
    elif mode == 'fast':
        return ci.interrogate_fast(image)
    elif mode == 'negative':
        return ci.interrogate_negative(image)

# Path to your image
image_path = "imageDescription/test.png"

# Load the image and run the model
image = Image.open(image_path)
prompt = image_to_prompt(image, mode='best')

# Print the result prompt
print(prompt)
