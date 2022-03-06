from typing import Optional
from discord.ext import commands
from discord.ext.commands import Cog
from discord.ext.commands.context import Context
from discord.message import Message
from neispy.error import DataNotFound

from bot.bot import JeongBalBot
from bot.utils.neis import Neis
from bot.utils.embeds import pleaseWait
from bot.utils.user import User


class NeisCog(Cog):
    def __init__(self, bot: JeongBalBot) -> None:
        self.bot = bot
        self.neis = Neis(self.bot.neis)
        self.user = User(self.bot.mongo)

    @commands.Cog.listener("on_message")
    async def onMessageEvent(self, message: Message):
        if message.content in ["밥", "ㅂ"]:
            msg = await message.channel.send(embed=pleaseWait)
            try:
                embed = await self.neis.meal_embed(None)
            except DataNotFound:
                return await message.channel.send("해당하는 데이터를 찾지 못했습니다.", delete_after=5)
            await msg.edit(embed=embed)

    @commands.command(name="밥")
    async def bab(self, ctx: Context, date: Optional[str]) -> None:
        """
        해당 날짜의 급식 정보를 보여줍니다.
        인자값: `..밥 [어제/오늘/내일/20211229](선택)`
        """
        msg = await ctx.send(embed=pleaseWait)
        embed = await self.neis.meal_embed(date)
        await msg.edit(embed=embed)

    @commands.command(name="학사일정")
    async def schedule(self, ctx: Context, date: Optional[str]) -> None:
        """
        해당 날짜의 학사일정을 보여줍니다.
        인자값: `..학사일정 [어제/오늘/내일/20211229](선택)`
        """
        msg = await ctx.send(embed=pleaseWait)
        embed = await self.neis.schedule_embed(date)
        await msg.edit(embed=embed)

    @commands.command(name="시간표")
    async def time_table(
        self,
        ctx: Context,
        grade: Optional[int],
        class_nm: Optional[int],
        date: Optional[str],
    ) -> None:
        """
        해당 날짜의 시간표를 보여줍니다.
        인자값: `..학사일정 [학년](필수) [반](필수) [어제/오늘/내일/20211229](선택)`
        """
        msg = await ctx.send(embed=pleaseWait)
        if (grade is None) == (class_nm is None):
            user_data = await self.user.get_user_class(ctx.author.id)
        elif (grade is None) != (class_nm is None):
            await ctx.send(
                "인자값이 부족합니다. `..help`를 입력하여 명령어 사용법을 확인할 수 있습니다.", delete_after=5
            )
            return
        embed = await self.neis.time_table_embed(
            user_data["grade"], user_data["class_nm"], date
        )
        await msg.edit(embed=embed)


def setup(bot: JeongBalBot) -> None:
    bot.add_cog(NeisCog(bot))
