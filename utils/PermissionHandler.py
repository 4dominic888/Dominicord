import discord
from discord.ext import commands

class PermissionHandler:
    @staticmethod
    async def check_user_in_voice(ctx: commands.Context) -> bool:
        """
        Checks if the user is in a voice channel.
        :param ctx:
        :return: True if the user is in a voice channel, False otherwise
        """
        if ctx.author.voice is None or ctx.author.voice.channel is None:
            await ctx.send(embed=discord.Embed(
                title="⚠️ No estás en un canal de voz",
                description="Unete a un canal de voz pibe, o creo que yo no estoy, no se como esta eso",
                color=discord.Color.orange()
            ))
            return False
        return True

    @staticmethod
    async def check_bot_in_voice(ctx: commands.Context) -> bool:
        """
        Checks if the bot is in a voice channel.
        :param ctx:
        :return: True if the bot is in a voice channel, False otherwise
        """
        if ctx.voice_client is None or ctx.voice_client.channel is None:
            await ctx.send(embed=discord.Embed(
                title="⚠️ Yo (Dominicord) no esta en un canal de voz",
                description="Invitame a entrar AL MENOS NO?",
                color=discord.Color.orange()
            ))
            return False
        return True

    @staticmethod
    async def check_both_in_voice(ctx: commands.Context) -> bool:
        """
        Checks if the bot and the user are in some voice channel.
        :param ctx:
        :return: True if the bot is in some voice channel, False otherwise
        """
        if not await PermissionHandler.check_user_in_voice(ctx):
            return False
        if not await PermissionHandler.check_bot_in_voice(ctx):
            return False
        return True

    @staticmethod
    async def check_same_in_voice(ctx: commands.Context) -> bool:
        """
        Checks if the user is in the same voice channel with the bot.
        :param ctx:
        :return: True if the user is in the same voice channel, False otherwise
        """
        one_is_not_in_a_voice_channel: bool = ctx.voice_client is None or ctx.voice_client is None
        not_in_the_same_voice_channel: bool = ctx.author.voice.channel != ctx.voice_client.channel

        if one_is_not_in_a_voice_channel:
            await ctx.send(embed=discord.Embed(
                title="⚠️ Creo que alguno de nosotros no esta en un canal de voz?",
                description="Entra o dejame entrar",
                color=discord.Color.orange()
            ))
            return False

        if not_in_the_same_voice_channel:
            await ctx.send(embed=discord.Embed(
                title="⚠️ Creo que no estamos en el mismo canal",
                description="TENEMOS QUE ESTAR EN EL MISMO WEON",
                color=discord.Color.orange()
            ))
            return False
        return True