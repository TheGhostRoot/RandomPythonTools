import discord
from discord.ext import commands, tasks
import requests  as rq
import os
#from bs4 import BeautifulSoup

bot = commands.Bot(command_prefix='fyou',intents=discord.Intents.all())
DISCORD_TOKEN = "bot_token"
VBOX7_USERNAME = "kris22bg"
CHANNEL_ID = 

videos = dict()

@tasks.loop(seconds=10)
async def post_new_videos():
    await bot.wait_until_ready()
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
              global videos
              if os.path.exists(VBOX7_USERNAME+".txt"):
                os.remove(VBOX7_USERNAME+".txt")
              html_text = rq.get(f'https://www.vbox7.com/user:{VBOX7_USERNAME}').text
              with open(VBOX7_USERNAME+".txt", 'wt') as f:
                f.write(html_text)
                f.close()
              lines = [l for l in open(VBOX7_USERNAME+".txt", 'rt')]
              for ind, line in enumerate(lines):
                if "card video-cell " in line:
                  filtered = lines[ind+1].split('"')
                  video_title = filtered[3]
                  video_link = "https://www.vbox7.com"+filtered[1]
                  if video_title not in videos.keys():
                    videos[video_title] = video_link
                    emb = discord.Embed(colour=discord.Colour.gold())
                    emb.set_author(name=VBOX7_USERNAME+" has new video!")
                    emb.add_field(name=video_title, value=video_link)
                    emb.set_footer(text='Vbox7 '+VBOX7_USERNAME+' videos!')
                    await channel.send(embed=emb)


@bot.event
async def on_ready():
    post_new_videos.start()
    print(f'Logged in as {bot.user.name}')




bot.run(DISCORD_TOKEN)