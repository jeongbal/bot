from typing import Dict, Optional
from motor.motor_asyncio import AsyncIOMotorClient


class Mongo:
    def __init__(self, mongo_url: str) -> None:
        self.__client = AsyncIOMotorClient(mongo_url)
        self.__user_class = self.__client.jbot.user_class

    def close(self) -> None:
        self.__client.close()

    async def get_user(self, user_id: int) -> Optional[Dict[str, int]]:
        return self.__user_class.find_one({"user_id": user_id})

    async def set_user(self, user_id: int, grade: int, class_nm: int) -> bool:
        if await self.get_user(user_id):
            await self.__user_class.update_one(
                {"user_id": user_id}, {"$set": {"grade": grade, "class_nm": class_nm}}
            )
            return True
        await self.__user_class.insert_one(
            {"user_id": user_id, "grade": grade, "class_nm": class_nm}
        )
        return False
