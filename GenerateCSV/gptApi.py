from dotenv import load_dotenv
from openai import OpenAI
import os

env_file_path = ".env"
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
    if title == "":
        return ""
    if language == "pt":
        gptKeywords = getGPTResponse(
            f"""
Me dê 40 palavras-chave que sejam relacionadas a esse título. Separadas por virgulas e ordenadas por ordem de relevância. Aqui está um exemplo:
INPUT:
Faces Diversas: Emoções e Determinação em uma Comunidade Inclusiva
OUTPUT:
emoções, determinação, comunidade inclusiva, diversidade, inclusão, aceitação, igualdade, respeito, empoderamento, diferenças, interação social, coletividade, pertencimento, autoestima, autoaceitação, tolerância, solidariedade, expressão emocional, apoio mútuo, convivência harmoniosa, inclusão social, diálogo aberto, compreensão, diversidade cultural, empatia, apoio emocional, autoconfiança, superação, desenvolvimento pessoal, integração, reconhecimento, celebração, pluralidade, bem-estar emocional, autoconhecimento, cidadania, identidade, amor próprio, comunicação eficaz, colaboração, união.

DON'T ADD ANYTHING TO YOUR ANSWER THAT ISN'T A KEYWORD
Título:
{title}
"""
        )
        return gptKeywords.replace('"', "").replace(".", "")
    else:
        gptKeywords = getGPTResponse(
            f"""
Give me 40 keywords related to this description. Here is an example:
Description:
A close up shot with a 50mm lens capturing a young woman enjoying a cozy moment by the fireplace with a book in hand and a warm blanket draped around her shoulders Soft natural light illuminates the scene creating a tranquil and peaceful atmosphere
Keywords:
Young woman, Cozy moment, Book, Blanket, Soft, Natural light, Embrace, Fireplace, Relaxation, Peaceful, Tranquil, Serene, Comfort, Reading, Contentment, Warmth, Leisure, Enjoyment, Atmosphere, Relaxing, Serenity, Quiet, Home, Coziness, Happiness, Content, Beauty, Calm, Serenity, Joy, Indoors, Female, Lifestyle, Reading by the fireplace, Comfortable, Warm blanket, Quietude, Illumination, Pleasant, Firelight, Relax, Relaxed
Description:
{title}
***The keywords should be ordered by relevancy***
***The keywords should be comma separated***
ONLY AWNSER WITH COMMA SEPARATED KEYWORDS AND NOTHING ELSE!
"""
        )
        return gptKeywords.replace('"', "").replace(".", "")


def createTitle(prompt, language):
    if not prompt:
        return ""
    if language == "pt":
        gptPrompt = f"""
I'm going to give you a brief description of an image, and you should generate a descriptive title for it in Brazillian Portuguese, don't be creative: {prompt}
"""
        gptTitle = getGPTResponse(gptPrompt)
        return gptTitle.replace('"', "")
    else:
        gptPrompt = f"""
I'm going to give you a brief description of an image, and you should generate a descriptive title for it, don't be creative, it should be at least 3 words: {prompt}
"""
        gptTitle = getGPTResponse(gptPrompt)
        return gptTitle.replace('"', "")
