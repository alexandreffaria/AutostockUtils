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
Me dê 30 palavras chaves que sejam relacionadas ao título de uma imagem que vou te passar no fim dessa mensagem.
Organize as palavras chave por ordem de relevância, e nunca utilize palavras genéricas como 'imagem', ou 'cena'.
Todas as palavras chave devem ser separadas por vírgulas
Apenas me de as palavras-chave me portugues sem nenhuma outra informação em sua resposta

EXEMPLO:
ENTRADA:
Uma jovem moça aproveitando um momento aconchegante perto de uma lareira lendo um livro em atmosfera tranquila
SAÍDA:
mulheres, livro, em casa, gente, sorridente, adolescente, quarto, lazer, cama, ler, beldade, sentado, sofá, rir, pessoa, estudante, educação

TÍTULO: {title}
"""
    )
    return gptKeywords.replace('"', "")

def createTitle(title):
    gptTitle = getGPTResponse(
f"""
I'm going to give you a title in English and you should create an similar one but in Portuguese, the title should not be longer than 200 letters! 
Just give me the translation with no other information in your response. Don't use any pontualtion like (',.-!)
Here is and example:
INPUT:
A close up shot with a 50mm lens capturing a young woman enjoying a cozy moment by the fireplace with a book in hand and a warm blanket draped around her shoulders Soft natural light illuminates the scene creating a tranquil and peaceful atmosphere
OUTPUT:
Uma jovem moça aproveitando um momento aconchegante perto de uma lareira lendo um livro em atmosfera tranquila com um cobertor quente nos ombros

Here is the title:
{title}
""",
    )
    return gptTitle.replace('"', "")
