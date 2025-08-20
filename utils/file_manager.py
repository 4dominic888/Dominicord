import os
import re

import discord
from discord.ext import commands

from constant import MUSIC_ALLOWED_EXTENSIONS, MUSIC_MAX_FILE_SIZE, PLAYLIST_FOLDER
from utils.enums.allow_extension_type import FileType

class FileManager:
    @staticmethod
    async def _validate_extension(ctx: commands.Context, filename: str, file_type: FileType) -> bool:
        """
        Validates that the extension of the given file matches the allowed extensions.
        :param ctx:
        :param filename: discord attachment filename
        :param file_type: file type
        :return: True if the extension of the given file matches the allowed extensions, False otherwise.
        """
        allowed_extensions: set[str] = []
        match file_type:
            case (FileType.AUDIO): allowed_extensions = MUSIC_ALLOWED_EXTENSIONS
            case (FileType.VIDEO): raise Exception("Module not implemented")

        _, ext = os.path.splitext(filename)
        if ext.lower() not in allowed_extensions:
            await ctx.send(embed=discord.Embed(
                title="WRONG",
                description=f"❌ Solo se permiten archivos con extensiones: {', '.join(allowed_extensions)}",
            ))
            return False
        return True

    @staticmethod
    async def _validate_size(ctx: commands.Context, file_size: int, file_type: FileType) -> bool:
        """
        Validates that the size of the given file matches the allowed file size.
        :param ctx:
        :param file_size: file size
        :param file_type: file type
        :return: True if the size of the given file matches the allowed file size, False otherwise.
        """
        max_file_size: int = 0
        match file_type:
            case (FileType.AUDIO): max_file_size = MUSIC_MAX_FILE_SIZE
            case (FileType.VIDEO): raise Exception("Module not implemented")

        if file_size > MUSIC_MAX_FILE_SIZE:
            await ctx.send(embed=discord.Embed(
                title="WRONG",
                description=f"❌ El archivo excede el límite de {max_file_size // (1024*1024)} MB."
            ))
            return False
        return True

    @staticmethod
    def _sanitize_name(ctx:commands.Context, filename: str) -> str:
        """
        Sanitizes the given filename or folder name.
        :param filename:
        :return: sanitized filename or folder name
        """
        base = os.path.basename(filename)
        name, ext = os.path.splitext(base)
        ext = ext.lower()

        # TODO, debe primero ir el match xdd
        if ext not in MUSIC_ALLOWED_EXTENSIONS:
            ctx.send(embed=discord.Embed(
                title="WRONG",
                description=f"Extensión no permitida: {ext}",
                color=discord.Color.red()
            ))

        name = re.sub(r"\.{2,}", ".", name)
        name = re.sub(r"[^A-Za-z0-9._-]", "_", name)
        name = name.strip(" .")
        if not name:
            name = "archivo"

        return f"{name}{ext}"

    @staticmethod
    def _existing_folder(folder_name: str) -> bool:
        """
        Checks if the given folder name already exists.
        :param folder_name:
        :return: True if the folder name already exists, False otherwise.
        """
        if os.path.isdir(os.path.join(PLAYLIST_FOLDER, folder_name)):
            return True
        return False

    @staticmethod
    async def create_folder(ctx: commands.Context, folder_name: str, omit_message: bool = True) -> bool:
        """
        Creates the given folder name.
        :param ctx:
        :param folder_name: The name of the folder
        :param omit_message: omit warning message
        :return: True if the folder name was successfully created, False otherwise.
        """
        sanitazed_folder_name = FileManager._sanitize_name(ctx, folder_name)

        if any(c in sanitazed_folder_name for c in r'\/:*?"<>|..'):
            await ctx.send(embed=discord.Embed(
                title="Error",
                description="No te pases de listo causa, este nombre tiene algunos caracteres feos"
            ))
            return False

        path = os.path.join(PLAYLIST_FOLDER, sanitazed_folder_name)

        try:
            os.makedirs(path, exist_ok=True)
            if not omit_message:
                await ctx.send(f"📁 Carpeta creada (o ya existente): `{sanitazed_folder_name}`")
            return True
        except Exception as e:
            await ctx.send(f"⚠️ No se pudo crear la carpeta: {e}")
            return False

    @staticmethod
    async def save_file(ctx: commands.Context, file: discord.Attachment, folder: str, file_type: FileType, omit_message: bool = True) -> bool:
        """
        Saves a discord attachment in the given folder.
        :param ctx:
        :param file: discord attachment file
        :param folder: folder name to save
        :param file_type: file type
        :param omit_message: omit warning message
        :return: True if the file was successfully saved, False otherwise.
        """
        if not await FileManager._validate_extension(ctx, file.filename, file_type): return False
        if not await FileManager._validate_size(ctx, file.size, file_type): return False
        foldername = FileManager._sanitize_name(ctx, folder)
        if not FileManager._existing_folder(foldername): return False

        filename = FileManager._sanitize_name(ctx, file.filename)

        dir_path: str = ""
        match file_type:
            case (FileType.AUDIO): dir_path = PLAYLIST_FOLDER
            case (FileType.VIDEO): raise Exception("Module not implemented")

        file_path = os.path.join(dir_path, foldername, filename)

        if os.path.exists(file_path):
            await ctx.send(embed=discord.Embed(
                title="Error",
                description=f"Rola `{file.filename}` ya existe w.",
                color=discord.Color.red()
            ))
            return False

        await file.save(file_path)

        if not omit_message:
            await ctx.send(embed=discord.Embed(
                title="NICE",
                description=f"✅ Archivo `{filename}` subido con éxito y guardado en `{foldername}/`",
                color=discord.Color.green()
            ))

        return True