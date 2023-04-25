import discord
from discord.ext import commands, tasks
import requests  as rq
import os

bot = commands.Bot(command_prefix='!!!!!!',intents=discord.Intents.all())
DISCORD_TOKEN = "discord_token"
VBOX7_USERNAME = "animebulgariansubs"
CHANNEL_ID = None

# USERNAME: {"videos": {"Title": "link"}, "total_pages": NUMBER}, USERNAME: {}
users = dict()

async def send_videos():
  global users
  channel = bot.get_channel(CHANNEL_ID)
  if channel:
    all_vids = get_all_videos()
    for name in get_files():
        for video_title, video_link in all_vids[name].items():
            emb = discord.Embed(colour=discord.Colour.gold())
            emb.set_author(name=VBOX7_USERNAME+" has new video!")
            emb.add_field(name=video_title, value=video_link)
            emb.set_footer(text='Vbox7 '+VBOX7_USERNAME+' videos!')
            await channel.send(embed=emb)

def get_files():
  return [f"{VBOX7_USERNAME}-page{page}.txt" for page in range(users[VBOX7_USERNAME]['total_pages'] + 1, 0, -1)]

def get_all_videos():
    global users
    videos_per_page = dict()
    all_videos = {}
    for name in get_files():
      all_lines = [one_line.replace("\n", "") for one_line in open(name, 'rt')]
      videos_per_page[name] = []
      for ind, lines in enumerate(all_lines):
        if "card video-cell " in lines:
          filtered = all_lines[ind+1].split('"')
          video_title = filtered[3]
          video_link = "https://www.vbox7.com"+filtered[1]
          if 'videos' not in users[VBOX7_USERNAME].keys():
            users[VBOX7_USERNAME]['videos'] = {}
          if video_title not in users[VBOX7_USERNAME]['videos'].keys():
            users[VBOX7_USERNAME]["videos"][video_title] = video_link
            all_videos[video_title] = video_link
            videos_per_page[name].append(video_title)
      videos_per_page[name].reverse()
    # "NAME" : {"TITLE": "LINK", "TITLE2": "LINK2"}, "NAME2": ...
    final_videos = {}
    for n, list_of_titles in videos_per_page.items():
      final_videos[n] = {}
      for title1 in list_of_titles:
        final_videos[n][title1] = all_videos[title1]
    return final_videos
      
    

def save_videos_from_page(page):
  if os.path.exists(VBOX7_USERNAME+f"-page{page}.txt"):
    os.remove(VBOX7_USERNAME+f"-page{page}.txt")
  html_text = rq.get(f'https://www.vbox7.com/user:{VBOX7_USERNAME}?page={page}').text
  with open(VBOX7_USERNAME+f"-page{page}.txt", 'wt') as f:
    f.write(html_text)
    f.close()

@tasks.loop(seconds=10)
async def get_new_videos():
    await bot.wait_until_ready()
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        global users
        if VBOX7_USERNAME not in users.keys():
          users[VBOX7_USERNAME] = {}
        print('Saving html of page 1')
        save_videos_from_page(1)
        lines = [l for l in open(VBOX7_USERNAME+"-page1.txt", 'rt')]
        links = set()
        for ind, line in enumerate(lines):
          if "page-item" in line:
            for p in line.split('"'):
              if p.startswith('https://'):
                links.add(p)
        users[VBOX7_USERNAME]['total_pages'] = len(links)
        for l in links:
          print('Saving html of page', l[-1])
          save_videos_from_page(l[-1])
          
        print('Sending videos')
        await send_videos()

@bot.command()
async def selchannel(ctx, channel: discord.TextChannel = None):
    if not channel:
        await ctx.send("You need to provide the channel where you want to receive notifications! Please use the following command: `!selchannel #channel`.")
        return
    global CHANNEL_ID
    try:
      if str(channel.type) != "text":
          await ctx.send("Sorry, but this command only works with text channels, not voice channels or categories.")
          return
      CHANNEL_ID = channel.id
    except Exception:
      pass
    else:
      await ctx.send(f"Notify Channel selected: {channel.mention}.")
    
  


@bot.event
async def on_ready():
    # !!!!!!selchannel
    get_new_videos.start()
    print(f'Logged in as {bot.user.name}')


#MTA5OTgyMjI0NDcxNDI1MDMxMw.G-iBP8.KX2UaEDKDBORSbLWrdxx4NeNRva4W0JsZJBZSc

bot.run(DISCORD_TOKEN)