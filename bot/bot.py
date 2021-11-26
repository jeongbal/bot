from typing import Optional
from glob import glob

from discord.ext.commands import Bot

from utils.neis import Neis


class JeongBalBot(Bot):
    def __init__(self, command_prefix: str, neis_token: str, **options) -> None:
        super().__init__(command_prefix, help_command=None, **options)
        self.neis = Neis(neis_token)

    async def close(self) -> None:
        await self.neis.close()
        await super().close()


def load_cogs(bot: JeongBalBot) -> None:
    extensions = list(
        map(
            lambda path: path.replace("./", "")
            .replace(".py", "")
            .replace("\\", ".")
            .replace("/", "."),
            filter(lambda path: "__" not in path, glob("./bot/cogs/*")),
        )
    )

    extensions.append("jishaku")
    for extension in extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(e)


def run(token: Optional[str], neis_token: Optional[str]) -> None:
    if not (token or neis_token):
        raise ValueError("Token was not found.")
    bot = JeongBalBot(command_prefix="..", neis_token=neis_token)
    load_cogs(bot)
    bot.run(token)
