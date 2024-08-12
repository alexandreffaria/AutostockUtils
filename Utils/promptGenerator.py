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
RULES = """
I want you to create a prompt for me for a topic that I'm going to give you. That prompt will then be used to create images, that are going to be sold on a big stock images website. 
FOLLOW THIS RULE:
The Midjourney Bot works best with simple, short sentences that describe what you want to see. 
Avoid long lists of requests and instructions. 
Instead of: Show me a picture of lots of blooming California poppies, make them bright, vibrant orange, and draw them in an illustrated style with colored pencils 
Do: Bright orange California poppies drawn with colored pencils

- Don't repeat yourself
- If you want something to be in text on the image put the text in quotation marks. You can choose to use a text or not, but if you  do, it must be in quotation marks.
- YOUR ANWSER SHOULD ONLY CONTAIN THE DESCRIPTION AND NOTHING ELSE
- Explore the topic and make it interesting but keep the description short but varied.
"""

def getGPTResponse(model, content, previousPrompts):
    gptPrompt = [
        {
            "role": "user", 
            "content": RULES,
        },
        {
            "role": "system",
            "content": "I understand the rules. Give me the topic you want me to create the description.",
        },
        {
            "role": "user", 
            "content": "Drinks",
        },
        {
            "role": "system",
            "content": "Mint mojito with lime garnish",
        },
    ]

    for prompt in previousPrompts:
        gptPrompt.append({"role": "user", "content": prompt[0]})
        gptPrompt.append({"role": "system", "content": prompt[1]})
    
    gptPrompt.append({"role": "user", "content": content})

    response = client.chat.completions.create(
        model=model,
        messages=gptPrompt,
        temperature=1.1,
        max_tokens=4096,
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
    with open(filename, "a", encoding="utf-8") as file:
        previousPrompts = []
        for i in range(amount):
            vivid_description = getGPTResponse(gptModel, description, previousPrompts)
            previousPrompts.append((description, vivid_description))
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
