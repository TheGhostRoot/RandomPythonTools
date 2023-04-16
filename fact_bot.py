import discord
import random
import requests
import json
from discord.ext import tasks, commands

bot = commands.Bot(command_prefix='!!', bot=True, self_bot=False, intents=discord.Intents.all())
TOKEN = 'token here'
FACT_API_URL = 'https://uselessfacts.jsph.pl/random.json?language=en'

subscribed_users = set()

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name='!!help, !!sub, !!unsub'))
    send_random_fact.start()
    print('Online')

# hours=24 seconds=10
@tasks.loop(hours=24)
async def send_random_fact():
    for user_id in subscribed_users:
        fact_categories = ['animal', 'career', 'celebrity', 'dev', 'explicit', 'fashion', 'food', 'history', 'money', 'movie', 'music', 'political', 'religion', 'science', 'sport', 'travel']
        fact_topic = random.choice(fact_categories)
        fact_url = FACT_API_URL + '&category=' + fact_topic
        fact_data = requests.get(fact_url).json()
        fact_text = fact_data['text']
        user = await bot.fetch_user(user_id)
        await user.send(f'Here\'s your random fact about **{fact_topic}**: **{fact_text}**')



@bot.command()
async def sub(ctx):
    subscribed_users.add(ctx.message.author.id)
    await ctx.send('You have been subscribed to receive a daily random fact. To unsubscribe, type !unsub.')



@bot.command()
async def unsub(ctx):
    subscribed_users.remove(ctx.message.author.id)
    await ctx.send('You have been unsubscribed from daily random facts.')





bot.run(TOKEN)
