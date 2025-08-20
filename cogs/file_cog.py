import discord
from discord.ext import commands
from utils.enums.allow_extension_type import FileType
from utils.file_manager import FileManager

class FileCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_group(name="create")
    async def create(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Usa un subcomando válido")

    @create.command(name="playlist", description="Crea una playlist (una carpeta para almacenar música)")
    async def create_playlist(self, ctx: commands.Context, nombre: str):
        created = await FileManager.create_folder(ctx, nombre, omit_message=True)
        if created:
            await ctx.send(embed=discord.Embed(
                title="Vuenaaaa",
                description="La playlist ha sido creada, EMPIEZA A METER ROLAS",
                color=discord.Color.green()
            ))

    @commands.hybrid_command(name="upload", description="Sube una canción a una playlist")
    async def upload_playlist(self, ctx: commands.Context, file: discord.Attachment, playlist: str):
        created = await FileManager.save_file(ctx, file, folder=playlist, file_type=FileType.AUDIO, omit_message=True)
        if created:
            await ctx.send(embed=discord.Embed(
                title="Rola subida",
                description=f"Tal parece que tenemos un `{file.filename}` en la playlist `{playlist}`. Radical No?",
            ))

async def setup(bot):
    await bot.add_cog(FileCog(bot))