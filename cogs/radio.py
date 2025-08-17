import datetime
import os
import random
import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
from utils.pagination_manager import PaginationManager
from utils.voice_manager import VoiceManager
from utils.permission_handler import PermissionHandler
from typing import Optional, Literal, NamedTuple

PLAYLIST_FOLDER = "./shared/music"

class QueueElement(NamedTuple):
    user_id: str
    user_name: str
    music_requested: str
    path_music: str
    timestamp: datetime.date

class Radio(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue: list[QueueElement] = [] # * {user_id: music}
        self.current: Optional[QueueElement] = None

    # region utils

    def get_queue(self) -> list[QueueElement]:
        """
        Gets a queue from the queue xd
        :return: The queue
        """
        return self.queue

    def set_queue(self, queue: list[QueueElement]): self.queue = queue

    def get_current(self) -> Optional[QueueElement]: return self.current

    async def set_current(self, queue_element: Optional[QueueElement], ctx: commands.Context, omit_message: bool = False):
        """
        Sets the current queue to the queue_element and give a message
        :param queue_element: The elemento to put
        :param omit_message: omit the message about what is playing about
        :param ctx:
        :return:
        """
        self.current = queue_element
        if queue_element is not None:
            if not omit_message:
                await ctx.send(
                    embed=discord.Embed(
                        title="Reproduciendo",
                        description=queue_element.music_requested,
                        color=discord.Color.dark_gray()
                    ).set_footer(text=f"Pedido por {queue_element.user_name}")
                )

    # * Play the music
    async def play_next(self, ctx: commands.Context, voice_client: discord.VoiceClient):
        """
        Plays the next song in the queue, until the queue is empty.

        Try to call it once and when the queue doesnt have elements
        :param ctx:
        :param voice_client: VoiceClient valid to use and parsed previously
        :return:
        """

        queue = self.get_queue()

        if not queue:
            await ctx.send(embed=discord.Embed(
                title="🎵 Cola vacía",
                description="No hay más rolas en la cola, PONGAN MÁsss",
                color=discord.Color.red()
            ))
            return

        source = queue.pop(0)
        await self.set_current(source, ctx)

        voice_client.play(
            FFmpegPCMAudio(source.path_music),
            after= lambda _: self.bot.loop.create_task(self.play_next(ctx, voice_client))
        )

    @staticmethod
    async def _playlist_exists(ctx: commands.Context, playlist_name: str) -> bool:
        """
        Checks if the playlist exists
        :param ctx:
        :param playlist_name: The name of the playlist
        :return: True if the playlist exists, False otherwise
        """
        if not os.path.isdir(os.path.join(PLAYLIST_FOLDER, playlist_name)):
            await ctx.send(embed=discord.Embed(
                title="❌ NOOOOO",
                description="Esa playlist no es valida, ESCRIBA BIEN MIJO",
                color=discord.Color.red()
            ))
            return False
        return True

    # endregion

    @commands.hybrid_command(name="connect", description="Conectas a dominicord")
    async def connect(self, ctx: commands.Context):
        voice_client: Optional[discord.VoiceClient] = await VoiceManager.connect_to_user_channel(ctx)
        if voice_client:
            await ctx.send(f"Me he conectado al canal {voice_client.channel.name}... ahora que")

    @commands.hybrid_command(name="leave", description="Sacar a dominicord del canal de voz actual")
    async def leave(self, ctx: commands.Context):
        leave_operation_successful = await VoiceManager.leave_voice_channel(ctx)
        if leave_operation_successful:
            self.set_queue([]) # * Empty the queue
            await self.set_current(None, ctx, omit_message=True) # * Clean current value as None


    @commands.hybrid_group(name="play")
    async def play(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            await ctx.send("Usa un subcomando válido")

    @play.command(name="playlist", description="Agrega una playlist en orden alfabetico o aleatorio a la cola")
    async def play_playlist(self, ctx: commands.Context, playlist_name: str, mode: Literal["normal", "random"]):
        # * Try to connect to the voice channel
        voice_client: Optional[discord.VoiceClient] = await VoiceManager.connect_to_user_channel(ctx)
        if not voice_client: return

        # * Validate if the playlist name exists
        if not await self._playlist_exists(ctx, playlist_name): return

        # * Get all the songs from that playlist
        playlist_folder_path = os.path.join(PLAYLIST_FOLDER, playlist_name)
        songs = [
            os.path.join(playlist_folder_path, f) for f in
                os.listdir(playlist_folder_path) if f.endswith(".mp3")
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

        # * Add list of musics from a playlist to the main queue
        queue = self.get_queue()
        queue.extend([QueueElement(
            user_id = str(ctx.author.id),
            music_requested = os.path.splitext(os.path.basename(qe))[0],
            path_music = qe,
            user_name=ctx.author.name,
            timestamp=datetime.date.today()
        ) for qe in songs])

        await ctx.send(embed=discord.Embed(
            title=f"Agregado {songs_length} {"rolas" if songs_length > 1 else "rola"}",
            description=f"La playlist {playlist_name} de manera {mode}",
        ).set_author(name=f"Pedido por {ctx.author.name}", icon_url=ctx.author.avatar.url))

        if not voice_client.is_playing(): await self.play_next(ctx, voice_client)

    @play.command(name="music", description="Agrega una canción de una playlist a la cola")
    async def play_music(self, ctx: commands.Context, playlist_name: str, music_requested: str):
        # * Try to connect to the voice channel
        voice_client: Optional[discord.VoiceClient] = await VoiceManager.connect_to_user_channel(ctx)
        if not voice_client: return

        # * Validate if the playlist name exists
        if not await self._playlist_exists(ctx, playlist_name): return

        playlist_folder_path = os.path.join(PLAYLIST_FOLDER, playlist_name)
        music_found = os.path.exists(os.path.join(playlist_folder_path, music_requested))
        if not music_found:
            await ctx.send("Rola no encontrada...")
            return

        queue = self.get_queue()
        queue.append(
            QueueElement(
                user_id = str(ctx.author.id),
                music_requested = os.path.splitext(music_requested)[0],
                path_music = os.path.join(playlist_folder_path, music_requested),
                user_name=ctx.author.name,
                timestamp=datetime.date.today()
            )
        )

        await ctx.send(embed=discord.Embed(
            title="Agregado",
            description=f"La rola {music_requested}",
        ).set_author(name=f"Pedido por {ctx.author.name}", icon_url=ctx.author.avatar.url))

        if not voice_client.is_playing(): await self.play_next(ctx, voice_client)

    @commands.hybrid_command(name="pause", description="Pausa cualquier música reproduciendose")
    async def pause(self, ctx: commands.Context):
        in_the_same_voice_channel = await PermissionHandler.check_same_in_voice(ctx)
        if not in_the_same_voice_channel: return

        voice_client: Optional[discord.VoiceClient] = ctx.voice_client
        if voice_client and voice_client.is_playing():
            voice_client.pause()
            await ctx.send(embed=discord.Embed(
                title="⏸ Pausado",
                description="ALGUIEN ME PARO, QUIEN",
                color = discord.Color.orange()
            ))

    @commands.hybrid_command(name="resume", description="Continua cualquier música recientemente pausada")
    async def resume(self, ctx: commands.Context):
        in_the_same_voice_channel = await PermissionHandler.check_same_in_voice(ctx)
        if not in_the_same_voice_channel: return

        voice_client: Optional[discord.VoiceClient] = ctx.voice_client
        if voice_client and voice_client.is_paused():
            voice_client.resume()
            await ctx.send(embed=discord.Embed(
                title="YEY",
                description="GRACIAS POR REANUDAR DOMINICORD.FM",
                color = discord.Color.green()
            ))

    @commands.hybrid_command(name="skip", description="Salta a la siguiente canción de la cola")
    async def skip(self, ctx: commands.Context):
        in_the_same_voice_channel = await PermissionHandler.check_same_in_voice(ctx)
        if not in_the_same_voice_channel: return

        voice_client: Optional[discord.VoiceClient] = ctx.voice_client
        if voice_client and voice_client.is_playing():
            voice_client.stop()
            await ctx.message.add_reaction("⏭️")
        else:
            await ctx.send(embed=discord.Embed(
                title="❌ Error",
                description="QUE QUIERES QUE SALTEE, NO TENGO NADA WEON",
                color=discord.Color.red())
            )


    @commands.hybrid_group(name="find")
    async def find(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            await ctx.send("Usa un subcomando válido")

    @find.command(name="playlists", description="Lista todas las playlists disponibles")
    async def list_playlists(self, ctx: commands.Context):
        playlists = [d for d in os.listdir(PLAYLIST_FOLDER) if os.path.isdir(os.path.join(PLAYLIST_FOLDER, d))]
        embed = discord.Embed(
            title="📂 Playlists disponibles",
            color=discord.Color.blue()
        )

        for pl in playlists:
            playlist_music_length = len(os.listdir(os.path.join(PLAYLIST_FOLDER, pl)))
            embed.add_field(name=pl, value=f"Carpeta con {playlist_music_length} rolas", inline=False)

        await ctx.send(embed=embed)

    @find.command(name="music", description="Lista todas las canciones de una playlist")
    async def list_music(self, ctx: commands.Context, playlist_name: str, music_name: str = None, page: int = 1):
        if not await self._playlist_exists(ctx, playlist_name): return

        # * Get playlist to find
        playlist_folder_path = os.path.join(PLAYLIST_FOLDER, playlist_name)
        songs: list[str] = []

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

        await PaginationManager.builder(
            ctx=ctx,
            title=f"🎶 Resultados de búsqueda {f"\"{music_name}\"" or "general"} en 📂 {playlist_name}",
            data=songs,
            for_each_field_name=lambda s: f"♪ {s}",
            for_each_field_value=lambda _: "",
            page=page
        )

    @find.command(name="queue", description="Lista las musicas que estan en cola, (no se considera la que se está reproduciendo)")
    async def list_queue(self, ctx: commands.Context, page: int = 1):
        queue = self.get_queue()

        if not queue:
            await ctx.send(embed=discord.Embed(
                title="No hay rolas en la cola",
                description="Que intentai buscar??",
                color=discord.Color.red()
            ))
            return

        await PaginationManager.builder(
            ctx=ctx,
            title="Lista de rolas en la cola",
            data=queue,
            for_each_field_name=lambda queue_el: f"{queue.index(queue_el) or "NEXT"} | {queue_el.music_requested}",
            for_each_field_value=lambda queue_el: queue_el.user_name,
            page=page
        )


    @commands.hybrid_command(name="current", description="Ver la canción reproduciendose ahora mismo")
    async def current(self, ctx: commands.Context):
        in_the_same_voice_channel = await PermissionHandler.check_same_in_voice(ctx)
        if not in_the_same_voice_channel: return

        current = self.get_current()
        if current is not None:
            await ctx.send(
                embed=discord.Embed(
                    title="Reproduciendo",
                    description=current.music_requested,
                    color=discord.Color.dark_gray()
                ).set_author(name=f"Pedido por {ctx.author.name}", icon_url=ctx.author.avatar.url)
            )
        else:
            await ctx.send(
                embed=discord.Embed(
                    title="Ninguna rola escuchandose",
                    color=discord.Color.red()
                )
            )

    @commands.hybrid_command(name="move_first", description="Logra que un elemento de la cola se posicione primero a escuchar")
    async def move_first(self, ctx: commands.Context, index: int):
        in_the_same_voice_channel = await PermissionHandler.check_same_in_voice(ctx)
        if not in_the_same_voice_channel: return

        queue = self.get_queue()
        if 0 <= index < len(queue):
            element = queue.pop(index)
            queue.insert(0, element)
            await ctx.send(embed=discord.Embed(
                title=f"{element.music_requested} puesto primero a escuchar... que tramposo que sos",
                description=f"La rola se escuchará después de\n\n {self.get_current().music_requested}",
            ).set_author(name=f"Pedido por {ctx.author.name}", icon_url=ctx.author.avatar.url))

    @commands.hybrid_command(name="remove", description="Elimina una canción de la cola")
    async def remove(self, ctx: commands.Context, index: int):
        in_the_same_voice_channel = await PermissionHandler.check_same_in_voice(ctx)
        if not in_the_same_voice_channel: return

        queue = self.get_queue()
        if 0 <= index < len(queue):
            element = queue.pop(index)
            await ctx.send(embed=discord.Embed(
                title=f"{element.music_requested} | eliminado de la cola ",
            ).set_author(name=f"Pedido por {ctx.author.name}", icon_url=ctx.author.avatar.url))


async def setup(bot):
    await bot.add_cog(Radio(bot))