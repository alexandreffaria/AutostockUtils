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
    1 : "Animais",
    2 : "Construções e Arquitetura",
    3 : "Negócios",
    4 : "Bebidas",
    5 : "Meio Ambiente",
    6 : "Sentimentos, Emoções e Estados mentais",
    7 : "Comida",
    8 : "Recursos Gráficos",
    9 : "Hobbies e Lazer",
    10 : "Indústria",
    11 : "Paisagens",
    12 : "Estilo de Vida",
    13 : "Pessoas",
    14 : "Plantas e Flores",
    15 : "Religião e Cultura",
    16 : "Ciência",
    17 : "Problemas Sociais",
    18 : "Esportes",
    19 : "Tecnologia",
    20 : "Transportes",
    21 : "Viagens",
}


def getGPTResponse(model, content):
    gptPrompt = [
        {
            "role": "system",
            "content": "Witness the unyielding precision and impact of a stock image maestro, draped in accolades.",
        },
        {"role": "user", "content": f'''
                                        {content}
                                        generate a very descriptive scene, paint it with words, like if you were describing it to a blind person.
                                        don't add anything to your anwser that isn't the description, don't adress me or anything else.
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

    return response.choices[0].message.content.strip()

def main(category, strategy, amount, description):
    date = datetime.now().strftime("%Y-%m-%d")
    filename = f"prompts_{categorias[category]}_{strategy}_{date}.txt"

    with open(filename, "a") as file:
        for _ in range(amount):
            topic_request = f"{description}\nGive me 10 interesting topics on the information above for stock photography that would be easily sold on a stock photography website."
            topics = getGPTResponse(gptModel, topic_request)
            
            # Separate the topics
            topic_list = topics.split("\n")

            for topic in topic_list:
                vivid_description_request = f'''
                "{topic}"
                generate a very descriptive scene, paint it with words, like you were describing it to a blind person.
                don't add anything to your answer that isn't the description, don't address me or anything else.
                '''
                vivid_description = getGPTResponse(gptModel, vivid_description_request)
                
                file.write(
                vivid_description.replace("'", "")
                .replace(",", "") 
                .replace(".", "") 
                .replace("-", "")  
                .replace("(", "")
                .replace(")", "")  
                + '\n')

def main(category, strategy, amount, description):
    date = datetime.now().strftime("%Y-%m-%d")
    filename = f"prompts_{categorias[category]}_{strategy}_{date}.txt"

    if description is None:
        description = f"I want to create images in the topic of {categorias[category]}."

    with open(filename, "a") as file:
        for _ in range(amount):
            topic_request = f"{description}\nGive me 10 interesting topics for stock photography that would be easily sold on a stock photography website."
            topics = getGPTResponse(gptModel, topic_request)
            
            topic_list = topics.split("\n")

            for topic in topic_list:
                vivid_description_request = f'''
                "{topic}"
                generate a very descriptive scene, paint it with words, like if you were describing it to a blind person.
                don't add anything to your answer that isn't the description, don't address me or anything else.
                '''
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
