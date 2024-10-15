from dotenv import load_dotenv
from openai import OpenAI
import os

env_file_path = ".env"
# gptModel = "gpt-3.5-turbo-1106"
gptModel = "gpt-4o-mini"

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

    if language == "pt":
        gptPrompt = f"""
Eu vou te fornecer uma descrição incompleta de uma imagem, você deve fazer o mínimo possível, ou até mesmo nada se for o caso, para completar a descrição, e então crie um título simples, descritivo e apropriado para essa imagem. Deve conter pelo menos 5 palavras, não seja nem um pouco criativo, e sua resposta deve ser apenas o título, não adicione nada mais que ele. Sempre me dê um título completo: {prompt}
"""
        gptTitle = getGPTResponse(gptPrompt)
        return gptTitle.replace('"', "")
    else:
        gptPrompt = f"""
I'm going to give you an incomplete description of an image, you should do as little as possible, if at all, to complete the description, and create a simple, discriptive and appropriate title for it. It should be at least 5 words long, and don't be creative at all, and your answer should be only the title, don't add anything else to it. Always give me a complete title: {prompt}
"""
        gptTitle = getGPTResponse(gptPrompt)
        return gptTitle.replace('"', "")


def getCategory(description, platform):
    if platform == "a":
        categories = """
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
"""
    elif platform == "d":
        categories = """
211: "Abstract -> Aerial",
112: "Abstract -> Backgrounds",
39: "Abstract -> Blurs",
164: "Abstract -> Colors",
40: "Abstract -> Competition",
41: "Abstract -> Craftsmanship",
42: "Abstract -> Danger",
43: "Abstract -> Exploration",
158: "Abstract -> Fun",
44: "Abstract -> Help",
149: "Abstract -> Love",
45: "Abstract -> Luxury",
187: "Abstract -> Mobile",
46: "Abstract -> Peace",
165: "Abstract -> Planetarium",
47: "Abstract -> Power",
48: "Abstract -> Purity",
128: "Abstract -> Religion",
155: "Abstract -> Seasonal & Holiday",
49: "Abstract -> Security",
50: "Abstract -> Sports",
51: "Abstract -> Stress",
52: "Abstract -> Success",
53: "Abstract -> Teamwork",
141: "Abstract -> Textures",
54: "Abstract -> Unique",
31: "Animals -> Birds",
33: "Animals -> Farm",
36: "Animals -> Insects",
32: "Animals -> Mammals",
34: "Animals -> Marine life",
30: "Animals -> Pets",
35: "Animals -> Reptiles & Amphibians",
37: "Animals -> Rodents",
168: "Animals -> Wildlife",
124: "Arts & Architecture -> Details",
71: "Arts & Architecture -> Generic architecture",
132: "Arts & Architecture -> Historic buildings",
153: "Arts & Architecture -> Home",
73: "Arts & Architecture -> Indoor",
70: "Arts & Architecture -> Landmarks",
131: "Arts & Architecture -> Modern buildings",
130: "Arts & Architecture -> Night scenes",
72: "Arts & Architecture -> Outdoor",
174: "Arts & Architecture -> Ruins & Ancient",
154: "Arts & Architecture -> Work places",
79: "Business -> Communications",
78: "Business -> Computers",
80: "Business -> Finance",
77: "Business -> Industries",
83: "Business -> Metaphors",
84: "Business -> Objects",
75: "Business -> People",
81: "Business -> Still-life",
76: "Business -> Teams",
82: "Business -> Transportation",
85: "Business -> Travel",
178: "Editorial -> Celebrities",
185: "Editorial -> Commercial",
179: "Editorial -> Events",
184: "Editorial -> Landmarks",
180: "Editorial -> People",
181: "Editorial -> Politics",
182: "Editorial -> Sports",
183: "Editorial -> Weather & Environment",
204: "Holidays -> Chinese New Year",
190: "Holidays -> Christmas",
207: "Holidays -> Cinco de Mayo",
203: "Holidays -> Diwali",
193: "Holidays -> Easter",
196: "Holidays -> Fathers Day",
192: "Holidays -> Halloween",
208: "Holidays -> Hanukkah",
206: "Holidays -> Mardi Gras",
195: "Holidays -> Mothers Day",
189: "Holidays -> New Years",
202: "Holidays -> Other",
205: "Holidays -> Ramadan",
191: "Holidays -> Thanksgiving",
194: "Holidays -> Valentines Day",
210: "IT & C -> Artificial Intelligence",
110: "IT & C -> Connectivity",
113: "IT & C -> Equipment",
111: "IT & C -> Internet",
109: "IT & C -> Networking",
212: "Illustrations & Clipart -> AI generated",
166: "Illustrations & Clipart -> 3D & Computer generated",
167: "Illustrations & Clipart -> Hand drawn & Artistic",
163: "Illustrations & Clipart -> Illustrations",
186: "Illustrations & Clipart -> Vector",
101: "Industries -> Agriculture",
89: "Industries -> Architecture",
87: "Industries -> Banking",
93: "Industries -> Cargo & Shipping",
94: "Industries -> Communications",
91: "Industries -> Computers",
90: "Industries -> Construction",
150: "Industries -> Education",
136: "Industries -> Entertainment",
99: "Industries -> Environment",
127: "Industries -> Food & Beverages",
92: "Industries -> Healthcare & Medical",
96: "Industries -> Insurance",
95: "Industries -> Legal",
100: "Industries -> Manufacturing",
102: "Industries -> Military",
161: "Industries -> Oil and gas",
97: "Industries -> Power and energy",
157: "Industries -> Sports",
98: "Industries -> Transportation",
88: "Industries -> Travel",
22: "Nature -> Clouds and skies",
17: "Nature -> Deserts",
14: "Nature -> Details",
27: "Nature -> Fields & Meadows",
25: "Nature -> Flowers & Gardens",
28: "Nature -> Food ingredients",
18: "Nature -> Forests",
137: "Nature -> Fruits & Vegetables",
11: "Nature -> Generic vegetation",
143: "Nature -> Geologic and mineral",
16: "Nature -> Lakes and rivers",
146: "Nature -> Landscapes",
15: "Nature -> Mountains",
12: "Nature -> Plants and trees",
19: "Nature -> Sea & Ocean",
26: "Nature -> Seasons specific",
23: "Nature -> Sunsets & Sunrises",
20: "Nature -> Tropical",
171: "Nature -> Water",
24: "Nature -> Waterfalls",
142: "Objects -> Clothing & Accessories",
147: "Objects -> Electronics",
138: "Objects -> Home related",
135: "Objects -> Isolated",
151: "Objects -> Music and sound",
145: "Objects -> Other",
152: "Objects -> Retro",
156: "Objects -> Sports",
144: "Objects -> Still life",
140: "Objects -> Tools",
134: "Objects -> Toys",
123: "People -> Active",
139: "People -> Body parts",
119: "People -> Children",
175: "People -> Cosmetic & Makeup",
115: "People -> Couples",
122: "People -> Diversity",
159: "People -> Expressions",
118: "People -> Families",
117: "People -> Men",
173: "People -> Nudes",
162: "People -> Portraits",
121: "People -> Seniors",
120: "People -> Teens",
116: "People -> Women",
160: "People -> Workers",
105: "Technology -> Computers",
106: "Technology -> Connections",
129: "Technology -> Electronics",
148: "Technology -> Other",
107: "Technology -> Retro",
209: "Technology -> Science",
104: "Technology -> Telecommunications",
56: "Travel -> Africa",
58: "Travel -> America",
176: "Travel -> Antarctica",
65: "Travel -> Arts & Architecture",
57: "Travel -> Asia",
60: "Travel -> Australasian",
62: "Travel -> Cruise",
63: "Travel -> Cuisine",
67: "Travel -> Currencies",
61: "Travel -> Destination scenics",
59: "Travel -> Europe",
68: "Travel -> Flags",
64: "Travel -> Resorts",
66: "Travel -> Tropical",
201: "Web Design Graphics -> Banners",
200: "Web Design Graphics -> Buttons",
199: "Web Design Graphics -> Web Backgrounds & Textures",
198: "Web Design Graphics -> Web Icons",
"""

    gptPrompt = f""" 
These are the categories you area allowed to chose:

{categories}

I'm going to give you a description of an image, and you should answer with the number of the category that mostly fits the image. You should give an answer, even if you think no category is good.
Only anwser with an integer of the category and nothing else, here is an example:
INPUT:
Beautiful landscape filled with mountains and flowers painted in an abstract oil paint.
OUTPUT:
11

and here is the real description for you: {description}
"""
    category = getGPTResponse(gptPrompt)
    return category

def getCountry(imageDescription):
    gptPrompt = f"""
Considering a description of an image give me a two letter code of the country that would most likely be the country where the image could be, if the description gives no indication just give the code for the united stated, here is an example:
INPUT:
A group of dancers celebrating carnival in the streets, cover with glitter and colors.
OUTPUT:
BR
INPUT:
A silluete of a person in a park
OUTPUT:
US

** Don't answer anything that is not a two letter code for a country
Here is the description:
{imageDescription}
"""
    
    country = getGPTResponse(gptPrompt)
    return country