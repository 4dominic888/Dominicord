from typing import Optional

import discord
from discord.ext import commands

from utils.permission_handler import PermissionHandler


class VoiceManager:

    @staticmethod
    async def connect_to_user_channel(ctx: commands.Context) -> Optional[discord.VoiceClient]:
        """
        Connect the bot to a user channel.
        :param ctx:
        :return: A VoiceClient object with the correct context
        """
        error_embed = discord.Embed(
            title="⚠️ No me puedo unir al canal de voz... que",
            description="No se que wea este pasando pero SOLUCIONALO YA",
            color=discord.Color.orange()
        )

        user_in_voice_channel = await PermissionHandler.check_user_in_voice(ctx)
        if not user_in_voice_channel: return None

        channel = ctx.author.voice.channel

        bot_in_voice_channel = await PermissionHandler.check_bot_in_voice(ctx, omit_warn=True)
        if bot_in_voice_channel:
            we_are_in_same_channel = await PermissionHandler.check_same_in_voice(ctx)
            if we_are_in_same_channel:
                return ctx.voice_client
            try:
                vc: Optional[discord.VoiceClient] = ctx.voice_client
                await vc.move_to(channel)
                return vc
            except discord.Forbidden:
                await ctx.send(embed=error_embed)
                return None

        else:
            try:
                return await channel.connect()
            except discord.Forbidden:
                await ctx.send(embed=error_embed)

    @staticmethod
    async def leave_voice_channel(ctx: commands.Context, force: bool = False) -> bool:
        """
        Leaves the bot from the voice channel where you are
        :param ctx:
        :param force: If the disconnection should be forced or not
        :return: True if the operation was successful, False otherwise
        """
        same_in_voice_channel = await PermissionHandler.check_same_in_voice(ctx)
        if not same_in_voice_channel:
            await ctx.send(embed=discord.Embed(
                title="⚠️ Solo puedes sacarme si es que estas en el mismo canal de voz",
                description="Piensa pe",
                color=discord.Color.orange()
            ))
            return False

        await ctx.voice_client.disconnect(force=force)
        await ctx.send(embed=discord.Embed(
            title="✅ Desconectado",
            description="HASTA LA PROXIMA... pei uf PUA PUA PUAA fafafafafa sadmkasnfjkasnf PUAPUA",
            color=discord.Color.green()
        ))
        return True