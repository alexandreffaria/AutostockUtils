from dotenv import load_dotenv
from openai import OpenAI
import os

env_file_path = '/home/meulindux/AutostockUtils/.env'
gptModel = "gpt-3.5-turbo-1106"

load_dotenv(env_file_path)
OpenAI.api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI()

def getGPTResponse(content):
    gptPrompt = [
        {
            "role": "system",
            "content": "",
        },
        {"role": "user", "content": content},
    ]

    response = client.chat.completions.create(
        model=gptModel,
        messages=gptPrompt,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

    return response.choices[0].message.content.strip()



def getKeywords(title):
    gptKeywords = getGPTResponse(
f"""
Me dê 40 palavras chaves que sejam relacionadas a esse título. Separadas por virgulas e ordenadas por ordem de relevância:
{title}
"""
)
    return gptKeywords.replace('"', "").replace(".", "")

def createTitle(title):
    gptTitle = getGPTResponse(
f"""
I'm going to give you a description of an image in English and you should create a title summarizing the description, try to use every important point of the description, 
Here is an example:

INPUT:
A close up shot with a 50mm lens capturing a young woman enjoying a cozy moment by the fireplace with a book in hand and a warm blanket draped around her shoulders Soft natural light illuminates the scene creating a tranquil and peaceful atmosphere
OUTPUT:
Uma jovem moça aproveitando um momento aconchegante perto de uma lareira lendo um livro em atmosfera tranquila com um cobertor quente nos ombros

***the title should have 20 words maximum! ***
***the title should be in Brazilian Portuguese***

Here is the title:
{title}
""",
)
    return gptTitle.replace('"', "")
