from dotenv import load_dotenv
from openai import OpenAI
import os

env_file_path = "/home/meulindux/AutostockUtils/.env"
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


def getKeywords(title, language):
    if language == "pt":
        gptKeywords = getGPTResponse(
        f"""
Me dê 40 palavras-chave que sejam relacionadas a esse título. Separadas por virgulas e ordenadas por ordem de relevância. Aqui está um exemplo:
Título:
Faces Diversas: Emoções e Determinação em uma Comunidade Inclusiva
Palavras-chave:
emoções, determinação, comunidade inclusiva, diversidade, inclusão, aceitação, igualdade, respeito, empoderamento, diferenças, interação social, coletividade, pertencimento, autoestima, autoaceitação, tolerância, solidariedade, expressão emocional, apoio mútuo, convivência harmoniosa, inclusão social, diálogo aberto, compreensão, diversidade cultural, empatia, apoio emocional, autoconfiança, superação, desenvolvimento pessoal, integração, reconhecimento, celebração, pluralidade, bem-estar emocional, autoconhecimento, cidadania, identidade, amor próprio, comunicação eficaz, colaboração, união.

Título:
{title}
"""
        )
        return gptKeywords.replace('"', "").replace(".", "")
    else:
        gptKeywords = getGPTResponse(
        f"""
Give me 40 keywords related to this title. Here is an example:
Title:
Young Woman Embraces Cozy Moment with Book and Blanket, Bathed in Soft Natural Light
Keywords:
Young woman, Cozy moment, Book, Blanket, Soft, Natural light, Embrace, Fireplace, Relaxation, Peaceful, Tranquil, Serene, Comfort, Reading, Contentment, Warmth, Leisure, Enjoyment, Atmosphere, Relaxing, Serenity, Quiet, Home, Coziness, Happiness, Content, Beauty, Calm, Serenity, Joy, Indoors, Female, Lifestyle, Reading by the fireplace, Comfortable, Warm blanket, Quietude, Illumination, Pleasant, Firelight, Relax, Relaxed
Título:
{title}
***The keywords should be comma separated***
***The keywords should be ordered by relevancy***
"""
        )
        return gptKeywords.replace('"', "").replace(".", "")

def createTitle(title, language):
    if language == "pt":   
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
"""
)
        return gptTitle.replace('"', "")
    else:
        gptTitle = getGPTResponse(
            f"""
I'm going to give you a description of an image  and you should create a title summarizing the description, try to use every important point of the description, 
Here is an example:

INPUT:
A close up shot with a 50mm lens capturing a young woman enjoying a cozy moment by the fireplace with a book in hand and a warm blanket draped around her shoulders Soft natural light illuminates the scene creating a tranquil and peaceful atmosphere
OUTPUT:
Young Woman Embraces Cozy Moment with Book and Blanket, Bathed in Soft Natural Light

***the title should have 20 words maximum! ***


Here is the title:
{title}
"""
)
        return gptTitle.replace('"', "")

    
