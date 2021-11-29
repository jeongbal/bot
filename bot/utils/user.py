from discord.embeds import Embed
from bot.utils.database.mongo import Mongo


class User:
    def __init__(self, mongo: Mongo) -> None:
        self.mongo = mongo

    async def set_class_embed(self, user_id: int, grade: int, class_nm: int) -> Embed:
        if await self.mongo.get_user(user_id):
            await self.mongo.set_user(user_id, grade, class_nm)
        else:
            await self.mongo.initialize_user(user_id, grade, class_nm)
        return Embed(title="반 정보 저장 완료")
