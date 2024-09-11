import os
import base64
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
env_file_path = ".env"
load_dotenv(env_file_path)

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def get_image_description(image_path, prompt):
    # Load API key from environment variables
    api_key = os.getenv("OPENAI_API_KEY")
    
    # Encode the image to base64
    base64_image = encode_image(image_path)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": f"Describe this image completely, everything in the image should be described.\n Here is the prompt used to create this image to give you context:\n{prompt}"},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image}"
                            "detail": "low" 
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    return response.json()["choices"][0]["message"]["content"]

if __name__ == "__main__":
    image_path = "fil.png"  # Provide the path to your local image here
    description = get_image_description(image_path)
    print("Image Description:", description)
