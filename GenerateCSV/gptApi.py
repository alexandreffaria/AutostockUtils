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

NÃO ADICIONE NADA NA SUA RESPOSTA QUE NÃO SEJAM PALAVRAS-CHAVE; TODAS AS PALAVRAS-CHAVE DEVEM SER EM PORTUGUÊS BRASILEIRO.
Título:
{title}
"""
        )
        return gptKeywords.replace('"', "").replace(".", "")
    else:
        gptKeywords = getGPTResponse(
            f"""
Give me 40 keywords related to this description, you should give me at least 6 keywords. Here is an example:
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
I'm going to give you a brief description of an image, and you should generate a descriptive title for it in Brazillian Portuguese, don't be creative. 
Here is an example:
Anxiety and stress portrayed as dark stormy clouds
output:
Ansiedade e estresse representados com formas abstratas
Here is the description: {prompt}
"""
        gptTitle = getGPTResponse(gptPrompt)
        return gptTitle.replace('"', "")
    else:
        gptPrompt = f"""
I'm going to give you a brief description of an image, and you should generate a descriptive title for it, don't be creative, it should be at least 3 words:
Here is an example:
Anxiety and stress portrayed as dark stormy clouds
output:
Anxiety and stress portrayed as dark stormy clouds
Here is the description: {prompt}
"""
        gptTitle = getGPTResponse(gptPrompt)
        return gptTitle.replace('"', "")

def createTitleWithoutPrompt(prompt, language):
    print(f"PROMTP: {prompt}")

    if language == "pt":
        gptPrompt = f"""
Eu vou te fornecer uma descrição incompleta de uma imagem, você deve fazer o mínimo possível, ou até mesmo nada se for o caso, para completar a descrição, e então crie um título simples, descritivo e apropriado para essa imagem. Deve conter pelo menos 5 palavras, não seja nem um pouco criativo, e sua resposta deve ser apenas o título, não adicione nada mais que ele. Sempre me dê um título completo: {prompt}
"""
        gptTitle = getGPTResponse(gptPrompt)
        print(f"GPTTITLE: {gptTitle}")
        return gptTitle.replace('"', "")
    else:
        gptPrompt = f"""
I'm going to give you an incomplete description of an image, you should do as little as possible, if at all, to complete the description, and create a simple, discriptive and appropriate title for it. It should be at least 5 words long, and don't be creative at all, and your answer should be only the title, don't add anything else to it. Always give me a complete title: {prompt}
"""
        gptTitle = getGPTResponse(gptPrompt)
        print(f"GPTTITLE: {gptTitle}")
        return gptTitle.replace('"', "")
