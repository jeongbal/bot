from typing import Any
from discord.ext import commands
from discord.ext.commands import Cog
from discord.ext.commands.context import Context
from discord.ext.commands.errors import (
    BadArgument,
    CommandInvokeError,
    CommandNotFound,
    MissingRequiredArgument,
    TooManyArguments,
)
from neispy.error import DataNotFound

from bot.bot import JeongBalBot


class Error(Cog):
    def __init__(self, bot: JeongBalBot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: Context, error: Any) -> None:
        if isinstance(error, CommandInvokeError):
            if isinstance(error.original, DataNotFound):
                await ctx.send("해당하는 데이터를 찾지 못했습니다.", delete_after=5)
        elif isinstance(error, CommandNotFound):
            await ctx.send(
                "명령어를 찾지 못했습니다. `..help`를 입력하여 명령어 목록을 확인할 수 있습니다.", delete_after=5
            )
        elif isinstance(error, MissingRequiredArgument):
            await ctx.send(
                "인자값이 부족합니다. `..help`를 입력하여 명령어 사용법을 확인할 수 있습니다.", delete_after=5
            )
        elif isinstance(error, BadArgument):
            await ctx.send(
                "인자값이 잘못되었습니다. `..help`를 입력하여 명령어 사용법을 확인할 수 있습니다.", delete_after=5
            )
        elif isinstance(error, TooManyArguments):
            await ctx.send(
                "인자값이 너무 많습니다. `..help`를 입력하여 명령어 사용법을 확인할 수 있습니다.", delete_after=5
            )
        else:
            await ctx.send("알 수 없는 오류가 발생했습니다.", delete_after=5)
            raise error


def setup(bot: JeongBalBot):
    bot.add_cog(Error(bot))
