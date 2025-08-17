import os
import traceback
from discord.ext import commands
import config

bot = commands.Bot(
    command_prefix=f"{config.PREFIX} ",
    intents=config.intents
)

@bot.event
async def on_command_error(ctx: commands.Context, error: commands.CommandError):
    """
    Called when a command error is raised.
    :param ctx:
    :param error:
    :return:
    """
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Faltan argumentos w: {error.param.name}")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send(f"NO TENGO PERMISOS PARA ESTO: {error.missing_permissions}")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Un argumento fue invalido? QUE, ESCRE$IVE VIEN")
    else:
        await ctx.send(f"No se que paso: {type(error).__name__}")
        traceback.print_exception(type(error), error, error.__traceback__)

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