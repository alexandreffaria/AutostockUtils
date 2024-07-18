from dotenv import load_dotenv
from openai import OpenAI
from argparse import ArgumentParser
from datetime import datetime
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
OpenAI.api_key = api_key

client = OpenAI()

# gptModel = "gpt-3.5-turbo-1106"
# gptModel = "gpt-4"
gptModel = "gpt-4o-mini"
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
            "content": "",
        },
        {
            "role": "user", 
            "content": content,
        }
    ]

    response = client.chat.completions.create(
        model=model,
        messages=gptPrompt,
        temperature=1.1,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

    return response.choices[0].message.content.strip()

def main(category, strategy, amount, description):
    date = datetime.now().strftime("%Y-%m-%d")
    output_folder = "promptGeneratorOutput"
    os.makedirs(output_folder, exist_ok=True)  # Create the folder if it doesn't exist
    filename = f"{output_folder}/prompts_{categorias[category]}_{strategy}_{date}.txt"
    if not description:
        description = categorias[category]
    with open(filename, "a",encoding="utf-8") as file:
        
        for i in range(amount):
                vivid_description = ""
                vivid_description_request = f'''
I want you to create a prompt for me for a topic that I'm going to give you. That prompt will than be used to create images, that are going to be sold in a big stock images website. 
FOLLOW THIS RULE:
The Midjourney Bot works best with simple, short sentences that describe what you want to see. 
Avoid long lists of requests and instructions. 
Instead of: Show me a picture of lots of blooming California poppies, make them bright, vibrant orange, and draw them in an illustrated style with colored pencils 
Do: Bright orange California poppies drawn with colored pencils
Here is the topic:
Topic: "{description}"
***ONLY GIVE ONE DESCRIPTION AT THE TIME WITH NO INFORMATION OTHER THAN THE DESCRIPTION ITSELF***
be a little bit creative every now and again c:
your anwser should look exactly like this: Fruit smoothie with colorful striped straws.
give me 15 different prompts at a time. One on each line, exactly like this:
Mint mojito with lime garnish
Cappuccino with cocoa powder on top
Cup of coffee with latte art
Pink lemonade with sliced lemons and mint leaves
Cold glass of water with lemon slices
Cocoa with marshmallows on top
Flavored water with fresh fruits and herbs
DONT EVER ADDRESS ME ONLY GIVE ME THE PROMPTS
                '''
                while not vivid_description.strip() or "sorry" in vivid_description.lower() or "cannot" in vivid_description.lower():
                    vivid_description = getGPTResponse(gptModel, vivid_description_request)
                    
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
