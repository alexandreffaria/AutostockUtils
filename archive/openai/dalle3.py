from openai import OpenAI
from dotenv import load_dotenv
import os
import requests  # Import the requests library

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
OpenAI.api_key = api_key

client = OpenAI()

prompt_text = "Design a winter jacket for a fashion show."  # Replace with your prompt
response = client.images.generate(
    model="dall-e-3",
    prompt=prompt_text,
    size="1024x1024",
    quality="standard",
    n=1,
)

# Extract the image URL from the response
image_url = response.data[0].url

# Make a request to the image URL and save the content to a file
output_folder = "output_results"
os.makedirs(output_folder, exist_ok=True)

# Generate a filename based on the prompt text
image_filename = os.path.join(
    output_folder, f"{prompt_text.replace(' ', '_')}_generated_image.jpg"
)
response = requests.get(image_url)

if response.status_code == 200:
    with open(image_filename, "wb") as file:
        file.write(response.content)
    print(f"Image saved to {image_filename}")
else:
    print(f"Failed to download the image. Status code: {response.status_code}")
