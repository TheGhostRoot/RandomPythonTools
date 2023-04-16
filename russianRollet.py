import discord
from discord.ext import commands
import random

token = "token here"

bot = commands.Bot(command_prefix="r.", self_bot=False, bot=True, intents=discord.Intents.all())

players = []


@bot.event
async def on_ready():
    print(" The Bot is online!")
    await bot.change_presence(status=discord.Status.online)
    await bot.change_presence(activity=discord.Game(name="r.helpMe for the help menu"))


@bot.command()
async def helpMe(ctx):
    embed1 = discord.Embed(colour=discord.Colour.blue())
    embed1.set_author(name="Commands:")
    embed1.add_field(name=" r.join", value="you will join the game", inline=False)
    embed1.add_field(name=" r.leave", value="you will leave the game", inline=False)
    embed1.add_field(name=" r.fire", value="fires the bullet", inline=False)
    embed1.add_field(name=" r.show", value="shows the players in game", inline=False)
    await ctx.send(embed=embed1)


@bot.command()
async def show(ctx):
    global players
    for p in players:
        await ctx.send("<@" + str(p.id) + "> is in game.")


@bot.command()
async def join(ctx):
    global players
    player = ctx.author
    if player in players:
        await ctx.send("**[!]**You are already playing the Russian Roulette.")
    else:
        players.append(player)
        await ctx.send("You joined the game of Russian Roulette.")


@bot.command()
async def leave(ctx):
    global players
    player = ctx.author
    if player in players:
        players.remove(player)
        await ctx.send("<@" + str(player.id) + "> just left the game.")
    else:
        await ctx.send("**[!]**You are not in the game so you can leave it.")



@bot.command()
async def fire(ctx):
    global players
    player = ctx.author
    if player in players:
        if len(players) < 2:
            await ctx.send("You need at least one more player.")
        else:
            random1 = random.randint(1, len(players) - 1)
            index = random1 - 1
            await ctx.send("<@" + str(players.pop(index).id) + "> just got eliminated!")
            if len(players) == 1:
                for p in players:
                    players.clear()
                    await ctx.send("<@" + str(p.id) + "> is the winner!")
            else:
                for p in players:
                    await ctx.send("<@" + str(p.id) + "> is still alive")
    else:
        await ctx.send("**[!]**You are not in game so you can't play.")


bot.run(token)
