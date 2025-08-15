import os
import random
import traceback
from typing import Optional, Literal, NamedTuple

import discord
from discord.ext import commands
from discord import FFmpegPCMAudio

PLAYLIST_FOLDER = "./shared/music"

class QueueElement(NamedTuple):
    user_id: str
    user_name: str
    music_requested: str
    path_music: str

class Radio(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue: list[QueueElement] = [] # * {user_id: music}
        self.current: Optional[QueueElement] = None

    # region utils
    @staticmethod
    async def _is_there_in_a_voice_channel(ctx: commands.Context) -> bool:
        """
        Checks if the user is in a voice channel and the bot also
        :param ctx:
        :return: True if the user is in a voice channel, False otherwise
        """
        if not (ctx.author and getattr(ctx.author, "voice", None)):
            await ctx.send(embed=discord.Embed(
                title="⚠️ No estás en un canal de voz",
                description="Unete a un canal de voz pibe, o creo que yo no estoy, no se como esta eso",
                color=discord.Color.orange()
            ))
            return False
        return True

    def get_queue(self) -> list[QueueElement]:
        """
        Gets a queue from the queue xd
        :return: The queue
        """
        return self.queue

    def set_queue(self, queue: list[QueueElement]):
        self.queue = queue

    async def set_current(self, queue_element: Optional[QueueElement], ctx: commands.Context):
        self.current = queue_element
        if queue_element is not None:
            await ctx.send(
                embed=discord.Embed(
                    title="Reproduciendo",
                    description=queue_element.music_requested,
                    color=discord.Color.dark_gray()
                ).set_footer(text=f"Pedido por {queue_element.user_name}")
            )

    def get_current(self) -> QueueElement | None:
        return self.current

    async def play_next(self, ctx: commands.Context):
        """
        Plays the next song in the queue
        :param ctx:
        :return:
        """
        in_a_voice_channel = await self._is_there_in_a_voice_channel(ctx)
        if not in_a_voice_channel: return

        queue = self.get_queue()

        if not queue:
            await ctx.send(embed=discord.Embed(
                title="🎵 Cola vacía",
                description="No hay más rolas en la cola, PONGAN MÁsss",
                color=discord.Color.red()
            ))
            return

        source = queue.pop()
        await self.set_current(source, ctx)
        vc: Optional[discord.VoiceClient] = ctx.voice_client

        def after_check(e):
            self.bot.loop.create_task(self.play_next(ctx))

        if vc is None:
            channel: discord.VoiceChannel = ctx.author.voice.channel
            await channel.connect()
        else:
            vc.play(
                FFmpegPCMAudio(source.path_music),
                after= after_check
            )

    @staticmethod
    async def _playlist_exists(ctx: commands.Context, playlist_name: str) -> bool:
        """
        Checks if the playlist exists
        :param ctx:
        :param playlist_name: The name of the playlist
        :return: True if the playlist exists, False otherwise
        """
        if not os.path.isdir(playlist_name):
            await ctx.send(embed=discord.Embed(
                title="❌ NOOOOO",
                description="Esa playlist no es valida, ESCRIBA BIEN MIJO",
                color=discord.Color.red()
            ))
            return False
        return True

    # endregion
    @commands.hybrid_group(name="play")
    async def play(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            await ctx.send("Usa un subcomando válido")

    @play.command(name="playlist", description="Agrega una playlist en orden alfabetico o aleatorio a la cola")
    async def play_playlist(self, ctx: commands.Context, playlist_name: str, mode: Literal["normal", "random"]):
        in_a_voice_channel = await self._is_there_in_a_voice_channel(ctx)
        if not in_a_voice_channel: return

        playlist_folder_name = os.path.join(PLAYLIST_FOLDER, playlist_name)

        playlist_exists = await self._playlist_exists(ctx, playlist_folder_name)
        if not playlist_exists: return

        songs = [
            os.path.join(playlist_folder_name, f) for f in
                os.listdir(playlist_folder_name) if f.endswith(".mp3")
        ]
        songs_length = len(songs)

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

        queue = self.get_queue()

        # * Add elementos to main queue
        queue.extend([QueueElement(
            user_id = str(ctx.author.id),
            music_requested = os.path.basename(qe),
            path_music = qe,
            user_name=ctx.author.name
        ) for qe in songs])


        if ctx.author.voice:
            vc: Optional[discord.VoiceClient] = ctx.voice_client
            channel: discord.VoiceChannel = ctx.author.voice.channel
            await ctx.send(embed=discord.Embed(
                title=f"Agregado {songs_length} {"rola" if songs_length > 1 else "rolas"}",
                description=f"La playlist {playlist_name} de manera {mode}",
            ).set_footer(text=f"Pedido por {ctx.author.name}"))
            if vc is None:
                await channel.connect()
                vc: Optional[discord.VoiceClient] = ctx.voice_client

            if not vc.is_playing(): await self.play_next(ctx)

    @play.command(name="music", description="Agrega una canción de una playlist a la cola")
    async def play_music(self, ctx: commands.Context, playlist_name: str, music_requested: str):
        in_a_voice_channel = await self._is_there_in_a_voice_channel(ctx)
        if not in_a_voice_channel: return

        playlist_folder_name = os.path.join(PLAYLIST_FOLDER, playlist_name)

        playlist_exists = await self._playlist_exists(ctx, playlist_folder_name)
        if not playlist_exists: return

        if not os.path.exists(os.path.join(playlist_folder_name, music_requested)):
            await ctx.send("Rola no encontrada...")
            return

        queue = self.get_queue()
        queue.append(QueueElement(
            user_id = str(ctx.author.id),
            music_requested = music_requested,
            path_music = os.path.join(playlist_folder_name, music_requested),
            user_name=ctx.author.name
        ))

        if ctx.author.voice:
            channel: discord.VoiceChannel = ctx.author.voice.channel
            vc: Optional[discord.VoiceClient] = ctx.voice_client
            await ctx.send(embed=discord.Embed(
                title="Agregado",
                description=f"La rola {music_requested}",
            ).set_footer(text=f"Pedido por {ctx.author.name}"))
            if vc is None:
                await channel.connect()
                vc: Optional[discord.VoiceClient] = ctx.voice_client

            if not vc.is_playing(): await self.play_next(ctx)

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
            queue = self.get_queue()
            await self.set_current(queue.pop(1), ctx)
            await ctx.message.add_reaction("⏭️")
        else:
            await ctx.send(embed=discord.Embed(
                title="❌ Error",
                description="QUE QUIERES QUE SALTEE, NO TENGO NADA WEON",
                color=discord.Color.red())
            )

    @commands.hybrid_group(name="list")
    async def list(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            await ctx.send("Usa un subcomando válido")

    @list.command(name="playlists", description="Lista todas las playlists disponibles")
    async def list_playlists(self, ctx: commands.Context):
        playlists = [d for d in os.listdir(PLAYLIST_FOLDER) if os.path.isdir(os.path.join(PLAYLIST_FOLDER, d))]
        embed = discord.Embed(
            title="📂 Playlists disponibles",
            color=discord.Color.blue()
        )
        for pl in playlists:
            embed.add_field(name=pl, value=f"Carpeta con {len(os.listdir(os.path.join(PLAYLIST_FOLDER, pl)))} rolas", inline=False)

        await ctx.send(embed=embed)

    @list.command(name="music", description="Lista todas las canciones de una playlist")
    async def list_music(self, ctx: commands.Context, playlist_folder_name: str, music_name: str = None, page: int = 1):
        songs = []
        page_size = 10

        # * Get playlist to find, get all playlist instead
        playlist_folder_path = os.path.join(PLAYLIST_FOLDER, playlist_folder_name)

        # * Find all the songs first...
        for f in os.listdir(playlist_folder_path):
            if f.endswith(".mp3"): songs.append(os.path.basename(f))

        # * Filter songs by name
        if music_name:
            all_titles = [f for f in songs]
            matches = [music for music in all_titles if  music_name.lower() in music.lower()]
            songs = [f for f in songs if f in matches]

        if not songs:
            await ctx.send(embed=discord.Embed(
                title="No se encontro nada",
                description="Intenta buscar de otra manera",
                color=discord.Color.red()
            ))
            return

        # * Pagination system
        # * Variables
        total_pages = (len(songs) + page_size) // page_size
        page = max(1, min(page, total_pages))
        start = (page - 1) * page_size
        end = start + page_size
        songs_page = songs[start:end]

        # * Build Message
        embed = discord.Embed(
            title=f"🎶 Resultados de búsqueda {music_name or "general"} en 📂 {playlist_folder_name}",
            color=discord.Color.green()
        ).set_footer(text=f"(Página {page}/{total_pages})")

        for song in songs_page:
            embed.add_field(name=f"♪ {song}", value="", inline=False)

        message = await ctx.send(embed=embed)

        # * Adding reaction page system
        if total_pages > 1:
            def check(c_reaction, c_user): return (
                c_user == ctx.author and str(c_reaction.emoji) in ["⬅️", "➡️"]
                and c_reaction.message.id == message.id
            )

            current_page = page

            while True:
                try:
                    await message.clear_reactions()

                    if current_page == 1: await message.add_reaction("➡️")
                    elif current_page == total_pages: await message.add_reaction("⬅️")
                    else:
                        await message.add_reaction("⬅️")
                        await message.add_reaction("➡️")

                    reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
                    if str(reaction.emoji) == "➡️" and current_page < total_pages:
                        current_page += 1
                    elif str(reaction.emoji) == "⬅️" and current_page > 1:
                        current_page -= 1
                    else:
                        await message.remove_reaction(reaction, user)
                        continue

                    start = (current_page - 1) * page_size
                    end = start + page_size
                    songs_page = songs[start:end]

                    embed = discord.Embed(
                        title=f"🎶 Resultados de búsqueda {music_name or "general"} en 📂 {playlist_folder_name}",
                        color=discord.Color.green()
                    ).set_footer(text=f"(Página {current_page}/{total_pages})")

                    for song in songs_page:
                        embed.add_field(name=f"♪ {song}", value="", inline=False)

                    await message.edit(embed=embed)
                    await message.remove_reaction(reaction, user)
                except Exception as e:
                    await message.clear_reactions()
                    print(e)
                    traceback.print_exception(type(e), e, e.__traceback__)
                    break

    @list.command(name="queue", description="Lista las musicas que estan en cola, (no se considera la que se está reproduciendo)")
    async def list_queue(self, ctx: commands.Context, page: int = 1):
        queue = self.get_queue()

        page_size = 10
        total_pages = (len(queue) + page_size) // page_size
        page = max(1, min(page, total_pages))
        start = (page - 1) * page_size
        end = start + page_size
        queue_page = queue[start:end]

        if not queue_page:
            await ctx.send(embed=discord.Embed(
                title="No hay rolas en la cola",
                description="Que intentai buscar??",
                color=discord.Color.red()
            ))
            return

        embed = discord.Embed(
            title="Lista de rolas en la cola",
            color=discord.Color.green(),
        ).set_footer(text=f"(Página {page}/{total_pages})")

        for qe in queue_page:
            embed.add_field(name=qe.user_name, value=qe.music_requested, inline=False)

        message = await ctx.send(embed=embed)

        if total_pages > 1:
            def check(c_reaction, c_user): return (
                c_user == ctx.author and str(c_reaction.emoji) in ["⬅️", "➡️"]
                and c_reaction.message.id == message.id
            )

            current_page = page

            while True:
                try:
                    await message.clear_reactions()

                    if current_page == 1: await message.add_reaction("➡️")
                    elif current_page == total_pages: await message.add_reaction("⬅️")
                    else:
                        await message.add_reaction("⬅️")
                        await message.add_reaction("➡️")

                    reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
                    if str(reaction.emoji) == "➡️" and current_page < total_pages:
                        current_page += 1
                    elif str(reaction.emoji) == "⬅️" and current_page > 1:
                        current_page -= 1
                    else:
                        await message.remove_reaction(reaction, user)
                        continue

                    start = (current_page - 1) * page_size
                    end = start + page_size
                    queue_page = queue[start:end]

                    embed = discord.Embed(
                        title="Lista de rolas en la cola",
                        color=discord.Color.green(),
                    ).set_footer(text=f"(Página {current_page}/{total_pages})")

                    for qe in queue_page:
                        embed.add_field(name=qe.user_name, value=qe.music_requested, inline=False)

                    await message.edit(embed=embed)
                    await message.remove_reaction(reaction, user)
                except Exception as e:
                    await message.clear_reactions()
                    print(e)
                    traceback.print_exception(type(e), e, e.__traceback__)
                    break

    @commands.hybrid_command(name="leave", description="Sacar a dominicord del canal de voz actual")
    async def leave(self, ctx: commands.Context):
        in_a_voice_channel = await self._is_there_in_a_voice_channel(ctx)
        if not in_a_voice_channel: return

        vc: Optional[discord.VoiceClient] = ctx.voice_client
        if not vc:
            await ctx.send("No ando en ningun canal de voz... COMO ME PIENSAS SACAR, MALO")
            return

        self.set_queue([])
        await vc.disconnect()
        await self.set_current(None, ctx)

        await ctx.send(embed=discord.Embed(
            title="✅ Desconectado",
            description="HASTA LA PROXIMA... pei uf PUA PUA PUAA fafafafafa sadmkasnfjkasnf PUAPUA",
            color=discord.Color.green()
        ))

    @commands.hybrid_command(name="current", description="Ver la canción reproduciendose ahora mismo")
    async def current(self, ctx: commands.Context):
        current = self.get_current()
        if self.get_current() is not None:
            await ctx.send(
                embed=discord.Embed(
                    title="Reproduciendo",
                    description=current.music_requested,
                    color=discord.Color.dark_gray()
                ).set_footer(text=f"Pedido por {current.user_name}")
            )
        else:
            await ctx.send(
                embed=discord.Embed(
                    title="Ninguna rola escuchandose",
                    color=discord.Color.red()
                )
            )


async def setup(bot):
    await bot.add_cog(Radio(bot))