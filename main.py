import os
from discord.ext import commands
import config

bot = commands.Bot(
    command_prefix=config.PREFIX,
    intents=config.intents
)

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user} (ID: {bot.user.id})")
    try:
        synced = await bot.tree.sync()
        print(f"{len(synced)} comandos slash/híbridos sincronizados")
    except Exception as e:
        print(f"Error al sincronizar comandos: {e}")


async def load_cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")

async def main():
    async with bot:
        await load_cogs()
        await bot.start(config.TOKEN)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())