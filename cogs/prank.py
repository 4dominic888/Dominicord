import discord
from discord.ext import commands

class Prank(commands.Cog):
    def __init__(self, bot): self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return

        if message.content.lower().strip().endswith("que"):
            await message.reply('SO.')

        await self.bot.process_commands(message)

async def setup(bot):
    await bot.add_cog(Prank(bot))