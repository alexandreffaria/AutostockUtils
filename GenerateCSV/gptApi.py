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
1: "Abstract -> Aerial",
2: "Abstract -> Backgrounds",
3: "Abstract -> Blurs",
4: "Abstract -> Colors",
5: "Abstract -> Competition",
6: "Abstract -> Craftsmanship",
7: "Abstract -> Danger",
8: "Abstract -> Exploration",
9: "Abstract -> Fun",
10: "Abstract -> Help",
11: "Abstract -> Love",
12: "Abstract -> Luxury",
13: "Abstract -> Mobile",
14: "Abstract -> Peace",
15: "Abstract -> Planetarium",
16: "Abstract -> Power",
17: "Abstract -> Purity",
18: "Abstract -> Religion",
19: "Abstract -> Seasonal & Holiday",
20: "Abstract -> Security",
21: "Abstract -> Sports",
22: "Abstract -> Stress",
23: "Abstract -> Success",
24: "Abstract -> Teamwork",
25: "Abstract -> Textures",
26: "Abstract -> Unique",
27: "Animals -> Birds",
28: "Animals -> Farm",
29: "Animals -> Insects",
30: "Animals -> Mammals",
31: "Animals -> Marine life",
32: "Animals -> Pets",
33: "Animals -> Reptiles & Amphibians",
34: "Animals -> Rodents",
35: "Animals -> Wildlife",
36: "Arts & Architecture -> Details",
37: "Arts & Architecture -> Generic architecture",
38: "Arts & Architecture -> Historic buildings",
39: "Arts & Architecture -> Home",
40: "Arts & Architecture -> Indoor",
41: "Arts & Architecture -> Landmarks",
42: "Arts & Architecture -> Modern buildings",
43: "Arts & Architecture -> Night scenes",
44: "Arts & Architecture -> Outdoor",
45: "Arts & Architecture -> Ruins & Ancient",
46: "Arts & Architecture -> Work places",
47: "Business -> Communications",
48: "Business -> Computers",
49: "Business -> Finance",
50: "Business -> Industries",
51: "Business -> Metaphors",
52: "Business -> Objects",
53: "Business -> People",
54: "Business -> Still-life",
55: "Business -> Teams",
56: "Business -> Transportation",
57: "Business -> Travel",
58: "Editorial -> Celebrities",
59: "Editorial -> Commercial",
60: "Editorial -> Events",
61: "Editorial -> Landmarks",
62: "Editorial -> People",
63: "Editorial -> Politics",
64: "Editorial -> Sports",
65: "Editorial -> Weather & Environment",
66: "Holidays -> Chinese New Year",
67: "Holidays -> Christmas",
68: "Holidays -> Cinco de Mayo",
69: "Holidays -> Diwali",
70: "Holidays -> Easter",
71: "Holidays -> Fathers Day",
72: "Holidays -> Halloween",
73: "Holidays -> Hanukkah",
74: "Holidays -> Mardi Gras",
75: "Holidays -> Mothers Day",
76: "Holidays -> New Years",
77: "Holidays -> Other",
78: "Holidays -> Ramadan",
79: "Holidays -> Thanksgiving",
80: "Holidays -> Valentines Day",
81: "IT & C -> Artificial Intelligence",
82: "IT & C -> Connectivity",
83: "IT & C -> Equipment",
84: "IT & C -> Internet",
85: "IT & C -> Networking",
86: "Illustrations & Clipart -> AI generated",
87: "Illustrations & Clipart -> 3D & Computer generated",
88: "Illustrations & Clipart -> Hand drawn & Artistic",
89: "Illustrations & Clipart -> Illustrations",
90: "Illustrations & Clipart -> Vector",
91: "Industries -> Agriculture",
92: "Industries -> Architecture",
93: "Industries -> Banking",
94: "Industries -> Cargo & Shipping",
95: "Industries -> Communications",
96: "Industries -> Computers",
97: "Industries -> Construction",
98: "Industries -> Education",
99: "Industries -> Entertainment",
100: "Industries -> Environment",
101: "Industries -> Food & Beverages",
102: "Industries -> Healthcare & Medical",
103: "Industries -> Insurance",
104: "Industries -> Legal",
105: "Industries -> Manufacturing",
106: "Industries -> Military",
107: "Industries -> Oil and gas",
108: "Industries -> Power and energy",
109: "Industries -> Sports",
110: "Industries -> Transportation",
111: "Industries -> Travel",
112: "Nature -> Clouds and skies",
113: "Nature -> Deserts",
114: "Nature -> Details",
115: "Nature -> Fields & Meadows",
116: "Nature -> Flowers & Gardens",
117: "Nature -> Food ingredients",
118: "Nature -> Forests",
119: "Nature -> Fruits & Vegetables",
120: "Nature -> Generic vegetation",
121: "Nature -> Geologic and mineral",
122: "Nature -> Lakes and rivers",
123: "Nature -> Landscapes",
124: "Nature -> Mountains",
125: "Nature -> Plants and trees",
126: "Nature -> Sea & Ocean",
127: "Nature -> Seasons specific",
128: "Nature -> Sunsets & Sunrises",
129: "Nature -> Tropical",
130: "Nature -> Water",
131: "Nature -> Waterfalls",
132: "Objects -> Clothing & Accessories",
133: "Objects -> Electronics",
134: "Objects -> Home related",
135: "Objects -> Isolated",
136: "Objects -> Music and sound",
137: "Objects -> Other",
138: "Objects -> Retro",
139: "Objects -> Sports",
140: "Objects -> Still life",
141: "Objects -> Tools",
142: "Objects -> Toys",
143: "People -> Active",
144: "People -> Body parts",
145: "People -> Children",
146: "People -> Cosmetic & Makeup",
147: "People -> Couples",
148: "People -> Diversity",
149: "People -> Expressions",
150: "People -> Families",
151: "People -> Men",
152: "People -> Nudes",
153: "People -> Portraits",
154: "People -> Seniors",
155: "People -> Teens",
156: "People -> Women",
157: "People -> Workers",
158: "Technology -> Computers",
159: "Technology -> Connections",
160: "Technology -> Electronics",
161: "Technology -> Other",
162: "Technology -> Retro",
163: "Technology -> Science",
164: "Technology -> Telecommunications",
165: "Travel -> Africa",
166: "Travel -> America",
167: "Travel -> Antarctica",
168: "Travel -> Arts & Architecture",
169: "Travel -> Asia",
170: "Travel -> Australasian",
171: "Travel -> Cruise",
172: "Travel -> Cuisine",
173: "Travel -> Currencies",
174: "Travel -> Destination scenics",
175: "Travel -> Europe",
176: "Travel -> Flags",
177: "Travel -> Resorts",
178: "Travel -> Tropical",
179: "Web Design Graphics -> Banners",
180: "Web Design Graphics -> Buttons",
181: "Web Design Graphics -> Web Backgrounds & Textures",
182: "Web Design Graphics -> Web Icons"
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