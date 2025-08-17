import traceback
from typing import Callable

import discord
from discord import Client
from discord.ext import commands

class PaginationManager:
    page_size: int = 10
    @staticmethod
    async def builder[T](
            ctx: commands.Context,
            bot: Client,
            data: list[T],
            title: str,
            for_each_field_name: Callable[[T],str],
            for_each_field_value: Callable[[T],str],
            page: int = 1
    ):
        """
        Create a builder refrescable pagination
        :param ctx: commands.Context
        :param bot: The client
        :param data: The list with the data to paginate
        :param title: The title of the message
        :param for_each_field_name: The way to print each field name from the **data** list in **embed.add_field**
        :param for_each_field_value: The way to print each field value from the **data** list in **embed.add_field**
        :param page: The current page from the pagination
        :return:
        """
        page_size = PaginationManager.page_size
        total_pages = (len(data) + page_size) // page_size
        page = max(1, min(page, total_pages))
        start = (page - 1) * page_size
        end = start + page_size
        data_page = data[start:end]

        embed = discord.Embed(
            title=title,
            color=discord.Color.blurple(),
        ).set_footer(text=f"(Página {page}/{total_pages})")

        for dp in data_page:
            embed.add_field(name=for_each_field_name(dp), value=for_each_field_value(dp), inline=False)

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

                    reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
                    if str(reaction.emoji) == "➡️" and current_page < total_pages:
                        current_page += 1
                    elif str(reaction.emoji) == "⬅️" and current_page > 1:
                        current_page -= 1
                    else:
                        await message.remove_reaction(reaction, user)
                        continue

                    start = (current_page - 1) * page_size
                    end = start + page_size
                    data_page = data[start:end]

                    embed = discord.Embed(
                        title=title,
                        color=discord.Color.blurple(),
                    ).set_footer(text=f"(Página {current_page}/{total_pages})")

                    for dp in data_page:
                        embed.add_field(name=for_each_field_name(dp), value=for_each_field_value(dp), inline=False)

                    await message.edit(embed=embed)
                    await message.remove_reaction(reaction, user)
                except Exception as e:
                    await message.clear_reactions()
                    print(e)
                    traceback.print_exception(type(e), e, e.__traceback__)
                    break