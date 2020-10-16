import discord
from discord.ext import commands, tasks
import requests
from bs4 import BeautifulSoup
import os

bot = commands.Bot(command_prefix='정발고 ')


@bot.event
async def on_ready():
    print('봇 온라인.')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('"정발고 명령어" 입력'))


@bot.command()
async def 명령어(ctx):
    embed = discord.Embed(title=':ticket: 정발고 급식봇 명령어 목록', color=0xababab)
    embed.set_thumbnail(url='http://www.jeongbal.hs.kr/upload/2018/09/04/3ae8ad2fe586c0f6449248bbab811998.jpg')
    embed.add_field(name=' - 정발고 급식 M D', value='M월 D일의 급식표를 불러옵니다.', inline=False)
    embed.add_field(name=' - 정발고 초대', value='이 봇의 초대 링크를 불러옵니다.', inline=False)
    await ctx.send(embed=embed)


@bot.command()
async def 급식(ctx, m, d):
    await ctx.send('불러오는 중...')

    req = requests.get(
        f'http://www.jeongbal.hs.kr/wah/main/schoolmeal/view.htm?menuCode=38775&domain.year=2020&domain.month={m}&domain.day={d}')
    con = req.content
    html = BeautifulSoup(con, "html.parser")


    try:
        lunchList = html.find("div", {"class": "Schoolmeal_Cont_Cont_Cont"}).text
    except:
        embed = discord.Embed(title=f':warning: 정발고 {m}월 {d}일 급식표',
                              description='불러오지 못했습니다.\n날짜가 주말이거나 급식이 나오지 않는 날인지 확인해주세요.', color=0xababab)
        embed.set_thumbnail(url='http://www.jeongbal.hs.kr/upload/2018/09/04/3ae8ad2fe586c0f6449248bbab811998.jpg')
        await ctx.send(embed=embed)
        return None
    try:
        cont2 = html.find_all("div", {"class":"Schoolmeal_Cont_Cont_2"})
        allergyList = cont2[1].text
    except:
        embed = discord.Embed(title=f':spoon: 정발고 {m}월 {d}일 급식표', description=f'{lunchList}', color=0xababab)
        embed.set_thumbnail(url='http://www.jeongbal.hs.kr/upload/2018/09/04/3ae8ad2fe586c0f6449248bbab811998.jpg')
        await ctx.send(embed=embed)
        return None

    embed = discord.Embed(title=f':spoon: 정발고 {m}월 {d}일 급식표', description=f'{lunchList}', color=0xababab)
    embed.add_field(name=':bulb: 알레르기 정보', value=allergyList, inline=True)
    embed.set_thumbnail(url='http://www.jeongbal.hs.kr/upload/2018/09/04/3ae8ad2fe586c0f6449248bbab811998.jpg')
    await ctx.send(embed=embed)

@bot.command()
async def 초대(ctx):
    await ctx.send('https://discord.com/oauth2/authorize?client_id=766501550687387659&scope=bot&permissions=2146954615')


bot.run(os.environ['token'])