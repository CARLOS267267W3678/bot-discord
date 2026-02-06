import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"🤖 Bot online como {bot.user}")
    await bot.load_extension("cogs.fila")

bot.run("MTQ2OTA4OTg3MDAxNzMzNTUyMg.G0ADHX.F3vwkuJqJU4ZjOPb_mUK7fD_Y3oykGZcLtbKC0")