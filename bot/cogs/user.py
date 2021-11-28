from discord.ext import commands
from discord.ext.commands import Cog
from discord.ext.commands.context import Context

from bot.bot import JeongBalBot
from bot.utils.user import User
from bot.utils.embeds import pleaseWait


class UserCog(Cog):
    def __init__(self, bot: JeongBalBot) -> None:
        self.bot = bot
        self.user = User(self.bot.mongo)

    @commands.command(name="설정")
    async def set_class(self, ctx: Context, grade: int, class_nm: int) -> None:
        """
        학년과 반을 저장합니다. 저장 시 시간표 명령어 사용 시에 학년, 반을 입력하지 않아도 됩니다.
        인자값: `..설정 [학년](필수) [반](필수)`
        """
        msg = await ctx.send(embed=pleaseWait)
        embed = await self.user.set_class_embed(ctx.author.id, grade, class_nm)
        await msg.edit(embed=embed)


def setup(bot: JeongBalBot) -> None:
    bot.add_cog(UserCog(bot))
