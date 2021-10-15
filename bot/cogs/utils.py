from typing import Any

from discord.ext import commands
from discord.ext.commands.context import Context


class Utils(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command(name="따라해", aliases=["ㄸㄹㅎ", "ㄷㄹㅎ"])
    async def today(self, ctx: Context, *args) -> None:
        await ctx.send(" ".join(*args))


def setup(bot):
    bot.add_cog(Utils(bot))
