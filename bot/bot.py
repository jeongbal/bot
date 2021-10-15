from discord.ext.commands.bot import Bot
from neispy.client import Client


class BBot(Bot):
    cwd: str
    neis: Client
