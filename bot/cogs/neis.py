from typing import Optional
from discord.ext import commands
from discord.ext.commands import Cog
from discord.ext.commands.context import Context
from discord.embeds import Embed

from bot.bot import JeongBalBot


class Neis(Cog):
    def __init__(self, bot: JeongBalBot) -> None:
        self.bot = bot

    @commands.command(name="밥")
    async def bab(self, ctx: Context, date: Optional[str]) -> None:
        msg = await ctx.send(embed=Embed(title="정보를 불러오는 중.."))
        embed = await self.bot.neis.meal_embed(date)
        await msg.edit(embed=embed)


def setup(bot: JeongBalBot) -> None:
    bot.add_cog(Neis(bot))
