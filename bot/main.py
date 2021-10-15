import discord
import os
from pathlib import Path
from discord.ext.commands.bot import Bot
from neispy.client import Client


token = os.getenv("token")
bot = Bot(command_prefix="밥 ")
cwd = Path(__file__).parents[0]
cwd = str(cwd)
bot.cwd = cwd
bot.neis = Client(KEY=os.getenv("neis"))


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("밥"))


if __name__ == "__main__":
    for file in os.listdir(os.path.join(cwd, "cogs")):
        if file.endswith(".py") and not file.startswith("_"):
            bot.load_extension(f"cogs.{file[:-3]}")
    bot.load_extension("jishaku")
    bot.run(token)
