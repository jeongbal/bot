from os import getenv

from bot.bot import run

run(getenv("token"), getenv("neis"), getenv("mongo"))
