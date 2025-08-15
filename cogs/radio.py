import os
import random
from typing import Optional, Literal

import discord
from discord.ext import commands
from discord import FFmpegPCMAudio, app_commands
from discord.ext.commands import hybrid_command

PLAYLIST_FOLDER = "./shared/music"

class Radio(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = {} # * {guild_id: [lista de canciones]}

    @staticmethod
    async def _is_there_in_a_voice_channel(ctx: commands.Context) -> bool:
        if not (ctx.author and getattr(ctx.author, "voice", None)):
            await ctx.send(embed=discord.Embed(
                title="⚠️ No estás en un canal de voz",
                description="Unete a un canal de voz pibe, si no como xddd",
                color=discord.Color.orange()
            ))
            return False
        return True

    def get_queue(self, guild_id):
        if guild_id not in self.queue:
            self.queue[guild_id] = []
        return self.queue[guild_id]

    async def play_next(self, ctx: commands.Context):
        in_a_voice_channel = await self._is_there_in_a_voice_channel(ctx)
        if not in_a_voice_channel: return

        queue = self.get_queue(ctx.guild.id)

        if not queue:
            await ctx.send(embed=discord.Embed(
                title="🎵 Cola vacía",
                description="No hay más rolas en la cola, PONGAN MÁsss",
                color=discord.Color.red()
            ))
            return

        source = queue.pop(0)
        vc: Optional[discord.VoiceClient] = ctx.voice_client

        if vc is None:
            channel: discord.VoiceChannel = ctx.author.voice.channel
            vc = await channel.connect()
        else:
            vc.play(
                FFmpegPCMAudio(source),
                after= lambda e: self.bot.loop.create_task(self.play_next(ctx))
            )

            await ctx.send(embed=discord.Embed(
                title="▶ Reproduciendo",
                description=os.path.basename(source),
                color=discord.Color.green()
            ))


    @commands.hybrid_command(name="playplaylist", description="Reproduce una playlist en orden alfabetico o aleatorio")
    async def play_playlist(self, ctx: commands.Context, playlist_name: str, mode: Literal["normal", "random"]):
        in_a_voice_channel = await self._is_there_in_a_voice_channel(ctx)
        if not in_a_voice_channel: return

        playlist_foder = os.path.join(PLAYLIST_FOLDER, playlist_name)
        if not os.path.isdir(playlist_foder):
            await ctx.send(embed=discord.Embed(
                title="❌ NOOOOO",
                description="Esa playlist no es valida, ESCRIBA BIEN MIJO",
                color=discord.Color.red()
            ))
            return

        songs = [
            os.path.join(playlist_foder, f) for f in
                os.listdir(playlist_foder) if f.endswith(".mp3")
        ]

        if not songs:
            await ctx.send(embed=discord.Embed(
                title="❌ NOOOOO",
                description="Esa playlist no tiene canciones :((((((",
                color=discord.Color.red()
            ))
            return

        # * Mode control
        if mode == "random": random.shuffle(songs)
        else: songs.sort()

        queue = self.get_queue(ctx.guild.id)
        queue.extend(songs)

        if ctx.author.voice:
            channel: discord.VoiceChannel = ctx.author.voice.channel
            vc: Optional[discord.VoiceClient] = ctx.voice_client
            if vc is None:
                await channel.connect()

            if not vc.is_playing():
                await self.play_next(ctx)

    @commands.hybrid_command(name="pause", description="Pausa cualquier música reproduciendose")
    async def pause(self, ctx: commands.Context):
        in_a_voice_channel = await self._is_there_in_a_voice_channel(ctx)
        if not in_a_voice_channel: return

        vc: Optional[discord.VoiceClient] = ctx.voice_client
        if vc and vc.is_playing():
            vc.pause()
            await ctx.send(embed=discord.Embed(
                title="⏸ Pausado",
                description="ALGUIEN ME PARO, QUIEN",
                color = discord.Color.orange()
            ))


    @commands.hybrid_command(name="skip", description="Salta a la siguiente canción de la cola")
    async def skip(self, ctx: commands.Context):
        in_a_voice_channel = await self._is_there_in_a_voice_channel(ctx)
        if not in_a_voice_channel: return

        vc: Optional[discord.VoiceClient] = ctx.voice_client
        if vc and vc.is_playing():
            vc.stop()
            await ctx.message.add_reaction("⏭️")
        else:
            await ctx.send(embed=discord.Embed(
                title="❌ Error",
                description="QUE QUIERES QUE SALTEE, NO TENGO NADA WEON",
                color=discord.Color.red())
            )

    @commands.hybrid_command(name="listplaylists", description="Lista todas las playlists disponibles")
    async def listplaylists(self, ctx: commands.Context):
        playlists = [d for d in os.listdir(PLAYLIST_FOLDER) if os.path.isdir(os.path.join(PLAYLIST_FOLDER, d))]
        embed = discord.Embed(title="📂 Playlists disponibles", color=discord.Color.blue())
        for pl in playlists:
            embed.add_field(name=pl, value=f"Carpeta con {len(os.listdir(os.path.join(PLAYLIST_FOLDER, pl)))} rolas", inline=False)

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Radio(bot))