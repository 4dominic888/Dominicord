from typing import Callable, TypeVar

import discord
from discord.ext import commands
from discord import ButtonStyle, InteractionResponse

T = TypeVar("T")

class PaginationView(discord.ui.View):
    def __init__(
        self,
        ctx: commands.Context,
        data: list[T],
        title: str,
        for_each_field_name: Callable[[T], str],
        for_each_field_value: Callable[[T], str],
        page_size: int = 10,
        start_page: int = 1
    ):
        super().__init__(timeout=60)
        self.ctx = ctx
        self.data = data
        self.title = title
        self.for_each_field_name = for_each_field_name
        self.for_each_field_value = for_each_field_value
        self.page_size = page_size
        self.total_pages = max(1, (len(data) + page_size - 1) // page_size)
        self.current_page = max(1, min(start_page, self.total_pages))

        self.update_buttons()

    def build_embed(self) -> discord.Embed:
        start = (self.current_page - 1) * self.page_size
        end = start + self.page_size
        data_page = self.data[start:end]

        embed = discord.Embed(
            title=self.title,
            color=discord.Color.blurple()
        )
        embed.set_footer(text=f"(Página {self.current_page}/{self.total_pages})")

        for dp in data_page:
            embed.add_field(
                name=self.for_each_field_name(dp),
                value=self.for_each_field_value(dp),
                inline=False
            )

        return embed

    def update_buttons(self):
        self.previous_page.disabled = (self.current_page <= 1)
        self.next_page.disabled = (self.current_page >= self.total_pages)

    async def update_message(self, interaction: discord.Interaction):
        response: InteractionResponse = interaction.response
        self.update_buttons()
        await response.edit_message(embed=self.build_embed(), view=self)

    @discord.ui.button(label="⬅️", style=ButtonStyle.primary)
    async def previous_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page > 1:
            self.current_page -= 1
            await self.update_message(interaction)

    @discord.ui.button(label="➡️", style=ButtonStyle.primary)
    async def next_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page < self.total_pages:
            self.current_page += 1
            await self.update_message(interaction)

class PaginationManager:
    page_size: int = 10
    @staticmethod
    async def builder[T](
            ctx: commands.Context,
            data: list[T],
            title: str,
            for_each_field_name: Callable[[T],str],
            for_each_field_value: Callable[[T],str],
            page: int = 1
    ):
        """
        Create a builder refrescable pagination
        :param ctx: commands.Context
        :param data: The list with the data to paginate
        :param title: The title of the message
        :param for_each_field_name: The way to print each field name from the **data** list in **embed.add_field**
        :param for_each_field_value: The way to print each field value from the **data** list in **embed.add_field**
        :param page: The current page from the pagination
        :return:
        """

        view = PaginationView(
            ctx,
            data,
            title,
            for_each_field_name,
            for_each_field_value,
            page_size=PaginationManager.page_size,
            start_page=page
        )

        embed = view.build_embed()
        await ctx.send(embed=embed, view=view)