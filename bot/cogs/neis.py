from typing import Optional
from discord.ext import commands
from discord.ext.commands import Cog
from discord.ext.commands.context import Context

from bot.bot import JeongBalBot
from bot.utils.neis import Neis
from bot.utils.embeds import pleaseWait


class NeisCog(Cog):
    def __init__(self, bot: JeongBalBot) -> None:
        self.bot = bot
        self.neis = Neis(self.bot.neis)

    @commands.command(name="밥")
    async def bab(self, ctx: Context, date: Optional[str]) -> None:
        msg = await ctx.send(embed=pleaseWait)
        embed = await self.neis.meal_embed(date)
        await msg.edit(embed=embed)

    @commands.command(name="학사일정")
    async def schedule(self, ctx: Context, date: Optional[str]) -> None:
        msg = await ctx.send(embed=pleaseWait)
        embed = await self.neis.schedule_embed(date)
        await msg.edit(embed=embed)

    @commands.command(name="시간표")
    async def time_table(
        self, ctx: Context, grade: int, class_nm: int, date: Optional[str]
    ) -> None:
        msg = await ctx.send(embed=pleaseWait)
        embed = await self.neis.time_table_embed(grade, class_nm, date)
        await msg.edit(embed=embed)


def setup(bot: JeongBalBot) -> None:
    bot.add_cog(NeisCog(bot))
