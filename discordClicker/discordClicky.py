import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Get the bot token from the environment variables
TOKEN = os.getenv('BOT_TOKEN')

# Define the intents
intents = discord.Intents.all()

# Create a bot instance with commands extension
client = commands.Bot(command_prefix='!', intents=intents)

# File to store unique content
file_path = 'unique_content.txt'

# Create the file if it doesn't exist
if not os.path.exists(file_path):
    with open(file_path, 'w') as file:
        pass

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    # Check if the message is from the desired channel
    if message.guild and message.channel.name == 'midjourney':
        # Extract content from the message
        content_start = message.content.find('Midjourney Bot:') + len('Midjourney Bot:')
        content_end = message.content.find('full screen, sharp focus')
        if content_start != -1 and content_end != -1:
            content = message.content[content_start:content_end].strip()

            # Print for debugging
            print(f'Extracted Content: {content}')

            # Check if content is not already in the file
            if not is_content_present(content):
                # Print and save the content
                print(f'Message received in #{message.channel.name} by {message.author.name}: {content}')
                save_content(content)
            else:
                print('Content is already present in the file.')

# Function to check if content is already present in the file
def is_content_present(content):
    with open(file_path, 'r') as file:
        file_content = file.read()
        print(f'File Content: {file_content}')
        return content in file_content

# Function to save content to the file
def save_content(content):
    with open(file_path, 'a') as file:
        file.write(content + '\n')
        print('Content saved to the file.')

# Run the bot with your token
client.run(TOKEN)
