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
        for _ in range(amount):
            for _ in range(10):  # Loop to get 10 topics
                topic_request = f"{description}\nGive me an interesting topic for stock photography that would be easily sold on a stock photography website."
                topic = ""
                while not topic.strip() or "sorry" in topic.lower():
                    topic = getGPTResponse(gptModel, topic_request)
                
                vivid_description = ""
                vivid_description_request = f'''
                "{topic}"
                Describe a scene, summarizing the the feeling of the above topic, using descriptive words.
                Don't add anything to your answer that isn't the description, don't address me or anything else.
                
                '''
                while not vivid_description.strip() or "sorry" in vivid_description.lower():
                    vivid_description = getGPTResponse(gptModel, vivid_description_request)
                
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
