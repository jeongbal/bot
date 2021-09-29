from neispy import Client


AE = "J10"
SE = "7530119"


class BabUtil:
    def __init__(self, neis: Client) -> None:
        self.neis = neis

    async def get_bab(self, date: int) -> list:
        meal = await self.neis.mealServiceDietInfo(AE, SE, MLSV_YMD=date)
        return meal[0].DDISH_NM.split("<br/>")
