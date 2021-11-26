from datetime import datetime, timedelta
from typing import List, Optional
from pytz import timezone

from neispy import Neispy
from discord.embeds import Embed

AE = "J10"
SE = "7530119"
SEOUL = timezone("Asia/Seoul")


class Neis(Neispy):
    def __init__(self, key: Optional[str]) -> None:
        super().__init__(self, key=key)

    async def close(self):
        await self.session.close()

    async def get_meal(self, date: str) -> List[str]:
        scmeal = await self.mealServiceDietInfo(AE, SE, MLSV_YMD=date)
        return scmeal[0].DDISM_NM.split("<br/>")

    async def get_schedule(self, date: str) -> str:
        scschedule = await self.SchoolSchedule(AE, SE, AA_YMD=int(date))
        return scschedule[0].EVENT_NM

    async def get_time_table(self, grade: int, class_nm: int, date: str) -> List[str]:
        sctime_table = await self.hisTimetable(
            AE, SE, TI_FROM_YMD=date, TI_TO_YMD=date, GRADE=grade, CLASS_NM=class_nm
        )
        return [info["ITRT_CNTNT"] for info in sctime_table["hisTimetable"][1]["row"]]

    async def meal_embed(self, date: Optional[str]) -> Embed:
        if not date:
            date = datetime.now(tz=SEOUL).strftime("%Y%m%d")

        if date == "내일":
            date = (datetime.now(tz=SEOUL) + timedelta(days=1)).strftime("%Y%m%d")

        meal = await self.get_meal(date)
        return Embed(
            title=f"{date[4:6]}월 {date[6:9]}일 급식 정보", description=", ".join(meal)
        )
