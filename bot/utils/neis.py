from datetime import datetime, timedelta
from typing import List, Optional
from pytz import timezone
from re import sub

from neispy import Neispy
from discord.embeds import Embed

AE = "J10"
SE = "7530119"
SEOUL = timezone("Asia/Seoul")


class Neis:
    def __init__(self, neis: Neispy) -> None:
        self.neis = neis

    async def close(self):
        await self.neis.session.close()

    @staticmethod
    def handle_date(date: Optional[str]) -> str:
        if not date:
            return datetime.now(tz=SEOUL).strftime("%Y%m%d")
        if date == "내일":
            return (datetime.now(tz=SEOUL) + timedelta(days=1)).strftime("%Y%m%d")
        elif date == "어제":
            return (datetime.now(tz=SEOUL) - timedelta(days=1)).strftime(
                "%Y%m%d"
            )  # TODO: 3.10 Switch
        return date

    async def get_meal(self, date: str) -> List[str]:
        scmeal = await self.neis.mealServiceDietInfo(AE, SE, MLSV_YMD=date)
        l = scmeal[0].DDISH_NM.split("<br/>")
        return list(map(lambda menu: sub(r"[0-9?.]", "", menu), l))

    async def get_schedule(self, date: str) -> str:
        scschedule = await self.neis.SchoolSchedule(AE, SE, AA_YMD=int(date))
        return scschedule[0].EVENT_NM

    async def get_time_table(self, grade: int, class_nm: int, date: str) -> List[str]:
        sctime_table = await self.neis.hisTimetable(
            AE, SE, TI_FROM_YMD=date, TI_TO_YMD=date, GRADE=grade, CLASS_NM=class_nm
        )
        return [info.ITRT_CNTNT for info in sctime_table]

    async def meal_embed(self, date: Optional[str]) -> Embed:
        date = self.handle_date(date)
        meal = await self.get_meal(date)
        return Embed(
            title=f"{date[4:6]}월 {date[6:9]}일 급식 정보", description=", ".join(meal)
        )

    async def schedule_embed(self, date: Optional[str]) -> Embed:
        date = self.handle_date(date)
        schedule = await self.get_schedule(date)
        return Embed(title=f"{date[4:6]}월 {date[6:9]}일 학사일정 정보", description=schedule)

    async def time_table_embed(
        self, grade: int, class_nm: int, date: Optional[str]
    ) -> Embed:
        date = self.handle_date(date)
        time_table = await self.get_time_table(grade, class_nm, date)
        return Embed(
            title=f"{date[4:6]}월 {date[6:9]}일 {grade}학년 {class_nm}반 시간표",
            description=", ".join(time_table),
        )
