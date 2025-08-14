from discord.ext import commands

class Ping(commands.Cog):
    def __init__(self, bot): self.bot = bot

    @commands.hybrid_command(name="ping", description="Muestra la latencia del bot")
    async def ping(self, ctx: commands.Context):
        latency = round(self.bot.latency * 1000)
        await ctx.send(f"Pong! {latency}ms")


async def setup(bot):
    await bot.add_cog(Ping(bot))