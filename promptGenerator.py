from dotenv import load_dotenv
from openai import OpenAI
from argparse import ArgumentParser
from datetime import datetime
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
OpenAI.api_key = api_key

client = OpenAI()

gptModel = "gpt-3.5-turbo-1106"
# gptmodel = "gpt-4"
prompts_file_path = "prompts.txt"


categorias = {
    1: "Animals",
    2: "Buildings and Architecture",
    3: "Business",
    4: "Drinks",
    5: "Environment",
    6: "Feelings, Emotions, and Mental States",
    7: "Food",
    8: "Graphic Resources",
    9: "Hobbies and Leisure",
    10: "Industry",
    11: "Landscapes",
    12: "Lifestyle",
    13: "People",
    14: "Plants and Flowers",
    15: "Religion and Culture",
    16: "Science",
    17: "Social Issues",
    18: "Sports",
    19: "Technology",
    20: "Transportation",
    21: "Travel",
}


def getGPTResponse(model, content):
    gptPrompt = [
        {
            "role": "system",
            "content": "You are a stock image photographer with years of experience.",
        },
        {
            "role": "user", 
            "content": f'''
                            {content}
                        '''},
    ]

    response = client.chat.completions.create(
        model=model,
        messages=gptPrompt,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

    return response.choices[0].message.content.strip().replace("'", "").replace(",", "").replace(".", "").replace("-", "").replace("(", "").replace(")", "")

def main(category, strategy, amount, description):
    date = datetime.now().strftime("%Y-%m-%d")
    output_folder = "promptGeneratorOutput"
    os.makedirs(output_folder, exist_ok=True)  # Create the folder if it doesn't exist
    filename = f"{output_folder}/prompts_{categorias[category]}_{strategy}_{date}.txt"
    if not description:
        description = categorias[category]
    with open(filename, "a") as file:
        
        for i in range(amount):
                vivid_description = ""
                vivid_description_request = f'''
                I want you to describe images for me for a topic that I'm going to give you, those images should give descriptions commonly found in stock image photography. 
                Here are a few rules I want you to follow:
                - If there is people in your description, you should always make sure to include "close up shot" in your description. You only have to to this if there are people in your description
                - You should avoid describing scenes that focus on human hands, like people toasting, high fiving, holding hands. The only exception is *shaking hands*
                - Every description should be focused and of one scene at a time.
                - You should be brief but you should describe the whole frame of the image, like the background, the foreground, what is in focus and everything you think is important to be in the image.
                - Your description should be like a director of photography planning, in the way that you should describe the type of lens (macro, telephoto, etc) what is the framing (close, medium or wide shot), at what position the point of focus should be (center frame, bottom third, golden ratio, etc) , soft natural light, warm tones, etc.
                Here is an example of the first rule:
                WRONG - A diverse group of professionals engaged in a lively discussion around a conference table, with laptops and paperwork scattered across the surface.
                RIGHT - A close up shot with a 35mm lens with a diverse group of professionals framed at the center of the frame, engaged in a lively discussion around a conference table, with laptops and paperwork scattered across the surface.

                Here is the topic:
                Topic: "{description}"
                ***ONLY GIVE ONE DESCRIPTION AT THE TIME WITH NO INFORMATION OTHER THAN THE DESCRIPTION ITSELF***
                '''
                while not vivid_description.strip() or "sorry" in vivid_description.lower():
                    vivid_description = getGPTResponse(gptModel, vivid_description_request)
                    print(vivid_description)
               

                print(f"{i}: {vivid_description}")

                file.write(vivid_description + "\n")


if __name__ == "__main__":
    # Set up command-line argument parsing
    parser = ArgumentParser(
        description="Generate prompts with specific strategy and saves it to a file."
    )
    parser.add_argument("--category", type=int, required=True)
    parser.add_argument("--strategy", type=str, required=True)
    parser.add_argument("--amount", type=int, required=True)
    parser.add_argument("--description", type=str)

    # Parse the command-line arguments
    args = parser.parse_args()

    # Call the function to create the CSV file
    main(args.category, args.strategy, args.amount, args.description)
