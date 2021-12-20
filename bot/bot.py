from glob import glob

from discord.ext.commands import Bot
from neispy import Neispy

from bot.utils.database.mongo import Mongo


class JeongBalBot(Bot):
    def __init__(
        self, command_prefix: str, neis_token: str, mongo_url: str, **options
    ) -> None:
        super().__init__(command_prefix, help_command=None, **options)
        self.neis = Neispy(KEY=neis_token)
        self.mongo = Mongo(mongo_url)

    async def close(self) -> None:
        self.mongo.close()
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


def run(token: str, neis_token: str, mongo_url: str) -> None:
    bot = JeongBalBot(command_prefix="..", neis_token=neis_token, mongo_url=mongo_url)
    load_cogs(bot)
    bot.run(token)
