from discord.ext import commands
from discord.ext.commands import Cog
from discord.ext.commands import Context
from discord.utils import oauth_url
from discord.embeds import Embed
from discord.permissions import Permissions

from bot.bot import JeongBalBot
from bot.utils.embeds import pleaseWait


class General(Cog):
    def __init__(self, bot: JeongBalBot) -> None:
        self.bot = bot

    @commands.command(name="초대")
    async def invite(self, ctx: Context) -> None:
        """
        정발고 봇의 초대 링크를 보여줍니다.
        인자값: `..초대`
        """
        url = oauth_url(self.bot.user.id, permissions=Permissions.administrator)
        await ctx.send(embed=Embed(title="정발고 봇 초대 링크", url=url))

    @commands.command(name="help")
    async def help(self, ctx: Context) -> None:
        msg = await ctx.send(embed=pleaseWait)
        embed = Embed(title="명령어 목록")
        command_list = [
            command
            for command in self.bot.commands
            if command.name not in ["jishaku", "help"]
        ]
        for command in command_list:
            embed.add_field(name=command.name, value=command.help, inline=False)
        await msg.edit(embed=embed)


def setup(bot: JeongBalBot) -> None:
    bot.add_cog(General(bot))
