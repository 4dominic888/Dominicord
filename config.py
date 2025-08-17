import os
import discord
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True
intents.reactions = True

load_dotenv()

TOKEN = str(os.getenv('DISCORD_TOKEN'))
PREFIX = str(os.getenv('PREFIX'))