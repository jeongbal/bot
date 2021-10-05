from datetime import datetime, timezone

from discord.embeds import Embed
from discord.ext import commands
from discord.ext.commands.context import Context
from utils.bab import BabUtil
import re


class Bab(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.bab_utils = BabUtil(self.bot.neis)

    @commands.command(name="오늘", aliases=["ㅇㄴ"])
    async def today(self, ctx: Context) -> None:
        date = datetime.now(timezone.utc).astimezone().strftime("%Y%m%d")
        meal_list = await self.bab_utils.get_bab(int(date))
        l = list(map(lambda meal: re.sub(r"[0-9?.]", "", meal), meal_list))
        embed = Embed(title="오늘 급식", description=", ".join(l))
        await ctx.send(embed=embed)

    @commands.command(name="내일")
    async def tomorrow(self, ctx: Context, date: int) -> None:
        date = datetime.now(timezone.utc).astimezone().strftime("%Y%m%d")
        meal_list = await self.bab_utils.get_bab(int(date) + 1)
        l = list(map(lambda meal: re.sub(r"[0-9?.]", "", meal), meal_list))
        embed = Embed(title="내일 급식", description=", ".join(l))
        await ctx.send(embed=embed)

    @commands.command(name="급식")
    async def meal(self, ctx: Context, date: int) -> None:
        meal_list = await self.bab_utils.get_bab(int(f"2021{date}"))
        l = list(map(lambda meal: re.sub(r"[0-9?.]", "", meal), meal_list))
        embed = Embed(title="급식", description=", ".join(l))
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Bab(bot))
