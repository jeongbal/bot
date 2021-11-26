from discord.activity import Game
from discord.enums import Status
from discord.ext.commands import Cog

from bot.bot import JeongBalBot


class Ready(Cog):
    def __init__(self, bot: JeongBalBot) -> None:
        self.bot = bot

    @Cog.listener()
    async def on_ready(self) -> None:
        print("Bot is ready.")
        await self.bot.change_presence(status=Status.online, activity=Game("..help"))


def setup(bot: JeongBalBot) -> None:
    bot.add_cog(Ready(bot))
